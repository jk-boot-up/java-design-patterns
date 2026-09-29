# Hedged Requests with gRPC Pattern — Video Narration Script

## 1. Hedged Requests with gRPC

Hello, and welcome. This video explains the Hedged Requests pattern, with gRPC, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. If a call has not answered after a short wait, send the same call again. Use whichever answer comes first, and cancel the other. gRPC is an open-source framework for calling other services, and it can hedge for you, as a setting. Think of phoning two branches of a shop. Ring one. If nobody answers after a few rings, ring the other, and hang up on the first. In this video, the domain is an online shop's product page, asking a price service for each price. By the end, you will hear how one setting cuts the slow calls. How gRPC cancels the loser. And why an order must never be hedged.

## 2. The Scenario

Here is the scenario. The product page asks the price service for each price, over gRPC. Most answers take twenty milliseconds. But about one call in thirty-three lands on a paused worker, and takes a whole second.

## 3. Act One — A slow tail

First demo: one call per price, and a slow tail. The product page looks up a hundred prices, over gRPC. Three of them take about a second. The rest, about twenty milliseconds. So the slowest pages wait a whole second.

## 4. Act Two — A hedging policy

Second demo: gRPC's hedging policy. The channel gets one setting. If no answer after fifty milliseconds, send a second attempt. The shop's code does not change at all. Now none of the hundred lookups is slow. And gRPC sent just three extra calls.

## 5. Act Three — The loser is cancelled

Third demo: the loser is cancelled. When the second attempt answers first, gRPC cancels the first. The server can see it. The three slow attempts find their call cancelled. They never reply.

## 6. Act Four — Hedge at once

Fourth demo: hedge at once, with a delay of zero. Every lookup is sent twice, immediately. A hundred lookups, two hundred calls. Twice the load on the price service.

## 7. Act Five — The bill

Fifth demo: the bill. The same policy is applied, by mistake, to placing orders. The customer sees one confirmation. The server placed two orders. Hedge only reads. And cap hedging, so an overloaded service is not sent even more.

## 8. The Pattern, in gRPC

Let's name the pattern, in gRPC's words. A hedging policy, in the channel's service config. Up to two attempts. The second after fifty milliseconds. And applied only to methods that are safe to repeat.

## 9. Who Does What

Here is who does what. Channels builds a plain gRPC channel, or one with the hedging policy. The price server answers, and is sometimes slow. And shop describes the two methods, price and place order.

## 10. Where You Have Seen It

You have probably met this already. gRPC's hedging and retry policies. Cassandra's speculative retry. And service meshes such as Envoy, which can hedge too.

## 11. When To Use It

So, when should you use it? For cheap reads that are safe to repeat, with a rare slow outlier. Scope the policy to those methods. Choose a delay near the normal worst case. And add throttling.

## 12. Thanks for Watching

That's Hedged Requests, with gRPC. If you remember one sentence, make it this one. Let the framework ask twice, but only for questions that are safe to ask twice. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add retry throttling, and make the server slow for every call. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
