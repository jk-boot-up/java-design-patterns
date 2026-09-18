# Dependencies

This project carries exactly one heavy dependency, and this document
answers the five questions every such dependency owes a reader before it
appears in a build file.

## What is Spring, in plain language?

Spring is a framework that builds your program's objects for you and
connects them together, instead of you writing the `new` calls yourself. At
its centre is something called an **application context** — a registry that,
when your program starts, reads a set of instructions (in this project, one
class with a method per object it needs to build), constructs every object
those instructions describe, and wires each one into whichever other object
asked for it by type.

The everyday word for this is **dependency injection**, and if you have
ever written a class with an `@Autowired` field, an `@Service`, or a method
in a class marked `@Configuration`, you have already met it.

## Why does this project use it?

Because it is the whole subject. [`clean-architecture-pattern`](../clean-architecture-pattern)
already built and taught the architecture, wiring its object graph by hand,
in one method, so that reaching into the outermost circle for a concrete
class and handing it to an interactor that only knows an interface could be
watched happening. This project takes that identical graph — the same
entities, the same use cases, the same adapters, copied unchanged — and has
a container build it instead, so the comparison a reader will actually meet
at work is available to see, side by side with the version they already
understand.

## What do you need to install?

Nothing extra. `./gradlew run` and `./gradlew test` download everything
through the Gradle wrapper, the same as every other project in this
repository.

| What | Version | Why this one |
| --- | --- | --- |
| Spring Boot | **4.1.1** | Newest generally available release at the time this project was built. A milestone release is not a release. |
| Spring Boot Gradle plugin | 4.1.1 | Matches the Boot version; produces the `bootJar` task and version-manages the starters. |
| `io.spring.dependency-management` | 1.1.7 | Applies Spring's own bill of materials, so no starter in this project names a version of its own. |
| `spring-boot-starter` | with 4.1.1 | Core only — an `ApplicationContext`, `@Configuration`, `@Bean`. No web starter, no database starter: this project is not a web application, it is a wiring comparison. |

## What does it cost?

**A reader now needs to know Spring to run this project at all.** Every
class in `entities`, `usecases` and `adapters` is unchanged from the
hand-wired project and needs nothing new — but `AppConfig`,
`BrokenAppConfig` and `Application` do, and understanding what they do
requires knowing what `@Configuration`, `@Bean` and an application context
are.

**Startup is slower.** A hand-wired `main()` runs in milliseconds. This
project's context has to be built, every bean method invoked, every
dependency resolved — real work, paid once per run, that the hand-wired
project never does.

**A wiring mistake surfaces at run time rather than at compile time.**
[`WiringContrastTest`](../src/test/java/com/jk/explore/cleanspring/WiringContrastTest.java)
proves this project's one owned contrast directly: the identical mistake —
one collaborator missing from the graph — fails `javac` in the hand-wired
project and fails `ApplicationContext` refresh here, seconds into a run
that otherwise looked completely normal.

## Does skipping this project lose anything?

**No.** [`clean-architecture-pattern`](../clean-architecture-pattern)
teaches Clean Architecture completely on its own — every entity, every use
case, every adapter, the dependency-inversion moment, the forced change,
the bill, all of it. This project's entire job is one comparison: the same
graph, wired by a container instead of by hand, and what that trade costs.
Nothing here is required to understand the architecture; it is only
required to see the architecture the way most readers will actually meet
it at work.
