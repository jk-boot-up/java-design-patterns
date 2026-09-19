# Optimistic Offline Lock Pattern — Video Narration Script

## 1. Optimistic Offline Lock

Hello, and welcome. This video explains the Optimistic Offline Lock pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: an optimistic offline lock lets people edit without locking anything. It detects a clash only when someone saves, by checking that the row has not changed since it was read. This is another project in the enterprise category, whose subject is how a business application organises its logic, its data and its requests. In our online store, two clerks edit the same product at the same time. By the end you will see two clerks silently overwrite each other, see a version number stop it, see how a retry keeps both changes, and see the three bills: a conflict that was not one, a busy row where most of the work is repeated, and a long edit lost at the last moment.

## 2. The Scenario

Here is the scenario. In the online store, two clerks open the same product. One raises the price. The other counts the stock. Each edits for a while, and then saves the whole row. The question: what happens to the first clerk's change?

## 3. No Lock: The Last Write Wins

First, no lock. Both clerks read the same row. Clerk A raises the price to twelve pounds and saves. Clerk B counts forty in stock, and saves the whole row, with the old price still in it. The row now says ten pounds. Clerk A's change vanished, and nobody was told.

## 4. The Pattern

The pattern. Nothing is locked while people work. Every row carries a version. A save succeeds only if the row still has the version that was read. If not, it is refused, and the writer must look again.

## 5. A Version On Every Row

Second, a version on every row. Clerk A saves, and the row moves to version two. Clerk B saves, but was working from version one, and is refused: changed by someone else since you read it. The twelve pound price survives.

## 6. Reload, Reapply, Save

Third, reload, reapply, save. Clerk B is refused, and reloads the row. Now it shows the new price. Clerk B reapplies the stock count, and saves. Two attempts, and both changes survive.

## 7. The Version Is Per Row

Fourth, the first bill. One clerk changed the price and another changed the stock. Different fields, and no real clash. But the second save is refused, because the version belongs to the whole row. A version for each field would let both through, at the cost of more bookkeeping.

## 8. The Bill: A Busy Row

Fifth, a busy row. Ten clerks each add one to the stock of the same product. Nothing is lost, and the stock ends at ten. But nineteen saves were attempted, and nine were refused. Nine of the ten did their work twice. A row that everyone wants is a row where most of the effort is repeated.

## 9. The Bill: You Find Out At The End

Last, the second bill. A user makes five changes over a long session. On saving, they are told the row changed. All five changes are discarded, and the user learns it only now. The cost of a conflict is paid at the moment it is found, which is the end.

## 10. How To Recognise It

How do you recognise this in code you did not write? A version column, and WHERE id = ? AND version = ? in an update. @Version in JPA and Hibernate. An OptimisticLockException or an HTTP 409 or 412 in the API. If-Match and ETag headers on a web request.

## 11. The Verdict

Here is my verdict, plainly. Use an optimistic lock when conflicts are rare, edits are short, and it is cheap to try again: most web applications. Keep the version in the row, check it in the update, retry by reloading, and tell the user honestly when their change cannot be applied. Use a pessimistic lock when a conflict is expensive, or a session is long.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? Where conflicts are frequent and costly, retrying wastes work and a lock is kinder. Where only one writer exists, a version is pure overhead.

## 14. Thanks for Watching

That's Optimistic Offline Lock. If you take one sentence away, take this one: an optimistic lock costs nothing until there is a clash, and then the clash is paid for in repeated work or lost edits. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, change the store so the version is per field, and see which conflicts disappear. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
