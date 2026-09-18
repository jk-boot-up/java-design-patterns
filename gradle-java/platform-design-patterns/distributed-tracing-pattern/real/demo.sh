#!/usr/bin/env bash
#
# The Tier 2 walkthrough, start to finish, unattended.
#
# Everything this script prints is real output from two running Spring Boot
# services and a real Jaeger. That matters more than it sounds: the standing
# rule across this repository is that every number quoted in a README is
# captured output rather than something written from memory, and for Tier 2 that
# means the transcript in real/README.md is produced by running this file and
# pasting what came back. Never hand-edit a transcript.
#
#   ./demo.sh
#
# Requires: a JDK 21, Docker, and a network connection the first time (Gradle
# has to fetch Spring and Docker has to pull Jaeger). Tier 1 needs none of it.
# That asymmetry is the whole reason the two tiers are separate builds.

set -euo pipefail
cd "$(dirname "$0")"

PAGE_PORT=8080
RECO_PORT=8081
JAEGER_UI=16686
LOG_DIR=build/demo-logs

# The wrapper one directory up is reused rather than checked in again here.
# `gradlew` is only a launcher -- Gradle takes its project directory from the
# working directory -- so running `../gradlew` from inside `real/` builds this
# build, and the repository is spared a second copy of the wrapper jar.
GRADLE=../gradlew

page_pid=""
reco_pid=""

cleanup() {
  [ -n "$page_pid" ] && kill "$page_pid" 2>/dev/null || true
  [ -n "$reco_pid" ] && kill "$reco_pid" 2>/dev/null || true
  docker compose down --remove-orphans >/dev/null 2>&1 || true
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

page() {
  # $1 is the propagate flag.
  curl -s "http://localhost:$PAGE_PORT/page?sku=SKU-4417&propagate=$1" | python3 -m json.tool
}

# Ask Jaeger what it actually received. This is the only assertion in the demo
# that cannot be faked by the services themselves: the ids printed by /page come
# from the services' own view of the world, whereas this comes from a separate
# process that saw only what arrived on the wire.
trace_shape() {
  local trace_id=$1
  local response="$LOG_DIR/trace-$trace_id.json"
  curl -s "http://localhost:$JAEGER_UI/api/traces/$trace_id" >"$response"
  # The response goes through a file rather than a pipe on purpose. A heredoc
  # *is* the script's standard input, so `curl | python3 - <<'PY'` hands python
  # the program on stdin and leaves nothing for the program to read.
  python3 - "$response" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
data = doc.get("data") or []
if not data:
    print("  Jaeger has no trace with that id.")
    sys.exit(0)
trace = data[0]
procs = trace.get("processes", {})
spans = trace["spans"]
by_id = {s["spanID"]: s for s in spans}
roots = [s for s in spans
         if not any(r.get("refType") == "CHILD_OF" and r["spanID"] in by_id
                    for r in s.get("references", []))]
services = sorted({procs[s["processID"]]["serviceName"] for s in spans})
print("  spans:    %d" % len(spans))
print("  services: %s" % ", ".join(services))
print("  roots:    %d" % len(roots))
# The waterfall, from the data Jaeger holds, drawn by the same rule Tier 1
# used: indentation is the parent reference, and nothing else.
def children(pid):
    return sorted((s for s in spans
                   if any(r.get("refType") == "CHILD_OF" and r["spanID"] == pid
                          for r in s.get("references", []))),
                  key=lambda s: s["startTime"])
def show(span, depth):
    name = "%s%s" % ("  " * depth, span["operationName"])
    print("    %-44s %6.0fms   [%s]"
          % (name, span["duration"] / 1000.0,
             procs[span["processID"]]["serviceName"]))
    for c in children(span["spanID"]):
        show(c, depth + 1)
for r in sorted(roots, key=lambda s: s["startTime"]):
    show(r, 0)
PY
}

# Everything Jaeger holds for one service, listed by the root of each trace.
# A bare count would have been shorter and would have taught less: the point of
# this step is not that there is one trace too many, it is that you can only see
# which one is the orphan by looking at what each trace starts with.
trace_roots() {
  local service=$1
  local response="$LOG_DIR/traces-$service.json"
  curl -s "http://localhost:$JAEGER_UI/api/traces?service=$service&limit=100" >"$response"
  python3 - "$response" <<'PY'
import json, sys
traces = json.load(open(sys.argv[1])).get("data") or []
print("  %d trace(s):" % len(traces))
for trace in sorted(traces, key=lambda t: min(s["startTime"] for s in t["spans"])):
    procs = trace["processes"]
    spans = trace["spans"]
    by_id = {s["spanID"]: s for s in spans}
    roots = [s for s in spans
             if not any(r.get("refType") == "CHILD_OF" and r["spanID"] in by_id
                        for r in s.get("references", []))]
    root = min(roots, key=lambda s: s["startTime"])
    services = sorted({procs[s["processID"]]["serviceName"] for s in spans})
    print("    %s  starts at %-28s %d span(s) across %s"
          % (trace["traceID"], root["operationName"], len(spans), ", ".join(services)))
PY
}

mkdir -p "$LOG_DIR"

say "0/6  starting Jaeger, and building both services"
docker compose up -d >"$LOG_DIR/jaeger.log" 2>&1
wait_for "http://localhost:$JAEGER_UI/" "Jaeger"
$GRADLE -q build -x test

say "1/6  starting the two services"
$GRADLE -q :recommendations:bootRun >"$LOG_DIR/recommendations.log" 2>&1 &
reco_pid=$!
$GRADLE -q :product-page:bootRun >"$LOG_DIR/product-page.log" 2>&1 &
page_pid=$!
wait_for "http://localhost:$RECO_PORT/actuator/health" "recommendations"
wait_for "http://localhost:$PAGE_PORT/actuator/health" "product page"

say "2/6  one page load, with the context forwarded"
echo "  Nothing in either service writes or reads a traceparent header. The"
echo "  instrumentation is on the RestClient builder at one end and on the"
echo "  servlet at the other, and this is what crossed between them:"
GOOD=$(curl -s "http://localhost:$PAGE_PORT/page?sku=SKU-4417&propagate=true")
echo "$GOOD" | python3 -m json.tool
GOOD_ID=$(echo "$GOOD" | python3 -c 'import json,sys; print(json.load(sys.stdin)["pageTraceId"])')

say "3/6  what Jaeger holds for trace $GOOD_ID"
echo "  Spans take a moment to be exported and indexed."
sleep 6
trace_shape "$GOOD_ID"
echo
echo "  Two processes, one trace, one root. The indentation is the parent"
echo "  reference and nothing else — the same rule Tier 1's Waterfall printed"
echo "  with string concatenation, applied here by software nobody in this"
echo "  repository wrote, to data it got off the wire."

say "4/6  the same page, through a client built with RestClient.create()"
echo "  Same URL, same response, same recommendations. One line different."
BAD=$(curl -s "http://localhost:$PAGE_PORT/page?sku=SKU-4417&propagate=false")
echo "$BAD" | python3 -m json.tool
BAD_ID=$(echo "$BAD" | python3 -c 'import json,sys; print(json.load(sys.stdin)["pageTraceId"])')

say "5/6  what Jaeger holds for trace $BAD_ID"
sleep 6
trace_shape "$BAD_ID"
echo
echo "  The page's trace now stops at the edge of the process. The ranking"
echo "  model's 340ms is not missing — it is in a second trace, under a root of"
echo "  its own, with nothing to say the two belong to the same customer."
echo "  Neither trace looks broken on its own."

say "6/6  everything Jaeger holds, by service"
echo "  product-page:"
trace_roots product-page
echo "  recommendations:"
trace_roots recommendations
echo
echo "  Read that by what each trace starts with, not by how many there are. One"
echo "  starts at the page and reaches the ranking model. One starts at the page"
echo "  and stops inside it. One starts at /recommendations, which is not where"
echo "  any customer started — that is the orphan, and nothing about it looks"
echo "  broken from the inside. The single-span traces starting at"
echo "  /actuator/health are this script's own readiness checks, and they are"
echo "  here for a reason worth keeping: a sampler set to 1.0 traces everything"
echo "  that arrives, including the traffic you did not mean to measure."
echo
echo "  Jaeger's UI is on http://localhost:$JAEGER_UI if you want to look"
echo "  before the script stops it."

say "done — stopping both services and Jaeger"
