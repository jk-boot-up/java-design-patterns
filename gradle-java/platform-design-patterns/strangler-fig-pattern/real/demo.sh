#!/usr/bin/env bash
#
# Tier 2: the strangler's router as a real nginx, in front of two real services.
#
# Everything this script prints is real output from three running containers. Never
# hand-edit the transcript in README.md: run this and paste what came back.
#
#   ./demo.sh
#
# Requires: a JDK 21, Docker, and a network the first time (Docker pulls a JRE and nginx).
# Tier 1 needs neither.

set -euo pipefail
cd "$(dirname "$0")"

ROUTER=http://localhost:18082

say()  { printf '\n\033[1m%s\033[0m\n' "$*"; }
rule() { printf '========================================================================\n'; }

cleanup() { docker compose down --remove-orphans >/dev/null 2>&1 || true; rm -rf nginx/live; }
trap cleanup EXIT

use_routes() {            # $1 = legacy | shadow | fresh
  mkdir -p nginx/live
  cp "nginx/routes-$1.conf" nginx/live/routes.conf
  docker exec strangler-demo-router nginx -s reload >/dev/null 2>&1
  sleep 1
}

price() {                 # $1 = order id, $2 = subtotal in pence
  curl -si "$ROUTER/api/orders/price?id=$1&subtotal=$2" | tr -d '\r' | awk -F': ' 'tolower($1)=="x-served-by"{by=$2} /^total=/{body=$0} END{print "    " body "   (X-Served-By: " by ")"}'
}

stats() { docker exec "$1" wget -qO- http://localhost:8080/stats; }

started_at() { docker inspect -f '{{.State.StartedAt}}' "$1"; }

say "Compiling Tier 1 and starting three containers"
../gradlew --quiet -p .. classes
rm -rf build/classes && mkdir -p build/classes
javac -d build/classes $(find ../src/main/java -name '*.java') service/ServiceMain.java
mkdir -p nginx/live && cp nginx/routes-legacy.conf nginx/live/routes.conf
docker compose up --build -d >/dev/null 2>&1
for _ in $(seq 1 60); do curl -sf "$ROUTER/api/orders/stock" >/dev/null 2>&1 && break; sleep 1; done
ROUTER_STARTED=$(started_at strangler-demo-router)
LEGACY_STARTED=$(started_at strangler-demo-legacy)
FRESH_STARTED=$(started_at strangler-demo-fresh)


rule
say "Act 1 — every route starts on legacy"
rule
echo "  a price for an order of exactly fifty pounds, and one of forty:"
price 1 5000
price 2 4000
echo "  stock, which will never move in this demo:"
curl -si "$ROUTER/api/orders/stock" | tr -d '\r' | awk -F': ' 'tolower($1)=="x-served-by"{print "    served by " $2}'


rule
say "Act 2 — shadow: legacy serves, and the new service receives a copy"
rule
use_routes shadow
before_fresh=$(stats strangler-demo-fresh)
echo "  the new service before: $before_fresh"
price 3 5000
sleep 1
echo "  the new service after:  $(stats strangler-demo-fresh)"
echo "  what each service computed for order 3, from its own log:"
docker logs strangler-demo-legacy 2>&1 | grep "price id=3" | sed 's/^/    legacy: /'
docker logs strangler-demo-fresh  2>&1 | grep "price id=3" | sed 's/^/    fresh:  /'
cat <<'EOF'

  The customer got legacy's answer. The new service was called as well, and the two
  disagree: at exactly fifty pounds legacy charges delivery and the rewrite does not.
  That is the difference Tier 1's shadow reads found, found here on real requests.
EOF


rule
say "Act 3 — move pricing: a config edit and a reload, with no restart"
rule
use_routes fresh
price 4 5000
echo "  the same order, now served by the new service."
echo "  did anything restart?"
echo "    router:  $([ "$ROUTER_STARTED" = "$(started_at strangler-demo-router)" ] && echo "no, started $ROUTER_STARTED" || echo YES)"
echo "    legacy:  $([ "$LEGACY_STARTED" = "$(started_at strangler-demo-legacy)" ] && echo "no, started $LEGACY_STARTED" || echo YES)"
echo "    fresh:   $([ "$FRESH_STARTED" = "$(started_at strangler-demo-fresh)" ] && echo "no, started $FRESH_STARTED" || echo YES)"


rule
say "Act 4 — roll pricing back, and nothing else moves"
rule
use_routes legacy
price 5 5000
echo "  stock was on legacy the whole time:"
curl -si "$ROUTER/api/orders/stock" | tr -d '\r' | awk -F': ' 'tolower($1)=="x-served-by"{print "    served by " $2}'
cat <<'EOF'

  One file, one reload. Pricing came back, stock never moved, and no service was
  restarted. That is what a switch per capability is worth.
EOF

say "Stopping the containers"
