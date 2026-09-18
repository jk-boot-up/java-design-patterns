# Session Guide — Distributed Tracing Pattern

A one-hour facilitated session. It works as a live-coded walkthrough, a
study-group session, or a lunchtime talk with the exercises cut.

The session has one shape: spend the first fifteen minutes making the group feel
the problem properly, because the pattern is obvious once the problem is felt and
forgettable if it is not.

---

## Learning Objectives

By the end, everyone can:

1. Say why merged logs cannot measure a service under concurrency, and why more
   logging does not fix it.
2. Name the two fields that make a trace — trace id and parent span id — and say
   what each one buys.
3. Compute self time by hand and explain why it names a culprit when total time
   cannot.
4. Recognise the three ways tracing quietly stops working: a missing span, a lost
   context across a thread, and a sampled-away trace.
5. Point at the one line in their own codebase most likely to be losing context.

---

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup, and a question nobody can answer |
| 0:05–0:15 | The problem: two customers, four logs |
| 0:15–0:25 | The pattern: one id, one parent link |
| 0:25–0:38 | Code walkthrough |
| 0:38–0:50 | Exercises |
| 0:50–0:58 | The bill |
| 0:58–1:00 | Wrap-up |

---

## 0:00–0:05 — Setup, And A Question Nobody Can Answer

Have everyone run:

```bash
./gradlew run
```

Then put the Act 1 text on screen and ask the room:

> A product page takes nine hundred milliseconds. Four services contributed.
> Which one is slow?

Take answers. Somebody will say "recommendations, it's always recommendations".
Ask them how they would *prove* it with what the shop currently has. That question
is the session.

**Facilitator note:** resist explaining anything yet. The next ten minutes work
only if the group has actually tried and failed.

---

## 0:05–0:15 — The Problem: Two Customers, Four Logs

Put the Act 2 output on screen. Give the room two full minutes with this and no
commentary:

```
  14:32:07.120  catalog          lookup complete
  14:32:07.120  pricing          quote started
  14:32:07.160  catalog          lookup complete
  14:32:07.160  pricing          quote started
  14:32:07.300  pricing          quote complete
  14:32:07.340  pricing          quote complete
```

> How long did pricing take?

Somebody will answer 180ms. Ask which two lines they subtracted. Then point out
that the other pairing gives 220ms and looks equally reasonable, and that one of
the two is Ada's start with Ben's finish.

Then ask the question that lands the point:

> What would you add to these log lines to fix it?

Collect suggestions. You will get: the thread name, the pod name, the product id,
the response size. Take each one and ask whether it is *the same across one
request and different across the next*. None of them is. The thread name is close
and fails the moment work crosses a thread — which is a nice piece of foreshadowing
for 0:50.

Land it explicitly: **the missing thing is not detail, it is an identifier.**

---

## 0:15–0:25 — The Pattern: One Id, One Parent Link

Two moves, and let the group discover the second one.

**Move one.** Give the front door an id and pass it down. Ask: does that fix the
question from Act 1? Let somebody work out that it fixes the *pairing* — you can
now filter the log to one request — but it still does not say where the time went,
because a filtered log is still a list of timestamps.

**Move two.** Each unit of work also records *what called it*. Put the Act 3
output up:

```
  ranking-model    span-6     parent span-5      340ms
  recommendations  span-5     parent span-1      400ms
  product-page     span-1     parent (none)      900ms
```

Ask someone to read the parent column aloud and describe the shape. Then show the
waterfall and let the room see that nobody designed it — it is that column, drawn.

Then do the self-time arithmetic **on a whiteboard, by hand**, before showing the
program's answer:

- page: 900ms, children 900ms → **0ms**
- recommendations: 400ms, child 340ms → **60ms**
- ranking-model: 340ms, no children → **340ms**

Ask: which of those three is the answer? The longest span is the page, and the
page did nothing at all. That is the moment the pattern earns its keep.

---

## 0:25–0:38 — Code Walkthrough

Read in this order, and do not read the whole file — read the named part.

| File | What to show | The sentence to say |
| --- | --- | --- |
| `TraceContext` | the record, and `childWith` | "Two strings. Everything else is bookkeeping." |
| `Span` | the six fields | "Five of these are obvious. The parent is the pattern." |
| `Tracer.Scope.close()` | the whole method | "The closing brace is what records the span." |
| `ProductPage.load` | the recommendations block | "This argument is `recommendations.context()`, not `request`." |
| `Trace.selfTime` | all four lines | "Duration minus what it was waiting on. That is the trick." |
| `Waterfall.appendSpan` | `offset` and `length` | "Two divisions. Jaeger's picture is this picture." |

Spend the most time on `ProductPage.load`'s recommendations block. Ask what would
happen if the inner span were started from `request` instead. Do not answer — that
is Exercise 1.

---

## 0:38–0:50 — Exercises

### Exercise 1 — Flatten the tree (everyone, 5 min)

In `ProductPage.load`, change the ranking model's span to start from `request`
instead of `recommendations.context()`. Run it.

What to expect: the model becomes a sibling of recommendations rather than its
child. Recommendations' self time jumps from 60ms to 400ms, and the model still
shows 340. The total still adds to 900.

The discussion point: the arithmetic still closes, the trace still has one root and
no orphans, and the answer is now wrong. **A trace can be internally consistent and
false.**

### Exercise 2 — Lose a span (everyone, 4 min)

Replace the pricing `try (...)` with a bare `tracer.start(request, "pricing")` and
no close. Run it.

Pricing vanishes entirely and the page grows 180ms of self time. Ask what that
would look like at three in the morning: a page that appears to spend a fifth of
its time rendering.

Then ask the real question: **in your own codebase, where could an exception be
thrown past an open span?**

### Exercise 3 — Break it across a thread (discussion, then code)

Before running Act 6, ask the room to predict what happens when the
recommendations call moves to a worker thread and the context is in a
thread-local.

Most rooms predict an error, or a missing span. The answer is neither: two roots, a
complete-looking trace, and no warning. Run it and show them.

Then show `withExplicitContext` and ask what changed. It is one line moved earlier.

### Exercise 4 — Stretch

Add a `fraud-check` span inside pricing, lasting 40ms, and adjust pricing's own
work so the page still totals 900. Run it. `Waterfall` and `Trace` need no changes
at all — which is the point about the drawing being derived rather than designed.

---

## 0:50–0:58 — The Bill

Three failures, and the honest framing is that all three are the *cost* of the
pattern rather than mistakes made while applying it.

**A service that is not instrumented.** Show Act 5's waterfall next to Act 4's.
Ask what is different. Somebody will spot that the ranking model moved up a level.
Ask what a person who had never seen Act 4 would conclude. They would conclude the
page renderer is slow, and they would be wrong, and nothing would have told them.

Land it: **partial instrumentation is worse than none**, because none tells you
nothing and partial tells you something false.

**Sampling.** Show Act 7. Ten thousand kept, nine hundred and ninety thousand
gone, and the one somebody complained about is in the second group. Ask when the
decision was made — at the front door, before anything was known.

Then ask the room what they would do about it, and let tail sampling be their idea
rather than yours. Somebody always gets there: hold the spans, decide at the end.

**If time allows — the question worth leaving open.** Tracing is one of three
things: logs, metrics, traces. Ask which of the three answers "what was the error
message", which answers "how did yesterday compare", and which answers "where did
the time go in this one request". Most teams try to make logs do all three.

---

## 0:58–1:00 — Wrap-Up

The three sentences to leave people with:

1. **A trace id makes a log readable. A parent span id makes it an answer.** If
   you only do one of the two, do both.
2. **Self time, not total time.** The longest span is always the request itself and
   it is always innocent.
3. **The context dies at boundaries.** Threads, queues, scheduled jobs. Pass it as
   a value; never trust a thread-local to make the trip.

And one action: ask everyone to find, in their own codebase this week, one
`executor.submit(...)` or `CompletableFuture.supplyAsync(...)` and check whether
anything traced happens inside it.

---

## Facilitator Notes

**The first fifteen minutes are not padding.** Every group that is shown the
waterfall before they have failed at the log exercise treats the pattern as
obvious, and then does not remember why the parent link matters.

**Do not let "just use Jaeger" close the conversation early.** It will come up
around 0:20. The reply is that Jaeger draws the picture and does not produce the
data — if your services do not open spans and forward context, Jaeger shows you
the same nothing.

**The self-time whiteboard moment is the peak of the session.** Do it by hand, do
it slowly, and let the room say "the page did nothing" out loud before you do.

**Exercise 1 is the highest-value exercise.** The lesson — that a wrong trace looks
exactly like a right one — is what people carry back to work.

**Expect a question about overhead.** Six spans per request costs serialisation, a
write to a collector, and storage. It is usually small and it is never zero, and
"trace everything at full fidelity" is a decision with an invoice attached.

**Expect a question about OpenTelemetry.** The honest answer: this project is forty
lines of the thing OpenTelemetry standardises, and learning the standard is a
better use of a week than learning any one vendor's SDK.

---

## Materials Checklist

- [ ] JDK 21 installed, `./gradlew test` green (82 tests)
- [ ] `./gradlew run` output ready to project, Acts 2, 3, 4, 5, 6 and 7 bookmarked
- [ ] `docs/animation.html` open in a browser tab
- [ ] A whiteboard, for the self-time arithmetic
- [ ] `docs/uml-diagram.md` diagram 4, for the thread boundary, if the room wants
      the sequence rather than the code
