# Pessimistic Offline Lock Pattern — Video Narration Script

## 1. Pessimistic Offline Lock

Hello, and welcome. This video explains the Pessimistic Offline Lock pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a pessimistic offline lock makes a person take a lock on a record before editing it. Nobody else can edit it until the lock is let go, so the clash is prevented instead of detected. This is another project in the enterprise category, whose subject is how a business application organises its logic, its data and its requests. In our online store, two clerks want to edit the same product, and we would rather they did not clash at all. By the end you will see a lock stop a clash before it starts, see edits that overwrite nothing, and see the three bills: waiting, a lock nobody let go of, and two people each waiting for the other. I will also show how much to lock.

## 2. The Scenario

Here is the scenario. In the online store, two clerks want to edit the same product. An edit takes several minutes, and a clash would throw away a lot of work. The question: can we stop the clash before it starts?

## 3. Lock First, Then Edit

First, lock, then edit. Clerk A asks for the lock on the blue mug, and gets it. Clerk B asks, and is refused, and told who holds it: A. Clerk B never starts an edit that could have been thrown away.

## 4. The Pattern

The pattern. Take a lock before you edit. Only the holder may write. Everyone else is refused, and told who holds it. You let go when you are done, or the lock expires by itself.

## 5. No Lost Update

Second, no lost update. Clerk A raises the price and lets go. Then B takes the lock, and reads the product. It already has the new price. B saves the stock count on top of it. Nothing was overwritten, and nothing needed retrying.

## 6. The Bill: Waiting

Third, the first bill. While clerk A edits, clerk B tries once a minute, and is refused three times. In that time B has done nothing useful. A lock trades lost updates for waiting.

## 7. The Bill: A Lock Nobody Let Go Of

Fourth, a lock nobody let go of. Clerk A goes to lunch without letting go. B is refused straight away, and again after ten minutes. After sixteen minutes the lock has expired, and B gets it. When A comes back and saves, A is refused, because A no longer holds the lock. An expiry solves the lunch, and creates a new problem for A.

## 8. The Bill: Each Waiting For The Other

Fifth, two clerks each waiting for the other. A holds the mug and now needs the tea. B holds the tea and now needs the mug. Neither can move, until a lock expires. That is a deadlock. The fix is a rule: everyone takes locks in the same order. Then A takes both, and B is stopped at the first, holding nothing, and simply waits.

## 9. How Much To Lock

Last, how much to lock. One lock on the whole catalogue: A gets it, and B, editing a completely different product, is refused. A lock per product: A gets the mug, and B gets the tea. The smaller the thing locked, the fewer people wait. But the more things you lock, the more there is to forget, and to deadlock on.

## 10. How To Recognise It

How do you recognise this in code you did not write? A lock or checkout step before an edit, and an unlock or checkin after. A locks table or a locked_by and locked_until column. SELECT ... FOR UPDATE held across a long session, which is a warning sign. A message such as 'this record is being edited by someone else'.

## 11. The Verdict

Here is my verdict, plainly. Use a pessimistic lock when a conflict would throw away a lot of work, when edits are long, and when it is acceptable that people sometimes wait. Lock the smallest thing that keeps the data safe, always give a lock an expiry, take locks in a fixed order, and refuse a write from anyone who no longer holds the lock. Use an optimistic lock where clashes are rare and retrying is cheap.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? Where conflicts are rare and edits short, a lock is waiting and bookkeeping for nothing. A long database lock held across a user's thinking time is almost always a mistake.

## 14. Thanks for Watching

That's Pessimistic Offline Lock. If you take one sentence away, take this one: a pessimistic lock prevents the clash, and the price is waiting, forgotten locks and deadlocks. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a way for a lock holder to renew its lock, and decide how many times it may. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
