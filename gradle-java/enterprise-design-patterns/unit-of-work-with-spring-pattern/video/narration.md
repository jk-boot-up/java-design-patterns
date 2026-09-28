# Unit of Work with Spring Pattern — Video Narration Script

## 1. Unit of Work with Spring

Hello, and welcome. This video explains the Unit of Work pattern, in Java, using Spring. This video is presented by Jayasekhar Konduru. First, a simple definition. A unit of work collects all the changes, and writes them together at the end. Or not at all. Think of a bank transfer. Money must leave one account and arrive in the other, together. Never just one half. This is the framework version of the Unit of Work video, with the very same order. We will hear the writes arrive at the end, not where the code is. And meet three failures that belong to Spring itself. An error that saves anyway, a write nobody asked for, and an annotation that does nothing.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Unit of Work video. That one builds the mechanism by hand. Register the changes, write them at the end, and undo everything on failure. Here, we use the same order: three lines, where the third stock update fails. We will not teach the pattern again. Instead, we ask what Spring does with it.

## 3. Before The First Annotation

Three things are new in this project. Spring, which creates the application's objects, and connects them. Hibernate, which turns work on objects into database commands. And H2, a database that runs in memory, so nothing needs installing. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. No Transaction

First demo: no transaction at all. Every step saves on its own. And the third stock update fails. What was saved? One order, with two of its three lines. Keyboard stock down to eight, mouse down to nine, and the monitor untouched. Half an order. The same problem as the hand-built video, now in Spring.

## 5. One Annotation

Second demo: one annotation, at Transactional, on the place order method. Listen to the counts. Inside the method, after changing three objects, nothing has been written yet. Zero inserts, and zero updates. After the method returns, two inserts and one update appear. The writes happened at the end, not where the code is. And now the same failure leaves no orders, and no lines. All of the order, or none of it. The whole hand-built class is replaced by one annotation.

## 6. The Checked Exception

Third demo: the first of Spring's own failures. The same stock failure, but now declared as a checked exception. That is the kind of error the compiler makes you handle. What was saved? One order, two lines, and stock of eight, nine, and ten. Half an order, even with the at Transactional annotation. Spring's default rule is this. Undo on unchecked errors. But save anyway on checked ones. Nothing in the code says so.

## 7. rollbackFor

Fourth demo: the fix. One setting on the annotation, called rollback for, naming the checked exception. Now the same failure undoes everything. No orders, no lines, and all stock back to ten. But someone had to know to write that setting. And nobody is warned when they forget.

## 8. A Flush Nobody Wrote

Fifth demo: a write nobody asked for. Changes are normally held until the end. Before changing a product's stock: zero updates written. After changing it: still zero, held back. Then an unrelated query runs, counting products. Now one update has been written. Hibernate wrote the change first, so the query would see it. This is called a flush. The write happened at a line that says nothing about writing. And if that write fails, it fails there, not at the end.

## 9. The Annotation That Does Nothing

Last demo: the annotation that does nothing. The at Transactional annotation works because Spring wraps the object in a proxy. The proxy begins and ends the transaction. Now one method calls another method on the same object, directly, through this. That call skips the proxy. So the annotation on the second method is never seen. The write fails, because there is no transaction. The error says: no entity manager with an actual transaction available. What was saved: one order, and no lines. This is one of the most common Spring errors there is.

## 10. Why These Surprise People

So why do these surprise people? The annotation hides the mechanism. But the mechanism still has rules. Checked exceptions save anyway. Queries can trigger writes. And only calls that go through the proxy count. None of those rules are visible in the code you wrote.

## 11. Where You Have Met This

Where have you met this before? In every at Transactional method in a Spring application. And the error from the last demo is one of the most common there is. Now you know why it happens, not just how to make it stop.

## 12. What Was Used

For the record, here are the versions. Spring Boot four point one point one. With whichever versions of Hibernate and H2 that release includes. There is no web server here. This video is about the transaction, not the web.

## 13. What Is Real Here

A quick, honest note about this demo. Everything here is real. The proxy is Spring's. The flush is Hibernate's. And the counts come from Hibernate's own statistics. The only stand-in is the database, H2, in memory.

## 14. When This Is Too Much

So, when is this too much? For a single write, the annotation is not needed at all. It earns its place when one business action writes several rows together.

## 15. Thanks for Watching

That's Unit of Work with Spring. If you remember one sentence, make it this one. An annotation hides the mechanism, but the mechanism still has rules. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make the stock failure a checked exception. And listen for what changes in the second demo. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
