# Concurrency Patterns

The sixth category. Six patterns that exist because more than one thing is
happening at once.

**Status: specified, not yet built.** The two documents below fix what the
projects are before any of them is written.

- [`docs/spec.md`](docs/spec.md) — the scenario each pattern is taught through,
  the failure it must reproduce, the cost it must admit to, and what its harness
  pins that the real scheduler does not.
- [`docs/implementation-plan.md`](docs/implementation-plan.md) — the order the
  six get built in, the shared test harness they all depend on, and the rules
  that keep the build from having to redo itself.

## The six

| # | Pattern | Scenario |
| --- | --- | --- |
| 46 | Producer–Consumer | Orders arrive faster than they can be packed |
| 47 | Thread Pool | A thread per order, until the server stops |
| 48 | Future/Promise | A result you are promised but do not have yet |
| 49 | Read–Write Lock | A thousand readers and one price change |
| 50 | Monitor Object | The object that guards its own state |
| 51 | Active Object | A method call that returns before the work does |

The order is a dependency order. Active Object is last because it is the other
five assembled: a queue, a thread, a future and an object that owns its state.

## Determinism is the whole discipline

The usual objection to teaching concurrency is that its bugs are not
reproducible, so a demo either misses them or shows them only sometimes.

This repository has already answered that. The `bulkhead-pattern` project runs
real threads, real contention and real starvation, deterministically, with no
`Thread.sleep` in any test. Every project here is built on the same technique:
latches and barriers park threads at an exact point and release them together,
a planned-interleaving runner replays a race the same way every time, and a
step-controlled executor lets a test advance the work one task at a time.

> **A race that appears "sometimes" has not been taught.** Every naive failure
> in this category fails on every run.

That determinism is bought by pinning an interleaving the real scheduler chooses
freely, so every project says so plainly — in its explainer and out loud in its
video. A reader who leaves believing a passing test proves thread safety has
been taught something false, and this is the category where that belief forms.

## Where this sits

Projects 46 to 51, after the twenty-five object-oriented patterns, the twelve
microservices ones and the eight platform ones. See [`../README.md`](../README.md)
for the full course.
