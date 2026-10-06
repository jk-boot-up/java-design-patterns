# Idempotent Consumer Pattern — Video Narration Script

## 1. Idempotent Consumer

Hello, and welcome. This video explains the Idempotent Consumer pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Idempotent means doing something twice has the same effect as doing it once. An idempotent consumer is a service that can receive the same message twice, and the second time, nothing changes. It does this by writing down that it handled the message, in the very same step as handling it. Think of a lift button. Press it once, and the lift is called. Press it five more times, and it is still called just once. In our online store, a message says an order was placed. Handling it means sending a confirmation email. The customer must get exactly one email. Even though the message system only promises to deliver each message at least once.

## 2. Why the same message arrives twice

Let's start with the message system, not your code. A broker is a program that passes messages between services. It hands a message to a service, and waits to be told it was handled. That reply is called an acknowledgement. Sometimes the acknowledgement never comes back. A network hiccup, a timeout, or a restart. Now the broker is stuck. It cannot tell whether the message was handled and the reply got lost, or whether it never arrived at all. It has two choices: send it again, or throw it away. Almost every broker sends it again. Because a duplicate can be recovered from, and a lost message cannot. That is called at-least-once delivery. So duplicates are not a bug someone will fix one day. They are part of the deal. And only the receiving service can deal with them.

## 3. The version everybody writes

The obvious answer is to keep a set of the message I Ds you have already handled. If a message's I D is in the set, do nothing. Otherwise, add it to the set, and queue the confirmation email. That is a good instinct. It is exactly the right idea. It is only wrong about one thing. And that thing is not what most people expect.

## 4. Act one — and it works

First demo. The message is delivered. The confirmation is queued. And the I D goes into the set. Then the acknowledgement is lost. So the broker sends the same message again. The I D is recognised, and the second delivery is skipped. One email, for one order. The duplicate was caught. The test passes. And this is the version that gets released.

## 5. Act two — a deploy lands in between

Second demo: the same two deliveries. But this time, the service restarts in between. The set of I Ds lives in memory, inside the running program. The restart empties it. So when the second delivery arrives, the message looks brand new. And a second confirmation is queued. The customer now has two identical emails, for one order of seventy pounds ninety-five. Here is the sentence to remember. The database survived the restart. The set of I Ds did not.

## 6. And this is not bad luck

It is tempting to call that bad luck. Two unlikely things happening at once. But it is not. Think about why the acknowledgement went missing. Very often, it went missing because the service restarted. So one event caused both problems. It caused the message to be sent again. And it emptied the memory that should have caught it. These two things usually arrive together. This is not a rare case. It is the normal case, waiting for your next release.

## 7. Act three — the gap, with no restart

Now take the restart away completely, because there is a second hole. In the third demo, the service queues the confirmation. Then it crashes, before it records the I D. The email was queued. But the I D was not remembered. So when the message comes again, it looks new, and a second email is queued. Two writes, at two different moments, with a gap between them. Anything that can crash can crash in that gap. And think about the stakes. Two confirmation emails is embarrassing. If this had been the payment service, it would have been two charges on someone's card.

## 8. Two failures, one cause

Put the two failures side by side. They are really one failure. In the second demo, the memory was in the wrong place. In the program's memory, not in the database. In the third demo, it was written at the wrong moment. After the work, not with it. Both come down to one sentence. Doing the work, and remembering that you did it, are treated as two separate things. So the fix is to stop treating them as two things.

## 9. The whole mechanism

Here is the whole mechanism, and it is small. Open a database transaction. A transaction is a group of changes that are saved together, or not at all. Queue the confirmation. Record the message I D as handled. Then save, which is called a commit. Two rows, one commit. So there is never a moment when one exists without the other. And the record lives in the same database as the email. So it outlives any restart.

## 10. The shape of it

Here is the shape of it, in words. A broker delivers a message to a consumer. And it may deliver the same one again, at any time. The consumer asks the database, not its own memory, whether it has already handled this I D. If it has, it does nothing at all. If it has not, it opens one transaction. It writes the email and the I D together, and commits. Beside it are two other consumers, which make the opposite point. One sets a shipment status, and needs no memory at all. The other awards loyalty points, and can be rewritten until it needs none either. We will come back to both.

## 11. Act four — one commit, and the redelivery

Fourth demo: the same story, with the I D saved inside the same commit. One confirmation and one handled I D are written together. The message is sent again. The consumer finds the I D already stored, and ignores it. Nothing is written. One email. Now the demo repeats the two failures that beat the set of I Ds. First, a restart between the deliveries. Still one confirmation. Because the memory is in the database, and the database did not restart. Second, a crash before the commit. Nothing at all was written: no email, and no I D. That sounds bad, but it is exactly right. The message is sent again, and it really has not been handled. So it is handled cleanly, and committed. Still one confirmation.

## 12. Exactly once, out of at least once

Say the result out loud, because it is worth keeping. The broker only promised to deliver the message at least once. It kept that promise, by sending it twice. And the customer received exactly one email. Exactly-once handling, from at-least-once delivery. And notice where the exactly-once lives. Not in the broker. Not in the network. Not in a framework someone sold you. In one ordinary database transaction, in your own service. So next time someone offers you exactly-once delivery, remember this. They are usually selling this same idea, built somewhere else.

## 13. Act five — the handler that needed none of it

Fifth demo. Before adding any of this, ask whether the consumer even needs it. Here is one that does not. A handler that sets a shipment's status to shipped. Deliver that message twice, and the status is still shipped. No memory, no transaction, nothing to run. It is naturally idempotent. And when that is possible, it is always the better answer. Here is one that is not, but could be. Add seventy loyalty points for an order. Handle that twice, and the customer has a hundred and forty points, for a seventy-pound order. Now rewrite it. Instead of: add seventy points. Say: set the points for this order to seventy. Handle that twice, and the customer has seventy. Same result, and a duplicate cannot get it wrong. Reaching for a table of handled I Ds before asking this question is the most common mistake here.

## 14. And the store's own cost

When you do need the table of handled I Ds, be honest about what it costs. Every handled I D is a row. And the table grows for as long as messages arrive. So old rows must be cleared out. That means someone owns a clean-up job, and gets called when it stops. Then this. The demo handles a message. It keeps I Ds for only thirty seconds. A minute later, the same message arrives again. Two confirmations. The duplicate came back after the memory of it had expired, so it looked new. That is not a bug. It is the trade. Too short a window, and a late duplicate gets through. Too long, and you run a very large table. There is no correct number to calculate. There is a number you choose, and must be able to defend.

## 15. What the sender owes you

One last thing, and it is the smallest part of the pattern. What does the sending side owe you? Just one thing: a stable message I D. The same message, delivered twice, must carry the same I D both times. That one field is everything the receiver needs. You do not compare the contents of the message. You just look up one I D. One field from the sender. And one transaction on your side.

## 16. Idempotent Consumer

That's the Idempotent Consumer pattern. If you remember one sentence, make it this one. Write the record of handling a message in the same transaction as its effect: both, or neither. What you get. A repeated message changes nothing. A restart cannot make the consumer forget. And a crash never leaves work half done. What you pay. A table that grows, which someone must run and clear out. And a time window, which is a number you choose. And before any of that, ask the cheaper question. Could this handler be rewritten to set a value, instead of adding to one? The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
