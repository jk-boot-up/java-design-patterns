# Session Guide — Secure Gateway Pattern

## Learning Objectives

By the end of the session you can:

- Explain why trusted services should not face the internet.
- Write an allow-list of request shapes.
- Strip internal headers at the boundary.
- Keep secrets off the internet-facing machine.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: The service faces the internet | 7 min |
| 0:17 | Act 2: A gatekeeper in front | 7 min |
| 0:24 | Act 3: An allow-list | 7 min |
| 0:31 | Act 4: Size and shape limits | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's two exports with acts two and
three. Open `Gatekeeper.handle`: size, path, method, strip, forward. End on
act five's `false`.

## Exercises

1. Add `GET /orders/<number>/invoice` to the allow-list.
2. Rate-limit refused requests per caller.
3. Make `OrderService` reject paths containing `..` itself, as a second layer.
