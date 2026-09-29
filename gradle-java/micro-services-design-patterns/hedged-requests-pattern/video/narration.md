# Hedged Requests Pattern — Video Narration Script

## 1. Hedged Requests

Hello, and welcome. This video explains the Hedged Requests pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. If a call has not answered after a short wait, send the same call to a second copy of the service. Use whichever answer comes first. And cancel the other. Think of phoning a shop to ask if something is in stock. Nobody picks up after a few rings. So you call their other branch too. Whichever answers first gets your question, and you hang up on the other. In this video, the domain is an online shop's product page. It asks a price service for each price. And there are several copies of that service, called replicas. By the end, you will hear why the average hides slow calls. How a second call after fifty milliseconds fixes them. Why not to send two calls every time. And which calls must never be hedged.

## 2. The Scenario

Here is the scenario. The product page asks the price service for each price. Most answers take twenty milliseconds. But now and then a replica pauses, for example to clean up memory. About one call in thirty-three then takes a whole second.

## 3. Act One — One call, and a slow tail

First demo: one call per price. We look up a thousand prices. Half the answers take twenty milliseconds or less. But about one call in thirty-three lands on a paused replica. That call takes a whole second. So the slowest one percent of calls take a full second. And the product page waits for them.

## 4. Act Two — Hedge after 50 ms

Second demo: hedge after fifty milliseconds. Fifty milliseconds is longer than a normal call ever takes. If there is no answer by then, the client asks a second replica. Whichever answers first, wins. The slowest calls now take seventy milliseconds. Fifty waiting, and twenty for the backup. And only three percent of calls needed a second call.

## 5. Act Three — Hedge at once

Third demo: why wait at all? Send every request to two replicas at once. Now the slowest calls take only twenty milliseconds. But every request is sent twice. The price service does double the work. Twice the load, to save fifty milliseconds on a few calls. Waiting first is the better deal.

## 6. Act Four — A real race

Fourth demo: a real race, with real threads. Replica A is paused. It would take a whole second. Replica B answers in twenty milliseconds. The hedger asks A, and waits fifty milliseconds. No answer, so it asks B too. B's answer comes back in well under half a second. Then the hedger cancels the call to A. So A stops working on an answer nobody needs.

## 7. Act Five — The bill

Fifth demo: the bill. Hedging sends the same request twice. So only hedge calls that are safe to repeat. Reading a price, is fine. Placing an order, is not. The customer could be charged twice. And if every replica is slow because they are all overloaded, extra calls make things worse. So keep hedges to a few percent of requests.

## 8. The Pattern

Let's name the pattern. Call one replica. If there is no answer after a short delay, call a second replica with the same request. The first answer wins. And the other call is cancelled.

## 9. Who Does What

Here is who does what. A replica is one copy of the price service. The hedger makes the call. It waits fifty milliseconds, asks a second replica if needed, takes the first answer, and cancels the other. And the latency model measures a thousand calls, so we can compare the slowest ones.

## 10. Where You Have Seen It

You have probably met this pattern already. Google made it famous, in a paper called The Tail at Scale. gRPC can hedge calls, with a setting per method. And Cassandra calls it speculative retry. In Java, racing futures with any-of is the same idea.

## 11. When To Use It

So, when should you use it? When a service has several replicas, and slow calls are rare. Only hedge calls that are safe to repeat. Wait a little before hedging. Cancel the loser. And cap how many hedges you send.

## 12. Thanks for Watching

That's the Hedged Requests pattern. If you remember one sentence, make it this one. When one copy is slow, ask another, and keep the first answer. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a budget, so hedges stop once they reach five percent of calls. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
