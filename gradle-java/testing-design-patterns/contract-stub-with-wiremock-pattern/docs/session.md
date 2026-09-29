# Session Guide — Contract Stub with WireMock Pattern

## Learning Objectives

By the end of the session you can:

- Build a WireMock stub from a contract file.
- Replay the same file against the real service.
- Explain why a strict stub helps.
- Describe how Spring Cloud Contract automates the flow.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A stub that drifted | 7 min |
| 0:17 | Act 2: A stub from the contract | 7 min |
| 0:24 | Act 3: The provider is checked too | 7 min |
| 0:31 | Act 4: A strict stub | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `contracts/payments.json`, then `ContractStub.fromContract`
and `ProviderVerifier`: both read the same file. End on act four's 404.

## Exercises

1. Add a USD interaction to the contract and make both sides pass.
2. Record a real service's replies with WireMock's recorder and compare.
3. Rewrite the contract as a Spring Cloud Contract YAML file.
