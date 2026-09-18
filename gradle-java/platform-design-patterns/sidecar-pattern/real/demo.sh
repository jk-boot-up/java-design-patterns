#!/usr/bin/env bash
#
# The Tier 2 walkthrough, start to finish, unattended.
#
# Everything this script prints is real output from five running containers.
# That matters more than it sounds: the standing rule across this repository is
# that every number quoted in a README is captured output rather than something
# written from memory, and for Tier 2 that means the transcript in
# real/README.md is produced by running this file and pasting what came back.
# Never hand-edit a transcript.
#
#   ./demo.sh
#
# Requires: a JDK 21, Docker, and a network connection the first time (Gradle
# has to fetch Spring and Docker has to pull nginx and a JRE). Tier 1 needs none
# of it. That asymmetry is the whole reason the two tiers are separate builds.

set -euo pipefail
cd "$(dirname "$0")"

GRADLE=../gradlew          # the wrapper one directory up; Gradle takes its
                           # project directory from the working directory, so
                           # this builds *this* build and the repository is
                           # spared a second copy of the wrapper jar.
CERTS=build/certs
PROVIDER=https://localhost:19443
CHECKOUT=http://localhost:18080
REFUNDS=http://localhost:18090

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

# Ask the provider what it actually saw. This is the only tally in the demo that
# the services cannot influence: a service cannot count the attempts a proxy made
# on its behalf, because not seeing them is the point of the pattern.
attempts() {
  curl -sk "$PROVIDER/attempts" | python3 -m json.tool
}

reset() {
  curl -sk -X POST "$PROVIDER/reset" \
       -H 'Content-Type: application/json' -d "$1" >/dev/null
}

pay() {
  # $1 is the service's base URL, $2 the payment reference, $3 the amount.
  curl -s -X POST "$1/pay" -H 'Content-Type: application/json' \
       -d "{\"reference\":\"$2\",\"amountPence\":$3}" | python3 -m json.tool
}

started_at() {
  docker inspect -f '{{.State.StartedAt}}' "$1"
}


# ---------------------------------------------------------------------------
say "Building the two service images"
# ---------------------------------------------------------------------------
"$GRADLE" --quiet bootJar

mkdir -p "$CERTS"
if [ ! -f "$CERTS/gateway.p12" ]; then
  echo "  generating the provider's certificate"
  keytool -genkeypair \
    -alias gateway -keyalg RSA -keysize 2048 -validity 365 \
    -dname "CN=gateway, OU=payments, O=provider, C=GB" \
    -storetype PKCS12 -keystore "$CERTS/gateway.p12" -storepass changeit \
    -ext "SAN=dns:gateway,dns:localhost" >/dev/null
fi

docker compose up --build -d >/dev/null 2>&1
wait_for "$PROVIDER/attempts" "the payment provider"
wait_for "$CHECKOUT/about" "checkout"
wait_for "$REFUNDS/about" "refunds"


rule
say "Act 1 — five containers, and only two of them are the shop"
rule
docker compose ps --format '  {{.Name}}\t{{.Image}}\t{{.Status}}' | sed 's/\t/  /g'
cat <<'EOF'

  Two services, one provider, and two proxies. The proxies are the third row
  of the bill: twice as many things to start, patch, version and look at.
EOF


rule
say "Act 2 — what is left in the service"
rule
echo "  checkout describes itself:"
curl -s "$CHECKOUT/about" | python3 -m json.tool | sed 's/^/    /'
cat <<'EOF'

  Every mention of retrying in the payments service, in full:
EOF
grep -rn "retry\|Retry" payments/src/main/java | sed 's/^/    /'
cat <<'EOF'

  Two comments and a field name. No loop, no backoff, no deadline, no
  certificate, no counter, and no address for the payment provider.
EOF


rule
say "Act 3 — one file, two proxies"
rule
cat <<'EOF'
  The policy lives in sidecar/payments-sidecar.conf.template, mounted into
  both proxies. Here is what each container actually ended up running,
  with the comments stripped:

EOF
for c in sidecar-demo-checkout-proxy sidecar-demo-refunds-proxy; do
  echo "  $c"
  docker exec "$c" sh -c "grep -v '^\s*#' /etc/nginx/conf.d/default.conf | grep -v '^\s*$'" \
    | sed 's/^/    /'
  echo
done
cat <<'EOF'
  Identical but for the name each one reports. They are not two copies that
  happen to agree — there is one file on disk and both containers mount it.
EOF


rule
say "Act 4 — a healthy payment, and who spoke TLS"
rule
reset '{"declineFirst":0,"allowance":12}'
pay "$CHECKOUT" "ORD-4417" 4799 | sed 's/^/    /'
echo
echo "  the provider's own record:"
attempts | sed 's/^/    /'
cat <<'EOF'

  One attempt, and the provider saw TLS 1.3. The service that made this
  payment sent plain HTTP to localhost and has no keystore, no trust store
  and no protocol list anywhere in its configuration.
EOF


rule
say "Act 5 — the wobble, and a retry the service never made"
rule
echo "  the provider will decline the first two attempts at any payment."
reset '{"declineFirst":2,"allowance":12}'
pay "$CHECKOUT" "ORD-4418" 4799 | sed 's/^/    /'
pay "$REFUNDS"  "REF-3820" 2250 | sed 's/^/    /'
echo
echo "  the provider's own record:"
attempts | sed 's/^/    /'
echo
echo "  what checkout's proxy logged, one line per attempt:"
docker exec sidecar-demo-checkout-proxy cat /var/log/nginx/attempts.log \
  | tail -n 4 | sed 's/^/    /'
cat <<'EOF'

  Three attempts each, from a service whose source you have just read. The
  proxy made them, the proxy waited, and the proxy is what the provider saw.
EOF


rule
say "Act 6 — changing the policy, without rebuilding either service"
rule
before_checkout=$(started_at sidecar-demo-checkout)
before_refunds=$(started_at sidecar-demo-refunds)
echo "  editing one line in one file: three attempts becomes one."
sed -i.bak 's/proxy_next_upstream_tries 3;/proxy_next_upstream_tries 1;/' \
    sidecar/payments-sidecar.conf.template
docker compose restart sidecar-checkout sidecar-refunds >/dev/null 2>&1
sleep 2
reset '{"declineFirst":2,"allowance":12}'
pay "$CHECKOUT" "ORD-4419" 4799 | sed 's/^/    /'
echo
echo "  the provider's own record:"
attempts | sed 's/^/    /'
echo
echo "  and the service containers, which were never touched:"
printf '    checkout started at %s, now %s\n' "$before_checkout" "$(started_at sidecar-demo-checkout)"
printf '    refunds  started at %s, now %s\n' "$before_refunds"  "$(started_at sidecar-demo-refunds)"
cat <<'EOF'

  One attempt, one decline, no payment — and the change reached both
  services. No Java was recompiled, no jar was rebuilt, no service process
  was restarted. In Tier 1 this same change was four pull requests, and one
  of them was forgotten.
EOF
mv sidecar/payments-sidecar.conf.template.bak sidecar/payments-sidecar.conf.template
docker compose restart sidecar-checkout sidecar-refunds >/dev/null 2>&1
sleep 2


rule
say "Act 7 — the second thing that can be down"
rule
echo "  stopping checkout's proxy. Nothing else is touched."
docker compose stop sidecar-checkout >/dev/null 2>&1
reset '{"declineFirst":0,"allowance":12}'
echo
echo "  checkout tries to take a payment:"
pay "$CHECKOUT" "ORD-4420" 4799 | sed 's/^/    /'
echo
echo "  refunds, whose own proxy is fine:"
pay "$REFUNDS" "REF-3821" 2250 | sed 's/^/    /'
echo
echo "  the provider's own record:"
attempts | sed 's/^/    /'
cat <<'EOF'

  The gateway is healthy, the network is healthy, checkout is healthy, and
  checkout cannot take a single payment. Zero of its attempts reached the
  provider, because the request never left the machine — and the service has
  no retry code to fall back on, on purpose.
EOF
docker compose start sidecar-checkout >/dev/null 2>&1
sleep 2
echo
echo "  starting the proxy again is the whole repair:"
pay "$CHECKOUT" "ORD-4421" 4799 | sed 's/^/    /'


rule
say "What Tier 2 added"
rule
cat <<'EOF'
  Tier 1 makes every claim above in one JVM, where the proxy is an object
  wrapping another object — which is Decorator, and Tier 1 says so.

  Three of those claims can only be shown here:

    the policy changed without the service being rebuilt or restarted
    the proxy is not written in Java, and the service does not care
    killing the proxy takes every call with it, on a healthy network

  Those three are the reasons to pay for a process. Nothing else is.
EOF
echo
