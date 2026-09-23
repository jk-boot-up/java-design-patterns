# Session Guide — Splitter and Aggregator with Camel Pattern

A 60-minute session built around one question: once a real framework is doing the splitting and the gathering, who decides when the gathering is finished?

## Learning Objectives

1. Say, in plain words, what a route, a correlation identifier and a completion condition are.
2. Show an aggregator with a count and nothing else, and say why it will never emit.
3. Show a deadline firing without anybody asking, and read Camel's own reason for it.
4. Explain why completion by size counted a repeated message as progress.
5. Name the memory a thousand unfinished orders hold, and what a restart does to them.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The kitchen analogy, and the partner project recapped in two minutes |
| 0:08–0:20 | Acts one to three: the split, the stamp, the jumbled arrivals |
| 0:20–0:35 | Acts four and five: the completion condition, and the deadline |
| 0:35–0:47 | Act six: the bill, and the repeated message |
| 0:47–0:53 | The verdict |
| 0:53–1:00 | Exercises |

## Walkthrough

```bash
cd messaging-integration-patterns/splitter-aggregator-with-camel-pattern
./gradlew -q run
```

Act one: how many steps in a row, and on how many threads? Act two: what did Camel stamp on each piece, and who asked it to? Act three: what order did they answer in, and what order did the answer come out in? Act four: how many answers came out, and how many orders are open? Act five: what word did Camel use for why it finished, and who told it to stop waiting? Act six: how many orders are held, what happens to them on a restart, and why did an order finish with a line missing?

Then open `src/main/java/com/jk/explore/splitteraggregatorcamel/StoreRoutes.java` and read the three aggregators aloud. The only difference between the first and the second is two lines: a deadline, and how often the clock is looked at.

## Discussion

Ask the room what the right deadline is for a real store. There is no answer, which is the point: it is a business decision about how long a customer will wait, and the framework makes you write it down.

Then ask what should happen to the two shipments in a partial answer. Ship them and refund the rest? Hold them? Cancel? The pattern gives you the partial result; it does not tell you what it is worth.

## Exercises

1. Remove the deadline from the second aggregator and run the demo again. Watch the fifth act stop producing an answer, and find the sentence in `Results` that says so instead of hanging.
2. Move the deadline into a header, so an express order gives up sooner than a standard one.
3. Add a completion predicate: finish as soon as the total passes a threshold, whatever the count.
4. Make the fold reject a shipment whose expected count disagrees with the first one it saw for that order.
5. Replace the in-memory store of unfinished orders with one backed by a file, and say what now survives a restart.

Close with the verdict: stamp every piece, correlate on something unique, and never set a completion count without a deadline beside it.
