# java-design-patterns

Learning material on design patterns in Java — the Gang of Four patterns, then
the microservices patterns that pick up where they stop, then the platform
patterns that deal with what a running system stores and how it is configured,
traced and replaced, and then the architectural patterns that fix which layer
of a codebase is allowed to depend on which. The substance of this repository
is [`gradle-java/`](gradle-java) — a worked course. Everything else is earlier
scratch work, kept for reference.

## Start here

**[`gradle-java/README.md`](gradle-java/README.md)** is the front door. The
patterns are grouped in eleven categories, and every category has its own
README with the order to read it in:

| Category | Projects | Covers |
| --- | --- | --- |
| [Creational](gradle-java/creational) | 9 | Simple Factory → Singleton, and the framework versions |
| [Structural](gradle-java/structural) | 8 | Adapter → Proxy |
| [Behavioural](gradle-java/behavioural) | 16 | Strategy → Interpreter |
| [Microservices](gradle-java/micro-services-design-patterns) | 28 | API Gateway → Scatter-Gather, and Service Discovery with Consul |
| [Platform](gradle-java/platform-design-patterns) | 12 | Externalised Configuration → Consumer-Driven Contract |
| [Architectural](gradle-java/architectural-design-patterns) | 14 | Layered → Serverless, with Spring Boot versions |
| [Concurrency](gradle-java/concurrency-design-patterns) | 16 | Producer–Consumer → Two-Phase Termination |
| [Enterprise](gradle-java/enterprise-design-patterns) | 17 | Data Mapper, Unit of Work, Gateway and the offline locks |
| [Foundational](gradle-java/foundational-design-patterns) | 15 | Null Object → Delegation, with Spring and HikariCP versions |
| [Messaging and integration](gradle-java/messaging-integration-patterns) | 5 | Message Channel → Event Bus |
| [Domain-driven design](gradle-java/domain-driven-design-patterns) | 6 | Value Object → Bounded Context |

That is 146 projects. Each has runnable code with deterministic tests, a README
with diagrams, an animation, a session plan and a narrated video pipeline, and
each is taught through an online store unless the pattern is clearer in another
setting. Every project ends with a bill: what the pattern costs.

Every pattern is taught through the same worked domain — an online store — so a
learner moving from one project to the next carries the setting with them and
only has to absorb the new structure. Each project is self-contained: Gradle
Java 21 with its own wrapper, JUnit 5 tests, a naive alternative that shows what
the pattern is worth, seven written documents, class and sequence diagrams, a
stepped animation in the browser, and a narrated teaching video.

```bash
cd gradle-java/creational/simple-factory-pattern
./gradlew test
./gradlew run
```

No global install is needed. Each project ships its own Gradle wrapper; a JDK 21
on the `PATH` is the only prerequisite, and every project's
`docs/prerequisites.md` says how to get one.

## Repository layout

```
gradle-java/                 the course — 11 categories, 146 projects
  docs/                      the repository-wide specs and the shared
                             generators for specs, thumbnails and
                             YouTube documents
  creational/                9 projects
  structural/                8 projects
  behavioural/               16 projects
  micro-services-design-patterns/
                             28 projects
  platform-design-patterns/  12 projects
  architectural-design-patterns/
                             14 projects
  concurrency-design-patterns/
                             16 projects
  enterprise-design-patterns/
                             17 projects
  foundational-design-patterns/
                             15 projects
  messaging-integration-patterns/
                             5 projects
  domain-driven-design-patterns/
                             6 projects

chain-of-reponsibility-example/    earlier Maven + Spring Boot sketches,
factory-pattern-example/           predating the course and superseded by
spring-boot-milestone-3-0-example/ it. Left in place, not maintained.
```

The three Maven directories are historical. They are not part of the course, are
not covered by its standards, and the patterns they sketch are taught properly
under `gradle-java/`. Prefer the course; treat those as archive.

## What is not in git

The narrated videos and their narration audio are build output, not sources.
Each project's `.mp4`, `.m4a`, `.srt` and `poster.png`, the per-step animation
audio under `docs/audio/`, and all Gradle build directories are ignored — they
are regenerated from committed scripts and would otherwise push the working tree
past a gigabyte. What *is* committed is everything needed to rebuild them:
`video/scenes.py` (slides and narration together), `make_slides.py`,
`build_video.sh`, `docs/make_animation_audio.sh`, and the diagrams under
`docs/images/`.

Rebuilding a project's video takes roughly ten minutes and needs macOS, for the
built-in `say` command, plus `ffmpeg`:

```bash
cd gradle-java/behavioural/strategy-pattern/video
./build_video.sh
```

## Standards

Two documents define what "finished" means for a project, and both are worth
reading before adding one:

- [`gradle-java/docs/video-and-publishing-spec.md`](gradle-java/docs/video-and-publishing-spec.md)
  — the repository-wide standard every project inherits: the required file set,
  the slide and narration rules, the audio pipeline and its self-checks, and the
  publishing conventions.
- Each project's own `docs/spec.md`, generated by
  [`gradle-java/docs/make_specs.py`](gradle-java/docs/make_specs.py) from a
  single source of truth, so the test counts, runtimes and loudness figures
  quoted in it are measured rather than remembered.

Built by Jayasekhar Konduru.
