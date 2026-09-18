# Platform Patterns — Implementation Plan

How the eight projects in this category get built. [`spec.md`](spec.md) fixes what
they are; this fixes the order, the rules that keep the build from redoing
itself, and what "finished" means.

**Five of the eight are built**: `event-sourcing`, the category reference, plus
`externalised-configuration`, `distributed-tracing`, `backends-for-frontends`
and `sidecar`, each complete across both tiers. The rest of this document is the
plan for the remaining three.

---

## Current state

| | |
| --- | --- |
| Projects specified | 8 (six patterns; Sidecar is three projects) |
| Projects built | 5 (`event-sourcing`, the category reference; `externalised-configuration`, `distributed-tracing`, `backends-for-frontends` and `sidecar`, all four complete in both tiers) |
| Category registered with the shared generators | yes — Phase 0 complete |
| Existing projects in the repository | 37, across four categories |

---

## Order of work

### Phase 0 — Wire the category into the shared tooling

Before any project is written, because discovering it afterwards means going
back round every project already built. The microservices category learned this
the expensive way.

1. Add `platform-design-patterns` to the `CATEGORIES` list in
   `gradle-java/docs/make_narration.py`. It discovers projects by walking the
   category directories, so this is the only change it needs.
2. Add all eight slugs to the per-project tables in `make_specs.py`,
   `make_thumbnails.py` and `make_youtube_docs.py`. **These three carry their own
   slug tables and silently skip anything missing from them** — a project absent
   from the table produces no output and no error.
3. Add the category to `gradle-java/README.md` and the root `README.md`, and to
   the table of subsidiary specifications in `docs/video-and-publishing-spec.md`.
4. Fix the exact versions from the framework register below in one shared place
   — a `gradle/libs.versions.toml` catalogue for the category, plus a pinned
   image-tag list — so eight projects cannot drift onto three Spring Boot
   versions. Doing this after the first project is written means going back.
5. Verify: `python3 docs/make_narration.py` run from `gradle-java` should list
   the category with zero projects rather than not mentioning it.

**Exit:** the tooling knows the category exists and produces empty, not absent,
results for it, and every version the category will use is written down in one
file.

### Phase 1 — Build Event Sourcing end to end, as the category's reference

Event Sourcing goes first, and deliberately not in learning order.

Three reasons. It is the project people actually want, so it is the one worth
getting right while attention is fresh. It is the strongest of the six patterns under
simulation (`spec.md` §2), so it will not be fighting the harness while the
conventions are being set. And it is the most demanding, so if this category's
approach cannot carry Event Sourcing, that is worth discovering in week one
rather than week five.

Build it complete — source, tests, six documents, both diagrams, animation,
video, publishing document — and treat the result as the template the other seven
are copied from.

Two things this phase must settle for everyone who follows:

- **The "What this simulation does not show" section.** Its length, its tone,
  and where it sits relative to the costs. Get it right once.
- **How the demo shows a cost as output rather than prose.** For Event Sourcing
  that is a stream long enough to need a snapshot, and a deletion request that
  the append-only log cannot cleanly honour.

**Exit:** one project passing every item in `spec.md` §9, and a decision
recorded on both points above.

**Note what this phase cannot settle.** Event Sourcing is the one project that
should have no Tier 2 at all (`spec.md` §2a), so the reference project does not
establish the Tier 2 conventions — the `real/` layout, the README shape, how a
container demo is filmed for the single scene it gets. Those are settled by
`externalised-configuration-pattern`, the first project in Phase 2, which
therefore carries a second job beyond its own content. Treat its `real/`
directory as the template the other three copy.

**Settled by §38, now that its `real/` directory is built and running.** These
are conventions rather than suggestions; a later Tier 2 that departs from one
should say why in its own README.

| Convention | What it is |
| --- | --- |
| Tier 2 is a **separate Gradle build** | `real/settings.gradle` is its own root and the parent does not include it. This is what makes `./gradlew test` one directory up pass offline, with no Spring on the resolution path |
| **No second wrapper** | `real/demo.sh` invokes `../gradlew`. The wrapper is only a launcher and Gradle takes the project directory from the working directory, so the repository is spared another wrapper jar |
| Versions come from the **catalogue, never inline** | `real/settings.gradle` imports `../../gradle/libs.versions.toml`. No Tier 2 build script names a version directly |
| One **`demo.sh`**, unattended, start to finish | It builds, starts everything, walks the sequence, and stops everything on a trap. Every transcript in `real/README.md` is its captured output, never hand-edited |
| The README's job is the **delta**, not the pattern | Tier 1 teaches the pattern. Tier 2's README opens by saying so, then spends its length on what the framework does, what it does *not* do, and what was deliberately left out |
| `build/` and `.gradle/` are **git-ignored**, sources and the demo are not | Same rule as everywhere else in the repository |

**And one finding worth carrying forward.** §38's Tier 2 was where the
difference between "a framework implements this pattern" and "a framework
implements most of this pattern" turned into running code:
`@RefreshScope @Validated` rejects a bad value but then fails *every subsequent
request*, rather than falling back to the last good one. Tier 1 had made
last-good look obvious; the framework made it invisible. The general lesson for
the remaining Tier 2 directories is to **run the failure case, not just the
happy path** — the interesting half of a Tier 2 is always the part the framework
leaves to you, and that part is only visible when something goes wrong.

### Every project's README carries five extra things

Added after §41, and applied retrospectively to the five projects that were
already built. Every project in this category — and every project built from
here on — carries these, because a reader arriving at one of these directories
should be able to answer *what is this built on* and *what would I have to
start* without reading a build file.

| What | Where it lives | Generated by |
| --- | --- | --- |
| A **technologies and versions** section | `README.md`, between the simulation note and the Learning Material table. One table per tier, every row saying not just which version but *why that dependency is here* | by hand, from `gradle/libs.versions.toml` and `docs/pinned-versions.md` |
| An **architecture diagram** | `docs/architecture-diagram.md`, embedded in the README under "What runs where". Both tiers on one picture, with the technology written on each box | `docs/make_diagrams.py` |
| A **data flow diagram** | `docs/data-flow-diagram.md`, embedded in the README under "How the data moves". One request followed end to end, with what each hop adds to it | `docs/make_diagrams.py` |
| A **sequence diagram** | `docs/sequence-diagram.md`, embedded in the README under "Who calls whom, in order". The pattern working, start to finish, in call order | `docs/make_diagrams.py` |
| A **`README.html`** beside every `README.md` | the project root, and each `real/` directory | `docs/make_readme_html.py` |

Four notes on getting these right.

**The three new diagrams answer questions the class diagram cannot.** It is
structure, and structure says neither what you would have to install nor what
happens in what order. Where a project has a Tier 2, the architecture diagram is
the only document in it that shows both tiers at once.

**`sequence-diagram.md` is not a copy of `uml-diagram.md`.** The UML document is
the full set — four or five sequences including the rejected designs and every
failure mode — and it is where a reader goes to study the pattern. The sequence
diagram is the single end-to-end run that belongs in a README: the pattern
working, once, with prose that names every actor so it can be followed by
someone who is only listening. It ends by pointing at the UML document for the
rest.

**No diagram may be drawn from the plan.** Draw them from the source, the
compose file and the build scripts, the same rule the specs already follow: a
picture that shows a container the project does not start is worse than no
picture, because it will be believed.

**`README.html` is generated and must never be hand-edited.** The renderer is
`make_specs.py`'s Markdown converter, imported rather than copied, so a README
and a spec look like the same document and a construct that renders in one
renders in the other. If a README needs Markdown the converter does not know,
extend the converter.

### Phase 2 — Build the remaining seven, one at a time, in learning order

**One project at a time, finished completely before the next is started.** Half-
finished projects are how a category ends up with a stale spec and a video whose
narration quotes numbers the demo no longer prints.

| Order | Project | The thing to get right | Tier 2 | Risk |
| --- | --- | --- | --- | --- |
| 1 | `externalised-configuration-pattern` | The bad value reaching production in seconds | Config Server + `@RefreshScope`, threshold visible over HTTP | Low |
| 2 | `distributed-tracing-pattern` | The console waterfall, and the trace that breaks across a thread boundary | Trace id surviving a real HTTP hop, into a collector UI | Low |
| 3 | `backends-for-frontends-pattern` | Staying off API Gateway's territory | **Two REST backends serving `/api/products/{id}`** | Medium |
| 4 | `sidecar-pattern` | The container boundary, and killing the proxy | **Essential** — nginx beside the service on Docker Compose | **Medium** |
| 5 | `sidecar-java-proxy-pattern` | The proxy swap under a service that never restarts | A forty-line Java proxy in place of nginx | Low — reuses 41's service unchanged |
| 6 | `sidecar-on-kubernetes-pattern` | Explaining Kubernetes before using it | The same two containers as a Pod, on `kind` | **High** — the heaviest dependency in the course |
| 7 | `strangler-fig-pattern` | The migration that stalls half-finished | Gateway routing `/api/orders` between old and new | Medium |

Strangler Fig is last because it is the capstone and reads better once the
others exist to link to.

**Two projects are no longer at risk of being cut.** Sidecar was a candidate for
being dropped outright, and containers changed that — it is the largest single
effect the permission has. Backends for Frontends was the redundancy risk, and
real REST endpoints changed that: two backends returning two differently shaped
and visibly differently sized JSON documents for the same product is the
pattern's whole argument, and it cannot be restated as API Gateway because API
Gateway has one response. Both now carry ordinary build risk rather than an
existential question.

Build Tier 1 first and completely, every time, including the video. Tier 2 is
added afterwards, against a project that is already finished and already passes.
That ordering is what keeps a container problem from blocking a project that
does not actually need containers to teach its pattern.

**The three Sidecar projects are built in a strict order**, because each later
one is only worth building if the earlier one works, and each reuses the one
before it:

1. **§41 `sidecar-pattern`** — Tier 1 in-process, honest about being Decorator,
   then nginx beside the service on Docker Compose. Video built. This is the
   default path and a complete lesson on its own.
2. **§42 `sidecar-java-proxy-pattern`** — the forty-line Java proxy swapped in
   under §41's service, which is started once and never restarted. The cheapest
   of the three and the strongest single moment in the set, so it comes before
   Kubernetes. Video built, Tier 2 captured. It also ended up carrying the
   category's most useful piece of honesty: as a real process the proxy is 112
   lines rather than forty, and Tier 2 prints that rather than letting the
   in-JVM figure stand.
3. **§43 `sidecar-on-kubernetes-pattern`** — the Pod, with
   `docs/dependencies.md` written **before** the manifests, so the explanation is
   the plan rather than an afterthought.

**Projects 42 and 43 depend on 41 and say so.** Each copies §41's service and
nginx configuration rather than reinventing them, and each README opens by naming
§41 as the project to read first. What they must not do is re-teach Sidecar: the
pattern is §41's job, and 42 and 43 each spend their time on the one thing they
add. If a draft of either finds itself explaining what a sidecar is for more than
one scene, it has drifted.

If the schedule runs short, **§43 is the one to defer**, and §42 after it. The
pattern is complete and publishable after §41; the other two are additions, and
shipping §43 late is better than shipping it unexplained.

**Exit:** eight projects complete, each verified before the next begins.

### Phase 3 — Verify the category

1. The artefact sweep from
   [`../../micro-services-design-patterns/docs/ai-session.md`](../../micro-services-design-patterns/docs/ai-session.md)
   §2, pointed at this category.
2. `./gradlew test` in every project; no `Thread.sleep` under any `src/test`.
3. Every spec regenerated **after** its video exists, and the printed line
   checked — a spec reporting `0 scenes` or `not yet built` is stale, and this
   has already shipped once.
4. Every video printed `audio timeline continuous`, and every one listened to.
5. Every poster and thumbnail looked at, not merely generated.
6. `git status` shows no mp4, m4a, srt, wav, log, `docs/audio/` or
   `video/build/`.
7. All forty-three specs regenerate clean.
8. The thirteen extra conformance items in `spec.md` §9 checked per project,
   including the offline one — stop Docker, then run `./gradlew test` in all
   six.

---

## Framework register

Any open-source framework may be used where it is genuinely needed, and so may
**off-the-shelf infrastructure** — nginx, Envoy, a reverse proxy, a collector.
This section is where all of it is accounted for: nothing enters a build file or
a compose file without a row here first, so the category's dependency surface can
be read in one place rather than reconstructed from eight `build.gradle` files and
five compose files.

**Prefer the real component over a Java re-implementation.** Where the industry
solves something with a standard piece of infrastructure, use that piece. A
reverse proxy written in Java for the sake of staying in Java teaches the
re-implementation rather than the pattern — and in Sidecar's case it would
actively destroy the point, since a Java proxy beside a Java service says nothing
about language independence. The register's "why" column exists to record that
judgement per project.

### The rules that keep the register honest

1. **A framework is a plan edit before it is a build edit.** Add the row, with
   its version and its one-line reason, then add the dependency.
2. **Pin exact versions.** No version ranges, no `latest`, no unpinned image
   tags. A course that worked last year and does not today is worse than one
   that never used the library.
3. **Tier 1 stays dependency-free at runtime** — the offline guarantee is the
   thing being protected, and it is the one rule the permission does not
   loosen. JUnit 5 is the exception already in place across all thirty-seven
   projects. If a Tier 1 project genuinely needs a library, it needs a row here
   naming what it could not do without it.
4. **Permissive licences only** — Apache 2.0, MIT, BSD, EPL. This material is
   published, so a copyleft dependency is a decision with consequences beyond
   the project.
5. **The test is the reader, not the dependency count.** Any open-source
   framework is available; the question is only whether a beginner reading the
   project ends up clearer or more confused. A library that makes the pattern
   visible earns its place easily. One that saves ten lines while adding a
   concept the reader must learn first does not.
6. **An infrastructure component's configuration is teaching material.** The
   nginx or Envoy config is committed, kept short, and commented line by line,
   because for those projects the config file *is* the pattern — more so than any
   Java in the repository. A forty-line proxy config a reader cannot follow is a
   failed project even if it runs.

### What each project is expected to pull in

**The versions are fixed**, in [`../gradle/libs.versions.toml`](../gradle/libs.versions.toml)
for the Java ones and [`pinned-versions.md`](pinned-versions.md) for the image
tags, which is Phase 0's job rather than this table's. The exact numbers below
are repeated from there for reading convenience; that file is the authority, and
a version changed in one place and not the other is a bug in this document.

| Project | Tier | Framework | Why it, rather than plain Java |
| --- | --- | --- | --- |
| all eight | 1 | JUnit 5 (`5.10.2`) | Already the repository standard. |
| `externalised-configuration` | 2 | Spring Boot (`4.1.1`), Spring Cloud Config (`2025.1.3`) | `@RefreshScope` is the canonical answer, and re-implementing it by hand teaches the re-implementation rather than the pattern. |
| `distributed-tracing` | 2 | **Built.** Spring Boot (`4.1.1`) × 2 services, `spring-boot-starter-opentelemetry` (OpenTelemetry SDK `1.62.0`), `spring-boot-starter-restclient`, and `jaegertracing/jaeger:2.20.0` as both collector and UI | Context propagation across a real HTTP hop is the point; the wire format and the header names must be the real ones. Jaeger also earns its place a second way: the demo queries its API and redraws the waterfall from what the backend received, which *tests* Tier 1's claim that a waterfall is a property of the data instead of repeating it. Two starters rather than one because Boot 4 split observability and the HTTP client into separate modules — both traps are written up in `real/README.md`. |
| `backends-for-frontends` | 2 | **Built.** Spring Boot (`4.1.1`) × 3 services — the shop, and a backend in front of it per screen | Two independently deployable HTTP backends is the pattern's premise, and standing up two servers by hand adds noise without adding insight. Three rather than two because the shop has to be a separate address for the internal call count to mean anything: the tally is kept by the callee, so the phone backend's four calls against the desktop's five is the shop's own record rather than a claim the backend makes about itself. The `?fields=` projection is implemented and shown *succeeding* — 1754 bytes to 212, in the same territory as the phone backend's 196 — because a Tier 2 that only demonstrated the happy path would leave the payload-size misreading of this pattern intact. The failure case is the duplicated `SavingRules`: after `POST /pricing/review` the two backends disagree about a legally constrained claim while both report UP. No Docker; three JVMs on three ports. |
| `sidecar` (§41) | 2 | **Built.** nginx (`1.31.5-alpine`) × 2 + Spring Boot (`4.1.1`) × 3 containers, on Docker Compose | The proxy is a separate process in a separate image, and `network_mode: "service:checkout"` puts it inside the service's network namespace so that `http://localhost:8081` in the service's configuration is literally true -- the closest thing Compose has to a Pod, which is what §43 then replaces with the real thing. nginx because its config is short enough to read on a slide, and because it is not Java: the payments service is a Spring Boot application whose entire payment method is one call to localhost, and the retry policy that governs it is written in a language nobody on that team has to know. One template file is mounted into both proxies, so the demo's sixth act changes `proxy_next_upstream_tries` once and both services obey it with neither service process restarting -- the claim Tier 1 cannot make, printed with the containers' unchanged start timestamps beside it. The provider is HTTPS with TLS 1.3 only, which makes the transport a concern the service genuinely never learns rather than one we assert it does not. Three nginx facts are written up rather than hidden: retrying needs the upstream listed more than once, `max_fails=0` is required or nginx adds a circuit breaker nobody asked for, and a POST is not retried without `non_idempotent`. The one honest gap is backoff, which nginx has no directive for -- that is §42's reason to exist. |
| `sidecar-java-proxy` (§42) | 2 | **Built.** A Java proxy on the JDK's own `HttpServer` (no framework) + §41's nginx image, config and Compose service | Its own project so the swap can be demonstrated: the same service, the same config, a different neighbour. That swap is what turns "language independent" from a claim into a demonstration, and the readable Java version also shows what a proxy actually does. Keeps nginx too, because the comparison *is* the project. Both proxies bind port 8081 inside the service's network namespace, so only one is ever up and the swap is `stop` on one and `up -d` on the other, with the service container's start timestamp identical before and after. The provider had to be rewritten from §41's: counting attempts cannot separate these two proxies, because both make exactly three, so it is time-based instead -- `unwellForMillis` plus a ledger of the millisecond each attempt landed, which is the only measurement a proxy cannot influence. Measured result: three attempts in 35ms under nginx, three in 687ms under the Java proxy, same payment, same allowance. Two things the Tier 1 line count flatters are printed here rather than hidden -- the proxy is 112 lines as a real process against nginx's 27 (the retry loop is twenty-five of them; the rest is binding a port, reading a request and presenting a certificate), and a fresh JVM's first request is slow enough to change the figures, which is why `demo.sh` warms both proxies before any act. |
| `sidecar-on-kubernetes` (§43) | 2 | **Kubernetes** (`kind` `0.33.0`) + §41's service and nginx images | Where sidecars actually live. Shows the shared network namespace and shared lifecycle that Compose can only approximate, plus injection beside a service whose manifest does not mention it. Carries a full `docs/dependencies.md`. `kind` rather than a cloud cluster: one binary, one command, no account, no bill. |
| `strangler-fig` | 2 | **nginx** as the router, or Spring Cloud Gateway | Decide at build time on one criterion: whichever shows a route moving from old to new in fewer lines a reader can follow. nginx `location` blocks are likely to win, and they have the advantage of being the thing a real migration would use. |
| `event-sourcing` | — | **none** | Deliberately. The pattern is entirely in-process; a database would add operational noise and teach nothing about it. |

### The named palette

The permission to use real infrastructure has been restated with specific
components: **Consul, RabbitMQ, Redis, Hazelcast, PostgreSQL, Kubernetes and
nginx**, to be used wherever they are needed. Read that as illustrative rather
than exhaustive, and as reaching beyond this category — it applies anywhere in
the course a pattern is better shown with the real component than with a
simulation.

The rule that a project should not hand-roll in Java what the real world solves
with a standard piece of infrastructure is what these are for. The likely homes:

| Component | Where it would earn its place |
| --- | --- |
| **nginx** | §41–§43 and §45, already planned and pinned |
| **Kubernetes** | §43, already planned and pinned |
| **PostgreSQL** | §33 `database-per-service`, where two services owning two real schemas is the whole argument; and a Tier 2 event store for §44 if a draft ever needs projection lag to be visible |
| **RabbitMQ** | §36 `transactional-outbox` and §37 `idempotent-consumer` — a real broker is what makes at-least-once delivery something that happens to you rather than something you are told about |
| **Redis** | §37 `idempotent-consumer`, as the deduplication store, and caching generally |
| **Hazelcast** | The alternative to Redis where the point is an embedded cluster rather than a server, which makes it a candidate for the concurrency category (§46–§51) |
| **Any distributed cache** | Granted as a class, not as a product list — Infinispan, Apache Ignite, Memcached and Coherence are as available as Redis and Hazelcast. Pick per project on which one shows the *pattern* in fewest readable lines, and say in that project's README why it was picked over the obvious alternative |
| **Consul** | §27 `service-discovery`, where a real registry with health checks replaces the in-memory map |
| **Vert.x** | §42 `sidecar-java-proxy`, where the plan already calls for a readable proxy of roughly forty lines and Vert.x's `HttpServer` plus `HttpClient` is close to the shortest honest way to write one; and the concurrency category (§46–§51), where an event loop is the subject rather than an implementation detail |

**Vert.x is the first application framework named here alongside Spring**, and
that is the useful signal in it: the permission is not Spring-specific. Where a
pattern reads better on an event-loop toolkit than on a servlet stack, the
toolkit is the right choice. The countervailing consideration is the audience —
a beginner who knows neither will find Spring's annotations easier to look up
than Vert.x's callbacks, so the bar for choosing Vert.x is that it makes the
*pattern* shorter, not merely that it makes the runtime smaller.

Nothing above is adopted yet, and **nothing gets a pin until the project that
uses it is being built** — a version pinned years before first use is a claim
nobody has tested. When one is adopted: pin it in
[`pinned-versions.md`](pinned-versions.md) first, add its row to the register
table above, then touch a build file. Those categories are already complete, so
adopting one of these there is a revision to a finished project and should be
weighed as such rather than done in passing.

### Considered, and not currently planned

**Any open-source framework is available.** This table is not a list of
prohibitions — it records the current judgement on candidates that came up, so a
later session does not re-derive the same reasoning from scratch. If a draft
shows one of these earning its place, take it and update its row; the register
exists to keep the dependency surface readable, not to gatekeep.

| Candidate | Current judgement |
| --- | --- |
| Kafka, for Event Sourcing | It is a log, which invites the mistake that Event Sourcing is a messaging pattern. An in-memory list shows the append-only store exactly. Reconsider if a draft needs to show a real projection lag. |
| Axon, or another event-sourcing framework | The project's job is the mechanism, and a framework that hides the fold hides the lesson. Worth one scene as "this is what you would really use". |
| Lombok | Saves typing, costs a reader who then has to know what the annotations generated. Java records already cover most of it. |
| A mocking framework | Thirty-seven projects have managed with hand-written fakes, which a beginner can read. No objection if a Tier 2 test genuinely needs one. |
| A service mesh control plane | Istio or Linkerd on top of §43 would make it a mesh tutorial. The Pod is the honest edge of what one laptop shows; the project names what a mesh adds beyond it. |

**Kubernetes and a Java proxy were previously listed here as exclusions and are
now built, each as a project of its own** — §42 and §43 (`spec.md` §2a). Both earn
their place by comparison: the Java proxy makes language independence
demonstrable rather than merely claimed, and the Pod shows the two containers
sharing a network namespace and a lifecycle by definition rather than by
configuration. Both come with the dependency explanation §2a requires, and
because each is a separate project, a reader who wants neither clones neither.

**This is done.** The versions live in
[`../gradle/libs.versions.toml`](../gradle/libs.versions.toml) and
[`pinned-versions.md`](pinned-versions.md), so the eight projects cannot drift
onto three Spring Boot versions. That file also records which pins have actually
been run and which are so far only claims, because a version nobody has executed
is not yet a fact.

---

## Sequencing rules

**Finish one project before starting the next.** Stated as a rule because it has
been the standing instruction across this repository from the beginning, and
because the failure it prevents is expensive: a spec regenerated against a demo
that has since changed is wrong in a way nothing detects.

**Write the demo before the narration.** Every number in a document, a slide or
a spoken line comes from real `./gradlew run` output. Writing narration first
means writing numbers you then have to make true.

**Regenerate the spec last, after the video exists.** `make_specs.py` measures
the mp4. Run before the render, it silently degrades the spec instead of
failing.

**Any fix to the shared pipeline is rolled out to all projects**, not left where
it was found. This is a standing instruction and has already been applied twice
across the whole repository.

**Nothing is committed or pushed unless asked.** Build artefacts go to
`.gitignore`; source, documents, `animation.html`, posters, thumbnails and
rendered diagrams stay in. Commit messages carry no co-author trailer.

---

## Risks

| Risk | Mitigation |
| --- | --- |
| **Containers leak into Tier 1 and the offline guarantee is lost** | The largest risk the permission introduces, because it happens gradually and nothing fails loudly. `spec.md` §9 makes it a conformance item checked by stopping Docker and running `./gradlew test`. |
| **Tier 2 rots** — images move, ports clash, a Spring Boot major lands | Pin every image tag and framework version in the shared catalogue fixed at Phase 0. Tier 2 is never on the path of `./gradlew test`, so rot degrades an extra rather than breaking the course. |
| **Dependency creep** — a convenience library at a time, until the category has a stack | The framework register is the gate: a row, with a reason, before a build-file line. The bar is "the pattern cannot be shown without it", not "this saves ten lines". |
| **Eight projects drift onto different framework versions** | One catalogue for the category, fixed before the first project is built. |
| A viewer is left thinking Docker is required | Tier 2 gets at most one scene, near the end, and the video is built entirely from Tier 1. |
| Spring Boot obscures the pattern | Tier 1 has no framework at all, so the pattern is always visible in plain Java first. Tier 2 shows the canonical implementation second, once the idea is already understood. |
| Sidecar's Tier 2 does not run on a clean machine | It is the payoff of all three projects, so test each on a machine that has never built it, with images pulled fresh. |
| **Three Sidecar projects become three maintenance burdens** | The cost of building both versions, and it is real. Mitigated by the strict build order above, by §42 and §43 reusing §41's service and nginx config rather than forking them, by §43 being deferrable, and by none of it being on the path of `./gradlew test`. |
| **Three Sidecar projects repeat each other and bore the viewer** | Each of §42 and §43 gets one job and states it in its first sentence. Neither re-teaches what a sidecar is; both link to §41 for that. A draft that spends more than one scene re-explaining the pattern has drifted. |
| **A reader is scared off by Kubernetes** | The worst outcome available here. §43 being its own project is the main mitigation: §41 and §42 never mention it in a build file. The videos for §41 and §42 are complete lessons, and §43's `docs/dependencies.md` states plainly that skipping it loses none of the pattern. |
| `kind` or the Kubernetes API moves | Pin the `kind` version and the node image; the manifests used are the stable core ones. A break degrades an addition, not the project. |
| Backends for Frontends restates API Gateway | `spec.md` §4.40 makes it a rule, not an intention: fan-out and aggregation belong to §26 and are linked, not re-taught. The Tier 2 two-backend comparison is the part §26 structurally cannot contain. |
| **REST endpoints drift off the shop's domain** — `/api/test`, `/demo/foo` | A conformance item in `spec.md` §9. Endpoint paths are teaching material and get the same scrutiny as class names. |
| **A `curl` transcript in a README goes stale** when the response shape changes | The standing rule that every quoted number is real captured output applies to responses too. Re-capture after any change to a Tier 2 endpoint; never hand-edit a transcript. |
| Event Sourcing turns into a second CQRS video | The project's job includes ending that confusion. It must show one of each, briefly, so the distinction is concrete. |
| The simulation over-claims | The mandatory "What this simulation does not show" section, in the explainer and spoken in the video. The category's credibility rests on this. |
| Videos drift back to eighteen minutes | Eleven to thirteen minutes is a conformance item in `spec.md` §9, not a preference. |
| The category grows by accretion | `spec.md` §8 names what is out. A seventh *pattern* needs a spec change first, and so does any further split of one pattern into projects. |
| Eight full projects is a large amount of work | Roughly a week each including the render, though projects 42 and 43 are cheaper because they reuse project 41's service unchanged. The one-at-a-time rule means the category is useful at any point, not only when complete. |

---

## Definition of done

The category is complete when:

- [ ] Eight projects exist, each passing the repository-wide conformance checklist
      and the thirteen extra items in `spec.md` §9.
- [ ] **All three Sidecar projects run** — §41 Tier 1 and nginx, §42's Java
      proxy, §43's Pod — and §42 demonstrates the proxy swap under an unchanged
      service image.
- [ ] **Each of §42 and §43 is a project in its own right**: its own README,
      documents, poster, thumbnail and video, naming §41 in its first paragraph,
      and §41 links forward to both.
- [ ] **Neither §42 nor §43 appears in §41's build files**, so a reader who
      wants only §41 installs only Docker.
- [ ] **Every project carries the five documentation extras**: a technologies
      and versions section in its README, an architecture diagram, a data flow
      diagram, a sequence diagram, and a generated `README.html` beside every
      `README.md`.
- [ ] **Every heavy dependency has a `docs/dependencies.md`** answering the five
      questions in `spec.md` §2a, written for someone who has never used it.
- [ ] **Every project's Tier 1 passes with Docker stopped**, verified by
      stopping it rather than by reasoning about it.
- [ ] The seven projects expected to have a Tier 2 have one — everything except
      Event Sourcing — each starting from a
      single command on a machine that has never built it, and each with a
      README a reader can follow using only `curl`.
- [ ] Every project builds, tests pass in under two seconds, and its README
      quotes real run output including both the failure and the cost.
- [ ] No `Thread.sleep` appears anywhere under `*/src/test`.
- [ ] **Every dependency and every image in the category appears in the
      framework register** with a pinned version and a reason, and the register
      matches what the build files actually declare.
- [ ] Every video is rendered, printed `audio timeline continuous`, runs between
      eleven and thirteen minutes, and has been listened to.
- [ ] Every poster and thumbnail has been looked at.
- [ ] Every explainer has its "What this simulation does not show" section, and
      every video says it aloud.
- [ ] All forty-five projects' `spec.md` / `spec.html` regenerate clean.
- [ ] The root `README.md`, `gradle-java/README.md` and the repository-wide spec
      all describe forty-five projects across five categories.
