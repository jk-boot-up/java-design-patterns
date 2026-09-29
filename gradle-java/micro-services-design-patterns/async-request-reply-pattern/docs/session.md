# Session Guide — Asynchronous Request-Reply Pattern

## Learning Objectives

By the end of the session you can:

- Explain why slow work behind a normal request fails, even when the work succeeds.
- Name the three addresses: submit, status and result.
- Say what 202, 303 and Retry-After mean.
- Make a repeated submit safe with a request key.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Waiting for a slow report | 7 min |
| 0:17 | Act 2: Accepted at once | 7 min |
| 0:24 | Act 3: Check back, then fetch | 7 min |
| 0:31 | Act 4: Asking twice | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and start with act one: built twice, received never. Then
open `AsyncReportApi.java` and read its three methods side by side: `submit`,
`status`, `fetch`. Finish with `PollingClient`, which is the half every
learner forgets: the caller must wait as told and follow the redirect.

## Exercises

1. Add a FAILED state: if the report cannot be built, the status link should say why.
2. Make the retry hint grow: 1 s, then 2 s, then 4 s. How many requests does one report take now?
3. Delete a finished job one minute after its report is fetched. What should a late status check answer?
4. Replace polling with a callback: the client gives a URL, and the server calls it when done.
