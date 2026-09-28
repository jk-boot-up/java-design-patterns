# Read-Write Lock Pattern — Video Narration Script

## 1. Read-Write Lock

Hello, and welcome. This video explains the Read-Write Lock pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A read-write lock lets many readers in together, but lets a writer in only alone. Because two reads can never conflict with each other. Only a write can conflict with anything. Think of a museum painting. Any number of visitors can look at it at once. But when the restorer works on it, the room is closed to everyone. In our online store, many shoppers read a product's price, and a merchandiser sometimes changes it. By the end, you will know what a torn read is. Why a waiting writer can still be overtaken. Why upgrading a read lock deadlocks. And, surprisingly, when a read-write lock is slower than a plain lock.

## 2. The Scenario

Here is the scenario. An online store shows a product's price. The price is two facts, kept together: an amount, and a currency. A thousand shoppers read that price all day. Now and then, a merchandiser changes it. So how do readers stay safe from a half-finished change? And how do they stay fast?

## 3. No Lock — The Torn Read

First demo: no lock at all. The writer changes the price in two steps. First the amount, then the currency. A reader is made to arrive exactly between those two steps. It reads fifty-four ninety-nine, in pounds. That price never existed. It is the new amount, with the old currency. This is called a torn read. It needs two separate fields to happen. A single value, written in one step, cannot be torn.

## 4. One Lock — Correct, But Queued

The obvious fix is one lock, around every read and every write. It is correct. A torn read is now impossible. But think about the readers. Two readers can never conflict with each other. Yet this lock cannot tell a reader from a writer. So every reader queues behind every other reader, for no good reason. Eight readers, each reading fifty thousand times, take fifteen milliseconds. Remember that number.

## 5. The Pattern — Two Locks In One

Now, the pattern: one lock, with two sides. The read lock is shared. Any number of readers can hold it at the same time. The write lock is exclusive. One writer holds it, and while it does, nobody else can get in. Not readers, and not other writers. In Java, this is the Reentrant Read Write Lock.

## 6. The Surprise

Third demo: the same eight readers, using the read-write lock. No reader ever waited for another reader. So surely this is faster? It is not. One hundred and thirty-eight milliseconds, compared with fifteen for the plain lock. Why? The lock keeps a count of how many readers are inside, in shared memory. Every reader updates that count, every time. And eight threads fight over it. For a read as cheap as returning one price, that fight costs more than it saves.

## 7. Cost One — Writer Starvation

Now the honest costs. The first: a waiting writer is not guaranteed to go next. In this demo, the writer is really waiting in line, for the current reader to finish. Then a second reader arrives. And it slips straight past the waiting writer. Java's documentation says this is allowed. If readers keep arriving, nothing limits how long the writer waits. That is called writer starvation.

## 8. Cost Two — The Upgrade Deadlock

The second cost: the upgrade deadlock. A thread holds the read lock, reads the price, and decides to change it. So it asks for the write lock. But the write lock waits for every reader to leave. That includes this very thread. And it cannot leave, because it is stuck waiting. It waits for itself, forever. This demo rescues it after about two hundred milliseconds, just to report what happened. Moving from the write lock down to the read lock is allowed. Moving up is not.

## 9. Cost Three — When The Lock Loses

The third cost, and the biggest. Here are three ways to protect the same price, measured on the same reads. A plain single lock: sixteen milliseconds. The read-write lock: one hundred and thirty-seven. An unchangeable snapshot: two milliseconds. How does the snapshot work? The price is an object that can never change. To publish a new price, you swap one reference, in one atomic step. A reader sees either the whole old price, or the whole new one. Never a mixture. And there is no lock, and no reader count, at all.

## 10. How The Demo Forces The Torn Read

How does the demo force the torn read, every time? Nothing is left to luck. The writer sets the new amount. It signals, through a latch, that it has done so. Then it waits at a gate, before setting the currency. The main thread waits for that signal, reads the price, and only then opens the gate. So the read is proven to land in the gap, on every run. No sleeping, and no hoping.

## 11. What The Scheduler Really Does

A quick, honest note about this demo. Every result was made repeatable by pinning one fact on purpose. A writer is waiting. A gap is open. The timings are real measurements, and they change from machine to machine. What stays the same is the ranking. For a read this cheap, the plain lock and the snapshot both beat the read-write lock. A passing test proves the forced scene, not safety under every possible timing.

## 12. The Bill

Here are the costs, all in one place. A waiting writer can be overtaken, so nothing limits its wait. Upgrading from a read lock to a write lock deadlocks the thread that tries it. And for a very cheap read, the lock's own bookkeeping can cost more than a plain lock.

## 13. When To Use It, And When Not

So, when is this pattern worth it? When there are many readers, few writers, and each read takes real time. Such as searching a large catalogue held in memory. Then letting readers overlap is worth the bookkeeping. Not for a tiny read, like this price. There, use a plain lock. Or better, an unchangeable snapshot, swapped in one step.

## 14. Thanks for Watching

That's the Read-Write Lock pattern. If you remember one sentence, make it this one. Letting readers share a lock is only worth it when each read is expensive enough to pay for the lock's own bookkeeping. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make the price read slower, by doing real work inside it. Then measure which of the three approaches wins. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
