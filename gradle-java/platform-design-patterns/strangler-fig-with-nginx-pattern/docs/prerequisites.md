# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later. The demo starts an NGINX container and stops it again. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need NGINX are skipped and the rest still run.
- The idea of the strangler fig: the new system grows around the old one, one capability at a time, behind a router the customer never sees. The plain-Java Strangler Fig project in this course teaches it with nothing installed, but this project explains everything it uses in its own files, so it can be read on its own.

## Explicitly not required

- No prior NGINX. Every word it introduces — reverse proxy, location, prefix, regular expression, `^~`, `proxy_pass`, upstream, reload, main process and worker process, 502 — is said in plain language before the name for it is used.
- No installed NGINX, and no NGINX configuration on your machine. NGINX lives in the container for the length of the run, and its whole configuration is written by the demo.
- No web framework. The two shop services are the HTTP server built into the JDK, a few dozen lines each.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls the NGINX image; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| NGINX image | `nginx:1.31.6-alpine` |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built. None is held back. NGINX 1.31.6 is on NGINX's mainline, which NGINX recommends for most users; the separate stable line was at 1.30.5.
