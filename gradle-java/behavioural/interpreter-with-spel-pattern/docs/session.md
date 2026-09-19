# Session Guide — Interpreter with SpEL Pattern

A 60-minute session built around one question: what does SpEL give you as an interpreter, and what does it ask of you?

## Learning Objectives

1. Say what is parsed, and when.
2. Explain why a misspelled name is found late.
3. Explain the two evaluation contexts.

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
cd behavioural/interpreter-with-spel-pattern
./gradlew -q run
```

Act one: which lines are rules? Act two: what came free? Act three: which typo fails at build time? Act four: what could a rule reach? Act five: what did the safe operator change? Act six: how many times was the tree built?

## Exercises

1. Add a rule that uses a list of countries.
2. Try `T(java.lang.System)` in the read-only context and read the message.
3. Write a test that loads every rule against a sample order.

Close with the verdict: parse once, read-only for people's rules, test every rule.
