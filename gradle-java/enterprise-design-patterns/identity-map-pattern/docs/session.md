# Session Guide — Identity Map Pattern

A 60-minute session built around one question: if two objects are the same customer, which one is right?

## Learning Objectives

1. Explain why two loads of one row give two objects.
2. Describe the lost-change bug, and why `equals()` does not prevent it.
3. Say what an identity map is scoped to, and why scope matters.
4. Name two costs of the map.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and two objects |
| 0:10–0:22 | The lost change |
| 0:22–0:34 | The pattern |
| 0:34–0:48 | Stale, and growing |
| 0:48–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/identity-map-pattern
./gradlew -q run
```

Act one: what does `==` say, and why? Act two: trace the two saves and say which columns each wrote. Act three: is `equals` true, and does it matter? Act four: count the operations. Act five: who is right, the session or the database? Act six: what scope would you choose for a web request?

## Exercises

1. Change `save` to write only the changed column. Does the lost change go away, and what does it cost?
2. Add `evict(id)` to the session. When would you call it?
3. Give the session a size limit. What should happen at the limit?

Close with: one row, one object, per session, and the session decides how long that is true.
