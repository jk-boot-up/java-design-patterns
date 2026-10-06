# Transactional Outbox Pattern — Video Narration Script

## 1. Transactional Outbox

Hello, and welcome. This video explains the Transactional Outbox pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Sometimes you need to save something, and also tell others about it. The outbox says: do not do two separate things. Write the announcement into your own database, in the same step as the data. Then let a separate process send it out later. Think of an office out-tray. You drop the letter in the tray, and the post room sends it later. In our online store, the order, and the message announcing it, are saved together. And the confirmation email goes out afterwards, from a message that was already safely stored.

## 2. Two things that have to happen together

A customer presses buy. Now two things must happen. The order must be saved, so the shop knows it exists, and can charge for it. And the rest of the business must be told. So the email goes out, the warehouse packs the parcel, and the accounts balance. The first is a write to your own database. The second is a message to a broker: a separate program, on a separate machine, that passes messages on. They are two systems. And no single transaction covers both. The obvious code does them one after the other, in two lines. That is where we start.

## 3. The version everybody writes first

Here is what almost everyone writes first. Two lines. Save the order to the database. Then send a message to the broker, saying the order was placed. That sounds correct. It is the order you would do it in yourself. It would pass any code review. Remember that. Because in about a minute, it will lose a customer's order without a single error.

## 4. Act one — and it works

First demo: the two lines. The order is saved. The broker accepts the message fifteen milliseconds later. The notification service receives it, and the email goes out. One order saved. One message delivered. One email sent. Here is the important point. This is what every test written for this code will see. The test passes, and the code is released. Everything that goes wrong from here happens in production, to a real customer, on a path no test ever took.

## 5. Act two — a deploy lands in the gap

Second demo: exactly the same two lines. But this time, the program dies between them. A new release landing in the middle of a request will do it. And that is one of the most ordinary ways a request dies. Now count what is left. The order is in the database. It is a real order, for seventy pounds ninety-five, and the customer will be charged. No messages were delivered. No emails were sent. The order is real. The customer will be charged. And nobody will ever be told.

## 6. Now ask what would retry it

Now ask the question that matters. What would retry this? Nothing will. Nothing anywhere recorded that a message was owed. There is no failed send in a log, because the send was never attempted. There is nothing in a queue of failed messages, because nothing reached the queue. There is no alert, because nothing went wrong that anything could see. This is not a message that failed to send. It is a message that stopped existing. And no retry logic, monitoring, or cleverness can find something that was never written down.

## 7. The two fixes somebody will suggest

Two fixes get suggested in every room. Both are worth taking seriously, before we take them apart. The first: swap the lines. Send the message first, then save. That does not close the gap. It moves it. Now a crash in the middle announces an order that does not exist. And the warehouse packs a parcel nobody paid for. You have chosen a different lie, not fewer lies. The second: wrap both lines in a transaction. But a database transaction only covers the database. The broker is a separate program, on a separate machine. It will not join your transaction. No single save covers both.

## 8. So think about an out-tray

So stop trying to make the broker part of your transaction. Think about an out-tray instead. You write a letter at your desk. You do not walk to the post box. You drop the letter in the out-tray beside you, at the same moment you file your own copy. One action, and both things are done. Later, the post room comes round, and posts what is in the tray. If the post office is shut, the letter goes out on the next round. Your job ended the moment the letter hit the tray. Whether the post office is open is not your problem.

## 9. The whole mechanism

Here is the whole mechanism, and it is small. Start a database transaction. Save the order. Save the message too, as an ordinary row, in an ordinary table, in your own database. Then commit, which means save both together. Two rows, one commit. So there is never a moment when one exists without the other. A crash before the commit leaves neither. A crash after it leaves both. And notice what is missing. There is no broker. The order service does not call it, and does not even know it exists. That absence is the pattern.

## 10. The shape of it

The shape has two halves, which run at different times. The first half is checkout. The order service opens a transaction, writes the order and the message, and commits. Then it is finished, and the customer sees their confirmation page. The second half is a separate process, called the relay. It reads the messages that have not been sent yet. It sends each one to the broker. And it marks each one as sent. The two halves share nothing but a table. One runs because a customer pressed a button. The other runs because a timer went off.

## 11. Act three — one commit, then a sweep

Third demo: one commit, then a sweep. After the checkout commits, and before anything else happens, there is one order saved. One message waiting in the out-tray. And no messages delivered. The order service never called the broker. Then the relay comes round. The broker accepts the message. The notification service sends the email. And the relay marks the message as sent. The customer got exactly the same email as in the first demo. What changed is this. There was never a moment when the order existed, and the message did not.

## 12. Act four — the broker is down

Fourth demo: the broker is down. Two customers check out while the broker cannot be reached. Both checkouts succeed. They never needed the broker. They wrote two rows to a database, and finished. In the two-line version, a broker outage would have been a checkout outage. The relay's first sweep sends nothing, because the broker will not answer. Both messages stay in the tray. The broker comes back. The second sweep sends both, and both emails go out. Now look for the retry logic. There is none. A message that was not sent is still an unsent row. So the next sweep simply picks it up again. The retry is not code. It comes from where the message is kept.

## 13. Act five — the bill

Fifth demo: the bill. Most explanations leave this part out. The relay sends a message. The broker takes it, and the email goes out. And then the relay dies, before it can mark the message as sent. So the row is still marked unsent. The relay restarts, reads the tray, and finds that message still there. So it sends it again. The message was delivered twice. The customer has two identical confirmation emails, for one order. Nothing failed. No test went red. And this is the pattern working exactly as designed.

## 14. Never lost, sometimes twice

Here is why that duplicate cannot be designed away. Sending to the broker, and marking the row as sent, happen in two different systems. So there is a gap between them. It is the same gap this pattern was invented to close, turning up again inside the fix. You cannot remove it. You can only choose which way it falls. Mark the row sent first, and a crash in the gap loses the message forever. Send first, and a crash in the gap sends it twice. This pattern sends first, on purpose. Because a duplicate can be recovered from, and a loss cannot. That promise is called at-least-once delivery. Say it out loud when you adopt this: never lost, sometimes twice.

## 15. What you owe whoever receives it

The duplicate cannot be fixed on this side. It belongs to whoever receives the message. What this side owes them is a way to notice it. And it provides exactly one thing. The message I D was the same both times. Same I D, same message. A receiver that remembers which I Ds it has already handled can throw the second one away. That one stable field is the whole handover. And it matters more than it sounds. Two confirmation emails is embarrassing. If the receiver were the payment service, it would be two charges on someone's card.

## 16. Transactional Outbox

That's the Transactional Outbox pattern. If you remember one sentence, make it this one. Save the message in your own database, in the same transaction as the data, and let a separate relay send it later. What you get. The data and its announcement are saved together, so nothing is silently lost. Checkout keeps working when the broker does not. And every message is eventually delivered, without any retry code. What you pay. The message goes out on the next sweep, not immediately. Someone must run and watch the relay. The table grows, and needs clearing out. And the same message will sometimes arrive twice. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Pay special attention to the fifth demo. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
