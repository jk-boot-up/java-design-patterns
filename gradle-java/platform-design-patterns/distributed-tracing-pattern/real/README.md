# Tier 2 — the same pattern, with Spring Boot, OpenTelemetry and Jaeger

Tier 1, one directory up, is plain Java with no framework, no network and no
clock you do not control. It is the lesson. This directory is the same pattern
as a real deployment writes it: two Spring Boot services, a real tracing
backend, and a waterfall that nobody in this repository drew.

**Read Tier 1 first.** Nothing here re-explains what a span is, why a parent id
is the whole pattern, or why a waterfall is a property of the data rather than a
picture. This directory answers a narrower question: what does the pattern look
like when a framework already implements all of it, and — more usefully —
*which part can still be wrong when it does?*

Everything below is captured output from `./demo.sh`. Nothing in this file is
written from memory.

## Run it

```
./demo.sh
```

A JDK 21, Docker, and a network connection the first time, so Gradle can fetch
Spring and Docker can pull Jaeger. The script starts Jaeger, starts both
services, walks the whole sequence, and stops everything again. It takes about
two minutes, most of which is the two five-second waits for spans to be
exported.

Tier 1 needs none of it. That asymmetry is why the two are separate Gradle
builds: `real/settings.gradle` is a build of its own and the parent does not
include it, so `../gradlew test` never tries to resolve Spring and passes with
the network unplugged.

## The two services

| Service | Port | What it is |
| --- | --- | --- |
| `product-page` | 8080 | Tier 1's `ProductPage`. Calls catalog and pricing in-process, then calls recommendations over HTTP |
| `recommendations` | 8081 | The downstream service. Runs a ranking model that is the slowest thing in the request |
| Jaeger | 16686 | The backend. Accepts OTLP directly on 4318, so there is no separate collector process |

The delays are the same ones Tier 1 used, so the shape is comparable: catalog
120ms, pricing 180ms, the ranking model 340ms, and 60ms of the downstream
service's own work around it.

## One page load, with the context forwarded

```json
{
    "sku": "SKU-4417",
    "propagated": true,
    "pageTraceId": "a05c5c929cc9639094af1e80905588ba",
    "recommendationsTraceId": "a05c5c929cc9639094af1e80905588ba",
    "traceparentSeenDownstream": "00-a05c5c929cc9639094af1e80905588ba-0daa3b625a20bbea-03",
    "sameTrace": true,
    "recommended": ["SKU-4417", "SKU-9002", "SKU-1183"]
}
```

Two processes agree on a trace id that neither of them chose and neither of them
sent. There is no line in either service that writes a `traceparent` header and
no line that reads one. The instrumentation is on the `RestClient` builder at
one end and on the servlet at the other.

That header is worth reading field by field, because it is the entire wire
protocol: `00` is the version, the long hex string is the trace id, the short
one is the id of the span that will be the *parent* of whatever the downstream
service opens, and `03` is the flags byte — bit one set, meaning sampled. The
sampling decision travels with the request. The downstream service does not get
a second vote, which is why one service quietly configured at 0.1 cannot punch
holes in a trace that was already accepted at the front door.

## What Jaeger holds for that trace

This is the only check in the demo that the services cannot fake. The ids above
are the services' own account of themselves; this comes from a separate process
that saw only what arrived on the wire.

```
  spans:    6
  services: product-page, recommendations
  roots:    1
    http get /page                                  813ms   [product-page]
      catalog                                       126ms   [product-page]
      pricing                                       184ms   [product-page]
      http get                                      484ms   [product-page]
        http get /recommendations                   430ms   [recommendations]
          ranking-model                             352ms   [recommendations]
```

Six spans, two processes, one root. The indentation is the parent reference and
nothing else — the same rule Tier 1's `Waterfall` applied with string
concatenation, applied here to data that crossed a network, and drawn by
`demo.sh` from Jaeger's own API rather than taken as a screenshot of the UI.

Two details in that tree are the whole argument for a real backend. The
client-side span, `http get` at 484ms, is not the same span as the server-side
`http get /recommendations` at 430ms; the gap between them is the network and
the queueing, and it exists only because both ends were instrumented. And
`ranking-model` at 352ms is nested under a span belonging to a *different
process*, which is a sentence that only means anything once the parent id has
crossed a wire.

## The same page, through `RestClient.create()`

```json
{
    "sku": "SKU-4417",
    "propagated": false,
    "pageTraceId": "2401370e6d1fe5037750acf7677f2f4a",
    "recommendationsTraceId": "bfa6b40061bb480ef1671174a5280388",
    "traceparentSeenDownstream": "none — the caller sent no traceparent header",
    "sameTrace": false,
    "recommended": ["SKU-4417", "SKU-9002", "SKU-1183"]
}
```

Same URL, same response, same three recommendations, same latency. One line
different, in `RecommendationsClients`:

```java
@Bean RestClient propagatingClient(RestClient.Builder builder) {
    return builder.baseUrl("http://localhost:8081").build();
}

@Bean RestClient nonPropagatingClient() {
    return RestClient.create("http://localhost:8081");
}
```

The injected builder arrives pre-loaded with the observation instrumentation
that reads the current span and writes the header. The static factory is a plain
constructor that owes Spring nothing and gets nothing. Both compile, both pass
their tests, and one is an autocomplete away from the other.

```
  spans:    3
  services: product-page
  roots:    1
    http get /page                                  768ms   [product-page]
      catalog                                       127ms   [product-page]
      pricing                                       191ms   [product-page]
```

This is Tier 1's third lie, in a real system. The page still takes 768ms. The
three spans account for about 320ms of it. The remaining 440ms is in the tree as
nothing at all — not an error, not a gap, not a warning. The ranking model's
time is not missing from the world; it is in a second trace under a root of its
own, and nothing anywhere says the two belong to the same customer.

## Everything Jaeger holds, by service

```
  product-page:
  3 trace(s):
    e5e21263a51851b93d25a3ec91075793  starts at http get /actuator/health    1 span(s) across product-page
    a05c5c929cc9639094af1e80905588ba  starts at http get /page               6 span(s) across product-page, recommendations
    2401370e6d1fe5037750acf7677f2f4a  starts at http get /page               3 span(s) across product-page
  recommendations:
  3 trace(s):
    53d91777be0bf9625ad4a1483b3499e2  starts at http get /actuator/health    1 span(s) across recommendations
    a05c5c929cc9639094af1e80905588ba  starts at http get /page               6 span(s) across product-page, recommendations
    bfa6b40061bb480ef1671174a5280388  starts at http get /recommendations    2 span(s) across recommendations
```

Read that by what each trace *starts with*, not by how many there are. One
starts at the page and reaches the ranking model. One starts at the page and
stops inside it. One starts at `/recommendations`, which is not where any
customer started — that is the orphan, and from the inside it looks like a
perfectly healthy two-span trace of a service doing its job in 430ms.

The single-span traces starting at `/actuator/health` are the script's own
readiness polling, and they are left in the output rather than filtered out
because they make a point Tier 1 argued in the abstract: a sampler at 1.0 traces
everything that arrives, including the traffic nobody meant to measure.

## What the framework replaced, and what it did not

Tier 1 built nine classes. Here is where each one went.

| Tier 1 | Here |
| --- | --- |
| `TraceContext`, `Span`, `Tracer` | OpenTelemetry's SDK, via `spring-boot-starter-opentelemetry` |
| The `parentSpanId` field | The `traceparent` header, W3C Trace Context |
| `Tracer.Scope`, and closing it | `Observation.observe(...)`, which closes it in a `finally` you do not write |
| `Waterfall` | Jaeger's UI — and, in this demo, thirty lines of Python in `demo.sh` reading Jaeger's API, because a picture you can regenerate beats a screenshot |
| `Sampler` | `management.tracing.sampling.probability`, default 0.1 |
| `InterleavedLog`, the rejected design | Nothing. It was never a thing you build; it is a thing you stop doing |
| `AsyncHandoff`, the thread failure | Mostly handled, by context propagation on Spring's executors — **and not fully**, see below |
| `Clock.Scripted` | Gone, and that is a real loss: these timings vary run to run, which is exactly why Tier 1's numbers are the ones the videos quote |

The pattern's three failure modes survive the framework, in different states.
The unclosed span is genuinely gone, because `observe` owns the lifetime. The
lost thread is mostly gone, as long as the work runs on something Spring
instrumented. The broken hop — the third, and the one everybody assumes a
framework has solved — is one bean definition away in a file that compiles, and
the demo above is what it produces.

## What is not here

- **A collector.** The services export straight to Jaeger on 4318. A deployment
  of any size puts an OpenTelemetry Collector in between, precisely so the
  endpoint can stay pointed at localhost while the backend behind it changes.
- **Persistence.** Jaeger is running with in-memory storage. Stop the container
  and every trace in this README is gone.
- **Authentication, TLS, and head-based sampling policy.** All three are
  deployment concerns with nothing to say about the pattern.
- **Tier 1's determinism.** Every duration here is measured, so no two runs
  agree to the millisecond. Quote Tier 1's numbers, not these.

Each is left out because it would cost a reader time without teaching the
pattern, not because a real deployment can do without it.

## Two traps Spring Boot 4 sets for anyone arriving from Boot 3

Both cost this project a wasted demo run, and both are recorded in the build
files rather than only here.

**Tracing is one starter now, not two dependencies.** Under Boot 3,
`micrometer-tracing-bridge-otel` plus `opentelemetry-exporter-otlp` was the
recipe, and it worked because the whole of the auto-configuration lived inside
the actuator. Boot 4 split observability into modules. Those same two
dependencies still resolve and still compile, and the context dies at startup
with *"required a bean of type `io.micrometer.tracing.Tracer`"* — the library is
on the classpath and the auto-configuration for it is not. The answer is the
single starter `spring-boot-starter-opentelemetry`.

**`spring-boot-starter-web` no longer brings an HTTP client.** The same split
separates the client side from the server side, so a service that calls another
service needs `spring-boot-starter-restclient` by name or it fails with
*"required a bean of type `org.springframework.web.client.RestClient$Builder`"*.

Two smaller ones, for completeness. The OTLP endpoint property moved to
`management.opentelemetry.tracing.export.otlp.endpoint`, with Boot 3's
`management.otlp.tracing.endpoint` kept as a deprecated alias. And the same
starter exports *metrics* on its own timer to `/v1/metrics`, which Jaeger does
not serve — so both services set `management.otlp.metrics.export.enabled: false`
to stop a 404 stack trace once a minute that reads exactly like a tracing
failure and is not one.

## Versions

Everything is pinned in
[`../../gradle/libs.versions.toml`](../../gradle/libs.versions.toml) and
explained in [`../../docs/pinned-versions.md`](../../docs/pinned-versions.md).
Spring Boot 4.1.1, OpenTelemetry SDK 1.62.0, `jaegertracing/jaeger:2.20.0`. No
ranges, no `latest`.
