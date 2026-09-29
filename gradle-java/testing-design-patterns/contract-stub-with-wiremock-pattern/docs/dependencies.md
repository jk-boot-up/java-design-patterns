# Dependencies

This project uses WireMock, which the plain Java version of Contract Stub does
not. Skipping it loses none of the pattern: the plain version teaches all of
it with nothing installed.

## What WireMock is

WireMock is an HTTP server for tests that answers from stubs. stubFor registers a stub: here, post to a URL with a request body equal to some JSON returns a given reply. equalToJson compares bodies as JSON, not as text. A request that matches no stub gets 404, Request was not matched, with a report of the nearest stub. The standalone jar bundles its own libraries.

## What Spring Cloud Contract is

Spring Cloud Contract takes contracts, written in Groovy, YAML or Java, and generates two things: WireMock stubs for consumers, and tests that check the provider. This project does both halves by hand from one JSON file, so every step can be read.

## Why this project uses them

The plain version keeps everything in memory. This version shows the real
pieces: a stub server over HTTP, a shared file, and a verifier replaying it.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the version is pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| WireMock (standalone) | 3.13.2 |

## What it costs

- A contract file both teams must maintain.
