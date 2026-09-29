# Session Guide — Secrets Manager with OpenBao Pattern

## Learning Objectives

By the end of the session you can:

- Store a secret in OpenBao's KV v2 engine.
- Write a policy and issue tokens that carry it.
- Rotate a secret by writing a new version.
- Revoke a leaked token.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A key in the code | 7 min |
| 0:17 | Act 2: Policies and tokens | 7 min |
| 0:24 | Act 3: Versions and rotation | 7 min |
| 0:31 | Act 4: Revoke a leaked token | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Compare act two's 200 and 403. Open
`Secrets`: every method is one HTTP call. End on act four's revoked token.

## Exercises

1. Enable AppRole auth and log in with a role instead of a root-issued token.
2. Give tokens a 10-second lifetime and watch one expire.
3. Replace the HTTP calls with Spring Cloud Vault pointed at OpenBao.
