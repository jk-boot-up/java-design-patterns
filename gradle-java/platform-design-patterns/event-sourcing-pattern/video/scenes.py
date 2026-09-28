"""Scene definitions for the Event Sourcing teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the analogy is spoken in full before any class
name, and the code slides are described in words rather than read out as
syntax. The slides illustrate the narration; they never carry it.

This pattern is the most over-applied one in the series, so the running order
gives the costs as much room as the benefits: scenes 11, 12 and 13 are the
bill, and they are not a footnote.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Event Sourcing",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Event Sourcing pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Event sourcing stores the '
            'things that happened, in order, and never changes them. '
            '[[slnc 300]] The current state is worked out by adding those '
            'things up, whenever someone asks. [[slnc 300]] The total is '
            'not something you keep. [[slnc 300]] It is something you '
            'calculate. [[slnc 600]] Think of a bank statement. [[slnc '
            '300]] The bank does not just send you a number. [[slnc 300]] '
            'It sends a list of payments, with a running total down the '
            'side. [[slnc 700]] In our online store, we look at the '
            'loyalty points scheme. [[slnc 300]] A customer rings up and '
            'asks why their balance is a hundred and forty. [[slnc 500]] '
            'By the end, you will know why a stored total can never '
            'explain itself. [[slnc 300]] How a bug found three weeks '
            'late is investigated with a question nobody planned. [[slnc '
            '300]] And the four things this pattern costs, because most '
            'systems should not use it.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The shop runs a loyalty scheme.",
            "",
            "    One point for every pound spent.",
            "    Points can be spent on later orders.",
            "    Unused points expire after twelve months.",
            "",
            "There is a table. It has one row per customer.",
            "The row has a number in it.",
            "",
            "    C-4417        140",
            "",
            "A customer rings up and asks why it is 140.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] The shop runs a very '
            'simple loyalty scheme. [[slnc 300]] You earn one point for '
            'every pound you spend. [[slnc 300]] You can spend points on '
            'a later order. [[slnc 300]] And points you have not used '
            'within twelve months expire. [[slnc 600]] The shop stores it '
            'the usual way. [[slnc 300]] A table, with one row per '
            'customer, holding one number. [[slnc 300]] One customer has '
            'a hundred and forty points. [[slnc 500]] And that number is '
            'correct. [[slnc 300]] This is not a broken system. [[slnc '
            '600]] Then one afternoon, the customer rings up with a '
            'reasonable question. [[slnc 300]] Why is it a hundred and '
            'forty?'
        ),
    ),
    dict(
        key="03-problem",
        kind="code",
        title="The Naive Approach — Keep the Total",
        body="""public void award(String customerId, int points,
                  String orderId, LocalDate on) {

    this.points.merge(customerId, points, Integer::sum);
}
// Four facts arrive.  One is used.
// The order id reached this method and went no further.
// So did the date.  Both are gone.""",
        narration=(
            'Here is the method that adds points to a customer. [[slnc '
            '300]] It is one line long. [[slnc 500]] It receives four '
            'things: the customer, the number of points, which order '
            'earned them, and the date. [[slnc 300]] Then it adds the '
            "points to the customer's total, and stops. [[slnc 600]] So "
            'four facts arrive. [[slnc 300]] Only one is used. [[slnc '
            '300]] The order number and the date reach the code, and are '
            'simply dropped. [[slnc 500]] Nobody wrote a bug. [[slnc '
            '300]] This is just what storing only the current state does. '
            '[[slnc 300]] It keeps the answer, and throws away the '
            'working. [[slnc 300]] And every interesting question is '
            'about the working.'
        ),
    ),
    dict(
        key="04-why-hurts",
        kind="console",
        title="What the Row Can Say",
        body="""Act 1 - a customer asks why their balance is 140
  balance: 140
  support asks why, and this is the whole answer:
    the row says 140 points. How it got there was
    never written down.
  the four things that happened in March were each
  added to a number and then forgotten.""",
        narration=(
            'First demo: a support agent tries to answer the customer. '
            '[[slnc 400]] The balance is a hundred and forty. [[slnc '
            '300]] And the whole explanation is: the row says a hundred '
            'and forty. [[slnc 300]] How it got there was never written '
            'down. [[slnc 600]] Four things happened to this customer in '
            'March. [[slnc 300]] Each was added to a number, and then '
            'forgotten. [[slnc 600]] The usual fix is an audit log: a '
            'second table, recording what happened. [[slnc 300]] That '
            'helps. [[slnc 300]] But an audit log is a second copy of the '
            'truth. [[slnc 300]] And copies drift apart. [[slnc 300]] '
            'When they disagree, you cannot tell which one is wrong.'
        ),
    ),
    dict(
        key="05-the-bug",
        kind="console",
        title="Three Weeks Later, a Bug",
        body="""Act 2 - a release awards points twice, and nobody
        notices for three weeks
  the fix is out. Now find the customers it touched:
    C-5120 = 100 points
    C-5122 = 25 points
    C-5121 = 60 points

  which of those three is wrong, and by how much?
  100 could be a doubled £45 order on top of £10,
  or one honest £100 order. Both write 100.
  the information needed to tell them apart was
  overwritten by the bug itself.""",
        narration=(
            'Second demo: a worse story. [[slnc 400]] A new release has a '
            'bug. [[slnc 300]] For three weeks, every order awards its '
            'points twice. [[slnc 300]] Then someone spots it, and the '
            'fix is one line. [[slnc 600]] The hard part is this. [[slnc '
            '300]] Which customers were affected, and by how much? [[slnc '
            '500]] Three customers have balances of a hundred, '
            'twenty-five, and sixty. [[slnc 300]] Which of those is '
            'wrong? [[slnc 600]] You cannot tell. [[slnc 300]] A doubled '
            'forty-five-pound order, plus an earlier ten-pound order, '
            'gives a hundred. [[slnc 300]] One honest hundred-pound order '
            'also gives a hundred. [[slnc 300]] They look exactly the '
            'same. [[slnc 600]] The bug did not just cause damage. [[slnc '
            '300]] Every time it ran, it also erased the evidence of the '
            'damage.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Pattern",
        body=[
            "Store what happened,",
            "not what the total is.",
            "",
            "Then add it up when somebody asks.",
        ],
        narration=(
            'So here is the idea. [[slnc 400]] Nobody ever told this '
            'system: the customer has a hundred and forty points. [[slnc '
            '300]] What it was told was a list of events. [[slnc 300]] '
            'Sixty earned on the first. [[slnc 200]] Twenty-five spent on '
            'the third. [[slnc 200]] A hundred and twenty earned on the '
            'eighth. [[slnc 200]] Fifteen expired on the fourteenth. '
            '[[slnc 500]] The hundred and forty is just arithmetic done '
            'on those facts. [[slnc 300]] And then the facts were thrown '
            'away, and only the arithmetic kept. [[slnc 600]] Event '
            'sourcing does it the other way round. [[slnc 300]] Keep the '
            'facts. [[slnc 300]] Do the arithmetic when someone asks. '
            '[[slnc 500]] Every benefit, and every cost, in this video '
            'comes from that one sentence.'
        ),
    ),
    dict(
        key="07-three-moves",
        kind="bullets",
        title="Three Moves",
        body=[
            "1.  Make each change a fact, named in the past tense.",
            "        PointsAwarded, not AwardPoints.",
            "        A command can be refused.  A fact cannot.",
            "",
            "2.  Append it to a log, and never touch it again.",
            "        One operation: add to the end.",
            "        No update.  No delete.",
            "",
            "3.  Derive the state by folding the log.",
            "        Start at zero, walk the events, add them up.",
            "        There is no balance field anywhere.",
        ],
        narration=(
            'In practice, it is three moves. [[slnc 600]] One. [[slnc '
            '200]] Make each change a fact, with a name, in the past '
            'tense. [[slnc 300]] Not: add sixty points. [[slnc 300]] But: '
            'sixty points were awarded to this customer, on the first of '
            'March, for this order. [[slnc 300]] An instruction can be '
            'refused. [[slnc 300]] A fact cannot, because it already '
            'happened. [[slnc 600]] Two. [[slnc 200]] Add it to the end '
            'of a log, and never touch it again. [[slnc 300]] The log has '
            'no update, and no delete. [[slnc 300]] The past does not '
            'change, so the record of it must not change either. [[slnc '
            '600]] Three, the one that feels strange at first. [[slnc '
            '200]] The current balance is not stored anywhere. [[slnc '
            '300]] When someone asks, start at zero, go through the '
            "customer's events in order, and add each one. [[slnc 300]] "
            'Ask again, and it is worked out again. [[slnc 500]] That '
            'sounds wasteful, and sometimes it is. [[slnc 300]] But '
            "first, let's hear what it buys."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 300]] There are four. [[slnc "
            '600]] First, the event. [[slnc 300]] It is just a fact, with '
            'no logic in it. [[slnc 300]] There are three kinds: points '
            'awarded, points redeemed, and points expired. [[slnc 300]] '
            'Each carries everything needed to understand it, including '
            'the order number and the date. [[slnc 500]] Second, the '
            'event store, which is the log. [[slnc 300]] You can add to '
            'it, and read it, but never change it. [[slnc 500]] Third, '
            'the class that turns events into a balance. [[slnc 300]] It '
            'has no stored balance at all. [[slnc 300]] Every number it '
            'gives is worked out on the spot. [[slnc 500]] Fourth, a '
            'snapshot store. [[slnc 300]] It is a cache, and never the '
            'truth. [[slnc 300]] We will come back to it, because it is '
            'where this pattern gets dangerous. [[slnc 600]] Checkout, '
            'which calls all this, cannot tell which design is behind it. '
            '[[slnc 300]] This is a choice about storage, not about the '
            'calling code.'
        ),
    ),
    dict(
        key="09-fold",
        kind="code",
        title="The Fold — and Why It Is 140",
        body="""int running = 0;
for (LoyaltyEvent event : store.eventsFor(customerId)) {
    running += event.effectOnBalance();
}
return running;

// 2025-03-01  earned 60 points on ORD-8801    balance 60
// 2025-03-03  spent 25 points on ORD-8814     balance 35
// 2025-03-08  earned 120 points on ORD-8907   balance 155
// 2025-03-14  lost 15 to the expiry           balance 140""",
        narration=(
            'Here is how the balance is worked out, in words. [[slnc '
            '400]] Start a running total at zero. [[slnc 300]] For each '
            "of the customer's events, add its effect on the balance. "
            '[[slnc 300]] Return the total. [[slnc 500]] That loop is the '
            'balance. [[slnc 300]] There is no other balance. [[slnc '
            '600]] Now print each step, not just the answer. [[slnc 500]] '
            'First of March: earned sixty points. [[slnc 300]] Balance, '
            'sixty. [[slnc 400]] Third of March: spent twenty-five. '
            '[[slnc 300]] Balance, thirty-five. [[slnc 400]] Eighth of '
            'March: earned a hundred and twenty. [[slnc 300]] Balance, a '
            'hundred and fifty-five. [[slnc 400]] Fourteenth of March: '
            'fifteen points expired. [[slnc 300]] Balance, a hundred and '
            'forty. [[slnc 600]] A support agent can read that down the '
            'phone. [[slnc 300]] It even explains the expiry, which is '
            'the question support dreads most. [[slnc 300]] Nobody wrote '
            'that explanation. [[slnc 300]] It is the sum, showing its '
            'working.'
        ),
    ),
    dict(
        key="10-investigation",
        kind="console",
        title="The Query Nobody Wrote in Advance",
        body="""Act 3 - the same bug, with an append-only log behind it
  balance as the log stands: 100 points
  orders that earned points more than once:
    ORD-9001 awarded 2 times
  nobody wrote that query before the bug shipped.
  It was written after, and the data was already there.
  balance with the second award ignored: 55 points
  no event was edited and none was deleted. The reading
  code changed, and every balance is right again.""",
        narration=(
            'Third demo: the same bug, with a log behind it. [[slnc 400]] '
            'The buggy release recorded two award events instead of one. '
            '[[slnc 300]] And two events never look like one. [[slnc '
            '600]] Three weeks later, someone writes a brand new '
            'question. [[slnc 300]] For this customer, find any order '
            'that earned points more than once. [[slnc 300]] The answer: '
            'order nine thousand and one, awarded twice. [[slnc 600]] '
            'That question was invented after the fact. [[slnc 300]] And '
            'it could be answered, because the data was already in the '
            'log. [[slnc 300]] Nobody predicted it. [[slnc 300]] Nobody '
            'built a table for it. [[slnc 600]] Then the repair. [[slnc '
            "300]] Count each order's award only once, and the balance is "
            'fifty-five, not a hundred. [[slnc 500]] And here is the key '
            'point. [[slnc 300]] No event was edited, or deleted, or '
            'added. [[slnc 300]] The log is exactly the same as before. '
            '[[slnc 500]] The log was never wrong. [[slnc 300]] The shop '
            'really did award those points twice. [[slnc 300]] What was '
            'wrong was how the log was read. [[slnc 300]] So the fix '
            'lives in the reading code, and history stays history.'
        ),
    ),
    dict(
        key="11-cost-replay",
        kind="console",
        title="The Bill — Reading Gets Expensive",
        body="""Act 6 - the bill: a stream long enough to need a snapshot
  events in the log: 5000
  one balance, folded from the start:
                       500 points, 5000 events read
  one more order, folded from the start again:
                       502 points, 5001 events read
  the same 502 points, from the snapshot plus what
  came after it:                     1 event read
  that is the fix, and it is also a second place
  a balance lives.""",
        narration=(
            'That is what you gain. [[slnc 300]] Now the bill, and it is '
            'large. [[slnc 600]] Four events is nothing. [[slnc 300]] '
            'Five thousand is not. [[slnc 300]] Working out one balance '
            'from the start reads all five thousand events. [[slnc 300]] '
            'Every time anyone asks. [[slnc 600]] The fix is a snapshot. '
            '[[slnc 300]] Save the balance as it stood at event five '
            'thousand. [[slnc 300]] The next read starts there, and reads '
            'one new event instead of five thousand. [[slnc 300]] Same '
            'answer, far less work. [[slnc 600]] But notice what a '
            'snapshot is. [[slnc 300]] It is a stored balance. [[slnc '
            '300]] The very thing this pattern set out to stop keeping, '
            'brought back for speed. [[slnc 500]] So in this project, '
            'each snapshot records which event it was taken at. [[slnc '
            '300]] And which version of the code calculated it. [[slnc '
            '300]] That second part matters more than it seems.'
        ),
    ),
    dict(
        key="12-cost-snapshot",
        kind="bullets",
        title="The Bill — A Snapshot Can Be Quietly Wrong",
        body=[
            "A snapshot taken by buggy reading code",
            "stays wrong for ever.",
            "",
            "    stale snapshot:  90 points",
            "    correct fold:    45 points",
            "",
            "Nothing throws.  Nothing warns.",
            "A wrong balance is just a number.",
            "",
            "The cure:  throw every snapshot away and refold.",
            "It is cheap only because the log kept everything.",
            "",
            "The log is the truth.  A snapshot is a cache.",
        ],
        narration=(
            'Here is how a snapshot goes wrong, silently. [[slnc 500]] '
            'Suppose a snapshot is taken while the double-counting bug is '
            'still in the reading code. [[slnc 300]] It records ninety '
            'points. [[slnc 300]] Then the fix lands. [[slnc 300]] Adding '
            'up the log correctly now gives forty-five. [[slnc 600]] The '
            'log is right. [[slnc 300]] The adding up is right. [[slnc '
            '300]] And the snapshot is wrong, forever, and nothing tells '
            'you. [[slnc 300]] No error, no warning, no failed test. '
            '[[slnc 300]] A wrong balance is just a number, and numbers '
            'do not look wrong. [[slnc 600]] The cure is blunt, and '
            'correct. [[slnc 300]] Throw every snapshot away, and add the '
            'log up again. [[slnc 300]] You can only do that because the '
            'log kept everything. [[slnc 600]] So here is the rule. '
            '[[slnc 300]] The log is the truth. [[slnc 300]] A snapshot '
            'is a cache you may always delete. [[slnc 300]] The moment '
            'anyone treats a snapshot as the record, you are back where '
            'you started.'
        ),
    ),
    dict(
        key="13-cost-erasure",
        kind="bullets",
        title="The Bill — Erasure, and Old Events",
        body=[
            "A customer asks to be erased.",
            "The log has no delete.",
            "",
            "\"Just remove their events\" does two things:",
            "    their history is gone beyond recovery, and",
            "    a snapshot still answers with their balance.",
            "",
            "Somebody added the order id field in 2023.",
            "Events written before it never gain it.",
            "",
            "    0 duplicates found — in a stream that",
            "    plainly contains two identical awards.",
        ],
        narration=(
            'Two more costs, the kind you meet years later. [[slnc 600]] '
            'The first is erasure. [[slnc 300]] A customer has a legal '
            'right to be forgotten. [[slnc 300]] And the log has no '
            'delete. [[slnc 500]] The obvious idea is: just remove their '
            'events. [[slnc 300]] That destroys their history forever, '
            'which the system was built to prevent. [[slnc 300]] And an '
            'old snapshot still holds their balance, so their data is '
            'still there. [[slnc 500]] The real answers are harder. '
            '[[slnc 300]] Encrypt personal details inside each event, and '
            'destroy the key when asked. [[slnc 300]] Or keep the event, '
            'but blank out who it was. [[slnc 300]] Either way, it must '
            'be designed in before the first event is ever written. '
            '[[slnc 600]] The second cost is versioning. [[slnc 300]] The '
            'order number field was only added in twenty twenty-three. '
            '[[slnc 300]] Older events do not have it, and never will. '
            '[[slnc 500]] So the duplicate search finds zero duplicates '
            'in an old stream, even when two identical awards are clearly '
            'there. [[slnc 300]] And it reports that calmly. [[slnc 300]] '
            'Every reader you ever write carries that gap forever.'
        ),
    ),
    dict(
        key="14-not-cqrs",
        kind="bullets",
        title="Event Sourcing Is Not CQRS",
        body=[
            "CQRS with no event sourcing:",
            "    writes go to a row,",
            "    reads come from a second model built for the screen.",
            "    No event log anywhere.",
            "",
            "Event sourcing with no CQRS:",
            "    writes append events,",
            "    reads fold the same events back.",
            "    No second model at all.",
            "",
            "CQRS changes where reads come from.",
            "Event sourcing changes what the writes store.",
        ],
        narration=(
            'One more thing, because two patterns are often confused. '
            '[[slnc 500]] C Q R S means reads and writes come from '
            'different models. [[slnc 300]] This project has a small '
            'class that does exactly that, with no event log at all. '
            '[[slnc 300]] Writes update a row, and reads come from a '
            'second model, shaped for the screen. [[slnc 300]] That is C '
            'Q R S, without event sourcing. [[slnc 600]] And the main '
            'class here does the opposite. [[slnc 300]] It stores events, '
            'and answers reads by adding up those same events. [[slnc '
            '300]] One model. [[slnc 300]] That is event sourcing, '
            'without C Q R S. [[slnc 600]] So here are two sentences '
            'worth remembering. [[slnc 300]] C Q R S changes where reads '
            'come from. [[slnc 300]] Event sourcing changes what writes '
            'store. [[slnc 500]] They often appear together. [[slnc 300]] '
            'But you can have either one without the other.'
        ),
    ),
    dict(
        key="15-wrapup",
        kind="bullets",
        title="When to Reach for It",
        body=[
            "Ask one question:",
            "",
            "    Will anybody ever need to know how this",
            "    number got to be what it is?",
            "",
            "A basket, a settings page, a stock level  ->  no.",
            "Keep the number.  This pattern is a large bill",
            "for nothing.",
            "",
            "Money, loyalty, orders, anything an auditor",
            "can ask about  ->  yes.  There the history",
            "is the product.",
        ],
        narration=(
            'So, when should you use this? [[slnc 400]] Ask one question. '
            '[[slnc 300]] Will anyone ever need to know how this number '
            'got to be what it is? [[slnc 600]] A shopping basket, a '
            'settings page, a stock level? [[slnc 300]] No. [[slnc 300]] '
            'Nobody will audit those. [[slnc 300]] Keep the number. '
            '[[slnc 300]] For those, this pattern is a large bill for '
            'nothing. [[slnc 600]] Money, loyalty points, orders, or '
            'anything an auditor might ask about? [[slnc 300]] Yes. '
            '[[slnc 300]] There, the history is not overhead. [[slnc '
            '300]] The history is the product. [[slnc 600]] This pattern '
            'is often used where it should not be. [[slnc 300]] That is '
            'why so much of this video is about its costs.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that fixes",
            "the same bug by appending a correcting event instead,",
            "and the awkward question of which repair you would rather",
            "explain to an auditor.",
        ],
        narration=(
            "That's the Event Sourcing pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Store '
            'what happened, not the total, and work the total out when '
            'asked, but remember that snapshots, erasure, and old events '
            'all have a price. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Fix the double-award '
            'bug a different way. [[slnc 300]] Instead of changing how '
            'the log is read, add a new event that takes the extra points '
            'back. [[slnc 300]] Then ask: which repair would you rather '
            'explain to an auditor? [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
