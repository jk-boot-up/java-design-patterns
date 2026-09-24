# Session Guide — Queue-Based Load Leveling with SQS Pattern

A 60-minute session built around one question: once the line is on a real queue service, what does that service decide for you?

## Learning Objectives

1. Say, in plain words, what waiting, in flight, a receipt, the visibility timeout, changing visibility, long polling and retention are.
2. Read a queue's depth from SQS during a burst, and explain the 10-per-request ceiling.
3. Show a taken order handed out a second time, and say why SQS did it.
4. Explain how a slow consumer packs an order twice, and the two ways to stop the harm.
5. Compare an in-memory queue whose process stops with an SQS queue whose consumer stops.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The post-office analogy, and the pattern in two minutes |
| 0:08–0:16 | Act one: the burst and its depth |
| 0:16–0:24 | Act two: the packer's pace, and in flight |
| 0:24–0:34 | Act three: taken is not removed |
| 0:34–0:44 | Act four: the slow packer |
| 0:44–0:50 | Acts five and six: the stopped packer and the bill |
| 0:50–0:55 | The verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd micro-services-design-patterns/queue-based-load-leveling-with-sqs-pattern
./gradlew -q run
```

Act one: how many requests did the burst of 100 take, and why? Act two: for a moment SQS reported 90 waiting and 10 in flight; where were the 10? Act three: why was the second packer given 0 orders, and what changed 2 seconds later? Act four: who is to blame for the two parcels — packer A, packer B, or the timeout? Act five: why were 0 orders lost when the plain-Java project lost 70? Act six: what would you need to build to get the limit of 50 that SQS refused?

Then open `src/main/java/com/jk/explore/loadlevelingsqs/Packer.java` and read `round` aloud. The delete comes after the packing, and that order is the pattern's safety.

## Discussion

Ask the room how long the visibility timeout should be. Too short, and a slow packer's order is packed twice. Too long, and an order held by a packer that died waits that long before anyone else may touch it.

Then ask what "packing twice must do no harm" means for a real warehouse. A table of order ids already packed? A check with the carrier before printing a label? There is no answer in SQS, which is the point.

## Exercises

1. Change act two's packer to ask for 5 at a time, and predict the depth after each round before you run it.
2. In act four, give the queue a 10-second timeout instead of 2, and say what packer B is given.
3. Make the `Warehouse` refuse to pack an order it has already packed, and run act four again.
4. In act five, stop the packer after it finishes 0 of its 10, and predict every count.
5. In act six, write a producer that asks SQS for the depth before each send and refuses orders once 50 are waiting, and count the extra requests it costs.

Close with the verdict: 10 at a time, a timeout longer than the slowest work, delete last, harmless twice, and watch the depth yourself.
