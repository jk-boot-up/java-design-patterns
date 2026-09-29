# Lock-Free Compare-and-Swap Pattern — Video Narration Script

## 1. Lock-Free Compare-and-Swap

Hello, and welcome. This video explains the Lock-Free Compare-and-Swap pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Compare-and-swap changes a shared value only if it still holds what you saw. If someone else changed it first, you read it again, and try again. Nobody ever waits for a lock. Think of booking a concert seat online. You pick seat twelve on the map. When you press book, it is booked only if seat twelve is still free. If someone beat you to it, you look at the map again, and pick another. In this video, the domain is an online shop's flash sale. A hundred kettles, and eight buyer threads racing to buy them. By the end, you will hear how a shop sells more kettles than it has. How a lock fixes it, slowly. How compare-and-swap fixes it without a lock. And its limits.

## 2. The Scenario

Here is the scenario. A flash sale: a hundred kettles. Eight buyer threads, each trying to buy fifty. To buy one, a thread reads the stock count, runs a quick fraud check, and then writes back the count, minus one.

## 3. Act One — Check, then act

First demo: check, then act, with no protection. A hundred kettles. Eight buyer threads, each trying fifty times. Each buyer reads the stock count, runs a quick fraud check, then writes back the count, minus one. Two buyers read the same count at the same moment. Both take the same kettle. The shop sells more than a hundred kettles, from a stock of a hundred.

## 4. Act Two — A lock

Second demo: a lock, one buyer at a time. Only the buyer holding the lock may look at the stock and take a kettle. Exactly a hundred kettles sold. None left. Correct. But every other buyer waits in line while one checks.

## 5. Act Three — Compare-and-swap

Third demo: compare-and-swap. Each buyer reads the count, and runs the fraud check. Then it says: take one, but only if the count is still what I saw. The processor does that in one indivisible step. If another buyer got there first, the swap fails. The buyer simply reads the count again, and retries. Exactly a hundred sold. None left. And no thread ever waited for a lock.

## 6. Act Four — The loop in one call

Fourth demo: the loop in one call. Java's atomic integer has a method, get and update. You give it a rule: if there is stock, take one. It runs the compare-and-swap, and retries it for you. A hundred sold. None left.

## 7. Act Five — The bill

Fifth demo: the bill. Compare-and-swap protects one value at a time. A buyer takes a kettle. Then its thread stops, before it records who bought it. Stock says ninety-nine. Buyers recorded: zero. Two atomic values are not one atomic change. And when many threads fight over one value, they keep retrying, instead of waiting quietly.

## 8. The Pattern

Let's name the pattern. Read the value. Work out the new value. Then swap it in, but only if the value is still what you read. The processor does that check and change as one indivisible step. If the swap fails, someone else changed it. Read again, and retry.

## 9. Who Does What

Here is who does what. An atomic integer holds the shared stock count. Compare and set is the indivisible step: swap if unchanged. CAS stock runs the retry loop. And unsafe stock and locked stock are the alternatives, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Java's atomic integer, atomic long, and atomic reference. And the concurrent hash map, which is built on them. Databases do the same with a version column: update the row, only if its version is still seven. And git refuses your push if the branch moved since you last pulled.

## 11. When To Use It

So, when should you use it? For one shared value at a time: counters, stock levels, flags, references. Prefer update and get, rather than writing your own loop. For very busy counters, use long adder. And when several values must change together, use a lock, or a database transaction.

## 12. Thanks for Watching

That's the Lock-Free Compare-and-Swap pattern. If you remember one sentence, make it this one. Change it only if it has not changed, and if it has, look again. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Count the retries with two, eight, and thirty-two buyers, and see how they grow. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
