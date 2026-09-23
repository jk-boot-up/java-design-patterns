# Session Guide — Content-Based Router with Camel Pattern

A 60-minute session built around one question: when the routing is declared rather than written, what happens to a message that nothing claims?

## Learning Objectives

1. Say what a route is, without using the word route.
2. Show that the order of the questions changes the destination.
3. Say exactly what Camel does with a message no question claims, and what it does not do.
4. Tell apart a branch that does not match from a branch that fails.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The scenario, and why there is a broker on the screen |
| 0:08–0:22 | The declared route, and the first four acts |
| 0:22–0:38 | The unclaimed message, three ways |
| 0:38–0:50 | The bill: coupling, failure, and running cost |
| 0:50–1:00 | Exercises and the verdict |

## Walkthrough

```bash
cd messaging-integration-patterns/content-based-router-with-camel-pattern
./gradlew -q run
```

Act one: how many of the six could the warehouse actually ship? Act two: which order went to fraud review, and why not to standard shipping? Act three: which ordering of the questions sent the gift card to fraud review? Act four: how many messages were left anywhere in the shop when there was no otherwise branch? Act five: which question was added, and which order did it not affect? Act six: how many attempts did the broken branch get?

## The moment to slow down on

Act four, second line. Ask the room where they think the message went before revealing the number. Most people guess a dead letter queue, or an error log. The answer is that it went nowhere and nothing said so. Then ask what the hand-built version in the partner project did instead, which was to count it — and ask which of the two behaviours is more honest, and which is more common in production.

## Exercises

1. Add a question for orders from outside the United Kingdom that need a customs form, and choose where in the order it goes. Predict the effect on ORD-3 before running it.
2. Change the otherwise branch to post to a queue called `unroutable` and add a second route that reads that queue and prints what it finds. That is the beginning of a dead letter channel.
3. Take the error handler out of the broken fraud check route and run it again. Say what happened to the order, and how you would have found out in production.
4. Move one question from the body to a header the sender fills in, and say what that buys and what it costs.

Close with the verdict: order the questions on purpose and test that order, always write an otherwise branch and send it somewhere named for the problem, always configure an error handler, and prefer a header the sender set deliberately over reaching into the body.
