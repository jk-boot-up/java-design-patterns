# Bulkhead Pattern — Video Narration Script

## 1. Bulkhead

Hello, and welcome. This video explains the Bulkhead pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Stop letting every kind of work draw from the same pot of resources. Give the work that must never fail a pot of its own. Then one slow job can fill up its own pot, but it cannot take what the important work needs. The name comes from shipbuilding. A bulkhead is a wall that divides a ship's hull into separate watertight compartments. A hole floods one compartment, not the whole ship. In our online store, there are two jobs. Taking a shopper's money. And importing a supplier's catalogue overnight. By the end, you will know how a background job that nobody is waiting for can stop the shop selling. Why a bigger pool does not help. And what the wall costs you, on every day that nothing goes wrong.

## 2. The Scenario

Here is the scenario. The shop runs as one application, with one pool of threads. A thread is a worker that runs one job at a time. Every job asks the pool for a thread, does its work, and gives the thread back. Showing a product page, taking a payment, sending an email. All from the same pool. That is a completely normal design, and for a long time it is the right one. Two of those jobs matter here. The first is checkout. It takes a shopper's money. It is fast, it is correct, and it needs exactly one thing: a thread. The second is the supplier feed. It imports the supplier's catalogue overnight. Nobody is waiting for it. And it calls a partner service which is, sometimes, very slow. In the code, these two jobs have nothing to do with each other. Keep that in mind.

## 3. One Pool, Shared By Everything

Here is the setup. One pool, with four threads. Four import batches are handed to it, one after another. Then a shopper arrives, and the payment is handed to the same pool. To be fair to this code, there is no bug in it. Every test passes. Almost every service starts this way. And in a code review, nobody would say a word. Tonight, the partner service that the feed calls has gone slow. Not failing. Answering, but slowly. Let's run it.

## 4. Act One — One Shared Pool Of Four

Everything follows from one small fact. A job that is waiting still holds its thread. It uses no processor time, and does nothing. But the thread stays with it, until its call comes back. So, the first import batch starts, and takes a thread. The second takes a thread. The third. The fourth. Four batches, four threads, and the pool only has four. Now the shopper tries to pay. There is no thread free. After three hundred milliseconds, they are still waiting, and the sale is lost. And here is the strange part. There is no line for checkout in the output at all. Not a slow line, and not an error. Checkout never started.

## 5. Starved, Not Broken

It would be easier if checkout were broken, because then there would be something to fix. But it is not broken. A test in this project runs the same checkout job the moment a thread is free, and it works perfectly. It was starved, not broken. And from the outside, those two look exactly the same. That is why this is so hard to find at three in the morning. You are looking for a bug in a class that does not have one. So here is the key sentence. The shop stopped selling because of a background job that nobody was waiting for. And the link between them is invisible. Checkout never mentions the feed. The feed never mentions checkout. They are tied together only by the pool they share. So reading either file will never show you the problem.

## 6. The Ship's Hull

Let's leave the code for a moment, and think about a ship. A bulkhead is a wall that divides a ship's hull into watertight compartments. Make a hole in a hull with no walls, and the water spreads along the whole ship, and it sinks. Make the same hole in a divided hull, and only one compartment floods. The ship sits a little lower, and keeps going. There are two lessons here. First, the hole did not change. Just as much water came in. The wall only limits how far it spreads. Second, the walls take up space. One compartment can be empty while the next one is full. And you cannot move space from one to the other. That is not a flaw. That is the design. Isolation is paid for in capacity you are not allowed to use. Hold on to that, because we will come back to it.

## 7. Two Tempting Fixes, Both Wrong

Before the real fix, here are two tempting fixes. Both are wrong. The first is: make the pool bigger. Forty threads, instead of four. That only buys time. If the partner is slow for long enough, the feed takes all forty threads. And checkout is starved at forty, just as it was at four. The number changed. The failure did not. Worse, a bigger pool takes longer to notice, and uses more memory when it finally fills up. The second is: never refuse a job. Let every job wait in a queue with no limit. That sounds generous, but it is more dangerous. It turns a fast, visible failure into a slow, invisible one. Jobs pile up until the program runs out of memory. And every caller waits for work that will not start for minutes. So neither fix works. The two jobs are only connected by the pool they share. So what if they stop sharing it?

## 8. The Whole Mechanism

Here is the whole mechanism, and it is very plain. A pool with a fixed number of threads. A queue that holds a fixed number of waiting jobs. And a name, which every thread in the pool carries. That is all. No clever algorithm. Nothing that adapts to load. Nothing to tune while it runs. So a bulkhead is not clever machinery. It is a decision to stop sharing. The pattern is not in this class. It is in having two of them. The hard part is deciding where the walls go. And that is a business decision, not a coding one. For now, the feed gets two threads of its own. Checkout gets two threads of its own. And we give them exactly the same bad night.

## 9. Act Two — Two Bulkheads

Same slow partner. Same four batches. Same moment. Two batches start. The other two wait in the feed's queue for a feed thread. On the feed side, nothing has improved. Then the shopper arrives, gets a thread straight away, and pays. The sale goes through in milliseconds. The names of the threads tell the whole story. The import batches run on threads called feed worker. The payment runs on a thread called checkout worker. They come from different pools. The feed cannot borrow from checkout. And checkout is not allowed to help the feed. That is the whole pattern, and it just saved a sale.

## 10. Who Owns What

Let's name the pieces. There are only a few, and each has one job. A bulkhead is a named pool of threads, with a limit, that one kind of work may use. Underneath, it is a fixed thread pool with a limited queue. When all its threads are busy and its queue is full, it refuses at once. And the error says which bulkhead was full. Not that the system is busy, but which pool ran out. Then there is the work. Checkout, which must never be starved. And the supplier feed, which nobody is waiting for, and which holds its thread the whole time it waits. Those two facts are the most important in the system. And they appear nowhere in the code. They come from the people who run the shop. If nobody writes them down, as a pool and a thread count, then in an outage they are decided by whichever job asked for a thread first. One more piece. The slow partner is not a real network call, and nothing in this project sleeps. It is a gate that a job waits at, until the test opens it. A job waiting at a closed gate holds its thread, just like a job waiting on a slow network.

## 11. How Do We Know It Was The Wall?

Before we celebrate, here is a fair question. Checkout worked. But how do we know the wall did that? Suppose the partner service had started answering again, just before the shopper arrived. The output would look exactly the same. We would have proved nothing. So one test checks that the feed is still jammed at the very moment the sale goes through. Two threads busy, and two jobs waiting. Nothing about the partner was fixed. The slow thing is still slow, and the shop is selling anyway. This lesson works far beyond thread pools. A test that only checks the good thing happened has not ruled out that it happened by luck.

## 12. Act Three — A Fifth Batch, With Nowhere To Go

The feed's bulkhead has two threads, and a queue that holds two. So four batches fit. Now a fifth batch arrives. It is refused, and the refusal takes zero milliseconds. That can feel unfriendly, but it is the opposite. The speed is the whole point. The caller finds out at once, while it still has time to do something useful. Drop the batch, do less, or try again later. It is the same idea as a circuit breaker failing fast, but applied to a queue. Now compare it with a queue that has no limit. That queue would have accepted this batch, and the next one, and every one after that. Nobody would be told anything, until the program ran out of memory instead of threads. Refusing is a feature.

## 13. Refusing Immediately Is A Feature

That refusal gives you three things, not just speed. First, the error names the pool that is full. Not, the system is busy. But, the feed's pool is full. One of those tells an engineer where to look. Second, the caller is told in a millisecond, so it still has choices. It can drop the work, do a smaller version, or save it for later. A caller that is simply kept waiting has no choices at all. Third, the size of the damage was decided in advance, calmly, in daylight. Not by chance, in the middle of an incident. The failure has not gone away. The partner is no faster. What changed is that you chose the shape of the failure, ahead of time.

## 14. Act Four — What The Partition Costs

Now the bill. Any honest explanation of this pattern has to include it. On a quiet afternoon, the divided shop looks like this. The feed has two threads busy, and two more jobs waiting. And checkout has two threads doing nothing at all. Two threads are idle, while two jobs wait for a thread. And they are not allowed to help. One shared pool of four would have run all four batches at once, and finished sooner. A test in this project checks exactly that. On a good day, the shared pool really is faster. So divided pools leave capacity idle, on purpose. That is not a bug, or a tuning problem. It is the price of the isolation. It is the ship again. The empty compartment cannot lend its space to the full one.

## 15. So Where Do The Walls Go?

So where should the walls go? The trade is worth it for work whose failure ends the business. In a shop, that is taking money. It is not worth it for everything. Fifteen bulkheads means fifteen pools to size. Fifteen numbers that go out of date as traffic changes. And a lot of threads doing nothing in the afternoon. A good rule is two or three pools, divided by what must survive. Not by how the code is organised into packages, even though that looks tidy. And remember, this is a business decision. Nobody can tell from the code that the supplier feed matters less than checkout. One last point. A bulkhead stops the damage spreading. It does not stop you calling a service that has stopped answering. That is the job of a circuit breaker. The two belong together. A breaker, so you stop calling a service that is down. And a bulkhead, so the calls already waiting cannot drown anything that matters.

## 16. Thanks for Watching

That's the Bulkhead pattern. If you remember one sentence, make it this one. A bulkhead gives the work that must survive a pool of its own, and pays for that safety with capacity left idle on purpose. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. It uses real threads, but nothing sleeps, so all the tests run in about a second. Here is one exercise to try. Give checkout's bulkhead one thread instead of two. Then put two sales through it while the feed is jammed. The second sale waits. The wall protects checkout from the feed, but not from checkout itself. And one question to think about. In your own system, which work must never be starved? And what are you willing to leave idle, to guarantee it? If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
