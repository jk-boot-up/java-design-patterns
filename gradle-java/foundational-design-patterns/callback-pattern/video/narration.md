# Callback Pattern — Video Narration Script

## 1. Callback

Hello, and welcome. This video explains the Callback pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a callback is a piece of code you hand to someone else, to be called when something you asked for has happened. This is another project in the foundational category, whose subject is how an object gets hold of another, and how small idioms shape everyday Java. In our online store, a card payment takes a while to be answered, and the shop must not stand still until it is. By the end you will see a caller asking again and again for an answer, see it hand over what to do and go on, see one callback told what happened, see a failing callback not stop the gateway, see answers arrive in another order and each callback still right, and see the bill, which is callbacks nested inside callbacks.

## 2. The Scenario

Here is the scenario. The payment gateway takes a while to answer a card charge. Meanwhile, the shop has other work to do, and other orders to charge. The question: how do we hear the answer?

## 3. Ask, And Keep Asking

First, ask, and keep asking. The answer arrived on the fifth look. Five looks were made, and four of them found nothing. And the caller could do nothing else in that time.

## 4. The Pattern

The pattern. Hand over the code to run. Go on with other work. When the answer is ready, the other side calls your code, with the result.

## 5. Say What To Do, And Go On

Second, say what to do, and go on. The charge is requested, and the caller goes on. The caller does other work. Then the callback runs: order one, paid.

## 6. What Happened Decides What To Do

Third, what happened decides what to do. One callback, told the result. Order one was paid: ship it. Order two was declined: ask for another card.

## 7. When The Callback Fails

Fourth, when the callback itself fails. The first callback threw an error. The gateway went on, and order two was paid. The error was recorded: order one, the mail server was down. The one who asked never sees that exception, because it happened in someone else's call.

## 8. Answers In Another Order

Fifth, answers in another order. Remembering the order in a field: both callbacks say order two. Each callback holding its own order id: order two paid, order one paid. The answers came in the other order, and each is right.

## 9. The Bill

Last, the bill. Pay, then reserve, then ship: three callbacks, each inside the one before, three levels deep. The lines run in one order, but are written in another. Every level needs its own handling for a failure. And each answer arrives with no stack that shows who asked.

## 10. How To Recognise It

How do you recognise this in code you did not write? A parameter named onSuccess, onComplete or handler. CompletableFuture.thenAccept(...), and whenComplete(...). Event handlers in a browser or in Swing, and Node.js style callbacks. Consumer<Result> passed to an async method.

## 11. The Verdict

Here is my verdict, plainly. Use a callback when you ask for something that takes a while, and want to go on. Pass the result to it. Let each callback carry what it needs, not read shared fields. Decide who handles a failure in the callback. When steps chain, move to futures or an async style, so the code reads in order.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For work that is quick, a plain return value is simpler. For chains of steps, futures or coroutines read better than nested callbacks.

## 14. Thanks for Watching

That's Callback. If you take one sentence away, take this one: a callback lets you go on while something takes time, and the price is code that runs out of written order, and failures that no caller sees. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a second callback that runs only when the payment fails, and check that the success one is not called. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
