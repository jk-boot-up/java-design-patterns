# Session Guide — Claim Check with S3 Pattern

A 60-minute session built around one question: once the luggage is in real storage and the ticket on a real queue, what do the two services decide for you?

## Learning Objectives

1. Say, in plain words, what a bucket, an object, a key, a message, versioning, a delete marker and a lifecycle rule are.
2. Show a PDF genuinely refused by SQS, and work out why one under the limit is refused too.
3. Explain what a checksum on the ticket catches that the key alone does not.
4. Show that a delete in a versioned bucket leaves every version stored, and how to really remove one.
5. Compare the ticket's clock with the luggage's clock, and say which should be shorter.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The left-luggage analogy, and the pattern in two minutes |
| 0:08–0:18 | Act one: the refusal, and base64 |
| 0:18–0:26 | Act two: the ticket |
| 0:26–0:34 | Act three: luggage nobody collected |
| 0:34–0:44 | Act four: the same key, twice |
| 0:44–0:50 | Acts five and six: the clocks and the bill |
| 0:50–0:55 | The verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd micro-services-design-patterns/claim-check-with-s3-pattern
./gradlew -q run
```

Act one: what is the queue's longest message, and why is a 786433-byte PDF refused? Act two: how big is the ticket, and what is in it? Act three: of the 5 invoices left in S3, which one can never be collected, and why? Act four: why did the checksum fail, and why did versioning not free any storage? Act five: which lasts longer, the ticket or the luggage? Act six: how many requests does one invoice cost each way?

Then open `src/main/java/com/jk/explore/claimchecks3/Receiver.java` and read `redeemNext` aloud. The order of its last two lines is the pattern's safety.

## Discussion

Ask the room who should delete the object: the receiver, straight after fetching it, or a lifecycle rule, days later? The first saves money and makes a retry after a crash impossible; the second is safe and costs storage.

Then ask what should happen to a ticket whose luggage is gone. Delete it? Leave it for a person? There is no answer in either service, which is the point.

## Exercises

1. Work out the largest PDF that fits in the queue whole, then change act one to try it and one byte more.
2. Change `Receiver.redeemNext` to delete the message before the object, kill the program between the two, and say what is left.
3. In act four, make the receiver delete by key and version id, and predict every count before you run it.
4. Set the queue's retention period to one day when it is created in act five, and read it back.
5. Change `Sender.send` to send the ticket first and store second, and describe the new failure between the two steps.

Close with the verdict: random keys, a checksum on every ticket, store first and sweep what nobody claims, and the ticket's clock shorter than the luggage's.
