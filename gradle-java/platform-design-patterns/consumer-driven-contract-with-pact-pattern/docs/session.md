# Session Guide — Consumer-Driven Contract with Pact Pattern

A 60-minute session built around one question: how does a real contract test find a break before the release?

## Learning Objectives

1. Say what a consumer's test produces.
2. Say what the provider's build does with it.
3. Read the failure message Pact gives.
4. Say what Pact cannot check.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:25 | The first acts |
| 0:25–0:40 | The failures of its own |
| 0:40–0:52 | The cost |
| 0:52–1:00 | Exercises and the verdict |

## Walkthrough

```bash
cd platform-design-patterns/consumer-driven-contract-with-pact-pattern
./gradlew -q run
```

Act one: what did the rename do in production? Act two: what did each pact list? Act three: how many interactions passed? Act four: which consumer was named? Act five: did the extra field pass? Act six: what total did checkout compute?

## Exercises

1. Add a third consumer that reads the currency.
2. Add a matcher for the range of priceCents, to catch pounds for pence.
3. Read the pact file, and change one field by hand.

Close with the verdict: consumers write, providers verify in their build, share the files, and test meaning separately.
