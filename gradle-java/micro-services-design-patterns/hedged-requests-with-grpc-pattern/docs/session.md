# Session Guide — Hedged Requests with gRPC Pattern

## Learning Objectives

By the end of the session you can:

- Configure a gRPC hedging policy in a service config.
- Choose a hedging delay.
- Show the server seeing a cancelled attempt.
- Scope hedging to methods that are safe to repeat.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A slow tail | 7 min |
| 0:17 | Act 2: A hedging policy | 7 min |
| 0:24 | Act 3: The loser is cancelled | 7 min |
| 0:31 | Act 4: Hedge at once | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Compare act one's 3 slow lookups with act two's 0. Open
`Channels.hedged`: the whole feature is a map. End on act five's two orders.

## Exercises

1. Add a `retryThrottling` section and make the server slow for every call.
2. Scope the policy to the Price method only, by method name.
3. Try a hedging delay of 0.5 s and count slow lookups.
