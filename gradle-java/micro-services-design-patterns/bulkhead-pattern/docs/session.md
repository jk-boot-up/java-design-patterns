# Session Guide — Bulkhead

A one-hour session. The mechanism takes about eight minutes and is genuinely
underwhelming — it is a second thread pool. Everything worth the hour is on either side
of it: the invisibility of the failure before, and the cost of the walls after.

Protect the last twenty minutes. Deciding what must never be starved, and admitting
out loud what you are leaving idle to guarantee it, is the part most treatments skip.

**Audience:** developers who know Java. No concurrency experience assumed beyond
knowing what a thread pool is.

**Format:** laptops open. Everything runs offline with a JDK.

## Learning Objectives

By the end, a participant can:

1. Explain why a background job nobody is waiting for can stop a shop selling, without
   either job referencing the other.
2. Say why starved and broken look identical from outside, and what that does to
   diagnosis during an incident.
3. Say why a bigger shared pool is not a fix, and why an unbounded queue is worse than
   no fix.
4. Describe the mechanism in one sentence, and state honestly how little code it is.
5. Explain why proving the slow job is *still stuck* is the test that makes act two
   evidence rather than coincidence.
6. State the price of a partition — idle threads, lower peak throughput, more numbers
   to size — and argue for or against paying it in a real system of their own.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check, and the two jobs |
| 0:05–0:16 | The outage: a background job stops the sale |
| 0:16–0:24 | Two tempting fixes, both wrong |
| 0:24–0:34 | The mechanism, and the second act |
| 0:34–0:42 | Refusing in zero milliseconds |
| 0:42–0:56 | Exercises, and the bill |
| 0:56–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check, And The Two Jobs

```bash
cd micro-services-design-patterns/bulkhead-pattern
./gradlew test
```

12 tests, green, in about a second.

Introduce the two jobs in words, without code, because the asymmetry between them is
the whole setup:

> **Checkout** takes a shopper's money. It is fast, it is correct, and nobody has ever
> filed a bug against it. It needs exactly one thing: a thread.
>
> **The supplier feed** imports a catalogue overnight. Nobody is waiting for it. If it
> finished an hour late, nothing bad would happen. It calls a partner API that is
> occasionally very slow.

Then the honest warning, which differs from every other project in this category:

> The threads here are real. This is the only project in the category with no fake
> clock, because the subject *is* threads genuinely waiting for one another, and you
> cannot fake a thread being unavailable. Nothing sleeps, though — the slow partner is
> a latch the test holds shut.

## 0:05–0:16 — The Outage

Run it and stop at act one:

```bash
./gradlew run
```

```
  ~  10ms  shared     feed-4         started on shared-worker
  ~  10ms  shared     feed-3         started on shared-worker
  ~  10ms  shared     feed-2         started on shared-worker
  ~  10ms  shared     feed-1         started on shared-worker
  checkout: still waiting for a thread after 300ms
```

**Ask the room what is missing before you explain anything.** Give it a real thirty
seconds. Someone will notice that checkout has no line.

Then the two facts, in this order:

1. **A waiting job holds its thread.** It uses no CPU and does nothing at all, but the
   thread is its until the call returns. Four batches waiting hold four threads.
2. **Checkout is not broken.** Open `theStarvedCheckoutWasNeverBroken`: the same job,
   run the moment a thread is free, completes perfectly.

Land the sentence:

> The shop stopped selling because of a background job nobody was waiting for.

And then the part that makes it hard rather than merely bad:

> Neither job mentions the other. No import, no call, no shared field. They are
> coupled by a resource neither of them names, which is why no amount of reading
> either file will show you this.

Worth saying plainly: starved and broken look identical from outside, and only one of
them is fixable in the code. At three in the morning you are looking for a bug in a
class that does not have one.

## 0:16–0:24 — Two Tempting Fixes, Both Wrong

Ask for fixes before offering any. Both of these will come up.

**"Make the pool bigger."** Forty threads instead of four. Draw it out: the feed takes
forty whenever the partner is slow enough for long enough, and checkout is starved at
forty exactly as it was at four. The number moved; the failure did not. Worse, the
bigger pool takes longer to notice and costs more memory when it goes.

**"Never refuse a job — queue them all."** This sounds like generosity. Ask what the
queue is made of. It converts a fast, visible failure into an out-of-memory crash at an
hour of its choosing, and every caller waits for work that will not start for minutes.

Then put the real question on the board and leave it there:

> The two jobs are connected only by the pool they share. What happens if they stop
> sharing it?

## 0:24–0:34 — The Mechanism, And Act Two

Show the constructor, and let it be a let-down:

```java
new ThreadPoolExecutor(threads, threads, 0L, MILLISECONDS,
        new ArrayBlockingQueue<>(queueCapacity),
        runnable -> new Thread(runnable, name + "-worker"));
```

A fixed pool, a bounded queue, and a name. No algorithm, nothing adaptive, nothing to
tune at runtime.

> A bulkhead is not a clever piece of machinery. It is a decision to stop sharing. The
> pattern lives in having *two* of them, not in anything either one does.

Now act two:

```
  ~   0ms  feed       feed-1         started on feed-worker
  ~   0ms  feed       feed-2         started on feed-worker
  ~   0ms  checkout   checkout       started on checkout-worker
  ~   0ms  checkout   checkout       finished
  checkout: paid ORD-5001
  the feed is jammed -- 2 threads busy, 2 jobs queued
```

Point at the thread names. `feed-worker` against `checkout-worker`. Different threads;
no amount of demand on one side can produce a thread on the other.

### The question to actually ask

Do not let the room celebrate that checkout worked. Ask:

> How do we know the isolation did that, and not the partner API quietly recovering?

Sit with it. Then open `theFeedIsGenuinelyStuck`, which asserts the feed is *still*
jammed at the moment the sale goes through. Without that assertion, a lucky run looks
identical to a correct one.

This generalises well beyond thread pools, and it is worth saying so: **a test that
only checks the good thing happened has not ruled out the good thing happening by
accident.**

## 0:34–0:42 — Refusing In Zero Milliseconds

Two threads, a queue of two, and a fifth batch:

```
  feed is full: no thread and no room in the queue (in 0ms)
  4 accepted, 1 refused
```

Ask whether refusing is a failure or a feature. Drive at the timing:
`theRefusalIsFast` asserts the answer comes back immediately, and that speed is the
entire value. The caller still has time to shed the batch, degrade, or write it down
for tonight.

Same idea as the circuit breaker's fast failure, applied to a queue rather than to a
broken service. If the group has done that project, this is a good moment to say the
two belong together: a breaker so you stop calling a service that has stopped
answering, and a bulkhead so the calls still in flight cannot drown anything that
matters.

## 0:42–0:56 — Exercises, And The Bill

Start with the bill, because it makes the exercises honest:

```
  feed:     2 threads, 2 busy, 2 queued and waiting
  checkout: 2 threads, 0 busy, 2 idle
```

Read the two lines together and let them be uncomfortable. Two threads are doing
nothing beside two jobs waiting for a thread, and they are not allowed to help.
`thesharedPoolIsFasterOnAGoodDay` asserts the other side: one pool of four runs all
four batches at once and finishes sooner.

> Partitioned pools are idle capacity by design. Any description of this pattern that
> does not say so is describing something free, and this is not free.

### Exercise 1 — Starve it again (everyone)

Give checkout's bulkhead one thread and submit two sales while the feed is jammed.
Watch the second sale wait. The wall protects checkout from the feed; it does not
protect checkout from checkout.

### Exercise 2 — Widen the queue (everyone)

Raise the feed's queue capacity to 50 and submit fifty batches. Note that nothing is
refused, the demo appears healthier, and every one of those batches is now waiting on
a partner that is not answering. Ask what has actually improved.

### Exercise 3 — Where do the walls go? (discussion)

In pairs, on their own current system: name the work that must never be starved, and
then name what they would leave idle to guarantee it. Two or three partitions, not
fifteen.

The point to surface: the classification is a business decision. Nothing in the code
can tell you the supplier feed matters less than checkout. If it is not written
down — as a pool, as a number — then during the outage it is decided by whichever job
asked for a thread first.

### Exercise 4 — Stretch: a third bulkhead

Add one for sending confirmation emails and size it. Then ask what happens when there
are fifteen of these: fifteen numbers to size, fifteen that drift out of date, and a
lot of threads doing nothing at three in the afternoon.

## 0:56–1:00 — Wrap-Up

Five sentences:

1. A bulkhead is a decision to stop sharing, not an algorithm.
2. Starved and broken look identical from outside, and only one is fixable in the code.
3. A bigger pool moves the number; an unbounded queue moves the failure somewhere
   worse.
4. Prove the slow job is still stuck, or you have shown a coincidence.
5. Isolation is paid for in idle threads, and you must be able to say that out loud.

## Facilitator Notes

- **The best thirty seconds of the session is silence in act one.** Do not point out
  the missing line. Let someone find it. The pattern lands completely differently when
  the room has experienced absence as a symptom.
- **Expect "just use virtual threads".** It is a good instinct and worth taking
  seriously: virtual threads make a blocked thread cheap, so pure thread exhaustion
  gets much harder to hit. But the underlying resource does not disappear — the
  connection pool, the rate limit, the memory — and neither does the question of what
  must never be starved. Bulkheads move from threads to permits; the decision is
  unchanged.
- **Expect "this is just a rate limiter".** No: a rate limiter bounds how fast work
  arrives, a bulkhead bounds how much of a resource one kind of work may hold. Related
  instinct, different lever.
- **If the group is quiet during exercise 3**, seed it with something concrete from
  your own system and let them argue with your classification. The argument is the
  learning.
- **Do not oversell it.** If someone leaves thinking bulkheads are free and should go
  everywhere, the session has taught them something worse than nothing. Fifteen pools
  is a real failure mode.
- **Timings assume a group that talks.** If they do not, act three and exercise 2 are
  the compressible parts. Act one and the bill are not.

## Materials Checklist

- [ ] JDK 21 installed, `./gradlew test` run once beforehand so nothing downloads live
- [ ] A terminal with a font big enough that the thread names are readable from the
      back of the room — `shared-worker` versus `feed-worker` is the argument
- [ ] [`animation.html`](animation.html) open in a browser tab for the threads being
      taken one at a time
- [ ] [`uml-diagram.md`](uml-diagram.md) open for the four acts as sequences
- [ ] A whiteboard for the two tempting fixes, and for exercise 3
