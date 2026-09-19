# Session Guide — Bulkhead with Resilience4j Pattern

A 60-minute session built around one question: what does Resilience4j give you for a bulkhead, and what do you still decide?

## Learning Objectives

1. Explain how one shared compartment starves checkout.
2. Say what the wall costs.
3. Choose between the two kinds.

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
cd micro-services-design-patterns/bulkhead-with-resilience4j-pattern
./gradlew -q run
```

Act one: who held every permit? Act two: which call was refused? Act three: what did the fallback say? Act four: how many permits were free in each? Act five: why were ten inside a compartment of two? Act six: what did the thread pool do with the fourth?

## Exercises

1. Size the checkout compartment to two and predict act four.
2. Give the feed a wait of one second and see what the caller feels.
3. Move the call in act five to another bean.

Close with the verdict: a compartment each, sized from real load, the right kind, never on this.
