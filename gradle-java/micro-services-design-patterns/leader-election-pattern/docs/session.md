# Session Guide — Leader Election Pattern

A 60-minute session built around one question: how do identical copies agree that only one of them does a job?

## Learning Objectives

1. Say how a lease elects a leader.
2. Explain the takeover delay.
3. Explain how two copies can both believe they lead.
4. Say how fencing stops the old one.

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
cd micro-services-design-patterns/leader-election-pattern
./gradlew -q run
```

Act one: how many reports? Act two: who got the lease? Act three: how long was nobody leading? Act four: who sent after the pause? Act five: which token was refused? Act six: when was a healthy leader lost?

## Exercises

1. Make the leader renew at half its lease and see which pauses it survives.
2. Add a lease store that is unavailable, and decide what nodes should do.
3. Give the sink a second writer and check the fencing token still works.

Close with the verdict: leases with a time limit, renewal inside it, fencing where a stale leader could harm, and a store built for it.
