# Session Guide — Distributed Tracing with Jaeger Pattern

A 60-minute session built around one question: once a trace is assembled by a separate collector from separate reports, what can make it late, split, out of order, or missing — without any error?

## Learning Objectives

1. Say, in plain words, what a span, a trace id, a parent, the traceparent header, sampling, a batch and a collector are.
2. Show one missing line splitting one page load into two traces, and read a traceparent header field by field.
3. Explain why the collector holds nothing when the customer has the page, and what a crash before the next batch loses.
4. Explain why the sampling decision travels in the header, and why a dropped trace cannot be recovered.
5. Explain what a slow clock does to a trace, and what Jaeger does about it out of the box.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The hospital wristband analogy, and the twin project recapped in two minutes |
| 0:08–0:20 | Acts one and two: the forgotten header, then the header forwarded |
| 0:20–0:30 | Act three: the collector puts it together, later |
| 0:30–0:40 | Act four: sampling at the front door |
| 0:40–0:50 | Act five: a clock that is off |
| 0:50–0:55 | Act six: the bill, and the verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd platform-design-patterns/distributed-tracing-with-jaeger-pattern
./gradlew -q run
```

Act one: nothing failed, so how would anybody notice? Act two: which part of the header is the trace id, and which part is the page's span? Act three: why does the customer never wait for the spans? Act four: why does recommendations not get its own vote? Act five: the parent links are right — so what exactly is wrong? Act six: which spans does a crash always lose?

Then open `src/main/java/com/jk/explore/tracingjaeger/ProductPageService.java` and find the `inject` line, and `RecommendationsService.java` and find the `extract` line. Those two lines are the whole of context propagation.

## Discussion

Ask the room where else a request leaves a program: a message on a queue, a scheduled job, a call to a database. Each needs the same two lines, and a message broker has no HTTP headers.

Then ask what a batch every 5 seconds means for a service that restarts ten times a day. What would you trade to lose less — a shorter batch, or a slower shop?

## Exercises

1. Remove the `inject` line and run the second act. Predict what Jaeger holds before you look.
2. Change the sampler to keep one in two, and predict whether the same page loads are kept as before.
3. Set `BATCH_EVERY` to 1 second and run the third act. What does the customer see, and what does Jaeger hold at once?
4. Make the recommendations clock 3 seconds fast instead of slow. Where does its span land now?
5. Add a line at the end of `main` that waits for Enter before Jaeger is stopped, print the query port, open Jaeger's web page on it, and find the two traces from the first act by their visit id.

Close with the verdict: carry the header across every hop, sample at the front door and let the decision travel, shut services down politely so their last batch is sent, keep the clocks in step, and give the collector real storage before relying on it.
