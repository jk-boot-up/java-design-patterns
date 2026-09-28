# Session Guide — Event Sourcing with EventStoreDB Pattern

A 60-minute session built around one question: once two programs can write to the same history, what stops them both spending the same points?

## Learning Objectives

1. Say, in plain words, what a stream, a revision, an append and an expected revision are, and what the rename from EventStoreDB to KurrentDB changes.
2. Reproduce two checkouts spending the same points with no check, and explain why the server accepted both.
3. Show the expected revision refusing the second append, and explain why the refused writer must read again rather than resend.
4. Explain how an event id lets the server recognise a retry.
5. Name the bill: a delete that hides, projections that must forget too, the check being off by default, and a server that ran insecure.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The post office ledgers, the rename, and the twin recapped in two minutes |
| 0:08–0:15 | Act one: a real log, read back |
| 0:15–0:30 | Acts two and three: the race, with and without the check |
| 0:30–0:38 | Act four: the retry |
| 0:38–0:46 | Act five: the catch-up subscription |
| 0:46–0:55 | Act six: the delete, and the verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd platform-design-patterns/event-sourcing-with-eventstoredb-pattern
./gradlew -q run
```

Questions to ask as you go through the output:

- **Act one:** where is 140 stored?
- **Act two:** at what moment did the second checkout's decision become wrong, and could it have known?
- **Act three:** which checkout won? The output does not say. Why not?
- **Act four:** why did the same id need the same expectation too?
- **Act five:** what would the dashboard show if it had started first?
- **Act six:** after the delete, where does C-5122's history still exist?

Then open `src/main/java/com/jk/explore/eventsourcingeventstoredb/LoyaltyLog.java` and read `append` and `appendExpecting` aloud. The only difference is one `StreamState`.

## Discussion

Ask the room how many places in a real shop append to a customer's points. The candidates include the website, the app, the till, the refund job and the expiry job. Every one of them has to carry the revision it read.

Then ask what the refused checkout should do if the second look still shows enough points. It should try again with the new revision. How many times? What does the customer see meanwhile?

## Exercises

1. Change act two to use `Check.EXPECTED_REVISION` and predict every line of its output before you run it.
2. In the race, make the refused checkout retry with the *same* expected revision and the same event id. What does the server answer, and why?
3. Replace `delete` with `tombstoneStream` in act six and predict what the later append does.
4. Give the dashboard a checkpoint, the last position it saw. Restart it from there instead of from the start, and count the events it receives.
5. Add a third checkout to the race and predict the counts of accepted and refused appends.

Close with the verdict: look, decide and append with the revision you looked at; on a refusal, look again; one event id per decision; erasure reaches every copy.
