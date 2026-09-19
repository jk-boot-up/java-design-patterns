# Session Guide — Front Controller Pattern

A 60-minute session built around one question: what does one entry point give you, and what does it cost?

## Learning Objectives

1. Say what a front controller does before a handler runs.
2. Show a check that cannot be forgotten.
3. Explain why logging is a filter.
4. Name the cost of one door.

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
cd enterprise-design-patterns/front-controller-pattern
./gradlew -q run
```

Act one: which handler had no check? Act two: where is the check written? Act three: which table answers 404? Act four: which requests are logged? Act five: what did the customer not see? Act six: what did one bad filter do?

## Exercises

1. Add a rate limit filter and decide where it runs.
2. Add a route for a new page and check nothing else changes.
3. Write a test that fails if a private route is reachable without a token.

Close with the verdict: one door for shared work, small filters, and a test on every private route.
