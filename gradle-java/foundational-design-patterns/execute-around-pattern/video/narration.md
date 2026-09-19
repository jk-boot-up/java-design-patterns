# Execute Around Pattern — Video Narration Script

## 1. Execute Around

Hello, and welcome. This video explains the Execute Around pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: execute around puts the set up and the clean up in one method. The caller hands in only the work in the middle. This is another project in the foundational category, whose subject is how an object gets hold of another, and how small idioms shape everyday Java. In our online store, every piece of code that reads orders must open a connection and close it again, and someone always forgets on the error path. By the end you will see a connection leak on a failure, see the closing done in one place, see a result come out, see a transaction undone on failure, see the same shape used for timing, and see the bill, which is a resource that escapes and a caller trapped in a lambda.

## 2. The Scenario

Here is the scenario. Every query to the order database needs a connection, and every connection must be closed, whether the query works or fails. The question: who does the closing?

## 3. Open, Use, Close, By Hand

First, open, use, close, by hand. The query broke, and the code that would close the connection was after it. Connections still open: one. Repeat that on every failure, and the pool runs dry.

## 4. The Pattern

The pattern. One method opens, runs the work, and closes. The caller passes only the work, as a lambda. The closing sits in a finally block, once.

## 5. The Caller Gives The Work

Second, the caller gives the work, and the pool does the rest. The same failure: the query broke. Connections opened: one. Still open: none. The closing is in one place, in a finally block, and cannot be forgotten.

## 6. Getting An Answer Out

Third, getting an answer out. A string came out: the rows for an order. A number came out: fifteen. Still open: none.

## 7. All Or Nothing

Fourth, all or nothing. Two purchases of three thousand from a credit of five thousand: the second failed, with not enough credit. The balance afterwards is five thousand. The first purchase was undone too. One purchase of three thousand that works leaves two thousand.

## 8. The Same Shape, For Measuring

Fifth, the same shape, for measuring. Receipt sent, in five ticks. And a failing job: the mail server timed out, and it was still measured: nine ticks.

## 9. The Bill

Last, the bill. The caller let the connection out of the block, and used it later: connection one is closed. The block cannot stop that. The caller's code is now inside a lambda: it cannot return early, and it cannot throw a checked exception without help. And with two resources the blocks nest, one inside the other, so the real work drifts to the right.

## 10. How To Recognise It

How do you recognise this in code you did not write? JdbcTemplate.query(...) and TransactionTemplate.execute(...) in Spring. try (var in = ...) { ... }, the language's own version. Files.lines used inside a block, lock.lock(); try { ... } finally { lock.unlock(); }. A method that takes a lambda named work, callback or action.

## 11. The Verdict

Here is my verdict, plainly. Use execute around wherever something must be undone or finished after use: connections, files, locks, transactions, timers. Put the clean-up in a finally block, once. Do not let the resource leave the block. For plain files and streams, try-with-resources is the language's own form of it.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a resource used once, in one place, try with resources is enough. Write your own around method when many callers repeat the same set-up and clean-up.

## 14. Thanks for Watching

That's Execute Around. If you take one sentence away, take this one: execute around puts the opening and closing in one place, and the price is that the work is trapped in a lambda, and the resource can still escape. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a method that retries the work up to three times, around the same connection. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
