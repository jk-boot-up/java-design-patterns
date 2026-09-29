# Session Guide — Memoization Pattern

## Learning Objectives

By the end of the session you can:

- Spot a function that is asked the same question repeatedly.
- Memoize it with a map and `computeIfAbsent`.
- Decide whether a function is safe to memoize.
- Explain the difference between a memo and a cache.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: The same questions again | 7 min |
| 0:17 | Act 2: Memoized | 7 min |
| 0:24 | Act 3: A reusable memo | 7 min |
| 0:31 | Act 4: Not safe to memoize | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and put the two call counts side by side: nearly ten
million against 26. Then open `MultiBuy` and compare `plain` and `memoized`
line by line: the only difference is the map. Finish with act four and ask the
group for other functions that look pure but are not.

## Exercises

1. Add a "10 for £28" offer. How do the two call counts change?
2. Give `Memo` a size limit that forgets the oldest answer.
3. Fix act four by putting the date in the memo's key.
4. Memoize a function whose argument is a mutable object, change the object, and see what goes wrong.
