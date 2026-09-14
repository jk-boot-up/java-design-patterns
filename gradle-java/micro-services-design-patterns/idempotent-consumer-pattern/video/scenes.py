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
            "This is the Idempotent Consumer pattern, in Java, explained from "
            "scratch with a program you can run yourself. "
            "I am Jayasekhar Konduru, and this is part of a series on design "
            "patterns for services that talk to each other. "
            "The Idempotent Consumer pattern says this: when the same message "
            "reaches you twice, handling it the second time should change "
            "nothing — and you get that by writing down that you have handled "
            "it in the very same act as handling it. "
            "In our online shop, the message says an order was placed and the "
            "handling means queueing a confirmation email. The customer must "
            "end up with exactly one email, out of a message system that only "
            "promises to deliver at least once."
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
            "Start with the message system, not with your code. "
            "A broker hands a message to a service and waits to be told it was "
            "handled. Sometimes that acknowledgement never comes back — a "
            "network blip, a timeout, a restart. "
            "The broker is now stuck. It cannot tell the difference between a "
            "message that was handled perfectly well and an acknowledgement "
            "that got lost, and a message that never arrived at all. It has two "
            "choices: send it again, or throw it away. "
            "Every broker you are likely to use sends it again, because sending "
            "twice is something you can recover from and losing a message is "
            "not. That is called at-least-once delivery. "
            "So duplicates are not a bug somebody will eventually fix. They are "
            "the deal, and the receiving end is the only place that can do "
            "anything about them."
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
            "The obvious answer is a set of the message identifiers you have "
            "already handled. If the identifier is in the set, return and do "
            "nothing. Otherwise add it to the set and queue the confirmation "
            "email. "
            "That is a good instinct. It is exactly the right idea about what "
            "to do. Hold on to it, because it is wrong about one thing only, "
            "and the wrong thing is not what most people expect."
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
            "Act one runs it. The message is delivered, the confirmation is "
            "queued, and the identifier goes into the set. Then the "
            "acknowledgement is lost, so the broker sends the same message "
            "again. The identifier is recognised, the second delivery is "
            "skipped, and one confirmation is queued. "
            "One email for one order. The duplicate was caught. The test is "
            "green, and this is the version that ships."
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
            "Act two runs the same two deliveries, and this time the process "
            "restarts in between them. "
            "The set of identifiers lives in a field, in memory, inside that "
            "process. The restart empties it. So when the second delivery "
            "arrives, the message looks completely new, and a second "
            "confirmation is queued. "
            "The customer now has two identical emails for one order, seventy "
            "pounds and ninety five pence, sent twice. "
            "Say the reason in one sentence, because it is the sentence to "
            "remember: the database survived the deploy, and the set of "
            "identifiers did not."
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
            "It would be comforting to file that under bad luck — two unlikely "
            "things happening at once. It is not. "
            "Think about why the acknowledgement went missing. Very often, it "
            "went missing because the process restarted. Which means the same "
            "event caused the redelivery and emptied the memory that was "
            "supposed to catch it. "
            "So these two do not arrive independently. They arrive together, "
            "much more often than chance would suggest. This is not the rare "
            "case you can shrug at. It is the ordinary case, waiting for your "
            "next deploy."
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
            "Now take the restart out of the argument entirely, because there "
            "is a second hole. "
            "In act three the consumer queues the confirmation, and then dies "
            "before it gets round to recording the identifier. The email was "
            "queued. The identifier was not remembered. So when the message "
            "comes again, it looks new, and a second email is queued. "
            "Two writes, at two different moments, with a gap between them. "
            "Anything that can die can die in that gap. "
            "And be clear about the stakes. Two confirmation emails is "
            "embarrassing. If this consumer had been the payments service, it "
            "would have been two charges on somebody's card."
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
            "Put the two failures side by side, because they are really one "
            "failure wearing two coats. "
            "In act two, the memory of having handled the message was in the "
            "wrong place: a field in a process, rather than a database. "
            "In act three, it was written at the wrong moment: after the work, "
            "rather than with it. "
            "Both reduce to the same sentence. Doing the work, and remembering "
            "that you did the work, are being treated as two separate things. "
            "So the fix is to stop treating them as two things."
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
            "Here is the whole mechanism, and it is small enough to be "
            "disappointing. "
            "Open a transaction. Queue the confirmation. Record the message "
            "identifier as handled. Commit. "
            "Two rows, one commit. Because it is one commit there is no instant "
            "where one exists without the other. And the record now lives in "
            "the same database as the effect, which means it outlives the "
            "process that wrote it."
        ),
    ),
    dict(
        key="10-the-shape",
        kind="diagram",
        title="The shape of it",
        body=None,
        narration=(
            "So the shape is this. A broker delivers a message to a consumer, "
            "and may deliver the same one again at any time. "
            "The consumer asks the database, not its own memory, whether it has "
            "already handled this identifier. If it has, it does nothing at "
            "all. If it has not, it opens one transaction, writes the effect "
            "and the identifier together, and commits. "
            "Alongside it sit two other consumers that make the opposite point. "
            "One sets a shipment status and needs no store of any kind. The "
            "other awards loyalty points, and can be rewritten until it needs "
            "none either. We will come back to both."
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
            "Act four runs the same story with the record inside the commit. "
            "One confirmation and one handled identifier are written together. "
            "The redelivery arrives, the consumer finds the identifier already "
            "stored, and ignores it. Nothing is written. One email. "
            "Then the demo throws the two failures that beat the set of "
            "identifiers straight at it. "
            "Restart the process between the deliveries: still one "
            "confirmation, because the memory is in the database and the "
            "database did not restart. "
            "Kill the process before the commit: nothing at all was written, no "
            "confirmation and no identifier. That sounds like a loss, but it is "
            "the opposite. Because nothing was written, the redelivery finds a "
            "message that genuinely has not been handled, does the work "
            "cleanly, and commits. Still one confirmation."
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
            "Say the result out loud, because it is the sentence worth keeping. "
            "The broker promised only that the message would arrive at least "
            "once, and it kept that promise by sending it twice. The customer "
            "received exactly one email. "
            "Exactly-once processing, out of at-least-once delivery. "
            "And notice where that exactly-once actually lives. It is not in "
            "the broker, and it is not in the network, and it is not in a "
            "framework somebody sold you. It is in one ordinary database "
            "transaction, in your own service, doing a thing databases have "
            "done for forty years. "
            "Which is worth knowing the next time somebody offers you "
            "exactly-once delivery. What they are selling is usually this, "
            "built somewhere else."
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
            "Before you add any of this to a consumer, ask whether that "
            "consumer needs it. "
            "Here is one that does not. A handler that sets a shipment's status "
            "to shipped. Deliver that message twice and the status is shipped. "
            "No store, no transaction, no expiry policy, nothing to operate. "
            "That is a naturally idempotent operation, and it is always the "
            "better answer when it is available. "
            "And here is one that is not, but could be. Awarding seventy "
            "loyalty points for an order. Handle that twice and the customer "
            "has a hundred and forty points for a seventy pound order. "
            "Now rewrite it. Instead of add seventy points, say set the points "
            "for this order to seventy. Handle that twice and the customer has "
            "seventy. Same business outcome, and a duplicate simply cannot get "
            "it wrong. "
            "Reaching for a dedupe table before asking that question is the "
            "most common mistake in this whole area."
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
            "And when you do need the store, be honest about what it costs. "
            "Every handled identifier is a row, and the table grows for as long "
            "as messages arrive. So the rows have to be cleared out, which "
            "means somebody owns a retention job and somebody gets paged when "
            "it stops running. "
            "Then this. The demo handles a message, waits a minute with a "
            "memory that only keeps identifiers for thirty seconds, and "
            "delivers the same message again. Two confirmations. The duplicate "
            "came back after the memory of it had expired, so it looked new. "
            "That is not a bug in the demo. It is the shape of the trade. Too "
            "short a window and a duplicate arriving after a long broker outage "
            "gets through. Too long and you are operating a very large table. "
            "There is no correct number to derive. There is a number you choose "
            "and have to be able to defend."
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
            "One last thing, and it is the smallest part of the pattern. "
            "What does the sending side owe you? One thing: a stable message "
            "identifier. The same message, delivered twice, has to carry the "
            "same identifier both times. "
            "That single field is everything the receiving side needs. You do "
            "not have to compare the contents of the message. You do not have "
            "to hash anything, or reason about whether two messages are really "
            "the same. You look up one identifier. "
            "One field from the sender, and one transaction on your side. That "
            "is the entire handover."
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
            "So, the Idempotent Consumer. Handling the same message twice has "
            "the same effect as handling it once, and you buy that by writing "
            "the record of having handled it in the same transaction as its "
            "effect. Both, or neither. "
            "What you get is three things. A redelivery changes nothing. A "
            "deploy cannot make the consumer forget, because the memory is in "
            "the database. And a crash never leaves half-done work, because "
            "there is only one commit to be on one side or the other of. "
            "What you pay is two things. A table that grows with every message, "
            "which somebody has to operate and clear out. And an expiry window, "
            "because those identifiers cannot be kept forever — a number you "
            "choose rather than derive, with a real duplicate getting through "
            "on one side of it and a very large table on the other. "
            "And before any of that, ask the cheaper question: is this handler "
            "already idempotent, or could it be rewritten until it is? Setting "
            "a value rather than adding to one costs nothing to operate. "
            "Everything is in the repository: the code, the five acts, the "
            "tests, and an animation you can step through. Thanks for watching."
        ),
    ),
]
