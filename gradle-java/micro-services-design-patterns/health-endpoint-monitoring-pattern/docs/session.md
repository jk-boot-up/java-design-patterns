# Session Guide — Health Endpoint Monitoring Pattern

## Learning Objectives

By the end of the session you can:

- Explain why an open port does not mean a healthy service.
- Tell liveness from readiness, and say who acts on each.
- Decide which dependencies make an instance DOWN and which make it DEGRADED.
- Explain why shared dependencies must stay out of liveness.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: An open port | 7 min |
| 0:17 | Act 2: Liveness | 7 min |
| 0:24 | Act 3: Readiness | 7 min |
| 0:31 | Act 4: A liveness check that is too deep | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: three lost orders to an instance whose
port was open. Then open `HealthEndpoint.java` and compare `live` and `ready`
line by line. Spend the most time on act four, the restart storm: it is the
mistake teams make in production, and the reason the two checks exist.

## Exercises

1. Add a startup check that answers DOWN for the first 20 seconds after a restart. Who should use it?
2. Cache the readiness answer for 5 seconds. How many dependency calls a minute now?
3. Make the public endpoint answer only UP or DOWN, and move the detail to an internal one.
4. Add a fourth dependency, the email service. Should it be critical?
