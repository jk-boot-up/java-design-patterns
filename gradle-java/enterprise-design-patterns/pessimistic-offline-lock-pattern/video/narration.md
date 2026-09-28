# Pessimistic Offline Lock Pattern — Video Narration Script

## 1. Pessimistic Offline Lock

Hello, and welcome. This video explains the Pessimistic Offline Lock pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A pessimistic lock makes a person take a lock on a record before editing it. Nobody else can edit it until the lock is released. So a clash is prevented, instead of detected. Think of a meeting room booking. Once you have booked the room, nobody else can use it until your booking ends. In our online store, two clerks want to edit the same product. And we would rather they did not clash at all. In this video, a lock stops a clash before it starts. Then we hear the costs: waiting, a forgotten lock, and two people each waiting for the other. And we learn how much to lock.

## 2. The Scenario

Here is the scenario. Two clerks want to edit the same product. An edit takes several minutes. And a clash would throw away a lot of work. So here is the question. Can we stop the clash before it even starts?

## 3. Lock First, Then Edit

First demo: lock first, then edit. Clerk A asks for the lock on the blue mug, and gets it. Clerk B asks, and is refused. And B is told who holds the lock: clerk A. Clerk B never starts an edit that might have been thrown away.

## 4. The Pattern

Now, the pattern. Take a lock before you edit. Only the lock holder may save changes. Everyone else is refused, and told who holds it. Release the lock when you are done. Or it expires by itself.

## 5. No Lost Update

Second demo: no lost update. Clerk A raises the price, and releases the lock. Then clerk B takes the lock, and reads the product. It already shows the new price, twelve pounds. Clerk B saves the stock count, on top of it. Nothing was overwritten. And nothing needed retrying.

## 6. The Bill: Waiting

Third demo: the first cost, waiting. While clerk A edits, clerk B tries once a minute. And is refused three times. In all that time, clerk B has done nothing useful. A lock swaps lost updates for waiting.

## 7. The Bill: A Lock Nobody Let Go Of

Fourth demo: a lock nobody released. Clerk A goes to lunch, without releasing the lock. Clerk B is refused straight away. And again, after ten minutes. After sixteen minutes, the lock has expired, and clerk B gets it. When clerk A comes back and saves, A is refused. Because A no longer holds the lock. An expiry solves the lunch problem, but creates a new problem for clerk A.

## 8. The Bill: Each Waiting For The Other

Fifth demo: two clerks, each waiting for the other. Clerk A holds the lock on the mug, and now needs the tea. Clerk B holds the lock on the tea, and now needs the mug. Neither can move, until a lock expires. That is called a deadlock. The fix is a simple rule: everyone takes locks in the same order. Then clerk A takes both. And clerk B is stopped at the first one, holding nothing, and simply waits.

## 9. How Much To Lock

Last demo: how much to lock. With one lock on the whole catalogue, clerk A gets it. And clerk B, editing a completely different product, is refused. With one lock per product, clerk A gets the mug, and clerk B gets the tea. Both can work. The smaller the thing you lock, the fewer people wait. But the more locks you have, the more there are to forget, and to deadlock on.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a lock, or check-out step, before an edit, and an unlock, or check-in, after. Look for a locks table, or columns saying who locked a record, and until when. Look for a database lock held across a long session, which is a warning sign. And a message like: this record is being edited by someone else.

## 11. The Verdict

So, here is the verdict. Use a pessimistic lock when a conflict would throw away a lot of work. When edits take a long time. And when it is acceptable for people to wait sometimes. Lock the smallest thing that keeps the data safe. Always give a lock an expiry. Take locks in a fixed order. And refuse a save from anyone who no longer holds the lock. Use an optimistic lock instead, where clashes are rare, and retrying is cheap.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every result you heard comes from the program's own output. Time is simulated, not read from the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? Where conflicts are rare and edits are short, a lock is waiting and bookkeeping for nothing. And a database lock held while a person thinks is almost always a mistake.

## 14. Thanks for Watching

That's the Pessimistic Offline Lock. If you remember one sentence, make it this one. A pessimistic lock prevents the clash, and the price is waiting, forgotten locks, and deadlocks. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a way for a lock holder to renew their lock. And decide how many times they may do it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
