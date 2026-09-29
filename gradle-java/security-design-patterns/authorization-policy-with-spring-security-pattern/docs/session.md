# Session Guide — Authorization Policy with Spring Security Pattern

## Learning Objectives

By the end of the session you can:

- Write URL rules ending in denyAll().
- Write @PreAuthorize rules over ownership and amounts.
- Call a policy bean from a rule.
- Publish and count authorization events.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Signed in is enough | 7 min |
| 0:17 | Act 2: Roles only | 7 min |
| 0:24 | Act 3: Rules beside each endpoint | 7 min |
| 0:31 | Act 4: Deny by default | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `ShopApp.security`: the URL rules. Open
`OrderController`: each rule beside its endpoint. Compare act two's 200 with
act three's 403.

## Exercises

1. Stop support staff refunding orders they placed themselves.
2. Allow export for admins only, and see act four change.
3. Remove the error-dispatch rule and count the refusal events again.
