# Idempotent Consumer Pattern — Video Narration Script

## 1. Idempotent Consumer

This is the Idempotent Consumer pattern, in Java, explained from scratch with a program you can run yourself. I am Jayasekhar Konduru, and this is part of a series on design patterns for services that talk to each other. The Idempotent Consumer pattern says this: when the same message reaches you twice, handling it the second time should change nothing — and you get that by writing down that you have handled it in the very same act as handling it. In our online shop, the message says an order was placed and the handling means queueing a confirmation email. The customer must end up with exactly one email, out of a message system that only promises to deliver at least once.

## 2. Why the same message arrives twice

Start with the message system, not with your code. A broker hands a message to a service and waits to be told it was handled. Sometimes that acknowledgement never comes back — a network blip, a timeout, a restart. The broker is now stuck. It cannot tell the difference between a message that was handled perfectly well and an acknowledgement that got lost, and a message that never arrived at all. It has two choices: send it again, or throw it away. Every broker you are likely to use sends it again, because sending twice is something you can recover from and losing a message is not. That is called at-least-once delivery. So duplicates are not a bug somebody will eventually fix. They are the deal, and the receiving end is the only place that can do anything about them.

## 3. The version everybody writes

The obvious answer is a set of the message identifiers you have already handled. If the identifier is in the set, return and do nothing. Otherwise add it to the set and queue the confirmation email. That is a good instinct. It is exactly the right idea about what to do. Hold on to it, because it is wrong about one thing only, and the wrong thing is not what most people expect.

## 4. Act one — and it works

Act one runs it. The message is delivered, the confirmation is queued, and the identifier goes into the set. Then the acknowledgement is lost, so the broker sends the same message again. The identifier is recognised, the second delivery is skipped, and one confirmation is queued. One email for one order. The duplicate was caught. The test is green, and this is the version that ships.

## 5. Act two — a deploy lands in between

Act two runs the same two deliveries, and this time the process restarts in between them. The set of identifiers lives in a field, in memory, inside that process. The restart empties it. So when the second delivery arrives, the message looks completely new, and a second confirmation is queued. The customer now has two identical emails for one order, seventy pounds and ninety five pence, sent twice. Say the reason in one sentence, because it is the sentence to remember: the database survived the deploy, and the set of identifiers did not.

## 6. And this is not bad luck

It would be comforting to file that under bad luck — two unlikely things happening at once. It is not. Think about why the acknowledgement went missing. Very often, it went missing because the process restarted. Which means the same event caused the redelivery and emptied the memory that was supposed to catch it. So these two do not arrive independently. They arrive together, much more often than chance would suggest. This is not the rare case you can shrug at. It is the ordinary case, waiting for your next deploy.

## 7. Act three — the gap, with no restart

Now take the restart out of the argument entirely, because there is a second hole. In act three the consumer queues the confirmation, and then dies before it gets round to recording the identifier. The email was queued. The identifier was not remembered. So when the message comes again, it looks new, and a second email is queued. Two writes, at two different moments, with a gap between them. Anything that can die can die in that gap. And be clear about the stakes. Two confirmation emails is embarrassing. If this consumer had been the payments service, it would have been two charges on somebody's card.

## 8. Two failures, one cause

Put the two failures side by side, because they are really one failure wearing two coats. In act two, the memory of having handled the message was in the wrong place: a field in a process, rather than a database. In act three, it was written at the wrong moment: after the work, rather than with it. Both reduce to the same sentence. Doing the work, and remembering that you did the work, are being treated as two separate things. So the fix is to stop treating them as two things.

## 9. The whole mechanism

Here is the whole mechanism, and it is small enough to be disappointing. Open a transaction. Queue the confirmation. Record the message identifier as handled. Commit. Two rows, one commit. Because it is one commit there is no instant where one exists without the other. And the record now lives in the same database as the effect, which means it outlives the process that wrote it.

## 10. The shape of it

So the shape is this. A broker delivers a message to a consumer, and may deliver the same one again at any time. The consumer asks the database, not its own memory, whether it has already handled this identifier. If it has, it does nothing at all. If it has not, it opens one transaction, writes the effect and the identifier together, and commits. Alongside it sit two other consumers that make the opposite point. One sets a shipment status and needs no store of any kind. The other awards loyalty points, and can be rewritten until it needs none either. We will come back to both.

## 11. Act four — one commit, and the redelivery

Act four runs the same story with the record inside the commit. One confirmation and one handled identifier are written together. The redelivery arrives, the consumer finds the identifier already stored, and ignores it. Nothing is written. One email. Then the demo throws the two failures that beat the set of identifiers straight at it. Restart the process between the deliveries: still one confirmation, because the memory is in the database and the database did not restart. Kill the process before the commit: nothing at all was written, no confirmation and no identifier. That sounds like a loss, but it is the opposite. Because nothing was written, the redelivery finds a message that genuinely has not been handled, does the work cleanly, and commits. Still one confirmation.

## 12. Exactly once, out of at least once

Say the result out loud, because it is the sentence worth keeping. The broker promised only that the message would arrive at least once, and it kept that promise by sending it twice. The customer received exactly one email. Exactly-once processing, out of at-least-once delivery. And notice where that exactly-once actually lives. It is not in the broker, and it is not in the network, and it is not in a framework somebody sold you. It is in one ordinary database transaction, in your own service, doing a thing databases have done for forty years. Which is worth knowing the next time somebody offers you exactly-once delivery. What they are selling is usually this, built somewhere else.

## 13. Act five — the handler that needed none of it

Before you add any of this to a consumer, ask whether that consumer needs it. Here is one that does not. A handler that sets a shipment's status to shipped. Deliver that message twice and the status is shipped. No store, no transaction, no expiry policy, nothing to operate. That is a naturally idempotent operation, and it is always the better answer when it is available. And here is one that is not, but could be. Awarding seventy loyalty points for an order. Handle that twice and the customer has a hundred and forty points for a seventy pound order. Now rewrite it. Instead of add seventy points, say set the points for this order to seventy. Handle that twice and the customer has seventy. Same business outcome, and a duplicate simply cannot get it wrong. Reaching for a dedupe table before asking that question is the most common mistake in this whole area.

## 14. And the store's own cost

And when you do need the store, be honest about what it costs. Every handled identifier is a row, and the table grows for as long as messages arrive. So the rows have to be cleared out, which means somebody owns a retention job and somebody gets paged when it stops running. Then this. The demo handles a message, waits a minute with a memory that only keeps identifiers for thirty seconds, and delivers the same message again. Two confirmations. The duplicate came back after the memory of it had expired, so it looked new. That is not a bug in the demo. It is the shape of the trade. Too short a window and a duplicate arriving after a long broker outage gets through. Too long and you are operating a very large table. There is no correct number to derive. There is a number you choose and have to be able to defend.

## 15. What the sender owes you

One last thing, and it is the smallest part of the pattern. What does the sending side owe you? One thing: a stable message identifier. The same message, delivered twice, has to carry the same identifier both times. That single field is everything the receiving side needs. You do not have to compare the contents of the message. You do not have to hash anything, or reason about whether two messages are really the same. You look up one identifier. One field from the sender, and one transaction on your side. That is the entire handover.

## 16. Idempotent Consumer

So, the Idempotent Consumer. Handling the same message twice has the same effect as handling it once, and you buy that by writing the record of having handled it in the same transaction as its effect. Both, or neither. What you get is three things. A redelivery changes nothing. A deploy cannot make the consumer forget, because the memory is in the database. And a crash never leaves half-done work, because there is only one commit to be on one side or the other of. What you pay is two things. A table that grows with every message, which somebody has to operate and clear out. And an expiry window, because those identifiers cannot be kept forever — a number you choose rather than derive, with a real duplicate getting through on one side of it and a very large table on the other. And before any of that, ask the cheaper question: is this handler already idempotent, or could it be rewritten until it is? Setting a value rather than adding to one costs nothing to operate. Everything is in the repository: the code, the five acts, the tests, and an animation you can step through. Thanks for watching.
