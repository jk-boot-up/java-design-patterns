# Session Guide — Gateway Pattern

A 60-minute session built around one question: what does a gateway keep out of the shop, and what does it leave out?

## Learning Objectives

1. Say what only the gateway knows.
2. Show a test that makes no network call.
3. Show a retry rule in one place.
4. Name what the common interface leaves out.

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
cd enterprise-design-patterns/gateway-pattern
./gradlew -q run
```

Act one: who forgot the currency? Act two: what does checkout not contain? Act three: how many network calls in the fake test? Act four: how many calls for one timeout? Act five: what changed to swap providers? Act six: how many places for partial capture?

## Exercises

1. Add a refund method to the gateway and count the classes that change.
2. Make the fake fail the third call, and test that checkout copes.
3. Add a logging decorator around any gateway.

Close with the verdict: a small gateway in the program's own words, the vendor's habits inside it, and a fake for tests.
