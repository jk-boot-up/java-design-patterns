# Blue-Green and Canary with Kubernetes Pattern

```
src/main/java/com/jk/explore/bgk8s/
├── BlueGreenK8sDemo.java        the six acts
├── Cluster.java                 makes a kind cluster; scales, selects, counts pods
├── Traffic.java                 sends requests, one new connection each
├── Shell.java                   runs kind and kubectl
src/main/resources/k8s/
├── kind-config.yaml             the cluster, with two ports mapped to this machine
└── checkout.yaml                v1 and v2 as Deployments, and two Services
```

**On Kubernetes, blue-green is a Service selector, and a canary is replica counts. The cluster does the spreading.**

This project is the framework version of [Blue-Green and Canary](../blue-green-and-canary-pattern). That project built the mechanism by hand. This one shows the same idea inside Kubernetes. It does not re-teach the pattern. It shows what Kubernetes adds, the failures that are its own, and what it costs.

## Run

```bash
./gradlew run
```

Six acts. The partner project, Blue-Green and Canary, built the mechanism by hand. Here the same idea runs through Kubernetes, and every count comes from real output.

```
ONE. Replace it where it stands.
  v1 stopped to make room for v2. 20 requests while nothing is running: failed 20 of 20.
TWO. Blue and green.
  v2 is running beside v1, and only a test port reaches it. test request to v2: v2.
  20 requests before the switch: {v1=20}. the switch is one patch to the service. 20 after: {v2=20}, failed 0.
THREE. Going back.
  v2 has a bug with big orders. 20 big orders on v2, failed: 20.
  one patch sent the service back to v1, whose pods had never stopped. 20 big orders, failed: 0.
FOUR. A canary.
  9 pods of v1 and 1 of v2, behind one service. 300 big orders: failed 24, which is a small share, as a canary should be.
  the spread is chosen by the cluster's own rules, so the exact count changes from run to run.
  had all 300 gone to v2, all 300 would have failed. a few customers found the bug, not everyone.
FIVE. Promote in steps, with a gate.
  the gate caught it at the first step.
  steps of 1, 5 and 10 pods of v2, and a gate at 5 failures in 100. buggy v2: halted true, and every pod is v1 again.
SIX. The bill.
  during a blue-green switch both releases are fully running: 4 pods, where one release needs 2.
  both releases share one database, so a release that changes the data cannot be switched back safely.
  and a cluster is a lot to run for a checkout: a control plane, a node, an image, a service and two deployments.
```

## Test

```bash
./gradlew test
```

1 test classes, 2 test methods, offline, with each Spring context started inside the test, and no server.

## Technologies and versions

| What | Version | Why it is here |
| --- | --- | --- |
| Java | 21 | The repository standard, via the Gradle toolchain block |
| Gradle | 9.2.1 | The wrapper in this directory |
| Docker | 24+ | Runs the cluster |
| kind | 0.33+ | A Kubernetes cluster in a container |
| kubectl | 1.30+ | Called by the demo |
| nginx | alpine | The two releases of the checkout |
| JUnit 5 | 5.10.2 | Test runner; the cluster test is skipped when the tools are missing |

See [`docs/dependencies.md`](docs/dependencies.md).

## Learning Material

| Document | What it covers |
| --- | --- |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The partner's router, and what is new |
| [`docs/blue-green-and-canary-with-kubernetes-pattern-explained.md`](docs/blue-green-and-canary-with-kubernetes-pattern-explained.md) | A real cluster, and its real spread |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types |
| [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | A Service, two Deployments and traffic |
| [`docs/data-flow-diagram.md`](docs/data-flow-diagram.md) | How a release goes live |
| [`docs/sequence-diagram.md`](docs/sequence-diagram.md) | Written for a listener with the screen off |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Four sequences |
| [`docs/animation.html`](docs/animation.html) | The six acts in a browser |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What you need to know |
| [`docs/session.md`](docs/session.md) | A one-hour taught session |
| [`docs/spec.md`](docs/spec.md) | The generated specification |
| [`docs/youtube.md`](docs/youtube.md) | Title, description and chapters |
| [`docs/dependencies.md`](docs/dependencies.md) | What Kubernetes is, what it costs, and that skipping this project loses none of the pattern |

### The pattern in one picture

![Class diagram](docs/images/class-diagram.png)

### Where each piece sits

![Architecture diagram](docs/images/architecture-diagram.png)

### How one request moves

![Data flow diagram](docs/images/data-flow-diagram.png)

### Who calls whom, in order

![Sequence diagram](docs/images/sequence-diagram.png)

### All four sequences

![Sequence one](docs/images/uml-diagram.png)

![Sequence two](docs/images/uml-diagram-2.png)

![Sequence three](docs/images/uml-diagram-3.png)

![Sequence four](docs/images/uml-diagram-4.png)

### Video

Built from [`video/scenes.py`](video/scenes.py) by
[`video/build_video.sh`](video/build_video.sh). The rendered file is not
committed; see the repository README for why.

## Where you have already met this

Kubernetes platforms and their release tools.

## When this is too much

For an internal tool where a short outage is fine, a plain restart is enough, and a cluster is a lot to run for one service.

## Where this sits

This project pairs with [Blue-Green and Canary](../blue-green-and-canary-pattern), and is a framework version in [`platform-design-patterns`](..).
