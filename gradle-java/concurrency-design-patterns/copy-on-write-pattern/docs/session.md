# Session Guide — Copy-on-Write Pattern

## Learning Objectives

By the end of the session you can:

- Explain why changing a list while iterating it fails.
- Describe copy, change, swap.
- Explain why readers need no lock.
- Decide when copying on every write is too costly.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A plain list, changed while read | 7 min |
| 0:17 | Act 2: A copy-on-write list | 7 min |
| 0:24 | Act 3: Readers never lock | 7 min |
| 0:31 | Act 4: Snapshots | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: a subscription during a notification
crashes the loop. Open `CowList`: `add` copies, `iterator` takes the array as
it is. Then show that Java's `CopyOnWriteArrayList` does the same, and end on
act five's copy count.

## Exercises

1. Replace CowList with `CopyOnWriteArrayList` and run the demo again.
2. Add `addAll` that copies once for many listeners. How many copies does act five need now?
3. Try act three with a `Collections.synchronizedList`. What happens to the readers?
