#!/usr/bin/env bash
#
# The Tier 2 walkthrough, start to finish, unattended.
#
# Everything this script prints is real output from two running Spring Boot
# services. That matters more than it sounds: the standing rule across this
# repository is that every number quoted in a README is captured output rather
# than something written from memory, and for Tier 2 that means the transcript
# in real/README.md is produced by running this file and pasting what came
# back. Never hand-edit a transcript.
#
#   ./demo.sh
#
# Requires: a JDK 21, and a network connection the first time (Gradle has to
# fetch Spring). Tier 1 needs neither. That asymmetry is the whole reason the
# two tiers are separate builds.

set -euo pipefail
cd "$(dirname "$0")"

CONFIG_PORT=8888
CHECKOUT_PORT=8080
THRESHOLD_FILE=config-repo/checkout-service.yml
LOG_DIR=build/demo-logs

# The wrapper one directory up is reused rather than checked in again here.
# `gradlew` is only a launcher -- Gradle takes its project directory from the
# working directory -- so running `../gradlew` from inside `real/` builds this
# build, and the repository is spared a second copy of the wrapper jar.
GRADLE=../gradlew

config_server_pid=""
checkout_pid=""

cleanup() {
  [ -n "$checkout_pid" ] && kill "$checkout_pid" 2>/dev/null || true
  [ -n "$config_server_pid" ] && kill "$config_server_pid" 2>/dev/null || true
  # Put the threshold back, so running the demo twice shows the same thing
  # both times.
  git checkout -- "$THRESHOLD_FILE" 2>/dev/null || true
}
trap cleanup EXIT

say() {
  printf '\n\033[1m%s\033[0m\n' "$*"
}

wait_for() {
  local url=$1 name=$2 tries=60
  printf '  waiting for %s' "$name"
  until curl -sf "$url" >/dev/null 2>&1; do
    tries=$((tries - 1))
    if [ "$tries" -le 0 ]; then
      printf ' — gave up\n'
      echo "  $name never came up. Its log is in $LOG_DIR." >&2
      exit 1
    fi
    printf '.'
    sleep 1
  done
  printf ' up\n'
}

set_threshold() {
  # Rewrite just the freeOver line, leaving the file's comments intact.
  local value=$1
  perl -i -pe "s/^(\s*freeOver:).*/\$1 $value/" "$THRESHOLD_FILE"
  printf '  %s now reads: %s\n' "$THRESHOLD_FILE" "$(grep 'freeOver:' "$THRESHOLD_FILE" | tr -s ' ')"
}

quote() {
  curl -s "http://localhost:$CHECKOUT_PORT/quote?total=$1" | python3 -m json.tool
}

refresh() {
  # This is the request that does it. Nothing is rebuilt, redeployed or
  # restarted; the @RefreshScope beans are discarded and built again from a
  # freshly fetched configuration.
  curl -s -X POST "http://localhost:$CHECKOUT_PORT/actuator/refresh" \
    -H 'Content-Type: application/json'
  printf '\n'
}

mkdir -p "$LOG_DIR"

say "0/6  building both services"
$GRADLE -q build -x test

say "1/6  starting the config server on $CONFIG_PORT"
$GRADLE -q :config-server:bootRun >"$LOG_DIR/config-server.log" 2>&1 &
config_server_pid=$!
wait_for "http://localhost:$CONFIG_PORT/actuator/health" "config server"

echo "  what the server is serving to checkout-service:"
curl -s "http://localhost:$CONFIG_PORT/checkout-service/default" | python3 -m json.tool

say "2/6  starting the checkout service on $CHECKOUT_PORT"
$GRADLE -q :checkout-service:bootRun >"$LOG_DIR/checkout-service.log" 2>&1 &
checkout_pid=$!
wait_for "http://localhost:$CHECKOUT_PORT/actuator/health" "checkout service"

say "3/6  a basket of £48.00, against the threshold of £50.00"
echo "  Forty-eight pounds does not reach fifty, so delivery is charged."
quote 48.00

say "4/6  moving the threshold to £35.00 — no rebuild, no restart"
set_threshold "35.00"
echo "  the refresh request, and the keys it says changed:"
refresh

echo "  the same basket, asked again:"
quote 48.00
echo "  Same process, same build, same uptime. Delivery is now free."

say "5/6  the guard: someone sets the threshold to -1"
set_threshold "-1"
echo "  the refresh request, which reports the key as changed either way:"
refresh || true
echo
echo "  Minus one is outside the declared range of £5.00 to £200.00, so the"
echo "  bind fails and the value never reaches the checkout. Read"
echo "  'thresholdState' below: the shop is still quoting, on the last value"
echo "  that passed. Without LastGoodSettings this request would be a 500,"
echo "  and so would every request after it."
quote 48.00

say "6/6  putting it back"
set_threshold "50.00"
refresh
quote 48.00
echo "  Back to charging delivery on a £48.00 basket, and the whole sequence"
echo "  took one process lifetime."

say "done — stopping both services"
