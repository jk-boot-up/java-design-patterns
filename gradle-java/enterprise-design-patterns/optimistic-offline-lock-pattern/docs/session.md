# Session Guide — Optimistic Offline Lock Pattern

A 60-minute session built around one question: what does it cost to assume nobody will clash?

## Learning Objectives

1. Say how a version detects a stale save.
2. Show a retry keeping both changes.
3. Name the three costs.
4. Say when to lock instead.

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
cd enterprise-design-patterns/optimistic-offline-lock-pattern
./gradlew -q run
```

Act one: whose change vanished? Act two: which version did the second save carry? Act three: how many attempts did clerk B need? Act four: which conflict was not one? Act five: how many saves for ten writers? Act six: what was discarded?

## Exercises

1. Change the store so the version is per field.
2. Add a merge function that combines changes to different fields.
3. Make the retry give up after three attempts, and decide what to tell the user.

Close with the verdict: optimistic where clashes are rare and edits short, pessimistic where they are costly.
