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
            "Hello, and welcome. This video explains the saga pattern in Java, "
            "and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. When one job "
            "has to happen in several different places, and you cannot hold all "
            "of them open until you are sure of all of them, you let each piece "
            "finish on its own — and you write down, for each piece, the action "
            "that cancels it out. If a later piece fails, you walk backwards "
            "cancelling the ones that already finished. [[slnc 350]] That is "
            "the whole mechanism, and it is about twenty lines of code. "
            "[[slnc 300]] The rest of the video builds a real working Java "
            "project: an online shop, and one checkout — reserve the stock, take "
            "the payment, create the order, book the parcel, send the email. "
            "Five steps, five different services. [[slnc 300]] And then the "
            "courier refuses the address. [[slnc 350]] The mechanism will take "
            "ten minutes. What the rest of this video is really about is the "
            "three things that undoing costs you, because almost nobody "
            "mentions them, and every one of them will find you in production."
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
            "Here is the shop, and it is worth picturing before any code. "
            "[[slnc 300]] Somebody buys a kettle. Seventy pounds and ninety-five "
            "pence. [[slnc 350]] For that to happen, five things have to happen. "
            "Reserve the kettle so nobody else takes it. Take the money. Create "
            "the order record. Book a courier to deliver it. Send the customer "
            "an email saying it is on the way. [[slnc 350]] Now here is the part "
            "that makes this hard. Those five things live in five different "
            "services. Stock is one team's system with one team's database. "
            "Payments is another, and the money actually leaves through a card "
            "network that belongs to nobody in this building. Orders, shipping "
            "and email are three more. [[slnc 400]] So there is no single "
            "database sitting underneath all of that. And if there is no single "
            "database, there is no single thing you can roll back. [[slnc 300]] "
            "Hold on to that sentence. Everything else in this video follows "
            "from it."
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
            "This is what everybody writes first, and I want to be fair to it, "
            "because it is not stupid code. [[slnc 300]] Four calls, one after "
            "another, all inside one try block. Reserve the stock. Charge the "
            "card. Create the order. Book the courier. If any of that goes "
            "wrong, catch the problem, write a line to the log, and return "
            "nothing. [[slnc 350]] Read it out loud and it sounds responsible. "
            "There is error handling. Nothing escapes. Nothing crashes. "
            "[[slnc 400]] And in a code review, this passes. I have written it. "
            "You have probably written it. [[slnc 350]] Now watch what it "
            "actually does when the fourth call fails."
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
            "No courier covers the delivery address. The fourth call throws. "
            "[[slnc 350]] So the catch runs, writes its line, and the method "
            "returns nothing. [[slnc 400]] Now count what is actually left "
            "behind. [[slnc 300]] The card has been charged seventy pounds and "
            "ninety-five pence. A kettle is still reserved, so nobody else can "
            "buy it. The order record says confirmed. And there is no parcel "
            "and there never will be. [[slnc 400]] Say that as one sentence. "
            "The customer has paid for something that will never arrive. "
            "[[slnc 350]] And now the part that should genuinely worry you. "
            "Nothing failed. No exception escaped, no alert fired, no dashboard "
            "went red. There is one line in a log file, and it gets read three "
            "weeks later by somebody investigating a complaint. [[slnc 400]] "
            "In the project there are four tests covering exactly this. The "
            "money stays taken. The stock stays reserved. The order stays "
            "confirmed. The failure is silent. [[slnc 300]] All four of them "
            "pass. They are passing tests that assert the shop is broken."
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
            "At this point, in every room I have ever taught this in, somebody "
            "says the same three words. Just add transactional. [[slnc 400]] So "
            "let's take that seriously, because it is the most important "
            "misunderstanding in the subject. [[slnc 350]] That annotation "
            "wraps your method in a database transaction on the database that "
            "this service owns. That is genuinely all it does. It has no reach "
            "into the stock service's database, because that is somebody else's "
            "process on somebody else's machine. It has no reach into payments. "
            "And it certainly has no reach over the card network, where the "
            "money actually went. [[slnc 400]] So when the shipping call fails "
            "and your transaction rolls back, the rollback covers whatever this "
            "service wrote — and the seventy pounds and ninety-five pence is "
            "still gone. [[slnc 400]] Now, there is a technology that spans all "
            "five. It is called two-phase commit, and it genuinely works. "
            "Almost nobody uses it for this, and the reason is worth knowing. "
            "It works by making every participant hold a lock open while it "
            "waits for the others to agree. So the stock table is locked while "
            "you wait for a courier's web service to answer. One slow courier, "
            "and under load the shop stops. [[slnc 350]] So we are not getting "
            "a rollback. If we want the shop put back, we are going to have to "
            "put it back ourselves."
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
            "Here is the same problem, away from any computer. [[slnc 350]] You "
            "are booking a holiday over the phone. A flight, a hotel, and a "
            "hire car. [[slnc 300]] You cannot hold all three open until you are "
            "happy with all three. The airline will not keep a seat "
            "unconfirmed while you ring the hotel, and the hotel will not hold "
            "a room while you ring the car hire company. So you book them one "
            "at a time, and each booking is final the moment you make it. "
            "[[slnc 400]] Then the car hire company tells you they have nothing "
            "that week. [[slnc 400]] Now. You do not have a magic button that "
            "makes the last hour not have happened. What you have is the "
            "cancellation policy for each thing you already booked. So you ring "
            "the hotel and cancel the room. Then you ring the airline and "
            "cancel the flight. [[slnc 350]] And you end up back where you "
            "started. Approximately. [[slnc 400]] Hold on to that word "
            "approximately, because three quarters of this video is inside it."
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
            "So here is the mechanism, and it is small. [[slnc 350]] Every step "
            "in the checkout becomes an object with four things on it. It has a "
            "name, so the timeline and the outcome can say which step we are "
            "talking about. It has an execute, which is the thing it does. It "
            "has a compensate, which is the action that cancels that out. And "
            "it can answer one question: can this be undone at all. "
            "[[slnc 400]] In pairs, for our shop, that is: reserve the stock, "
            "release the stock. Take the payment, refund it. Create the order, "
            "cancel it. Book the parcel, cancel the booking. [[slnc 350]] Now, "
            "if that shape feels familiar, it should. An execute and an undo, "
            "on an object, is the command pattern. There is a whole separate "
            "video about it. The structure here is deliberately the same. "
            "[[slnc 400]] But one difference matters more than everything else "
            "in this video put together. A command's undo happens in memory, "
            "and it always works. A compensation is a network call to somebody "
            "else's service. It can be slow. It can be refused. It can fail "
            "outright. [[slnc 300]] Remember that. We come back to it."
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
            "And this is the orchestrator, which is the whole of the rest of "
            "it. [[slnc 350]] Go forward through the steps. Run each one. After "
            "each one succeeds, write it down on a list. [[slnc 300]] That list "
            "is not a transaction and it is not holding anything open. Every "
            "step on it is already finished and committed. The list is simply a "
            "record of what will have to be undone if the next call goes wrong. "
            "[[slnc 400]] If a step throws, stop going forward, and walk that "
            "list backwards, calling the compensate on each one. [[slnc 350]] "
            "And notice one thing that is easy to skim past. This method never "
            "throws. It always returns an outcome object describing what "
            "happened. There is a test called it always returns an outcome, and "
            "it is there because a saga that can itself blow up has no way of "
            "telling anybody what state the shop was left in — which puts you "
            "straight back in the try block we started with."
        ),
    ),
    dict(
        key="09-the-shape",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let's put the whole cast in one place. [[slnc 350]] On one side is "
            "the design we are replacing: four calls in a try block, and a "
            "catch that writes a log line. The courier refuses, and what it "
            "leaves behind is seventy pounds and ninety-five pence taken, a "
            "kettle still reserved, an order marked confirmed, and no parcel. "
            "And an annotation on that method would not have helped, because it "
            "only ever covered this service's own database. [[slnc 400]] On the "
            "other side is the mechanism. A step, which is an execute paired "
            "with a compensate and a question about whether it can be "
            "compensated at all. An orchestrator, which runs them forward "
            "keeping a list and then backwards undoing it, in about twenty "
            "lines, and which never throws. And an outcome, which has three "
            "possible values, not two — completed, compensated, and needs human "
            "help. [[slnc 400]] And then the odd one out, sitting at the "
            "bottom. The email service, which has no compensate at all, because "
            "there is no unsend. That is why it has to go last. [[slnc 350]] "
            "Underneath all of it, one line that is the honest summary of this "
            "whole pattern. A refund is a new fact, not an erasure. The undo "
            "can be refused. And some steps have no undo at all."
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
            "Let's run it when nothing goes wrong, because the boring case "
            "carries the important fact. [[slnc 350]] Stock is reserved in "
            "thirty milliseconds. The payment takes a hundred, which is the "
            "slowest thing here and that is realistic. The order record takes "
            "twenty. The courier booking takes sixty. The email takes forty. "
            "Two hundred and fifty milliseconds, one order, and a completed "
            "outcome for seventy pounds and ninety-five pence. [[slnc 400]] "
            "Nothing clever happened. That is the point of showing it. "
            "[[slnc 350]] But read the last line of that output, because it is "
            "the thing that makes everything afterwards necessary. No "
            "transaction spanned any of that. Each step committed on its own. "
            "[[slnc 400]] By the time the payment was taken, the stock "
            "reservation was already final, and nothing was holding it open. By "
            "the time the courier was called, the money had already left the "
            "customer's account for good. [[slnc 350]] There is a test in the "
            "project with a deliberately long name — every step is already "
            "committed when the next one starts. It exists because that fact is "
            "the reason compensation is the only tool available to us."
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
            "Now the same refusal from the same courier, but this time through "
            "the saga. [[slnc 350]] The first three steps run and succeed, "
            "exactly as before. Stock reserved, money taken, order created. "
            "Then the shipping step fails. [[slnc 350]] And the orchestrator "
            "stops going forward, and starts walking its list in reverse. "
            "Cancel the order. Refund the payment. Release the stock. Then an "
            "outcome that says compensated, and the customer owes nothing. "
            "[[slnc 400]] Twenty kettles back on the shelf out of twenty. The "
            "shop is holding nothing. The order says cancelled. [[slnc 400]] "
            "Now, why backwards? It is not tidiness. [[slnc 350]] Later steps "
            "lean on earlier ones. The order has to be cancelled before the "
            "money is refunded, because otherwise there is a moment where "
            "finance is looking at a confirmed order with no payment against "
            "it. And the stock reservation comes off last, because the "
            "reservation is the thing that made every step after it legal in "
            "the first place. [[slnc 350]] Reverse order is not neatness. It is "
            "the only order in which each undo is safe. [[slnc 400]] So. The "
            "shop is back where it started. [[slnc 300]] Approximately."
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
            "So that is the mechanism, and we are about eight minutes in. "
            "[[slnc 350]] If this were most explanations of the saga pattern, "
            "it would end here. A step with an undo, an orchestrator that walks "
            "backwards, and a happy summary. [[slnc 400]] I think that does "
            "real damage, because everything so far is the easy half. "
            "[[slnc 350]] There are three things that undoing costs you. "
            "[[slnc 300]] One. The undo leaves a trace. It is not a rollback, "
            "and calling it one is how people get surprised. [[slnc 300]] Two. "
            "The undo is itself a network call to somebody else's service, "
            "which means the undo can fail. [[slnc 300]] And three. Some steps "
            "cannot be undone at all. Not badly, not expensively — not at all, "
            "by anybody, ever. [[slnc 400]] The rest of this video is those "
            "three, one at a time, with the demo output for each. Go and make a "
            "cup of tea if you need one, but do not skip them, because these "
            "are the parts that will actually find you."
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
            "Cost number one. Go and look at the payment ledger after that "
            "perfectly successful compensation. [[slnc 400]] It does not show "
            "nothing. It shows two lines. A charge of seventy pounds and "
            "ninety-five pence, and then a refund of seventy pounds and "
            "ninety-five pence. [[slnc 400]] Two lines, not zero. The net is "
            "zero. The history is not. [[slnc 350]] And that difference is not "
            "an accounting detail. A rollback leaves no trace — the database "
            "behaves as though the write never happened, and nobody outside can "
            "tell. A compensation is a new action that cancels out an old one, "
            "and both of them are permanently true. [[slnc 400]] Which means "
            "the customer watched seventy pounds leave their account and come "
            "back. They may well ring up to ask what that was. Their bank may "
            "show it as pending for three days. The card network may keep its "
            "fee either way. [[slnc 350]] Think back to the holiday. The "
            "airline charged you a cancellation fee, and your statement shows a "
            "payment and a refund rather than nothing at all. [[slnc 400]] So "
            "here is the sentence to take away, and it is the one to quote "
            "when somebody describes this pattern as rollback for "
            "microservices. [[slnc 300]] Compensation is not rollback."
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
            "Cost number two, and this is the uncomfortable one. Ask yourself "
            "the question before I answer it. [[slnc 400]] What happens if the "
            "refund fails? [[slnc 500]] The payment service does not answer. "
            "The money cannot be given back. [[slnc 400]] Two things happen, "
            "and both are deliberate. [[slnc 350]] The first is that the "
            "unwinding carries on anyway. The refund failed, but the order is "
            "still cancelled and the stock is still released. A saga that gave "
            "up at the first refusal would leave more broken than it had to. "
            "There is a test called unwinding carries on, and that is why it "
            "exists. [[slnc 400]] The second is that the outcome says so, out "
            "loud. This is why there are three possible outcomes and not two. "
            "Completed. Compensated. And needs human help. [[slnc 400]] That "
            "third one names a state that no code in this project can fix. The "
            "shop is holding seventy pounds and ninety-five pence that it is "
            "not entitled to, and it cannot give it back automatically. "
            "[[slnc 400]] Now compare that with the try block from the "
            "beginning of the video. The money is in exactly the same place. "
            "The difference is that this version knows, and says so. "
            "[[slnc 400]] Which puts a question back on you. In your system, "
            "what is needs human help? It has to be something. A queue, a "
            "ticket, a dashboard, a person whose job it is. [[slnc 350]] "
            "Because if there is nowhere for that outcome to go, then it is "
            "quietly the same as the log line we started with."
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
            "Cost number three. [[slnc 350]] This act runs the same five steps, "
            "with one change: the confirmation email is moved earlier, before "
            "the courier is booked. Then the courier refuses, exactly as "
            "before. [[slnc 400]] And everything unwinds correctly. The order "
            "is cancelled. The money is refunded. The stock goes back on the "
            "shelf. The code does precisely what it was written to do. "
            "[[slnc 400]] And the customer is sitting there holding an email "
            "that says their order is confirmed. Which it is not. "
            "[[slnc 400]] There is no compensate that helps, because there is "
            "no unsend. The only fix available to anybody is a second email "
            "apologising — which is, once again, a new fact rather than an "
            "erasure. [[slnc 350]] That is why the step interface has that "
            "fourth method on it, the one asking whether a step can be "
            "compensated at all. The email step answers no, the orchestrator "
            "records it as a step it could not undo, and the saga reports needs "
            "human help. [[slnc 400]] Nothing in the code is broken. The "
            "sequence is. [[slnc 350]] Which gives the rule, and it is the most "
            "practical thing in this video. Steps that cannot be undone go "
            "last, after everything that might fail. [[slnc 400]] So go and "
            "think about your own flows for a second. Emails. Text messages. "
            "Push notifications. Anything that talks to a third party. Anything "
            "a customer can see. Printing a label. Opening a barrier. "
            "[[slnc 300]] That list is always longer than people expect."
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
            "That's the saga pattern. [[slnc 250]] The full source, the written "
            "notes, the diagrams and an animated walkthrough are all in the "
            "repository, and everything runs offline with nothing installed but "
            "a Java development kit. [[slnc 300]] There is no message broker "
            "and no database in this project, and that is deliberate. A broker "
            "would add a container, a topic and several minutes to every run, "
            "and it would teach you nothing about the actual subject, which is "
            "what you do when you cannot roll back. [[slnc 350]] If you try one "
            "exercise, try this one. Make a compensation fail on purpose — "
            "there is a method on the stock service for it — and then watch "
            "which of the other undos still run, and what the outcome says "
            "afterwards. [[slnc 400]] And then the harder question, which no "
            "exercise can answer for you. Take a flow you actually work on. "
            "Write down its steps in order. Then mark the ones that genuinely "
            "cannot be undone, and see whether any of them happen before "
            "something that might fail. [[slnc 400]] Because the real lesson "
            "here is this. The mechanism is a list, a loop, and a loop that "
            "goes the other way, and you already know how to write all three. "
            "Deciding what each undo really costs, ordering the steps so the "
            "irreversible ones come last, and building somewhere for the "
            "outcome that needs a person to actually go — that is the part that "
            "needs a person. [[slnc 300]] If this helped, a like genuinely does "
            "help other people find it, and subscribe if you would like the "
            "rest of the series. [[slnc 250]] Thanks for watching, and I'll see "
            "you in the next one."
        ),
    ),
]
