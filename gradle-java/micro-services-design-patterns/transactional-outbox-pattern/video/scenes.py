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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Transactional Outbox pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Sometimes you need '
            'to save something, and also tell others about it. [[slnc '
            '300]] The outbox says: do not do two separate things. [[slnc '
            '300]] Write the announcement into your own database, in the '
            'same step as the data. [[slnc 300]] Then let a separate '
            'process send it out later. [[slnc 600]] Think of an office '
            'out-tray. [[slnc 300]] You drop the letter in the tray, and '
            'the post room sends it later. [[slnc 700]] In our online '
            'store, the order, and the message announcing it, are saved '
            'together. [[slnc 300]] And the confirmation email goes out '
            'afterwards, from a message that was already safely stored.'
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
            'A customer presses buy. [[slnc 300]] Now two things must '
            'happen. [[slnc 500]] The order must be saved, so the shop '
            'knows it exists, and can charge for it. [[slnc 300]] And the '
            'rest of the business must be told. [[slnc 300]] So the email '
            'goes out, the warehouse packs the parcel, and the accounts '
            'balance. [[slnc 600]] The first is a write to your own '
            'database. [[slnc 300]] The second is a message to a broker: '
            'a separate program, on a separate machine, that passes '
            'messages on. [[slnc 500]] They are two systems. [[slnc 300]] '
            'And no single transaction covers both. [[slnc 500]] The '
            'obvious code does them one after the other, in two lines. '
            '[[slnc 300]] That is where we start.'
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
            'Here is what almost everyone writes first. [[slnc 300]] Two '
            'lines. [[slnc 500]] Save the order to the database. [[slnc '
            '300]] Then send a message to the broker, saying the order '
            'was placed. [[slnc 600]] That sounds correct. [[slnc 300]] '
            'It is the order you would do it in yourself. [[slnc 300]] It '
            'would pass any code review. [[slnc 500]] Remember that. '
            '[[slnc 300]] Because in about a minute, it will lose a '
            "customer's order without a single error."
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
            'First demo: the two lines. [[slnc 400]] The order is saved. '
            '[[slnc 300]] The broker accepts the message fifteen '
            'milliseconds later. [[slnc 300]] The notification service '
            'receives it, and the email goes out. [[slnc 500]] One order '
            'saved. [[slnc 200]] One message delivered. [[slnc 200]] One '
            'email sent. [[slnc 600]] Here is the important point. [[slnc '
            '300]] This is what every test written for this code will '
            'see. [[slnc 300]] The test passes, and the code is released. '
            '[[slnc 300]] Everything that goes wrong from here happens in '
            'production, to a real customer, on a path no test ever took.'
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
            'Second demo: exactly the same two lines. [[slnc 300]] But '
            'this time, the program dies between them. [[slnc 500]] A new '
            'release landing in the middle of a request will do it. '
            '[[slnc 300]] And that is one of the most ordinary ways a '
            'request dies. [[slnc 600]] Now count what is left. [[slnc '
            '300]] The order is in the database. [[slnc 300]] It is a '
            'real order, for seventy pounds ninety-five, and the customer '
            'will be charged. [[slnc 500]] No messages were delivered. '
            '[[slnc 300]] No emails were sent. [[slnc 500]] The order is '
            'real. [[slnc 300]] The customer will be charged. [[slnc '
            '300]] And nobody will ever be told.'
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
            'Now ask the question that matters. [[slnc 300]] What would '
            'retry this? [[slnc 600]] Nothing will. [[slnc 500]] Nothing '
            'anywhere recorded that a message was owed. [[slnc 300]] '
            'There is no failed send in a log, because the send was never '
            'attempted. [[slnc 300]] There is nothing in a queue of '
            'failed messages, because nothing reached the queue. [[slnc '
            '300]] There is no alert, because nothing went wrong that '
            'anything could see. [[slnc 600]] This is not a message that '
            'failed to send. [[slnc 300]] It is a message that stopped '
            'existing. [[slnc 500]] And no retry logic, monitoring, or '
            'cleverness can find something that was never written down.'
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
            'Two fixes get suggested in every room. [[slnc 300]] Both are '
            'worth taking seriously, before we take them apart. [[slnc '
            '600]] The first: swap the lines. [[slnc 300]] Send the '
            'message first, then save. [[slnc 500]] That does not close '
            'the gap. [[slnc 300]] It moves it. [[slnc 300]] Now a crash '
            'in the middle announces an order that does not exist. [[slnc '
            '300]] And the warehouse packs a parcel nobody paid for. '
            '[[slnc 300]] You have chosen a different lie, not fewer '
            'lies. [[slnc 600]] The second: wrap both lines in a '
            'transaction. [[slnc 500]] But a database transaction only '
            'covers the database. [[slnc 300]] The broker is a separate '
            'program, on a separate machine. [[slnc 300]] It will not '
            'join your transaction. [[slnc 300]] No single save covers '
            'both.'
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
            'So stop trying to make the broker part of your transaction. '
            '[[slnc 300]] Think about an out-tray instead. [[slnc 600]] '
            'You write a letter at your desk. [[slnc 300]] You do not '
            'walk to the post box. [[slnc 300]] You drop the letter in '
            'the out-tray beside you, at the same moment you file your '
            'own copy. [[slnc 300]] One action, and both things are done. '
            '[[slnc 600]] Later, the post room comes round, and posts '
            'what is in the tray. [[slnc 300]] If the post office is '
            'shut, the letter goes out on the next round. [[slnc 500]] '
            'Your job ended the moment the letter hit the tray. [[slnc '
            '300]] Whether the post office is open is not your problem.'
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
            'Here is the whole mechanism, and it is small. [[slnc 500]] '
            'Start a database transaction. [[slnc 300]] Save the order. '
            '[[slnc 300]] Save the message too, as an ordinary row, in an '
            'ordinary table, in your own database. [[slnc 300]] Then '
            'commit, which means save both together. [[slnc 600]] Two '
            'rows, one commit. [[slnc 300]] So there is never a moment '
            'when one exists without the other. [[slnc 300]] A crash '
            'before the commit leaves neither. [[slnc 300]] A crash after '
            'it leaves both. [[slnc 600]] And notice what is missing. '
            '[[slnc 300]] There is no broker. [[slnc 300]] The order '
            'service does not call it, and does not even know it exists. '
            '[[slnc 300]] That absence is the pattern.'
        ),
    ),
    dict(
        key="10-the-shape",
        kind="diagram",
        title="The shape of it",
        body="",
        narration=(
            'The shape has two halves, which run at different times. '
            '[[slnc 600]] The first half is checkout. [[slnc 300]] The '
            'order service opens a transaction, writes the order and the '
            'message, and commits. [[slnc 300]] Then it is finished, and '
            'the customer sees their confirmation page. [[slnc 600]] The '
            'second half is a separate process, called the relay. [[slnc '
            '300]] It reads the messages that have not been sent yet. '
            '[[slnc 300]] It sends each one to the broker. [[slnc 300]] '
            'And it marks each one as sent. [[slnc 600]] The two halves '
            'share nothing but a table. [[slnc 300]] One runs because a '
            'customer pressed a button. [[slnc 300]] The other runs '
            'because a timer went off.'
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
            'Third demo: one commit, then a sweep. [[slnc 400]] After the '
            'checkout commits, and before anything else happens, there is '
            'one order saved. [[slnc 300]] One message waiting in the '
            'out-tray. [[slnc 300]] And no messages delivered. [[slnc '
            '300]] The order service never called the broker. [[slnc '
            '600]] Then the relay comes round. [[slnc 300]] The broker '
            'accepts the message. [[slnc 300]] The notification service '
            'sends the email. [[slnc 300]] And the relay marks the '
            'message as sent. [[slnc 600]] The customer got exactly the '
            'same email as in the first demo. [[slnc 300]] What changed '
            'is this. [[slnc 300]] There was never a moment when the '
            'order existed, and the message did not.'
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
            'Fourth demo: the broker is down. [[slnc 400]] Two customers '
            'check out while the broker cannot be reached. [[slnc 500]] '
            'Both checkouts succeed. [[slnc 300]] They never needed the '
            'broker. [[slnc 300]] They wrote two rows to a database, and '
            'finished. [[slnc 300]] In the two-line version, a broker '
            'outage would have been a checkout outage. [[slnc 600]] The '
            "relay's first sweep sends nothing, because the broker will "
            'not answer. [[slnc 300]] Both messages stay in the tray. '
            '[[slnc 500]] The broker comes back. [[slnc 300]] The second '
            'sweep sends both, and both emails go out. [[slnc 600]] Now '
            'look for the retry logic. [[slnc 300]] There is none. [[slnc '
            '300]] A message that was not sent is still an unsent row. '
            '[[slnc 300]] So the next sweep simply picks it up again. '
            '[[slnc 500]] The retry is not code. [[slnc 300]] It comes '
            'from where the message is kept.'
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
            'Fifth demo: the bill. [[slnc 300]] Most explanations leave '
            'this part out. [[slnc 600]] The relay sends a message. '
            '[[slnc 300]] The broker takes it, and the email goes out. '
            '[[slnc 300]] And then the relay dies, before it can mark the '
            'message as sent. [[slnc 600]] So the row is still marked '
            'unsent. [[slnc 300]] The relay restarts, reads the tray, and '
            'finds that message still there. [[slnc 300]] So it sends it '
            'again. [[slnc 600]] The message was delivered twice. [[slnc '
            '300]] The customer has two identical confirmation emails, '
            'for one order. [[slnc 500]] Nothing failed. [[slnc 300]] No '
            'test went red. [[slnc 300]] And this is the pattern working '
            'exactly as designed.'
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
            'Here is why that duplicate cannot be designed away. [[slnc '
            '500]] Sending to the broker, and marking the row as sent, '
            'happen in two different systems. [[slnc 300]] So there is a '
            'gap between them. [[slnc 300]] It is the same gap this '
            'pattern was invented to close, turning up again inside the '
            'fix. [[slnc 600]] You cannot remove it. [[slnc 300]] You can '
            'only choose which way it falls. [[slnc 500]] Mark the row '
            'sent first, and a crash in the gap loses the message '
            'forever. [[slnc 300]] Send first, and a crash in the gap '
            'sends it twice. [[slnc 600]] This pattern sends first, on '
            'purpose. [[slnc 300]] Because a duplicate can be recovered '
            'from, and a loss cannot. [[slnc 500]] That promise is called '
            'at-least-once delivery. [[slnc 300]] Say it out loud when '
            'you adopt this: never lost, sometimes twice.'
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
            'The duplicate cannot be fixed on this side. [[slnc 300]] It '
            'belongs to whoever receives the message. [[slnc 600]] What '
            'this side owes them is a way to notice it. [[slnc 300]] And '
            'it provides exactly one thing. [[slnc 300]] The message I D '
            'was the same both times. [[slnc 500]] Same I D, same '
            'message. [[slnc 300]] A receiver that remembers which I Ds '
            'it has already handled can throw the second one away. [[slnc '
            '300]] That one stable field is the whole handover. [[slnc '
            '600]] And it matters more than it sounds. [[slnc 300]] Two '
            'confirmation emails is embarrassing. [[slnc 300]] If the '
            'receiver were the payment service, it would be two charges '
            "on someone's card."
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
            "That's the Transactional Outbox pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Save '
            'the message in your own database, in the same transaction as '
            'the data, and let a separate relay send it later. [[slnc '
            '600]] What you get. [[slnc 300]] The data and its '
            'announcement are saved together, so nothing is silently '
            'lost. [[slnc 300]] Checkout keeps working when the broker '
            'does not. [[slnc 300]] And every message is eventually '
            'delivered, without any retry code. [[slnc 600]] What you '
            'pay. [[slnc 300]] The message goes out on the next sweep, '
            'not immediately. [[slnc 300]] Someone must run and watch the '
            'relay. [[slnc 300]] The table grows, and needs clearing out. '
            '[[slnc 300]] And the same message will sometimes arrive '
            'twice. [[slnc 600]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 300]] Pay '
            'special attention to the fifth demo. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
