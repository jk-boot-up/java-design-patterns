# Concurrency Patterns — Category Specification

The sixth category. Six projects, numbered 46 to 51, on the patterns that exist
because more than one thing is happening at once.

This document fixes what each project is before any of it is written. It is the
contract; [`implementation-plan.md`](implementation-plan.md) is the schedule.

---

## 1. Scope

Six patterns, in learning order:

| # | Project | One line |
| --- | --- | --- |
| 46 | `producer-consumer-pattern` | Orders arrive faster than they can be packed |
| 47 | `thread-pool-pattern` | A thread per order, until the server stops |
| 48 | `future-promise-pattern` | A result you are promised but do not have yet |
| 49 | `read-write-lock-pattern` | A thousand readers and one price change |
| 50 | `monitor-object-pattern` | The object that guards its own state |
| 51 | `active-object-pattern` | A method call that returns before the work does |

The order is a dependency order. Producer–Consumer introduces the queue and the
handoff. Thread Pool is what consumes the queue in practice. Future/Promise is
how a caller gets an answer back from it. Read–Write Lock and Monitor Object are
the two ways shared state is protected. Active Object is the capstone: it is a
queue, a thread, a monitor and a future assembled into one idea, and it should be
taught only once all four are familiar.

---

## 2. Why this category, and what makes it teachable

This is the most natural category to follow the Gang of Four in a Java course.
Concurrency is where a beginner's mental model breaks first, and it breaks
quietly — the code looks right, the tests pass, and it is wrong on a busier
machine.

The objection to teaching it is that concurrency bugs are not reproducible, so a
demo either fails to show the bug or shows it only sometimes. That objection is
already answered inside this repository. The `bulkhead-pattern` project (§31)
runs real threads, real contention and real starvation, and does it
deterministically with no `Thread.sleep` anywhere in its tests. The harness that
made that possible is what this category is built on.

> **The rule for this category: every failure is reproduced on demand, and every
> test is deterministic. A race that appears "sometimes" has not been taught.**

Three harnesses carry it, and all three exist because the alternative is sleeps:

- **Latches and barriers instead of sleeps.** `CountDownLatch`, `CyclicBarrier`
  and `Phaser` let a test say "both threads are now exactly here" and then
  release them together. That is how a race is forced rather than awaited.
- **An interleaving harness.** A small helper that runs the same two operations
  against a shared object across a fixed set of pre-planned interleavings, so
  "the lost update" is a named scenario that fails every single run, not a
  flake that shows up one time in eighty.
- **A deterministic executor.** A single-threaded and a step-controlled
  `Executor` so a test can advance the work one task at a time and assert on
  the state in between.

### The honesty rule for this category

Determinism is bought by controlling the schedule, and a controlled schedule is
not the JVM's real one. So each project states plainly what its harness fixes:

> **Every project must say, in its explainer and aloud in the video, that the
> demo pins an interleaving the real scheduler chooses freely — and that the
> bug being shown is a bug on *some* schedules, which is what makes it
> dangerous.**

A reader who believes a passing test proves thread safety has been taught
something false, and this is the category where that belief is formed.

---

## 3. The store, continued

Same online shop. Orders arrive at the checkout, a packing team works through
them, the catalogue is read constantly and its prices change rarely, and stock
counts are the shared number everyone fights over.

That last one is worth stating because it recurs: **the stock count for a single
product is this category's shared mutable state.** Producer–Consumer moves
orders that will decrement it, Read–Write Lock protects it under a read-heavy
load, and Monitor Object is the version that guards it itself. Reusing one piece
of state across six projects means a reader compares the protections rather than
relearning the scenario.

---

## 4. The six scenarios

Each project shows a naive version failing — reproducibly — then the pattern,
then the bill.

### 4.46 Producer–Consumer — orders arrive faster than they are packed

**Scenario.** Checkout accepts orders. A packing step handles each one, and it
is slower than the arrivals.

**The naive version.** The checkout thread packs the order itself. The demo
shows the queue that forms in front of the customer: the shopper waits for a
warehouse operation they do not care about, and one slow pack blocks every
checkout behind it.

The second naive version is the interesting one, because it is the fix most
people reach for first: hand each order to a new thread and return immediately.
That works, and the demo shows it working, and then shows what it costs when
arrivals outpace packing — an unbounded pile of work, memory climbing, and
nothing anywhere applying a brake.

**The pattern.** A bounded queue between them. Producers offer orders, consumers
take them, and the two run at their own speeds. The bound is not an
implementation detail — it is the whole point, and the demo must make the queue
full and show what a producer does when there is nowhere to put the work.

**The bill.** You have chosen a policy for "full" and there is no pleasant
option: block the producer (checkout gets slow again), drop the order (never),
or grow without limit (the failure you just fixed). You have also introduced
ordering questions and a shutdown problem — the demo must show a clean shutdown
that drains the queue, and the one that loses the last four orders.

### 4.47 Thread Pool — a thread per order

**Scenario.** The shop gets busy. Each order is handled on its own thread.

**The naive version.** `new Thread(...).start()` per order. The demo runs it up
and prints what actually happens: thread creation cost per order, thousands of
threads each holding a stack, context switching that costs more than the work,
and eventually the failure everyone meets once — `OutOfMemoryError: unable to
create native thread`. Reproducibly, with the numbers printed.

**The pattern.** A fixed set of worker threads pulling from the queue built in
§46. Threads are created once and reused; the queue absorbs the burst.

**The bill, which is the part most treatments skip.** Sizing is a real decision
and the demo must show both directions: too few threads and the queue grows
while the CPU idles; too many and you are back to thrash. Worse, a pool where
tasks block on each other **deadlocks at any fixed size**, and the demo shows
that — a task submitted to the pool that waits for another task in the same
pool. And the default `Executors` factories carry traps worth naming: an
unbounded queue that hides the backlog until it is a heap dump.

**Java's answer, stated plainly.** Virtual threads (Java 21) change this
calculus and the project must say so honestly: for blocking I/O work the
thread-per-task model is viable again. The pool is still the pattern for
bounding a resource, and that distinction is the modern lesson.

### 4.48 Future/Promise — the answer you do not have yet

**Scenario.** The product page needs price, stock and reviews. Each takes
200ms.

**The naive version.** Call them in sequence: 600ms, and the demo prints the
timings. The reader can see the three calls do not depend on each other.

**The pattern.** Each call is submitted and returns a handle to a result that
does not exist yet. The page waits for all three at once and renders in
roughly 200ms. The demo then separates the two halves that beginners
conflate: the **Future** is the reader's side, the **Promise** is the writer's
side, and one piece of code completes what another piece is waiting on.

**The bill.** Exceptions move: a failure inside the task does not throw where
you called it, it surfaces when you ask for the result, wrapped. The demo shows
a stack trace that does not contain the line that caused it — which is the real
cost of asynchrony and the reason it is hard to debug. Then: a `get()` with no
timeout is a hang, cancellation is cooperative and may do nothing, and chaining
callbacks reaches a depth where it is unreadable.

### 4.49 Read–Write Lock — a thousand readers, one price change

**Scenario.** The catalogue is read on every page view. Prices change a few
times a day.

**The naive version.** One mutual-exclusion lock around the catalogue. Correct,
and the demo shows it being correct — then shows the cost: readers queue behind
each other for no reason, because two readers cannot possibly interfere. The
throughput number is printed under a read-heavy load.

Before that, a shorter naive version: no lock at all, and a reader that observes
half of a price update — old price, new currency. The interleaving harness makes
that happen every run.

**The pattern.** Many readers together, writers alone. The demo prints the
throughput difference under the same load.

**The bill.** More machinery than it looks: writer starvation under continuous
reads, an upgrade from read to write that deadlocks if attempted naively, and
the fact that the lock's own overhead can exceed the win when the guarded
section is short. The honest conclusion the project must reach: for a catalogue
this size, a copy-on-write snapshot or an immutable map swap beats the lock
outright, and the reader should leave knowing *when* the lock is the answer.

### 4.50 Monitor Object — the object that guards itself

**Scenario.** The stock count for one product, decremented by many checkout
threads.

**The naive version.** A plain `int`, decremented. The interleaving harness
forces the lost update every run: two threads read 10, both write 9, two items
sold and one item gone from inventory. Then the half-fix: the field is made
`volatile` and the demo shows it *still* wrong, because `volatile` gives
visibility and not atomicity — that misconception is common enough to be worth
a scene of its own.

Then the more instructive naive version: the caller locks the object from
outside. It works, until one caller forgets, and the demo shows that one
forgetful call site corrupting state that four correct ones were carefully
protecting.

**The pattern.** The object owns its lock. Its public methods are the only way
in, each runs under that lock, and a caller cannot forget. Waiting is done with
the object's own condition — a thread that needs stock waits, and is signalled
by the thread that adds some.

**The bill.** The lock is a bottleneck by design. Nested monitors deadlock, and
the demo shows two objects locking each other in opposite orders. `wait()` must
always sit in a loop because of spurious wakeups, and the demo shows the
`if`-instead-of-`while` version failing. And calling out to unknown code while
holding the lock is how a well-written monitor deadlocks anyway.

### 4.51 Active Object — a call that returns before the work does

**Scenario.** Inventory updates arrive from several places at once: checkout
reserves stock, returns add it back, an import corrects it.

**The naive version.** A monitor from §50. Correct, but every caller blocks
while holding up a shared lock, and the demo shows the checkout thread waiting
on a slow import.

**The pattern.** The object gets its own thread. Calls become messages on its
queue and return a future immediately. One thread owns the state, so **there is
no lock at all** — mutual exclusion comes from there being exactly one worker.
The demo shows callers returning at once and results arriving later.

This is the capstone, and the project must say what it is made of: the queue
from §46, a thread from §47, a future from §48, and the state-ownership idea
from §50. Nothing in it is new; the assembly is.

**The bill.** Everything is now asynchronous, including errors and ordering. The
queue can back up, and the demo shows the mailbox growing when the single worker
is slower than its callers. Debugging is harder because the stack trace shows
the worker, not the caller. And the single thread is a hard throughput ceiling —
the demo prints it.

**Where this leads.** The project names actors and event loops as where this
idea went, without teaching a framework.

---

## 5. Relationships to the existing projects

| Project | Depends on | Why |
| --- | --- | --- |
| Producer–Consumer | Bulkhead (§31) | Bulkhead isolates pools; this is what is inside one. |
| Thread Pool | Producer–Consumer (§46), Bulkhead (§31) | The pool consumes the queue; Bulkhead partitions pools. |
| Future/Promise | API Composition (§33) | The fan-out that project performs is what futures are for. |
| Read–Write Lock | Flyweight (§13) | The shared read-mostly catalogue is the same data. |
| Monitor Object | Singleton (§4) | The shared instance everyone reaches for is where this bites. |
| Active Object | §46, §47, §48, §50, Command (§17) | The queued message is a Command. |

---

## 6. Deliverables per project

Identical to the microservices category — the same committed file set, the same
generators, documented in [`../../micro-services-design-patterns/docs/ai-build-spec.md`](../../micro-services-design-patterns/docs/ai-build-spec.md).

Three additions specific to this category:

- A **`docs/determinism.md`**, or a named section of the explainer, saying how
  this project's failure is forced: which latch, which barrier, which
  interleaving. It is the category's distinguishing technique and a reader will
  want to reuse it.
- The explainer carries a **"What the scheduler really does"** section: what the
  harness pins, and what the JVM is free to do instead.
- The demo prints **timings and counts from a real run** — throughput, queue
  depth, thread count. Concurrency claims made without numbers are the thing
  this category exists to correct.

---

## 7. Video, poster and publishing

Unchanged: 14 to 16 scenes, `Samantha` at 145 wpm, −16 LUFS, a poster that does
not strike out its message, an outro naming no successor, and the required
four-step opening. Target length eleven to thirteen minutes.

One extra constraint, and it is not optional. **These explanations must work
with the listener's eyes closed**, which is harder here than anywhere else in
the course: an interleaving is naturally drawn, not spoken. So narration names
the threads (`the checkout thread`, `the packing thread`), says what each one
does in order, and says the timing out loud — *"both threads read ten; both
write nine; one item has vanished."* If a sentence needs a diagram, it is
rewritten.

---

## 8. Deliberately not included

| Pattern | Why not |
| --- | --- |
| Fork/Join and work stealing | A refinement of Thread Pool, covered as a section of §47. A project of its own would be about the algorithm rather than the pattern. |
| Reactor / Proactor | Event-loop I/O architectures. They need real non-blocking I/O to be honest, which puts them in the platform category's territory, not here. |
| Double-Checked Locking | A famous bug more than a pattern, and its correct form is an idiom rather than a design. Covered in a scene of §50. |
| Thread-Local Storage | One class and no design decision. It appears in §4.39's context-propagation discussion, where it matters. |
| Reactive Streams | A framework and a specification, not a pattern. Backpressure is taught in §46 where it belongs. |
| Software Transactional Memory | Not idiomatic in Java, and teaching it would mean teaching a library. |

A seventh project requires editing this section first.

---

## 9. Conformance

Every item from the microservices category's §9 applies, plus six:

- [ ] **The naive version's failure reproduces on every single run.** Not most
      runs. A test that flakes is a defect in this category, not a quirk.
- [ ] **No `Thread.sleep` anywhere, in tests or in the demo**, except where a
      deliberate delay is the subject being measured — and then it is named as
      such.
- [ ] The whole test suite still finishes in under two seconds.
- [ ] The explainer has its **"What the scheduler really does"** section, and
      the video says it aloud.
- [ ] The demo prints **real measured numbers**, and every figure quoted
      anywhere comes from that output.
- [ ] The narration names the threads and their order, and is followable with
      the video muted to a black screen.
