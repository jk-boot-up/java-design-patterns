# Session Guide — Read–Write Lock Pattern

A 60-minute session built around one question: if two readers can never
conflict, why would a lock ever make them wait for each other — and does
the fix that stops it always pay for itself?

## Learning Objectives

By the end of the session a participant can:

1. Explain what a torn read is, and why it needs two fields, not one.
2. State the one difference between `ReentrantLock` and
   `ReentrantReadWriteLock` that matters for this scenario.
3. Explain why a queued writer is not guaranteed to run next, with a
   concrete mechanism, not a hand-wave.
4. Predict, correctly, whether the read-write lock or a plain mutex will
   be faster for a given critical section — and say why.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the torn read |
| 0:10–0:20 | The naive lock, and its cost |
| 0:20–0:32 | The pattern — and a surprise |
| 0:32–0:44 | Writer starvation and the upgrade deadlock |
| 0:44–0:54 | When the lock loses |
| 0:54–1:00 | Exercises, and wrap-up |

## 0:00–0:10 — Setup, And The Torn Read

```bash
cd concurrency-design-patterns/read-write-lock-pattern
./gradlew -q run
```

Read act one's output together. Ask: how many fields does a `Price`
have? Why does that matter here? What would a single `AtomicReference`
have done differently — hold that thought for act six.

## 0:10–0:20 — The Naive Lock, And Its Cost

Open `naive/SingleLockCatalogue.java`. Ask: can two readers of this class
ever actually conflict with each other? Then why does the lock make them
wait? Run act two and note the number.

## 0:20–0:32 — The Pattern — And A Surprise

Before running act three, ask the room to predict whether it will be
faster or slower than act two. Run it. If the room predicted "faster" —
most will — discuss why the honest measurement disagrees, and read the
explanation in
[`read-write-lock-pattern-explained.md`](read-write-lock-pattern-explained.md)
together.

## 0:32–0:44 — Writer Starvation And The Upgrade Deadlock

Open `pattern/WriterBarging.java`. Ask: what does `tryLock()`'s own
documentation say about a waiting writer? Run act four and confirm.
Then open `pattern/UpgradeDeadlock.java` and ask the room to predict act
five's outcome before running it.

## 0:44–0:54 — When The Lock Loses

Run act six. Ask: of the three approaches measured, which one needs no
lock at all, and why is that safe here specifically? What would have to
be different about `Price` for the snapshot approach to stop being safe?

## 0:54–1:00 — Exercises, And Wrap-Up

1. **Make the critical section heavier.** Add a small, real computation
   inside `ReadWriteCatalogue.read()` — enough to take a few
   microseconds — and re-run act three and act six. Discuss whether the
   ordering changes, and why that would make sense.
2. **Try a fair lock.** Construct `ReentrantReadWriteLock` with `true`
   for fairness in act four, and observe how the writer-barging outcome
   changes, or does not.
3. **Break the upgrade on purpose, safely.** Rewrite
   `UpgradeDeadlock.attemptUpgrade` to release the read lock before
   requesting the write lock, and confirm it no longer deadlocks.

Close with the sentence worth remembering: a read-write lock is not a
free upgrade over a plain mutex — it trades one cost, readers waiting on
each other, for another, coordinating who is currently reading — and for
a small enough critical section, that trade loses.
