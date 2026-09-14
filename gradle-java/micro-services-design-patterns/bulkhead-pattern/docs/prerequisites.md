# Prerequisites

What you need before starting this project, what you can pick up as you go, and what
you explicitly do not need to know.

This is the one project in the category with **real threads**, so the bar is slightly
higher than elsewhere — but only slightly, and the list below says exactly where.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, `final` fields, constructors, `List`.
- **What a thread pool is, roughly.** A fixed number of workers; a job asks for one,
  runs, and gives it back. If you can say that sentence you have enough.
- **`Callable` and `Future`, at reading level.** `bulkhead.submit("feed-1", job)` hands
  over some work and returns a `Future` you can ask for the answer later. You do not
  need to have written one.
- **Lambdas.** The jobs are lambdas. Reading them is enough.
- **Exceptions** — `throw`, `catch`, and the idea that failing fast can be deliberate.
- **Reading a JUnit test** — `assertEquals`, `assertThrows`, `assertTimeout`.

### Helpful, but explained as we go

- **`ThreadPoolExecutor`'s constructor.** Six arguments look intimidating and only
  three of them matter here: how many threads, how big the queue, and what to name the
  worker. The explained document quotes the line and walks it.
- **`CountDownLatch`.** One integer and two methods. `Gate` is a latch with friendlier
  names, and the primer below covers it.
- **Circuit Breaker** ([`../circuit-breaker-pattern`](../circuit-breaker-pattern)).
  The two patterns solve the same outage from opposite ends and are usually deployed
  together. Either order works; neither depends on the other.

### Explicitly NOT required

- **Writing correct concurrent code.** You are reading threads here, not designing a
  lock-free queue. There is no `synchronized` block in this project, no `volatile`, and
  no shared mutable state you have to reason about — the one thing several threads
  write to is a `CopyOnWriteArrayList`, which is thread-safe for you.
- **The Java Memory Model, happens-before, visibility.** Not needed, not used.
- **Virtual threads.** They change how expensive a thread is. They do not remove the
  need to decide what must never be starved, which is what this project is about.
- **Resilience4j, Hystrix, or any library.** They implement this in twenty lines of
  configuration. Understanding it first is the point.
- **HTTP, Spring, Docker, Kubernetes.** A JDK is the whole toolchain.

## A 60-Second "Bulkhead" Primer

A bulkhead is the real name for the walls that divide a ship's hull into watertight
compartments. Hole in an undivided hull: the water spreads and the ship goes down.
Hole in a divided one: one compartment floods and the ship keeps going.

In a service, the compartment is a thread pool. Instead of one pool that every kind of
work draws from, you give the work that must never be starved a pool of its own.

The whole mechanism is a second `ThreadPoolExecutor`. There is no algorithm in this
pattern — the decision to stop sharing *is* the pattern, and the hard part is choosing
where the wall goes.

## A 60-Second "Thread Starvation" Primer

A job that is *waiting* still holds its thread. It is using no CPU and doing nothing at
all, but the thread belongs to it until its call comes back.

So four import batches waiting on a slow partner API hold four threads. In a pool of
four, checkout then asks for a thread and there is none. Checkout never runs.

Two things follow, and both are easy to miss:

- **Starved and broken look identical from outside.** Nothing appears in the log,
  because the job never started. Absence is the symptom.
- **A bigger pool does not fix it.** Forty threads get taken too, just later, and the
  pile-up costs more memory before anyone notices.

## A 60-Second "Bounded Queue" Primer

Each bulkhead here has two threads and a queue that holds two. Four jobs fit. The
fifth is refused immediately, with a `BulkheadFullException`, in zero milliseconds.

That refusal feels hostile and is the opposite. The caller finds out instantly and
still has time to shed the batch, degrade, or write it down for tonight.

An unbounded queue would have taken that job, and every job after it, and told nobody
anything — turning a fast, visible failure into an out-of-memory crash later. **A queue
that never says no is not generous; it is a slow leak with good manners.**

## A 60-Second "Gate" Primer

The tests need a partner API that is slow, and they need it to stop being slow at a
moment of their choosing. `Gate` is a `CountDownLatch(1)` with two friendly methods:
`awaitOpen()` blocks the calling thread, `open()` releases everybody at once.

A job parked at a closed gate holds its thread in exactly the way a job waiting on a
slow network holds one. The difference is that the test decides when it ends.

This is why nothing in this project calls `Thread.sleep` to simulate slowness.
A sleep is only long enough until the machine running it is busy — which is how thread
tests become flaky. Where a test has to prove something is *not* happening, it uses a
bounded wait instead: `oneSharedPoolStarvesCheckout` expects a `TimeoutException` after
250ms, which is a statement about the shopper's patience, not a guess about the
scheduler.

## Why There Is No SimulatedClock Here

Every other project in this category has one, and this project deliberately does not.

Elsewhere, time is something the test controls: `RemoteCall` "takes sixty
milliseconds" by pushing a `long` forward. That works because those patterns are about
*which call waits for which*, which can be reasoned about exactly without concurrency.

Here the subject *is* threads genuinely waiting for one another. A fake clock cannot
demonstrate that a real thread is unavailable. So the threads are real, the timestamps
are real milliseconds, and the slowness is a latch the test holds shut.

## Software Prerequisites

- **JDK 21 or newer.** Nothing else.
- **Gradle:** not needed globally. The project ships a wrapper.

### Installing JDK 21

macOS, with Homebrew:

```bash
brew install openjdk@21
sudo ln -sfn $(brew --prefix)/opt/openjdk@21/libexec/openjdk.jdk \
    /Library/Java/JavaVirtualMachines/openjdk-21.jdk
```

Linux (Debian or Ubuntu):

```bash
sudo apt install openjdk-21-jdk
```

Windows: install the Microsoft Build of OpenJDK 21 or Temurin 21 from the installer,
and let it set `JAVA_HOME`.

### Verify Your Setup

```bash
java -version          # expect 21 or newer
cd micro-services-design-patterns/bulkhead-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 12 tests
./gradlew run          # expect four acts
```

If `./gradlew` will not execute on macOS or Linux, make it executable:

```bash
chmod +x gradlew
```

The first `./gradlew` command downloads Gradle itself and needs a network connection.
Everything after that works offline.

## Troubleshooting

**"Unsupported class file major version"** — Gradle is using an older JDK than the
toolchain asks for. Check `java -version`, and set `JAVA_HOME` to a 21 install.

**The timestamps in act one are not exactly 10ms** — they will not be. These are real
threads on a real machine, so a millisecond or two of drift is normal and nothing
depends on the exact figure. What the tests assert is *order* and *thread name*, never
a precise duration.

**Act one prints nothing for checkout, and that looks like a bug** — it is the
finding, not a bug. Checkout never got a thread, so it never started, so it wrote no
line. That absence is the whole of act one.

**Act three prints a failure and the build still succeeds** — correct. The refusal is
the expected outcome: four accepted, one refused. `afullBulkheadRefuses` asserts it.

**Act four shows idle threads and that looks wasteful** — it is wasteful, deliberately.
Two idle threads sit beside two jobs waiting for a thread, and they are not allowed to
help. That is the price of the walls, and `thesharedPoolIsFasterOnAGoodDay` asserts the
other side of the trade.

**The demo hangs** — it should not. Every wait in this project is bounded, and
`Gate.awaitOpen()` gives up after ten seconds rather than blocking forever, precisely so
that a mistake shows up as a failure rather than as a stuck terminal.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — a background job nobody was
   waiting for stops the shop selling, and why a bigger pool is not the answer
2. Run `./gradlew run` and read all four acts in order. In acts one and two, read the
   **thread names** — `shared-worker` against `feed-worker` and `checkout-worker` is
   the entire argument
3. [`bulkhead-pattern-explained.md`](bulkhead-pattern-explained.md) — the ship's hull,
   and the part about where the walls take up space
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) — the
   structure, including the arrow that is missing on purpose, then the four acts as
   sequences
5. [`animation.html`](animation.html) — the threads being taken one at a time, and
   checkout arriving to find none left
6. The tests, which are the specification. Read `theStarvedCheckoutWasNeverBroken`
   first, then `theFeedIsGenuinelyStuck` — which is the test that makes act two proof
   rather than coincidence
