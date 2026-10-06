# Queue-Based Load Leveling with SQS Pattern — Video Narration Script

## 1. Queue-Based Load Leveling with SQS

Hello, and welcome. This video explains the Queue-Based Load Leveling pattern in Java, using a real Amazon queue, running on your own machine. This video is presented by Jayasekhar Konduru. First, a simple definition. When work arrives in bursts, faster than a service can handle it, you put a queue in between. The burst waits in line. And the service keeps its own steady pace. It works like a post office the day before a holiday. A crowd arrives at once, and a machine at the door hands out numbered tickets. The clerk serves one person after another, never rushed. In our online store, a sale sends a hundred orders in the same moment. Checkout puts every order on a queue, and tells the customer at once that it is received. The packing service takes orders off the queue at its own pace, ten at a time. By the end, you will hear a real burst fill the queue. An order that is taken, but not removed. A slow packer that packs one order twice. A packer that stops, and loses nothing. And the bill.

## 2. The Scenario

Here is the scenario. The shop runs a sale, and in its first second, a hundred orders arrive at once. The packing service can handle ten orders per round, however many are waiting. So checkout does not call the packing service directly. It puts each order on a queue, a waiting line for work. And it tells the customer straight away that the order is received. The plain Java version kept its queue in memory, with a made-up clock. This time, the queue is Amazon's queue service. And the rules it plays by are Amazon's rules.

## 3. A Burst Lands On The Queue

First demo: a burst lands on the queue. The queue service is called S Q S, short for Simple Queue Service. A hundred orders arrive at once, and checkout sends them to S Q S. It tries to send eleven orders in one request. And S Q S refuses. The most it accepts in one request is ten. That is not a rule this program made up. It is the real service saying no. So the burst goes as ten requests, of ten orders each. S Q S now reports a hundred orders waiting. Nobody was refused. And S Q S will keep an order that nobody takes for four days.

## 4. The Service's Words

The real service brings a few words with it. Each one is simpler than it sounds. An order that nobody has taken yet is waiting. The number of waiting orders is the depth of the queue. When a packer takes an order, S Q S does not remove it. It hides it from everyone else. Until the packer says it has finished, by deleting it. An order that is taken, but not yet deleted, is called in flight. And how long S Q S hides a taken order, before handing it out again, is called the visibility timeout. None of this is really on Amazon here. A program called LocalStack answers exactly as S Q S would. It runs in a container, a small sealed box on this machine, that the demo switches on and off.

## 5. The Packer Keeps Its Own Pace

Second demo: the packer keeps its own pace. It asks S Q S for eleven orders at once. And S Q S refuses again. It hands out between one and ten. So the packer takes ten. For a moment, S Q S reports ninety waiting, and ten in flight. Those ten are neither in the line, nor gone. They are taken, hidden, and not yet finished. The packer packs the ten parcels, and only then deletes them. Round after round, the depth falls by ten. Ninety, eighty, seventy, and so on, down to zero. A hundred orders packed in ten rounds. And the packer never did more than ten at once. That is the pattern working.

## 6. Where The Orders Live

Here is the whole picture, in words. There are four parts, in order. First, checkout. It sends the burst to the queue, ten orders per request. Second, the S Q S queue. It counts the orders waiting, and the orders in flight. It lives outside both checkout and the packers. Third, the packer. It takes up to ten orders, packs them, and then deletes them. Fourth, a second packer. It is handed any order whose timeout ran out. The rule that holds it together is the order of the last two steps. Pack first. Delete only after the parcel is packed.

## 7. Taken Is Not Removed

Third demo, and this is the heart of it. By default, S Q S hides a taken order for thirty seconds. This queue hides it for only two seconds. A packer takes order two thousand and one. Then it stops, before it finishes. It never deletes the order. S Q S reports no orders waiting, and one in flight. A second packer asks straight away, and is given nothing. The second packer keeps asking. Once the two seconds have passed, order two thousand and one comes back. And S Q S says it has now handed it out twice. S Q S never knew the first packer had stopped. It only knew the time had run out.

## 8. Why Hide, And Not Remove?

Why does S Q S hide an order, instead of removing it? Think of a coat check. An attendant lifts a coat off its hook, and drapes a cloth over the hook. If the attendant comes back and says done, the coat is gone for good. If the attendant never comes back, the cloth comes off, and the next attendant can take the coat. If S Q S removed an order the moment it was taken, a packer that crashed would lose it forever. So S Q S waits for the delete that says finished. If it does not come in time, the order goes back in line. The price is simple. An order can be handed out more than once.

## 9. A Slow Packer

Fourth demo: that price, paid. Packer A takes order three thousand and one. It has not stopped. It is just slow, and needs more than two seconds. The two seconds run out. S Q S does not know packer A is still working. So it hands order three thousand and one to packer B as well. Both packers pack it, and both delete it. The order was packed twice. The customer gets two parcels for one order. And the shop pays for both.

## 10. Still Working

There is a cure. Packer A takes order three thousand and two. Before its two seconds run out, it tells S Q S: I am still working, hide it for ten seconds more. Packer B asks for orders. This time it asks S Q S to hold its question open for three seconds, rather than answer at once. That is called long polling. Packer B is given nothing. Packer A finishes, and deletes the order. Order three thousand and two was packed once.

## 11. The Packer Stops Half Way

Fifth demo, the moment the plain Java version could not survive. In its last demo, the program holding the queue stopped, and seventy orders were lost. Here, a hundred orders wait on a queue with a two-second timeout. The packer takes ten, finishes three, and then its program stops. S Q S reports ninety waiting, and seven in flight. Nothing is lost. The seven are only hidden. When the timeout runs out, they come back, and ninety-seven are waiting. A new packer clears the queue. A hundred packed. None lost. Seven orders were handed out a second time. And that was safe, because the packer that stopped had not packed them. The queue outlived the program reading it.

## 12. The Bill

Finally, the bill. The plain Java version could give its queue a limit of fifty orders. The demo asks S Q S for the same. And S Q S does not know that setting. There is no limit to set. Then orders arrive at fifteen per round, and the packer handles ten, for twenty rounds. S Q S refuses none. A hundred are waiting, and the number keeps growing. Nothing warns you. You have to ask for the depth yourself, and act on it. The demo also counts every request S Q S receives. A hundred orders, sent, taken, and deleted ten at a time, cost thirty requests. One at a time, they would cost three hundred.

## 13. What The Simulation Left Out

The plain Java version got the shape right. A burst waits on a queue. The worker keeps its own pace. And the price is waiting. All of that holds on real S Q S, with the same numbers. But it left out four things. First, in the plain version an order was either waiting, or done. The real queue has a third state, in flight, with a clock on it. Second, that clock means a slow worker can pack an order twice. Third, a worker that dies loses nothing, because the queue lives outside it. And fourth, the real queue has no limit to set, and handles ten orders at a time.

## 14. The Verdict

So, here is the verdict. Use a queue when bursts come, and the caller does not need the answer straight away. Then settle four things, because the service will not. One. Set the visibility timeout longer than your slowest work. And when work runs long, tell the queue you are still working. Two. Delete an order only after the work is done. Three. Make handling an order twice harmless, because one day it will happen. Four. Watch the depth yourself, because the queue will never refuse a backlog.

## 15. What Is Real, And When Not

A quick, honest note about this demo. The queue is played by LocalStack, version four point fourteen, in a container the demo starts and stops by itself. That version is held back on purpose, because newer ones need a LocalStack account. The code is ordinary Amazon code, using the newest Amazon library for Java. It would run unchanged against Amazon itself. You just need Docker switched on first. Every number you heard comes from the program's own output. So, when is this too much? If the load is steady and the service copes, a queue is one more thing to run and pay for. And if the caller needs the answer now, like a price or a stock check, a queue is the wrong shape.

## 16. Thanks for Watching

That's Queue-Based Load Leveling, with S Q S. If you remember one sentence, make it this one. A taken order is only hidden, so delete it after the work, and make doing it twice harmless. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Give the slow packer's queue a ten-second timeout, instead of two. Guess what packer B will be given, and then run it to check. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
