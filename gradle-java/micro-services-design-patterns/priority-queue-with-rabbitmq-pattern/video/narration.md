# Priority Queue with RabbitMQ Pattern — Video Narration Script

## 1. Priority Queue with RabbitMQ

Hello, and welcome. This video explains the Priority Queue pattern, with a real RabbitMQ broker, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. In a priority queue, urgent messages overtake routine ones. However long the routine ones have been waiting. RabbitMQ is an open-source message broker, and it can make a queue a priority queue. Think of the fast-track lane at airport security. Passengers with a tight connection skip the queue. But nobody can overtake someone already in the scanner. In this video, the domain is an online shop's warehouse, where same-day orders must catch the courier's van. By the end, you will hear how RabbitMQ puts same-day orders first. Why a setting called prefetch can undo it. And why routine orders need a share kept for them.

## 2. The Scenario

Here is the scenario. The warehouse pickers take ten orders a minute, from a queue. Same-day orders must be picked before the van leaves, at five past nine. On a busy morning, a hundred standard orders came first.

## 3. Act One — First in, first out

First demo: an ordinary queue, first in, first out. A hundred standard orders arrive, then five same-day orders. The pickers take ten a minute, from nine o'clock. The last same-day order is picked at eleven minutes past. The van left at five past.

## 4. Act Two — A priority queue

Second demo: a RabbitMQ priority queue. The queue is declared with priorities from zero to ten. Same-day orders are sent with priority nine. RabbitMQ hands out the highest priority first. All five same-day orders are picked by one minute past nine.

## 5. Act Three — A flood

Third demo: a flood of standard orders. A thousand standard orders are waiting first. The same-day orders overtake them all. Still picked by one minute past nine.

## 6. Act Four — Only what is still waiting

Fourth demo: priority only reorders what is still waiting. A picker's handheld subscribes with no limit. RabbitMQ pushes all hundred standard orders to it, at once. Then the same-day orders arrive. They join the back of the handheld. Positions one hundred and one, to one hundred and five. With a prefetch of one, only one order sits in the handheld. And the next one handed out is same-day.

## 7. Act Five — The bill: starvation

Fifth demo: the bill. Twelve same-day orders arrive every minute. The pickers can do ten. With strict priority, standard orders are never picked. Zero of twenty, in ten minutes. RabbitMQ keeps no share for routine work. So the shop builds one. Standard orders on their own queue, with two picks a minute kept for them. All twenty are picked.

## 8. The Pattern, in RabbitMQ

Let's name the pattern, in RabbitMQ's words. Declare the queue with a maximum priority. Send each message with its priority. And keep the prefetch small, so messages stay on the queue, where priority can reorder them.

## 9. Who Does What

Here is who does what. The warehouse class declares the queues, places orders, and picks ten a minute. The broker class runs RabbitMQ in a container. And poll waits for real conditions.

## 10. Where You Have Seen It

You have probably met this already. RabbitMQ's priority queues. Separate high and low priority queues, on cloud services. And hospital triage, and airport fast-track lanes.

## 11. When To Use It

So, when should you use it? When some work has a real, earlier deadline. Keep prefetch small. Use few priority levels. And build a reserved share for routine work yourself.

## 12. Thanks for Watching

That's the Priority Queue, with RabbitMQ. If you remember one sentence, make it this one. Urgent first, but only for what is still waiting, and never at the cost of everything else. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It needs Docker running, and starts the broker for you. Here is one exercise to try. Try a prefetch of ten, and find where the same-day orders land. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
