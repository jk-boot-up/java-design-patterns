# Session Guide — Content-Based Router Pattern

A 60-minute session built around one question: who should decide where a message goes?

## Learning Objectives

1. Say what a router does.
2. Show that rule order changes the answer.
3. Explain the fallback.
4. Say what the router is coupled to.

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
cd messaging-integration-patterns/content-based-router-pattern
./gradlew -q run
```

Act one: what did the warehouse need? Act two: where did each order go? Act three: which rule order gave fraud review? Act four: what happened with no fallback? Act five: which rule was added? Act six: what did 'goods' do?

## Exercises

1. Add a rule for orders over a thousand pounds to manual approval, and choose its place.
2. Route on a header instead of the body.
3. Log every message the fallback receives, and alert on the count.

Close with the verdict: rules in order on purpose, a reporting fallback, and headers over bodies.
