# Session Guide — Consumer-Driven Contract Pattern

A 60-minute session built around one question: how can a provider change safely when it does not know who uses it?

## Learning Objectives

1. Show a break found in production.
2. Show contracts as data.
3. Show a break named before release.
4. Show what a contract cannot catch.

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
cd platform-design-patterns/consumer-driven-contract-pattern
./gradlew -q run
```

Act one: what did the order return? Act two: what does reports read? Act three: how many problems for the current release? Act four: what was named? Act five: which consumer was unaffected? Act six: what total did checkout compute?

## Exercises

1. Add a third consumer that reads the currency.
2. Add a check for a value range, to catch pounds for pence.
3. Make the verifier read contracts from a folder.

Close with the verdict: consumers say what they use, providers check before release, and meaning still needs tests.
