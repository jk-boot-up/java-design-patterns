# Queue-Based Load Leveling with SQS, Explained

## The pattern in one sentence

When work arrives in bursts faster than a service can handle it, put a queue in between, so the burst waits in line and the service keeps its own steady pace.

## The analogy, before any of the service's words

Think of a busy post office on the day before a holiday. A crowd arrives at once. The clerk serves one person at a time, at the clerk's own speed. A ticket machine at the door gives each person a number, and they wait. Nobody is sent home, and the clerk is never rushed.

Now four questions the post office has to answer, and a simulation never has to. When the clerk calls a number and walks off with that person's parcel, is the person served, or only called? What if the clerk is slow, and the next clerk calls the same number? What if a clerk goes home mid-shift, holding three tickets? And how long can the line get before somebody says "no more"? Those four questions are the six acts of this project.

## What SQS calls these things

**SQS**, Amazon's Simple Queue Service, is the ticket machine and the line. A **queue** is one line. A **message** is one piece of text on it; here, an order id such as ORD-2001.

An order nobody has taken is **waiting**. The number of waiting orders is the queue's **depth**, and SQS will tell you it whenever you ask.

When a packer takes an order, SQS does not remove it. It hides it from everybody else and counts it as **in flight**. Only the packer's **delete**, made with the **receipt** SQS gave it, removes the order for good.

How long SQS hides a taken order is the **visibility timeout**. If no delete arrives in that time, SQS puts the order back as waiting and hands it out again, to whoever asks next. A packer that needs longer can tell SQS, before the time is up, to keep hiding it; SQS calls this **changing the message's visibility**.

Asking SQS for orders and letting it hold the question open for a few seconds, rather than answering "none" at once, is **long polling**. An order nobody ever takes is thrown away after the **retention period**.

**LocalStack** plays SQS on your own machine, in one container the demo starts and stops.

## The six acts

### A Burst Lands On The Queue

A hundred orders arrive at once. SQS takes at most 10 in one request, and says so when sent 11. So checkout sends the burst as 10 requests of 10, and SQS reports the depth it built.

```
  100 orders arrive at once. checkout puts each one on a queue on Amazon SQS, played by LocalStack.
  11 orders in one request: Maximum number of entries per request are 10. You have sent 11.
  so the burst goes as 10 requests of 10. SQS reports 100 waiting and 0 in flight.
  nobody was refused. SQS keeps an order nobody takes for 345600 seconds, which is 4 days.
```

### The Packer Keeps Its Own Pace

The packer asks for 11 and is refused: SQS hands out at most 10 to one request. It takes 10, and for a moment those 10 are neither waiting nor gone, but in flight. Then it packs and deletes them, round after round, and the depth falls by 10 each time.

```
  the packing service asks for 11 at once: Value 11 for parameter MaxNumberOfMessages is invalid. Reason: Must be between 1 and 10, if provided.
  it takes 10. SQS now reports 90 waiting and 10 in flight: taken, not yet finished.
  it packs and deletes them. waiting after each round: 90, 80, 70, 60, 50, 40, 30, 20, 10, 0.
  100 packed in 10 rounds, never more than 10 at once. the deepest the queue got: 100.
```

### Taken Is Not Removed

A queue whose visibility timeout is 2 seconds. A packer takes ORD-2001 and stops without deleting it. SQS hides it: 0 waiting, 1 in flight, and a second packer asking at once is given nothing. The second packer keeps asking, and once the 2 seconds have passed, ORD-2001 is handed out again.

```
  SQS hides a taken order for a while, then hands it out again. it calls that time the visibility timeout. the default is 30 seconds.
  this queue's timeout is 2 seconds. a packer takes ORD-2001 and stops before it finishes. SQS reports 0 waiting and 1 in flight.
  a second packer asks at once, and is given 0 orders.
  it keeps asking. ORD-2001 comes back once the 2 seconds have passed, not before: true. SQS has now handed it out 2 times.
  SQS never knew the first packer stopped. it only knew the time ran out.
```

How long after the 2 seconds it returns depends on the machine, so the demo prints whether it returned only after the timeout had passed, not the milliseconds.

### A Slow Packer

The same rule, when the first packer has not stopped but is merely slow. Both packers end up with the order, and the customer gets two parcels. Then the cure: before the time runs out, packer A tells SQS it is still working, and packer B, waiting three seconds for an order in a long poll, is given none.

```
  packer A takes ORD-3001 and needs longer than 2 seconds. the time runs out, and packer B is given ORD-3001 too.
  both pack it and both delete it. ORD-3001 was packed 2 times: two parcels for one order.
  next, packer A takes ORD-3002 and, before its time runs out, tells SQS it is still working: hide it 10 seconds more.
  packer B asks SQS to hold its question open for 3 seconds, past the old timeout. it is given 0 orders.
  packer A finishes and deletes. ORD-3002 was packed 1 time.
```

### The Packer Stops Half Way Through A Round

The plain-Java project's last act lost 70 orders when the process holding its queue stopped. Here the packer's process stops while it holds 10 orders, 3 of them finished. SQS still has the other 7, hidden, and gives them back when the timeout runs out.

```
  100 orders on a queue with a 2-second timeout. the packer takes 10, finishes 3, and its process stops.
  SQS reports 90 waiting and 7 in flight. nothing is lost; 7 are only hidden.
  when the timeout runs out they come back: 97 waiting. a new packer drains the queue.
  packed: 100, lost: 0, packed twice: 0. orders SQS handed out a second time: 7.
  the queue outlived the process reading it.
```

### The Bill

There is no setting for the deepest a queue may get; SQS does not know the word. A backlog fed at 15 a round and drained at 10 grows by 5 a round, and nothing refuses it. Every request is counted by the SDK itself, so the last line is requests SQS really received.

```
  asked for a queue that holds at most 50 orders, SQS answers: Unknown Attribute MaximumDepth.
  orders arrive at 15 a round and the packer does 10, for 20 rounds. SQS refused none. waiting: 100, and growing.
  nothing warns you. the depth is a number you ask SQS for, and act on: more packers, or a limit of your own.
  100 orders, 10 to a request: 30 requests (SendMessageBatch x10, ReceiveMessage x10, DeleteMessageBatch x10). one at a time: 300.
  a taken order can come back, so packing one twice must do no harm. this demo needed 1 container for 1 queue service.
```

## The verdict

Use a queue to level load when bursts come and the caller does not need the answer at once. Then send and take 10 at a time; set the visibility timeout longer than your slowest piece of work, and say "still working" when work runs long; delete only after the work is done; make handling an order twice harmless, because one day it will happen; and watch the depth yourself, because SQS will never refuse the backlog.
