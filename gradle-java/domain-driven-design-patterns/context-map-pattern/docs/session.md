# Session Guide — Context Map and Shared Kernel Pattern

## Learning Objectives

By the end of the session you can:

- Explain what a context map shows.
- Decide when two contexts should share a kernel.
- Keep a kernel small and jointly owned.
- Check the code against the map.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Two copies of an address | 7 min |
| 0:17 | Act 2: A shared kernel | 7 min |
| 0:24 | Act 3: The context map | 7 min |
| 0:31 | Act 4: The map, checked | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: the flat lost in the converter. Open the
`kernel` package: two records. Then open `ContextMap`: three relationships and
a list of allowed imports. Add the shortcut import to shipping and watch the
test fail.

## Exercises

1. Add a postcode to the kernel's Address. Which contexts must change?
2. Add a payments context that sales depends on through an anti-corruption layer, and put it on the map.
3. Make the map print itself as a list a new team member could read on day one.
