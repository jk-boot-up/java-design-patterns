# Future/Promise with Spring Pattern — Video Narration Script

## 1. Future/Promise with Spring

Hello, and welcome. This video explains the Future/Promise pattern with Spring Boot, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Future/Promise video. That one built the future and promise handoff by hand, and showed three costs: an exception that surfaces later, a get with no timeout that is a hang, and a cancellation a task can ignore. This one shows the same idea inside Spring Boot. The plain definition, in short: each piece of work is submitted and immediately returns a handle to a result that does not exist yet, so independent work can run at once. By the end you will see that the pool, not the annotation, decides how concurrent a page is, watch an exception vanish from a void method, lose a thread-local across the thread boundary, and learn why a timeout and a cancel both leave the work running.

## 2. The Partner Project

This video assumes the Future/Promise video. If you have not seen it, start there. It builds the future and promise handoff by hand, and shows three costs: an exception that surfaces later, a get with no timeout that is a hang, and a cancellation a task can ignore. This one uses the same example. It does not teach the pattern again. It shows what Spring Boot does with it.

## 3. Before The First Line

Before the first line of code, what Spring Boot is. Spring is a framework whose core is a container that creates your objects. Its async annotation runs a method on a thread pool it owns, and hands back a completable future, which the container completes when the method returns. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. The Pool Decides

First, concurrency. Three independent lookups, price, stock and rating, each marked async. On the default pool, all three are in flight at the same moment. Three. On a pool of one thread, only one is. The annotation asked for concurrency. The pool decided whether to give it. Concurrency is a property of the pool, not of the annotation.

## 5. Exceptions

Second, exceptions. A method returning a future fails, and the caller sees a completion exception, with the real cause inside it. The stack trace belongs to a pool thread. The calling method appears nowhere in it. Now a void method that throws. The caller gets nothing. The call returned normally. The exception went only to a handler that you have to register by hand. Without one, it is just logged. That is why the rule is: return a future, never void.

## 6. Thread-Locals

Third, context. The caller is working for customer seven. That is held in a thread-local, the way request context, security context, and logging context all are. The async method asks whose order it is. Customer null. A thread-local does not cross to a pool thread. The fix is a task decorator, a small bean that copies it across. With it: customer seven. The fix is yours to write.

## 7. A Timeout Does Not Stop It

Fourth, a timeout. The caller waits two hundred milliseconds for a slow task, and gets a timeout exception. The task had not finished. Then the gate opens, and the task runs to the end anyway, and does its work. Nobody is waiting for the answer. A timeout is the caller giving up. It does not stop the work.

## 8. cancel(true) Interrupts Nothing

Fifth, cancellation. Cancel true reports true. The future says it is cancelled. And the task ran to completion anyway. On a completable future, cancel sets a flag on the future. It never interrupts the thread. The hand-built video showed a task that ignored an interrupt. Here, no interrupt is even sent.

## 9. Composing The Page

Last, composing the page. Three futures combine into one, with no blocking until the very end. Now the review service is down. With a fallback chosen at that one step, the page still assembles: rating unavailable. Without the fallback, one failing lookup fails the whole page. That is the callback depth cost from the hand-built video, in a real library.

## 10. The Verdict

My verdict, plainly. Return a completable future, never void. Choose the pool. Carry the context across on purpose. A timeout is the caller giving up, not the work stopping. And design tasks that check for cancellation themselves.

## 11. How To Recognise It

How do you recognise this in code you did not write? Async on a method returning a completable future. Chains of then combine, exceptionally, and or timeout. A task decorator bean. And logging or security context copied by hand across a thread.

## 12. Where You Have Met This

You have met this in every async method that returns a completable future, and in every log line that lost its request identifier on the way to a pool thread.

## 13. What Was Used

For the record. Spring Boot four point one point one. No web server, no database, and no web starter.

## 14. What Is Real Here

The same honest admission as everywhere in this course, and short. Everything is real: Spring's executor, its futures, and its handlers. Every wait is a latch, a gate, or a bounded spin, so every result is the same each run.

## 15. When This Is Too Much

So when is it too much? For two lookups that are already fast, or where the second needs the first's result, a future around work that never overlaps is ceremony.

## 16. Thanks for Watching

That's Future/Promise with Spring. If you take one sentence away, take this one: a future is a promise about when a value will be ready, never a promise that the work can be stopped. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, make the slow task check for interruption in a loop, and cancel it through an executor's future, and see the difference. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
