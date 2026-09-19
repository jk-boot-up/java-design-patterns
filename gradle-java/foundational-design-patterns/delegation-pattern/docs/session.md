# Session Guide — Delegation Pattern

A 60-minute session built around one question: why hold a helper, instead of inheriting from a parent?

## Learning Objectives

1. Show classes multiplying by feature.
2. Show one class with a swappable helper.
3. Show helpers combined.
4. Explain why the owner passes itself in.

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
cd foundational-design-patterns/delegation-pattern
./gradlew -q run
```

Act one: how many classes for two features? Act two: what did premium give? Act three: what changed on the same object? Act four: how many classes were added? Act five: what did three items cost? Act six: how many forwarding methods?

## Exercises

1. Add a shipping fee rule and combine it with premium.
2. Make the order refuse a null rule.
3. Add a rule that depends on the customer's country.

Close with the verdict: hold a helper for what varies, pass yourself in, and pay for the hop.
