# Session Guide — Balking Pattern

A 60-minute session built around one question: what should a call do when the object is not ready for it?

## Learning Objectives

1. Say what balking is.
2. Show balking on a clean state and a busy state.
3. Show the edit-during-save bug and its fix.
4. Say where balking is wrong.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | The scenario and the naive version |
| 0:10–0:30 | The pattern |
| 0:30–0:45 | The bill |
| 0:45–0:52 | The verdict |
| 0:52–1:00 | Exercises |

## Walkthrough

```bash
cd concurrency-design-patterns/balking-pattern
./gradlew -q run
```

Act one: how many writes? Act two: what did the four later calls say? Act three: what was the second caller told? Act four: which draft lost the edit? Act five: what did the result enum say? Act six: what happened to the click?

## Exercises

1. Make the Save button wait for a running save instead of balking.
2. Add a result for a save that failed, and decide what the draft should do.
3. Write a stress test with many threads editing and saving, and check the last edit is always saved.

Close with the verdict: skippable work, a result that says what happened, a version and not a flag, and waiting where requests must be honoured.
