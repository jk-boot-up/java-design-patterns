# Platform Patterns — Category Specification

The fifth category. Six patterns across **eight projects**, numbered 38 to 45,
covering the patterns the microservices category ruled out in its own §8.

The count differs from the pattern count because Sidecar is taught three times —
once per deployment choice — and **each version is a separate project** with its
own number, its own README and its own video. See §2a.

This document fixes what each project is before any of it is written. It is the
contract; [`implementation-plan.md`](implementation-plan.md) is the schedule.

---

## 1. Scope

Six patterns and eight projects, in learning order:

| # | Project | One line |
| --- | --- | --- |
| 38 | `externalised-configuration-pattern` | The number that changes without a deploy |
| 39 | `distributed-tracing-pattern` | Which of the four services made the page slow |
| 40 | `backends-for-frontends-pattern` | One response cannot serve a phone and a desktop |
| 41 | `sidecar-pattern` | The retry code that lives outside the service |
| 42 | `sidecar-java-proxy-pattern` | The same service, with the proxy written in Java |
| 43 | `sidecar-on-kubernetes-pattern` | Two containers in one Pod, which is where sidecars live |
| 44 | `event-sourcing-pattern` | Why is this balance 140? |
| 45 | `strangler-fig-pattern` | Replacing the checkout without a cutover weekend |

Projects 41, 42 and 43 are the same pattern and the same shop service, deployed
three ways. 41 is the default and the one a reader is assumed to run; 42 and 43
are additive, each linking back to 41 and stating in one sentence what it adds.

The order is a dependency order, not a difficulty order. Externalised
Configuration needs nothing. Distributed Tracing needs the idea of a call graph.
Backends for Frontends builds directly on API Gateway (§26). Sidecar needs
"a cross-cutting concern moved out". Event Sourcing needs CQRS (§34) so it can
spend its time being *distinguished* from it. Strangler Fig needs all of them,
and is the capstone.

---

## 2. Why this category exists, and why these six were excluded before

The microservices category's §8 excluded all six, and those reasons were
correct **for that category**, whose binding rule is that everything runs in one
JVM with no network, no broker and no container. Under that rule a pattern
whose entire subject is the platform has nothing left once you simulate it.

This category does not overturn that rule. It changes what is being simulated.

> **The microservices category simulates calls. This category simulates time,
> topology and change.**

That is the whole difference, and it is what makes these six teachable where
they were not before. Concretely, this category adds three harnesses that the
microservices projects do not have:

- **`SimulatedClock` spanning months, not milliseconds.** Strangler Fig is a
  migration measured in months. Compressed into a deterministic timeline it
  becomes a sequence of observable phases.
- **A restartable `Deployment`.** A process that can be stopped, replaced and
  rolled back, so "changed without a redeploy" and "the old version came back"
  are things the demo can actually show rather than assert.
- **A `Topology` the demo can reconfigure.** Routes moved one at a time, a
  proxy inserted in front of a service, a second front door added.

### The honesty rule

Adding those harnesses buys a great deal, but it does not make a single JVM into
a cluster. So this category carries an obligation the others do not:

> **Every project must state, in its explainer, what its simulation does not
> capture — and the video must say it out loud.**

A reader who finishes `sidecar-pattern` believing they have seen a service mesh
has been taught something false. A reader who finishes it knowing they have seen
the *shape* of the decision, and knowing what a real mesh adds, has been taught
something true.

### Rank the six by how well they survive this

This was assessed honestly before committing to the category, and the answer is
not uniform. It is recorded here so nobody has to rediscover it mid-build.

| Project | Survives simulation | Note |
| --- | --- | --- |
| Event Sourcing | **Strongly** | Never needed a network. It was excluded for being large and CQRS-adjacent, not for being unsimulatable. |
| Externalised Configuration | **Strongly** | The whole pattern is a value read from somewhere other than the source file. |
| Distributed Tracing | **Well** | The original objection was "needs a collector and a UI". Answered by rendering the waterfall in the console — which is what the UI would have shown. |
| Strangler Fig | **Well, with the clock** | Months compress into phases. The pattern is the routing decision, and that is code. |
| Backends for Frontends | **Adequately** | Real risk of restating API Gateway. Mitigated by §4.40. |
| Sidecar | **Poorly in one JVM** | Rescued by the second tier below, which is the reason that tier exists. |

---

## 2a. The two tiers: a pure core, and an optional real deployment

Containers, real REST APIs and any open-source framework that is genuinely
needed are permitted in this category. That permission changes what is possible,
and it needs a rule or it will quietly destroy the thing that makes this course
work.

Which frameworks, at which versions, and why each one rather than plain Java, is
settled in [`implementation-plan.md`](implementation-plan.md) § *Framework
register* rather than here. This document says what the projects teach; the plan
accounts for what they depend on.

### Why a rule is needed

The repository's offline guarantee is its most valuable and least visible
asset. Thirty-seven projects run with nothing but a JDK, their tests finish in
under two seconds, and a beginner can clone the repository on a train and run
any of them. A category that requires Docker before it will start has excluded
part of the audience this course is written for, and it will rot: images move,
ports clash, a Spring Boot major version lands and a project that worked last
year does not.

So the permission is used deliberately, not by default.

### The rule

> **Every project has a Tier 1 core that runs offline with only a JDK. Tier 2 is
> optional, additive, and never required to understand the pattern.**

| | Tier 1 — the core | Tier 2 — the real thing |
| --- | --- | --- |
| Runs with | a JDK, offline | Docker, and whichever frameworks the register names |
| Contains | the pattern, the naive version, the failure, the cost | the same pattern at a real process boundary |
| Location | the project root, as in every other category | a `real/` subdirectory with its own README |
| Tests | deterministic, under two seconds, always run | excluded from the default `./gradlew test` |
| The video | is built entirely from this | may show it for two minutes, never depends on it |
| If it is missing | the project is incomplete | the project is still complete |

**The teaching video is built from Tier 1.** A viewer who never installs Docker
must still get the whole pattern. Tier 2 earns at most a short scene near the
end, and that scene is the one that says what the simulation could not show —
which is a better use of it than a separate section making the same claim in
prose.

### REST APIs, and the shop they belong to

Tier 2 may expose **real REST endpoints** that a reader calls with `curl`, and
for several of these patterns that is what makes the difference between being
told something and seeing it. A response you can fetch, measure and diff is
evidence; a method return value described in prose is not.

The e-commerce rule governs the API surface exactly as it governs the code.
Endpoints are shop endpoints and carry the nouns the reader has met across the
previous thirty-seven projects:

```
GET  /api/products/{id}          the product page, in its various shapes
GET  /api/products/{id}/reviews  the slow call in the tracing waterfall
POST /api/carts/{id}/items       the write that triggers a price lookup
POST /api/orders                 the checkout being strangled
GET  /api/orders/{id}            the read the router may serve from either side
GET  /api/customers/{id}/points  the loyalty balance, and why it is 140
GET  /actuator/health            operational, not part of the teaching
```

No `/api/foo`, no `/demo/test`, and no borrowed domain. A reader who has watched
the API Gateway video must recognise these paths.

Three consequences worth fixing now rather than discovering later. The endpoints
are **read-mostly and idempotent** wherever the demo allows, so a reader can run
them repeatedly and get the same answer. Responses are **small enough to print
whole on a slide**, because a payload that needs scrolling cannot be shown in a
video. And every `curl` transcript quoted in a README or spoken in narration is
**real captured output**, under the same rule that governs `./gradlew run`
output everywhere else in this repository.

### Where Tier 2 actually earns its place

Not everywhere. Ranked by how much it adds:

| Project | Tier 2 | Verdict |
| --- | --- | --- |
| **Sidecar** | Two containers sharing a network: the service, and a proxy beside it | **Essential.** This is the project the permission rescues. |
| **Backends for Frontends** | Two REST backends over shared services, both serving the product page | **Strong.** Upgraded by the REST permission — see below. |
| **Externalised Configuration** | Spring Cloud Config Server, a live `@RefreshScope` refresh, and the threshold visible over HTTP | **Strong.** The canonical implementation, and the refresh is observable from outside. |
| **Distributed Tracing** | Micrometer Tracing over real HTTP calls into a collector UI | **Useful.** Propagation across a real network hop, not a method call. |
| **Strangler Fig** | Spring Cloud Gateway routing `/api/orders` between legacy and new | **Useful.** Routing rules as configuration rather than as code. |
| **Event Sourcing** | — | **None. Do not build one.** The pattern is entirely in-process; containers would add a database and teach nothing. |

Tier 2 is expected for the first five and explicitly discouraged for the last. A
project with no Tier 2 is not deficient.

**Backends for Frontends is the second project the permission changes.** It was
marginal when Tier 2 meant only "the same objects, in containers". With real
endpoints it is not: the reader calls the phone backend and the desktop backend
for the same product, and sees two different JSON documents of two visibly
different sizes come back from the same underlying services. The pattern's
entire claim is that one response shape cannot serve two clients, and that claim
is made of responses. Being able to fetch both, side by side, is the argument.

### Paired versions: build both, and give each one its own project

Where a dependency is contested — where taking it would arguably obscure the
lesson — the answer is **not** to pick a side and exclude the other. It is to
build both versions and let them be compared. A reader who sees the same thing
done two ways can judge it; a reader told that one way was rejected has to take
that on trust.

**Each version is a separate project.** Not two variants inside one directory,
and not a `variant-b/` subfolder: a project in this repository is the unit a
viewer consumes — one project, one README, one video, one lesson — so a version
hidden inside another project is a version nobody is taught. Separate projects
also keep the lighter one genuinely light: a reader who never installs Kubernetes
clones a project whose build files do not mention it.

For Sidecar that gives three projects rather than one:

| # | Project | What it is | What it adds over the one before |
| --- | --- | --- | --- |
| 41 | `sidecar-pattern` | Tier 1 in-process, then nginx beside the service on Docker Compose | The default path. The pattern, a real process boundary, a separate lifecycle |
| 42 | `sidecar-java-proxy-pattern` | The identical service image, with a ~40-line Java proxy beside it instead of nginx | Turns "language independent" from a claim into a demonstration, and shows what a proxy actually does |
| 43 | `sidecar-on-kubernetes-pattern` | The same two containers as a Kubernetes Pod | A shared network namespace and lifecycle by definition rather than by configuration; injection; `kubectl` showing `2/2` |

**Project 41 is the default**, and the one a reader is assumed to run. 42 and 43
are additive, are never required by any test in 41, and earn their place only
because the comparison teaches something one project could not.

The pairing is visible from both sides. Each of 42 and 43 opens by naming 41 and
saying in one sentence what it adds, and 41's README links forward to both, so a
reader who stops at 41 knows what they chose not to install.

### Explaining a heavy dependency is part of the deliverable

The audience is beginners, so a dependency is never assumed knowledge. **Any
project that uses Kubernetes, Spring or anything comparable must explain it** —
in a `docs/dependencies.md`, and aloud in the video scene that uses it:

1. **What it is**, in two or three plain sentences, for someone who has never
   used it.
2. **Why it is here** — what this project needed that the lighter variant could
   not provide.
3. **What the reader must install**, with the version pinned, and how long it
   takes.
4. **What it costs** — the setup, the concepts, and the failure modes it adds.
5. **How to skip it**, and confirmation that skipping loses none of the pattern.

A project that runs Kubernetes without explaining Kubernetes has excluded the
people it was written for.

### What Tier 2 costs, and the standing obligations it does not suspend

Every Tier 2 addition is a thing that can break while nobody is looking. It must
pin every image tag and framework version against the category's shared
catalogue, carry its own README with a single command to start and a single
command to stop, and never be on the path of `./gradlew test`.

And the category's honesty rule survives the permission intact. Tier 2 narrows
the gap between the simulation and reality; it does not close it. Two containers
on one laptop are not a fleet, a control plane or a network that partitions. The
**"What this simulation does not show"** section is still required, and for
projects that have a Tier 2 it now has two jobs: what Tier 1 does not show, and
what Tier 2 still does not.

---

## 3. The store, continued

Same online shop, same services, same customers. A reader arriving here has
already met Catalog, Pricing, Orders, Payments, Shipping, Notifications and
Recommendations across thirty-seven projects, and must not have to learn a new
domain to learn a new pattern.

Continuity is load-bearing in this category specifically: Backends for Frontends
must serve the *same* product page the API Gateway project served, and Strangler
Fig must strangle the *same* checkout the Saga project orchestrated. Reusing the
scenario is what lets the project spend its time on the new idea.

---

## 4. The eight projects

Each project shows a naive version failing, then the pattern, then the bill.
The third part is not optional — it is the part most treatments skip and the
reason these projects are worth making.

### 4.38 Externalised Configuration — the free-delivery threshold

**Scenario.** Free delivery over £50. The threshold is a constant in the
checkout code. Marketing wants £35 for one weekend, starting Saturday.

**The naive version.** Change the constant, rebuild, redeploy. The demo shows
the cost honestly: the change is correct, the code review is trivial, and the
weekend promotion still misses its start because a deploy is not a thing you do
at 9am on a Saturday.

**The pattern.** The threshold is read from a configuration source at runtime.
A change takes effect without a rebuild, and the code carries a default so the
service starts even when the source is unreachable.

**The bill — and this is the real lesson.** You have just removed the compiler,
the code review and the test suite from the path of a production change. The
demo must show a bad value — a threshold of `-1`, or the string `"fifty"` —
reaching the running shop in seconds, because that is the thing teams discover
the hard way. Then the mitigations: typed and validated config, a schema, an
audit trail of who changed what, and a rollback that is as fast as the change.

### 4.39 Distributed Tracing — which service made the page slow

**Scenario.** The product page takes 900ms. Four services contribute to it.
Nobody can say which one is at fault.

**The naive version.** Timestamps in four logs. The demo interleaves them the
way a real log aggregator would and asks the viewer to work out where the time
went. It is not possible, and that is the point: with concurrent requests in
flight, you cannot even tell which lines belong to the same customer.

**The pattern.** One trace id created at the front door and propagated through
every call, with each unit of work recording a span — a start, a duration, and a
parent. The demo then prints the waterfall, and the 400ms is visibly in
Recommendations.

That waterfall *is* the collector's UI. Rendering it in the console is not a
substitute for tracing; it is the thing tracing exists to produce.

**Tier 2 — propagation over a real hop.** Tier 1 passes context between method
calls, where losing it takes effort. Over HTTP the trace id has to survive being
written into a header by one service and read out by another, and a service that
forgets to forward it breaks the trace for everything downstream. That is the
failure teams actually meet, and it needs a real request to show.

**The bill.** Every service must be instrumented or the trace breaks at the
first one that is not. Context propagation is the hard part and it silently
fails across thread boundaries and async handoffs — the demo must show a trace
losing its parent when work moves to another thread. And sampling: you cannot
keep every trace, so you keep 1%, and the outage you are investigating is
statistically in the 99% you threw away.

### 4.40 Backends for Frontends — one response, two clients

**Scenario.** The phone app and the desktop site both call the same gateway for
the product page.

**The naive version.** One response shaped for both. The phone downloads a large
payload it cannot use on a slow connection; the desktop is missing two fields
and makes a second call for them. The demo shows the escalation that follows:
`?fields=`, then `?view=mobile`, then a `v2` of the endpoint, until the gateway
is a switchboard nobody will change without fear.

**The pattern.** One backend per frontend. The phone's backend returns what a
phone screen shows; the desktop's returns what a desktop screen shows. Each is
owned by the team that owns its client.

**Guarding against restating API Gateway (§26).** This is the category's main
redundancy risk, and the mitigation is a rule rather than an intention: the
project may not re-teach fan-out, aggregation or the single front door. Those
belong to §26 and this project links to them. Its subject is strictly **the
moment one response shape stops being able to serve two clients**, and what it
costs to split.

**Tier 2 — two real backends.** `GET /api/products/{id}` served by both a phone
backend and a desktop backend, over the same underlying services. The reader
calls each in turn and compares: different fields, different nesting, and a
payload size difference they can read off `curl -s ... | wc -c`. Tier 1 can
assert that the shapes diverge; only this can show it. This is the closing scene
of the video.

**The bill.** Logic duplicated across backends and drifting apart. A third
client means a third backend. And the question that has no clean answer: what do
you do with the code that genuinely is shared — extract a library that now
couples the backends you just decoupled, or accept the duplication?

### 4.41 Sidecar — the retry code that lives outside the service

**Scenario.** Four services each carry their own copy of retry, timeout, metrics
and TLS. A change to the retry policy has to be made four times, and the demo
shows the fourth one being missed.

**The pattern.** The cross-cutting concern moves out of the application process
and into a proxy alongside it. The service talks to the proxy; the proxy does
the retrying. The demo's strongest moment is a diff: the service class after the
move contains business logic and nothing else.

**Tier 1 is honest about being Decorator.** In one JVM, a proxy the service
talks through is a wrapper object, and a wrapper object is Decorator (§11). The
core project says so rather than pretending otherwise, and spends its time on
what the deployment decision buys and costs rather than on the wrapper.

**Tier 2 is the project.** This is the one case in the category where the
optional tier is not an extra — it is the only place the pattern's defining
claim becomes true. Two containers share a network: the Java service in one, and
beside it an off-the-shelf proxy — nginx — in the other. **The proxy is
deliberately not Java in this project**, because the real-world answer is a piece
of infrastructure rather than code you wrote, and hand-rolling it would teach the
re-implementation instead of the pattern. (§42 then builds the Java one on
purpose, for a reason of its own.) The nginx configuration file is committed,
short and commented, and for this project that file is the most important
artefact in the repository. Three things become demonstrable that no simulation
can fake:

1. **A real process boundary.** The service's container has no retry code in it
   at all, and can be inspected to prove it.
2. **A separate lifecycle.** Restart the proxy and the service does not restart.
   Kill the proxy and watch what the service does without it — which is the
   failure mode teams meet first and rarely anticipate.
3. **Language independence.** The proxy does not know or care that the service
   is Java. That is the actual argument for sidecars in a polyglot estate, and
   it cannot be made from inside a JVM.

The video's closing scenes show the two containers running, and they are the
payoff for the whole project. The project's last scene names its two companions —
§42 and §43 — and says in one sentence what each adds, so a reader who stops here
knows what they chose not to install.

**The bill.** You now operate the proxy. A bug in it is a bug in every service at
once. Debugging is harder because there is a hop in the path that nobody on the
team wrote. The latency is real. And the Tier 2 demo should show the
uncomfortable one: the proxy is a second thing that can be down, so you have
added a dependency to every call in order to make calls more reliable.

**Previously this project was a candidate for being dropped**, because in one
JVM it could not teach anything Decorator does not. The container permission is
what changed that, and it is the single largest effect that permission has on
this category.

### 4.42 Sidecar with a Java proxy — the same service, a different neighbour

**What it is.** §41 again, with one thing changed: the proxy beside the service
is a small Java program, roughly forty lines, instead of nginx. The service image
is byte-for-byte identical to §41's, and so is its configuration.

**Why it is a project and not a footnote.** §41 *claims* language independence.
This project *demonstrates* it. The demo starts §41's service with nginx beside
it, stops the proxy, starts the Java proxy in its place, and the service — never
restarted, never reconfigured, never rebuilt — keeps serving the shop. A reader
watches the service neither know nor care what is next to it, which is the actual
argument for sidecars in a polyglot estate. Asserting that from a slide is not
the same thing.

**The second reason is readability.** nginx's behaviour lives in a config file
and a large C program. Forty lines of Java that accept a connection, retry a
failed call and forward the response let a reader see what a proxy *is*. For many
readers this is the project that makes §41 make sense in retrospect.

**The honest warning this project must carry.** A Java proxy beside a Java
service is not what you would deploy. It is a teaching instrument: it costs a
second JVM's memory per service, it re-implements badly what nginx and Envoy do
well, and choosing it in production would be a mistake. The project says this
plainly, in the README and aloud in the video, and points at §41 as the version
to copy.

**The bill.** Everything in §41's bill, plus a proxy you now maintain yourself.
That is the trade real teams refuse, and naming it is the lesson.

### 4.43 Sidecar on Kubernetes — two containers, one Pod

**What it is.** §41's two containers again, deployed as a **Kubernetes Pod**
instead of a Docker Compose file. Same service, same nginx config, different
deployment.

**Why it is a project and not a footnote.** This is where sidecars actually live,
and where a reader will meet the word. Four things become visible that a compose
file can only approximate:

1. **A shared network namespace by definition, not by configuration.** The two
   containers reach each other on `localhost` because they are in one Pod, not
   because a network was wired up for them.
2. **A shared lifecycle.** The Pod is scheduled, restarted and deleted as one
   unit, and the demo shows a container crash taking its neighbour with it.
3. **Injection.** The sidecar arrives beside a service whose own manifest does
   not mention it, which is the mechanism every service mesh is built on.
4. **`kubectl get pods` printing `2/2`** — one logical service, two containers,
   which is the shape of the thing in every production cluster.

**Kubernetes must be explained, not assumed.** It is the largest dependency
anywhere in this course, so §2a's rule applies in full: a `docs/dependencies.md`
says what Kubernetes is in plain language, why this project needs it, what to
install and how long that takes, what it costs in concepts and failure modes, and
that **skipping this project loses none of the pattern** — §41 teaches Sidecar
completely. The video says the same aloud, early, before the first `kubectl`
command.

**The local cluster is part of the deal.** `kind` rather than a cloud cluster:
one pinned binary, one command, no account, no bill. The project's README starts
and stops the cluster in one command each.

**The bill.** Everything in §41's bill, plus a cluster. You have added a
scheduler, a control plane, a YAML dialect and a networking model to a shop that
worked with two containers and a compose file. For a fleet that is a bargain; for
four services it is the reason "do you need Kubernetes yet?" is a real question,
and the project answers it honestly rather than selling the cluster.

### 4.44 Event Sourcing — why is this balance 140?

**Scenario.** A customer's loyalty balance says 140 points. Support is asked why.

**The naive version.** A current-state row: `points = 140`. The question is
simply unanswerable — the row knows the balance and nothing about how it got
there. The demo makes this land by having a bug double-award points, and then
showing that after the fact there is no way to tell an affected customer from an
unaffected one, because the evidence was overwritten by the thing that went
wrong.

**The pattern.** Store the facts, not the conclusion. An append-only log of
events — `PointsAwarded`, `PointsRedeemed`, `PointsExpired` — and the balance
becomes a fold over that log. The demo then does three things a current-state
row cannot: answer *why* it is 140, rebuild the balance from scratch after a bug
is fixed, and answer what it was on the 3rd of March.

**The bill, which is heavy and must not be softened.** Events are a schema you
can never migrate, only version, because you cannot rewrite history. Long
streams need snapshots, which is a second mechanism with its own staleness.
Deleting a customer's data is genuinely hard when your store is append-only, and
"just delete the events" defeats the point of having them.

**And the confusion this project exists to end:** Event Sourcing is not CQRS.
CQRS (§34) separates the read path from the write path. Event Sourcing changes
what the write path *stores*. You can have either without the other, and the
project must show one of each, briefly, so the distinction is concrete rather
than asserted.

### 4.45 Strangler Fig — replacing the checkout without a cutover weekend

**Scenario.** The legacy checkout is one large class that does pricing, stock,
payment and email. It works. It is also where every change is slow and every
incident starts.

**The naive version.** The big-bang rewrite. The demo runs it on a compressed
timeline: months of parallel work, a cutover weekend, and a failure on the
Monday where the only available rollback is all-or-nothing, so a fault in one
capability takes the whole checkout back.

**The pattern.** A router in front of the legacy checkout. Capabilities move
across one at a time, each with its own switch. Pricing goes first; if it
misbehaves, pricing alone comes back. The demo runs shadow reads — both
implementations called, results compared, differences reported — so a route is
moved on evidence rather than on hope.

**The bill.** Two systems are live for months and both must be maintained. Data
has to stay consistent across both while the fig grows. And the failure mode
that actually happens in the field: the migration stalls half-finished, budget
moves elsewhere, and the organisation lives with two checkouts forever — which
is worse than either endpoint. The project must name that, because it is the
most likely outcome and nobody warns about it.

---

## 5. Relationships to the existing thirty-seven

Each project states its cross-reference explicitly. These are the ones that
carry teaching weight:

| Project | Depends on | Why |
| --- | --- | --- |
| Backends for Frontends | API Gateway (§26) | It is the same front door, split. Must not restate it. |
| Distributed Tracing | API Gateway (§26), API Composition (§33) | The trace id is minted at the front door and spans the fan-out. |
| Sidecar | Decorator (§11), Retry (§29), Circuit Breaker (§30) | The mechanism is Decorator; the concerns moved out are §29 and §30. |
| Event Sourcing | CQRS (§34), Transactional Outbox (§36) | Distinguished from the first; the second is how events leave the service. |
| Strangler Fig | Saga (§35), Facade (§12) | It strangles the checkout Saga orchestrates; the router is a Facade with a switch. |
| Externalised Configuration | Circuit Breaker (§30) | Its thresholds are the most-tuned numbers in the category. |

---

## 6. Deliverables per project

Identical to the microservices category — same twenty-two committed files, same
shapes, same generators. [`../../micro-services-design-patterns/docs/ai-build-spec.md`](../../micro-services-design-patterns/docs/ai-build-spec.md)
is the authority on how they are produced and is not restated here.

Three additions specific to this category:

- The explainer carries a **"What this simulation does not show"** section. Not
  a footnote — a named section, placed before the costs. Where the project has a
  Tier 2, the section covers both gaps: what the core does not show, and what
  two containers on a laptop still do not.
- The video says the same thing aloud, in the scene before the outro.
- Projects with a Tier 2 add a `real/` subdirectory holding it, with its own
  `README.md` giving one command to start and one to stop, pinned image tags and
  a pinned Spring Boot version. It is excluded from the root `settings.gradle`
  so `./gradlew test` never reaches it.
- Where Tier 2 exposes REST endpoints, its README lists every path with a
  ready-to-paste `curl` line and the **real captured response** beneath it. The
  endpoints use the shop's nouns (§2a). A reader should be able to work through
  that README without reading any Java.

---

## 7. Video, poster and publishing

Unchanged: 14 to 16 scenes, `Samantha` at 145 wpm, −16 LUFS, a poster that does
not strike out its message, an outro that names no successor pattern, and an
opening that states what the video is, credits Jayasekhar Konduru, gives the
pattern in plain words, then puts it in the shop.

**Target length is eleven to thirteen minutes.** The microservices category ran
to 16–18 and the last two projects, at around eleven, are the better watch. This
category takes the shorter target as the standard rather than drifting back.

---

## 8. Deliberately not included

| Pattern | Why not |
| --- | --- |
| Service Mesh, as a project of its own | It is Sidecar at fleet scale plus a control plane. §4.43 already goes as far as a Kubernetes Pod, which is the honest edge of what one laptop shows; adding Istio or Linkerd on top would make that project a mesh tutorial rather than a pattern lesson. Covered as a section of §4.43, which names what a real mesh adds beyond the Pod. |
| Health Check API | A method returning `OK`. The interesting part is what the orchestrator does with it, and that is the orchestrator's behaviour, not the service's. |
| Log Aggregation | An operational concern with no design decision visible in the code a reader would write. The teachable half is the correlation id, which belongs to §4.39. |
| Ambassador | A sidecar for outbound calls specifically. The same objection as Service Mesh, with less to say. |
| Blue-Green and Canary Deployment | Deployment strategies rather than design patterns. They share Strangler Fig's routing machinery but none of its design content. |

A seventh *pattern* requires editing this section first. That rule is what stops
the category becoming a survey.

---

## 9. Conformance

Every item from the microservices category's §9 applies, plus thirteen:

- [ ] The explainer has a **"What this simulation does not show"** section, and
      the video says it aloud.
- [ ] The project states its cross-reference from §5, and does not re-teach the
      pattern it depends on.
- [ ] The demo shows the pattern's **cost**, not only its benefit, as runnable
      output — not as a paragraph of prose.
- [ ] Runtime is between eleven and thirteen minutes.
- [ ] **Tier 1 runs offline with only a JDK**, and `./gradlew test` passes with
      Docker absent from the machine. This is the item to check by actually
      stopping Docker, not by reasoning about it.
- [ ] **The video is comprehensible to a viewer who never runs Tier 2.** Tier 2
      appears in at most one scene.
- [ ] Any `real/` directory pins every image tag and framework version against
      the category catalogue, and its README gives one command to start and one
      to stop.
- [ ] **Every dependency and every image the project uses has a row in the
      plan's framework register**, with a reason that is stronger than
      convenience.
- [ ] **Any proxy, gateway or collector configuration is committed, short and
      commented**, and a reader can follow it without knowing the product. Where
      the config expresses the pattern, it is read aloud in the video rather
      than shown silently.
- [ ] **Where a version of a pattern is built with a dependency, it is its own
      project** — its own number, README, documents and video — and it names the
      lighter project it pairs with in its first paragraph and in its opening
      scene. The lighter project links forward to it.
- [ ] **Every heavy dependency has a `docs/dependencies.md`** answering §2a's
      five questions — what it is, why it is here, what to install, what it
      costs, and that skipping it loses none of the pattern — and the video says
      it aloud.
- [ ] **Every REST path uses the shop's nouns** — products, carts, orders,
      payments, customers — and nothing is named `foo`, `test` or `demo`.
- [ ] **Every `curl` transcript quoted anywhere is real captured output**, and
      every response shown on a slide fits on it without scrolling.
