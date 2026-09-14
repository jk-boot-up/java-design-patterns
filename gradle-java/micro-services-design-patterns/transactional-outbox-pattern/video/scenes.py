#!/usr/bin/env python3
"""Scene-by-scene script for the Transactional Outbox video.

Every explanation here has to work for somebody who is only listening, with the
video in a pocket. Nothing says "as you can see" and nothing depends on a class
name being visible: the narration names the actors, says what each one decides,
and describes the order things happen in.

Every number in these scenes comes from `./gradlew run`. Nothing is rounded and
nothing is invented.

Scenes 9 through 12 are the bill, and they are the reason the video exists.
Most explanations of this pattern stop at scene 8, with the message safely
delivered, and leave the room believing it has bought exactly-once delivery.
Do not cut or reorder them.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Transactional Outbox",
        body="",
        narration=(
            "This is the Transactional Outbox pattern, in Java, explained from "
            "scratch with a program you can run yourself. "
            "I am Jayasekhar Konduru, and this is part of a series on design "
            "patterns for services that talk to each other. "
            "The Transactional Outbox pattern says this: when you need to save "
            "something and also tell somebody about it, do not do two things. "
            "Write the announcement into your own database, in the same "
            "transaction as the data, and let a separate process post it later. "
            "In our online shop, that means the order row and the message that "
            "announces it are written by one commit, and the confirmation email "
            "goes out afterwards, from a message that was already safely stored."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="Two things that have to happen together",
        body=[
            "A customer checks out. Two things must now happen.",
            "",
            "One:  the order is saved, so the shop knows it exists.",
            "Two:  everybody else is told, so the email goes out,",
            "      the warehouse picks it, and the books balance.",
            "",
            "The first is a write to your database.",
            "The second is a message to a broker.",
            "",
            "They are two different systems.",
            "There is no transaction that covers both of them.",
            "And the obvious code does them on two separate lines.",
        ],
        narration=(
            "A customer presses buy. Two things have to happen now. The order has "
            "to be saved, so the shop knows it exists and can be charged for. And "
            "the rest of the business has to be told, so the confirmation email "
            "goes out, the warehouse picks the parcel, and the accounts balance at "
            "the end of the month. "
            "The first of those is a write to your own database. The second is a "
            "message to a broker, which is a different piece of software on a "
            "different machine. They are two systems, and no transaction covers "
            "both of them. "
            "The obvious code does them one after the other, on two lines. That is "
            "where we start."
        ),
    ),
    dict(
        key="03-two-lines",
        kind="code",
        title="The version everybody writes first",
        body="""public void placeOrder(Order order) {
    database.saveOnItsOwn(order);
    broker.publish(eventFor(order));
}

// Save it. Then announce it.
// Nobody would stop this in a review.""",
        narration=(
            "Here is what almost everybody writes first, and it is two lines long. "
            "Save the order to the database. Then publish an event to the broker "
            "saying the order was placed. "
            "Read that out loud and it sounds correct, because it is the order you "
            "would do it in yourself. It would pass a code review in any team I "
            "have worked in. Hold on to that, because in about a minute it is "
            "going to lose a customer's order without raising a single error."
        ),
    ),
    dict(
        key="04-act-one",
        kind="console",
        title="Act one — and it works",
        body="""Act 1 - save the order, then publish the event
      0ms ->     0ms  OrderDb   COMMIT   ord-8001 on its own
      0ms ->    15ms  Broker    OK       accepted msg-ord-8001
      7ms ->     7ms  Notifications  EMAILED  msg-ord-8001
  orders saved: 1, events delivered: 1, emails sent: 1

  two lines, and they did the right thing.
  This is what every test the author writes will see.""",
        narration=(
            "Act one runs those two lines. The order commits. The broker accepts "
            "the message fifteen milliseconds later. The notification service "
            "receives it and the email goes out. One order saved, one event "
            "delivered, one email sent. "
            "This is the important thing about act one: it is what every test "
            "written for this code will see. The author writes a test, it passes, "
            "and the code ships. Everything that goes wrong from here on goes "
            "wrong in production, to a real customer, on a path no test ever took."
        ),
    ),
    dict(
        key="05-act-two",
        kind="console",
        title="Act two — a deploy lands in the gap",
        body="""Act 2 - the same two lines, and a deploy in between
      0ms ->     0ms  OrderDb  COMMIT  ord-8002 on its own
      0ms ->     0ms  Orders   DIED    after the save,
                                      before the publish
  the order in the database:
    Order[orderId=ord-8002, customerId=cust-7, total=£70.95]
  events delivered: 0, emails sent: 0

  the order is real. The customer will be charged.
  Nobody will ever be told.""",
        narration=(
            "Act two runs exactly the same two lines, and this time the process "
            "dies in between them. A deploy landing in the middle of a request will "
            "do it, and a deploy landing mid request is one of the most ordinary "
            "reasons a request dies at all. "
            "Now count what is left. The order is in the database. It is a real "
            "order, for seventy pounds and ninety five pence, and the customer will "
            "be charged for it. Zero events were delivered and zero emails were "
            "sent. "
            "The order is real, the customer will be charged, and nobody will ever "
            "be told."
        ),
    ),
    dict(
        key="06-nothing-to-retry",
        kind="quote",
        title="Now ask what would retry it",
        body=[
            "Nothing will.",
            "",
            "Nothing anywhere recorded that a message was owed.",
            "There is no failed send sitting in a log.",
            "There is no row in a dead letter queue.",
            "There is no alert, because nothing errored.",
            "",
            "This is not a message that failed to send.",
            "It is a message that stopped existing.",
            "",
            "And you cannot retry something",
            "that was never written down.",
        ],
        narration=(
            "Now ask the question that matters, and sit with the answer. What "
            "would retry this? "
            "Nothing will. Nothing anywhere recorded that a message was owed. There "
            "is no failed send in a log, because the send was never attempted. "
            "There is no row in a dead letter queue, because nothing reached the "
            "queue. There is no alert, because nothing errored. "
            "This is not a message that failed to send. It is a message that "
            "stopped existing. And no amount of retry logic, monitoring, or "
            "cleverness can find something that was never written down anywhere. "
            "That is what makes this failure different from an ordinary outage."
        ),
    ),
    dict(
        key="07-the-tempting-fixes",
        kind="bullets",
        title="The two fixes somebody will suggest",
        body=[
            "\"Swap the lines. Publish first, then save.\"",
            "",
            "  The gap does not close. It moves.",
            "  Now a crash announces an order that does not exist,",
            "  and the warehouse picks a parcel nobody paid for.",
            "  You have chosen a different lie, not fewer lies.",
            "",
            "\"Wrap both lines in a transaction.\"",
            "",
            "  A database transaction covers the database.",
            "  The broker is a different process on a different",
            "  machine, and it will not join your transaction.",
        ],
        narration=(
            "Two fixes get suggested in every room, and both are worth taking "
            "seriously before taking apart. "
            "The first is to swap the lines. Publish first, then save. That does "
            "not close the gap; it moves it. Now a crash in the middle announces an "
            "order that does not exist, and the warehouse picks a parcel that "
            "nobody paid for. You have chosen a different lie, not fewer lies. "
            "The second is to wrap both lines in a transaction. But a database "
            "transaction covers the database. The broker is a separate program on a "
            "separate machine, and it is not going to join your transaction. There "
            "is no commit that spans the two of them."
        ),
    ),
    dict(
        key="08-the-out-tray",
        kind="quote",
        title="So think about an out-tray",
        body=[
            "You write a letter at your desk.",
            "",
            "You do not walk to the post box.",
            "You drop it in the out-tray, next to you,",
            "at the same moment you file your own copy.",
            "",
            "One action. Both things done.",
            "",
            "The post room comes round later and posts it.",
            "Door locked? It goes out on the next round.",
            "",
            "Your job ended when the letter hit the tray.",
        ],
        narration=(
            "So stop trying to make the broker part of your transaction, and think "
            "about an out-tray instead. "
            "You write a letter at your desk. You do not get up and walk to the "
            "post box. You drop the letter in the out-tray beside you, at the same "
            "moment you file your own copy of it. That is one action, and it does "
            "both things. "
            "Later, the post room comes round, takes what is in the tray, and posts "
            "it. If the post office is shut, the letter comes back and goes out on "
            "the next round. "
            "The important part is that your job ended the moment the letter hit "
            "the tray. Whether the post office is open is not your problem."
        ),
    ),
    dict(
        key="09-two-rows-one-commit",
        kind="code",
        title="The whole mechanism",
        body="""database.begin()
        .save(order)
        .save(outboxMessage)
        .commit();

// Two rows. One commit. Both, or neither.
// And no mention of the broker anywhere.""",
        narration=(
            "Here is the whole mechanism, and it is small enough to be "
            "disappointing. Begin a transaction. Save the order. Save the message "
            "as well, as an ordinary row in an ordinary table in your own database. "
            "Commit. "
            "Two rows, one commit. Because it is one commit, there is no instant at "
            "which one exists without the other. A crash before it leaves neither. "
            "A crash after it leaves both. "
            "And look at what is not in those four lines. There is no broker. The "
            "order service does not call it, does not import it, and does not know "
            "it exists. That absence is the pattern."
        ),
    ),
    dict(
        key="10-the-shape",
        kind="diagram",
        title="The shape of it",
        body="",
        narration=(
            "So the shape has two halves that run at different times. "
            "The first half is the checkout. The order service opens a transaction, "
            "writes the order row and the message row, and commits. Then it is "
            "finished, and the customer sees their confirmation page. "
            "The second half is a separate process called the relay. It reads the "
            "messages in the table that have not been sent, publishes each one to "
            "the broker, and marks each one as sent. "
            "The two halves share nothing but a table. One runs because a customer "
            "pressed a button. The other runs because a timer fired."
        ),
    ),
    dict(
        key="11-act-three",
        kind="console",
        title="Act three — one commit, then a sweep",
        body="""after the commit, before any sweep:
  orders saved: 1, waiting in the out-tray: 1,
  events delivered: 0

Orders never called the broker. Now the relay comes round:
      0ms ->     0ms  OrderDb  COMMIT  1 order and
                                      1 outbox message too
      0ms ->    15ms  Broker   OK      accepted msg-1
      7ms ->     7ms  Notifications  EMAILED  msg-1
     15ms ->    15ms  OrderDb  MARKED-SENT  msg-1
  published on that sweep: 1, still waiting: 0""",
        narration=(
            "Act three. After the checkout commits, and before anything else "
            "happens, there is one order saved, one message waiting in the out-tray, "
            "and zero events delivered. The order service never called the broker. "
            "Then the relay comes round. Read the timeline: one commit wrote the "
            "order and the message together. The broker accepted the message. The "
            "notification service sent the email. And the relay marked the message "
            "as sent. "
            "The customer got exactly the same email as in act one. What changed is "
            "that between the commit and the email there was no moment where the "
            "order existed and the message did not."
        ),
    ),
    dict(
        key="12-act-four",
        kind="console",
        title="Act four — the broker is down",
        body="""two customers checked out while the broker was
unreachable -- checkout does not depend on it
  first sweep, broker still down: published 0
  messages still in the out-tray: 2
  broker comes back. Second sweep: published 2
     15ms  Relay  LEFT-IN-TRAY  msg-1 -- broker down
     30ms  Relay  LEFT-IN-TRAY  msg-2 -- broker down
     45ms  Broker  OK  accepted msg-1
     60ms  Broker  OK  accepted msg-2
  events delivered: 2, emails sent: 2, still waiting: 0

  nobody wrote any retry logic.""",
        narration=(
            "Act four takes the broker away completely, and two customers check out "
            "while it is unreachable. Both checkouts succeed. They never needed the "
            "broker; they wrote two rows to a database and finished. In the version "
            "we started with, a broker outage would have been a checkout outage. "
            "The first sweep publishes nothing, because the broker will not answer, "
            "and both messages stay in the tray. The broker comes back, the second "
            "sweep publishes both, and both emails go out. "
            "Now go and look for the retry logic, because there is none. No backoff "
            "setting, no attempt counter, no scheduled retry table. A row that was "
            "not published is still an unsent row, so the next sweep picks it up "
            "again. The retry is not code. It is a consequence of where the message "
            "is kept."
        ),
    ),
    dict(
        key="13-act-five",
        kind="console",
        title="Act five — the bill",
        body="""the broker took the message. Emails sent: 1
but the relay died before writing down that it had,
so the out-tray still holds: 1
     15ms  Relay   DIED  after publishing msg-1,
                         before marking it sent
     15ms  Relay   RESTARTED
     30ms  Broker  OK    accepted msg-1
     30ms  OrderDb MARKED-SENT  msg-1
  times message msg-1 was delivered: 2
  emails in the customer's inbox: 2
    "your order ord-8006 for £70.95 is confirmed"
    "your order ord-8006 for £70.95 is confirmed\"""",
        narration=(
            "Act five is the bill, and this is the part most explanations leave "
            "out. "
            "The relay publishes a message. The broker takes it and the email goes "
            "out. And then the relay dies, before it can write down that it had "
            "sent it. The row is still marked unsent, because nothing ever marked "
            "it. So the relay restarts, reads the tray, finds that message still "
            "sitting there, and publishes it again. "
            "The message was delivered twice. The customer has two identical "
            "confirmation emails in their inbox for one order. Nothing failed, no "
            "test went red, and this is the pattern working exactly as designed."
        ),
    ),
    dict(
        key="14-at-least-once",
        kind="quote",
        title="Never lost, sometimes twice",
        body=[
            "Publishing and marking-as-sent are two systems.",
            "So there is a gap between them —",
            "the same gap, one level down.",
            "",
            "You cannot remove it. You can only choose",
            "which way it falls:",
            "  Mark sent first  →  a crash loses the message.",
            "  Publish first    →  a crash sends it twice.",
            "",
            "This pattern publishes first, deliberately,",
            "because a duplicate can be recovered from",
            "and a loss cannot. That is at-least-once.",
        ],
        narration=(
            "Here is why that duplicate cannot be engineered away. Publishing to "
            "the broker and marking the row as sent are in two different systems, "
            "so there is a gap between them. It is the same gap this pattern was "
            "invented to close, turning up again inside the fix. "
            "You cannot remove it. You can only choose which way it falls. Mark the "
            "row sent first, and a crash in the gap loses the message forever. "
            "Publish first, and a crash in the gap sends it twice. "
            "This pattern publishes first, on purpose, because a duplicate is "
            "something you can recover from and a loss is not. The name for that "
            "guarantee is at-least-once delivery. Say it out loud when you adopt "
            "this: never lost, sometimes twice. Anybody who tells you their outbox "
            "gives exactly-once has not looked at this gap."
        ),
    ),
    dict(
        key="15-the-handover",
        kind="console",
        title="What you owe whoever receives it",
        body="""note that the message id was the same both times.
That is the only thing a receiver needs
to spot the duplicate.

  first delivery:   msg-1
  second delivery:  msg-1

the fix is not in this project. It belongs to
whoever receives the message.

Two confirmation emails is embarrassing.
If the receiver were Payments,
it would be two charges.""",
        narration=(
            "The duplicate is not fixable on this side, and pretending otherwise is "
            "how teams end up believing in exactly-once. It belongs to whoever "
            "receives the message. "
            "What this side owes them is the ability to notice it, and it provides "
            "exactly one thing: the message identifier was identical both times. "
            "Same id, same message. A receiver that remembers which identifiers it "
            "has already handled can throw the second one away. That one stable "
            "field is the entire handover. "
            "And it matters more than it sounds. Two confirmation emails is "
            "embarrassing. If the thing receiving that message were the payments "
            "service, it would be two charges on somebody's card."
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Transactional Outbox",
        body=[
            "Write the message into your own database,",
            "in the same transaction as the data.",
            "Let a separate relay post it later.",
            "",
            "You get:  one atomic act, a checkout that",
            "          survives a broker outage, and",
            "          delivery without retry logic.",
            "",
            "You pay:  a little latency, a relay to run,",
            "          a table to keep clear —",
            "          and sometimes the same message twice.",
        ],
        narration=(
            "So, the Transactional Outbox. When you have to save something and also "
            "announce it, do not do two things. Write the announcement into your "
            "own database, as an ordinary row, in the same transaction as the data. "
            "Then let a separate relay read those rows and post them. "
            "What you get is three things. The data and its announcement are one "
            "atomic act, so nothing is silently lost. Your checkout keeps working "
            "when the broker does not, because it never talks to the broker. And "
            "every message is delivered eventually, without anybody writing a line "
            "of retry logic. "
            "What you pay is four things. The message goes out on the next sweep "
            "rather than immediately. Somebody has to run and watch the relay. The "
            "table grows and needs clearing out. And the same message will "
            "sometimes arrive twice. "
            "Everything is in the repository: the code, the five acts, the tests, "
            "and an animation you can step through. Run it, and pay particular "
            "attention to act five. Thanks for watching."
        ),
    ),
]
