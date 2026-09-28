# Future/Promise Pattern — Video Narration Script

## 1. Future/Promise

Hello, and welcome. This video explains the Future and Promise pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When you start a piece of work, you immediately get back a handle to a result that does not exist yet. That handle is called a future. So independent pieces of work can run at the same time, instead of each one waiting for the last. Think of a coffee shop buzzer. You order, and get a buzzer straight away. You sit down, and the buzzer tells you when your coffee is ready. In our online store, a product page needs three separate lookups. By the end, you will know which half of this pattern belongs to the reader, and which to the writer. You will hear an error whose report does not mention the line that caused it. And you will learn why cancelling a task is only a request.

## 2. The Scenario

Here is the scenario. A product page needs three things before it can appear. The price, the stock count, and a review score. Each is a real lookup, and each takes about two hundred milliseconds. Here is the key detail. None of the three depends on the others. The price does not need the stock count. The review score does not care about the price. So why would the code make them wait for each other?

## 3. Naive — Sequential Lookups

First, the naive version. It calls all three lookups, one after another. It waits for each to finish before starting the next. The page takes six hundred and nineteen milliseconds. Three lookups of two hundred milliseconds each, simply added together. For work that has no reason to wait at all.

## 4. The Pattern — Concurrent Lookups

Now the fix, in one sentence. Each lookup is started, and immediately returns a future. All three are started before the page asks any of them for its value. The page now takes two hundred and eight milliseconds. Not the sum of three lookups. Roughly the time of the slowest one, because all three really ran at the same time.

## 5. The Two Halves Beginners Conflate

Before the next demo, one important distinction. Java's Completable Future holds both halves of this pattern at once. That is why they are easy to mix up. The future is the reader's half. Whoever holds it calls get, and waits until a value appears. It does not need to know who produces the value. The promise is the writer's half. Whoever holds it calls complete, once its work is done. It does not need to know who is reading, or whether anyone is.

## 6. Future And Promise, Made Explicit

Third demo: the two halves, on two separate threads. A reader thread creates a future, and immediately calls get. So it waits. At the same moment, a writer thread does its own work. Then it calls complete on that very same object, with the price: one hundred and twenty-nine pounds ninety-nine. The reader wakes up the instant the writer completes it. One piece of code fills in exactly what another piece is waiting for.

## 7. Exceptions Move

Now the first honest cost. A task that fails does not fail where it was started. It fails quietly, on whichever worker thread ran it. The error only appears later, wrapped up, when someone calls get. And the error's stack trace belongs entirely to the worker thread. The line of code that started the task is not in it. It cannot be, because a stack trace records one thread, at one moment. And the thread that started the task was somewhere else entirely when it failed.

## 8. get() With No Timeout Is A Hang

The second honest cost. A task that never finishes leaves a plain get call waiting for as long as the thread is willing. And by default, that is forever. This demo protects itself with a two hundred millisecond timeout, so it can finish, and report what happened. It timed out after about two hundred and five milliseconds. That timeout is not a nice extra. For a task that never finishes, it is the only difference between waiting, and hanging forever.

## 9. Cancellation Is Cooperative

The third honest cost surprises people most. Calling cancel with true interrupts the thread running the task. But it does not stop the task. In this demo, the task catches every interruption, and simply carries on. Real code sometimes does this by accident. Cancel reports success. And the task runs to the end anyway. Cancel asked, the task said no, and nothing forced it to listen.

## 10. One More Cost: Chained Callbacks

One more cost, briefly. Completable Future has methods like then apply, then compose, and then combine. They let results flow from one step to the next, without ever calling get. In a small example, they are powerful. But by the fourth or fifth step, they become hard to read. Each step adds another nested function. And another place where an error can quietly disappear, if a handler is forgotten.

## 11. The Same Harness, Proven Again

How does the demo make its results repeatable? With the same small tools used across these concurrency videos. For example: two threads each read a shared stock count of ten. Then they meet at a meeting point, which releases neither until both have arrived. Only then does each write back what it read, minus one. Run it twenty times, and the answer is nine, twenty times, never eight. Because both threads are proven to hold the same old value before either writes.

## 12. What The Scheduler Really Does

A quick, honest note about this demo. Every repeatable result was made repeatable on purpose. A lookup is proven to have started. A gate is set never to open. A task is proven to be inside its loop. Everywhere else, the operating system decides freely which thread runs when. So a passing test proves the forced scene, not every possible timing.

## 13. The Bill

Here are the costs, gathered in one place. One. Errors move. They appear later, wrapped up, and their stack trace never includes the line that started the task. Two. A plain get with no timeout is not a long wait. It can be a hang. Three. Cancel is a request, not a command. A task must check for it, and choose to stop. Plenty of real code forgets.

## 14. When This Is Too Much

So, when is this pattern worth it? When two or more pieces of work are truly independent, and each takes real, measurable time. Exactly like this video's three lookups. It is not worth it for calls that are already fast. Or when the second call needs the first call's result. Then there is nothing to overlap.

## 15. Thanks for Watching

That's the Future and Promise pattern. If you remember one sentence, make it this one. A future promises when a value will be ready, but never that the work behind it can be stopped. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Remove the timeout from the hanging demo's get call. Read the code carefully, and work out what would happen, before you run it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
