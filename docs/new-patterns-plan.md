# Plan — Ten New Pattern Projects and a Root Index

Spec: [`new-patterns-spec.md`](new-patterns-spec.md). Work is done one project
at a time. Progress is tracked in the checklist below and updated as each step
finishes.

## Phase 0 — Tooling (once, before the first project)

1. **`tools/patternkit/`**: a small Python tool, run through the videokit venv.
   - `scaffold <category> <slug>`: creates the project directory, Gradle
     build and wrapper (copied from an existing project), package folders,
     `video/videokit.toml` with the `amy-slow` voice, and a starter
     `pattern.toml`.
   - `docs <slug>`: writes `README.md` and every `docs/*.md` from
     `pattern.toml`.
   - `diagrams <slug>`: draws the PNG diagrams from `[[diagram]]` entries
     (flow, class and sequence shapes; dark theme matching the slides).
   - `animation <slug>`: writes `docs/animation.html` from `[[step]]`
     entries, in the same style as the existing pages.
   - `scenes <slug>`: writes `video/scenes.py` from `[[scene]]` entries.
   - `build <slug>`: all of the above, then `./gradlew test`, the shared docs
     generators, `videokit all` and `videokit animation`, and the index.
2. **Registration without hand-editing:** the shared generators
   (`make_specs.py`, `make_youtube_docs.py`, `make_thumbnails.py`) also read
   `pattern.toml`, so a new project needs no edits to their tables.
3. **`gradle-java/docs/make_index.py`**: writes the root `index.md` and
   `index.html` by scanning the projects.
4. Try the whole chain on project 1 before building the others.

## Phase 1 — The ten projects, one at a time

For each project, in order:

1. `scaffold`.
2. Write the Java code: the naive version, the pattern and the demo, in 4–6
   acts with exact numbers. Write the tests.
3. `./gradlew test run`, and fix until green and the output reads well.
4. Write `pattern.toml`: the prose, diagrams, animation steps and scenes,
   using the numbers the demo actually printed.
5. `build`. Check the generated README, one diagram and the animation page.
6. Render the video and animation clips in the background; move on to the
   next project while they render.
7. Tick the checklist.

## Phase 2 — Finish

1. Regenerate `index.md` / `index.html` and the category READMEs.
2. Confirm every acceptance point in the spec for all ten.
3. Commit and push the source only when the author asks.

## Checklist

| # | Project | Code + tests | Docs | Diagrams | Animation | Video | Index |
| --- | --- | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | Tooling + index | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 1 | Money | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | Test Double | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | Content Enricher | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4 | Materialized View | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 | Asynchronous Request–Reply | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6 | Health Endpoint Monitoring | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 7 | Write-Behind Cache | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 8 | Immutable Object | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 9 | Table-Driven State Machine | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 10 | Modular Monolith | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Risks and how they are handled

- **Generated prose reading as filler.** The tool only lays text out; every
  sentence is written for the project in `pattern.toml`, from the real demo
  output.
- **Diagram layout.** Positions are given in the description, not computed,
  so every diagram is predictable. A diagram that looks cramped is fixed in
  its description, not by hand-editing the PNG.
- **Render time.** Videos render in the background while the next project is
  written.
- **A new category** (`testing-design-patterns`) needs a category README; the
  index script picks up any category automatically.

## Phase 2: the rest of the catalogue, one by one

<!-- phase2:start -->

Updated automatically by `patternkit.sh build` (and `patternkit.sh plan`).

**60 of 60 done.**

| # | Pattern | Category | Status |
| ---: | --- | --- | --- |
| 1 | Blackboard | behavioural | ✅ done |
| 2 | Servant | behavioural | ✅ done |
| 3 | Acyclic Visitor | behavioural | ✅ done |
| 4 | Extension Object | foundational-design-patterns | ✅ done |
| 5 | Role Object | foundational-design-patterns | ✅ done |
| 6 | Private Class Data | foundational-design-patterns | ✅ done |
| 7 | Marker Interface | foundational-design-patterns | ✅ done |
| 8 | Memoization | foundational-design-patterns | ✅ done |
| 9 | Special Case | enterprise-design-patterns | ✅ done |
| 10 | Plugin | enterprise-design-patterns | ✅ done |
| 11 | Service Stub | enterprise-design-patterns | ✅ done |
| 12 | Query Object | enterprise-design-patterns | ✅ done |
| 13 | Table Data Gateway | enterprise-design-patterns | ✅ done |
| 14 | Single Table Inheritance | enterprise-design-patterns | ✅ done |
| 15 | Page Controller | enterprise-design-patterns | ✅ done |
| 16 | Remote Facade | enterprise-design-patterns | ✅ done |
| 17 | Entity | domain-driven-design-patterns | ✅ done |
| 18 | Domain Service | domain-driven-design-patterns | ✅ done |
| 19 | Context Map and Shared Kernel | domain-driven-design-patterns | ✅ done |
| 20 | Reactor | concurrency-design-patterns | ✅ done |
| 21 | Proactor | concurrency-design-patterns | ✅ done |
| 22 | Half-Sync/Half-Async | concurrency-design-patterns | ✅ done |
| 23 | Leader/Followers | concurrency-design-patterns | ✅ done |
| 24 | Copy-on-Write | concurrency-design-patterns | ✅ done |
| 25 | Lock-Free Compare-and-Swap | concurrency-design-patterns | ✅ done |
| 26 | Scheduler | concurrency-design-patterns | ✅ done |
| 27 | Micro-Frontends | architectural-design-patterns | ✅ done |
| 28 | Broker | architectural-design-patterns | ✅ done |
| 29 | Space-Based Architecture | architectural-design-patterns | ✅ done |
| 30 | Cell-Based Architecture | architectural-design-patterns | ✅ done |
| 31 | Message Translator / Normalizer | messaging-integration-patterns | ✅ done |
| 32 | Message Filter | messaging-integration-patterns | ✅ done |
| 33 | Recipient List | messaging-integration-patterns | ✅ done |
| 34 | Wire Tap | messaging-integration-patterns | ✅ done |
| 35 | Resequencer | messaging-integration-patterns | ✅ done |
| 36 | Request-Reply with Correlation Identifier | messaging-integration-patterns | ✅ done |
| 37 | Process Manager | messaging-integration-patterns | ✅ done |
| 38 | Routing Slip | messaging-integration-patterns | ✅ done |
| 39 | Polling Consumer | messaging-integration-patterns | ✅ done |
| 40 | Guaranteed Delivery | messaging-integration-patterns | ✅ done |
| 41 | Write-Through Cache | micro-services-design-patterns | ✅ done |
| 42 | Sharding | micro-services-design-patterns | ✅ done |
| 43 | Valet Key | micro-services-design-patterns | ✅ done |
| 44 | Priority Queue | micro-services-design-patterns | ✅ done |
| 45 | Backpressure | micro-services-design-patterns | ✅ done |
| 46 | Hedged Requests | micro-services-design-patterns | ✅ done |
| 47 | Gateway Offloading | micro-services-design-patterns | ✅ done |
| 48 | Event-Carried State Transfer | micro-services-design-patterns | ✅ done |
| 49 | Object Mother / Test Data Builder | testing-design-patterns | ✅ done |
| 50 | Page Object | testing-design-patterns | ✅ done |
| 51 | Contract Stub | testing-design-patterns | ✅ done |
| 52 | Authorization Policy (RBAC / ABAC) | security-design-patterns | ✅ done |
| 53 | Token-Based Authentication (JWT) | security-design-patterns | ✅ done |
| 54 | Secure Gateway | security-design-patterns | ✅ done |
| 55 | Secrets Manager | security-design-patterns | ✅ done |
| 56 | Input Validation Pipeline | security-design-patterns | ✅ done |
| 57 | Railway-Oriented Programming (Optional / Either) | functional-design-patterns | ✅ done |
| 58 | Higher-Order Functions | functional-design-patterns | ✅ done |
| 59 | Currying | functional-design-patterns | ✅ done |
| 60 | Lenses for Immutable Updates | functional-design-patterns | ✅ done |

<!-- phase2:end -->

## Phase 3: framework and real-infrastructure versions, one by one

Each is a new project beside its plain-Java twin; the twin is never edited or removed.

<!-- phase3:start -->

Updated automatically by `patternkit.sh build` (and `patternkit.sh plan`).

**31 of 31 done.**

| # | New project | Plain-Java twin (unchanged) | Framework or infrastructure | Status |
| ---: | --- | --- | --- | --- |
| 1 | message-translator-with-camel | message-translator | Apache Camel | ✅ done |
| 2 | message-filter-with-camel | message-filter | Apache Camel | ✅ done |
| 3 | recipient-list-with-camel | recipient-list | Apache Camel | ✅ done |
| 4 | wire-tap-with-camel | wire-tap | Apache Camel | ✅ done |
| 5 | resequencer-with-camel | resequencer | Apache Camel | ✅ done |
| 6 | routing-slip-with-camel | routing-slip | Apache Camel | ✅ done |
| 7 | process-manager-with-camel | process-manager | Apache Camel | ✅ done |
| 8 | guaranteed-delivery-with-rabbitmq | guaranteed-delivery | RabbitMQ | ✅ done |
| 9 | request-reply-with-rabbitmq | request-reply | RabbitMQ | ✅ done |
| 10 | polling-consumer-with-rabbitmq | polling-consumer | RabbitMQ | ✅ done |
| 11 | priority-queue-with-rabbitmq | priority-queue | RabbitMQ | ✅ done |
| 12 | event-carried-state-transfer-with-kafka | event-carried-state-transfer | Apache Kafka | ✅ done |
| 13 | write-through-cache-with-redis | write-through-cache | Redis | ✅ done |
| 14 | space-based-with-hazelcast | space-based | Hazelcast | ✅ done |
| 15 | sharding-with-postgresql | sharding | PostgreSQL | ✅ done |
| 16 | backpressure-with-reactor | backpressure | Project Reactor | ✅ done |
| 17 | reactor-with-netty | reactor | Netty | ✅ done |
| 18 | hedged-requests-with-grpc | hedged-requests | gRPC | ✅ done |
| 19 | valet-key-with-s3 | valet-key | Amazon S3 (LocalStack) | ✅ done |
| 20 | secrets-manager-with-openbao | secrets-manager | OpenBao (open-source Vault) | ✅ done |
| 21 | token-authentication-with-spring-security | token-authentication | Spring Security | ✅ done |
| 22 | authorization-policy-with-spring-security | authorization-policy | Spring Security | ✅ done |
| 23 | gateway-offloading-with-spring-cloud-gateway | gateway-offloading | Spring Cloud Gateway | ✅ done |
| 24 | secure-gateway-with-nginx | secure-gateway | NGINX | ✅ done |
| 25 | contract-stub-with-wiremock | contract-stub | WireMock (the stubs Spring Cloud Contract generates) | ✅ done |
| 26 | page-object-with-selenium | page-object | Selenium WebDriver | ✅ done |
| 27 | single-table-inheritance-with-jpa | single-table-inheritance | JPA (Hibernate) | ✅ done |
| 28 | table-data-gateway-with-jdbc-template | table-data-gateway | Spring JdbcTemplate | ✅ done |
| 29 | page-controller-with-spring-mvc | page-controller | Spring MVC | ✅ done |
| 30 | remote-facade-with-spring-mvc | remote-facade | Spring MVC | ✅ done |
| 31 | railway-oriented-with-vavr | railway-oriented | Vavr | ✅ done |

<!-- phase3:end -->
