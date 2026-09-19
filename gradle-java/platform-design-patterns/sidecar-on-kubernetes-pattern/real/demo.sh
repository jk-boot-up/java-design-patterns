#!/usr/bin/env bash
#
# Tier 2: the same two containers as a Kubernetes Pod, on a real cluster.
#
# Everything this script prints is real output from a real `kind` cluster. Never
# hand-edit the transcript in README.md: run this and paste what came back.
#
#   ./demo.sh          # creates the cluster, runs six acts, deletes the cluster
#
# Requires: Docker (running), `kind` 0.33.0, `kubectl`, a JDK 21, and a network the
# first time (kind pulls a ~1 GB node image). Tier 1 needs none of it.
#
# It reuses sidecar-pattern's service and gateway sources and its nginx template
# rather than copying them, so the comparison with Docker Compose is exact.

set -euo pipefail
cd "$(dirname "$0")"

SIDECAR_REAL=../../sidecar-pattern/real
CLUSTER=sidecar-demo
KIND_VERSION=0.33.0

say()  { printf '\n\033[1m%s\033[0m\n' "$*"; }
rule() { printf '========================================================================\n'; }

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing: $1 — see ../docs/dependencies.md" >&2; exit 1; }; }
need docker; need kubectl; need kind
docker info >/dev/null 2>&1 || { echo "Docker is not running" >&2; exit 1; }
case "$(kind version)" in
  *"v$KIND_VERSION"*) ;;
  *) echo "this demo is pinned to kind v$KIND_VERSION, found: $(kind version)" >&2; exit 1 ;;
esac

# KEEP=1 leaves the cluster running afterwards, and REUSE=1 uses one that is already up. Both are for
# iterating on the script. A transcript is only ever produced by a plain run, which creates and deletes.
cleanup() {
  pkill -f "port-forward.*sidecar-demo" >/dev/null 2>&1 || true
  if [ "${KEEP:-0}" != 1 ]; then
    kind delete cluster --name "$CLUSTER" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

k() { kubectl --context "kind-$CLUSTER" "$@"; }

wait_ready() {
  k rollout status "deployment/$1" --timeout=180s >/dev/null
}

pod_of() { k get pods -l "app=$1" -o jsonpath='{.items[0].metadata.name}'; }

# ---------------------------------------------------------------------------
say "Building the two images from sidecar-pattern's sources"
# ---------------------------------------------------------------------------
( cd "$SIDECAR_REAL" && ../gradlew --quiet bootJar )
CERTS="$SIDECAR_REAL/build/certs"
mkdir -p "$CERTS"
if [ ! -f "$CERTS/gateway.p12" ]; then
  keytool -genkeypair -alias gateway -keyalg RSA -keysize 2048 -validity 365 \
    -dname "CN=gateway, OU=payments, O=provider, C=GB" -storetype PKCS12 \
    -keystore "$CERTS/gateway.p12" -storepass changeit \
    -ext "SAN=dns:gateway,dns:localhost" >/dev/null
fi
docker build -q -t sidecar-k8s-payments:demo "$SIDECAR_REAL/payments" >/dev/null
docker build -q -t sidecar-k8s-gateway:demo  "$SIDECAR_REAL/gateway"  >/dev/null
docker image inspect nginx:1.31.5-alpine >/dev/null 2>&1 || docker pull -q nginx:1.31.5-alpine >/dev/null

say "Creating the cluster (one node, in one Docker container)"
if [ "${REUSE:-0}" = 1 ] && kind get clusters 2>/dev/null | grep -qx "$CLUSTER"; then
  echo "  (reusing the running cluster)"
else
  kind delete cluster --name "$CLUSTER" >/dev/null 2>&1 || true
  kind create cluster --config kind-config.yaml --wait 120s >/dev/null 2>&1
fi
echo "  node image: $(docker inspect -f '{{.Config.Image}}' ${CLUSTER}-control-plane | sed 's/@sha256.*//')"
echo "  Kubernetes: $(k version -o json | python3 -c 'import json,sys; print(json.load(sys.stdin)["serverVersion"]["gitVersion"])')"
for image in sidecar-k8s-payments:demo sidecar-k8s-gateway:demo nginx:1.31.5-alpine; do
  kind load docker-image "$image" --name "$CLUSTER" >/dev/null 2>&1
done

k create secret generic gateway-cert --from-file="$CERTS/gateway.p12" --dry-run=client -o yaml | k apply -f - >/dev/null
k create configmap sidecar-config \
  --from-file=default.conf.template="$SIDECAR_REAL/sidecar/payments-sidecar.conf.template" --dry-run=client -o yaml | k apply -f - >/dev/null
k apply -f k8s/gateway.yaml -f k8s/checkout.yaml -f k8s/refunds.yaml >/dev/null
wait_ready gateway; wait_ready checkout; wait_ready refunds
CHECKOUT_POD=$(pod_of checkout)


rule
say "Act 1 — kubectl get pods, and 2/2"
rule
k get pods --no-headers | awk '{print "  " $1 "  READY " $2 "  " $3 "  restarts " $4}'
side_started=$(k get pod "$CHECKOUT_POD" -o jsonpath='{.status.initContainerStatuses[0].state.running.startedAt}')
main_started=$(k get pod "$CHECKOUT_POD" -o jsonpath='{.status.containerStatuses[0].state.running.startedAt}')
echo "  the sidecar is a native sidecar (an init container with restartPolicy: Always):"
echo "    sidecar started $side_started, checkout started $main_started"
echo "    the sidecar started first: $([ "$side_started" \< "$main_started" ] || [ "$side_started" = "$main_started" ] && echo yes || echo no)"
cat <<'EOF'

  checkout reads 2/2: one logical service, two containers. refunds reads 1/1,
  because it is one container, and the next act gives it a second.
EOF


rule
say "Act 2 — one network, by definition"
rule
echo "  from inside the checkout container, on the loopback address, with no network configured anywhere:"
k exec "$CHECKOUT_POD" -c checkout -- wget -qO- http://127.0.0.1:8081/healthz | sed 's/^/    /'
echo "  the address of the Pod, and of each container in it:"
echo "    pod IP: $(k get pod "$CHECKOUT_POD" -o jsonpath='{.status.podIP}')"
echo "    containers: $(k get pod "$CHECKOUT_POD" -o jsonpath='{range .spec.initContainers[*]}{.name} {end}{range .spec.containers[*]}{.name} {end}')"
cat <<'EOF'

  The checkout container reached a port that belongs to a different container,
  and the manifest contains no network settings at all. That is a Pod.
EOF


rule
say "Act 3 — a payment through the sidecar"
rule
k port-forward "pod/$CHECKOUT_POD" 18080:8080 >/dev/null 2>&1 &
PF1=$!
k port-forward "deployment/gateway" 19443:9443 >/dev/null 2>&1 &
PF2=$!
for _ in $(seq 1 30); do curl -sf http://localhost:18080/about >/dev/null 2>&1 && break; sleep 1; done
for _ in $(seq 1 30); do curl -skf https://localhost:19443/attempts >/dev/null 2>&1 && break; sleep 1; done
curl -sk -X POST https://localhost:19443/reset -H 'Content-Type: application/json' -d '{"declineFirst":2,"allowance":12}' >/dev/null
echo "  the provider is told to decline the first two attempts at each payment. checkout pays once:"
curl -s -X POST http://localhost:18080/pay -H 'Content-Type: application/json' \
     -d '{"reference":"order-1","amountPence":4200}' | python3 -m json.tool | sed 's/^/    /'
echo "  what the provider saw:"
curl -sk https://localhost:19443/attempts | python3 -m json.tool | sed 's/^/    /'
echo "  the proxy's own log, read from inside its container:"
k exec "$CHECKOUT_POD" -c sidecar -- cat /var/log/nginx/attempts.log | grep -v "status=-" | tail -2 | sed 's/^/    /'
kill $PF1 $PF2 >/dev/null 2>&1 || true


rule
say "Act 4 — kill the proxy: only the proxy restarts"
rule
restarts() { k get pod "$CHECKOUT_POD" -o jsonpath='{.status.initContainerStatuses[0].restartCount} {.status.containerStatuses[0].restartCount}'; }
echo "  before: restart counts (sidecar, checkout): $(restarts)"
checkout_started=$(k get pod "$CHECKOUT_POD" -o jsonpath='{.status.containerStatuses[0].state.running.startedAt}')
k exec "$CHECKOUT_POD" -c sidecar -- kill 1 >/dev/null 2>&1 || true
for _ in $(seq 1 60); do
  [ "$(k get pod "$CHECKOUT_POD" -o jsonpath='{.status.initContainerStatuses[0].restartCount}')" -ge 1 ] && break
  sleep 1
done
for _ in $(seq 1 60); do
  [ "$(k get pod "$CHECKOUT_POD" -o jsonpath='{.status.initContainerStatuses[0].ready}')" = "true" ] && break
  sleep 1
done
echo "  after:  restart counts (sidecar, checkout): $(restarts)"
after_started=$(k get pod "$CHECKOUT_POD" -o jsonpath='{.status.containerStatuses[0].state.running.startedAt}')
if [ "$checkout_started" = "$after_started" ]; then
  echo "  checkout's start time is unchanged: $after_started"
else
  echo "  checkout's start time CHANGED: $checkout_started -> $after_started"
fi
k get pods -l app=checkout --no-headers | awk '{print "  " $1 "  READY " $2 "  " $3}'
cat <<'EOF'

  The kubelet restarted the container that died, and only that one. A crash
  does not take a neighbour with it. What the Pod shares is scheduling and
  deletion, which is the next act.
EOF


rule
say "Act 5 — delete the Pod: everything in it goes, and comes back new"
rule
old_ip=$(k get pod "$CHECKOUT_POD" -o jsonpath='{.status.podIP}')
old_uid=$(k get pod "$CHECKOUT_POD" -o jsonpath='{.metadata.uid}')
k delete pod "$CHECKOUT_POD" --wait=true >/dev/null
wait_ready checkout
NEW_POD=$(pod_of checkout)
echo "  deleted $CHECKOUT_POD ($old_ip). the Deployment made $NEW_POD ($(k get pod "$NEW_POD" -o jsonpath='{.status.podIP}'))."
echo "  a new Pod: $([ "$old_uid" != "$(k get pod "$NEW_POD" -o jsonpath='{.metadata.uid}')" ] && echo yes || echo no)"
echo "  restart counts on the replacement (sidecar, checkout): $(k get pod "$NEW_POD" -o jsonpath='{.status.initContainerStatuses[0].restartCount} {.status.containerStatuses[0].restartCount}')"
CHECKOUT_POD=$NEW_POD


rule
say "Act 6 — injection: a sidecar for a service that never mentions one"
rule
sum_before=$(shasum -a 256 k8s/refunds.yaml | cut -c1-12)
echo "  refunds' manifest, k8s/refunds.yaml, sha256 $sum_before, lists these containers: $(grep -c 'name: refunds' k8s/refunds.yaml >/dev/null; k get deployment refunds -o jsonpath='{range .spec.template.spec.containers[*]}{.name} {end}')"
k patch deployment refunds --type=json --patch-file k8s/inject-sidecar.json >/dev/null
REFUNDS_POD=""
for _ in $(seq 1 90); do
  REFUNDS_POD=$(k get pods -l app=refunds -o jsonpath='{.items[?(@.spec.initContainers)].metadata.name}')
  [ -n "$REFUNDS_POD" ] && break
  sleep 1
done
k wait --for=condition=Ready "pod/$REFUNDS_POD" --timeout=120s >/dev/null
sum_after=$(shasum -a 256 k8s/refunds.yaml | cut -c1-12)
echo "  the Pod that is now running lists: $(k get pod "$REFUNDS_POD" -o jsonpath='{range .spec.initContainers[*]}{.name} {end}{range .spec.containers[*]}{.name} {end}')"
echo "  and reads: $(k get pod "$REFUNDS_POD" --no-headers | awk '{print $2}')"
echo "  the manifest the team wrote is unchanged: sha256 $sum_after ($([ "$sum_before" = "$sum_after" ] && echo identical || echo CHANGED))"
cat <<'EOF'

  The sidecar arrived from outside, beside a service whose own manifest does
  not mention it. This was a patch applied by hand. A service mesh does the same
  thing automatically, for every Pod, through an admission webhook -- which
  this project names and does not build.
EOF

say "Deleting the cluster"
