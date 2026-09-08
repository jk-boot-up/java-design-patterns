"""Scene definitions for the Template Method pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="The Template Method Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Template Method pattern "
            "in Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. The template "
            "method pattern writes an order of operations down in a base class, "
            "in a method that subclasses are not allowed to override, and leaves "
            "the individual steps for them to fill in. The sequence is written "
            "once and cannot be rearranged; only the steps vary. [[slnc 350]] "
            "That's the idea in a sentence. It's the oldest trick in object- "
            "oriented design and the one people most often use without knowing "
            "its name. The rest of the video does it properly, by building a real "
            "working Java project: an online store that fulfils orders three "
            "completely different ways. [[slnc 250]] By the end you'll know what "
            "the word final is actually buying you, how to choose between a "
            "required step, a default and a hook, and the one serious price this "
            "pattern charges."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "Every order in the shop is fulfilled by the same six steps:",
            "",
            "  validate    refuse anything that cannot be fulfilled",
            "  reserve     make sure the goods exist",
            "  charge      take the money",
            "  pack        get the goods ready to leave",
            "  dispatch    hand over, and produce a reference",
            "  notify      tell the customer, quoting that reference",
            "",
            "Three routes: own warehouse, marketplace seller, digital download.",
            "Every step differs. The order does not.",
        ],
        narration=(
            "So, imagine an online shop. [[slnc 250]] Every order it fulfils runs "
            "through the same six steps: validate, reserve, charge, pack, "
            "dispatch, notify. [[slnc 300]] That order is not a matter of taste. "
            "Charge before you reserve and you have taken money for goods you "
            "cannot supply. Notify before you dispatch and you have emailed "
            "somebody a tracking number that does not exist yet. [[slnc 300]] "
            "What does vary, and varies enormously, is the inside of each step. "
            "The shop fulfils from its own warehouse, from marketplace sellers, "
            "and as digital downloads. Holding stock at Reading, asking a third "
            "party to confirm, and minting a licence key have nothing in common "
            "at all — except where they sit in that list of six."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="The Obvious First Move",
        body=[
            "Write each route out from beginning to end:",
            "",
            "  fulfilFromWarehouse(order)     six steps",
            "  fulfilFromMarketplace(order)   six steps",
            "  fulfilDigital(order)           six steps",
            "",
            "Each one reads top to bottom with nothing hidden.",
            "It is a third of the code of the alternative.",
            "",
            "And on the day it was written, it was correct.",
        ],
        narration=(
            "The obvious first move is to write each route out. [[slnc 250]] "
            "Three methods, one per route, each saying what it does from "
            "beginning to end. [[slnc 300]] I want to be fair to this, because it "
            "is genuinely good code. Every method reads top to bottom with "
            "nothing hidden behind an abstraction. There is no vocabulary to "
            "learn. It is about a third of the code of the alternative. And on "
            "the day each one was written, it was almost certainly correct. "
            "[[slnc 350]] Three copies of a six-step sequence is not, by itself, "
            "a crisis. What happens to them over the following year is."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Two Lines the Wrong Way Round",
        body="""public FulfilmentReport fulfilDigital(Order order) {
    // validate ... reserve ... charge ... pack ...

    // Drifted: the email is composed before the key exists.
    report.notified(order.customerEmail() + ": Order " + order.id()
            + " is ready to download. Key: " + report.dispatchReference());

    report.dispatchedAs(LicenceKeys.mint(order));
    return report;
}""",
        narration=(
            "And here is the day it bites. [[slnc 250]] Somebody, at some point, "
            "moved one line in one copy. The digital route now notifies the "
            "customer and then dispatches. [[slnc 300]] Follow it through. The "
            "email quotes the dispatch reference — but dispatch has not run yet, "
            "so the reference is still the placeholder. The customer receives a "
            "message that says, ready to download, key, open bracket, not "
            "dispatched. [[slnc 300]] A microsecond later the licence key is "
            "minted, and it is perfectly correct. Nobody will ever be told what "
            "it is. [[slnc 300]] Nothing threw. Nothing failed to compile. No "
            "test went red, because no test knew those six calls had an order at "
            "all. The order was marked fulfilled. [[slnc 250]] And in the "
            "marketplace copy the same thing happened in a different place: the "
            "charge drifted above the seller confirmation, so a customer can be "
            "charged forty-two pounds and then told the seller will not supply it."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   The sequence exists only as a convention, typed out three times",
            "✗   Nothing in the language or the compiler knows it is a sequence",
            "✗   So the copies drift — one line at a time, in a hurry",
            "✗   A seventh step has to be inserted three times, in the right place",
            "✗   A missing step is not an error; it is just a route that skips it",
            "",
            "Duplication is the complaint.",
            "The customer charged and given nothing is the bug.",
        ],
        narration=(
            "So why does that hurt? [[slnc 250]] Ask a room what is wrong with "
            "three copies of six steps and everyone says duplication. That is "
            "true, and it is the weaker argument — plenty of teams live with "
            "three short duplicated methods for years. [[slnc 300]] Here is the "
            "strong one. Forget the bodies. What is duplicated that the compiler "
            "cannot see? [[slnc 300]] The order. It exists only as a shape, typed "
            "out by hand in three places, and nothing anywhere knows it is a "
            "shape. So it drifts, one line at a time, in whichever copy somebody "
            "last edited in a hurry. [[slnc 250]] And the day the shop adds a "
            "fraud check, somebody has to find all three copies and insert it in "
            "the same position in each. The compiler will not help. A copy that "
            "is missing the step is not an error — it is just a route that "
            "doesn't run it. [[slnc 300]] The duplication is the design "
            "complaint. The customer who was charged and given nothing is the "
            "actual bug."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Template Method Pattern",
        body=[
            "“Define the skeleton of an algorithm in an operation,",
            "deferring some steps to subclasses. Template Method lets",
            "subclasses redefine certain steps of an algorithm without",
            "changing the algorithm's structure.”",
            "",
            "— Gang of Four, 1994",
            "",
            "In plain language:",
            "the subclass decides how each step behaves.",
            "It never decides when the steps run.",
        ],
        narration=(
            "The Gang of Four put it like this: define the skeleton of an "
            "algorithm in an operation, deferring some steps to subclasses. "
            "Template method lets subclasses redefine certain steps of an "
            "algorithm without changing the algorithm's structure. [[slnc 350]] "
            "In plain language: the subclass decides how each step behaves, and "
            "it never decides when the steps run. [[slnc 300]] Read the last "
            "words of that definition again — without changing the algorithm's "
            "structure. That is not a description of what subclasses happen to "
            "do. It is a constraint the base class enforces, and in Java it is "
            "enforced by one keyword."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="Everyday Analogy: The Recipe",
        body=[
            "A cake recipe. Which parts are negotiable?",
            "",
            "  the flavouring        yours to choose",
            "  the tin               yours to choose",
            "  the icing             optional — skip it if you like",
            "",
            "  mix, then bake, then ice        not yours to choose",
            "",
            "Ice it before you bake it and you have neither a cake nor icing.",
        ],
        narration=(
            "Here is the everyday version. [[slnc 250]] A cake recipe. Ask "
            "yourself which parts of it are negotiable. [[slnc 300]] The "
            "flavouring is — lemon, chocolate, whatever you have. The tin is. The "
            "icing is genuinely optional; plenty of good cakes have none. [[slnc "
            "300]] But mix, then bake, then ice is not negotiable, and it isn't "
            "negotiable in a fussy, house-style way. Ice it before you bake it "
            "and you do not have a differently styled cake. You have no cake and "
            "no icing. [[slnc 300]] A recipe that let you reorder those three "
            "would not be a more flexible recipe. It would be a worse one. "
            "[[slnc 250]] That is the whole pattern: the ingredients are holes, "
            "the icing is a hook, and the order is fixed by the person who wrote "
            "the recipe, on purpose."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So here are the roles. [[slnc 250]] At the top, the abstract class, "
            "Fulfilment Process, and inside it the template method itself — "
            "fulfil — marked final. That method is the only thing in the system "
            "that knows the six steps have an order. [[slnc 300]] Underneath it, "
            "the three routes. Look at how many methods each one overrides: the "
            "warehouse route four, the marketplace six, the digital seven. "
            "[[slnc 250]] The shortest one is the most ordinary one, and that is "
            "exactly the sign you want. It means the defaults in the base class "
            "were chosen well, so the common case costs almost nothing to "
            "express. [[slnc 300]] And on the right, the report every step writes "
            "itself onto. That is how the project can prove its central claim "
            "rather than assert it: run all three routes, print the list of step "
            "names each one produced, and they come out identical — character for "
            "character. No route chose that. Fulfil did."
        ),
    ),
    dict(
        key="09-template",
        kind="code",
        title="The Template Method — Seven Lines and One Keyword",
        body="""public final FulfilmentReport fulfil(Order order) {
    FulfilmentReport report = new FulfilmentReport(order.id(), routeName());

    validate(order, report);        // private -- nobody may replace it
    reserveStock(order, report);    // abstract -- you must answer
    charge(order, report);          // abstract -- you must answer
    pack(order, report);            // default  -- you may replace it
    dispatch(order, report);        // abstract -- you must answer
    notifyCustomer(order, report);  // default  -- you may replace it
    afterFulfilment(order, report); // hook     -- does nothing at all

    return report;
}""",
        narration=(
            "And here is the entire pattern. [[slnc 300]] Seven calls, in one "
            "method, on an abstract class. Every route in the system runs "
            "exactly this. [[slnc 250]] The important word is on the first line, "
            "and it is final. A route may decide how any of these steps behaves. "
            "It cannot decide when they run, and that is not a convention "
            "somebody has to remember during code review — it is a compile error. "
            "[[slnc 350]] Now read the comments down the right hand side, because "
            "everything else in this pattern is a decision about what kind of "
            "hole each step should be. Validate is private, so nobody can replace "
            "it. Three steps are abstract, so every route must answer them. Two "
            "have defaults, so a route that wants the usual behaviour writes "
            "nothing. And the last one does nothing whatsoever. [[slnc 250]] We "
            "will come back to that one, because an empty method that gets called "
            "on every single run sounds like dead code, and it is one of the most "
            "useful things here."
        ),
    ),
    dict(
        key="10-holes",
        kind="bullets",
        title="Three Kinds of Hole",
        body=[
            "abstract    you must answer      no default could be right",
            "            reserveStock, charge, dispatch, routeName",
            "",
            "default     you may replace it   most routes want the usual thing",
            "            pack, notifyCustomer",
            "",
            "hook        you may join in      the base class asks a question,",
            "            requiresShippingAddress()   or offers a place to stand",
            "            afterFulfilment()",
            "",
            "Choosing which is which is most of the work.",
        ],
        narration=(
            "So, three kinds of hole, and choosing between them is most of the "
            "work of using this pattern. [[slnc 300]] Abstract means you must "
            "answer, and you use it when no default could possibly be right for "
            "everybody. Reserving stock in a warehouse and asking a marketplace "
            "seller to confirm are not variations on a theme; there is nothing "
            "sensible to inherit. [[slnc 300]] A default means you may replace "
            "it. Packing is packing — box it and label it — so the warehouse "
            "route says nothing at all about packing and gets the right behaviour "
            "for free. Only the routes that genuinely differ speak up. [[slnc "
            "300]] And then hooks, which come in two flavours. One is a question: "
            "does this route require a shipping address? The digital route "
            "answers no, and gets its addressless orders through validation "
            "without weakening the address check for anybody else. [[slnc 250]] "
            "The other is a place to stand: after fulfilment does nothing at all, "
            "and is called on every run, so the marketplace route has somewhere "
            "to post its commission without the base class ever learning that "
            "marketplaces exist. [[slnc 300]] Be careful with hooks, though. Each "
            "one is a permission you are granting for the lifetime of the class, "
            "and a base class with a hook around every step has stopped "
            "protecting anything."
        ),
    ),
    dict(
        key="11-route",
        kind="code",
        title="Why the Order Being Fixed Is Worth Something",
        body="""// DigitalFulfilment -- runs fifth
protected void dispatch(Order order, FulfilmentReport report) {
    report.dispatchedAs(LicenceKeys.mint(order));
}

// DigitalFulfilment -- runs sixth
protected void notifyCustomer(Order order, FulfilmentReport report) {
    report.notified(order.customerEmail() + ": Order " + order.id()
            + " is ready to download. Key: " + report.dispatchReference());
}""",
        narration=(
            "Now put those two methods side by side, because this is the payoff. "
            "[[slnc 300]] Dispatch mints the licence key and writes it onto the "
            "report. Notify customer reads it back out and puts it in the email. "
            "[[slnc 250]] Those are the same two lines of code you saw in the "
            "naive version, doing the same two things. Here they are correct, and "
            "they are correct for a reason that has nothing to do with the author "
            "being careful. [[slnc 350]] Notify customer is allowed to rely on "
            "dispatch having already run. Not because it happens to be written "
            "underneath it. Because fulfil is final, so there is no route — none "
            "that exists, and none that anybody writes next year — that can put "
            "these two the other way round. [[slnc 300]] That is what the keyword "
            "bought. A step can depend on an earlier step's work, and that "
            "dependency is safe forever."
        ),
    ),
    dict(
        key="12-proof",
        kind="code",
        title="The Test That Proves It",
        body="""private static final class RecordingRoute extends FulfilmentProcess {
    final List<String> calls = new ArrayList<>();
    // every step appends its own name, and does nothing else
}

@Test
void stepsRunInTheOrderTheTemplateDefines() {
    route.fulfil(order);

    assertEquals(List.of("reserveStock", "charge", "pack",
                         "dispatch", "notifyCustomer", "afterFulfilment"),
                 route.calls);
}""",
        narration=(
            "This is the test that proves the claim. [[slnc 300]] Recording route "
            "is a subclass whose steps do nothing except write down that they "
            "were called. Fulfil it, and you can assert on the order directly. "
            "[[slnc 250]] Ask yourself whether you could write this test against "
            "the naive version. You could — but it would only tell you about the "
            "three routes that exist today. It could say nothing at all about the "
            "fourth one somebody adds in six months, which is precisely where the "
            "drift comes from. [[slnc 300]] Here the guarantee is structural, and "
            "the test is just checking that the structure says what we think it "
            "says. [[slnc 250]] Beside it there are forty-six tests in total, "
            "including a set that pins the naive version's two bugs as passing "
            "tests, asserting the wrong behaviour on purpose so you can watch them "
            "describe it."
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== 1. The trap: three hand-written copies of the same sequence ===
  sam@example.com: Order D-9001 is ready to download. Key: (not dispatched)
  The customer was told before the key existed.

=== 2. The pattern: one sequence, three routes ===
  step names, warehouse   : [validate, reserve, charge, pack, dispatch, notify]
  step names, marketplace : [validate, reserve, charge, pack, dispatch, notify]
  step names, digital     : [validate, reserve, charge, pack, dispatch, notify]
  Identical, and no route chose that. FulfilmentProcess.fulfil did.

=== 4. A fourth route, defined in this demo file ===
  click-and-collect       [validate, reserve, charge, pack, dispatch, notify]""",
        narration=(
            "Run it, and the two halves sit side by side. [[slnc 250]] Section "
            "one is the hand-written version: an email about a licence key, sent "
            "before the key existed. [[slnc 300]] Section two runs the same three "
            "routes through the template, and prints the step names each one "
            "produced. Three lists, three completely different implementations, "
            "and the lists are identical. Not because the routes agreed to be "
            "consistent — none of them has any idea what the others do. Because "
            "fulfil is the only thing that gets to decide. [[slnc 300]] Then "
            "section four adds a fourth route, click and collect, defined inside "
            "the demo file itself. One new class, no change to the base class, no "
            "change to any existing route, and it gets the same six steps in the "
            "same order for free."
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "✓   One final method owns the order; subclasses fill in the steps",
            "✓   abstract = must answer, default = may replace, hook = may join in",
            "✓   A step may rely on an earlier step, because the order is fixed",
            "✓   A new route is one class, and nothing that works gets reopened",
            "",
            "✗   It spends the subclass's one inheritance slot, permanently",
            "✗   The sequence is public API — a seventh step hits every route",
            "✗   Hooks are permissions; a hook per step protects nothing",
            "",
            "Factory Method is this, narrowed to creating one object.",
            "Strategy composes instead — and guarantees no order at all.",
        ],
        narration=(
            "So, what to remember. [[slnc 300]] One final method owns the order, "
            "and subclasses fill in the steps. Abstract means must answer, a "
            "default means may replace, a hook means may join in. A step is "
            "allowed to rely on an earlier step's work, because the order cannot "
            "change. And a new route is one class, with nothing that already "
            "works reopened. [[slnc 350]] Now the honest part, because a pattern "
            "video that only lists benefits is selling you something. [[slnc "
            "250]] This spends the subclass's one inheritance slot, permanently. "
            "Every route extends this base class and can extend nothing else, "
            "ever, and that is the real reason composition is the better modern "
            "default for most problems. [[slnc 250]] The sequence is public API: "
            "add a seventh step and you have changed every route at once, "
            "including ones you cannot see. And hooks are permissions — grant "
            "them one at a time and only when somebody actually needs one. "
            "[[slnc 300]] Finally, know its neighbours. Factory method is this "
            "same pattern narrowed down to a single hole that returns an object. "
            "And strategy composes instead of inheriting: it costs you nothing, "
            "and it guarantees you nothing about order either. Choose by asking "
            "which invariant you actually need. [[slnc 250]] You have used this "
            "already, by the way — Abstract List, Input Stream dot read, H T T P "
            "Servlet dot service, JUnit's before-each, and every Spring class "
            "with the word Template in its name."
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that adds a",
            "seventh step to both versions, and counts the edits.",
            "",
            "Next in the behavioural series: the State pattern.",
        ],
        narration=(
            "That's the template method pattern. [[slnc 250]] The full source, "
            "the written notes, the diagrams and an animated walkthrough are all "
            "in the repository — including the exercise I would most recommend: "
            "add a fraud check between validate and reserve, first to the "
            "template and then to the three hand-written copies, and count the "
            "edits each one takes. The shape of those two diffs is the entire "
            "argument, and it lands better when you have typed it than when I "
            "have said it. [[slnc 300]] If this helped, a like genuinely does "
            "help other people find it, and subscribe if you would like the rest "
            "of the behavioural series — the state pattern is next. [[slnc 250]] "
            "Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
