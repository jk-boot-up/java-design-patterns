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
            "Hello, and welcome. This video explains the Event Sourcing design "
            "pattern in Java, and it is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] Let's start with the simple definition. Event "
            "sourcing means storing the things that happened, in the order they "
            "happened, and never changing them — and then working out the current "
            "state by adding those things up when somebody asks. The total is not "
            "a thing you keep. It is a thing you calculate. [[slnc 350]] Think of "
            "a bank statement. The bank does not send you a number; it sends you a "
            "list, with a running total down the side. The number at the bottom is "
            "the only thing on the page you could have worked out from the rest. "
            "[[slnc 350]] That's the idea in a sentence. The rest of the video "
            "does it properly, by building a real working Java project: the "
            "loyalty points scheme of an online shop, where a customer rings up "
            "and asks why their balance is a hundred and forty. [[slnc 250]] By "
            "the end you'll know why a stored total can never explain itself, how "
            "a bug found three weeks late gets investigated with a query nobody "
            "wrote in advance, and — just as importantly — the four things this "
            "pattern will cost you, because most systems should not use it."
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
            "So, imagine an online shop with a loyalty scheme, and it is the "
            "simplest scheme you could design. [[slnc 250]] You earn one point for "
            "every pound you spend. You can spend those points on a later order. "
            "And anything you have not used within twelve months expires. [[slnc "
            "300]] The shop stores it the way almost everybody stores it: a table "
            "with one row per customer, and the row has a number in it. Customer "
            "C four four one seven has a hundred and forty points. [[slnc 350]] "
            "That number is correct. I want to be really clear about that, because "
            "I am not going to show you a broken system and then rescue it. The "
            "row is right, it has always been right, and it will still be right in "
            "five years. [[slnc 300]] And then one afternoon that customer rings "
            "up and asks a question that sounds completely reasonable. Why is it a "
            "hundred and forty?"
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
            "Here is the method that adds points to a customer, and it is one line "
            "long. [[slnc 250]] It takes four things: the customer, how many "
            "points, which order earned them, and the date it happened. And then "
            "the body of the method adds the points to the customer's total, and "
            "stops. [[slnc 350]] Read those two halves against each other, because "
            "this is the whole problem in miniature. Four facts arrive at that "
            "method. One of them is used. The order number and the date reach the "
            "code, go no further, and are dropped on the floor. [[slnc 300]] "
            "Nobody wrote a bug. Nobody was careless. That line is what a "
            "current-state design is: it keeps the answer and it discards the "
            "working. [[slnc 300]] And the reason that matters is that the working "
            "is what every interesting question is about."
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
            "So here is the first act of the demo, and it is the support agent "
            "trying to answer that customer. [[slnc 250]] The balance is a hundred "
            "and forty. And the entire rest of the answer is: the row says a "
            "hundred and forty points, and how it got there was never written "
            "down. [[slnc 350]] Four things happened to that customer in March. "
            "Each one was added to a number, and then forgotten. There is nobody "
            "left to ask, and there is no file to look in. [[slnc 300]] Now, the "
            "usual response to this is to add an audit log — a second table, "
            "written alongside the first, recording what happened. And that does "
            "help. But hold onto one thing about it, because we will come back to "
            "it: an audit log is a second copy of the truth. And second copies "
            "drift. The day the two disagree, you will have no way of knowing "
            "which one is lying."
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
            "And now the worse story, which is the one that makes this pattern "
            "worth paying for. [[slnc 250]] A release goes out with a bug in it: "
            "for three weeks, every order awards its points twice. Then somebody "
            "spots it, and the fix itself is easy — one line. [[slnc 300]] The "
            "hard part is what comes next. Which customers were affected, and by "
            "how much? [[slnc 300]] Look at three balances. One customer has a "
            "hundred points, one has twenty-five, one has sixty. Which of those is "
            "wrong? [[slnc 350]] You cannot tell, and here is why. A doubled "
            "forty-five pound order sitting on top of an earlier ten pound one "
            "writes the number one hundred. And one honest hundred pound order "
            "also writes the number one hundred. The two are the same row. "
            "[[slnc 350]] The information you would need to tell them apart was "
            "destroyed by the bug itself, as it ran. That is the thing to sit with "
            "for a second. The bug did not just cause damage — it erased the "
            "evidence of the damage, every time it fired."
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
            "So here is the move. [[slnc 300]] Notice that the balance was never "
            "something the shop was told. Nobody ever said to this system, this "
            "customer has a hundred and forty points. What the shop was told was: "
            "they earned sixty on the first, they spent twenty-five on the third, "
            "they earned a hundred and twenty on the eighth, and fifteen expired on "
            "the fourteenth. The hundred and forty is arithmetic the shop did on "
            "those four facts, and then it threw the facts away and kept the "
            "arithmetic. [[slnc 400]] Event sourcing is the decision to do that the "
            "other way round. Keep the facts. Do the arithmetic when somebody asks. "
            "[[slnc 350]] And that is the whole pattern. Everything else in this "
            "video — every benefit, and every single one of the costs — falls out "
            "of that one sentence."
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
            "In practice it is three moves, and the third is the one people "
            "struggle with. [[slnc 300]] First: make each change a fact, with a "
            "name, in the past tense. Not add sixty to the balance, but sixty "
            "points were awarded to this customer, on the first of March, for this "
            "order. And the past tense is not a style preference. Award points, as "
            "an instruction, is something that can be refused. Points were "
            "awarded, as a fact, cannot be refused, because it already happened. "
            "Everything in the log is the second kind. [[slnc 400]] Second: append "
            "it to a log, and then never touch it again. The log has exactly one "
            "way to write to it, which is to add to the end. There is no update "
            "and there is no delete, and that absence is the design. The past does "
            "not change, so the record of the past must not change either. "
            "[[slnc 400]] Third, and this is the one that feels wrong at first: "
            "the current state is not stored anywhere at all. When somebody asks "
            "for the balance, you start at zero, walk the customer's events in "
            "order, apply each one, and return what you end up with. Ask again a "
            "second later, and that whole walk happens again. [[slnc 350]] It "
            "sounds wasteful. Sometimes it genuinely is, and we will price it "
            "properly later. But look first at what it buys you."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let me name the parts, because there are only four and they each do "
            "one thing. [[slnc 300]] There is the event. It is a fact — it has no "
            "behaviour, no opinion and no logic in it. In this project there are "
            "exactly three kinds: points awarded, points redeemed, and points "
            "expired. Each one carries everything needed to understand it, "
            "including the order number and the date, copied inside it rather than "
            "pointed at, so that reading it in three years' time tells you what was "
            "true then rather than what is true now. [[slnc 400]] There is the "
            "event store, which is the log. It has append, and it has reads, and it "
            "has no way to change anything. [[slnc 300]] There is the class that "
            "turns events into a balance, and the striking thing about it is what "
            "it does not have. Go looking for a field holding the balance and there "
            "isn't one. Every number it gives you is worked out on the spot. "
            "[[slnc 350]] And off to one side there is a snapshot store, which is a "
            "cache, and which is never the truth. We will come back to it, because "
            "it is where this pattern gets dangerous. [[slnc 300]] The caller — the "
            "checkout — sees none of this. It talks to an interface, and it cannot "
            "tell which of the two designs is behind it. That is deliberate: the "
            "choice we are making is a choice about storage, not about the code "
            "that calls it."
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
            "This is the fold, and it is five lines. Start a running total at zero. "
            "For each of the customer's events, add that event's effect on the "
            "balance. Return the running total. [[slnc 350]] That loop is the "
            "balance. There is no other balance. [[slnc 300]] And now watch what "
            "happens when you print the same walk instead of only its answer. "
            "[[slnc 250]] On the first of March, earned sixty points on order "
            "eight eight oh one — balance sixty. On the third, spent twenty-five — "
            "balance thirty-five. On the eighth, earned a hundred and twenty — "
            "balance a hundred and fifty-five. On the fourteenth, lost fifteen "
            "points to the twelve-month expiry — balance a hundred and forty. "
            "[[slnc 400]] A support agent can read that down the phone. And notice "
            "the last line especially, because where did my points go is the call "
            "support dreads most, and here the expiry explains itself along with "
            "everything else. [[slnc 300]] That is not a stored explanation that "
            "somebody remembered to write. It is the sum, printing itself as it "
            "goes."
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
            "Now back to that bug, with a log behind it this time. [[slnc 300]] The "
            "double-awarding release ran, and it left behind two events instead of "
            "one — and two events never look like one. [[slnc 300]] So three weeks "
            "later somebody sits down and writes a query that did not exist when "
            "the bug was live: group this customer's awards by order number, and "
            "tell me about any order that earned points more than once. Order nine "
            "thousand and one, awarded twice. [[slnc 350]] Think about what just "
            "happened there. The question was invented after the fact, and it was "
            "answerable, because the data it needed was already lying in the log. "
            "Nobody predicted the question. Nobody built a table for it. [[slnc "
            "400]] And then the repair. Count each order's award once, and the "
            "balance is fifty-five instead of a hundred. [[slnc 300]] Here is the "
            "line I would like you to take away from this whole video: no event was "
            "edited, and none was deleted. Nothing was appended either. The log "
            "before the repair and the log after it are identical. [[slnc 350]] "
            "Because the log was never wrong. The shop really did award those "
            "points twice — that really is what happened, and pretending otherwise "
            "would be falsifying the record. What was wrong was the interpretation. "
            "So the fix lives in the code that interprets, and history stays "
            "history."
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
            "Right. That is what you gain, and now the bill, because every pattern "
            "has one and this one's is large. [[slnc 350]] Four events is nothing. "
            "Five thousand is not. Folding from the beginning to answer one balance "
            "reads all five thousand events, and it does it again every single time "
            "anybody asks. [[slnc 300]] The fix is a snapshot: save the balance as "
            "it stood at event five thousand, and the next read starts from there "
            "and walks one event instead of five thousand. Same answer, three "
            "orders of magnitude less work. [[slnc 400]] But look at what a "
            "snapshot actually is. It is a stored balance. It is precisely the "
            "thing this pattern set out to stop doing, brought back in through the "
            "side door for performance. [[slnc 350]] Which is why, in this project, "
            "a snapshot records two things about itself: which event it was taken "
            "at, and which code computed it. That second one matters more than it "
            "looks."
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
            "Here is how that goes wrong, and it is worth a slide of its own "
            "because it is silent. [[slnc 300]] Suppose a snapshot gets taken while "
            "the double-awarding interpretation is still in use. It records ninety "
            "points. Then the repair lands, and folding the log correctly now gives "
            "forty-five. [[slnc 350]] The log is right. The fold is right. And the "
            "snapshot is wrong, permanently, and nothing anywhere tells you. There "
            "is no exception, no warning, no failed test — because a wrong balance "
            "is just a number, and numbers do not look wrong. [[slnc 400]] The cure "
            "is blunt and it is the correct one: throw every snapshot away and add "
            "the log up again. And you can only afford to do that because the log "
            "kept everything. [[slnc 300]] So if you take one rule from this "
            "section, take this one. The log is the truth. A snapshot is a cache "
            "you are always allowed to delete. The moment anybody starts treating "
            "a snapshot as the record, you have quietly gone back to the design "
            "we started with, and this time with two of them."
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
            "Two more costs, and both are the kind you meet years in rather than in "
            "week one. [[slnc 350]] The first is erasure. A customer has a legal "
            "right to be forgotten, and your log has no delete in it. The first "
            "thing everybody reaches for is: fine, we will make an exception and "
            "remove their events. [[slnc 300]] That does two things, and neither is "
            "what you wanted. Their history is destroyed beyond any recovery, which "
            "is the one thing you built this system to prevent. And a snapshot "
            "taken last week still holds their balance and will still happily "
            "report it — so the data you just deleted is still in the building. "
            "[[slnc 400]] The real answers are harder. Encrypt the personal fields "
            "inside the event and then destroy the key. Or keep the shape of the "
            "event and blank the identity out of it. Both of those have to be "
            "designed in before the first event is ever written, not after the "
            "first request arrives. [[slnc 400]] The second cost is versioning. "
            "Somebody added the order number field in twenty twenty-three. Every "
            "event written before that does not have it, and never will, because "
            "you cannot go back and fill in information that was not recorded. "
            "[[slnc 350]] Which means that duplicate hunt we were so pleased with "
            "reports zero duplicates on a stream that visibly contains two "
            "identical awards — and reports it perfectly calmly. An event is a "
            "schema you version and never migrate, and every reader you write from "
            "then on carries that gap for ever."
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
            "One last thing, because these two patterns get treated as one idea "
            "constantly, and it makes people argue about the wrong trade-off. "
            "[[slnc 350]] C Q R S — command query responsibility segregation — "
            "means reads and writes come from different models. In this project "
            "there is a small class that does exactly that, with no event log "
            "anywhere near it: writes update a row, and reads come from a second "
            "model shaped for the screen that displays it. That is CQRS, complete, "
            "with no event sourcing in it at all. Its own cost is drift — if the "
            "update to the read side is lost, nothing throws, and the customer sees "
            "an empty history next to a balance that is not zero. [[slnc 400]] And "
            "the main class in this project is the opposite: it stores events, and "
            "it answers reads by folding those very same events. One model. That is "
            "event sourcing, complete, with no CQRS in it at all. [[slnc 350]] So "
            "here are the two sentences, and they are worth memorising. CQRS "
            "changes where reads come from. Event sourcing changes what the writes "
            "store. [[slnc 300]] They do turn up together often, because a log is "
            "an awkward thing to read from directly and a second model fixes that. "
            "But often together is not the same thing, and you can have either one "
            "without the other."
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
            "So, when should you actually reach for this? [[slnc 300]] There is one "
            "question, and it is not a technical one. Will anybody ever need to know "
            "how this number got to be what it is? [[slnc 350]] A shopping basket. A "
            "settings page. A stock level on a shelf. No — nobody is going to audit "
            "those, and keeping the number is the right design. For those, this "
            "pattern is a large bill for nothing, and I would push back on anyone "
            "who proposed it. [[slnc 400]] Money. Loyalty points. Orders. Anything a "
            "regulator or an auditor can ask you about, or anything where somebody "
            "will one day say: prove it. There, the history is not overhead. The "
            "history is the product, and storing only the total is the thing that "
            "will hurt. [[slnc 350]] This is the most over-applied pattern I know "
            "of, which is why three of the nine acts in this project are spent on "
            "what it costs. A pattern taught without its bill is a sales pitch, and "
            "you deserve better than a sales pitch."
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
            "That's event sourcing. [[slnc 250]] The full source, the written "
            "notes, the diagrams and an animated walkthrough are all in the "
            "repository, and everything runs offline with nothing installed but a "
            "Java development kit — no database, no Kafka, no Docker. [[slnc 300]] "
            "If you try one exercise, try this one. Fix the double-awarding bug the "
            "other way: instead of changing how the log is read, append a "
            "correcting event that takes the extra points back off. Get it working, "
            "and then ask yourself which of the two repairs you would rather "
            "explain to an auditor, and which you would rather explain to a "
            "developer joining next year. [[slnc 300]] They are different answers, "
            "and working out why they are different is the moment this pattern "
            "stops being a technique and starts being a judgement. [[slnc 300]] If "
            "this helped, a like genuinely does help other people find it, and "
            "subscribe if you would like the rest of the series. [[slnc 250]] "
            "Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
