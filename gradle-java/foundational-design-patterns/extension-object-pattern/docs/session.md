# Session Guide — Extension Object Pattern

## Learning Objectives

By the end of the session you can:

- Recognise a class that grows a field for every feature.
- Attach roles to individual objects and look them up by type.
- Handle a missing role as "not supported".
- Explain what is lost: compile-time checks and discoverability.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One class, every field | 7 min |
| 0:17 | Act 2: A small core, with roles | 7 min |
| 0:24 | Act 3: Asking for a role | 7 min |
| 0:31 | Act 4: A new role | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and open `FatProduct`, counting the empty fields for a mug.
Then open `Product`: three fields, `with` and `extension`. Finish in
`Checkout.afterPayment`, where each role is asked for and acted on.

## Exercises

1. Add a `GiftWrap` role and make checkout print a wrapping note.
2. Write a startup check that every product in the `ebooks` category has a Download role.
3. Let a role have behaviour: give `Warranty` a method that works out its expiry date.
4. List every product that has a Warranty role.
