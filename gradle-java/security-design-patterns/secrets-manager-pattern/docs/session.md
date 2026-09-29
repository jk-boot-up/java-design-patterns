# Session Guide — Secrets Manager Pattern

## Learning Objectives

By the end of the session you can:

- Explain the risks of secrets in code.
- Grant secrets per service and audit reads.
- Rotate a secret with caching and a grace period.
- Respond to a leak without a redeploy.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A key in the code | 7 min |
| 0:17 | Act 2: A key in the manager | 7 min |
| 0:24 | Act 3: Rotation without a rebuild | 7 min |
| 0:31 | Act 4: A leak | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and follow act three's minutes 2, 5 and 10. Open
`CachedSecret`: a value, a time, and `refresh`. End on act four's refetch.

## Exercises

1. Make `SecretsManager.read` fail while the manager is down, and have `CachedSecret` keep its last value.
2. Store the database password too, granted to one service only.
3. Replace `SecretsManager` with Spring Cloud Vault against a local Vault.
