# Session Guide — Contract Stub Pattern

## Learning Objectives

By the end of the session you can:

- Explain how hand-written stubs drift.
- Write a contract as request-and-reply interactions.
- Build a stub from it, and verify a provider with it.
- Explain why a strict stub is a feature.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A stub that drifted | 7 min |
| 0:17 | Act 2: A stub made from the contract | 7 min |
| 0:24 | Act 3: The provider is checked too | 7 min |
| 0:31 | Act 4: A strict stub | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's two lines. Open `Contract.payments`,
then `ContractStub` and `ProviderVerifier`: both read the same list. End on
act three's version 2 failing.

## Exercises

1. Add a USD interaction to the contract and make both sides pass.
2. Let the contract match amounts by pattern rather than exact value.
3. Replace the maps with real HTTP and WireMock stubs.
