# Session Guide — Token Authentication Pattern

## Learning Objectives

By the end of the session you can:

- Explain why in-memory sessions break with several servers.
- Build and verify a signed token.
- Explain why tampering and expiry are caught.
- Handle early sign-out with short lifetimes and revocation.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Sessions on one server | 7 min |
| 0:17 | Act 2: A signed token | 7 min |
| 0:24 | Act 3: Forged and expired | 7 min |
| 0:31 | Act 4: Signing out early | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 401 from B with act two's 200. Open
`TokenService.issue` and `verify`: sign, then check signature, expiry and
revocation in that order. End on act four's two servers.

## Exercises

1. Move the revoked list into a shared class both servers use.
2. Add a refresh token that is checked against a store.
3. Replace the hand-built token with the jjwt or Nimbus library.
