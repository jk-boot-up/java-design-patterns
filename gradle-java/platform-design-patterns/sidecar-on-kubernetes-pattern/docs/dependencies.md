# Dependencies

Tier 1 needs only a JDK. **Tier 2**, in [`real/`](real/), uses Kubernetes, the heaviest dependency in this
course, so this page explains it before anything uses it.

**Skipping this project loses none of the pattern.** [`sidecar-pattern`](../sidecar-pattern) teaches Sidecar
completely, and [`sidecar-java-proxy-pattern`](../sidecar-java-proxy-pattern) shows the proxy swap.

## 1. What Kubernetes is

Kubernetes is a system that runs containers across one or many machines and keeps them running. You describe
what you want, for example "one copy of checkout, with a proxy beside it", in a file. Kubernetes makes it
true, and keeps making it true: if a container dies it restarts it, and if a machine dies it starts the
container somewhere else. The unit it schedules is a **Pod**: one or more containers that are placed
together, share one network, and live and die as one.

## 2. Why this project uses it

A Pod is the thing a sidecar is designed around, and a Compose file can only approximate it. Shared network by
definition, one lifecycle, injection and `READY 2/2` cannot be shown honestly without one.

## 3. What to install

| What | Version | How long |
| --- | --- | --- |
| Docker | any recent version, running | Already needed for the Sidecar projects |
| `kind` | 0.33.0 | one binary, under a minute |
| `kubectl` | any recent version | one binary, under a minute |

`kind` ("Kubernetes in Docker") runs a whole cluster as one Docker container. It needs no cloud account, has no
bill, and is removed with one command. The node image `kind` pulls is about a gigabyte, downloaded once.

## 4. What it costs

- **Setup:** the first cluster takes a couple of minutes, mostly the image pull.
- **Concepts:** Pod, Deployment, Service, ConfigMap, Secret and namespace, six words you did not need with
  two containers and a file.
- **Failure modes:** a Pod stuck in `Pending`, an image that is not on the node, and a manifest that is valid
  YAML and still wrong.
- **Machine:** a cluster in Docker uses noticeable memory. Delete it when you are done.

## 5. How to skip it

Do not run Tier 2. Read [`real/README.md`](real/README.md) for the transcript, which is real output. Tier 1 and
its tests need no cluster and no Docker, and nothing in the default `./gradlew test` touches one.
