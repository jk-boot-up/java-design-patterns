# Architectural Patterns

The eighth category. Four patterns, in five projects, that decide the shape of a
whole application rather than the shape of a few classes.

**Status: specified, not yet built.** The two documents below fix what the
projects are before any of them is written.

- [`docs/spec.md`](docs/spec.md) — the feature all four implement, the forced
  change each is judged by, the architecture test each must ship, and the scale
  at which each becomes over-engineering.
- [`docs/implementation-plan.md`](docs/implementation-plan.md) — the order the
  five get built in, the shared feature written before any of them, and the
  rules that keep the build from having to redo itself.

## The five projects

| # | Pattern | Scenario |
| --- | --- | --- |
| 63 | Layered | Four layers, and the one call that ruins them |
| 64 | MVC | The view that knew too much |
| 65 | Hexagonal / Ports and Adapters | The application that does not know it has a database |
| 66 | Clean Architecture | Which way does the arrow point? |
| 67 | Clean Architecture with Spring | The same graph, wired by a container |

Each is one step from the one before, and every project says which step it takes.
A reader who finishes thinking these are four unrelated architectures has learned
four things instead of one.

**Clean Architecture is taught twice, and each version is its own project.**
Project 66 assembles the object graph by hand in a `main` method, because watching
twenty lines of constructor calls is where dependency inversion stops being a
diagram. Project 67 assembles the identical graph with Spring, because that is the
version a reader meets at work — and putting the two side by side gives the
contrast worth having: hand-wiring fails at compile time, container wiring fails
at startup. Spring appears in no build file except 67's, so a reader who wants the
architectures without the framework gets them, and 67 explains Spring from scratch
in its own `docs/dependencies.md`.

## The vagueness problem, and the three rules that answer it

Architecture is usually taught with boxes, arrows and adjectives —
*decoupled*, *maintainable*, *flexible* — none of which anyone can run or check.
Four videos of concentric circles would be worth nothing, and worse than nothing
for sounding authoritative.

So this category is built on three rules:

1. **One feature, built five times.** All five projects place the same order,
   with the same acceptance tests. Only the shape changes, so they can be
   diffed against each other.
2. **Every architecture is judged by a forced change**, performed on camera, with
   the cost counted in files touched and lines changed. Layered replaces its
   storage; MVC adds a second view; Hexagonal swaps its database *and* gets
   driven by a CLI; Clean does both at once.
3. **The architecture is a test that fails.** "The domain does not depend on the
   database" is an assertion, not a promise — each project ships an ArchUnit
   rule, breaks it deliberately, and shows the build go red naming the offending
   class.

> **If a claim cannot be expressed as a failing test or a counted diff, it does
> not go in the video.**

Every project also carries a **"when this is too much"** section naming the
application size at which its architecture is over-engineering. Without that,
four videos in a row argue for more structure, which is bad advice.

## Where this sits

Projects 63 to 67. See [`../README.md`](../README.md) for the full course.
