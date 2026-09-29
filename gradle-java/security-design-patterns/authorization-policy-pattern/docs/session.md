# Session Guide — Authorization Policy Pattern

## Learning Objectives

By the end of the session you can:

- Tell authentication from authorization.
- Explain role-based and attribute-based access control.
- Write a central policy that denies by default.
- Log each decision with its reason.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Checks in every endpoint | 7 min |
| 0:17 | Act 2: Roles only | 7 min |
| 0:24 | Act 3: Rules on attributes | 7 min |
| 0:31 | Act 4: Deny by default | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's ALLOWED with act three's DENY. Open
`Policy.shop`: seven rules, one per line. End on act four's deny by default.

## Exercises

1. Add a rule: support may not refund orders they placed themselves.
2. Allow `order:export` for admins only, during office hours.
3. Rewrite two rules in Spring Security's `@PreAuthorize` syntax.
