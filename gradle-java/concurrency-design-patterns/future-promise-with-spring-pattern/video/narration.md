# Future/Promise with Spring Pattern — Video Narration Script

## 1. Future/Promise with Spring

Hello, and welcome. This video explains the Future and Promise pattern, in Java, using Spring Boot. This video is presented by Jayasekhar Konduru. First, a simple definition. When you start a piece of work, you immediately get back a handle to a result that does not exist yet. So independent pieces of work can run at the same time. Think of dropping clothes at a dry cleaner. You get a ticket straight away, and collect the clothes later. This is the framework version of the Future and Promise video, with the same product page. We will learn that the thread pool, not the annotation, decides how much runs at once. We will hear an error vanish from a method that returns nothing. Lose a customer's details between threads. And learn why a timeout and a cancel both leave the work running.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Future and Promise video. That one builds the handoff between a future and a promise by hand. And it shows three costs: an error that appears later, a wait with no timeout that hangs, and a cancel that a task can ignore. If you are new to the pattern, watch that one first. Here, we keep the same product page, with its price, stock, and review score, and ask what Spring Boot does with it.

## 3. Before The First Line

One thing is new in this project: Spring Boot. At its heart, Spring is a container that creates your objects. Its at Async annotation runs a method on a thread pool that Spring owns. And it hands back a Completable Future. Spring completes that future when the method returns. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. The Pool Decides

First demo: the pool decides. Three independent lookups, for price, stock, and rating, each marked at Async. On the default pool, all three run at the same moment. On a pool with just one thread, only one runs at a time. The annotation asked for things to run at once. The pool decided whether to allow it. How much runs at once is a property of the pool, not the annotation.

## 5. Exceptions

Second demo: errors. A method that returns a future fails. The caller receives a Completion Exception, with the real cause inside: the review service is down. And the stack trace belongs to a pool thread, not the caller. Now a method that returns nothing, called a void method, throws an error. The caller gets nothing at all. The call returned normally. The error only went to a special handler, which you must register yourself. Without one, it is just written to a log. That is why the rule is: return a future, never void.

## 6. Thread-Locals

Third demo: thread-local data. The caller is working for customer seven. That fact is stored in a thread-local, which is where request details, security details, and logging details usually live. The async method asks: whose order is this? The answer is: nobody's. A thread-local does not travel to a pool thread. The fix is a Task Decorator, a small bean that copies the data across. With it, the answer is customer seven. But you have to write that fix yourself.

## 7. A Timeout Does Not Stop It

Fourth demo: a timeout does not stop the work. The caller waits two hundred milliseconds for a slow task. Then it gets a Timeout Exception. The task had not finished. Later, the task carries on, runs to the end, and does its work anyway. Nobody is waiting for its answer any more. A timeout means the caller gave up. It does not stop the work.

## 8. cancel(true) Interrupts Nothing

Fifth demo: cancelling. Calling cancel with true reports success. The future says it is cancelled. And the task runs to the end anyway. Why? On a Completable Future, cancel only sets a flag on the future. It never interrupts the thread doing the work. In the hand-built video, a task ignored an interruption. Here, no interruption is even sent.

## 9. Composing The Page

Last demo: building the page from futures. Three futures are combined into one. Nothing waits until the very end. The page shows a price of one hundred and twenty-nine pounds ninety-nine, a stock of seven, and a rating of four point six. Now the review service goes down. With a fallback chosen at that one step, the page still appears, with the rating marked as unavailable. Without the fallback, one failed lookup fails the whole page.

## 10. The Verdict

So, here is the verdict. Return a Completable Future, never void. Choose your thread pool deliberately. Carry thread-local data across on purpose. Remember that a timeout is giving up, not stopping. And design tasks that check for cancellation themselves.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for at Async methods that return a Completable Future. Look for chains of then combine, exceptionally, and or timeout. Look for a Task Decorator bean. And look for logging or security details, copied by hand between threads.

## 12. Where You Have Met This

Where have you met this before? In every at Async method that returns a future. And in every log line that lost its request I D on the way to a pool thread.

## 13. What Was Used

For the record, here are the versions. Spring Boot four point one point one. No web server, no database, and no web library.

## 14. What Is Real Here

A quick, honest note about this demo. Spring's thread pool, its futures, and its error handlers are all real. Every wait uses a latch, a gate, or a short, limited loop. So every run gives the same result.

## 15. When This Is Too Much

So, when is this too much? For lookups that are already fast, or where the second needs the first's result, a future adds ceremony and saves no time.

## 16. Thanks for Watching

That's Future and Promise with Spring. If you remember one sentence, make it this one. A future promises when a value will be ready, but never that the work behind it can be stopped. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make the slow task check for interruption in its loop. Then cancel it through a normal executor's future, and listen for the difference. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
