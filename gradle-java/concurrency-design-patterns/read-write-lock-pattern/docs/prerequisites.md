# Prerequisites

## Knowledge Prerequisites

### Required

- **Producer–Consumer (§46).** This project reuses its harness unchanged,
  and assumes the "forced, not guessed" habit that project builds.
- **`java.util.concurrent.locks.ReentrantLock`** — not required
  beforehand; `naive/SingleLockCatalogue.java` is short enough to read as
  the introduction.

### Explicitly NOT required

- **No prior experience with `ReentrantReadWriteLock`.** Act three
  introduces it from nothing, and the project's own measurements — not a
  slide — carry the lesson about when it actually helps.
- **No prior experience with memory visibility or torn reads.** Act one
  is built to be the first time this is seen forced, on purpose, rather
  than stumbled into by accident in production.

## A 60-Second "Why Not Just Sleep" Primer

See §46's own primer — it applies unchanged here. This project's tests
never bet on timing; every scenario that needs forcing is forced with a
`Gate`, a `CountDownLatch`, or a structural guarantee the JDK documents
directly, and the two scenarios that need neither — the upgrade deadlock,
and `tryLock()`'s barging — have exactly one possible outcome regardless
of scheduling.

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | The Gradle toolchain |
| Gradle | none to install | The wrapper (`./gradlew`) fetches what it needs |

### Verify Your Setup

```bash
java -version
cd concurrency-design-patterns/read-write-lock-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 162 tests, in under ten seconds
./gradlew -q run       # expect six acts of output
```

If a test ever fails intermittently, that is a defect in this project —
please open an issue rather than re-running it. Every failure in this
category is supposed to be forced, on every run, not occasional.

**One number that will differ from machine to machine: the throughput
timings in acts two, three and six.** Their relative ordering — the
read-write lock coming in slowest, on this project's own measurements —
is the lesson; the exact millisecond counts are not.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md)
2. Run `./gradlew -q run` and read all six acts
3. [`read-write-lock-pattern-explained.md`](read-write-lock-pattern-explained.md)
4. [`determinism.md`](determinism.md) — how every act above is forced, not hoped for
5. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
6. [`animation.html`](animation.html)
7. The source, starting with `naive/SingleLockCatalogue.java`, then `pattern/ReadWriteCatalogue.java`
8. `ReadWriteCatalogueTest` and `WriterBargingTest`
