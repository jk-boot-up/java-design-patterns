# Problem Statement

## The scenario

A customer opens the page for product A-2231. The product page looks the product up in the catalog, asks pricing for a quote, checks stock, asks the recommendations service what else to show, and renders. Recommendations is a separate program, reached over HTTP, and inside it a ranking model does the slowest single piece of work in the whole page. When the page is slow, somebody has to say which of those steps spent the time — and the steps live in two different programs, each with its own log and its own clock.

## The naive version

Each service keeps its own record. The product page knows it called recommendations and waited. Recommendations knows it ran a ranking model. Neither record mentions the other, and nothing joins them. The first act of the demo shows exactly this with real tracing turned on but the header left off the call:

```
  Jaeger holds 2 traces for one page load, and neither says anything is wrong.
  trace beeb8da1: 6 spans, all from product-page, 1 root.
    its call to recommendations has 0 spans under it.
  trace 3ac55a49: 2 spans, all from recommendations, 1 root.
```

## What the twin project already did

The plain-Java Distributed Tracing project in this course built the whole idea by hand: a trace id minted at the front door, a span for every step naming its parent, a waterfall drawn from the parent links, own time as the way to find the culprit, and the three quiet failures — a service that opens no span, a context lost across a thread, and a trace sampled away. It is a complete teaching of the pattern and nothing here replaces it.

It had three comforts, though. Everything ran in one program, so the context was an object handed from method to method. The demo held every span in a list and drew the trace itself, the moment the request finished. And there was one clock, scripted by the demo, so every span started exactly when it should.

## What this project must deliver

The same product page and the same steps, as two real services in two Java programs, talking over real HTTP, instrumented with OpenTelemetry and reporting to a real Jaeger that the demo starts in a container and removes at the end. The trace context carried across the hop in the W3C `traceparent` header, and the same call without it, splitting one page load into two traces. A trace assembled by the collector, not by the demo, and read back from the collector's own query API. Spans that arrive in batches after the customer has the page. A sampling decision that travels in the header's last two characters. A clock 3 seconds slow, and what Jaeger does about it. And an honest bill: a service killed before its next batch loses its spans for good, every page load costs 8 spans, and Jaeger out of the box keeps everything in memory.

Every figure printed is the program's own, and two runs back to back print the same thing.
