# Enterprise Application Patterns

The seventh category. Seven patterns from Martin Fowler's *Patterns of
Enterprise Application Architecture*, in eleven projects, covering the space
between an application's objects and its database.

**Status: specified, not yet built.** The two documents below fix what the
projects are before any of them is written.

- [`docs/spec.md`](docs/spec.md) — the scenario each pattern is taught through,
  the naive version it must show failing, the cost it must admit to, and the
  framework feature it lives inside.
- [`docs/implementation-plan.md`](docs/implementation-plan.md) — the order the
  eleven get built in, the shared toy database they all use, the framework
  register, and the rules that keep the build from having to redo itself.

## The seven patterns, built by hand

| # | Pattern | Scenario |
| --- | --- | --- |
| 52 | Data Mapper | The object that does not know it is a row |
| 53 | Identity Map | The same customer, loaded twice, in two states |
| 54 | Unit of Work | Save half an order and nothing else |
| 55 | Lazy Load | Loading one order, and getting the whole catalogue |
| 56 | Repository | Query the collection, not the table |
| 57 | Service Layer | Where does "place an order" actually live? |
| 58 | DTO | The object that crosses the boundary |

The order is Fowler's own dependency order. Identity Map solves a problem Data
Mapper creates; Unit of Work needs the Identity Map to know what changed; Lazy
Load is the escape hatch all three make possible; Repository hides the four of
them; Service Layer sits above it; DTO is last because you must know what is
inside before deciding what leaves.

## The four framework projects

| # | Project | Pairs with | What only it can show |
| --- | --- | --- | --- |
| 59 | Identity Map with JPA | 53 | The same customer twice and `==` true — then two persistence contexts making it false |
| 60 | Unit of Work with Spring | 54 | `@Transactional`, the checked exception that commits anyway, and a flush nobody wrote |
| 61 | Lazy Load with Hibernate | 55 | A real `LazyInitializationException`, and what each of the three usual fixes costs |
| 62 | Repository with Spring Data | 56 | Deleting the implementation and the application still running — then the managed entity that leaks |

**Each version is its own project.** The hand-built one and the framework one are
not two halves of one directory: each has its own README, its own video and its
own lesson, because a framework demo buried inside another project is a lesson
nobody is taught. Projects 52 to 58 have no framework in any build file, so a
reader who wants the mechanism alone gets it; projects 59 to 62 each open by
naming their partner, reuse its domain unchanged, and explain Hibernate or Spring
from scratch in their own `docs/dependencies.md`.

Only four of the seven get a framework project, and the test is whether the
framework version has **a failure of its own** — a detached entity, a swallowed
rollback, a closed session, a leaked managed entity. For Data Mapper, Service
Layer and DTO the framework adds recognition rather than a new lesson, so it stays
one scene inside the hand-built project.

## Why this is the most directly useful category in the course

Every Java developer using Spring, JPA or Hibernate is already using all seven of
these, and most do not know it. The persistence context **is** an Identity Map.
`@Transactional` **is** a Unit of Work. `save()` on a Spring Data interface **is**
a Repository over a Data Mapper. `LazyInitializationException` is what a Lazy
Load does when its session has gone.

> **A framework you cannot explain is a framework you cannot debug.**

So each project builds the mechanism by hand first — plain Java, an in-memory
table, small enough to read in one sitting — and then shows the same thing
happening inside the real framework, so the reader recognises it. The hand-built
version is not a toy standing in for the real thing; it is the real thing with
the volume turned down.

## By hand first, then in the framework

**The hand-built project comes first, always.** Offline, no database, no network,
deterministic tests under two seconds, and its video is built entirely from it. A
reader who installs nothing gets the whole pattern.

**The framework project comes after it**, never before, and its job is
recognition plus one failure. It uses the real thing a reader meets at work —
Hibernate, Spring, Spring Data — over an in-memory H2, so it still needs nothing
installed beyond a JDK and a warm Gradle cache. That is what makes it reasonable
to ship these as projects rather than as optional extras.

## Where this sits

Projects 52 to 62, after the twenty-five object-oriented patterns, the twelve
microservices ones, the eight platform ones and the six concurrency ones. See
[`../README.md`](../README.md) for the full course.
