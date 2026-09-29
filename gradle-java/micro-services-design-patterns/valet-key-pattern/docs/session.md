# Session Guide — Valet Key Pattern

## Learning Objectives

By the end of the session you can:

- Explain why big uploads should not pass through app servers.
- Sign a narrow, short-lived permission.
- Check a key's signature, method, path, size and expiry.
- Name the risks of bearer keys.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Carried by the app | 7 min |
| 0:17 | Act 2: A valet key | 7 min |
| 0:24 | Act 3: Only what it allows | 7 min |
| 0:31 | Act 4: Expiry | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 40 MB with act two's key. Open
`Signer.sign` (what is signed) and `Storage.handle` (what is checked). End on
act five: how short should a key live?

## Exercises

1. Add a download key for GET, valid for one minute.
2. Allow a key to be used only once by remembering signatures already used.
3. Put the customer's user ID into the signed text, and check it at storage.
