# Prerequisites

This is the reference project for the concurrency category, and the first
place several techniques used throughout it are introduced.

## Knowledge Prerequisites

### Required

- **Threads, in outline.** What `Thread.start()` does, and that two threads
  running at once can interleave their work in more than one order.
- **`java.util.concurrent.BlockingQueue`** — not required beforehand;
  `pattern/BoundedOrderQueue.java` is a thin wrapper and is short enough to
  read as the introduction.

### Explicitly NOT required

- **No prior concurrency pattern.** This is the first project in the
  category, and everything else in it depends on what is built here.
- **No experience debugging a real race condition.** That is what this
  project — and this category — teaches.

## A 60-Second "Why Not Just Sleep" Primer

The obvious way to write a test for "thread A must finish before thread B
starts" is `Thread.sleep(500)` between them and hope 500ms is enough. It
usually is, on the machine that wrote it, which is exactly the problem: a
sleep-based test is a bet on how fast a particular machine happens to be
on a particular day, and it loses that bet on a slower or busier one,
unpredictably.

This project's tests never make that bet. See [`determinism.md`](determinism.md)
for the three small classes — `Gate`, `Rendezvous`, `StepExecutor` — that
replace every sleep with a mechanism that says "we are certain of this",
rather than "we are probably right about this".

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | The Gradle toolchain |
| Gradle | none to install | The wrapper (`./gradlew`) fetches what it needs |

### Verify Your Setup

```bash
java -version
cd concurrency-design-patterns/producer-consumer-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 88 tests, in under two seconds
./gradlew -q run       # expect five acts of output
```

If a test ever fails intermittently, that is a defect in this project —
please open an issue rather than re-running it. Every failure in this
category is supposed to be forced, on every run, not occasional.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md)
2. Run `./gradlew -q run` and read all five acts
3. [`producer-consumer-pattern-explained.md`](producer-consumer-pattern-explained.md)
4. [`determinism.md`](determinism.md) — how every act above is forced, not hoped for
5. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
6. [`animation.html`](animation.html)
7. The source, starting with `harness/Gate.java`, then `pattern/BoundedOrderQueue.java`
8. `HarnessSelfTest` and `PackerTest`
