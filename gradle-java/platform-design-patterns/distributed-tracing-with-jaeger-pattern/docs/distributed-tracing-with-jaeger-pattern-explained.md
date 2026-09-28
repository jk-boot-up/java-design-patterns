# Distributed Tracing with Jaeger, Explained

## The pattern in one sentence

Distributed tracing means giving one customer request one identifier, having every piece of work record how long it took and which piece of work asked for it, and putting those records back together afterwards into one story.

## The analogy, before any of the tools' words

Think of a hospital. At reception you are given a wristband with a number on it. You go to X-ray, then for a blood test, then to see a consultant. Every department writes on its own form: what it did, when it started, how long it took, your wristband number, and which department sent you. Nobody carries the forms around with you. At the end of the shift, each department sends its own pile of forms to the records office, and the records office puts your afternoon back together by wristband number.

Now four things the records office makes you think about. If one department forgets to read your wristband and gives you a new number, your afternoon becomes two afternoons, and each looks complete. The forms reach the office at the end of the shift, not while you are still in the building; and if a department burns down before the shift ends, its forms never arrive. Reception may decide to keep forms for only one patient in four, and that decision has to be written on the wristband, or the other departments will keep forms nobody wants. And if one department's clock is slow, its form says you were X-rayed before you arrived. Those four things are this project.

## What OpenTelemetry and Jaeger call these things

**OpenTelemetry** is the set of forms and the rules for filling them in: the tracing library the industry has settled on. Each service uses it to write its own records.

A **span** is one form: one piece of work, with a name, a start time, a length, and the id of the span that asked for it — its **parent**. A span with no parent is a **root**: the front door.

The **trace id** is the wristband number. Every span of one customer request carries the same one.

**traceparent** is the HTTP header that carries the wristband from one program to the next. It is 55 characters: a version, the trace id, the caller's span id, and a flags byte. Writing it onto an outgoing request is called **injecting**; reading it from an incoming one is **extracting**.

**Sampling** is reception's decision to keep a request's records or not. It is made once, at the front door, and travels in the flags byte: 01 for kept, 00 for dropped.

A **batch** is the pile of finished forms sent together. OpenTelemetry holds finished spans in memory and sends a batch every 5 seconds, out of the box, using its own protocol, **OTLP**.

**Jaeger** is the records office: a **collector** that receives every service's batches and joins them by trace id, a store, and a **query API** to ask what it holds.

**Clock skew** is the difference between two machines' clocks. Jaeger can notice it; out of the box it only warns.

## The two services

The **product page** is the front door. It is a real HTTP server in the demo's own Java program. It looks the product up in the catalog, asks pricing for a quote, checks stock, calls recommendations over HTTP, and renders. Each step is a span; the call to recommendations is a span too.

**Recommendations** is a second Java program, started by the demo, with its own HTTP server and its own OpenTelemetry. It reads the header, if there is one, and inside its own span runs a ranking model, the slowest single piece of work in the page.

## The six acts

### A Hop That Forgets The Header

The product page calls recommendations over real HTTP, but leaves out the one line that writes the header. Nothing fails. Recommendations finds no header, so it starts a trace of its own. Jaeger holds two traces for one page load, and each looks perfectly healthy: the page's trace, whose call to recommendations has nothing under it, and a trace holding only recommendations and its ranking model, with no page above it. The two could only be found together by searching both services for the visit id the shop recorded.

```
  the product page calls recommendations over real HTTP, in a second Java process.
  the page does not write the trace header onto that call. traceparent sent: none.
  Jaeger holds 2 traces for one page load, and neither says anything is wrong.
  trace beeb8da1: 6 spans, all from product-page, 1 root.
    its call to recommendations has 0 spans under it.
  trace 3ac55a49: 2 spans, all from recommendations, 1 root.
    the ranking model is in here, with no page above it.
  the two were found together only by searching both services for the visit id the shop recorded.
```

### The Header Forwarded

One line is added: write the current trace context onto the outgoing request. The header the page sent and the header recommendations received are the same 55 characters. Jaeger now holds one trace: eight spans, from two services, with one root. Read as a tree, the ranking model sits inside recommendations' span, which sits inside the page's call. By its own time — its length, less the time spent inside its children — the slowest piece of work is the ranking model, 340 milliseconds or more. And the page's call lasted longer than recommendations took to answer: the difference is the hop itself, the network and the other program's HTTP handling, visible only because both sides reported.

```
  one line added: write the current trace context onto the outgoing request.
  traceparent sent:     00-bfc846100bfc1e42987bbcbfdd7e532f-b9f24f7bae4a6586-01
  traceparent received: 00-bfc846100bfc1e42987bbcbfdd7e532f-b9f24f7bae4a6586-01
  version 00, trace id, the caller's span id, flags 01, which means sampled.
  Jaeger holds 1 trace: 8 spans from 2 services, 1 root. its shape, as Jaeger holds it:
    GET /product/A-2231        product-page
      catalog                  product-page
      pricing                  product-page
      inventory                product-page
      call recommendations     product-page
        GET /recommendations   recommendations
          ranking-model        recommendations
      render                   product-page
  the slowest piece of work, by its own time: ranking-model, in recommendations, 340 ms or more.
  the page's call lasted longer than recommendations took to answer. the difference is the hop itself.
```

### The Collector Puts It Together, Later

The customer has the page, and at that moment Jaeger holds none of its spans. Each service sends its finished spans by itself, in a batch every five seconds. The spans arrive more than two seconds after the customer had the page, and Jaeger then holds eight: six sent by the product page, two sent by recommendations, joined by their trace id. The customer never waits for tracing, which is the point; and nobody sees the trace immediately, which is the price.

```
  the customer has the page. Jaeger holds 0 spans of it.
  each service sends its finished spans by itself, in a batch every 5 seconds.
  the spans arrive more than 2 seconds after the customer had the page.
  Jaeger then holds 8 spans: 6 sent by product-page, 2 sent by recommendations, joined by trace id.
```

### Sampling At The Front Door

The page now keeps one trace in four, decided once, at the front door, from the trace id. Twenty page loads: six kept, fourteen dropped. A kept load's header ends 01; a dropped load's header ends 00. Recommendations obeys the flag it is sent, and records spans only for the six. Jaeger holds six traces of the twenty. A customer complains about the first page load of the twenty, and Jaeger has no trace of it, and never will: the decision was made at the only moment when nothing at all was known about that request.

```
  the page keeps one trace in 4, decided once, at the front door, from the trace id.
  20 page loads. kept: 6. dropped: 14.
  a kept load's header ends -01:    00-2ee9dc9fc86ae25de30fe2669284d85d-d6e5445f3c8658e2-01
  a dropped load's header ends -00: 00-e474c66a4b98b030dbef19fc8e7b845f-ebb1ae25f75e1f5e-00
  recommendations obeys the flag it is sent. it recorded spans for 6 page loads.
  Jaeger holds 6 traces of the 20.
  a customer complains about visit-4-1. Jaeger has no trace of it, and never will.
```

### A Clock That Is Off

The recommendations machine's clock is set three seconds slow; the page's clock is right. The trace is complete and every parent link is correct. But in time order, Jaeger's first span is recommendations' own, before the page that asked for it: it starts between two and three seconds before the call that caused it. Jaeger notices, and attaches its own warning — clock skew adjustment disabled; not applying calculated delta of about three seconds. Out of the box it stores what each service said and corrects nothing.

```
  the recommendations machine's clock is 3 seconds slow. the page's clock is right.
  Jaeger holds 1 trace: 8 spans, 1 root. the parent links are all correct.
  in start order, Jaeger's first span is GET /recommendations, before the page that asked for it.
  recommendations' span starts between 2 and 3 seconds before the call that caused it.
  Jaeger's own warning: clock skew adjustment disabled; not applying calculated delta of about 3 seconds.
  the collector stores what each service says. it does not correct a service's clock.
```

### The Bill

Recommendations answers the customer and is then killed before its next batch. The page stops politely, which sends what it holds. Jaeger holds six spans of that page load, all from the page, and none from recommendations; they never arrive, and the page's call to recommendations has nothing under it. The spans a crash loses are always the last ones before it — the ones about the crash. Every page load costs eight spans from two processes, and a 55-character header on every hop. And Jaeger is one more system to run; at start-up it said it was using its default configuration with memory storage, so everything it holds goes when it stops.

```
  recommendations answers visit-6, then is killed before its next batch. the page stops politely.
  Jaeger holds 6 spans of visit-6: 6 from product-page, 0 from recommendations. they never arrive.
  the page's call to recommendations has 0 spans under it. the spans lost are the last ones before the crash.
  every page load costs 8 spans from 2 processes, and a 55 character traceparent header on every hop.
  and Jaeger is one more system to run. it said at start-up: No '--config' flags detected, using default All-in-One configuration with memory storage.
  this demo needed 1 container for 2 service processes, and removes it, with every span in it, at the end.
```

## The verdict

Put a collector behind your services as soon as one customer request crosses more than one program. Then say five things out loud, because nothing will fail if you forget them: write the header on every call that leaves a program, and read it on every call that arrives; sample once, at the front door, and let the decision travel; shut services down politely, so their last batch is sent; keep the machines' clocks in step; and give the collector real storage before you rely on it.

## How to recognise this in code you did not write

- A call to `inject` with the current context just before an HTTP request is sent, and `extract` at the top of a request handler. That is context propagation.
- An HTTP client created with no tracing on it, in a service that is otherwise traced. That is act one waiting to happen.
- `Sampler.parentBased(...)`: the service follows the decision in the header rather than making its own.
- `BatchSpanProcessor` and its schedule delay: how many seconds of spans a crash can lose.
- A shutdown hook that closes the tracer provider, or its absence.

## Where you have already met this

Any request that goes through several services at a shop, a bank or a streaming site. Spring Boot, Quarkus, Micronaut and the OpenTelemetry Java agent all write and read `traceparent` for you; Jaeger, Grafana Tempo, Zipkin and the hosted tracing products all assemble the same trees from the same batches.

## When this is too much

If the shop is one program, a profiler or a log with a request id answers the question without a collector to run. A collector earns its keep once a single request crosses several programs and somebody has to say which of them was slow.
