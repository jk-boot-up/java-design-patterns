# Retry with Resilience4j Pattern — Video Narration Script

## 1. Retry with Resilience4j

Hello, and welcome. This video explains the Retry with Backoff pattern with Resilience4j, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Retry with Backoff video. That one retried a flaky payment gateway with a growing wait between attempts, and showed why a retry is safe only when the failure is temporary and doing the operation twice cannot do it twice. This one shows the same idea inside Resilience4j. The plain definition, in short: in Resilience4j, a retry is an annotation on a method, and the attempts and the waits are configuration. By the end you will see the retry as an annotation and four settings, then see the three ways it goes wrong: retrying what should not be retried, charging twice, and retries that multiply.

## 2. The Partner Project

This video assumes the Retry with Backoff video. If you have not seen it, start there. It retries a flaky payment gateway, waiting longer each time, and shows that a retry is safe only when the failure is temporary and doing the operation twice cannot do it twice. This one uses the same example. It does not teach the pattern again. It shows what Resilience4j does with it.

## 3. Before The First Line

Before the first line of code, what Resilience4j is. Resilience4j is a library of resilience patterns for Java. It contains a retry with configurable waits and exception lists, and a Spring Boot module that turns it into an annotation. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. A Flaky Call, Retried

First, the good case. The gateway times out twice. The third attempt works. The caller receives a receipt, and never sees the two failures. Three calls reached the gateway.

## 5. Backoff

Second, backoff. Before the first retry, one millisecond. Before the second, two. Each wait doubles. In production the numbers would be larger, but the shape is the same. A struggling gateway is given room to recover.

## 6. Giving Up

Third, giving up. If the gateway never answers, the retry stops after three attempts. The caller gets the timeout exception. A retry has to end, and this is how.

## 7. Not Everything Is Worth Retrying

Fourth, what to retry. A declined card will decline again. With a list that retries only timeouts, there is one attempt. With the default, which retries everything, there are three. Three attempts against a card that will not change its mind, and a customer waiting.

## 8. A Retry Can Charge Twice

Fifth, the danger the partner video warned about. The charge went through, but the answer was lost, so the retry charged again. Without a key, two charges of forty nine ninety nine. With an idempotency key, the gateway recognises the repeat and charges once. The library cannot supply this. You must.

## 9. Retries Multiply

Last, layers. Checkout has a retry, and so does the payments client below it. Three attempts, each making three. One customer and one dead gateway make nine calls. Add a third layer and it is twenty seven. Retry in one layer only, and choose which.

## 10. The Verdict

My verdict, plainly. Retry only temporary failures. Send an idempotency key with every call that changes something. Retry in one layer, not two. And keep the attempts and the waits small.

## 11. How To Recognise It

How do you recognise this in code you did not write? A retry annotation with a name. Settings under resilience four j retry. And retry exceptions or ignore exceptions lists.

## 12. Where You Have Met This

You have met this in any Spring service that calls a payment, email or shipping provider over the network.

## 13. What Was Used

For the record. Spring Boot four point one point one. Resilience four j two point four point zero. No web server, and no web starter.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: the real retry and the real annotation. The waits are one and two milliseconds, and the values shown are the ones Resilience4j chose, not measured.

## 15. When This Is Too Much

So when is it too much? For a failure that will not go away, a retry only delays the error.

## 16. Thanks for Watching

That's Retry with Resilience4j. If you take one sentence away, take this one: Resilience4j gives you the retry as configuration, and safety is still your decision. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, remove the retry from the checkout layer, and rerun act six. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
