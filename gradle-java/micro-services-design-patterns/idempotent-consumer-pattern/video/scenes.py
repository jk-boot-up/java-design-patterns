#!/usr/bin/env python3
"""Scene definitions for the Idempotent Consumer teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches, so no sentence points at the screen: the doorman
tearing the ticket is described in full before any class name is spoken, and
the console slides are read out as a story about what ended up in a customer's
inbox rather than as columns of numbers. The slides illustrate the narration;
they never carry it.

Every number quoted here comes from the real output of `./gradlew run`: two
confirmations for one order in acts two and three, one in act four, a hundred
and forty loyalty points for a seventy pound order, and a duplicate that gets
through once the thirty-second memory of it has expired.

Scene order is the argument. The video starts with the version everybody
writes, because the mechanism is boring until the room has watched a green test
ship a bug.

Two scenes must not be cut. Scene fourteen is the handler that needed no dedupe
store at all, and the rewrite from "add points" to "set points" -- a room that
leaves adding a dedupe table to every consumer has been made worse at this.
Scene fifteen is the expiry window, which is a number somebody chooses and
cannot derive, and it is the honest ending.

Layout limit: on "bullets" and "quote" slides the body starts at y=260 and
steps 60 pixels a line, and the footer sits at y~1022, so twelve body lines is
the maximum.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Idempotent Consumer",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Idempotent Consumer pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Idempotent means '
            'doing something twice has the same effect as doing it once. '
            '[[slnc 300]] An idempotent consumer is a service that can '
            'receive the same message twice, and the second time, nothing '
            'changes. [[slnc 300]] It does this by writing down that it '
            'handled the message, in the very same step as handling it. '
            '[[slnc 600]] Think of a lift button. [[slnc 300]] Press it '
            'once, and the lift is called. [[slnc 300]] Press it five '
            'more times, and it is still called just once. [[slnc 700]] '
            'In our online store, a message says an order was placed. '
            '[[slnc 300]] Handling it means sending a confirmation email. '
            '[[slnc 300]] The customer must get exactly one email. [[slnc '
            '300]] Even though the message system only promises to '
            'deliver each message at least once.'
        ),
    ),
    dict(
        key="02-at-least-once",
        kind="bullets",
        title="Why the same message arrives twice",
        body=[
            "A broker delivers a message and waits to be told",
            "it was handled.",
            "",
            "That acknowledgement goes missing. A blip. A timeout.",
            "A restart.",
            "",
            "The broker now cannot tell the difference between",
            "\"handled, and you didn't hear\" and \"never handled\".",
            "",
            "It has two choices. Send it again, or drop it.",
            "Every real broker sends it again.",
            "That is at-least-once delivery, and it is the contract.",
        ],
        narration=(
            "Let's start with the message system, not your code. [[slnc "
            '400]] A broker is a program that passes messages between '
            'services. [[slnc 300]] It hands a message to a service, and '
            'waits to be told it was handled. [[slnc 300]] That reply is '
            'called an acknowledgement. [[slnc 600]] Sometimes the '
            'acknowledgement never comes back. [[slnc 300]] A network '
            'hiccup, a timeout, or a restart. [[slnc 500]] Now the broker '
            'is stuck. [[slnc 300]] It cannot tell whether the message '
            'was handled and the reply got lost, or whether it never '
            'arrived at all. [[slnc 500]] It has two choices: send it '
            'again, or throw it away. [[slnc 300]] Almost every broker '
            'sends it again. [[slnc 300]] Because a duplicate can be '
            'recovered from, and a lost message cannot. [[slnc 300]] That '
            'is called at-least-once delivery. [[slnc 600]] So duplicates '
            'are not a bug someone will fix one day. [[slnc 300]] They '
            'are part of the deal. [[slnc 300]] And only the receiving '
            'service can deal with them.'
        ),
    ),
    dict(
        key="03-the-set",
        kind="code",
        title="The version everybody writes",
        body="""if (seen.contains(message.messageId())) {
    return;
}
seen.add(message.messageId());
database.queueConfirmationOnItsOwn(text);

// Keep the ids you have already handled.
// Skip anything you recognise.""",
        narration=(
            'The obvious answer is to keep a set of the message I Ds you '
            "have already handled. [[slnc 500]] If a message's I D is in "
            'the set, do nothing. [[slnc 300]] Otherwise, add it to the '
            'set, and queue the confirmation email. [[slnc 600]] That is '
            'a good instinct. [[slnc 300]] It is exactly the right idea. '
            '[[slnc 300]] It is only wrong about one thing. [[slnc 300]] '
            'And that thing is not what most people expect.'
        ),
    ),
    dict(
        key="04-act-one",
        kind="console",
        title="Act one — and it works",
        body="""Act 1 - the same OrderPlaced arrives twice
     10ms  Broker         REDELIVERY msg-1
                          the acknowledgement was lost
     15ms  Notifications  SKIPPED    msg-1 -- already seen
  confirmations queued: 1

  a HashSet of ids caught the duplicate. This is the
  test everybody writes, and it passes.""",
        narration=(
            'First demo. [[slnc 400]] The message is delivered. [[slnc '
            '300]] The confirmation is queued. [[slnc 300]] And the I D '
            'goes into the set. [[slnc 500]] Then the acknowledgement is '
            'lost. [[slnc 300]] So the broker sends the same message '
            'again. [[slnc 500]] The I D is recognised, and the second '
            'delivery is skipped. [[slnc 300]] One email, for one order. '
            '[[slnc 500]] The duplicate was caught. [[slnc 300]] The test '
            'passes. [[slnc 300]] And this is the version that gets '
            'released.'
        ),
    ),
    dict(
        key="05-act-two",
        kind="console",
        title="Act two — a deploy lands in between",
        body="""     10ms  Notifications  RESTARTED
                          and its memory of what it
                          has handled is empty
     15ms  NotifDb        COMMIT  a confirmation on its own
  confirmations queued: 2
    "your order ord-7002 for £70.95 is confirmed"
    "your order ord-7002 for £70.95 is confirmed"

  the database survived the deploy. The HashSet did not.""",
        narration=(
            'Second demo: the same two deliveries. [[slnc 300]] But this '
            'time, the service restarts in between. [[slnc 500]] The set '
            'of I Ds lives in memory, inside the running program. [[slnc '
            '300]] The restart empties it. [[slnc 500]] So when the '
            'second delivery arrives, the message looks brand new. [[slnc '
            '300]] And a second confirmation is queued. [[slnc 500]] The '
            'customer now has two identical emails, for one order of '
            'seventy pounds ninety-five. [[slnc 600]] Here is the '
            'sentence to remember. [[slnc 300]] The database survived the '
            'restart. [[slnc 300]] The set of I Ds did not.'
        ),
    ),
    dict(
        key="06-not-unlucky",
        kind="quote",
        title="And this is not bad luck",
        body=[
            "A restart is one of the most common reasons",
            "an acknowledgement goes missing in the first place.",
            "",
            "So the redelivery and the empty memory",
            "do not arrive independently.",
            "",
            "They arrive together,",
            "because the same event caused both.",
            "",
            "This is not the rare case.",
            "It is the ordinary case,",
            "waiting for your next deploy.",
        ],
        narration=(
            'It is tempting to call that bad luck. [[slnc 300]] Two '
            'unlikely things happening at once. [[slnc 300]] But it is '
            'not. [[slnc 600]] Think about why the acknowledgement went '
            'missing. [[slnc 300]] Very often, it went missing because '
            'the service restarted. [[slnc 500]] So one event caused both '
            'problems. [[slnc 300]] It caused the message to be sent '
            'again. [[slnc 300]] And it emptied the memory that should '
            'have caught it. [[slnc 500]] These two things usually arrive '
            'together. [[slnc 300]] This is not a rare case. [[slnc 300]] '
            'It is the normal case, waiting for your next release.'
        ),
    ),
    dict(
        key="07-act-three",
        kind="console",
        title="Act three — the gap, with no restart",
        body="""      5ms  NotifDb        COMMIT  a confirmation on its own
      5ms  Notifications  DIED    after queueing the email,
                                  before remembering the id
      5ms  Notifications  RESTARTED
     10ms  NotifDb        COMMIT  a confirmation on its own
  confirmations queued: 2

  two emails is embarrassing. Had this consumer been
  Payments, it would have been two charges.""",
        narration=(
            'Now take the restart away completely, because there is a '
            'second hole. [[slnc 500]] In the third demo, the service '
            'queues the confirmation. [[slnc 300]] Then it crashes, '
            'before it records the I D. [[slnc 500]] The email was '
            'queued. [[slnc 300]] But the I D was not remembered. [[slnc '
            '300]] So when the message comes again, it looks new, and a '
            'second email is queued. [[slnc 600]] Two writes, at two '
            'different moments, with a gap between them. [[slnc 300]] '
            'Anything that can crash can crash in that gap. [[slnc 600]] '
            'And think about the stakes. [[slnc 300]] Two confirmation '
            'emails is embarrassing. [[slnc 300]] If this had been the '
            "payment service, it would have been two charges on someone's "
            'card.'
        ),
    ),
    dict(
        key="08-one-cause",
        kind="quote",
        title="Two failures, one cause",
        body=[
            "In act two, the memory was in the wrong place:",
            "a field, not a database.",
            "",
            "In act three, it was written at the wrong moment:",
            "after the work, not with it.",
            "",
            "Both come down to the same sentence.",
            "",
            "Doing the work, and remembering that you did it,",
            "are being treated as two separate things.",
            "",
            "So stop treating them as two things.",
        ],
        narration=(
            'Put the two failures side by side. [[slnc 300]] They are '
            'really one failure. [[slnc 600]] In the second demo, the '
            "memory was in the wrong place. [[slnc 300]] In the program's "
            'memory, not in the database. [[slnc 500]] In the third demo, '
            'it was written at the wrong moment. [[slnc 300]] After the '
            'work, not with it. [[slnc 600]] Both come down to one '
            'sentence. [[slnc 300]] Doing the work, and remembering that '
            'you did it, are treated as two separate things. [[slnc 500]] '
            'So the fix is to stop treating them as two things.'
        ),
    ),
    dict(
        key="09-one-commit",
        kind="code",
        title="The whole mechanism",
        body="""database.begin()
        .queueConfirmation(confirmationFor(message))
        .recordHandled(message.messageId())
        .commit();

// Two rows. One commit. Both, or neither.""",
        narration=(
            'Here is the whole mechanism, and it is small. [[slnc 500]] '
            'Open a database transaction. [[slnc 300]] A transaction is a '
            'group of changes that are saved together, or not at all. '
            '[[slnc 500]] Queue the confirmation. [[slnc 300]] Record the '
            'message I D as handled. [[slnc 300]] Then save, which is '
            'called a commit. [[slnc 600]] Two rows, one commit. [[slnc '
            '300]] So there is never a moment when one exists without the '
            'other. [[slnc 300]] And the record lives in the same '
            'database as the email. [[slnc 300]] So it outlives any '
            'restart.'
        ),
    ),
    dict(
        key="10-the-shape",
        kind="diagram",
        title="The shape of it",
        body=None,
        narration=(
            'Here is the shape of it, in words. [[slnc 500]] A broker '
            'delivers a message to a consumer. [[slnc 300]] And it may '
            'deliver the same one again, at any time. [[slnc 500]] The '
            'consumer asks the database, not its own memory, whether it '
            'has already handled this I D. [[slnc 300]] If it has, it '
            'does nothing at all. [[slnc 300]] If it has not, it opens '
            'one transaction. [[slnc 300]] It writes the email and the I '
            'D together, and commits. [[slnc 600]] Beside it are two '
            'other consumers, which make the opposite point. [[slnc 300]] '
            'One sets a shipment status, and needs no memory at all. '
            '[[slnc 300]] The other awards loyalty points, and can be '
            'rewritten until it needs none either. [[slnc 300]] We will '
            'come back to both.'
        ),
    ),
    dict(
        key="11-act-four",
        kind="console",
        title="Act four — one commit, and the redelivery",
        body="""      5ms  NotifDb        COMMIT   1 confirmation(s) and
                                    1 handled id(s) together
     10ms  Broker         REDELIVERY msg-1
     15ms  Notifications  IGNORED  msg-1 -- handled already
  confirmations queued: 1, handled ids stored: 1

  now the same two failures that beat the HashSet:
    after a restart, confirmations queued: 1
    died before the commit: 0 confirmation(s), 0 id(s)
    after the redelivery, confirmations queued: 1""",
        narration=(
            'Fourth demo: the same story, with the I D saved inside the '
            'same commit. [[slnc 500]] One confirmation and one handled I '
            'D are written together. [[slnc 300]] The message is sent '
            'again. [[slnc 300]] The consumer finds the I D already '
            'stored, and ignores it. [[slnc 300]] Nothing is written. '
            '[[slnc 300]] One email. [[slnc 600]] Now the demo repeats '
            'the two failures that beat the set of I Ds. [[slnc 500]] '
            'First, a restart between the deliveries. [[slnc 300]] Still '
            'one confirmation. [[slnc 300]] Because the memory is in the '
            'database, and the database did not restart. [[slnc 500]] '
            'Second, a crash before the commit. [[slnc 300]] Nothing at '
            'all was written: no email, and no I D. [[slnc 300]] That '
            'sounds bad, but it is exactly right. [[slnc 300]] The '
            'message is sent again, and it really has not been handled. '
            '[[slnc 300]] So it is handled cleanly, and committed. [[slnc '
            '300]] Still one confirmation.'
        ),
    ),
    dict(
        key="12-exactly-once",
        kind="quote",
        title="Exactly once, out of at least once",
        body=[
            "The broker promised only that the message",
            "would arrive at least once.",
            "",
            "It kept that promise. It arrived twice.",
            "",
            "The customer received exactly one email.",
            "",
            "And notice where the exactly-once lives.",
            "Not in the broker.",
            "Not in the network.",
            "",
            "In one ordinary database transaction, on your side.",
        ],
        narration=(
            'Say the result out loud, because it is worth keeping. [[slnc '
            '500]] The broker only promised to deliver the message at '
            'least once. [[slnc 300]] It kept that promise, by sending it '
            'twice. [[slnc 300]] And the customer received exactly one '
            'email. [[slnc 600]] Exactly-once handling, from '
            'at-least-once delivery. [[slnc 500]] And notice where the '
            'exactly-once lives. [[slnc 300]] Not in the broker. [[slnc '
            '300]] Not in the network. [[slnc 300]] Not in a framework '
            'someone sold you. [[slnc 300]] In one ordinary database '
            'transaction, in your own service. [[slnc 500]] So next time '
            'someone offers you exactly-once delivery, remember this. '
            '[[slnc 300]] They are usually selling this same idea, built '
            'somewhere else.'
        ),
    ),
    dict(
        key="13-did-you-need-it",
        kind="console",
        title="Act five — the handler that needed none of it",
        body="""  status of ord-7006: SHIPPED, orders known: 1
  no dedupe store, no transaction, no expiry policy.
  Setting a status twice sets the same status.

  and one that is not: "add 70 loyalty points" twice
    running total: 140 points for a 70 pound order

  rewritten as "set the points for this order to 70":
    points awarded: 70 after handling it twice""",
        narration=(
            'Fifth demo. [[slnc 300]] Before adding any of this, ask '
            'whether the consumer even needs it. [[slnc 600]] Here is one '
            "that does not. [[slnc 300]] A handler that sets a shipment's "
            'status to shipped. [[slnc 300]] Deliver that message twice, '
            'and the status is still shipped. [[slnc 300]] No memory, no '
            'transaction, nothing to run. [[slnc 300]] It is naturally '
            'idempotent. [[slnc 300]] And when that is possible, it is '
            'always the better answer. [[slnc 600]] Here is one that is '
            'not, but could be. [[slnc 300]] Add seventy loyalty points '
            'for an order. [[slnc 300]] Handle that twice, and the '
            'customer has a hundred and forty points, for a seventy-pound '
            'order. [[slnc 500]] Now rewrite it. [[slnc 300]] Instead of: '
            'add seventy points. [[slnc 300]] Say: set the points for '
            'this order to seventy. [[slnc 300]] Handle that twice, and '
            'the customer has seventy. [[slnc 500]] Same result, and a '
            'duplicate cannot get it wrong. [[slnc 300]] Reaching for a '
            'table of handled I Ds before asking this question is the '
            'most common mistake here.'
        ),
    ),
    dict(
        key="14-the-window",
        kind="console",
        title="And the store's own cost",
        body="""  and the dedupe store's own cost, which is a guess:
    handled, confirmations queued: 1
    a minute later, with a thirty second memory,
    the same message arrives again: 2 confirmation(s)

  ids cannot be kept forever, so they expire, and the
  window is chosen rather than derived.
  too short and a duplicate after a long broker outage
  looks new; too long and it is a large table
  somebody operates.""",
        narration=(
            'When you do need the table of handled I Ds, be honest about '
            'what it costs. [[slnc 500]] Every handled I D is a row. '
            '[[slnc 300]] And the table grows for as long as messages '
            'arrive. [[slnc 300]] So old rows must be cleared out. [[slnc '
            '300]] That means someone owns a clean-up job, and gets '
            'called when it stops. [[slnc 600]] Then this. [[slnc 300]] '
            'The demo handles a message. [[slnc 300]] It keeps I Ds for '
            'only thirty seconds. [[slnc 300]] A minute later, the same '
            'message arrives again. [[slnc 300]] Two confirmations. '
            '[[slnc 500]] The duplicate came back after the memory of it '
            'had expired, so it looked new. [[slnc 600]] That is not a '
            'bug. [[slnc 300]] It is the trade. [[slnc 300]] Too short a '
            'window, and a late duplicate gets through. [[slnc 300]] Too '
            'long, and you run a very large table. [[slnc 300]] There is '
            'no correct number to calculate. [[slnc 300]] There is a '
            'number you choose, and must be able to defend.'
        ),
    ),
    dict(
        key="15-the-handover",
        kind="quote",
        title="What the sender owes you",
        body=[
            "One thing. A stable message id.",
            "",
            "The same message, delivered twice,",
            "carrying the same id both times.",
            "",
            "That single field is everything",
            "the receiving side needs to notice the duplicate.",
            "",
            "Nothing else about the message has to be reliable.",
            "Nothing else has to be compared.",
            "",
            "One field, and one transaction.",
        ],
        narration=(
            'One last thing, and it is the smallest part of the pattern. '
            '[[slnc 400]] What does the sending side owe you? [[slnc '
            '500]] Just one thing: a stable message I D. [[slnc 300]] The '
            'same message, delivered twice, must carry the same I D both '
            'times. [[slnc 500]] That one field is everything the '
            'receiver needs. [[slnc 300]] You do not compare the contents '
            'of the message. [[slnc 300]] You just look up one I D. '
            '[[slnc 500]] One field from the sender. [[slnc 300]] And one '
            'transaction on your side.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Idempotent Consumer",
        body=[
            "Write the record of having handled the message",
            "in the same transaction as its effect.",
            "Both, or neither.",
            "",
            "You get:  a redelivery that changes nothing,",
            "          a deploy that cannot forget,",
            "          a crash that leaves nothing half done.",
            "",
            "You pay:  a table somebody operates, and",
            "          an expiry window that is a guess.",
            "",
            "And first: ask whether you needed it at all.",
        ],
        narration=(
            "That's the Idempotent Consumer pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Write '
            'the record of handling a message in the same transaction as '
            'its effect: both, or neither. [[slnc 600]] What you get. '
            '[[slnc 300]] A repeated message changes nothing. [[slnc '
            '300]] A restart cannot make the consumer forget. [[slnc '
            '300]] And a crash never leaves work half done. [[slnc 500]] '
            'What you pay. [[slnc 300]] A table that grows, which someone '
            'must run and clear out. [[slnc 300]] And a time window, '
            'which is a number you choose. [[slnc 500]] And before any of '
            'that, ask the cheaper question. [[slnc 300]] Could this '
            'handler be rewritten to set a value, instead of adding to '
            'one? [[slnc 600]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
