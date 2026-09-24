# Prerequisites

## Required

- **A container runtime**, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later, with about 1 GB of memory free. kind runs the Kubernetes node as a container inside it.
- **kind**, version 0.33.0 or later, on the `PATH`. On a Mac, `brew install kind`; elsewhere, see kind.sigs.k8s.io. kind creates the one-node cluster the demo uses and deletes it at the end.
- Without either, the demo prints two sentences saying what to do, and stops. The tests that need a cluster are skipped, and the rest still run.
- The plain-Java Leader Election project in this course, which this project pairs with. Read it first: this project does not re-teach the pattern.

## Explicitly not required

- No `kubectl`. The demo talks to the API server through the Fabric8 Java client.
- No existing Kubernetes cluster, and no change to your own Kubernetes settings. The demo gives kind a private file for the cluster's address, so `~/.kube/config` is never touched.
- No prior Kubernetes. Every word it introduces — cluster, node, API server, Lease, holder, renewal, resource version, 409 Conflict — is said in plain language before the name for it is used.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and the kind node image, about 1 GB; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| kind | 0.33.0 |
| Kubernetes, as the kind node image | `kindest/node:v1.37.0`, pinned by digest |
| `io.fabric8:kubernetes-client` | 8.0.0 |
| `io.fabric8:kubernetes-httpclient-jdk` | 8.0.0 |
| `org.slf4j:slf4j-simple` | 2.0.20 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built. None is held back.
