# Session Guide — Modular Monolith Pattern

## Learning Objectives

By the end of the session you can:

- Say what a monolith is, and what makes one modular.
- Put a module's data and rules behind a front door.
- Check module boundaries automatically.
- Explain how a modular monolith prepares a module to become a service.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Every table open | 7 min |
| 0:17 | Act 2: Modules with front doors | 7 min |
| 0:24 | Act 3: Boundaries checked | 7 min |
| 0:31 | Act 4: Moving a module out | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and start with act one: stock at -1. Then look at the
package tree: `catalog`, `orders`, `payments`, each with a public interface and
an `internal` package. Open `OrdersModule` and show that it only ever sees two
interfaces. Finish with `BoundaryCheck` and the test that runs it over the real
source.

## Exercises

1. Add a `shipping` module with its own front door. Which module should call it?
2. Make the boundary check also refuse imports of `mud` from any module.
3. Give payments an event, "payment taken", that orders listens to, instead of a direct call.
4. Write `module-info.java` files that make Java itself enforce the walls.
