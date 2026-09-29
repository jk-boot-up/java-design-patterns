# Session Guide — Gateway Offloading Pattern

## Learning Objectives

By the end of the session you can:

- Spot duplicated cross-cutting code across services.
- Move sign-in checks, rate limiting and compression into a gateway.
- Pass the checked identity on to the services.
- Explain why services must not be reachable around the gateway.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Every service checks for itself | 7 min |
| 0:17 | Act 2: One check, at the gateway | 7 min |
| 0:24 | Act 3: Rate limiting | 7 min |
| 0:31 | Act 4: Compression | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 200 from orders with act two's 401.
Open `Gateway.handle`: four numbered steps. Then open `ShopService`: no
sign-in code at all. End on act five's side door.

## Exercises

1. Add request logging to the gateway: one line per request, with the customer and status.
2. Make the services refuse calls without a secret header only the gateway adds.
3. Cache catalog responses at the gateway for five seconds.
