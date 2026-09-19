# Session Guide — Active Object Pattern

A 60-minute session built around one question: if callers never wait, who
does the work, and what does that cost?

## Learning Objectives

1. Say what four earlier ideas the pattern is assembled from.
2. Explain why the pattern needs no lock.
3. Say where an error in a message surfaces, and why the stack trace surprises.
4. Explain why one worker caps throughput however many callers there are.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the blocked caller |
| 0:10–0:22 | The pattern |
| 0:22–0:32 | No lock at all |
| 0:32–0:44 | The mailbox, and errors |
| 0:44–0:54 | The ceiling |
| 0:54–1:00 | Exercises |

## Walkthrough

```bash
cd concurrency-design-patterns/active-object-pattern
./gradlew -q run
```

Act one: which thread state does the checkout thread show, and why?
Act two: open `InventoryActiveObject` and find the four ideas from the
earlier projects. Act three: find the lock. Act four: what would you do to
stop the mailbox growing? Act five: why does the trace not name the caller?
Act six: what would you change to raise the ceiling?

## Exercises

1. Give the mailbox a bound with `ArrayBlockingQueue` and decide what
   `send` should do when it is full.
2. Attach the caller's own stack trace to each message, so a failure can
   name who sent it.
3. Run two active objects and have them message each other. What can go wrong?

Close with: an active object trades a lock for a queue, and the queue has to
be watched.
