# Session Guide — Claim Check Pattern

A 60-minute session built around one question: how do you send something too big for the broker?

## Learning Objectives

1. Say what the claim contains and why.
2. Show the bytes the broker no longer carries.
3. Show what happens to uncollected luggage.
4. Say why the claim must be unguessable.

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
cd micro-services-design-patterns/claim-check-pattern
./gradlew -q run
```

Act one: what limit was passed? Act two: what is in the claim? Act three: how many bytes with and without? Act four: how many blobs were left, and what did the sweep do? Act five: what caught the changed byte? Act six: which claims could be guessed?

## Exercises

1. Make the sender delete the blob if publishing the claim fails.
2. Add a signed, time-limited claim, so it cannot be used after an hour.
3. Let the receiver ask for only the first 100 bytes.

Close with the verdict: a ticket that is unguessable and checked, luggage with a life span, and a sweep.
