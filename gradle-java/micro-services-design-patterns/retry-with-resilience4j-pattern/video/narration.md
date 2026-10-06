# Retry with Resilience4j Pattern — Video Narration Script

## 1. Retry with Resilience4j

Hello, and welcome. This video explains the Retry with Backoff pattern in Java, using a library called Resilience four J. This video is presented by Jayasekhar Konduru. First, a simple definition. When a call fails for a reason that might not happen again, you try again. Each time, you wait a little longer first. And you only do it if doing the job twice cannot do it twice. In Resilience four J, a retry is an annotation on a method. The number of attempts, and the waits, are settings. In our online store, checkout calls a flaky payment gateway. By the end, you will hear the retry built from one annotation and a few settings. Then the three ways it goes wrong. Retrying what should not be retried. Charging a customer twice. And retries that multiply.

## 2. The Partner Project

This video builds on the plain Java Retry with Backoff video. If you have not seen it, start there. That video retries a flaky payment gateway, waiting longer each time. And it shows that a retry is only safe when the failure is temporary. And when doing the operation twice cannot do it twice. This video uses the same example. It does not teach the pattern again. It shows what Resilience four J does with it.

## 3. Before The First Line

Before any code, what is Resilience four J? It is a library of resilience patterns for Java. It includes a retry, with settings for the waits, and lists of which errors to retry. It also has a Spring Boot module that turns the retry into an annotation. And a promise. Skipping this video loses none of the pattern. The plain Java video teaches all of it.

## 4. A Flaky Call, Retried

First demo: the good case. The gateway times out twice. The third attempt works. The caller receives a receipt. And it never sees the two failures. Three calls reached the gateway.

## 5. Backoff

Second demo: backoff. Before the first retry, the wait is one millisecond. Before the second, two milliseconds. Each wait doubles. In a real system, the numbers would be bigger, but the shape is the same. A struggling gateway is given room to recover.

## 6. Giving Up

Third demo: giving up. This time, the gateway never answers. The retry stops after three attempts. And the caller gets the timeout error. A retry has to end somewhere. And this is how.

## 7. Not Everything Is Worth Retrying

Fourth demo: what is worth retrying? A declined card will be declined again. With a setting that retries only timeouts, there is one attempt. With the default, which retries every error, there are three. Three attempts, against a card that will not change its mind. And a customer left waiting.

## 8. A Retry Can Charge Twice

Fifth demo: the danger the plain Java video warned about. The charge went through, but the reply was lost. So the retry charged again. Without a key, there are two charges of forty-nine pounds ninety-nine. With an idempotency key, the gateway recognises the repeat. And it charges only once. The library cannot supply that key. You must.

## 9. Retries Multiply

Last demo: retries in layers. Checkout has a retry. And the payment client underneath it also has one. Checkout makes three attempts. And each of those makes three attempts of its own. So one customer and one dead gateway make nine calls. Add a third layer, and it is twenty-seven. So retry in one layer only, and choose which one.

## 10. The Verdict

So, here is the verdict. Retry only temporary failures. Send an idempotency key with every call that changes something. Retry in one layer, not two. And keep the number of attempts, and the waits, small.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a retry annotation, with a name. Look for retry settings in the configuration file. And look for lists of which errors to retry, and which to ignore.

## 12. Where You Have Met This

Where have you met this before? In any Spring service that calls a payment, email, or shipping provider over the network.

## 13. What Was Used

For the record, here is what was used. Spring Boot, version four point one point one. Resilience four J, version two point four point zero. There is no web server, and no web starter.

## 14. What Is Real Here

A quick, honest note about this demo. Everything is real: the real retry, and the real annotation. The waits are only one and two milliseconds. And the values you heard are the ones Resilience four J chose, not measured times.

## 15. When This Is Too Much

So, when is this too much? For a failure that will not go away, a retry only delays the error.

## 16. Thanks for Watching

That's Retry, with Resilience four J. If you remember one sentence, make it this one. Resilience four J gives you the retry as settings, but deciding whether it is safe is still your job. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Remove the retry from the checkout layer. Then run the last demo again, and count the calls. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
