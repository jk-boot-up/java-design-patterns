# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later. The demo starts a Jaeger container and removes it again. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need Jaeger are skipped and the rest still run.
- The idea of distributed tracing: one id for one customer request, and a span for every piece of work that names the span that asked for it. The plain-Java Distributed Tracing project in this course teaches it with nothing installed, but this project explains everything it uses in its own files, so it can be read on its own.

## Explicitly not required

- No prior OpenTelemetry or Jaeger. Every word they introduce — span, trace id, parent, the traceparent header, sampling and its flag, batch export, collector, OTLP, clock skew — is said in plain language before the name for it is used.
- No installed Jaeger and no configuration on your machine. Jaeger lives in the container for the length of the run.
- No web framework. Both services are the HTTP server that ships with Java.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls the Jaeger image; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| Jaeger image | `jaegertracing/jaeger:2.21.0` |
| `io.opentelemetry:opentelemetry-bom` (api, sdk, exporter-otlp) | 1.66.0 |
| `tools.jackson.core:jackson-databind` | 3.2.3 |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built. None is held back.
