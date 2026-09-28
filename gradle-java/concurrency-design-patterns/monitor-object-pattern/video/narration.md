# Monitor Object Pattern — Video Narration Script

## 1. Monitor Object

Hello, and welcome. This video explains the Monitor Object pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A monitor object owns its own lock, and its own waiting. So every one of its methods runs safely, and no caller can forget to be careful. Think of a shop with one fitting room, and an attendant at the door. Customers never lock the door themselves. The attendant lets one person in at a time. In our online store, many threads change the stock count of a product. By the end, you will know why volatile does not stop a lost update. Why a lock held by the caller is weaker than a lock the object owns. Why waiting must sit in a loop. And how a correct monitor can still deadlock.

## 2. The Scenario

Here is the scenario. An online store keeps one number for each product: how many are in stock. Many checkout threads reduce that number, one sale at a time. A delivery thread adds to it when new stock arrives. And a checkout that wants three items, when only two are left, should wait for the delivery, not simply fail.

## 3. A Plain Count — The Lost Update

First demo: a plain number. Selling one item takes three steps. Read the count, subtract one, and write the answer back. Two checkout threads both read ten. Both subtract one. Both write nine. Two items left the shelf, but the count says only one did. That is called a lost update. And this demo makes it happen every time.

## 4. volatile — Still Not Atomic

A popular half-fix is the keyword volatile. Surely that helps? It does not. Both threads still read ten, and both still write nine. Volatile promises that when one thread writes, other threads will see it. That is called visibility. It does not promise that read, subtract, and write happen as one step. That is called atomicity, and it is a different promise.

## 5. The Caller Holds The Lock

Next idea: put a lock next to the count, and ask every caller to take it first. In this demo, one checkout thread takes the lock, and sells. Another checkout thread forgets the lock, and sells anyway. Both read ten, and both write nine. Four careful callers protect nothing, if a fifth one forgets. A rule that every caller must remember will eventually be broken.

## 6. The Pattern — The Object Owns Its Lock

The pattern moves the responsibility. The lock becomes a private field, inside the stock object. Every public method takes that lock itself, does its work, and lets go. A caller cannot forget, because a caller never touches the lock. There is no way in, except the safe way. Waiting is private too. In Java, that means a private Reentrant Lock, and a private Condition.

## 7. Waiting And Signalling

Now the pattern, running. Eight checkout threads each sell twenty-five thousand items, from a stock of two hundred thousand. The final count is zero. Not one update was lost. Waiting happens inside the object too. A thread asks for three items, but there are none. So it waits on the object's own condition, and lets go of the lock while it waits. Then a delivery thread adds three items, and sends a signal. The waiting thread wakes, takes the lock again, and takes its three items. It never kept checking, and it never guessed how long to sleep.

## 8. Cost One — wait In A Loop

Now the costs. The first: waiting must sit inside a loop. Two threads are waiting, for one item each. One item is added, and both are woken. If the code checks with a single if statement, both carry on. One item, two sales, and the count ends at minus one. With a while loop, the second thread checks again, sees the item is gone, and goes back to waiting. Being woken means stock might be there. It does not mean stock is there.

## 9. Cost Two — Nested Monitors

The second cost: two monitors can deadlock. One thread moves stock from monitor A to monitor B. It holds A, and asks for B. At the same moment, another thread moves stock from B to A. It holds B, and asks for A. Each holds what the other needs. Both wait forever. Java detects it, and this demo breaks it by interrupting both threads. Real code has no such rescue.

## 10. Cost Three — Calling Out

The third cost: calling out while holding the lock. Suppose the monitor, while holding its lock, calls some outside code, like a listener. That listener asks another thread to read the stock, and waits for the answer. But that other thread needs the lock. And the monitor is holding the lock, while it waits for the listener. Nobody can move. This demo gives up after about two hundred milliseconds. The rule: never call code you do not own, while holding your lock.

## 11. How The Demo Forces The Race

How does the demo make these failures happen reliably? Nothing is left to luck. The plain stock accepts a hook that runs between reading and writing. The demo plugs in a meeting point, which releases neither thread until both have arrived. So both threads have read ten, before either one writes nine. For the two waiting threads, the demo checks that both are really waiting, before it adds the item. No sleeping, and no hoping.

## 12. What The Scheduler Really Does

A quick, honest note about this demo. Each failure was made repeatable by pinning one fact on purpose. Both threads have read. Both are waiting. Both hold a lock. Java still decides everything else, such as which woken thread runs first. The timing numbers are real measurements, and they vary by machine. A passing test proves the forced scene, not safety under every possible timing.

## 13. The Bill, And When It Is Too Much

Here are the costs, all in one place. The lock is a bottleneck by design, because only one thread can be inside at a time. Waiting needs a loop. Two monitors can deadlock. And calling out while holding the lock can deadlock too. So when is it too much? For a single counter, an Atomic Integer is simpler, and faster. A monitor earns its place when several fields must change together, or when threads must wait for a condition.

## 14. Thanks for Watching

That's the Monitor Object pattern. If you remember one sentence, make it this one. A lock that callers must remember will eventually be forgotten, so let the object own it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Fix the nested monitors, by always locking them in the same order. Then run it, and listen for the deadlock to disappear. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
