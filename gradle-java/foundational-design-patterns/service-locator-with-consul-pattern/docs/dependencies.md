# Dependencies

This project uses three things the hand-built projects do not: Consul, Docker and nginx. This page says what
they are, why they are here, and what they cost. It comes before the first line of code on purpose.

**Skipping this project loses none of the pattern.** [Service Locator](../service-locator-pattern) teaches all
of it with plain Java, including `java.util.ServiceLoader`, the standard-library form.

## What Consul is

Consul is a service registry. Services register themselves with a name, an address and a health check, and
callers ask for the healthy instances of a name. It is written in Go and ships as one binary. This project runs
it in **development mode as a local process**, on ports it chooses at run time, and stops it when the run ends.

## What Docker and nginx are

nginx is a web server and reverse proxy. Docker runs it in a container. Here nginx sits in front of the service
instances and shares their traffic, so the caller needs one address and no lookup.

## Why this project uses them

Real service discovery cannot be shown honestly with a simulation: the stale cache and the failing instance
need a real agent. And server-side discovery needs a real proxy.

## What to install

| What | Version | Needed for |
| --- | --- | --- |
| A JDK | 21 | Everything |
| Consul | 1.16 or newer, on the PATH | Acts one to four, and the tests |
| Docker | any recent version | Act five only |
| The nginx image | `nginx:1.31.5-alpine` | Act five only |

Without `consul` on the PATH the demo says so and stops, and the tests are skipped rather than failed. Without
Docker, only act five is skipped.

## What it costs

Consul starts in under a second and uses a few tens of megabytes. The nginx image is about seventy megabytes.
Nothing is left running: the agent is stopped when the run ends, and the container is removed. The demo instances
listen on every interface for the length of the run, on ephemeral ports, and answer only with an echo, because a
container reaches the host through `host.docker.internal`.

Act five relies on Docker Desktop providing `host.docker.internal`. On Linux, the container would also need
`--add-host host.docker.internal:host-gateway`.

## Where this pattern lives

In every service-discovery client: Spring Cloud's `DiscoveryClient`, a Consul or Eureka library, and the
service-name lookups inside a service mesh.
