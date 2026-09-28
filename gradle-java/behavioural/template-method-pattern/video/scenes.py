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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Template Method pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Template Method pattern '
            'writes down an order of steps once, in a base class. [[slnc '
            '300]] That method is locked, so subclasses cannot change it. '
            '[[slnc 300]] Subclasses only fill in what each step does. '
            '[[slnc 400]] So the sequence is written once, and can never '
            'be rearranged. [[slnc 300]] Only the steps vary. [[slnc '
            '600]] Think of a cake recipe. [[slnc 300]] You choose the '
            'flavour and the tin. [[slnc 300]] But you always mix, then '
            'bake, then ice. [[slnc 700]] In this video, an online shop '
            'fulfils orders in three very different ways. [[slnc 500]] By '
            'the end, you will know what the word final really buys you. '
            '[[slnc 300]] How to choose between a required step, a '
            'default, and a hook. [[slnc 300]] And the one serious price '
            'this pattern charges.'
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
            'Here is the scenario. [[slnc 400]] Every order the shop '
            'fulfils goes through the same six steps. [[slnc 300]] '
            'Validate, reserve the stock, charge the customer, pack, '
            'dispatch, and notify the customer. [[slnc 500]] That order '
            'is not a matter of taste. [[slnc 300]] Charge before you '
            'reserve, and you may take money for goods you cannot supply. '
            '[[slnc 300]] Notify before you dispatch, and you email a '
            'tracking number that does not exist yet. [[slnc 600]] But '
            'what happens inside each step varies enormously. [[slnc '
            '300]] The shop fulfils from its own warehouse, from '
            'marketplace sellers, and as digital downloads. [[slnc 300]] '
            'Holding stock in a warehouse, asking a seller to confirm, '
            'and creating a licence key have nothing in common. [[slnc '
            '300]] Except where they sit in that list of six.'
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
            'The obvious first approach is to write each route out in '
            'full. [[slnc 300]] Three methods, one per route, each doing '
            'all six steps from start to finish. [[slnc 500]] To be fair, '
            'this is good code. [[slnc 300]] Each method reads top to '
            'bottom, with nothing hidden. [[slnc 300]] There is no new '
            'vocabulary to learn. [[slnc 300]] And on the day each was '
            'written, it was almost certainly correct. [[slnc 500]] Three '
            'copies of a six-step sequence is not a crisis by itself. '
            '[[slnc 300]] What happens to those copies over the next year '
            'is.'
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
            'Here is the day it goes wrong. [[slnc 400]] Someone moved '
            'one line, in one copy. [[slnc 300]] The digital route now '
            'notifies the customer before it dispatches. [[slnc 500]] '
            "Let's follow it. [[slnc 300]] The email quotes the licence "
            'key. [[slnc 300]] But dispatch has not run yet, so there is '
            'no key. [[slnc 300]] The customer receives a message that '
            'says: ready to download, key: not dispatched. [[slnc 400]] A '
            'moment later, the real key is created, and it is correct. '
            '[[slnc 300]] But nobody will ever tell the customer what it '
            'is. [[slnc 500]] Nothing crashed, nothing failed to compile, '
            'and no test failed. [[slnc 300]] The order was marked as '
            'fulfilled. [[slnc 500]] The marketplace copy drifted too, in '
            'a different place. [[slnc 300]] The charge moved above the '
            "seller's confirmation. [[slnc 300]] So a customer can be "
            'charged forty-two pounds, and then told the seller cannot '
            'supply it.'
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
            'So why does this hurt? [[slnc 400]] Most people would say, '
            'duplication. [[slnc 300]] That is true, but it is the weaker '
            'argument. [[slnc 500]] Here is the stronger one. [[slnc '
            '300]] What is duplicated that the compiler cannot see? '
            '[[slnc 300]] The order of the steps. [[slnc 400]] It exists '
            'only as a habit, typed out by hand in three places. [[slnc '
            '300]] Nothing in the code knows it is a sequence. [[slnc '
            '300]] So it drifts, one line at a time, in whichever copy '
            'someone last edited in a hurry. [[slnc 500]] And when the '
            'shop adds a seventh step, like a fraud check, someone must '
            'find all three copies. [[slnc 300]] And insert the step in '
            'the same place in each. [[slnc 300]] A copy that misses it '
            'is not an error. [[slnc 300]] It is just a route that '
            'silently skips the check.'
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
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Define the skeleton of an algorithm '
            'in one method, and leave some steps to subclasses. [[slnc '
            '300]] Subclasses can change certain steps, without changing '
            "the algorithm's structure. [[slnc 500]] In plain words: the "
            'subclass decides how each step works. [[slnc 300]] It never '
            'decides when the steps run. [[slnc 500]] And that last part '
            'is not a polite request. [[slnc 300]] The base class '
            'enforces it. [[slnc 300]] In Java, it is enforced by one '
            'keyword.'
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
            'Here is an everyday example: a cake recipe. [[slnc 400]] '
            'Which parts can you change? [[slnc 500]] The flavouring, '
            'yes. [[slnc 300]] Lemon, chocolate, whatever you have. '
            '[[slnc 300]] The tin, yes. [[slnc 300]] The icing is '
            'optional. [[slnc 300]] Plenty of good cakes have none. '
            '[[slnc 500]] But mix, then bake, then ice, is not up for '
            'debate. [[slnc 300]] Ice it before you bake it, and you do '
            'not get a different style of cake. [[slnc 300]] You get no '
            'cake, and no icing. [[slnc 500]] That is the whole pattern. '
            '[[slnc 300]] The ingredients are the steps you fill in. '
            '[[slnc 300]] The icing is an optional hook. [[slnc 300]] And '
            'the order is fixed by the person who wrote the recipe, on '
            'purpose.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'So here are the roles. [[slnc 500]] At the top is the '
            'abstract class, called Fulfilment Process. [[slnc 300]] '
            'Inside it is the template method itself, called fulfil, '
            'marked final. [[slnc 300]] It is the only thing in the '
            'system that knows the six steps have an order. [[slnc 500]] '
            'Below it are the three routes: warehouse, marketplace, and '
            'digital. [[slnc 300]] The warehouse route overrides four '
            'methods. [[slnc 300]] The marketplace route overrides six. '
            '[[slnc 300]] The digital route overrides seven. [[slnc 400]] '
            'The most ordinary route is the shortest. [[slnc 300]] That '
            "tells you the base class's defaults were well chosen. [[slnc "
            '500]] And every step writes to a shared report. [[slnc 300]] '
            'So the project can prove its claim. [[slnc 300]] Run all '
            'three routes, list the steps each one performed, and the '
            'three lists are identical.'
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
            'Here is the whole pattern, in one method. [[slnc 400]] Seven '
            'calls, in order, in the fulfil method. [[slnc 300]] Every '
            'route in the system runs exactly this method. [[slnc 500]] '
            'The key word is final. [[slnc 300]] A route may decide how '
            'any step behaves. [[slnc 300]] It cannot decide when the '
            'steps run. [[slnc 300]] That is not a rule someone must '
            'remember in code review. [[slnc 300]] Breaking it is a '
            'compile error. [[slnc 600]] Each step is also a deliberate '
            'kind of gap. [[slnc 300]] Validate is private, so nobody can '
            'replace it. [[slnc 300]] Three steps are abstract, so every '
            'route must fill them in. [[slnc 300]] Two steps have '
            'defaults, so a route that wants the usual behaviour writes '
            'nothing. [[slnc 300]] And the last step does nothing at all, '
            'on purpose. [[slnc 300]] We will come back to that one.'
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
            'So, there are three kinds of gap, and choosing between them '
            'is most of the work. [[slnc 500]] Abstract means: you must '
            'fill this in. [[slnc 300]] Use it when no default could be '
            'right for everyone. [[slnc 300]] Reserving stock in a '
            'warehouse and asking a seller to confirm have nothing in '
            'common to share. [[slnc 500]] A default means: you may '
            'replace this. [[slnc 300]] Packing is usually the same, box '
            'it and label it. [[slnc 300]] So the warehouse route says '
            'nothing about packing, and gets the right behaviour for '
            'free. [[slnc 500]] And then hooks, which come in two kinds. '
            '[[slnc 300]] One kind is a question, such as: does this '
            'route need a shipping address? [[slnc 300]] The digital '
            'route answers no, without weakening the address check for '
            'anyone else. [[slnc 400]] The other kind is a place to join '
            'in. [[slnc 300]] A step called after fulfilment does nothing '
            'by default, but runs every time. [[slnc 300]] So the '
            'marketplace route can record its commission there, without '
            'the base class ever knowing marketplaces exist. [[slnc 500]] '
            'But be careful with hooks. [[slnc 300]] Each one is a '
            'permission you give away for the life of the class.'
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
            'Now here is the payoff. [[slnc 400]] In the digital route, '
            'dispatch creates the licence key, and writes it on the '
            'report. [[slnc 300]] Then notify reads the key from the '
            'report, and puts it in the email. [[slnc 500]] These are the '
            'same two actions as in the naive version. [[slnc 300]] Here '
            'they are correct, and not because the author was careful. '
            '[[slnc 500]] Notify can rely on dispatch having already run. '
            '[[slnc 300]] Because fulfil is final. [[slnc 300]] So no '
            'route, today or next year, can ever swap those two steps. '
            '[[slnc 500]] That is what the keyword buys. [[slnc 300]] A '
            "step can safely depend on an earlier step's work, forever."
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
            'Here is the test that proves the claim. [[slnc 400]] It uses '
            'a recording route. [[slnc 300]] Each of its steps does '
            'nothing, except write down its own name. [[slnc 300]] Run '
            'it, and you can check the order of the steps directly. '
            '[[slnc 500]] Could you write this test for the naive '
            'version? [[slnc 300]] Only for the three routes that exist '
            'today. [[slnc 300]] It could say nothing about a fourth '
            'route added next year, and that is exactly where drift comes '
            'from. [[slnc 500]] Here, the guarantee is built into the '
            'structure. [[slnc 300]] The test simply confirms it. [[slnc '
            '400]] There are forty-six tests in total. [[slnc 300]] Some '
            "of them deliberately confirm the naive version's two bugs, "
            'so you can hear exactly what goes wrong.'
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
            "Let's run the demo. [[slnc 500]] First, the hand-written "
            'version. [[slnc 300]] An email about a licence key is sent '
            'before the key even exists. [[slnc 500]] Second, the same '
            'three routes, running through the template. [[slnc 300]] The '
            'demo lists the steps each route performed. [[slnc 300]] '
            'Three completely different implementations, and three '
            'identical lists. [[slnc 300]] Not because the routes agreed. '
            '[[slnc 300]] None of them knows what the others do. [[slnc '
            '300]] Because only the fulfil method decides the order. '
            '[[slnc 500]] Finally, a fourth route is added: click and '
            'collect. [[slnc 300]] One new class. [[slnc 300]] No change '
            'to the base class, or to any existing route. [[slnc 300]] '
            'And it gets the same six steps, in the same order, for free.'
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
            'So, what should you remember? [[slnc 400]] One final method '
            'owns the order, and subclasses fill in the steps. [[slnc '
            '300]] Abstract means must fill in. [[slnc 300]] A default '
            'means may replace. [[slnc 300]] A hook means may join in. '
            '[[slnc 300]] A step can rely on an earlier step, because the '
            'order cannot change. [[slnc 300]] And a new route is one new '
            'class, with nothing that works reopened. [[slnc 600]] Now '
            'the honest cost. [[slnc 300]] Each route uses up its one '
            'chance to extend a class. [[slnc 300]] Every route extends '
            'this base class, and can never extend anything else. [[slnc '
            '300]] That is why composing objects is usually the better '
            'modern default. [[slnc 400]] Also, the sequence is shared by '
            'everyone. [[slnc 300]] Add a seventh step, and every route '
            'changes at once, including ones you cannot see. [[slnc 600]] '
            'Finally, two related patterns. [[slnc 300]] Factory Method '
            'is this same idea, narrowed to a single gap that creates an '
            'object. [[slnc 300]] And Strategy uses composition instead '
            'of inheritance. [[slnc 300]] It costs nothing, but it '
            'guarantees nothing about order. [[slnc 500]] You have met '
            "Template Method already, in Java's Abstract List, in "
            "servlets, in JUnit's before-each methods, and in every "
            'Spring class with Template in its name.'
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
        ],
        narration=(
            "That's the Template Method pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Let '
            'one final method own the order of the steps, and let '
            'subclasses fill in only the steps themselves. [[slnc 500]] '
            'The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Add a fraud check '
            'between validate and reserve. [[slnc 300]] Add it first to '
            'the template, and then to the three hand-written copies. '
            '[[slnc 300]] And count how many edits each one takes. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
