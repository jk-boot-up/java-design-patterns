# Platform Patterns

The fifth category. Six patterns, in eight projects, whose subject is the
platform around a service, or the shape of a system as it changes over time.

**Status: all eight are built.** Each has Tier 1 (offline, a JDK) and, for the Sidecar projects and Strangler
Fig, a Tier 2 that runs the real thing (Docker Compose, or a `kind` cluster). The two documents below fixed
what all eight are before any of them was written.

- [`docs/spec.md`](docs/spec.md) — the scenario each pattern is taught through,
  the naive version it must show failing, the cost it must admit to, and what
  its simulation cannot honestly claim.
- [`docs/implementation-plan.md`](docs/implementation-plan.md) — the order the
  eight get built in, and the rules that keep the build from having to redo
  itself.

## The eight projects

| # | Pattern | Scenario |
| --- | --- | --- |
| 38 | [Externalised Configuration](externalised-configuration-pattern) | The free-delivery threshold that changes without a deploy |
| 39 | [Distributed Tracing](distributed-tracing-pattern) | Which of four services made the product page slow |
| 40 | [Backends for Frontends](backends-for-frontends-pattern) | One response cannot serve a phone and a desktop |
| 41 | [Sidecar](sidecar-pattern) | The retry code that lives outside the service |
| 42 | [Sidecar with a Java proxy](sidecar-java-proxy-pattern) | The same service, with the proxy written in Java |
| 43 | [Sidecar on Kubernetes](sidecar-on-kubernetes-pattern) | Two containers in one Pod, which is where sidecars live |
| 44 | [Event Sourcing](event-sourcing-pattern) | Why is this customer's loyalty balance 140? |
| 45 | [Strangler Fig](strangler-fig-pattern) | Replacing the checkout without a cutover weekend |

Sidecar is taught three times because the deployment *is* the pattern, and
**each version is a separate project** — its own README, its own video, its own
lesson. Project 41 is the default; 42 and 43 are additive and each says in one
sentence what it adds over 41. A reader who only ever runs 41 has learned
Sidecar.

## Why these six, and why they were excluded before

All six were ruled out by the microservices category's
[`spec.md`](../micro-services-design-patterns/docs/spec.md) §8, and those reasons
were correct for that category, whose binding rule is that everything runs in one
JVM with no network, no broker and no container.

This category does not overturn that rule. It changes what is simulated: the
microservices projects simulate **calls**, and these simulate **time, topology
and change** — a clock spanning months, a deployment that can be restarted and
rolled back, and a topology the demo can reconfigure while it runs.

That buys a great deal, but it does not turn one JVM into a cluster. So every
project here carries an obligation the other categories do not: a named section
in its explainer saying **what its simulation does not show**, repeated aloud in
the video. A reader who finishes the Sidecar project believing they have seen a
service mesh has been taught something false.

## Two tiers

Containers, real REST APIs and any open-source framework that is genuinely
needed are permitted here, which the other four categories do not allow. They
are used deliberately rather than by default, because the offline guarantee —
every project running with nothing but a JDK — is this course's least visible and
most valuable property.

Every framework the category uses is accounted for in the plan's **framework
register**, with a pinned version and a reason stronger than convenience. A
dependency is a plan edit before it is a build edit.

So each project has **two tiers**:

- **Tier 1** is the core. Plain Java, offline, deterministic tests under two
  seconds. It holds the pattern, the naive version, the failure and the cost.
  The teaching video is built entirely from it. A viewer who never installs
  Docker gets the whole pattern.
- **Tier 2** is optional and additive: the same pattern at a real process
  boundary, with real HTTP endpoints you can call, in a `real/` subdirectory,
  never on the path of `./gradlew test`. It earns at most one scene near the end
  of the video.

Tier 2 is expected for five of the six patterns and explicitly discouraged for Event
Sourcing, whose pattern is entirely in-process and would gain nothing but a
database.

The endpoints stay in the shop — `/api/products/{id}`, `/api/orders`,
`/api/customers/{id}/points` — because the e-commerce rule governs the API
surface just as it governs the code, and a reader who has watched the API
Gateway video should recognise the paths.

**Two projects are what these permissions rescue.** In one JVM, a proxy you call
through is just Decorator, so **Sidecar** was previously a candidate for being
dropped; two containers sharing a network make its defining claims real — a
service image containing no retry code, a proxy you can kill independently, and
a boundary that does not care the service is Java. In project 41 the proxy is
nginx rather than anything written here, because the real-world answer is a piece
of infrastructure and hand-rolling it would teach the re-implementation instead
of the pattern; its short commented config file ends up being the project's most
important artefact. Projects 42 and 43 then take the two choices that are worth
arguing about and build them out properly: 42 swaps in a forty-line Java proxy
under an unchanged service, which *demonstrates* language independence rather
than claiming it, while warning that you would not deploy it; 43 moves the same
two containers into a Kubernetes Pod, where sidecars actually live, and explains
Kubernetes from scratch in its own `docs/dependencies.md` — including that
skipping it loses none of the pattern. **Backends for Frontends** was
the redundancy risk against API Gateway; with two real backends you can fetch the
same product from each and see two differently shaped, visibly different-sized
responses come back, which is the pattern's entire argument and something a
single gateway cannot show. [`docs/spec.md`](docs/spec.md) §2 and §2a give the
full reasoning and rank all six honestly.

## Where this sits

Projects 38 to 45, after the twenty-five object-oriented patterns and the twelve
microservices ones. See [`../README.md`](../README.md) for the full course.
