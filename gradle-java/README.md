# Design Patterns in Java — A Worked Course

Design patterns in Java — the twenty-five object-oriented ones first, then
twelve microservices patterns, then eight platform patterns, then six
concurrency patterns, then five architectural patterns — each a
self-contained Gradle Java 21 project with runnable code, JUnit 5 tests,
written notes, diagrams, an animated walkthrough, and a narrated video.

The first four categories — creational, structural, behavioural and
microservices — are complete, and so is architectural, the fifth. Platform
and concurrency are the two categories still being built; see their
sections below.

**Every pattern is taught through the same worked domain: an online store.**
Not a photo gallery, not shapes on a canvas — checkout, catalog, orders,
shipping, payments. The projects are meant to be worked through in sequence, so
a learner who has already met orders, carts and couriers in the previous
project spends none of their attention re-learning the setting and all of it on
the structure being introduced.

Start with [`creational/simple-factory-pattern`](creational/simple-factory-pattern)
and follow the order below.

---

## Creational — making objects

| # | Pattern | What it buys you |
| --- | --- | --- |
| 1 | [Simple Factory](creational/simple-factory-pattern) | Let data choose the class — payment methods |
| 2 | [Static Factory](creational/static-factory-pattern) | Give the constructor a name — discounts |
| 3 | [Factory Method](creational/factory-method-pattern) | One step, left to the subclass — delivery tiers |
| 4 | [Abstract Factory](creational/abstract-factory-pattern) | Choose the whole family at once — regional checkout |
| 5 | [Builder](creational/builder-pattern) | Decide it a piece at a time — purchase orders |
| 6 | [Prototype](creational/prototype-pattern) | Copy the one you already have — product listings |
| 7 | [Singleton](creational/singleton-pattern) | Exactly one, actually enforced — order numbers |

Simple Factory and Static Factory are not in the Gang of Four book. They are
here because they are the idioms everyone actually meets first, and because
Factory Method and Abstract Factory both grow out of them.

## Structural — arranging objects

| # | Pattern | What it buys you |
| --- | --- | --- |
| 8 | [Adapter](structural/adapter-pattern) | One class translates, not every caller — a shipping SDK |
| 9 | [Bridge](structural/bridge-pattern) | Two hierarchies varying independently — notifications × channels |
| 10 | [Composite](structural/composite-pattern) | One tree, one interface, zero `instanceof` — the catalog |
| 11 | [Decorator](structural/decorator-pattern) | Wrap it, don't subclass it — gift wrap and insurance |
| 12 | [Facade](structural/facade-pattern) | One door in front of many — placing an order |
| 13 | [Flyweight](structural/flyweight-pattern) | Stop paying for the same data twice — catalog badges |
| 14 | [Proxy](structural/proxy-pattern) | Same interface, it controls the door — product images |

## Behavioural — how objects decide and talk

All eleven are complete. See
[`behavioural/docs/spec.md`](behavioural/docs/spec.md) for the scenario each
pattern is taught through and why, and
[`behavioural/docs/implementation-plan.md`](behavioural/docs/implementation-plan.md)
for the order they were built in.

| # | Pattern | Scenario |
| --- | --- | --- |
| 15 | [Strategy](behavioural/strategy-pattern) | Swap the rule, not the code — shipping cost rules |
| 16 | [Observer](behavioural/observer-pattern) | Tell everyone, know no one — order status events |
| 17 | [Command](behavioural/command-pattern) | Make the action an object — undoable cart edits |
| 18 | [Template Method](behavioural/template-method-pattern) | Fix the steps, vary the how — the fulfilment workflow |
| 19 | [State](behavioural/state-pattern) | Behaviour follows the state — the order lifecycle |
| 20 | [Chain of Responsibility](behavioural/chain-of-responsibility-pattern) | Each link answers or passes it on — checkout screening |
| 21 | [Iterator](behavioural/iterator-pattern) | Hide how the walk really works — paging the catalog |
| 22 | [Mediator](behavioural/mediator-pattern) | Components talk through one hub — the checkout page |
| 23 | [Memento](behavioural/memento-pattern) | Snapshot it, restore it, safely — restoring a saved cart |
| 24 | [Visitor](behavioural/visitor-pattern) | New reports, untouched model — catalog reports |
| 25 | [Interpreter](behavioural/interpreter-pattern) | Turn a rule into a tree — promotion rules |

## Microservices — one shop, many services

The same online store, split across services that talk over a network. These
are not Gang of Four patterns, and they are here because the twenty-five above
stop short of the questions a service raises: what happens when the thing you
called does not answer, has moved, is slow, or answers twice.

The category's own [`docs/spec.md`](micro-services-design-patterns/docs/spec.md)
says which scenario each pattern is taught through and why. Every project runs
in one JVM with nothing installed but a JDK — no Spring, no Docker, no broker
and no sockets — because a simulated clock and a simulated network make the
timings exact and the failures repeatable.

| # | Pattern | Scenario |
| --- | --- | --- |
| 26 | [API Gateway](micro-services-design-patterns/api-gateway-pattern) | One call from the phone, not seven — the product page |
| 27 | [Service Registry and Discovery](micro-services-design-patterns/service-discovery-pattern) | Ask where it is, don't hard-code it — finding Catalog |
| 28 | [Client-Side Load Balancing](micro-services-design-patterns/load-balancing-pattern) | Spread the calls, skip the sick one — three Catalog instances |
| 29 | [Retry with Backoff](micro-services-design-patterns/retry-pattern) | Try again, but not immediately — a blip in Pricing |
| 30 | [Circuit Breaker](micro-services-design-patterns/circuit-breaker-pattern) | Stop calling what is down — Recommendations |
| 31 | [Bulkhead](micro-services-design-patterns/bulkhead-pattern) | One slow service must not sink the page — thread pools |
| 32 | [Database per Service](micro-services-design-patterns/database-per-service-pattern) | The join you can no longer write — orders and names |
| 33 | [API Composition](micro-services-design-patterns/api-composition-pattern) | Gather in parallel, decide what to do with a gap — order details |
| 34 | [CQRS](micro-services-design-patterns/cqrs-pattern) | Keep the page ready — the order history |
| 35 | [Saga](micro-services-design-patterns/saga-pattern) | No transaction spans five services — placing an order |
| 36 | [Transactional Outbox](micro-services-design-patterns/transactional-outbox-pattern) | Save it and announce it, or neither — the order event |
| 37 | [Idempotent Consumer](micro-services-design-patterns/idempotent-consumer-pattern) | The same message, twice — one confirmation email |

## Platform — what the system stores, and how it is run

The same online store again, but the questions are now about the platform it
runs on rather than the calls between services: where configuration comes from,
how a request is followed across machines, what is actually kept in storage, and
how a system too big to rewrite gets replaced anyway.

This category is **under construction**. Its
[implementation plan](platform-design-patterns/docs/implementation-plan.md) is
the authority on what each project will contain; the table below links the ones
that exist.

It is also the first category to allow real infrastructure, under a rule worth
knowing before you start. **Tier 1** of every project runs offline with only a
JDK, and the teaching video is built entirely from Tier 1 — so a learner who
installs nothing still gets the whole lesson. **Tier 2** is optional and
additive: it lives in a `real/` subdirectory, is excluded from `./gradlew test`,
and is where Spring Boot, Docker or Kubernetes may appear for anyone who wants
to see the pattern against the real thing.

| # | Pattern | Scenario |
| --- | --- | --- |
| 38 | [Externalised Configuration](platform-design-patterns/externalised-configuration-pattern) | The threshold you must not redeploy to change — free delivery |
| 39 | [Distributed Tracing](platform-design-patterns/distributed-tracing-pattern) | Four healthy services, one slow page — which of them spent the time? |
| 40 | [Backends for Frontends](platform-design-patterns/backends-for-frontends-pattern) | Six fields on a phone, fifteen on a desktop — one endpoint fits neither |
| 41 | [Sidecar](platform-design-patterns/sidecar-pattern) | The concern that travels beside the service, not inside it |
| 42 | [Sidecar (Java proxy)](platform-design-patterns/sidecar-java-proxy-pattern) | The same sidecar, written as a Java proxy |
| 43 | Sidecar (on Kubernetes) | The same sidecar again, as a real second container |
| 44 | [Event Sourcing](platform-design-patterns/event-sourcing-pattern) | Store the facts, not the total — why is this balance 140? |
| 45 | Strangler Fig | Replacing a system you are not allowed to switch off |

Event Sourcing is the category's reference project and is finished. It was built
first because it is the most demanding of the eight and the one that most needs
its costs shown honestly: three of its nine acts are spent on what the pattern
costs rather than what it buys. Externalised Configuration is finished too, and
is deliberately the gentlest of the eight — it depends on none of the others, so
the listed order is a dependency order for the material rather than a difficulty
order. Distributed Tracing is finished as well, and follows the same shape: the
pattern is one string field naming a span's parent, and three of its seven acts
are spent on the three ways the resulting picture can be wrong without anything
throwing. Backends for Frontends is finished in both tiers. It spends its first five
scenes on the problem for a reason: the obvious fix — asking a shared endpoint
for only the fields you want — is shown *working*, and reaching the same byte
count the pattern does, before the one request it cannot serve arrives. Sidecar
is finished in Tier 1. Its incident is an absence rather than a mistake — a
retry policy that four services each hold a copy of, changed in three of them
and missed in the fourth because there was no fourth place to look — and its
last four scenes are the bill: twice as many processes, a second thing that can
be down, one millisecond on every call, and the admission that inside one JVM
this structure is Decorator.

## Concurrency — more than one thing happening at once

The same online store, but the question this time is what happens when two
threads reach for the same shared state together: the stock count for one
product, decremented by every checkout. This is where a beginner's mental
model of Java breaks first, and it breaks quietly — the code looks right,
the tests pass, and it is wrong only on a busier machine. The category's
whole discipline is answering that: **every naive failure is forced to
reproduce on every single run**, with a latch, a barrier or a planned
interleaving — never a `Thread.sleep`, and never a bug that only shows up
"sometimes".

This category is **under construction** — three of six projects built. Its
[implementation plan](concurrency-design-patterns/docs/implementation-plan.md)
is the authority on what each remaining project will contain.

| # | Pattern | Scenario |
| --- | --- | --- |
| 46 | [Producer–Consumer](concurrency-design-patterns/producer-consumer-pattern) | Orders arrive faster than they are packed |
| 47 | [Thread Pool](concurrency-design-patterns/thread-pool-pattern) | A thread per order, until the server stops |
| 48 | [Future/Promise](concurrency-design-patterns/future-promise-pattern) | A result you are promised but do not have yet |
| 49 | Read–Write Lock | A thousand readers and one price change |
| 50 | Monitor Object | The object that guards its own state |
| 51 | Active Object | A method call that returns before the work does |

The order is a dependency order: Producer–Consumer introduces the bounded
queue; Thread Pool is what actually consumes it; Future/Promise is how a
caller gets an answer back from either; Read–Write Lock and Monitor Object
are the two ways the shared stock count gets protected; and Active Object
is the capstone, assembling a queue, a thread, a future and an
object that owns its own state into one idea, re-teaching none of them.

## Architectural — where a dependency is allowed to point

The same online store one more time, but the question is now the shape of the
codebase itself: which layer is allowed to know about which, and what happens
when someone takes a shortcut across that rule. All five projects implement
**the same feature** — a customer places an order for three products, stock is
checked, payment is taken, a confirmation is sent — so the only thing that
differs between them is the arrangement, and a reader can compare projects
directly instead of taking anyone's word for which one is cleaner.

This category is **complete** — all five projects built. Its
[implementation plan](architectural-design-patterns/docs/implementation-plan.md)
is the authority on how it was built and in what order.

| # | Pattern | Scenario |
| --- | --- | --- |
| 63 | [Layered Architecture](architectural-design-patterns/layered-architecture-pattern) | Folders are not a rule until a test enforces it |
| 64 | [MVC](architectural-design-patterns/mvc-pattern) | Two views, one calculation |
| 65 | [Hexagonal Architecture](architectural-design-patterns/hexagonal-architecture-pattern) | The core never learns it has a database |
| 66 | [Clean Architecture](architectural-design-patterns/clean-architecture-pattern) | The call goes out, the arrow points in |
| 67 | [Clean Architecture with Spring](architectural-design-patterns/clean-architecture-with-spring-pattern) | The same graph, wired by a container instead of by hand |

Layered Architecture is the category's reference: it is the architecture
most readers already have, and its failure mode — layers that exist as
folders and are violated by one convenient call — is the one everyone has
lived with. MVC is one step on from it: the same shared feature, with the
presentation side split into a model and views so that a screen and a
confirmation email cannot show a customer two different totals. Hexagonal
Architecture inverts the one honest cost Layered Architecture's own
documents admitted: the use case now declares its own ports, and an
adapter reaches up to implement or call them — proved by swapping the
storage adapter and the calling adapter at the same time, with zero
changes to the core either way. Clean Architecture generalises that
inversion into three named rings, with the dependency-inversion moment
shown in running code and proved under the category's largest forced
change — a new delivery mechanism and a new data source, added
simultaneously, with zero changes to entities or use cases. Clean
Architecture with Spring closes the category: the identical graph Clean
Architecture built by hand, assembled instead by a Spring container, so
the one contrast a container adds — hand-wiring fails at compile time,
container wiring fails at startup — can be shown directly, with the
missing-bean failure proved rather than narrated.

The numbering above skips 52 to 62 and 68 to 72. Those are reserved for two
more categories specified in the same planning pass — enterprise (52–62) and
foundational (68–72) — each with its own README, `spec.md` and
`implementation-plan.md` already committed under `gradle-java/`. Neither has a
single project built yet, and neither is wired into the shared generators;
they are out of scope for the architectural category's build and are recorded
here only so the gap in the numbers has an explanation. Concurrency (46–51),
the other category specified in that same pass, is covered in its own section
above.

---

## What each project contains

| Path | Content |
| --- | --- |
| `src/` | The pattern applied, plus the naive alternative it replaces |
| `docs/problem-statement.md` | The problem, and why the naive approach hurts |
| `docs/{pattern}-pattern-explained.md` | The pattern, the code, pitfalls, comparisons |
| `docs/class-diagram.md`, `docs/uml-diagram.md` | Structure and runtime call flow |
| `docs/animation.html` | Step-by-step walkthrough — open in a browser |
| `docs/session.md` | A 60-minute guided teaching session |
| `docs/spec.md` | That project's specification and quality bar |
| `video/` | A narrated 1080p video, plus the script and build pipeline |

Each project also carries the naive version of its problem — the code a
competent developer would write without the pattern. The comparison is the
point; a pattern shown without the thing it replaces is just structure.

## Running one

```bash
cd creational/simple-factory-pattern
./gradlew run
./gradlew test
```

Java 21 and no third-party runtime dependencies. JUnit 5 for tests only.

## The standards these are built to

| Document | Covers |
| --- | --- |
| [`docs/video-and-publishing-spec.md`](docs/video-and-publishing-spec.md) | The domain rule, narration, audio and video pipeline, poster and thumbnail, publishing |
| [`docs/implementation-plan.md`](docs/implementation-plan.md) | How the first fourteen were brought up to that standard |
| [`behavioural/docs/spec.md`](behavioural/docs/spec.md) | The behavioural category's scenarios and extra conformance items |
| [`micro-services-design-patterns/docs/spec.md`](micro-services-design-patterns/docs/spec.md) | The microservices category's scenarios, its one-JVM rule and its extra conformance items |
| [`platform-design-patterns/docs/implementation-plan.md`](platform-design-patterns/docs/implementation-plan.md) | The platform category's eight projects, its two-tier rule, and the infrastructure each one is allowed to use |
| [`architectural-design-patterns/docs/implementation-plan.md`](architectural-design-patterns/docs/implementation-plan.md) | The architectural category's five projects, the shared feature all five implement, and the ArchUnit dependency-rule test each one carries |
| [`concurrency-design-patterns/docs/implementation-plan.md`](concurrency-design-patterns/docs/implementation-plan.md) | The concurrency category's six projects, the determinism harness they share, and the rule that every naive failure reproduces on every run |

The generators in `docs/` — `make_specs.py`, `make_youtube_docs.py`,
`make_thumbnails.py` — produce the per-project specification, publishing
document and thumbnail from each project's own files, so those cannot drift
from the code they describe.

---

Built by Jayasekhar Konduru.
