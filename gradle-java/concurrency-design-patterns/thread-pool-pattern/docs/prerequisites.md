# Prerequisites

## Knowledge Prerequisites

### Required

- **Producer–Consumer (§46).** This project reuses its harness, its bounded
  queue idea, and its `Order`/`Packing` domain unchanged. If the bounded
  queue there is unfamiliar, start there first.
- **`java.util.concurrent.ThreadPoolExecutor`** — not required beforehand;
  `pattern/BoundedPackingPool.java` builds one directly with named
  arguments and is short enough to read as the introduction.

### Explicitly NOT required

- **No prior experience with `Executors` factory methods.** This project's
  whole second act is about the trap one of them hides.
- **No prior experience with virtual threads.** Act six introduces them
  from nothing, contrasted directly against act one's measured numbers.

## A 60-Second "Why Not Just Sleep" Primer

See §46's own primer — it applies unchanged here. This project's tests
never bet on timing; every scenario is forced with a `Gate` or a
`CountDownLatch`, or in the pool-starvation scenario, needs no forcing at
all because it has exactly one possible outcome.

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | The Gradle toolchain, and virtual threads in act six |
| Gradle | none to install | The wrapper (`./gradlew`) fetches what it needs |

### Verify Your Setup

```bash
java -version
cd concurrency-design-patterns/thread-pool-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 125 tests, in under a few seconds
./gradlew -q run       # expect six acts of output
```

If a test ever fails intermittently, that is a defect in this project —
please open an issue rather than re-running it. Every failure in this
category is supposed to be forced, on every run, not occasional.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md)
2. Run `./gradlew -q run` and read all six acts
3. [`thread-pool-pattern-explained.md`](thread-pool-pattern-explained.md)
4. [`determinism.md`](determinism.md) — how every act above is forced, not hoped for
5. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
6. [`animation.html`](animation.html)
7. The source, starting with `naive/UnboundedPoolPacking.java`, then `pattern/BoundedPackingPool.java`
8. `BoundedPackingPoolTest` and `PoolStarvationTest`
