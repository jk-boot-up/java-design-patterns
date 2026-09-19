# Prerequisites

## Knowledge Prerequisites

### Required

- **Producer–Consumer (§46) or Thread Pool (§47).** This project reuses
  their harness unchanged, and assumes the "forced, not guessed" habit
  those projects build.
- **`java.util.concurrent.Future` and `ExecutorService.submit`** — not
  required beforehand; act two's `ConcurrentProductPage` is short enough
  to read as the introduction.

### Explicitly NOT required

- **No prior experience with `CompletableFuture`.** Act three introduces
  it from nothing, using only `new CompletableFuture<>()`, `get()` and
  `complete()` — none of its callback methods.
- **No prior experience debugging an asynchronous stack trace.** Act four
  is built to be the first time.

## A 60-Second "Why Not Just Sleep" Primer

See §46's own primer — it applies unchanged here. This project's tests
never bet on timing; every scenario that needs forcing is forced with a
`Gate` or a `CountDownLatch`, and the two scenarios that need none —
a task parked on a gate that is never opened, and a stack trace that
structurally cannot contain another thread's frames — have exactly one
possible outcome regardless of timing at all.

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | The Gradle toolchain |
| Gradle | none to install | The wrapper (`./gradlew`) fetches what it needs |

### Verify Your Setup

```bash
java -version
cd concurrency-design-patterns/future-promise-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 124 tests, in under ten seconds
./gradlew -q run       # expect six acts of output
```

If a test ever fails intermittently, that is a defect in this project —
please open an issue rather than re-running it. Every failure in this
category is supposed to be forced, on every run, not occasional.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md)
2. Run `./gradlew -q run` and read all six acts
3. [`future-promise-pattern-explained.md`](future-promise-pattern-explained.md)
4. [`determinism.md`](determinism.md) — how every act above is forced, not hoped for
5. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
6. [`animation.html`](animation.html)
7. The source, starting with `pattern/FutureAndPromise.java`, then `pattern/ConcurrentProductPage.java`
8. `ConcurrentProductPageTest` and `CooperativeCancellationTest`
