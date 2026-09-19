# Pinned versions and image tags

Every version this category uses, in one place. The
[implementation plan's framework register](implementation-plan.md#framework-register)
says *why* each of these is here and what it would cost to drop it; this file
says *which*, exactly.

There is one rule and it has no exceptions: **no ranges, no `latest`, no
unpinned tag.** A course that worked last year and does not work today is worse
than one that never took the dependency. `latest` is how a project rots without
anybody touching it.

Two files hold the pins. Java versions live in
[`../gradle/libs.versions.toml`](../gradle/libs.versions.toml), because Gradle
can read that. Container images live here, because nothing can.

## Tier 1 — every project, offline

| What | Version | Note |
| --- | --- | --- |
| JDK | 21 | The repository standard, via each project's own Gradle toolchain block |
| Gradle | 9.2.1 | Per-project wrapper, as everywhere else in the repository |
| JUnit 5 | 5.10.2 | The only Tier 1 dependency anywhere in the category |

That is the whole Tier 1 surface, and keeping it that short is the point. A
reader clones any project in this category, runs `./gradlew test` with no
network and no Docker, and it passes.

## Tier 2 — container images

| Image | Tag | Used by |
| --- | --- | --- |
| `nginx` | `1.31.5-alpine` | `sidecar` (§41), `sidecar-java-proxy` (§42), `sidecar-on-kubernetes` (§43), `strangler-fig` (§45) |
| `eclipse-temurin` | `21-jre-alpine` | every Tier 2 service image in the category |
| `jaegertracing/jaeger` | `2.20.0` | `distributed-tracing` (§39) — collector and trace UI in one image |
| `kindest/node` | `v1.37.0`, the default of `kind` 0.33.0, exercised | `sidecar-on-kubernetes` (§43) |

The alpine variants are chosen for size rather than for preference: a reader on
a slow connection pulling four images notices the difference, and none of these
projects needs anything the slim image leaves out.

## Tier 2 — frameworks and tools

| What | Version | Used by |
| --- | --- | --- |
| Spring Boot | 4.1.1 | `externalised-configuration` (§38), `distributed-tracing` (§39), `backends-for-frontends` (§40), `sidecar` (§41) |
| Spring Cloud | 2025.1.3 | `externalised-configuration` (§38) — Config Server and `@RefreshScope` |
| Spring dependency-management plugin | 1.1.7 | the Tier 2 builds that use Spring Boot |
| OpenTelemetry SDK | 1.62.0 | `distributed-tracing` (§39). Not pinned directly — it arrives with `spring-boot-starter-opentelemetry` and the version is whatever the Boot BOM says, which is the right way round for a library this closely tied to its auto-configuration |
| `kind` | 0.33.0, exercised: the demo refuses any other version | `sidecar-on-kubernetes` (§43) |
| Docker Compose | v2, any | Tier 2 generally. The compose file uses no feature newer than v2, so this one is deliberately not pinned tighter |

**Why Spring Boot 4.1 rather than 3.5.** An earlier version of this file pinned
3.5.16, on the argument that Spring Cloud 2025.0.x was built against it and that
the older line had a larger body of written material for a beginner to fall back
on. That argument loses to the purpose of the course: a reader is here to learn
what they would start a project on today, and pinning a superseded major version
to save them from reading newer documentation is not a favour. 4.1.1 is the
newest generally available release; 4.2.0-M1 exists, and a milestone is not a
release.

Spring Cloud 2025.1.x is the train built against Boot 4, so the pairing moves
together.

**What the move actually cost, measured rather than guessed:** nothing. §38's
Tier 2 went from 3.5.16 to 4.1.1 with no source change at all, and `demo.sh`
produced the same output on both — the same threshold, the same refresh, the
same rejection, the same last-good fallback. That is worth recording because a
major version bump is usually assumed to be a project of its own, and here it
was a two-line edit to this table.

## Components available but not yet adopted

Consul, RabbitMQ, Redis, Hazelcast and PostgreSQL are all permitted, and the
[implementation plan's named palette](implementation-plan.md#the-named-palette)
says where each would earn its place. None has a pin here, deliberately: a
version fixed long before anything runs against it is a claim rather than a
fact, and this file already carries enough of those. The pin is added in this
file, first, on the day the project that uses it is built.

## What is not yet exercised

Honesty about the state of the pins, so nobody reads this table as a report of
things that have been run.

| Row | State |
| --- | --- |
| JDK, Gradle, JUnit | **Exercised.** Every built project in this category runs on them |
| Spring Boot, Spring Cloud | **Exercised.** §38's Tier 2 builds and runs on them: Config Server serves the threshold, the client binds and validates it, and `POST /actuator/refresh` puts a new value in force without a restart |
| `jaegertracing/jaeger` 2.20.0 | **Exercised.** §39's Tier 2 exports to it over OTLP on 4318 and queries it back on 16686, and the waterfall in that project's `real/README.md` is drawn from what the image returned. Note that 2.21.0 has since been released; the pin stays at 2.20.0 because it is a category-wide choice that also binds the unbuilt sidecar projects, and moving it is a decision rather than a tidy-up |
| Temurin | Pinned from the current upstream release, not yet run. (nginx `1.31.5-alpine`, `kind` 0.33.0 and its node image `v1.37.0` have now been run, in §41 to §43.) Each becomes exercised when its project's Tier 2 is built, and a tag that turns out not to work gets corrected **here first** |

Pinning a version before running it is deliberate: the alternative is eight
projects each choosing their own, which is the drift this file exists to stop.
But a pin that has never been run is a claim, not a fact, and this table is
where the difference is recorded.
