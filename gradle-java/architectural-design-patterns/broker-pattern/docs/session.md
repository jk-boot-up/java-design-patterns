# Session Guide — Broker Pattern

## Learning Objectives

By the end of the session you can:

- Explain location transparency.
- Register services by name and forward calls.
- Handle moved services and several instances.
- Name the costs and how real systems reduce them.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A hard-coded address | 7 min |
| 0:17 | Act 2: Calls through a broker | 7 min |
| 0:24 | Act 3: A service moves | 7 min |
| 0:31 | Act 4: Several instances | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one. Open `Broker`: `/register` stores a
name and address, `/call/{name}` looks up and forwards. Then compare act four's
alternating answers with what a client-side load balancer would do.

## Exercises

1. Remove an instance when a forwarded call to it fails.
2. Let clients ask the broker for an address once and then call the service directly. What do you gain and lose?
3. Run two brokers and make checkout try the second if the first does not answer.
