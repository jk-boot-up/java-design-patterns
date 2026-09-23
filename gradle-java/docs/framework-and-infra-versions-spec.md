# Specification — Framework And Real-Infrastructure Versions For The Remaining Patterns

| | |
| --- | --- |
| Created | 2026-09-23 19:12:32 IST |
| Author | Jayasekhar Konduru |
| Repository state at creation | 152 projects across 11 categories, `main` at `8994c81` |
| Projects this specification adds | 28 |
| Repository state when finished | 180 projects across 11 categories |

This document specifies a batch of new projects. Each one pairs an existing pattern project,
written as a plain-Java simulation, with a second project that teaches the same pattern using
the real tool or the real framework that the industry actually reaches for.

It follows the precedent already set in this repository. Six patterns — Blue-Green and Canary,
Service Mesh, Feature Toggle, Consumer-Driven Contract, Event-Driven Architecture and
Serverless — were each given a real-infrastructure twin in September 2026, and a further
fifteen patterns carry a Spring, Resilience4j, Hibernate, HikariCP or Consul version. The
simulations were left exactly as they were in every case, and that rule holds here too.

Read [`../micro-services-design-patterns/docs/ai-build-spec.md`](../micro-services-design-patterns/docs/ai-build-spec.md)
before building any project in this batch. It is the toolchain document: the shared generators,
the exact shape of every generated file, the audio chain, and the traps that have already cost
real time. This document says *what* to build and *why*; that one says *how*.

---

## 1. Why a second project rather than a rewrite

The simulations are not drafts waiting to be replaced. They exist because every demo in this
repository prints numbers that its tests assert exactly, and a run that cannot vary is the only
way to do that. Real infrastructure brings timing, start-up delay and network behaviour with
it, so the same demo prints different numbers on different machines.

So each pattern ends up with two projects that answer two different questions. The simulation
answers "what is the idea, in the smallest code that can hold it". The real version answers
"what does this look like when the tool is doing the work, and what does the tool make you
deal with that the simulation quietly skipped". The second question is the interesting one, and
it is the reason this batch exists.

Every real version keeps a section in its README naming what the simulation got right and what
it left out. That is the teaching payload.

---

## 2. Naming and placement

A new project is named `<base-slug>-with-<tool>-pattern` and sits in the **same category
directory as the pattern it pairs with**. This matches every existing pair in the repository:
`service-mesh-pattern` and `service-mesh-with-envoy-pattern` are siblings, as are
`retry-pattern` and `retry-with-resilience4j-pattern`.

The tool name in the slug is the tool, not the vendor and not the protocol —
`cache-aside-with-redis`, not `cache-aside-with-in-memory-data-grid`.

---

## 3. Tier 1 — real infrastructure

Nineteen projects. Each one runs a real broker, database, proxy, cluster or cloud emulator,
almost always in a container brought up and torn down by the demo itself.

### 3.1 Messaging and integration

The category has five projects and not one of them has ever touched a real broker, which makes
it the weakest category in the repository for a learner who has to work with one.

| # | New project | Pairs with | Real tool | What the real version adds |
| --- | --- | --- | --- | --- |
| 1 | `message-channel-with-rabbitmq-pattern` | `message-channel-pattern` | RabbitMQ | A channel that outlives the process: durability, acknowledgement, and what happens to a message when nobody is listening yet |
| 2 | `dead-letter-channel-with-rabbitmq-pattern` | `dead-letter-channel-pattern` | RabbitMQ dead-letter exchange | The broker decides when a message is dead, not the application, and the reasons it records |
| 3 | `content-based-router-with-camel-pattern` | `content-based-router-pattern` | Apache Camel over RabbitMQ | Routing written as a declared route rather than an `if` chain, and what Camel does with a message no predicate claims |
| 4 | `splitter-aggregator-with-camel-pattern` | `splitter-aggregator-pattern` | Apache Camel | A real aggregator's completion condition and its timeout — the part the simulation gets for free |
| 5 | `event-bus-with-nats-pattern` | `event-bus-pattern` | NATS | An out-of-process bus with no durable log, so a subscriber that is not listening misses the event outright |

NATS is chosen for the event bus deliberately, rather than Kafka, because
`event-driven-architecture-with-kafka-pattern` already teaches the durable-log shape. NATS is
the opposite trade — fire-and-forget delivery — and the contrast between the two is worth more
to a learner than a second Kafka project.

### 3.2 Microservices

| # | New project | Pairs with | Real tool | What the real version adds |
| --- | --- | --- | --- | --- |
| 6 | `transactional-outbox-with-debezium-pattern` | `transactional-outbox-pattern` | Postgres, Debezium, Kafka | The canonical production shape: the outbox row is committed with the order, and change data capture — not the application — publishes it |
| 7 | `cache-aside-with-redis-pattern` | `cache-aside-pattern` | Redis | A cache another process can also see, real expiry, and the stampede the simulation cannot produce |
| 8 | `database-per-service-with-containers-pattern` | `database-per-service-pattern` | Postgres and MongoDB | Two services on genuinely different engines, and a join that is now impossible rather than merely discouraged |
| 9 | `leader-election-with-kubernetes-pattern` | `leader-election-pattern` | Kubernetes Lease API, through kind | Election by lease renewal against a real API server, and what a lost lease does to the loser |
| 10 | `competing-consumers-with-rabbitmq-pattern` | `competing-consumers-pattern` | RabbitMQ | Prefetch, and why an unacknowledged message returns to the queue when a consumer dies mid-work |
| 11 | `queue-based-load-leveling-with-sqs-pattern` | `queue-based-load-leveling-pattern` | Amazon SQS, through LocalStack | A real visibility timeout, and the queue depth that a burst actually builds |
| 12 | `publisher-subscriber-with-redis-pattern` | `publisher-subscriber-pattern` | Redis Pub/Sub | Fan-out across processes, and the message a late subscriber never gets |
| 13 | `claim-check-with-s3-pattern` | `claim-check-pattern` | Amazon S3, through LocalStack | A payload that genuinely will not fit in a message, stored and fetched by key |
| 14 | `rate-limiter-with-redis-pattern` | `rate-limiter-pattern` | Redis and Bucket4j | A limit shared by every instance, which is the only kind that holds when the service is scaled out |
| 15 | `idempotent-consumer-with-kafka-pattern` | `idempotent-consumer-pattern` | Kafka and Postgres | Real at-least-once redelivery, and a deduplication table that has to survive a restart |

### 3.3 Platform

| # | New project | Pairs with | Real tool | What the real version adds |
| --- | --- | --- | --- | --- |
| 16 | `distributed-tracing-with-jaeger-pattern` | `distributed-tracing-pattern` | OpenTelemetry and Jaeger | Context propagated across a real HTTP hop, and a trace assembled by a collector rather than by the demo |
| 17 | `externalised-configuration-with-spring-cloud-config-pattern` | `externalised-configuration-pattern` | Spring Cloud Config Server | Configuration served over HTTP from outside the application, and a refresh that takes effect without a restart |
| 18 | `event-sourcing-with-eventstoredb-pattern` | `event-sourcing-pattern` | EventStoreDB | Append-only streams with real optimistic concurrency on the expected version |
| 19 | `strangler-fig-with-nginx-pattern` | `strangler-fig-pattern` | NGINX | A real reverse proxy moving one route at a time from the old service to the new, with the old one still serving the rest |

---

## 4. Tier 2 — framework versions

Nine projects. No container in most of them; the point is that a framework in wide use
*embodies* the pattern, and seeing the pattern's own vocabulary in that framework's API is what
makes it stick.

| # | New project | Pairs with | Framework | Why this pairing |
| --- | --- | --- | --- | --- |
| 20 | `front-controller-with-spring-mvc-pattern` | `front-controller-pattern` | Spring MVC | `DispatcherServlet` is this pattern, unmodified, in the framework most Java web work uses |
| 21 | `service-layer-with-spring-pattern` | `service-layer-pattern` | Spring | `@Service` and `@Transactional` are the boundary the pattern describes, declared rather than hand-written |
| 22 | `specification-with-spring-data-jpa-pattern` | `specification-pattern` | Spring Data JPA | The `Specification` API is the pattern by name, and it composes into SQL rather than filtering in memory |
| 23 | `domain-event-with-spring-pattern` | `domain-event-pattern` | Spring | `ApplicationEventPublisher` and `@TransactionalEventListener`, which fixes the ordering problem the simulation has to hand-roll |
| 24 | `optimistic-offline-lock-with-jpa-pattern` | `optimistic-offline-lock-pattern` | JPA `@Version`, Postgres | A real lost update, detected by the database and surfaced as `OptimisticLockException` |
| 25 | `active-record-with-spring-data-jpa-pattern` | `active-record-pattern` | Spring Data JPA, Postgres | A row that really is a live object, against a real table |
| 26 | `onion-architecture-with-spring-boot-pattern` | `onion-architecture-pattern` | Spring Boot | The remaining gap: Layered, Hexagonal and Clean all already have a Spring Boot version |
| 27 | `actor-with-pekko-pattern` | `actor-pattern` | Apache Pekko | The mainstream JVM actor runtime — mailboxes, supervision and a real message loop |
| 28 | `cqrs-with-axon-pattern` | `cqrs-pattern` | Axon Framework | Command and query sides wired by the framework built for exactly this split |

Apache Pekko is named rather than Akka because Pekko is the open-source continuation and Akka's
licence no longer suits a teaching repository.

---

## 5. What every project in this batch must do

Everything in the existing standing conventions applies unchanged. The items below are the
ones this batch makes harder, so they are written out.

### 5.1 The e-commerce domain

Every worked example is the same online store carried across all 180 projects. The real tool
changes how the example runs, never what it is about. A Kafka topic carries orders, not
`test-topic-1`. A Redis key holds a product's price, not `foo`.

Analogies used to *explain* a pattern may come from any domain and often should. The code may
not.

### 5.2 Every explanation works with the listener's eyes closed

A large share of the audience listens rather than watches. No sentence may say "as you can see
here", and none may depend on a diagram, a class name on a slide or a line of code being
visible. The words alone name the actors, say what each decides, and give the order things
happen in. The audience is beginners: short sentences, plain language, one idea at a time.

This is harder in this batch than in any previous one, because a real tool brings vocabulary
with it. Every term a tool introduces — exchange, lease, visibility timeout, offset, prefetch —
is said in plain words the first time it appears, before the tool's name for it is used.

### 5.3 Determinism, with real infrastructure in the way

The repository's rule is that every demo reproduces its failure on every run and that no test
contains `Thread.sleep`. The six existing real-infrastructure projects worked out how to keep
that rule, and this batch follows them:

- **Counts that cannot vary stay exact.** A Kafka group's lag after three events is three, on
  every machine, and the test asserts three.
- **Counts that depend on the tool's own scheduling are asserted as a range** and printed as a
  description rather than as a number. The spread of a canary is the existing example; the
  spread of RabbitMQ's prefetch across two consumers is the new one.
- **Every wait is a bounded poll on a real condition.** Never a fixed sleep. Poll until the
  consumer group reports caught up, until the lease holder changes, until the trace appears in
  the collector — with a timeout that fails the test rather than hanging it.
- **Numbers in documents come from a real run.** Every figure quoted in a README, a slide or a
  narration line is the actual output of `./gradlew run` for that project. Nothing is rounded
  and nothing is invented.

### 5.4 Versions

Pin the newest generally available version of each tool at the time the project is built, not
an older major line. Record the exact version in the project's README and in its
`prerequisites.md`. Where a version has to be held back, say so and say why — the way the
Serverless project pins LocalStack 4.14.0 because later images refuse to start without an
account.

### 5.5 What a learner needs installed

Every Tier 1 project states its prerequisite plainly in `docs/prerequisites.md` and in the
README: a container runtime, and for the Kubernetes project, kind. A project that cannot run
without a daemon says so in its first paragraph rather than failing confusingly at run time.

### 5.6 The git surface

Source and documentation are committed. Rendered output never is — no mp4, m4a, srt, wav or
log, nothing under `video/build/`, nothing under `docs/audio/`. `animation.html`,
`video/poster.png`, `docs/thumbnail.png` and the rendered diagrams under `docs/images/` are
committed, because nothing rebuilds those on GitHub.

Commit messages carry a subject and a body and stop there. No `Co-Authored-By` trailer and no
mention of any assistant, in a commit message or in a pull request description. This repository
is published under its author's name and the history shows him as sole author.

---

## 6. Definition of done, per project

A project is finished when all of the following hold. This is the checklist from
`ai-build-spec.md` §10 with the three items this batch adds marked.

- [ ] Twenty-two committed files plus source, in the shape every other project has.
- [ ] Registered by hand in `docs/make_specs.py`, `docs/make_thumbnails.py` and
      `docs/make_youtube_docs.py`. A project missing from those tables is silently skipped.
- [ ] `./gradlew test` passes; no `Thread.sleep` anywhere under `src/test`.
- [ ] **The container or cluster is started and stopped by the demo itself**, and a second run
      immediately after the first produces the same result.
- [ ] **A run with no container runtime available fails with a sentence a beginner can act on**,
      not a stack trace.
- [ ] `./gradlew run` prints a timeline showing both the failure and the pattern's answer.
- [ ] Every number in every document, slide and narration line matches that output.
- [ ] **The README names what the simulation twin got right and what it left out.**
- [ ] `scenes.py` uses `title=` keyword form; 14 to 16 scenes; no slide overflows the
      12-line, 62-character or 52-character limits.
- [ ] `make_slides.py` docstring, footer, poster and diagram name *this* pattern; the poster
      strikes nothing out.
- [ ] `build_video.sh` and `make_subtitles.py` name *this* project's output file.
- [ ] Scene 1 narration follows the required order: what the video is, credit to Jayasekhar
      Konduru, the pattern in plain general words, then the same thing in e-commerce terms.
- [ ] The outro names no other pattern, because publishing order is not fixed.
- [ ] The build printed `audio timeline continuous`; loudness within 0.02 LU of −16 LUFS.
- [ ] `animation.html` passes all four validation checks in `ai-build-spec.md` §6.
- [ ] Both diagrams rendered; poster and thumbnail looked at, not merely generated.
- [ ] Spec regenerated **after** the video existed, and the line it printed checked.
- [ ] `git status` clean of mp4, m4a, srt, wav, log, `docs/audio/` and `video/build/`.

---

## 7. Build order

Projects are built in waves. Within a wave they are independent and can be built in parallel;
between waves the order matters only because a wave's first project settles the shape the rest
of that wave copies.

| Wave | Projects | Why grouped |
| --- | --- | --- |
| 1 | 1–5, messaging and integration | Smallest coherent category, and two brokers between them; settles the container-in-a-demo shape for everything after |
| 2 | 6–15, microservices | The largest wave; Redis and RabbitMQ shapes are already settled by wave 1 |
| 3 | 16–19, platform | Each uses a different tool, so nothing is shared and they are fully independent |
| 4 | 20–28, framework versions | No containers in most; a different and lighter shape |

Two constraints on parallel work:

**The three registration tables are shared files.** `make_specs.py`, `make_thumbnails.py` and
`make_youtube_docs.py` are edited by every project in a wave. Registration is done once,
centrally, after a wave's projects exist — not by each build in parallel, which only produces
conflicts.

**A video render takes eight to ten minutes and is run in the background.** Wait on the output
file rather than blocking, and delete `video/.build.log` afterwards; it is not covered by
`.gitignore`.

---

## 8. Out of scope

The remaining unpaired patterns get no framework or infrastructure version, and this is a
decision rather than an omission. They are the classic structural, creational, behavioural and
concurrency patterns — Builder, Decorator, Composite, Visitor, Memento, Read-Write Lock and
their neighbours — together with the patterns whose real-world form another project in this
batch already covers, such as Saga, which
`event-driven-architecture-with-kafka-pattern` already shows running on a real broker.

For those patterns there is no tool or framework that embodies them better than plain Java
already does, and pairing them for the sake of symmetry would add a project without adding a
lesson. If a pairing for one of them is proposed later, it is a change to this document first,
not a build.
