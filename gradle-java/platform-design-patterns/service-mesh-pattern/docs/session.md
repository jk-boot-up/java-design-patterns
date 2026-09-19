# Session Guide — Service Mesh Pattern

A 60-minute session built around one question: what should each service do for itself, and what should a proxy do for it?

## Learning Objectives

1. Show three different retry behaviours.
2. Show one policy for all.
3. Show an unknown caller refused.
4. Name three costs.

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
cd platform-design-patterns/service-mesh-pattern
./gradlew -q run
```

Act one: which services failed? Act two: how many attempts? Act three: what changed with one setting? Act four: how many calls did payments receive? Act five: how many attempts did checkout make? Act six: how many ticks did the call take?

## Exercises

1. Allow only checkout to call payments.
2. Add a timeout to the policy.
3. Set the retries so high that payments receives twenty calls, and think about what that does.

Close with the verdict: one policy for many services, small retries, and pay for the extra hop.
