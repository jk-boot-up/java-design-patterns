# Optimistic Offline Lock Pattern — Video Narration Script

## 1. Optimistic Offline Lock

Hello, and welcome. This video explains the Optimistic Offline Lock pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An optimistic lock lets people edit without locking anything. It only detects a clash when someone saves. By checking that the data has not changed since it was read. Think of editing a shared document offline. When you reconnect, the app checks whether someone else changed it meanwhile, before accepting your version. In our online store, two clerks edit the same product at the same time. In this video, they silently overwrite each other. Then a version number stops it, and a retry keeps both changes. And then we hear three costs.

## 2. The Scenario

Here is the scenario. Two clerks open the same product. One raises its price. The other counts its stock. Each one edits for a while, and then saves the whole product row. So here is the question. What happens to the first clerk's change?

## 3. No Lock: The Last Write Wins

First, no lock at all. Both clerks read the same row. Clerk A raises the price to twelve pounds, and saves. Clerk B counts forty in stock, and saves the whole row, with the old price still in it. The row now says ten pounds. Clerk A's change has vanished. And nobody was told. The last one to save simply wins.

## 4. The Pattern

Now, the pattern. Nothing is locked while people work. But every row carries a version number. A save only succeeds if the row still has the version that was read. If not, the save is refused. And the person saving must look again.

## 5. A Version On Every Row

Second demo: a version on every row. Clerk A saves, and the row moves to version two. Clerk B saves. But clerk B was working from version one. So the save is refused, with the message: changed by someone else since you read it. The twelve pound price survives.

## 6. Reload, Reapply, Save

Third demo: reload, reapply, and save. Clerk B is refused, and reloads the row. Now it shows the new price of twelve pounds. Clerk B reapplies the stock count of forty, and saves again. Two attempts in total. And both changes survive: price twelve pounds, stock forty.

## 7. The Version Is Per Row

Fourth demo, and the first cost. One clerk changed the price. Another changed the stock. Different fields, so there was no real clash. But the second save is still refused. Because the version number belongs to the whole row. It is a conflict that was not really a conflict. A version for each field would let both through, but at the cost of more bookkeeping.

## 8. The Bill: A Busy Row

Fifth demo: a busy row. Ten clerks each add one to the stock of the same product. Nothing is lost, and the stock ends at ten. But nineteen saves were attempted, and nine were refused. Nine of the ten clerks did their work twice. On a row everyone wants, most of the effort gets repeated.

## 9. The Bill: You Find Out At The End

Last demo: the second cost, you only find out at the end. A user makes five changes, over a long editing session. When they save, they are told the row has changed. All five changes are thrown away. And the user only learns this now, at the very end. The cost of a conflict is paid at the moment it is found.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a version column, and an update that checks both the I D and the version. Look for the at Version annotation in J P A, or Hibernate. Look for an Optimistic Lock Exception, or a web service answering four hundred and nine, meaning conflict. And look for web requests using the If Match header, with an E Tag.

## 11. The Verdict

So, here is the verdict. Use an optimistic lock when conflicts are rare, edits are short, and trying again is cheap. That describes most web applications. Keep the version in the row. Check it in the update. Retry by reloading. And tell the user honestly when their change cannot be applied. Use a pessimistic lock instead, when a conflict is expensive, or an editing session is long.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? Where conflicts are frequent and costly, retrying wastes work, and a lock is kinder. And where there is only ever one writer, a version number is pure overhead.

## 14. Thanks for Watching

That's the Optimistic Offline Lock. If you remember one sentence, make it this one. An optimistic lock costs nothing until there is a clash, and then the clash is paid for in repeated work, or lost edits. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Change the store, so the version is kept per field instead of per row. Then see which conflicts disappear. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
