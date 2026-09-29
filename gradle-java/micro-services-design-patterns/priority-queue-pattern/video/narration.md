# Priority Queue Pattern — Video Narration Script

## 1. Priority Queue

Hello, and welcome. This video explains the Priority Queue pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. In a priority queue, urgent messages overtake routine ones. However long the routine ones have been waiting. And a share of capacity is kept, so routine work still gets done. Think of the fast-track lane at airport security. Passengers with a tight connection skip the long queue. But at least one officer stays on the ordinary lane. And if every ticket came with fast track, the fast lane would just be another queue. In this video, the domain is an online shop's warehouse. Pickers work through the orders, and same-day orders must catch the courier's van. By the end, you will hear how same-day orders missed the van. How a priority queue fixes it. How to stop routine work being starved. And what happens when everything is urgent.

## 2. The Scenario

Here is the scenario. The warehouse pickers work through a queue of orders, ten a minute. Same-day orders must be picked before the courier's van leaves, at five past nine. The queue was first come, first served.

## 3. Act One — First come, first served

First demo: one queue, first come, first served. The pickers do ten orders a minute. At nine o'clock, a hundred standard orders arrive. At one minute past, five same-day orders. The van leaves at five past. The same-day orders wait behind all hundred. The last one is picked at ten past nine. The van has gone.

## 4. Act Two — A priority queue

Second demo: a priority queue. Same-day orders now go first. Then, oldest first. All five same-day orders are picked by one minute past nine. In time for the van. The standard orders carry on straight after.

## 5. Act Three — A flood of standard orders

Third demo: a flood of standard orders makes no difference. This time, a thousand standard orders arrive first. The same-day orders overtake all of them. Still picked by one minute past nine.

## 6. Act Four — Starvation, and a reserved share

Fourth demo: too many urgent orders starve the rest. Twelve same-day orders arrive every minute. The pickers can do ten. With strict priority, standard orders are never picked. Zero of twenty, in ten minutes. Now keep two picks a minute for the oldest standard orders. All twenty are picked.

## 7. Act Five — The bill

Fifth demo: the bill. If everything is urgent, nothing is. Marketplace sellers learn that same-day jumps the queue. So they mark every order same-day. Priorities need rules about who may set them. And more queues, and settings, to watch.

## 8. The Pattern

Let's name the pattern. Each message carries a priority. Workers take the highest priority first. Within the same priority, the oldest first. And keep a share of capacity for routine work, so it is never starved.

## 9. Who Does What

Here is who does what. An order knows whether it is same-day, and when it arrived. The priority queue orders same-day first, then oldest. The run method is the pickers: ten a minute, with an optional share kept for standard orders. And the first-in, first-out queue is the old way.

## 10. Where You Have Seen It

You have probably met this pattern already. Java has a priority queue class. RabbitMQ supports priorities on queues. And many systems run separate high and low priority queues. Hospital triage and airport fast-track lanes work the same way.

## 11. When To Use It

So, when should you use it? When some work has a real, earlier deadline than the rest. Order by priority, then by age. Reserve a share for routine work. And control who is allowed to mark work as urgent.

## 12. Thanks for Watching

That's the Priority Queue pattern. If you remember one sentence, make it this one. Let urgent work go first, but never let routine work wait for ever. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Promote standard orders that have waited more than fifteen minutes. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
