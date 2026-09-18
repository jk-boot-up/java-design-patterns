#!/usr/bin/env bash
#
# The Tier 2 walkthrough, start to finish, unattended.
#
# Everything this script prints is real output from running containers. That
# matters more than it sounds: the standing rule across this repository is that
# every number quoted in a README is captured output rather than something
# written from memory, and for Tier 2 that means the transcript in
# real/README.md is produced by running this file and pasting what came back.
# Never hand-edit a transcript.
#
#   ./demo.sh
#
# Requires: a JDK 21, Docker, and a network connection the first time (Gradle
# has to fetch Spring and Docker has to pull nginx and a JRE). Tier 1 needs none
# of it. That asymmetry is the whole reason the two tiers are separate builds.
#
# One warning about the figures. Unlike Tier 1, this demo has a real network, a
# real TLS handshake and a real JVM in the path, so the arrival times move by a
# few milliseconds from run to run. The shape is what is being shown: three
# attempts inside a handful of milliseconds under one proxy, and three attempts
# spread across roughly six hundred under the other.

set -euo pipefail
cd "$(dirname "$0")"

GRADLE=../gradlew          # the wrapper one directory up; Gradle takes its
                           # project directory from the working directory, so
                           # this builds *this* build and the repository is
                           # spared a second copy of the wrapper jar.
CERTS=build/certs
PROVIDER=https://localhost:19443
CHECKOUT=http://localhost:18080

cleanup() {
  docker compose down --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

say() {
  printf '\n\033[1m%s\033[0m\n' "$*"
}

rule() {
  printf '========================================================================\n'
}

wait_for() {
  local url=$1 name=$2 tries=90
  printf '  waiting for %s' "$name"
  until curl -sfk "$url" >/dev/null 2>&1; do
    tries=$((tries - 1))
    if [ "$tries" -le 0 ]; then
      printf ' — gave up\n'
      docker compose logs --tail 40 >&2
      exit 1
    fi
    printf '.'
    sleep 1
  done
  printf ' up\n'
}

# Ask the provider what it actually saw, and when. This is the only ledger in
# the demo that a proxy cannot influence: a proxy claiming to have waited is a
# claim, and arrival times measured at the far end are what happened.
attempts() {
  curl -sk "$PROVIDER/attempts" | python3 -m json.tool
}

# The one line that matters, pulled out of that ledger: when each attempt
# landed, and how far apart the first and the last were.
arrivals() {
  curl -sk "$PROVIDER/attempts" | python3 -c '
import json, sys
seen = json.load(sys.stdin)
for a in seen["arrivals"]:
    print("    attempt at %6dms   %s" % (a["atMillis"], a["outcome"]))
print("    %d attempts, first to last: %dms"
      % (seen["total"], seen["firstToLastMillis"]))
'
}

reset() {
  curl -sk -X POST "$PROVIDER/reset" \
       -H 'Content-Type: application/json' -d "$1" >/dev/null
}

pay() {
  # $1 is the payment reference, $2 the amount in pence.
  curl -s -X POST "$CHECKOUT/pay" -H 'Content-Type: application/json' \
       -d "{\"reference\":\"$1\",\"amountPence\":$2}" | python3 -m json.tool
}

bound_to_the_port() {
  # Which proxy container is running. Nothing asks checkout, because checkout
  # has no way to answer.
  if docker ps --format '{{.Names}}' | grep -q '^sidecar-java-proxy-java$'; then
    echo "java-proxy"
  elif docker ps --format '{{.Names}}' | grep -q '^sidecar-java-proxy-nginx$'; then
    echo "nginx"
  else
    echo "nothing"
  fi
}

started_at() {
  docker inspect -f '{{.State.StartedAt}}' "$1"
}


# ---------------------------------------------------------------------------
say "Building the two services and the proxy"
# ---------------------------------------------------------------------------
"$GRADLE" --quiet bootJar jar

mkdir -p "$CERTS"
if [ ! -f "$CERTS/gateway.p12" ]; then
  echo "  generating the provider's certificate"
  keytool -genkeypair \
    -alias gateway -keyalg RSA -keysize 2048 -validity 365 \
    -dname "CN=gateway, OU=payments, O=provider, C=GB" \
    -storetype PKCS12 -keystore "$CERTS/gateway.p12" -storepass changeit \
    -ext "SAN=dns:gateway,dns:localhost" >/dev/null
fi

docker compose build >/dev/null 2>&1
# Only the nginx proxy is started. The Java one is built and waiting, and Act 4
# is what puts it on the port.
docker compose up -d gateway checkout sidecar-nginx >/dev/null 2>&1
wait_for "$PROVIDER/attempts" "the payment provider"
wait_for "$CHECKOUT/about" "checkout"
sleep 2

# One throwaway payment, before any act, so that the first TLS handshake and the
# first class-loading are not inside a measured window. Both proxies get this
# treatment, and neither act below is the first request its proxy has made.
warm_up() {
  reset '{"unwellForMillis":0,"allowance":99}' >/dev/null
  curl -s -o /dev/null -X POST "$CHECKOUT/pay" -H 'Content-Type: application/json' \
       -d '{"reference":"WARM-UP","amountPence":1}' || true
  sleep 1
}
warm_up

CHECKOUT_STARTED_AT=$(started_at sidecar-java-proxy-checkout)


rule
say "Act 1 — what checkout knows, and what is on the port"
rule
echo "  checkout describes itself:"
curl -s "$CHECKOUT/about" | python3 -m json.tool | sed 's/^/    /'
echo
printf '  currently bound to localhost:8081:  %s\n' "$(bound_to_the_port)"
cat <<'EOF'

  One address, on its own machine. Not a provider hostname, not a
  certificate, not a retry count — and nothing in that description says
  which of the two proxies in this directory is answering.
EOF


rule
say "Act 2 — the wobble, under a proxy that cannot wait"
rule
echo "  the provider will decline everything for its first 600 milliseconds."
reset '{"unwellForMillis":600,"allowance":12}'
pay "ORD-4418" 4799 | sed 's/^/    /'
echo
echo "  what the provider itself recorded, at its own end:"
arrivals
echo
echo "  and what checkout's nginx proxy logged, one line per attempt:"
docker exec sidecar-java-proxy-nginx cat /var/log/nginx/attempts.log \
  | tail -n 3 | sed 's/^/    /'
cat <<'EOF'

  Three attempts, all of them inside the bad window, because all of them
  were made inside the bad window. The whole allowance for that payment was
  spent before the provider had time to get better.
EOF


rule
say "Act 3 — the sentence there is nowhere to write"
rule
cat <<'EOF'
  This is what the proxy is actually running, with the comments stripped:

EOF
docker exec sidecar-java-proxy-nginx \
  sh -c "grep -v '^\s*#' /etc/nginx/conf.d/default.conf | grep -v '^\s*$'" \
  | sed 's/^/    /'
cat <<'EOF'
  The provider's address appears three times in the upstream group, because
  three entries is how "up to three attempts" is spelled when there is one
  address to talk to. Moving to the next entry happens immediately, and
  there is no directive in nginx's http proxy module that expresses a wait.

  Nobody wrote a bug. The sentence is not in the language.
EOF


rule
say "Act 4 — the swap"
rule
echo "  stopping nginx and starting the Java proxy on the same port."
docker compose stop sidecar-nginx >/dev/null 2>&1
docker compose up -d sidecar-java >/dev/null 2>&1
sleep 3
warm_up
printf '  now bound to localhost:8081:  %s\n' "$(bound_to_the_port)"
echo
echo "  checkout, which was not part of any of that:"
curl -s "$CHECKOUT/about" | python3 -m json.tool | sed 's/^/    /'
printf '\n    checkout started at %s\n' "$CHECKOUT_STARTED_AT"
printf '    checkout now says   %s\n' "$(started_at sidecar-java-proxy-checkout)"
cat <<'EOF'

  Same container, same start time, same one-line configuration. No jar was
  rebuilt, no service was restarted, and there is no notification step in
  this script because there is nothing to notify.
EOF


rule
say "Act 5 — the same wobble, the same three attempts"
rule
echo "  identical provider, identical 600ms wobble, identical payment."
reset '{"unwellForMillis":600,"allowance":12}'
pay "ORD-4418" 4799 | sed 's/^/    /'
echo
echo "  what the provider itself recorded:"
arrivals
echo
echo "  the provider's full ledger, including the transport it saw:"
attempts | sed 's/^/    /'
cat <<'EOF'

  Still three attempts. The provider's allowance is untouched and it got no
  extra traffic out of this change. Only the spacing moved — and by the
  third attempt the provider is well again.

  Note the transport line: the forty-line proxy is presenting TLS 1.3 to
  the provider, exactly as nginx was. checkout still has no keystore.
EOF


rule
say "Act 6 — a refusal is still final"
rule
echo "  an allowance of two attempts, and a provider that is unwell for 600ms."
reset '{"unwellForMillis":600,"allowance":2}'
pay "ORD-4419" 3150 | sed 's/^/    /'
echo
echo "  what the provider itself recorded:"
arrivals
cat <<'EOF'

  The third attempt was refused — 429, the account's allowance is spent —
  and the proxy stopped there rather than waiting and asking again. Being
  able to write the waiting is not a licence to become greedier, and the
  Java proxy enforces the same rule nginx did.
EOF


rule
say "Act 7 — the gap in the middle of a swap"
rule
echo "  stopping the Java proxy. Nothing else is touched."
docker compose stop sidecar-java >/dev/null 2>&1
sleep 1
printf '  bound to localhost:8081:  %s\n' "$(bound_to_the_port)"
reset '{"unwellForMillis":0,"allowance":12}'
echo
echo "  a customer pays for a kettle:"
pay "ORD-4420" 3150 | sed 's/^/    /'
echo
echo "  the provider's own ledger:"
attempts | sed 's/^/    /'
cat <<'EOF'

  The provider is healthy, the network is healthy, checkout is healthy, and
  the payment failed instantly. Zero attempts reached the provider, because
  the request never left the machine — so nothing in the provider's
  dashboards will ever show that this happened.

  This is why a swap is a rollout: start the new proxy before stopping the
  old one, move one service at a time, and keep the old one installable.
EOF
echo
echo "  putting nginx back is the whole rollback:"
docker compose up -d sidecar-nginx >/dev/null 2>&1
sleep 3
printf '  bound to localhost:8081:  %s\n' "$(bound_to_the_port)"
reset '{"unwellForMillis":0,"allowance":12}'
pay "ORD-4421" 3150 | sed 's/^/    /'


rule
say "What Tier 2 added"
rule
LINES_NGINX=$(grep -vc '^\s*#\|^\s*$' sidecar/payments-sidecar.conf.template)
LINES_JAVA=$(grep -vc '^\s*//\|^\s*\*\|^\s*/\*\|^\s*$' \
  javaproxy/src/main/java/com/jk/explore/sidecarjavaproxy/real/javaproxy/JavaProxy.java)
printf '    nginx configuration, comments stripped:   %s lines\n' "$LINES_NGINX"
printf '    Java proxy, comments stripped:            %s lines\n' "$LINES_JAVA"
cat <<'EOF'

  Tier 1 makes every claim above in one JVM, where installing a proxy is
  assigning a field. Three of those claims can only be shown here:

    the proxy that answered changed language, in a separate container,
      and the service was not rebuilt, restarted or told
    the new proxy had to satisfy the same transport contract as the old
      one, and the provider's ledger says it did
    a request arriving while nothing is bound is refused by the operating
      system, before anybody can see it

  And here is the fourth thing, which is the one Tier 1 flatters.

  Tier 1 compares 22 lines of configuration with 40 of Java, because in one
  JVM the Java proxy is a retry loop and nothing else. Out here it is not.
  The count above is what a proxy actually has to do before it can retry at
  all: bind a port, read a request, present a certificate, hand an answer
  back, and decide what to trust. The retry loop itself is still small --
  forward() is twenty-five of those lines, and the sleep is one of them.
  The other eighty-seven are what nginx was already doing for free,
  and it is still missing an access log in the shop's format, connection
  pooling, inbound TLS, header hygiene, and anybody publishing security
  fixes for it while you sleep.

  That is the bill, measured rather than asserted. The benefit has not
  changed -- the same three attempts, properly spaced, and a payment that
  goes through. Decide whether one is worth the other in your own system.
EOF
echo
