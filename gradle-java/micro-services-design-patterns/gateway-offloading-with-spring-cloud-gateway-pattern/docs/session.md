# Session Guide — Gateway Offloading with Spring Cloud Gateway Pattern

## Learning Objectives

By the end of the session you can:

- Define gateway routes to real services.
- Write a global filter that checks, limits and passes on the customer.
- Switch on response compression by configuration.
- Explain why services must not be reachable around the gateway.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Every service checks for itself | 7 min |
| 0:17 | Act 2: One check at the gateway | 7 min |
| 0:24 | Act 3: Rate limiting | 7 min |
| 0:31 | Act 4: Compression | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `SignInFilter.filter`: check, limit, strip, add.
Open `GatewayApp.routes`: three lines. End on act five's side door.

## Exercises

1. Replace the in-memory limiter with RequestRateLimiter and Redis.
2. Add a route filter that adds a request identifier header for tracing.
3. Make the services refuse calls without a secret header only the gateway adds.
