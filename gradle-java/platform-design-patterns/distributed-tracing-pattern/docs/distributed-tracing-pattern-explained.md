# The Distributed Tracing Pattern, Explained

## In One Sentence

Give every customer request a single identifier at the front door, make every
piece of work along the way record what it was, how long it took, and **which
piece of work called it**, and the request's shape — and the reason it was slow —
falls out of the arithmetic.

Two fields are doing all the work there. The **trace id** is what lets you gather
one request's worth of data out of four hundred requests' worth of noise. The
**parent span id** is what turns that data into a shape you can read. Most
homegrown versions of this pattern have the first and not the second, which is why
they can filter a log and still not name a culprit.

---

## Everyday Analogy: The Hospital Wristband

A patient arrives at a hospital for a day of tests. Reception puts a wristband on
them with a number printed on it, and from that moment on every department writes
that number on everything: the blood sample, the X-ray, the notes, the
prescription. At the end of the day somebody can pull every record with that
number on it and see the whole visit.

That is the trace id, and on its own it is already a large improvement over a
hospital where each department keeps its own book. But notice what it still cannot
tell you. If the patient waited three hours, the wristband number lets you gather
all the records, and it does not tell you *where the three hours went*, because
nothing in the file says that the X-ray was waiting on the blood result, or that
the consultant was waiting on the X-ray.

Now add one line to each record: **who sent me here**. Radiology writes down that
the patient was sent by the consultant. The consultant writes down that the
patient came from reception. Suddenly the day has a shape. You can lay every
department's slot out on a timeline, nested under whoever referred the patient, and
see at a glance that two hours and forty minutes of the three hours was one
department, and that everybody else was simply waiting behind it.

That second line — *who sent me here* — is the parent span id, and it is the whole
difference between a searchable record and an answer.

One more thing the analogy gets right, unfortunately. If a porter wheels the
patient to a department and forgets to hand over the notes, nothing goes wrong
visibly. The department does its work, writes its own record, and that record sits
in the file with no referral on it — belonging to the visit, but attached to
nothing. Nobody is alerted. The only symptom is that the timeline no longer adds
up, and you have to already be looking to notice.

---

## The Problem, In The Shop

A customer opens a product page and it takes nine hundred milliseconds. Four
services contributed: catalog, pricing, inventory and recommendations. Every one of
them is healthy, every one of them logs, and the log aggregator works.

The aggregator merges the four streams by time, and because the shop serves more
than one customer at once, the merged log contains two of everything:

```
  14:32:07.120  catalog          lookup complete
  14:32:07.120  pricing          quote started
  14:32:07.160  catalog          lookup complete
  14:32:07.160  pricing          quote started
  14:32:07.300  pricing          quote complete
  14:32:07.340  pricing          quote complete
```

Two starts, two finishes, four correct timestamps and no way to pair them. Pairing
the first start with the first finish gives 180ms. Pairing it with the second gives
220ms. Both look plausible; one of them is Ada's start and Ben's finish.

Adding more fields to the log lines does not help, because the missing thing is not
detail. It is an identifier that is the same across one request and different
across the next.

---

## The Pattern

Three moves, and the third is the one that is usually skipped.

**One: mint an id at the front door.** The first service to see the request
generates a trace id and puts it in the outgoing headers of every call it makes.
Everything downstream reads it from the incoming headers and passes it on. In this
project the id is `trace-4f2a`; in a real system it is random hexadecimal.

**Two: record a span around every unit of work.** A span is four things — a name,
a start, a duration, and the id of the span that caused it. Opening and closing a
span is all the instrumentation asks of you:

```java
try (Tracer.Scope pricing = tracer.start(request, "pricing")) {
    clock.advance(PRICING_MS);
}
```

**Three: pass the context to everything you call.** `scope.context()` carries the
trace id and this span's id, and whatever receives it opens its spans as children
of that. This is the move that produces the shape, and it is also the move that
gets forgotten, because forgetting it is silent.

Once those three habits are in place, nobody has to design the waterfall. The
waterfall is simply what a set of spans *looks like* when each one knows its
parent.

---

## Participants

| Type | Role |
| --- | --- |
| `TraceContext` | The two values that must travel: trace id and current span id |
| `Span` | One unit of work — name, start, duration, parent |
| `Tracer` | Mints span ids, times the work, collects the spans |
| `Tracer.Scope` | An open span; closing it is what records the duration |
| `Trace` | Every span from one request, and the arithmetic over them |
| `Waterfall` | The drawing, derived entirely from the parent links |
| `ProductPage` | The e-commerce request being traced, instrumented and not |
| `InterleavedLog` | The problem: four logs merged by time, with nothing to pair |
| `AsyncHandoff` | The thread boundary, breaking the trace and then not |
| `Sampler` | The third item on the bill: the trace you needed was discarded |
| `Clock.Scripted` | Declared durations, so every number here is reproducible |

---

## Code Walkthrough

### The two values that have to travel

```java
public record TraceContext(String traceId, String spanId) {

    public TraceContext childWith(String childSpanId) {
        return new TraceContext(traceId, childSpanId);
    }
}
```

The smallest type in the project and the one everything else depends on. Same
trace, new parent: the span doing the calling becomes the parent of the span being
called. Get that one line wrong — keep the parent id instead of replacing it — and
the trace comes back flat, every span a sibling of every other, with the shape that
told you where the time went thrown away.

Notice that it is passed as an ordinary method argument throughout this project.
Real libraries hide it in a thread-local, and that convenience is exactly where it
gets lost. More on that below.

### The span, and the field people leave out

```java
public record Span(String traceId,
                   String spanId,
                   String parentSpanId,   // null only at the front door
                   String name,
                   long startMillis,
                   long durationMillis) { }
```

A name so you know what the work was. A start and a duration so you know when and
how long. And a parent, which is the field that turns a pile of timings into a
tree. Timestamps tell you when things happened; they do not tell you that the
pricing call happened *because of* this page request.

### Opening and closing a span

```java
public Scope startRoot(String name) {
    return new Scope(null, name);
}

public Scope start(TraceContext parent, String name) {
    return new Scope(parent.spanId(), name);
}
```

And the part worth dwelling on — `close()` is what records the span, because
closing is the moment the duration is known:

```java
@Override
public void close() {
    if (closed) {
        return;
    }
    closed = true;
    spans.add(new Span(traceId, spanId, parentSpanId, name,
            startMillis, clock.now() - startMillis));
}
```

A span that is started and never closed never appears in the trace at all. That is
not a quirk of this implementation; it is why real instrumentation uses
try-with-resources. An exception thrown past an un-closed span deletes the record
of the very call that failed, which is the worst possible moment to lose a span.
`TracerTest` pins that behaviour down deliberately rather than treating it as an
embarrassment.

### The instrumented page

```java
try (Tracer.Scope page = tracer.startRoot("product-page")) {
    TraceContext request = page.context();

    try (Tracer.Scope catalog = tracer.start(request, "catalog")) {
        clock.advance(CATALOG_MS);
    }
    ...
    try (Tracer.Scope recommendations = tracer.start(request, "recommendations")) {
        try (Tracer.Scope model =
                     tracer.start(recommendations.context(), "ranking-model")) {
            clock.advance(RANKING_MODEL_MS);
        }
        clock.advance(RECOMMENDATIONS_MS - RANKING_MODEL_MS);
    }
```

Read the shape rather than the contents. Every unit of work opens a span, hands
`context()` to anything it calls, and closes the span when it is done. Note the
inner block: the ranking model is started from `recommendations.context()`, not
from `request`, which is why it nests one level deeper. That single argument is the
difference between "recommendations is slow" and "the scoring model inside
recommendations is slow", and only one of those is actionable.

### Self time, which is the whole trick

```java
public long selfTime(Span span) {
    long childTime = childrenOf(span.spanId()).stream()
            .mapToLong(Span::durationMillis)
            .sum();
    return span.durationMillis() - childTime;
}
```

Four lines, and they are the reason a trace beats a stopwatch.

The root span lasted the entire request, so on total time it is always the biggest
and always useless — it tells you the page was slow, which is what you were told
at the start. Subtract the time it spent waiting on its children and the page's
self time is **zero**, because the page did no work; it waited. Do that for every
span and the list sorts itself into an accusation:

```
    ranking-model     340ms   37% of the page
    pricing           180ms   20% of the page
    catalog           120ms   13% of the page
    render            110ms   12% of the page
    inventory          90ms   10% of the page
    recommendations    60ms    6% of the page
```

Recommendations lasted four hundred milliseconds but is charged only sixty, because
three hundred and forty of them belong to the model it called. And those six
figures add up to exactly nine hundred — every millisecond of the request charged
to exactly one span, which `TraceTest` asserts, because if that sum ever drifts the
arithmetic is lying.

### The drawing

```java
long total = Math.max(trace.endMillis(), 1);

int offset = (int) (span.startMillis() * BAR / total);
int length = Math.max(1, (int) (span.durationMillis() * BAR / total));
```

Two lines of arithmetic per span: where its bar starts, and how long it is, both as
a share of the whole request. Everything else is indentation from the parent links.

The `Math.max(1, ...)` matters more than it looks. A one-millisecond span in a
nine-hundred-millisecond request rounds to zero characters of bar, and a span drawn
as nothing looks exactly like a span that never happened — which is the one thing
this drawing must never suggest.

And `trace.endMillis()` rather than the root's duration, because on a broken trace
those are different numbers. Scaling to the first root would draw orphaned work as
though it filled the request, hiding the very failure the drawing is being used to
show.

---

## And Now The Bill

### One: a service that is not instrumented

Recommendations forgets to open a span. It still receives the context and still
forwards it, so nothing errors and nothing warns:

```java
// No span opened here. The context is forwarded unchanged, which is
// the part that makes this so hard to spot: the chain is not
// broken, it is just missing a link, so the model's parent becomes
// the page.
try (Tracer.Scope model = tracer.start(request, "ranking-model")) {
    clock.advance(RANKING_MODEL_MS);
}
clock.advance(RECOMMENDATIONS_MS - RANKING_MODEL_MS);
```

The result is not a gap. It is a wrong answer:

```
  trace trace-7c19   total 900ms
  product-page            |============================================|   900ms   60ms of it its own
    catalog               |=====                                       |   120ms
    pricing               |     ========                               |   180ms
    inventory             |              ====                          |    90ms
    ranking-model         |                   ================         |   340ms
    render                |                                      ===== |   110ms
```

The four hundred milliseconds did not disappear — it landed on the parent. The page
now appears to spend sixty milliseconds doing work it never did. The ranking model
appears to hang directly off the page, which is a call that does not exist in the
code. And the service actually responsible is not on the diagram at all.

The trace has one root and no orphans. By every check you would think to run, it
looks healthy. `ProductPageTest` asserts exactly that, because "it looks healthy"
is the finding, not an oversight:

```java
assertEquals(List.of(), partial.orphans());
assertEquals(1, partial.roots().size());
```

Somebody spends the afternoon reading the page renderer.

### Two: the work moves to another thread

```java
private static final ThreadLocal<TraceContext> CURRENT = new ThreadLocal<>();
```

Real tracing libraries do this, for a good reason: it keeps the context out of
every method signature. It works perfectly until the work moves to a thread pool, a
`CompletableFuture`, or a scheduled job, because a thread-local belongs to a thread
and the new thread's copy is empty.

```java
runOnAnotherThread(() -> {
    // On the worker thread this is null, because thread-locals
    // do not travel. The code reads as though it does.
    TraceContext inherited = CURRENT.get();
```

```
  trace trace-async-broken   total 400ms   2 separate roots — this trace is broken
  product-page            |============================================|   400ms
  recommendations         |============================================|   400ms
```

Two roots in one trace. Four hundred milliseconds belonging to nobody. No
exception, no warning, and the broken code is indistinguishable from the working
code at a glance.

The fix is unglamorous and total. Read the context on the thread that has it, and
hand it to the task as an ordinary value:

```java
// Captured here, on the thread that actually has it.
TraceContext captured = page.context();

runOnAnotherThread(() -> {
    try (Tracer.Scope strip = tracer.start(captured, "recommendations")) {
        clock.advance(ProductPage.RECOMMENDATIONS_MS);
    }
});
```

```
  trace trace-async-fixed   total 400ms
  product-page            |============================================|   400ms   0ms of it its own
    recommendations       |============================================|   400ms
```

A value does not care which thread reads it. Every real tracing library ships a
wrapper that does this for you, and the reason to see it written out once is so the
wrapper stops being magic — and so that when you write the executor submission
yourself, you remember there is something to wrap.

`AsyncHandoffTest` has one assertion that states the discomfort plainly: both
versions record two spans, the same four hundred milliseconds, and no error. The
only thing the broken run lost is the link, and the link was the only useful part.

### Three: you kept one trace in a hundred

```java
public boolean keep() {
    return seen++ % oneIn == 0;
}
```

A thousand requests a second at six spans each is half a billion spans a day.
Nobody pays for that, so you sample.

```
  kept       10,000
  discarded  990,000

  A customer complains about request number 862,144.
  Was it kept?  no — it is gone, and it is not recoverable
```

The uncomfortable part is *when* the decision is made. Sampling is per trace, at
the front door, before anybody could know the request was going to matter. So the
one request somebody complains about was discarded for exactly the same reason as
every other request: nothing about it stood out yet.

You are not left with nothing. A one per cent sample answers "recommendations is
slow on average" perfectly well, which is what tracing is genuinely best at. What
you are left without is the specific trace for the specific complaint, which is
what you were asked for.

The way out is **tail sampling**: buffer the spans briefly and decide to keep the
trace once you know it was slow or it failed. That costs more and needs a collector
that can hold spans in flight, and it is what to reach for the first time "we
sample at one per cent" fails you.

---

## What This Simulation Does Not Show

Being straight about the boundaries of the model matters, because Tier 1 here runs
entirely offline with declared durations.

**There is no network.** The five services are method calls. In a real system the
context travels in HTTP headers — `traceparent`, under the W3C Trace Context
standard — and the failure modes include a proxy that strips unknown headers, a
message queue with no header support, and a service written in another language
whose library uses a different propagation format. None of those can happen here.

**Time is declared, not measured.** `Clock.Scripted` moves forward when a service
says how long it took. That is what makes every figure in this document and in the
video reproducible, and it also means there is no clock skew — which in a real
distributed trace is a genuine nuisance, because two machines disagreeing by fifty
milliseconds can draw a child that appears to start before its parent.

**Span ids are sequential.** `span-1`, `span-2`, and so on, for readability. Real
ids are random so that two machines cannot collide.

**The handoff waits.** `AsyncHandoff` submits to an executor and then blocks on the
result, because the scripted clock is not thread-safe and this project would rather
be readable than concurrent. The trace breaks in exactly the same way it would
under a real pool, because what breaks it is the thread change, not the
parallelism.

**There is no backend.** No collector, no storage, no query UI, no retention
policy. The waterfall is drawn in the console. That is deliberate: a hosted tracing
tool's flame graph is not a feature of the tool, it is what a set of spans looks
like once each one knows its parent, and seeing it drawn from forty lines of Java
is the point.

The Tier 2 directory, described in the category's plan, is where the trace id has
to survive a real HTTP hop into a real backend.

---

## Why The Tests Are The Proof

Eighty-two tests, and they are doing something slightly unusual: several of them
assert that a **broken** trace is broken in a specific way.

`ProductPageTest` asserts that the partially-instrumented trace has one root and no
orphans — that it passes every health check — and then asserts that the page's self
time is sixty milliseconds when it should be zero. Those two assertions together
are the finding: the failure is invisible to structure and visible only in
arithmetic.

`AsyncHandoffTest` asserts that the broken and fixed traces contain the same number
of spans and the same elapsed time, differing only in one parent link.

`WaterfallTest` checks properties rather than characters — that a child is indented
under its parent, that a later span's bar starts further right, that a
one-millisecond span still gets one character — so the drawing can be re-tuned
without rewriting the tests.

`DemoRunsTest` captures the demo's output and asserts the exact strings this
document and the video quote, including `ranking-model     340ms   37% of the page`.
Nothing in the teaching material is typed from memory; if a figure in a narration
line stops matching the program, a test says so before a recording does.

---

## What You Gain

- **A culprit, by name.** "The ranking model, 340ms, 37% of the page" instead of
  "the page is slow".
- **The shape of the request.** Which calls were sequential, which nested, and what
  each one was waiting on.
- **A readable merged log.** The trace id alone fixes the pairing problem the four
  logs had.
- **Arithmetic that closes.** Every millisecond charged to exactly one span, so you
  can tell the difference between slow work and slow waiting.
- **One place to look.** Not four dashboards and a guess.

---

## What To Watch Out For

**Partial instrumentation is worse than none.** A missing span produces a
confident wrong answer, not a visible gap. If you instrument, instrument every hop
in the path you care about.

**Thread and process boundaries are where the context dies.** Executors,
`CompletableFuture`, message queues, scheduled jobs, retries on a background
thread. Pass the context as a value, or use your library's wrapper, and never
assume a thread-local made the trip.

**Head-based sampling throws away the trace you will want.** If the question is
"why was this one slow", one per cent will fail you. Know that before the incident,
not during it.

**Span names must be low-cardinality.** `"pricing"`, not
`"pricing for customer 88213"`. A name per customer makes aggregation impossible
and the storage bill enormous.

**A trace is not a log and not a metric.** It tells you where the time went in one
request. It will not tell you the error message, and it will not tell you the
ninety-ninth percentile across the day. Those are the other two of the three, and
this pattern does not replace them.

**Instrumentation has a cost.** Six spans per request is not free — there is
serialisation, a network write to a collector, and storage. It is usually a small
cost, and it is not zero, and "trace everything at full fidelity" is a decision
with an invoice attached.

---

## Distributed Tracing vs. Logs vs. Metrics

| | Answers | Cannot answer |
| --- | --- | --- |
| **Logs** | What happened, and what the error said | Which of four hundred concurrent requests this line belongs to |
| **Metrics** | How the system behaves in aggregate, cheaply | Anything about one specific request |
| **Traces** | Where the time went in one request, and what called what | What the error message was; how yesterday compared |

The three are complements, not competitors, and the usual mistake is trying to make
logs do the third column's job by adding fields to them. A trace id in your log
lines is the bridge — it is the single highest-value change you can make to an
existing logging setup, because it makes the logs you already have
request-scoped.

---

## Where You Have Already Seen It

- **OpenTelemetry** — the vendor-neutral standard for spans and propagation, and
  the thing to learn rather than any one vendor's SDK.
- **W3C Trace Context** — the `traceparent` header, which is why a Java service and
  a Python service can share a trace.
- **Jaeger** and **Zipkin** — open-source backends that collect spans and draw the
  waterfall you have just drawn by hand.
- **Micrometer Tracing** — Spring's bridge, which instruments the web layer and the
  HTTP client for you, so a Spring service is traced with configuration rather than
  code.
- **Google's Dapper paper (2010)** — the origin of all of the above, and still the
  clearest statement of why sampling is unavoidable at scale.

---

## Try It Yourself

```bash
./gradlew run     # the seven acts
./gradlew test    # 82 tests
```

Then break things on purpose:

1. In `ProductPage.load`, start the ranking model from `request` instead of
   `recommendations.context()`. Run it. The model is now a sibling of
   recommendations rather than its child, recommendations' self time jumps from 60
   to 400, and the arithmetic still adds to 900 — a plausible, wrong answer from a
   one-word change.
2. Delete the `try (...)` around the pricing span and call `tracer.start(...)`
   without closing it. Pricing vanishes from the trace entirely and the page grows
   180ms of self time.
3. Change `Sampler`'s rate to one in ten and see how many complaints are still
   unanswerable.
4. Add a sixth service — a `fraud-check` that runs inside pricing — and watch the
   percentages redistribute without touching `Waterfall` or `Trace`.

---

## See Also

- `docs/problem-statement.md` — the nine hundred milliseconds, and why the logs
  cannot help
- `docs/class-diagram.md` — the static structure, and the one dependency direction
  that matters
- `docs/uml-diagram.md` — the sequences, including both sides of the thread
  boundary
- `docs/animation.html` — the waterfall assembling itself, span by span
- `docs/session.md` — a one-hour facilitated session
