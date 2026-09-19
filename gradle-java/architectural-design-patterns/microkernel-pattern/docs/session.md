# Session Guide — Microkernel Pattern

A 60-minute session built around one question: what does the core need to know, and what should it not know?

## Learning Objectives

1. Show a feature added without editing the core.
2. Explain the plugin lifecycle.
3. Show a broken plugin contained.
4. Show that order changes the result.

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
cd architectural-design-patterns/microkernel-pattern
./gradlew -q run
```

Act one: was gift wrap supported? Act two: what is the total with two plugins? Act three: what is it with gift wrap? Act four: what was recorded? Act five: which order gave the lower price? Act six: what did the plugins want?

## Exercises

1. Add a plugin that rounds the total to ten cents.
2. Give each plugin a priority so order is stated, not accidental.
3. Add a country to the interface, and see what breaks.

Close with the verdict: tiny core, stable interface, ordered on purpose, failures isolated.
