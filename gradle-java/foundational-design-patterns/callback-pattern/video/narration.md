# Callback Pattern — Video Narration Script

## 1. Callback

Hello, and welcome. This video explains the Callback pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A callback is a piece of code you hand to someone else. They call it when the thing you asked for has happened. Think of leaving your phone number with a shop. You do not stand at the counter waiting. They call you when your order is ready. In our online store, a card payment takes a while to be answered. And the shop must not stand still until it is. In this video, a caller keeps asking for an answer, again and again. Then it hands over what to do, and carries on. We will hear a failing callback, answers arriving out of order, and the cost of nesting callbacks.

## 2. The Scenario

Here is the scenario. The payment gateway takes a while to answer a card charge. Meanwhile, the shop has other work to do. And other orders to charge. So here is the question. How do we hear the answer?

## 3. Ask, And Keep Asking

First, the naive way: ask, and keep asking. Is it done yet? Is it done yet? The answer arrived on the fifth look. Four looks found nothing. And the caller could do nothing else in all that time.

## 4. The Pattern

Now, the pattern. Hand over the code you want run. Carry on with other work. When the answer is ready, the other side calls your code, and passes it the result.

## 5. Say What To Do, And Go On

Second demo: say what to do, and carry on. The charge is requested, together with a callback. And the caller carries on straight away. The caller does some other work. Then the payment is answered, and the callback runs: order one, paid.

## 6. What Happened Decides What To Do

Third demo: the result decides what happens. One callback is given the result each time. Order one was paid, so the callback says: ship it. Order two was declined, so the callback says: ask for another card.

## 7. When The Callback Fails

Fourth demo: when the callback itself fails. The first callback throws an error. But the gateway carries on, and order two is paid. The error is recorded: order one, the mail server was down. The code that asked for the payment never sees that error. Because it happened inside someone else's call.

## 8. Answers In Another Order

Fifth demo: answers arriving in a different order. First, a version that remembers the current order in a shared field. The answers arrive in reverse order. And both callbacks say order two. One of them is wrong. Now a version where each callback carries its own order I D. Order two, paid. Order one, paid. The answers came in a different order, and each one is right.

## 9. The Bill

Finally, the cost. Pay, then reserve the stock, then ship. Three callbacks, each one inside the one before, three levels deep. The steps run in one order, but are written in another. Every level needs its own failure handling. And each answer arrives with no trace of who originally asked.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for parameters named on success, on complete, or handler. Look for Completable Future methods like then accept, and when complete. Look for event handlers, in a browser or in a desktop app. And look for a function passed into a method that works in the background.

## 11. The Verdict

So, here is the verdict. Use a callback when you ask for something that takes a while, and you want to carry on. Pass the result into the callback. Let each callback carry what it needs, instead of reading shared fields. Decide who handles a failure inside the callback. And when steps start chaining together, move to futures, so the code reads in the order it runs.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every result you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For work that is quick, simply returning a value is easier. And for chains of steps, futures read much better than nested callbacks.

## 14. Thanks for Watching

That's the Callback pattern. If you remember one sentence, make it this one. A callback lets you carry on while something takes time, and the price is code that runs out of written order, and failures no caller sees. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a second callback, which only runs when the payment fails. And check that the success callback is not called. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
