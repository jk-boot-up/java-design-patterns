# Session Guide — MVP and MVVM Pattern

A 60-minute session built around one question: where should the rules of a screen live, and how does the screen learn of them?

## Learning Objectives

1. Show why rules inside a screen are hard to check.
2. Show a presenter and a passive view.
3. Show binding to a view model.
4. Say what each approach costs.

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
cd architectural-design-patterns/mvp-and-mvvm-pattern
./gradlew -q run
```

Act one: how many windows opened? Act two: what was the view told? Act three: who decided checkout was off? Act four: who told the screen? Act five: what did the watch show? Act six: what did the forgetful screen draw?

## Exercises

1. Add a warning when the total is over five hundred pounds, in the presenter.
2. Add the same warning in the view model.
3. Add a check that every observable of the view model is bound.

Close with the verdict: rules out of the screen, test without one, and check the wiring.
