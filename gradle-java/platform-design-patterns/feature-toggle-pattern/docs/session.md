# Session Guide — Feature Toggle Pattern

A 60-minute session built around one question: how can you release a feature to a few customers and take it back at once?

## Learning Objectives

1. Show why deploy and release differ.
2. Show a switch turned on for some.
3. Show a kill switch.
4. Explain the safe default and stale toggles.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | The scenario and the naive version |
| 0:10–0:30 | The pattern |
| 0:30–0:45 | The bill |
| 0:45–0:52 | The verdict |
| 0:52–1:00 | Exercises |

## Walkthrough

```bash
cd platform-design-patterns/feature-toggle-pattern
./gradlew -q run
```

Act one: how many deploys? Act two: what did the order cost after the switch? Act three: how many got it at ten percent? Act four: how many failed after the switch was off? Act five: what did the order cost with the table down? Act six: how many combinations?

## Exercises

1. Add a rule for customers with an even number.
2. Add a toggle age check that fails the build for stale toggles.
3. Make the table down mean on, and think about what breaks.

Close with the verdict: ship off, roll out slowly, keep a kill switch, default safe, and remove old toggles.
