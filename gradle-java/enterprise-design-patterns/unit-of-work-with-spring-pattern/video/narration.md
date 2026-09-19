# Unit of Work with Spring Pattern — Video Narration Script

## 1. Unit of Work with Spring

Hello, and welcome. This video explains the Unit of Work pattern with Spring, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Unit of Work video. That one built the pattern by hand. This one shows the very same order going through one annotation. The plain definition, in short: collect all the changes, and write them together at the end, or not at all. By the end you will see the writes arrive at commit, not where the code is, and meet the failures that belong to Spring itself: a checked exception that commits anyway, a flush nobody wrote, and an annotation that does nothing.

## 2. The Partner Project

This video assumes the Unit of Work video. If you have not seen it, start there. It builds the mechanism by hand: register the changes, write them at commit, roll back to nothing. This one uses the same order: three lines, where the third stock update fails. It does not teach the pattern again. It shows what Spring does with it.

## 3. Before The First Annotation

Before the first annotation, three new things. Spring creates the objects of an application, and wires them together. Hibernate turns operations on objects into S Q L. H two is a database that runs in memory, so nothing needs installing. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. No Transaction

First, with no transaction around the order. Every step commits on its own. The third stock update fails. What is committed: one order. Two lines. Keyboard stock down to eight, mouse stock down to nine, monitor untouched. Half an order. The very first act of the Unit of Work video, now in Spring.

## 5. One Annotation

Now the one annotation: transactional, on the place method. Watch the counts. Inside the method, after changing three objects, inserts written: zero. Updates written: zero. After the method returned: two inserts, one update. The writes appeared at commit, not where the code is. And the same failure now leaves orders zero, lines zero. All of the order, or none of it. That whole hand-built class is one annotation.

## 6. The Checked Exception

Now the failures that are Spring's own. The same failure, but declared as a checked exception, one the compiler makes you handle. Committed: one order, two lines, stock eight, nine, ten. Half an order. Under the transactional annotation. Spring's default: roll back on unchecked exceptions and errors. Commit on checked ones. Nothing in the code says so. The annotation looks the same.

## 7. rollbackFor

The fix is one attribute: rollback for, naming the checked exception. Now the same failure rolls everything back. Orders zero, lines zero, stock ten, ten, ten. But the default had to be overridden, in the annotation, by someone who knew. Nobody is warned when they forget.

## 8. A Flush Nobody Wrote

Second failure. Changes are held until commit. But look at this. Updates written before the change: zero. After changing a product's stock: still zero, held back. Then an unrelated query runs, counting products. Updates written: one. Hibernate wrote the change first, so that the query would see it. The write happened at a line that says nothing about writing. And if that write fails, it fails there, not at the end.

## 9. The Annotation That Does Nothing

Third failure. The transactional annotation works because Spring wraps the object in a proxy. The proxy begins and commits the transaction. Now a method calls another method on the same object, through this. That call skips the proxy. The annotation on the second method is never seen. The write fails, for want of a transaction. Transaction required exception: no entity manager with actual transaction available. Committed: one order, no lines. One of the most common Spring errors there is.

## 10. Why These Surprise People

So why do these surprise people? The annotation hides the mechanism. But the mechanism still has rules. Checked exceptions commit. Queries can flush. And only calls that go through the proxy count. None of those rules are visible in the code you wrote.

## 11. Where You Have Met This

You have met this. Every transactional method in a Spring application. And the error in act six is one of the most common Spring errors there is. Now you know why it happens, not just how to make it stop.

## 12. What Was Used

For the record. Spring Boot four point one point one. Hibernate and H two are whichever versions that release manages. There is no web server and no web starter in this project. It is about the transaction boundary, not H T T P.

## 13. What Is Real Here

The same honest admission as everywhere in this course, and again short. Everything is real. The proxy is Spring's. The flush is Hibernate's. The counts come from Hibernate's own statistics. The only stand-in is the database, H two in memory.

## 14. When This Is Too Much

So when is it too much? For a single write, the annotation is not needed at all. It earns its place when one business action writes several rows together.

## 15. Thanks for Watching

That's Unit of Work with Spring. If you take one sentence away, take this one: an annotation hides the mechanism, and the mechanism still has rules. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, make the stock failure extend Exception instead, and see what changes in act two. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
