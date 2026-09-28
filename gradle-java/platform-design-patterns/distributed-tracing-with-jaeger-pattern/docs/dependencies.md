# Dependencies

This project uses OpenTelemetry, Jaeger, Jackson and Testcontainers, which the plain-Java twin does not. This page says what they are, why they are here, and what they cost. It comes before the first line of tracing code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Distributed Tracing project in this course teaches all of it, with nothing installed.

## What OpenTelemetry is

OpenTelemetry is the tracing library nearly every language and vendor has agreed on. Think of a hospital. You are given a wristband at reception, and every department you visit writes on its own form, with your wristband number and the name of the department that sent you. Nobody carries the forms around with you. At the end of each shift, every department sends its pile of forms to the records office.

In OpenTelemetry's words, each form is a **span**: one piece of work, with a name, a start, a length, and the id of the span that asked for it, its **parent**. The wristband number is the **trace id**. When a request leaves one program for another, the trace id and the caller's span id have to travel with it, as text, in an HTTP header named **traceparent**; writing it is called **injecting** and reading it **extracting**. Deciding at the front door whether this request is worth recording at all is **sampling**, and the decision travels in the header's last two characters, 01 for kept and 00 for dropped. Finished spans are not sent one by one; they are held and sent in a **batch**, every 5 seconds out of the box, over OpenTelemetry's own protocol, **OTLP**.

## What Jaeger is

Jaeger is the records office: a **collector**, a separate program that receives batches of spans from every service and joins them by trace id. The image used here holds the collector, a store, and a **query API** — the same HTTP API Jaeger's own web page uses — in one process. When two services' clocks disagree, the difference is called **clock skew**; Jaeger notices it, and out of the box only warns.

## What Jackson is

A Java library that reads JSON. Jaeger's query API answers in JSON, and Jackson turns it into objects the demo can count.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so that the demo owns Jaeger's lifetime: `./gradlew run` brings Jaeger up, uses it, and removes it at the end. It maps Jaeger's two ports — 4318, where spans are sent, and 16686, where the query API answers — to free random ports on your machine, so this demo can run beside any other Jaeger.

## Why this project uses them

Because the things this project teaches — a context that has to cross a real network as a header, a trace assembled by a separate program from separate reports, spans that arrive late or never, and clocks that disagree — cannot happen when the tracer, the services and the trace all live in one program with one scripted clock.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| Jaeger image | `jaegertracing/jaeger:2.21.0` |
| OpenTelemetry Java (api, sdk, exporter-otlp) | 1.66.0 |
| `tools.jackson.core:jackson-databind` | 3.2.3 |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back.

## What it costs

The first run pulls the Jaeger image, about 110 MB. After that a run takes about twenty seconds: the second Java program is started six times, once per act, and the third act genuinely waits for a 5-second batch. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

## Where this pattern lives in a real system

In the HTTP client and server of every service, where the header is written and read — usually by a framework or the OpenTelemetry Java agent rather than by hand; in the sampler's setting at the front door; in the batch settings, which decide how much a crash loses; in the collector's storage, which decides how long anything is kept; and in the clock synchronisation of every machine that reports.
