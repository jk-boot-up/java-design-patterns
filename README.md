# java-design-patterns

Learning material on design patterns in Java — the Gang of Four patterns, and
then the enterprise, domain-driven, concurrency, architectural, messaging,
microservices, platform, testing, security and functional patterns that go
beyond them, each with a plain-Java version and, where it helps, a framework
version. The substance of this repository
is [`gradle-java/`](gradle-java) — a worked course.

## Start here

**[`gradle-java/README.md`](gradle-java/README.md)** is the front door. The
patterns are grouped in fourteen categories, and every category has its own
README with the order to read it in. [`gradle-java/index.md`](gradle-java/index.md)
lists every project, and [`youtube-index.md`](youtube-index.md) links every video:

| Category | Projects | Covers |
| --- | ---: | --- |
| [Creational](gradle-java/creational) | 9 | Simple Factory → Singleton, and the framework versions |
| [Structural](gradle-java/structural) | 8 | Adapter → Proxy |
| [Behavioural](gradle-java/behavioural) | 20 | Strategy → Interpreter, plus Blackboard, Servant and more |
| [Foundational](gradle-java/foundational-design-patterns) | 21 | Null Object → Memoization, with Spring and HikariCP versions |
| [Enterprise](gradle-java/enterprise-design-patterns) | 30 | Data Mapper, Unit of Work, Gateway, the offline locks and more |
| [Domain-driven design](gradle-java/domain-driven-design-patterns) | 9 | Value Object → Context Map |
| [Concurrency](gradle-java/concurrency-design-patterns) | 24 | Producer–Consumer → Scheduler |
| [Architectural](gradle-java/architectural-design-patterns) | 22 | Layered → Cell-Based, with Spring Boot versions |
| [Messaging and integration](gradle-java/messaging-integration-patterns) | 31 | Message Channel → Guaranteed Delivery, with RabbitMQ, Camel and NATS versions |
| [Microservices](gradle-java/micro-services-design-patterns) | 58 | API Gateway → Hedged Requests, with Spring Cloud, Resilience4j and real-infrastructure versions |
| [Platform](gradle-java/platform-design-patterns) | 20 | Externalised Configuration → Consumer-Driven Contract |
| [Testing](gradle-java/testing-design-patterns) | 6 | Test Double → Contract Stub |
| [Security](gradle-java/security-design-patterns) | 9 | Authorization Policy → Input Validation Pipeline |
| [Functional](gradle-java/functional-design-patterns) | 5 | Railway-Oriented Programming → Lenses |

That is 272 projects. Each has runnable code with deterministic tests, a README
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
gradle-java/                 the course — 14 categories, 272 projects
  docs/                      the repository-wide specs and the shared
                             generators for specs, thumbnails, indexes and
                             YouTube documents
  <category>/<slug>-pattern  one self-contained Gradle project per pattern
tools/                       patternkit (scaffolds and builds a project),
                             videokit (audio and video), ytupload (YouTube)
docs/                        the pattern catalogue and the upload plans
index*.md, youtube-index.md  every project and every video, generated
```

## What is not in git

The narrated videos and their narration audio are build output, not sources.
Each project's `.mp4`, `.m4a`, `.srt` and `poster.png`, the per-step animation
audio under `docs/audio/`, and all Gradle build directories are ignored — they
are regenerated from committed scripts and would otherwise push the working tree
past a gigabyte. What *is* committed is everything needed to rebuild them:
`video/scenes.py` (slides and narration together), `make_slides.py`,
`build_video.sh`, `docs/make_animation_audio.sh`, and the diagrams under
`docs/images/`.

Videos and audio are built by the shared library in `tools/videokit`, with the
`amy-slow` Piper voice and `ffmpeg`; every project's `video/videokit.toml` says
what it needs. The rules are in [`AUDIO-VIDEO-SPEC.md`](AUDIO-VIDEO-SPEC.md).

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
