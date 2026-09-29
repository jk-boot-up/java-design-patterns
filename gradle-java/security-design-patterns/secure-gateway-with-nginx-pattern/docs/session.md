# Session Guide — Secure Gateway with NGINX Pattern

## Learning Objectives

By the end of the session you can:

- Write an NGINX allow-list with location blocks.
- Strip a header with proxy_set_header.
- Limit methods and body size.
- Explain why path normalisation defeats the dot-dot trick.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: The service faces the internet | 7 min |
| 0:17 | Act 2: An NGINX gatekeeper | 7 min |
| 0:24 | Act 3: An allow-list of locations | 7 min |
| 0:31 | Act 4: Size and shape | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Open `Gatekeeper.config`: the whole
policy is about twenty lines. Compare act one's two exports with acts two and
three.

## Exercises

1. Add a location for GET /orders/<number>/invoice.
2. Add limit_req to rate-limit each client address.
3. Make the order service reject paths containing dot-dot itself, as a second layer.
