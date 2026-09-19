# Session Guide — Anti-Corruption Layer Pattern

A 60-minute session built around one question: what does an anti-corruption layer protect, and what does it cost?

## Learning Objectives

1. Say where the old system's codes are known.
2. Show what happens when the old system adds a code.
3. Explain why bad data is refused at the layer.
4. Name what the layer costs.

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
cd domain-driven-design-patterns/anti-corruption-layer-pattern
./gradlew -q run
```

Act one: how many places knew the codes? Act two: which class translated? Act three: where did 12X stop? Act four: what did each side decide about H? Act five: which fields were dropped? Act six: what changes if the old system is replaced?

## Exercises

1. Add a status to the old system and decide what the layer should make of it.
2. Add a `lastCountedOn` date to StockLevel, and extend the layer.
3. Write a second adapter for a new inventory system.

Close with the verdict: a layer against a foreign model, one adapter, refuse bad data, list what is dropped.
