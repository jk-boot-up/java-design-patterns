"""Scene definitions for the Saga teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches, so no sentence points at the screen, the holiday
booking is described in full before any class name is spoken, and the console
slides are read out as a story about what the shop and the customer ended up
with rather than as columns of numbers. The slides illustrate the narration;
they never carry it.

Every number quoted here comes from the real output of `./gradlew run`: seventy
pounds and ninety-five pence charged and refunded, twenty of twenty kettles put
back on the shelf, two hundred and fifty milliseconds for a checkout that
works, and one email sitting in an inbox that no amount of undoing removes.

Scene order is the argument. The video starts with the broken version, because
the mechanism is boring until the room has felt the problem -- scenes three and
four are ten minutes of a real session compressed, and cutting them would leave
a viewer memorising an interface they have no reason to want.

Three scenes must not be cut or moved earlier. Scene thirteen is the payment
ledger with two lines on it, which is the difference between a compensation and
a rollback and the single most-skipped fact about this pattern. Scene fourteen
is the compensation that itself fails, which is why there are three outcomes
and not two. Scene fifteen is the email that cannot be unsent, and the ordering
rule that follows from it. A viewer who leaves with the mechanism and none of
those three has learned something worse than nothing.

Layout limit: on "bullets" and "quote" slides the body starts at y=260 and
steps 60 pixels a line, and the footer sits at y~1022, so twelve body lines
is the maximum.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Saga",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Saga pattern, in Java. [[slnc 300]] This video is presented '
            'by Jayasekhar Konduru. [[slnc 600]] First, a simple '
            'definition. [[slnc 300]] Sometimes one job has to happen in '
            'several different places. [[slnc 300]] And you cannot keep '
            'them all on hold until you are sure of all of them. [[slnc '
            '300]] So you let each piece finish on its own. [[slnc 300]] '
            'And for each piece, you write down the action that cancels '
            'it. [[slnc 300]] If a later piece fails, you walk backwards, '
            'cancelling the ones that already finished. [[slnc 600]] '
            'Think of booking a holiday: a flight, a hotel, and a hire '
            'car. [[slnc 300]] If the car falls through, you cancel the '
            'hotel, then the flight. [[slnc 700]] In our online store, '
            'one checkout has five steps, in five different services. '
            '[[slnc 300]] Reserve the stock. [[slnc 200]] Take the '
            'payment. [[slnc 200]] Create the order. [[slnc 200]] Book '
            'the parcel. [[slnc 200]] Send the email. [[slnc 300]] And '
            'then the courier refuses the address. [[slnc 500]] The '
            'mechanism is small. [[slnc 300]] This video is really about '
            'the three things undoing costs you, which almost nobody '
            'mentions.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="One Checkout, Five Services",
        body=[
            "A shopper buys a kettle. Seventy pounds, ninety-five.",
            "",
            "Reserve the stock. Take the payment. Create the order.",
            "Book the parcel. Send the confirmation email.",
            "",
            "Five steps — and five separate services, each with",
            "its own database, behind its own network call.",
            "",
            "There is no database that can see all five.",
            "",
            "So there is no single thing that can be rolled back.",
        ],
        narration=(
            'Here is the shop. [[slnc 400]] Somebody buys a kettle for '
            'seventy pounds ninety-five. [[slnc 500]] For that, five '
            'things must happen. [[slnc 300]] Reserve the kettle, so '
            'nobody else takes it. [[slnc 300]] Take the money. [[slnc '
            '300]] Create the order record. [[slnc 300]] Book a courier '
            'to deliver it. [[slnc 300]] And email the customer to say it '
            'is on the way. [[slnc 600]] Here is what makes it hard. '
            '[[slnc 300]] Those five things live in five different '
            'services. [[slnc 300]] Each has its own database. [[slnc '
            '300]] And the money actually leaves through a card network '
            'that belongs to nobody in this building. [[slnc 600]] So '
            'there is no single database underneath all of it. [[slnc '
            '300]] And without a single database, there is nothing single '
            'to roll back. [[slnc 500]] Remember that sentence. [[slnc '
            '300]] Everything else in this video follows from it.'
        ),
    ),
    dict(
        key="03-the-try-block",
        kind="code",
        title="What Everybody Writes First",
        body="""// NaiveCheckoutService.placeOrder(context)

try {
    stock.reserve(context);
    payments.charge(context);
    orders.create(context);
    shipping.schedule(context);  // <- this throws
    return context.orderRef();
} catch (RuntimeException e) {
    log.add("LOGGED-IT", e.getMessage());
    return null;
}""",
        narration=(
            'Here is what everybody writes first. [[slnc 300]] And it is '
            'not stupid code. [[slnc 600]] Four calls, one after another, '
            'inside one try block. [[slnc 300]] Reserve the stock. [[slnc '
            '200]] Charge the card. [[slnc 200]] Create the order. [[slnc '
            '200]] Book the courier. [[slnc 500]] If anything goes wrong, '
            'catch the problem, write a line to the log, and return '
            'nothing. [[slnc 600]] It sounds responsible. [[slnc 300]] '
            'There is error handling. [[slnc 300]] Nothing crashes. '
            '[[slnc 300]] In a code review, this passes. [[slnc 500]] Now '
            "let's hear what it does when the fourth call fails."
        ),
    ),
    dict(
        key="04-act-five",
        kind="console",
        title="The Courier Refuses",
        body="""$ ./gradlew run

Act 5 - the same failure, without a saga
  returned: null
  card charged: £70.95
  kettles still reserved: 1
  order state: CONFIRMED
  shipments scheduled: 0
  nothing threw. A line went into a log.
  the customer has paid for a parcel
  that will never be sent.""",
        narration=(
            'No courier covers the delivery address. [[slnc 300]] So the '
            'fourth call fails. [[slnc 500]] The catch runs, writes its '
            'line, and the method returns nothing. [[slnc 600]] Now count '
            'what is left behind. [[slnc 300]] The card has been charged '
            'seventy pounds ninety-five. [[slnc 300]] A kettle is still '
            'reserved, so nobody else can buy it. [[slnc 300]] The order '
            'record says confirmed. [[slnc 300]] And there is no parcel, '
            'and there never will be. [[slnc 600]] In one sentence: the '
            'customer has paid for something that will never arrive. '
            '[[slnc 600]] And here is the worrying part. [[slnc 300]] '
            'Nothing looked wrong. [[slnc 300]] No error escaped, no '
            'alert fired. [[slnc 300]] There is one line in a log file, '
            'read weeks later, by someone investigating a complaint. '
            '[[slnc 600]] The project has four tests for exactly this. '
            '[[slnc 300]] The money stays taken. [[slnc 200]] The stock '
            'stays reserved. [[slnc 200]] The order stays confirmed. '
            '[[slnc 200]] The failure is silent. [[slnc 300]] All four '
            'tests pass. [[slnc 300]] They are passing tests that prove '
            'the shop is broken.'
        ),
    ),
    dict(
        key="05-transactional",
        kind="bullets",
        title="No, @Transactional Does Not Fix It",
        body=[
            "It wraps the method in a transaction on the database",
            "this service owns. That is all it does.",
            "",
            "It has no reach into the stock service's database.",
            "None into payments. None over the card network.",
            "",
            "Rolling back a transaction that never touched the",
            "money does not bring the money back.",
            "",
            "Two-phase commit does span all five — by making every",
            "one hold a lock while it waits for the others.",
            "One slow courier, and the whole shop stops.",
        ],
        narration=(
            'At this point, someone always says: just add the '
            "Transactional annotation. [[slnc 400]] Let's take that "
            'seriously. [[slnc 300]] It is the biggest misunderstanding '
            'in this subject. [[slnc 600]] That annotation wraps your '
            'method in a transaction, on the one database this service '
            'owns. [[slnc 300]] That is all it does. [[slnc 300]] It '
            "cannot reach the stock service's database. [[slnc 300]] It "
            'cannot reach payments. [[slnc 300]] And it certainly cannot '
            'reach the card network, where the money went. [[slnc 600]] '
            'So when shipping fails and your transaction rolls back, only '
            "this service's own writes are undone. [[slnc 300]] The "
            'seventy pounds ninety-five is still gone. [[slnc 600]] There '
            'is a technology that can span all five, called two-phase '
            'commit. [[slnc 300]] It works. [[slnc 300]] But almost '
            'nobody uses it for this. [[slnc 300]] It makes every service '
            'hold a lock while it waits for the others. [[slnc 300]] So '
            "the stock table stays locked while you wait for a courier's "
            'website to answer. [[slnc 300]] One slow courier, and under '
            'load, the shop stops. [[slnc 600]] So there is no rollback. '
            '[[slnc 300]] If we want the shop put back, we must put it '
            'back ourselves.'
        ),
    ),
    dict(
        key="06-holiday",
        kind="quote",
        title="You Already Know How This Works",
        body=[
            "You book a holiday over the phone.",
            "Flight. Hotel. Hire car.",
            "",
            "Nobody will hold a seat while you ring the hotel,",
            "so each booking is final the moment you make it.",
            "",
            "Then the car hire company has nothing that week.",
            "",
            "There is no button that unhappens the last hour.",
            "There is a cancellation policy for each thing.",
            "",
            "So you ring the hotel. Then you ring the airline.",
        ],
        narration=(
            'Here is the same problem, away from any computer. [[slnc '
            '500]] You are booking a holiday by phone: a flight, a hotel, '
            'and a hire car. [[slnc 500]] You cannot keep all three on '
            'hold until you are happy with all three. [[slnc 300]] The '
            'airline will not hold a seat while you ring the hotel. '
            '[[slnc 300]] So you book them one at a time. [[slnc 300]] '
            'And each booking is final the moment you make it. [[slnc '
            '600]] Then the car hire company says they have nothing that '
            'week. [[slnc 600]] There is no magic button that undoes the '
            "last hour. [[slnc 300]] What you have is each booking's "
            'cancellation policy. [[slnc 300]] So you ring the hotel, and '
            'cancel the room. [[slnc 300]] Then you ring the airline, and '
            'cancel the flight. [[slnc 600]] And you end up back where '
            'you started. [[slnc 300]] Approximately. [[slnc 500]] Hold '
            'on to that word, approximately. [[slnc 300]] Most of this '
            'video lives inside it.'
        ),
    ),
    dict(
        key="07-the-step",
        kind="code",
        title="A Step That Carries Its Own Undo",
        body="""public interface SagaStep {

    String name();

    void execute(SagaContext context);

    void compensate(SagaContext context);

    default boolean canBeCompensated() {
        return true;
    }
}""",
        narration=(
            'Here is the mechanism, and it is small. [[slnc 500]] Every '
            'step in the checkout becomes an object with four things. '
            '[[slnc 300]] A name, so we can say which step we mean. '
            '[[slnc 300]] An action, which does the step. [[slnc 300]] A '
            'compensation, which is the action that cancels it. [[slnc '
            '300]] And an answer to one question: can this step be undone '
            'at all? [[slnc 600]] For our shop, in pairs. [[slnc 300]] '
            'Reserve the stock, and release it. [[slnc 300]] Take the '
            'payment, and refund it. [[slnc 300]] Create the order, and '
            'cancel it. [[slnc 300]] Book the parcel, and cancel the '
            'booking. [[slnc 600]] If this feels familiar, it is. [[slnc '
            '300]] An action and an undo on an object is the Command '
            'pattern. [[slnc 500]] But one difference matters more than '
            "anything else in this video. [[slnc 300]] A command's undo "
            'happens in memory, and always works. [[slnc 300]] A '
            "compensation is a network call to someone else's service. "
            '[[slnc 300]] It can be slow. [[slnc 300]] It can be refused. '
            '[[slnc 300]] It can fail. [[slnc 300]] Remember that.'
        ),
    ),
    dict(
        key="08-the-orchestrator",
        kind="code",
        title="Forward, Then Backwards",
        body="""for (SagaStep step : steps) {
    try {
        step.execute(context);
        done.add(step);            // remember it
    } catch (RuntimeException e) {
        unwind(done, context);     // walk back
        return SagaOutcome.compensated(...);
    }
}
return SagaOutcome.completed(...);

// unwind() iterates 'done' in reverse.""",
        narration=(
            'And here is the orchestrator, which is the rest of it. '
            '[[slnc 500]] Go forward through the steps. [[slnc 300]] Run '
            'each one. [[slnc 300]] After each one succeeds, add it to a '
            'list. [[slnc 500]] That list is not holding anything open. '
            '[[slnc 300]] Every step on it has already finished. [[slnc '
            '300]] It is simply a record of what must be undone, if a '
            'later step fails. [[slnc 600]] If a step fails, stop going '
            'forward. [[slnc 300]] Walk the list backwards, and run each '
            "step's compensation. [[slnc 600]] One more thing, easy to "
            'miss. [[slnc 300]] The orchestrator never crashes. [[slnc '
            '300]] It always returns a result describing what happened. '
            '[[slnc 300]] Because a saga that can crash has no way to '
            'tell anyone what state the shop was left in. [[slnc 300]] '
            'That would put us right back at the try block.'
        ),
    ),
    dict(
        key="09-the-shape",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let's put all the pieces in one place. [[slnc 500]] On one "
            'side is the design we are replacing. [[slnc 300]] Four calls '
            'in a try block, and a catch that writes a log line. [[slnc '
            '300]] When the courier refuses, it leaves money taken, a '
            'kettle reserved, an order confirmed, and no parcel. [[slnc '
            '600]] On the other side is the saga. [[slnc 300]] A step: an '
            'action, paired with a compensation, and whether it can be '
            'undone at all. [[slnc 300]] An orchestrator, which runs the '
            'steps forward keeping a list, and then backwards to undo '
            'them. [[slnc 300]] And a result, with three possible values, '
            'not two. [[slnc 300]] Completed. [[slnc 200]] Compensated. '
            '[[slnc 200]] And needs human help. [[slnc 600]] Then there '
            'is the odd one out: the email service. [[slnc 300]] It has '
            'no compensation at all, because there is no unsend. [[slnc '
            '300]] That is why it must go last. [[slnc 600]] And one '
            'honest summary of the whole pattern. [[slnc 300]] A refund '
            'is a new fact, not an erasure. [[slnc 300]] An undo can be '
            'refused. [[slnc 300]] And some steps have no undo at all.'
        ),
    ),
    dict(
        key="10-act-one",
        kind="console",
        title="Act One — It Usually Works",
        body="""Act 1 - placing an order across five services
     0ms ->    30ms  Stock      OK   res-1
    30ms ->   130ms  Payments   OK   chg-1
   130ms ->   150ms  Orders     OK   ord-9001
   150ms ->   210ms  Shipping   OK   shp-1
   210ms ->   250ms  Email      OK   emailed cust-7
   250ms ->   250ms  Saga  COMPLETED ord-9001 for £70.95

  no transaction spanned any of that.
  Each step committed on its own.""",
        narration=(
            'First demo: when nothing goes wrong. [[slnc 300]] The boring '
            'case carries an important fact. [[slnc 600]] The stock is '
            'reserved in thirty milliseconds. [[slnc 300]] The payment '
            'takes a hundred, the slowest step. [[slnc 300]] The order '
            'record takes twenty. [[slnc 300]] The courier booking takes '
            'sixty. [[slnc 300]] The email takes forty. [[slnc 300]] Two '
            'hundred and fifty milliseconds, and the order is completed. '
            '[[slnc 600]] Nothing clever happened. [[slnc 300]] But here '
            'is the key fact. [[slnc 300]] No transaction covered any of '
            'that. [[slnc 300]] Each step was saved on its own. [[slnc '
            '600]] By the time the payment was taken, the stock '
            'reservation was already final. [[slnc 300]] By the time the '
            'courier was called, the money had already left the '
            "customer's account for good. [[slnc 500]] That is exactly "
            'why compensation is the only tool we have.'
        ),
    ),
    dict(
        key="11-act-two",
        kind="console",
        title="Act Two — Walked Backwards",
        body="""Act 2 - no courier covers the postcode
   180ms  Saga  STEP-FAILED  schedule shipment
   180ms ->   200ms  Orders    cancelled ord-9002
   200ms ->   300ms  Payments  refunded chg-1
   300ms ->   330ms  Stock     released res-1
   330ms  Saga  COMPENSATED  customer owes nothing

  kettles back on the shelf: 20 of 20
  money the shop is holding: £0.00
  order state: CANCELLED""",
        narration=(
            'Second demo: the same courier refusal, but through the saga. '
            '[[slnc 500]] The first three steps succeed, just as before. '
            '[[slnc 300]] Stock reserved, money taken, order created. '
            '[[slnc 300]] Then the shipping step fails. [[slnc 600]] The '
            'orchestrator stops going forward, and walks its list '
            'backwards. [[slnc 300]] Cancel the order. [[slnc 300]] '
            'Refund the payment. [[slnc 300]] Release the stock. [[slnc '
            '300]] The result says: compensated. [[slnc 300]] The '
            'customer owes nothing. [[slnc 600]] All twenty kettles are '
            'back on the shelf. [[slnc 300]] The shop is holding no '
            'money. [[slnc 300]] The order says cancelled. [[slnc 600]] '
            'Why backwards? [[slnc 300]] It is not tidiness. [[slnc 300]] '
            'Later steps depend on earlier ones. [[slnc 500]] The order '
            'must be cancelled before the refund. [[slnc 300]] Otherwise, '
            'for a moment, the finance team sees a confirmed order with '
            'no payment. [[slnc 300]] And the stock reservation comes off '
            'last, because it made every later step possible. [[slnc '
            '500]] Reverse order is the only order in which each undo is '
            'safe. [[slnc 600]] So the shop is back where it started. '
            '[[slnc 300]] Approximately.'
        ),
    ),
    dict(
        key="12-in-reverse",
        kind="bullets",
        title="Three Things This Costs You",
        body=[
            "Everything you have seen so far is the easy half.",
            "",
            "One. The undo leaves a trace. It is not a rollback.",
            "",
            "Two. The undo is a network call, so the undo itself",
            "can be refused.",
            "",
            "Three. Some steps cannot be undone at all, at any",
            "price, by anybody.",
            "",
            "The rest of this video is those three, one at a time.",
        ],
        narration=(
            'That is the whole mechanism. [[slnc 500]] Most explanations '
            'of the saga pattern end here. [[slnc 300]] A step with an '
            'undo, an orchestrator that walks backwards, and a happy '
            'summary. [[slnc 500]] But everything so far is the easy '
            'half. [[slnc 600]] There are three things that undoing costs '
            'you. [[slnc 500]] One. [[slnc 200]] The undo leaves a trace. '
            '[[slnc 300]] It is not a rollback. [[slnc 400]] Two. [[slnc '
            "200]] The undo is itself a network call to someone else's "
            'service. [[slnc 300]] So the undo can fail. [[slnc 400]] '
            'Three. [[slnc 200]] Some steps cannot be undone at all, by '
            'anybody, ever. [[slnc 600]] The rest of this video takes '
            'those three, one at a time. [[slnc 300]] Do not skip them. '
            '[[slnc 300]] These are the parts that will actually find '
            'you.'
        ),
    ),
    dict(
        key="13-the-ledger",
        kind="console",
        title="One — A Refund Is A New Fact",
        body="""and note what the payment ledger looks like:

  CHARGE  £70.95   chg-1
  REFUND -£70.95   ref-2

two lines, not zero.
A refund is a new fact, not an erasure.

the customer saw the money leave and come back,
and may well ring up to ask why.""",
        narration=(
            'Cost number one. [[slnc 300]] Look at the payment records '
            'after that perfectly successful compensation. [[slnc 600]] '
            'They do not show nothing. [[slnc 300]] They show two lines. '
            '[[slnc 300]] A charge of seventy pounds ninety-five. [[slnc '
            '300]] And a refund of seventy pounds ninety-five. [[slnc '
            '500]] The total is zero. [[slnc 300]] The history is not. '
            '[[slnc 600]] That is not an accounting detail. [[slnc 300]] '
            'A database rollback leaves no trace. [[slnc 300]] It is as '
            'if the write never happened. [[slnc 300]] A compensation is '
            'a new action that cancels an old one. [[slnc 300]] And both '
            'stay true, forever. [[slnc 600]] So the customer saw seventy '
            'pounds leave their account, and come back. [[slnc 300]] They '
            'may ring up to ask why. [[slnc 300]] Their bank may show it '
            'as pending for days. [[slnc 300]] And the card network may '
            'keep its fee either way. [[slnc 500]] Just like the holiday, '
            'where the airline charged a cancellation fee. [[slnc 600]] '
            'So here is the sentence to remember. [[slnc 300]] '
            'Compensation is not rollback.'
        ),
    ),
    dict(
        key="14-needs-human",
        kind="console",
        title="Two — When The Undo Fails Too",
        body="""Act 3 - the refund fails as well
   200ms ->   300ms  Payments  FAILED  no answer
   300ms  Saga  UNDO-FAILED  take payment
   300ms ->   330ms  Stock     released res-1
   330ms  Saga  NEEDS-HUMAN  could not undo
                             [take payment]

  needs a human: true
  money the shop is holding that it
  should not: £70.95""",
        narration=(
            'Cost number two, and this one is uncomfortable. [[slnc 400]] '
            'What happens if the refund fails? [[slnc 600]] The payment '
            'service does not answer. [[slnc 300]] The money cannot be '
            'given back. [[slnc 600]] Two things happen, and both are '
            'deliberate. [[slnc 500]] First, the undoing carries on '
            'anyway. [[slnc 300]] The refund failed, but the order is '
            'still cancelled, and the stock is still released. [[slnc '
            '300]] A saga that gave up at the first failure would leave '
            'more broken than necessary. [[slnc 500]] Second, the result '
            'says so, clearly. [[slnc 300]] This is why there are three '
            'results, not two. [[slnc 300]] Completed. [[slnc 200]] '
            'Compensated. [[slnc 200]] And needs human help. [[slnc 600]] '
            'That third result names a problem no code can fix. [[slnc '
            '300]] The shop is holding seventy pounds ninety-five that it '
            'should not have. [[slnc 300]] And it cannot give it back '
            'automatically. [[slnc 600]] Compare that with the try block '
            'from the start. [[slnc 300]] The money is in exactly the '
            'same place. [[slnc 300]] The difference is that this version '
            'knows, and says so. [[slnc 600]] So, in your system, where '
            'does needs human help go? [[slnc 300]] A queue, a ticket, a '
            'dashboard, or a person whose job it is. [[slnc 300]] If it '
            'goes nowhere, it is no better than that log line.'
        ),
    ),
    dict(
        key="15-the-email",
        kind="console",
        title="Three — There Is No Unsend",
        body="""Act 4 - the confirmation email, sent too early

  emails in the customer's inbox: 1
    "your order ord-9004 is confirmed"

  the order is cancelled and the money is back,
  and that email is still sitting there.

so: steps that cannot be undone go last,
after everything that might fail.""",
        narration=(
            'Cost number three. [[slnc 500]] This demo runs the same five '
            'steps, with one change. [[slnc 300]] The confirmation email '
            'is sent earlier, before the courier is booked. [[slnc 300]] '
            'Then the courier refuses, just as before. [[slnc 600]] '
            'Everything is undone correctly. [[slnc 300]] The order is '
            'cancelled. [[slnc 300]] The money is refunded. [[slnc 300]] '
            'The stock goes back on the shelf. [[slnc 600]] And the '
            'customer is holding an email that says their order is '
            'confirmed. [[slnc 300]] It is not. [[slnc 600]] No '
            'compensation can help, because there is no unsend. [[slnc '
            '300]] The only fix is a second email, apologising. [[slnc '
            '300]] Which is, once again, a new fact, not an erasure. '
            '[[slnc 600]] That is why each step says whether it can be '
            'undone at all. [[slnc 300]] The email step says no. [[slnc '
            '300]] So the saga records it, and reports: needs human help. '
            '[[slnc 500]] Nothing in the code is broken. [[slnc 300]] The '
            'order of the steps is. [[slnc 600]] So here is the most '
            'practical rule in this video. [[slnc 300]] Steps that cannot '
            'be undone go last, after everything that might fail. [[slnc '
            '500]] Think about your own systems. [[slnc 300]] Emails, '
            'text messages, notifications, printing a label, anything a '
            'customer can see. [[slnc 300]] That list is always longer '
            'than people expect.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the four tests that pass",
            "while asserting the shop is broken, and the one that",
            "proves a refund leaves two lines and not zero.",
        ],
        narration=(
            "That's the Saga pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] A saga undoes '
            'finished steps one by one, in reverse, but an undo is a new '
            'fact, it can fail, and some steps can never be undone, so '
            'they go last. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Make a compensation '
            'fail on purpose, using a setting on the stock service. '
            '[[slnc 300]] Then see which other undos still run, and what '
            'the result says. [[slnc 500]] And one question to think '
            'about. [[slnc 300]] Take a process you work on, and list its '
            'steps in order. [[slnc 300]] Mark the ones that can never be '
            'undone. [[slnc 300]] Do any of them happen before something '
            'that might fail? [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
