# Foundational Patterns

The ninth category. Five patterns taught alongside the Gang of Four without
being in it, and used by every Java codebase daily.

**Status: all five built, and four framework versions.** Each project has code, deterministic tests, a README,
diagrams, an animation, a narrated video pipeline and a YouTube document. The two
documents below fixed what the projects are before any of them was written. One
thing differs from the plan: Dependency Injection writes a small container in plain
Java instead of running Spring, so its container scene shows the mechanism and does
not run a framework.

- [`docs/spec.md`](docs/spec.md) — the scenario each pattern is taught through,
  the naive version it must show failing, the bill it must present, and the
  verdict it must reach.
- [`docs/implementation-plan.md`](docs/implementation-plan.md) — the order the
  five get built in, the shared collaborators the last three all use, the
  framework register, and the rules that keep the build from having to redo
  itself.

## The five

| # | Pattern | Scenario |
| --- | --- | --- |
| 68 | Null Object | The discount that is not there |
| 69 | Object Pool | Expensive to make, cheap to borrow |
| 70 | Registry | The well-known place everything is kept |
| 71 | Service Locator | Ask a middleman for what you need |
| 72 | Dependency Injection | Stop asking; be given |

## Not loose ends

These are usually presented as leftovers. They are not — they share a subject:

> **How does an object get hold of another object, and what happens when there
> isn't one?**

Null Object answers the second question. Object Pool answers it when creating
one is expensive. The last three are one argument in three moves: Registry is a
well-known place to put things, Service Locator is a middleman you ask, and
Dependency Injection is what happens when you stop asking altogether. All three
solve the same problem with the same three collaborators — a discount policy, a
payment gateway and a notifier — so they can be compared directly rather than
described separately.

## Contested patterns, taught honestly

Three of the five exist largely to be argued about. Service Locator is widely
considered an anti-pattern. Registry is a global variable with better manners.
Object Pool is usually the wrong answer on a modern JVM, where allocation is
cheap.

Teaching them as straightforwardly good would be false; skipping them would
leave a reader unable to recognise them in the code they maintain. So each
project shows what the pattern is, why it was reasonable, what replaced it, and
**how to recognise it in code you did not write** — then ends with a plain
verdict rather than a hedge.

The arguments are made with runnable evidence, not assertion: pooling a small
object measured slower than allocating one, a test that fails because of the
order the tests ran in, and a compiler that says nothing while a required
dependency is missing.

Dependency Injection closes the argument, and it is the most useful project
here. The wiring is shown by hand first — about twenty lines in a `main`
method — so a reader sees that **a container is an optimisation of something they
could write themselves**, before any annotation appears.

## The four framework versions

Each of these is its own project, with its own README, video and lesson. It opens by naming its
hand-built partner, reuses the partner's collaborators, does not re-teach the pattern, and carries a
`docs/dependencies.md` saying what to install, what it costs, and that skipping it loses none of the
pattern. The hand-built projects keep no framework in their build files.

| Project | Pairs with | Uses | What only it can show |
| --- | --- | --- | --- |
| Dependency Injection with Spring | Dependency Injection | Spring Boot 4.1.1 | What `@Component` replaced, and Spring's real start-up failures |
| Registry with Spring | Registry | Spring Boot 4.1.1 | The context as a registry, and the test-cache leak that brings back order-dependent tests |
| Object Pool with HikariCP | Object Pool | HikariCP, H2 | What a mature pool solves, and the session state it cannot reset |
| Service Locator with Consul | Service Locator | A real Consul agent, real HTTP services, nginx in Docker | Real service discovery, a stale cache, and being given an address instead of asking |

## Where this sits

Projects 68 to 72. See [`../README.md`](../README.md) for the full course.

## More foundational patterns

- [Multiton](multiton-pattern)
- [Type Object](type-object-pattern)
- [Fluent Interface](fluent-interface-pattern)
- [Execute Around](execute-around-pattern)
- [Callback](callback-pattern)
- [Delegation](delegation-pattern)
