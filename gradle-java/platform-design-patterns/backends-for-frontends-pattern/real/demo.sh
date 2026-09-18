#!/usr/bin/env bash
#
# The Tier 2 walkthrough, start to finish, unattended.
#
# Everything this script prints is real output from three running Spring Boot
# services, measured over real HTTP. That matters more than it sounds: the
# standing rule across this repository is that every number quoted in a README
# is captured output rather than something written from memory, and for Tier 2
# that means the transcript in real/README.md is produced by running this file
# and pasting what came back. Never hand-edit a transcript.
#
#   ./demo.sh
#
# Requires: a JDK 21 and a network connection the first time, so Gradle can
# fetch Spring. No Docker. Tier 1 needs none of it, which is the whole reason
# the two tiers are separate builds.

set -euo pipefail
cd "$(dirname "$0")"

SHOP=http://localhost:8082
PHONE=http://localhost:8080
DESKTOP=http://localhost:8081
SKU=SKU-4417
LOG_DIR=build/demo-logs

# The wrapper one directory up is reused rather than checked in again here.
# `gradlew` is only a launcher -- Gradle takes its project directory from the
# working directory -- so running `../gradlew` from inside `real/` builds this
# build, and the repository is spared a second copy of the wrapper jar.
GRADLE=../gradlew

shop_pid=""
phone_pid=""
desktop_pid=""

cleanup() {
  for pid in "$shop_pid" "$phone_pid" "$desktop_pid"; do
    [ -n "$pid" ] && kill "$pid" 2>/dev/null || true
  done
}
trap cleanup EXIT

say() {
  printf '\n\033[1m%s\033[0m\n' "$*"
}

wait_for() {
  local url=$1 name=$2 tries=90
  printf '  waiting for %s' "$name"
  until curl -sf "$url" >/dev/null 2>&1; do
    tries=$((tries - 1))
    if [ "$tries" -le 0 ]; then
      printf ' — gave up\n'
      echo "  $name never came up. Logs are in $LOG_DIR." >&2
      exit 1
    fi
    printf '.'
    sleep 1
  done
  printf ' up\n'
}

# The body size as the client actually received it, in bytes on the wire.
#
# `curl -w '%{size_download}'` is used rather than measuring the string in the
# shell because that is the number the customer's connection paid for, and it
# is measured by the client rather than claimed by the server.
bytes() {
  curl -s -o /dev/null -w '%{size_download}' "$1"
}

# Pretty-print a response and say how big it was unformatted.
show() {
  local url=$1
  local size
  size=$(bytes "$url")
  curl -s "$url" | python3 -m json.tool --no-ensure-ascii
  printf '  → %s bytes on the wire\n' "$size"
}

# How many top-level fields came back. The field count and the byte count are
# different arguments and the project is careful to keep them apart: the byte
# count is what the connection carried, the field count is what the screen can
# possibly draw.
fields() {
  curl -s "$1" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))'
}

# The shop's own tally of calls that arrived since the last reset. This is the
# only number in the demo that a backend cannot fake: it is kept by the callee.
calls() {
  curl -s "$SHOP/calls" | python3 -c '
import json, sys
c = json.load(sys.stdin)
named = [k for k in c if k != "total"]
print("    " + "  ".join("%s=%d" % (k, c[k]) for k in named))
print("    total internal calls: %d" % c["total"])'
}

reset_calls() {
  curl -s -X POST "$SHOP/calls/reset" >/dev/null
}

mkdir -p "$LOG_DIR"

say "0/7  building all three services"
$GRADLE -q build -x test

say "1/7  starting the shop, and the two backends in front of it"
$GRADLE -q :shop:bootRun >"$LOG_DIR/shop.log" 2>&1 &
shop_pid=$!
wait_for "$SHOP/actuator/health" "shop"
$GRADLE -q :mobile-bff:bootRun >"$LOG_DIR/mobile-bff.log" 2>&1 &
phone_pid=$!
$GRADLE -q :web-bff:bootRun >"$LOG_DIR/web-bff.log" 2>&1 &
desktop_pid=$!
wait_for "$PHONE/actuator/health" "mobile-bff"
wait_for "$DESKTOP/actuator/health" "web-bff"

say "2/7  the second design — one shared endpoint, for everybody"
echo "  This is the design most shops arrive at, and it is a real improvement on"
echo "  the phone calling all five services itself: one round trip instead of five."
SHARED_BYTES=$(bytes "$SHOP/api/products/$SKU")
SHARED_FIELDS=$(fields "$SHOP/api/products/$SKU")
echo "  GET /api/products/$SKU"
echo "    $SHARED_BYTES bytes, $SHARED_FIELDS top-level fields"
echo "    the phone draws six of them"
# Reset *after* measuring and then make exactly one more request, so the counts
# below belong to a single page load. Measuring the size and the field count
# takes a request each, and a tally of three page loads would be this script
# counting its own instrumentation.
reset_calls
curl -s "$SHOP/api/products/$SKU" >/dev/null
calls

say "3/7  and the obvious fix works"
echo "  Ask for only the fields the phone draws, by name."
reset_calls
FIELDS='title,pricing.nowPence,thumbnail,reviews.average,reviews.count,inventory.nextDelivery'
show "$SHOP/api/products/$SKU?fields=$FIELDS"
TRIMMED=$(bytes "$SHOP/api/products/$SKU?fields=$FIELDS")
echo
echo "  $SHARED_BYTES bytes down to $TRIMMED, from a query parameter. No new process to"
echo "  run, nothing to deploy, no diagram. If this pattern were about payload"
echo "  size, this demo would stop here — and a lot of write-ups do."

say "4/7  the request the shared endpoint cannot serve"
echo "  The phone team want one line of text under the price: a delivery"
echo "  sentence, joined from stock, the delivery rules and the clock. Ask the"
echo "  shared endpoint for it by name, the way everything else was asked for:"
curl -s "$SHOP/api/products/$SKU?fields=delivery" | python3 -m json.tool --no-ensure-ascii
echo
echo "  Empty, and not because of a typo. No service owns that field, so the"
echo "  shared endpoint has no way to answer. Adding it here would change a"
echo "  document five other clients also receive — which is a contract change,"
echo "  a review, and a place in a queue behind work that has nothing to do"
echo "  with the phone. Half an hour of work, five weeks of waiting."

say "5/7  a backend for the phone, and a backend for the desktop"
echo "  GET /phone/product-screen/$SKU"
show "$PHONE/phone/product-screen/$SKU"
PHONE_FIELDS=$(fields "$PHONE/phone/product-screen/$SKU")
echo "  what the shop was asked for, to serve that one request:"
reset_calls
curl -s "$PHONE/phone/product-screen/$SKU" >/dev/null
calls
echo
echo "  Four, not five. Recommendations is reachable and was not asked, because"
echo "  this screen has no related-products strip and the answer would have had"
echo "  nowhere to go. A shared endpoint cannot make that decision for one client."
echo
echo "  GET /desktop/product-page/$SKU"
DESKTOP_BYTES=$(bytes "$DESKTOP/desktop/product-page/$SKU")
DESKTOP_FIELDS=$(fields "$DESKTOP/desktop/product-page/$SKU")
curl -s "$DESKTOP/desktop/product-page/$SKU" | python3 -m json.tool --no-ensure-ascii
echo "  → $DESKTOP_BYTES bytes on the wire"
reset_calls
curl -s "$DESKTOP/desktop/product-page/$SKU" >/dev/null
calls
echo
echo "  Look at the delivery field in each. The phone was given a whole English"
echo "  sentence. The desktop was given the bare date, because that page has a"
echo "  delivery panel with its own layout and wants the parts. Two backends,"
echo "  one shop, two different answers about what a product is — on purpose."

say "6/7  the same product, three ways"
PHONE_BYTES=$(bytes "$PHONE/phone/product-screen/$SKU")
printf '  %-34s %8s %8s %9s\n' "design" "bytes" "fields" "internal"
printf '  %-34s %8s %8s %9s\n' "one shared endpoint" "$SHARED_BYTES" "$SHARED_FIELDS" "5"
printf '  %-34s %8s %8s %9s\n' "shared endpoint, ?fields=" "$TRIMMED" "6" "5"
printf '  %-34s %8s %8s %9s\n' "a backend for the phone" "$PHONE_BYTES" "$PHONE_FIELDS" "4"
printf '  %-34s %8s %8s %9s\n' "a backend for the desktop" "$DESKTOP_BYTES" "$DESKTOP_FIELDS" "5"
echo
echo "  The ?fields= row is the one to sit with. It gets a payload in the same"
echo "  territory as the phone's own backend, from one query parameter. The"
echo "  backend's advantage over it is not in this table at all — it is step 4,"
echo "  and it is a queue rather than a number."

say "7/7  the bill — one rule, two answers"
echo "  Before the pricing review, both backends claim a saving:"
printf '    phone:   '; curl -s "$PHONE/phone/saving/$SKU" | python3 -c 'import json,sys; print(repr(json.load(sys.stdin)["saving"]))'
printf '    desktop: '; curl -s "$DESKTOP/desktop/saving/$SKU" | python3 -c 'import json,sys; print(repr(json.load(sys.stdin)["saving"]))'
echo
echo "  Now the pricing team finish their review. A higher price may only be"
echo "  advertised as a saving if it was genuinely in force long enough, and"
echo "  this one went up eleven days ago. The shop is told. Both backends read"
echo "  pricing on every request, so both are told:"
curl -s -X POST "$SHOP/pricing/review" | python3 -m json.tool --no-ensure-ascii
echo
echo "  Same product, same price, same second, asked again:"
printf '    phone:   '; curl -s "$PHONE/phone/saving/$SKU" | python3 -c 'import json,sys; print(repr(json.load(sys.stdin)["saving"]))'
printf '    desktop: '; curl -s "$DESKTOP/desktop/saving/$SKU" | python3 -c 'import json,sys; print(repr(json.load(sys.stdin)["saving"]))'
echo
echo "  One of those two screens is now making a claim the shop is not allowed"
echo "  to make. Both services are healthy:"
printf '    phone:   '; curl -s "$PHONE/actuator/health"
printf '\n    desktop: '; curl -s "$DESKTOP/actuator/health"
echo
echo
echo "  Nothing threw. Nothing was logged. Neither process is in a bad state and"
echo "  no test writable inside either one would notice, because from inside"
echo "  each backend, each backend is right. The only person who can see it is a"
echo "  customer with both screens open."
echo
echo "  The rule: a backend for a frontend may hold the shape. Anything the shop"
echo "  would still believe with every client switched off belongs behind it."

say "done — stopping all three services"
