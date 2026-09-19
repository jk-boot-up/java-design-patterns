# Session Guide — Future/Promise Pattern

A 60-minute session built around one question: if three lookups do not
depend on each other, why does the naive code make them wait for each
other anyway?

## Learning Objectives

By the end of the session a participant can:

1. Explain, precisely, what a `Future` is a handle to, and when it
   becomes valid to read.
2. State which half of a `CompletableFuture` is the Future and which is
   the Promise, and who holds each.
3. Predict what a stack trace looks like when an asynchronous task fails,
   before seeing act four's output.
4. Explain why `cancel(true)` may not stop a running task, with a
   concrete example.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | Setup, and act one |
| 0:08–0:18 | Act two, and where the time actually went |
| 0:18–0:30 | Future and Promise, the two halves |
| 0:30–0:42 | Exceptions move |
| 0:42–0:52 | Hangs and cancellation |
| 0:52–1:00 | Exercises, and wrap-up |

## 0:00–0:08 — Setup, And Act One

```bash
cd concurrency-design-patterns/future-promise-pattern
./gradlew -q run
```

Read act one's output together. Ask: does the price lookup need to know
the stock count first? (No.) Then why did it wait?

## 0:08–0:18 — Act Two

Open `pattern/ConcurrentProductPage.java`. Ask the room to predict the
total elapsed time before running act two. Confirm it is roughly one
lookup's cost, not three, and ask why — what actually ran at the same
time as what?

## 0:18–0:30 — Future And Promise, The Two Halves

Open `pattern/FutureAndPromise.java`. Ask: which thread calls `get()`?
Which thread calls `complete()`? Are they ever the same thread in this
class? Run act three and confirm the answer out loud.

## 0:30–0:42 — Exceptions Move

Before running act four, ask the room to predict what the stack trace
will contain. Run it and compare. Ask: where is the line that called
`AsyncFailure.attempt(...)`? Why is it not there?

## 0:42–0:52 — Hangs And Cancellation

Run act five and act six back to back. Ask: in act five, what would
happen with no timeout at all on `get()`? In act six, why does `cancel`
return `true` even though the task keeps running? Open
`pattern/CooperativeCancellation.java` and find the exact line that
causes that.

## 0:52–1:00 — Exercises, And Wrap-Up

1. **Make the cancellation actually work.** Change the task in
   `CooperativeCancellation` to check `Thread.currentThread().isInterrupted()`
   at the top of each loop iteration and return early. Confirm the task no
   longer runs to completion after `cancel(true)`.
2. **Chain three callbacks.** Rewrite act two using `thenCombine` instead
   of three separate `get()` calls, and discuss whether the result is more
   or less readable.
3. **Remove the timeout in act five.** Change `attemptGet`'s call to a
   bare `future.get()` with no timeout, and discuss what would happen if
   this ran in the actual test suite rather than being talked about.

Close with the sentence worth remembering: a `Future` is a promise about
*when* a value will be ready, never a promise about *whether* the work
producing it can be stopped once it is running.
