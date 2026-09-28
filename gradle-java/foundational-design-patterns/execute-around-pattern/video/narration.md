# Execute Around Pattern — Video Narration Script

## 1. Execute Around

Hello, and welcome. This video explains the Execute Around pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Execute Around puts the setting up, and the cleaning up, in one method. The caller only hands in the work that goes in the middle. Think of a car wash. The machine always opens the gate at the start, and closes it at the end. You only drive through the middle. In our online store, every piece of code that reads orders must open a database connection, and close it again. And someone always forgets, when something goes wrong. In this video, a connection leaks on a failure. Then the closing moves into one place. We will get results out, undo a failed transaction, measure time, and then hear the cost.

## 2. The Scenario

Here is the scenario. Every query to the order database needs a connection. And every connection must be closed, whether the query works, or fails. So here is the question. Who does the closing?

## 3. Open, Use, Close, By Hand

First, the naive way: open, use, and close, by hand. The query breaks. And the line that would close the connection came after it, so it never runs. Connections still open: one. Repeat that on every failure, and the connection pool runs dry.

## 4. The Pattern

Now, the pattern. One method opens the connection, runs the work, and closes it. The caller passes in only the work, as a lambda. The closing sits in a finally block, written once.

## 5. The Caller Gives The Work

Second demo: the caller only gives the work. The same failure: the query breaks. Connections opened: one. Still open: none. The closing lives in one place, in a finally block. So it cannot be forgotten.

## 6. Getting An Answer Out

Third demo: getting an answer out. The work can return a value. Here, it returns the rows for an order. And here, it returns a number: fifteen. And still, no connections are left open.

## 7. All Or Nothing

Fourth demo: all or nothing. A customer has fifty pounds of credit. Two purchases of thirty pounds each are made, inside one transaction. The second fails, because there is not enough credit. Afterwards, the balance is still fifty pounds. The first purchase was undone too. A single purchase of thirty pounds, which works, leaves twenty pounds.

## 8. The Same Shape, For Measuring

Fifth demo: the same shape, for measuring time. Sending a receipt took five ticks. And a job that fails, because the mail server timed out, is still measured. Nine ticks. Because the measuring also sits in a finally block.

## 9. The Bill

Finally, the costs. First, the caller let the connection out of the block, and used it later. By then, it was closed. The pattern cannot stop that. Second, the caller's code now lives inside a lambda. It cannot return early from the outer method. And it cannot throw a checked exception without extra help. Third, with two resources, the blocks nest one inside the other. And the real work drifts further and further to the right.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? In Spring, look for the JDBC template's query method, and the transaction template's execute method. In Java itself, look for try-with-resources, which is the language's own version. Look for a lock, followed by try, and an unlock in a finally block. And look for methods that take a lambda named work, callback, or action.

## 11. The Verdict

So, here is the verdict. Use Execute Around wherever something must be undone, or finished, after use. Connections, files, locks, transactions, and timers. Put the cleaning up in a finally block, once. And do not let the resource escape from the block. For simple files and streams, try-with-resources is the language's own form of this pattern.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Time is counted in ticks, not by the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a resource used once, in one place, try-with-resources is enough. Write your own execute around method when many callers repeat the same setting up, and cleaning up.

## 14. Thanks for Watching

That's the Execute Around pattern. If you remember one sentence, make it this one. Execute Around puts the opening and closing in one place, and the price is work trapped in a lambda, and a resource that can still escape. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a method that retries the work up to three times. All around the same connection. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
