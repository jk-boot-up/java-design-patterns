# Queue-Based Load Leveling with SQS Pattern — Video Narration Script

## 1. Queue-Based Load Leveling with SQS

Hello, and welcome. This video explains the Queue-Based Load Leveling pattern in Java, using a real Amazon queue, running on your own machine. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. When work arrives in bursts, faster than a service can handle it, you put a queue in between. The burst waits in line, and the service keeps its own steady pace. It works like a post office the day before a holiday. A crowd arrives at once, a machine at the door hands out numbered tickets, and the clerk serves one person after another, never rushed. Now the same thing in our online store. A sale sends a hundred orders in the same moment. Checkout puts every order on a queue and tells the customer at once that the order is received. The packing service takes orders off the queue at its own pace, ten at a time. By the end you will have seen the depth a real burst builds, an order that is taken but not removed, a slow packer that packs one order twice, a packer that stops and loses nothing, and the bill for all of it.

## 2. The Scenario

Here is the scenario. The shop runs a sale, and in its first second a hundred orders arrive at once. The packing service picks the items and packs the parcels, and it can do ten orders a round, however many are waiting. So checkout does not call the packing service directly. It puts each order on a queue, a waiting line for work, and tells the customer straight away that the order is received. The hand-built partner project in this course kept its queue in memory, with a clock it made up for itself. This time the queue is Amazon's queue service, and the rules it plays by are Amazon's rules.

## 3. A Burst Lands On The Queue

First, the burst. The queue service is called S Q S, short for Simple Queue Service. A hundred orders arrive at once, and checkout sends them to S Q S. It tries eleven orders in one request, and S Q S refuses, in its own words: the maximum number of entries per request is ten. That is not a rule this program made up. It is the service saying no. So the burst goes as ten requests of ten. S Q S now reports a hundred orders waiting, and none in flight. Nobody was refused. And S Q S will keep an order that nobody takes for three hundred and forty five thousand, six hundred seconds. That is four days.

## 4. The Service's Words

The real service brings a few words with it, and each one is simpler than it sounds. An order that nobody has taken yet is waiting. The number of waiting orders is the depth of the queue. When a packer takes an order, S Q S does not remove it. It hides it from everyone else, until the packer says it is finished by deleting it. An order that is taken but not yet deleted is what S Q S calls in flight. And how long S Q S hides a taken order, before it gives up waiting and hands it out again, is what S Q S calls the visibility timeout. None of this is on Amazon here. A program called LocalStack answers exactly as S Q S would, in one small sealed box on this machine, called a container. The demo switches it on at the start and off at the end.

## 5. The Packer Keeps Its Own Pace

Second, the packer. It asks S Q S for eleven orders at once, and S Q S refuses again: it hands out between one and ten. So it takes ten. And for a moment S Q S reports ninety waiting, and ten in flight. Those ten are neither on the line nor gone. They are taken, and hidden, and not yet finished. The packer packs the ten parcels, and only then deletes them. Round after round, the depth falls by ten: ninety, eighty, seventy, and so on, down to zero. A hundred orders packed in ten rounds, and the packer never did more than ten at once. That is the pattern working.

## 6. Where The Orders Live

Here is the whole picture in words. There are four parts, in order. Checkout comes first: it sends the burst to the queue, ten orders to a request. The S Q S queue is second: it counts the orders waiting and the orders in flight, and it lives in neither checkout nor the packers. The packer is third: it takes up to ten, packs them, and then deletes them. A second packer is last: it is handed any order whose timeout ran out. The one rule that holds it together is the order of the last two steps. Pack first, and delete only after the parcel is packed.

## 7. Taken Is Not Removed

Third, the heart of it. S Q S hides a taken order for thirty seconds, unless you choose a different time. This queue hides it for two seconds. A packer takes order two thousand and one, and stops before it finishes. It never deletes it. S Q S reports no orders waiting, and one in flight. A second packer asks at once, and is given nothing. The second packer keeps asking. Once the two seconds have passed, order two thousand and one comes back, and S Q S says it has now handed it out two times. S Q S never knew the first packer had stopped. It only knew the time had run out.

## 8. Why Hide, And Not Remove?

Why does S Q S hide an order, instead of removing it? Think of a coat check. An attendant lifts a coat to fetch it, and drapes a cloth over its hook. If the attendant comes back and says done, the coat is gone for good. If the attendant never comes back, the cloth comes off by itself, and the next attendant can take the coat. If S Q S removed an order the moment it was taken, a packer that crashed would lose that order for ever. So S Q S waits for the delete that says finished, and if it does not come in time, the order goes back on the line. The price is simple to say. An order can be handed out more than once.

## 9. A Slow Packer

Fourth, that price, paid. Packer A takes order three thousand and one. It has not stopped. It is just slow, and it needs longer than two seconds. The two seconds run out. S Q S does not know packer A is still working, so it hands order three thousand and one to packer B as well. Both packers pack it, and both delete it. Order three thousand and one was packed two times. The customer gets two parcels for one order, and the shop pays for both.

## 10. Still Working

There is a cure. Packer A takes order three thousand and two, and before its two seconds run out, it tells S Q S: I am still working, hide it for ten seconds more. S Q S calls this changing the message's visibility. Packer B asks for orders, and this time it asks S Q S to hold the question open for three seconds, well past the old timeout, rather than answer straight away. S Q S calls that long polling. Packer B is given nothing. Packer A finishes, and deletes. Order three thousand and two was packed one time.

## 11. The Packer Stops Half Way

Fifth, the moment the hand-built project could not survive. Its last act stopped the program holding its queue, and seventy orders were lost. Here, a hundred orders wait on a queue with a two second timeout. The packer takes ten, finishes three, and its process stops. S Q S reports ninety waiting, and seven in flight. Nothing is lost. The seven are only hidden. When the timeout runs out they come back, and ninety seven are waiting. A new packer drains the queue. Packed, a hundred. Lost, none. Seven orders were handed out a second time, and that was safe, because the packer that stopped had not packed them. The queue outlived the program that was reading it.

## 12. The Bill

Last, the bill. The hand-built project could give its queue a limit of fifty orders. The demo asks S Q S for the same, and S Q S does not know the setting. There is no limit to set. Then orders arrive at fifteen a round, and the packer does ten, for twenty rounds. S Q S refused none. A hundred are waiting, and the number keeps growing. Nothing warns you. The depth is a number you have to ask S Q S for, and act on. The demo also counts every request S Q S receives. A hundred orders, sent, taken and deleted ten to a request, cost thirty requests. One at a time, they cost three hundred. Here that was one container, for one queue service.

## 13. What The Simulation Left Out

The hand-built partner project got the shape right. A burst waits on a queue, the worker keeps its own pace, and the price is waiting. A queue fed faster than it is drained grows for ever. All of that holds on real S Q S, with the same numbers. It left out four things. In the simulation an order was waiting or done, and nothing in between. The real queue has a third state, in flight, with a clock on it. That clock means a slow worker can pack an order twice. It also means a worker that dies loses nothing, because the queue lives outside it. And the real queue has no limit to set, and takes and gives ten at a time.

## 14. The Verdict

Here is my verdict, plainly. Use a queue to level load when bursts come, and the caller does not need the answer straight away. Then say four things out loud, because the service will not assume them. One. Set the visibility timeout longer than your slowest piece of work, and when work runs long, tell the queue you are still working. Two. Delete an order only after the work is done. Three. Make handling an order twice do no harm, because one day it will happen. Four. Watch the depth yourself, because the queue will never refuse the backlog.

## 15. What Is Real, And When Not

What is real here? The queue is played by LocalStack, version four point fourteen, in a container the demo starts and stops itself. That version is held back on purpose: the newer ones refuse to start without a LocalStack account. The code is plain Amazon code, using the newest Amazon library for Java, and would run unchanged against Amazon itself. The one thing you need is a container runtime, such as Docker Desktop, switched on before you start. Every number in this video is the program's own output, and two runs print the same thing. So when is this too much? If load is steady and the service copes, a queue is one more thing to run and pay for. And if the caller needs the answer now, such as a price or a stock check, a queue is the wrong shape.

## 16. Thanks for Watching

That's Queue-Based Load Leveling with S Q S. If you take one sentence away, take this one: a taken order is only hidden, so delete it after the work, and make doing it twice harmless. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, give the slow packer's queue a ten second timeout instead of two, predict what packer B is given, and run it to see if you were right. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
