# Proactor Pattern — Video Narration Script

## 1. Proactor

Hello, and welcome. This video explains the Proactor pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. In a proactor, you start slow operations without waiting for them. With each one, you hand over a completion handler: what to do when it finishes, and what to do if it fails. The system does the waiting, and calls you back. Think of a food court with a buzzer at every stall. You order at five stalls, and each gives you a buzzer. You sit down. As each buzzer goes off, you collect that dish. In this video, the domain is an online shop's warehouse. Before ordering kettles, it asks five suppliers for today's price, and each takes a fifth of a second to answer. By the end, you will hear why asking one after another is slow. How a proactor overlaps the waits. How failures are reported. And what it costs.

## 2. The Scenario

Here is the scenario. The warehouse buys kettles from five suppliers. Before each order, it asks all five: what is today's price? Then it picks the cheapest. Each supplier takes a fifth of a second to answer. And the warehouse asked them one after another.

## 3. Act One — One after another

First demo: ask five suppliers for a kettle price, one after another. Each supplier takes a fifth of a second to answer. The warehouse asks the first, and waits. Then the second, and waits. And so on. Five prices take nearly a second. And the asking thread does nothing else, the whole time.

## 4. Act Two — Start everything at once

Second demo: a proactor. The warehouse starts all five requests at once. For each, it hands over a completion handler: what to do when that request finishes. It does not wait. All five are started, and the method returns, in under a tenth of a second. The system does the waiting. The five waits overlap. All five answers arrive in under six tenths of a second.

## 5. Act Three — Completion handlers

Third demo: completion handlers receive the results. When a connection is made, one handler sends the question. When the question is sent, another starts reading. When the answer arrives, a third records the price. Twenty-one pounds. Nineteen fifty. Twenty-two forty. Eighteen ninety. Twenty ten. The cheapest is eighteen pounds ninety.

## 6. Act Four — A failure is a completion

Fourth demo: a failure arrives as a completion too. A sixth supplier's server is down. Its request cannot connect. So the system calls that request's failed handler, instead of its completed handler. The failure is recorded. The other two suppliers answer as normal. Like a buzzer that goes off to say: sorry, sold out.

## 7. Act Five — The bill

Fifth demo: the bill. One request is now spread across three handlers. Connected. Written. Read. The steps no longer read top to bottom in one method. And when something goes wrong, the error starts in the system's thread, not in the code that asked.

## 8. The Pattern

Let's name the pattern. Start the operation, and do not wait for it. Hand over a completion handler, with two methods. Completed, for when it succeeds. Failed, for when it does not. The system does the waiting, and calls the right one when the operation is done.

## 9. Who Does What

Here is who does what. Proactor quotes starts every request, and returns at once. Java's asynchronous channels do the waiting. Connected, written, and read are the completion handlers, one for each step. Supplier is a slow price server. And blocking quotes is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Java's asynchronous socket and file channels take completion handlers. The HTTP client's send async, and completable futures, are friendlier faces of the same idea. And Node.js file and network calls take callbacks.

## 11. When To Use It

So, when should you use it? When many slow operations can overlap. Keep handlers short, and collect their results safely, because they run on other threads. And when readable, top-to-bottom code matters more, Java's virtual threads let blocking code wait just as cheaply.

## 12. Thanks for Watching

That's the Proactor pattern. If you remember one sentence, make it this one. Start everything, wait for nothing, and let each result call you back. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a timeout, so a supplier slower than half a second counts as failed. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
