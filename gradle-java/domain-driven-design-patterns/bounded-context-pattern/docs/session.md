# Session Guide — Bounded Context Pattern

A 60-minute session built around one question: why does one word need more than one model, and how do the models stay linked?

## Learning Objectives

1. Show that one word can have three correct meanings.
2. Say what the contexts share.
3. Explain how a rename travels between contexts.
4. Name the bill.

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
cd domain-driven-design-patterns/bounded-context-pattern
./gradlew -q run
```

Act one: how many fields, and who depends on them? Act two: which answers differ? Act three: what do the models share? Act four: when did Shipping change its name? Act five: which check found zero? Act six: what is stored more than once?

## Exercises

1. Add a support context that reacts to the rename event.
2. Add a field to Recipient and check nothing else changes.
3. Draw the context map: who is upstream of whom.

Close with the verdict: a boundary where a word changes meaning, separate models, events and ids between them.
