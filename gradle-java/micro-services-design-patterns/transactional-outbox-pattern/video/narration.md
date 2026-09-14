# Transactional Outbox Pattern — Video Narration Script

## 1. Transactional Outbox

This is the Transactional Outbox pattern, in Java, explained from scratch with a program you can run yourself. I am Jayasekhar Konduru, and this is part of a series on design patterns for services that talk to each other. The Transactional Outbox pattern says this: when you need to save something and also tell somebody about it, do not do two things. Write the announcement into your own database, in the same transaction as the data, and let a separate process post it later. In our online shop, that means the order row and the message that announces it are written by one commit, and the confirmation email goes out afterwards, from a message that was already safely stored.

## 2. Two things that have to happen together

A customer presses buy. Two things have to happen now. The order has to be saved, so the shop knows it exists and can be charged for. And the rest of the business has to be told, so the confirmation email goes out, the warehouse picks the parcel, and the accounts balance at the end of the month. The first of those is a write to your own database. The second is a message to a broker, which is a different piece of software on a different machine. They are two systems, and no transaction covers both of them. The obvious code does them one after the other, on two lines. That is where we start.

## 3. The version everybody writes first

Here is what almost everybody writes first, and it is two lines long. Save the order to the database. Then publish an event to the broker saying the order was placed. Read that out loud and it sounds correct, because it is the order you would do it in yourself. It would pass a code review in any team I have worked in. Hold on to that, because in about a minute it is going to lose a customer's order without raising a single error.

## 4. Act one — and it works

Act one runs those two lines. The order commits. The broker accepts the message fifteen milliseconds later. The notification service receives it and the email goes out. One order saved, one event delivered, one email sent. This is the important thing about act one: it is what every test written for this code will see. The author writes a test, it passes, and the code ships. Everything that goes wrong from here on goes wrong in production, to a real customer, on a path no test ever took.

## 5. Act two — a deploy lands in the gap

Act two runs exactly the same two lines, and this time the process dies in between them. A deploy landing in the middle of a request will do it, and a deploy landing mid request is one of the most ordinary reasons a request dies at all. Now count what is left. The order is in the database. It is a real order, for seventy pounds and ninety five pence, and the customer will be charged for it. Zero events were delivered and zero emails were sent. The order is real, the customer will be charged, and nobody will ever be told.

## 6. Now ask what would retry it

Now ask the question that matters, and sit with the answer. What would retry this? Nothing will. Nothing anywhere recorded that a message was owed. There is no failed send in a log, because the send was never attempted. There is no row in a dead letter queue, because nothing reached the queue. There is no alert, because nothing errored. This is not a message that failed to send. It is a message that stopped existing. And no amount of retry logic, monitoring, or cleverness can find something that was never written down anywhere. That is what makes this failure different from an ordinary outage.

## 7. The two fixes somebody will suggest

Two fixes get suggested in every room, and both are worth taking seriously before taking apart. The first is to swap the lines. Publish first, then save. That does not close the gap; it moves it. Now a crash in the middle announces an order that does not exist, and the warehouse picks a parcel that nobody paid for. You have chosen a different lie, not fewer lies. The second is to wrap both lines in a transaction. But a database transaction covers the database. The broker is a separate program on a separate machine, and it is not going to join your transaction. There is no commit that spans the two of them.

## 8. So think about an out-tray

So stop trying to make the broker part of your transaction, and think about an out-tray instead. You write a letter at your desk. You do not get up and walk to the post box. You drop the letter in the out-tray beside you, at the same moment you file your own copy of it. That is one action, and it does both things. Later, the post room comes round, takes what is in the tray, and posts it. If the post office is shut, the letter comes back and goes out on the next round. The important part is that your job ended the moment the letter hit the tray. Whether the post office is open is not your problem.

## 9. The whole mechanism

Here is the whole mechanism, and it is small enough to be disappointing. Begin a transaction. Save the order. Save the message as well, as an ordinary row in an ordinary table in your own database. Commit. Two rows, one commit. Because it is one commit, there is no instant at which one exists without the other. A crash before it leaves neither. A crash after it leaves both. And look at what is not in those four lines. There is no broker. The order service does not call it, does not import it, and does not know it exists. That absence is the pattern.

## 10. The shape of it

So the shape has two halves that run at different times. The first half is the checkout. The order service opens a transaction, writes the order row and the message row, and commits. Then it is finished, and the customer sees their confirmation page. The second half is a separate process called the relay. It reads the messages in the table that have not been sent, publishes each one to the broker, and marks each one as sent. The two halves share nothing but a table. One runs because a customer pressed a button. The other runs because a timer fired.

## 11. Act three — one commit, then a sweep

Act three. After the checkout commits, and before anything else happens, there is one order saved, one message waiting in the out-tray, and zero events delivered. The order service never called the broker. Then the relay comes round. Read the timeline: one commit wrote the order and the message together. The broker accepted the message. The notification service sent the email. And the relay marked the message as sent. The customer got exactly the same email as in act one. What changed is that between the commit and the email there was no moment where the order existed and the message did not.

## 12. Act four — the broker is down

Act four takes the broker away completely, and two customers check out while it is unreachable. Both checkouts succeed. They never needed the broker; they wrote two rows to a database and finished. In the version we started with, a broker outage would have been a checkout outage. The first sweep publishes nothing, because the broker will not answer, and both messages stay in the tray. The broker comes back, the second sweep publishes both, and both emails go out. Now go and look for the retry logic, because there is none. No backoff setting, no attempt counter, no scheduled retry table. A row that was not published is still an unsent row, so the next sweep picks it up again. The retry is not code. It is a consequence of where the message is kept.

## 13. Act five — the bill

Act five is the bill, and this is the part most explanations leave out. The relay publishes a message. The broker takes it and the email goes out. And then the relay dies, before it can write down that it had sent it. The row is still marked unsent, because nothing ever marked it. So the relay restarts, reads the tray, finds that message still sitting there, and publishes it again. The message was delivered twice. The customer has two identical confirmation emails in their inbox for one order. Nothing failed, no test went red, and this is the pattern working exactly as designed.

## 14. Never lost, sometimes twice

Here is why that duplicate cannot be engineered away. Publishing to the broker and marking the row as sent are in two different systems, so there is a gap between them. It is the same gap this pattern was invented to close, turning up again inside the fix. You cannot remove it. You can only choose which way it falls. Mark the row sent first, and a crash in the gap loses the message forever. Publish first, and a crash in the gap sends it twice. This pattern publishes first, on purpose, because a duplicate is something you can recover from and a loss is not. The name for that guarantee is at-least-once delivery. Say it out loud when you adopt this: never lost, sometimes twice. Anybody who tells you their outbox gives exactly-once has not looked at this gap.

## 15. What you owe whoever receives it

The duplicate is not fixable on this side, and pretending otherwise is how teams end up believing in exactly-once. It belongs to whoever receives the message. What this side owes them is the ability to notice it, and it provides exactly one thing: the message identifier was identical both times. Same id, same message. A receiver that remembers which identifiers it has already handled can throw the second one away. That one stable field is the entire handover. And it matters more than it sounds. Two confirmation emails is embarrassing. If the thing receiving that message were the payments service, it would be two charges on somebody's card.

## 16. Transactional Outbox

So, the Transactional Outbox. When you have to save something and also announce it, do not do two things. Write the announcement into your own database, as an ordinary row, in the same transaction as the data. Then let a separate relay read those rows and post them. What you get is three things. The data and its announcement are one atomic act, so nothing is silently lost. Your checkout keeps working when the broker does not, because it never talks to the broker. And every message is delivered eventually, without anybody writing a line of retry logic. What you pay is four things. The message goes out on the next sweep rather than immediately. Somebody has to run and watch the relay. The table grows and needs clearing out. And the same message will sometimes arrive twice. Everything is in the repository: the code, the five acts, the tests, and an animation you can step through. Run it, and pay particular attention to act five. Thanks for watching.
