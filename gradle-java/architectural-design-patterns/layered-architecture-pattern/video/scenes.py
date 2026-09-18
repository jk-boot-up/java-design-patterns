"""Scene definitions for the Layered Architecture teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own with the screen off. No sentence
says "as you can see"; architecture is described as rules and directions in
words -- "the checkout names the application layer, and nothing else" -- so a
listener holds the same picture a viewer gets from the slide.

This is the category's reference project and it goes first for a reason: the
architecture almost every reader already has, drawn as four folders, and the
video's whole argument is that four folders are not an architecture until
something checks them.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Layered Architecture",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Layered Architecture "
            "pattern in Java, and it is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] Let's start with the plain definition. A "
            "layered architecture splits a program into stacked groups of "
            "classes, called layers, where each layer is only allowed to "
            "depend on the layer directly beneath it. The promise is that a "
            "change to one layer should not force a change to the layers above "
            "it. [[slnc 350]] Now here is the part almost nobody says out "
            "loud. Drawing four boxes on a whiteboard costs nothing, and "
            "nothing stops a developer, on a busy Tuesday, from adding one "
            "import that skips a box. [[slnc 300]] So this video builds a real "
            "working online shop -- one order, four layers -- and does three "
            "things with it. It shows the shortcut happening, on purpose, and "
            "shows that nothing in the build objects to it. Then it writes the "
            "rule down as a test, and watches that test go red, naming the "
            "class that broke it. And then it performs a real change -- "
            "swapping out the entire way orders are stored -- and counts, from "
            "the actual files on disk, exactly what that change touched. "
            "[[slnc 300]] By the end you will know why four folders with the "
            "right names are not an architecture, and what the one thing is "
            "that turns them into one."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online shop. One order, three lines.",
            "",
            "    Ada Okafor, customer cust-8801, buys:",
            "    1 Espresso Machine        £249.00",
            "    1 Burr Grinder             £89.50",
            "    2 Coffee Beans, 1kg        £44.00",
            "                       Total  £382.50",
            "",
            "Stock is checked. Payment is taken.",
            "A confirmation is sent.",
        ],
        narration=(
            "Here is the feature this whole video is built around, and it "
            "stays the same from the first minute to the last. [[slnc 250]] "
            "Ada Okafor, customer number cust-8801, orders three things from "
            "an online shop: one espresso machine at two hundred and "
            "forty-nine pounds, one burr grinder at eighty-nine pounds fifty, "
            "and two bags of coffee beans at twenty-two pounds each. That "
            "comes to three hundred and eighty-two pounds fifty. [[slnc 300]] "
            "Placing that order means four things happen, in order. Stock is "
            "checked, so nobody buys the last grinder twice. Payment is taken. "
            "Then, and only then, the stock is reduced and the order is "
            "written down. And a confirmation email goes out. [[slnc 300]] "
            "Hold onto that order. Every version of the code in this video -- "
            "the bad one, the good one, and the one with a shortcut hidden in "
            "it -- places exactly this order, so you can compare them "
            "directly rather than take my word for which one is better."
        ),
    ),
    dict(
        key="03-no-layers",
        kind="code",
        title="Version One — No Layers At All",
        body="""public class EverythingOrderService {

    private final Map<String,Long> priceInPence;
    private final Map<String,Integer> stock;
    private final Map<String,String> orders;
    private final List<String> sentEmail;

    public String checkout(String customerId,
            String email, Map<String,Integer> w) {
        // price it, check stock, reduce stock,
        // store the order, send the email --
        // all seventy-four lines, one method.
    }
}""",
        narration=(
            "Before there is a layer to skip, there have to be no layers at "
            "all, so that is where the project starts. [[slnc 300]] This is "
            "one class. It holds the catalogue prices in a map, the stock "
            "levels in a map, the placed orders in a map, and the sent emails "
            "in a list, and one method does the entire checkout: work out the "
            "total, check the stock, take the money, reduce the stock, write "
            "the order down, send the email. Seventy-four lines, and every "
            "single one of them is easy to read on its own. [[slnc 350]] Here "
            "is the property no amount of tidying removes. Try to write a "
            "test that only checks the arithmetic -- that three lines really "
            "do come to three hundred and eighty-two pounds fifty -- without "
            "touching anything else. You cannot. To construct this class at "
            "all, you construct its catalogue map, its order map, and its "
            "list of sent email, because they are fields of the same object. "
            "The pricing and the storage are welded together, and there is no "
            "seam anywhere to prise them apart."
        ),
    ),
    dict(
        key="04-four-layers",
        kind="bullets",
        title="Four Layers, Stacked",
        body=[
            "presentation",
            "    turns a request into a call, and an answer into words",
            "",
            "application",
            "    runs the checkout as one fixed sequence of steps",
            "",
            "domain",
            "    the nouns -- an order, a price, a product",
            "    knows nothing above it, or below it",
            "",
            "infrastructure",
            "    where orders, products, cards and email actually live",
        ],
        narration=(
            "So we split it. Four layers, and I want to name each one and say "
            "exactly what job it does, because the names alone are not the "
            "architecture -- what each one is not allowed to know is. [[slnc "
            "300]] At the top, presentation. Its only job is to turn what a "
            "customer typed into one call, and turn what comes back into "
            "words. Underneath it, application. This layer runs the checkout "
            "as a fixed sequence: check stock, charge the card, reduce stock, "
            "save the order, send the confirmation. Reading that sentence "
            "aloud is genuinely most of what this layer does. [[slnc 350]] "
            "Below that, domain -- the nouns of the business. An order, a "
            "price, a product. These classes know nothing about anything "
            "above them or below them, because an order and a price are true "
            "whether or not anybody is storing them or showing them to "
            "anyone. [[slnc 300]] And at the bottom, infrastructure -- where "
            "orders, products, card charges and emails actually live. "
            "[[slnc 300]] The rule that makes this an architecture rather "
            "than four labelled folders is one sentence: each layer depends "
            "only on the layer directly beneath it. Presentation reaches "
            "application. Application reaches infrastructure. Nothing reaches "
            "back up, and nothing reaches sideways past its neighbour."
        ),
    ),
    dict(
        key="05-shortcut",
        kind="console",
        title="The One Call That Ruins Them",
        body="""THREE. The one call that ruins them.
  ord-1001 £382.50

  that screen skipped the application layer and read
  storage directly.
  it compiles, it is tidy, the tests pass, and it shipped.

  NOTHING IN THE BUILD OBJECTED.""",
        narration=(
            "Now here is the moment this whole category exists to name. "
            "[[slnc 300]] Somebody needs a screen listing a customer's past "
            "orders. The application layer has no method for that yet, and "
            "adding one properly means a request object, a result object and "
            "a service method -- three files, to return rows that are sitting "
            "right there in the order storage. So the new screen takes the "
            "storage class directly. Ten minutes, instead of an afternoon. "
            "[[slnc 350]] It compiles. It is tidy. A reviewer skimming the "
            "diff sees a small, clear screen and approves it without a "
            "comment. The tests pass. It ships. [[slnc 350]] Read that last "
            "line on the screen again, because it is the entire lesson of "
            "this project. Nothing in the build objected. The four layers "
            "still exist, the names on the folders are still correct, and one "
            "screen has quietly reached straight past application into "
            "storage -- and not one tool anywhere told anybody. That is what "
            "layering as it is usually practised actually is: a convention, "
            "and a convention that nothing checks decays, not all at once, "
            "but one reasonable Tuesday at a time."
        ),
    ),
    dict(
        key="06-vague",
        kind="quote",
        title="Why This Keeps Happening",
        body=[
            "Architecture is usually taught with diagrams",
            "and adjectives -- decoupled, maintainable, clean.",
            "",
            "None of which a build can check.",
            "",
            "A diagram cannot fail.",
            "A test can.",
        ],
        narration=(
            "Before I show you the fix, I want to name the actual problem, "
            "because it is not that anyone involved was careless. [[slnc "
            "300]] Architecture is almost always taught with diagrams and "
            "adjectives -- decoupled, maintainable, clean. Every one of those "
            "words sounds like a property of the code, and not one of them is "
            "something a build can check. A diagram lives on a wiki page, "
            "gets glanced at during onboarding, and is never consulted again. "
            "[[slnc 350]] So the actual claim this video is going to make is "
            "narrower and much more useful than 'be disciplined'. A dependency "
            "rule -- presentation may not touch infrastructure -- is a "
            "sentence about imports, and a sentence about imports is exactly "
            "the kind of thing a program can check mechanically, every single "
            "time it builds. [[slnc 300]] A diagram cannot fail. A test can. "
            "Everything from here on is about turning the first kind of "
            "sentence into the second kind."
        ),
    ),
    dict(
        key="07-rule-as-test",
        kind="code",
        title="The Rule, Written Where A Build Can Read It",
        body="""ArchRule rule = noClasses()
    .that().resideInAPackage(PRESENTATION)
    .should().dependOnClassesThat()
        .resideInAPackage(INFRASTRUCTURE)
    .because(
        "a screen that reads storage directly "
      + "has to be opened every time storage "
      + "changes, and nothing warns you");

rule.check(layers);""",
        narration=(
            "This is the whole architecture, written down. Not a diagram of "
            "it -- the thing itself, in a form a build can check. [[slnc "
            "300]] It uses a small open-source library called ArchUnit, and I "
            "want you to read it almost as English, because that is "
            "deliberately how it is written. No classes that reside in the "
            "presentation package should depend on classes that reside in the "
            "infrastructure package. [[slnc 350]] That is it. That is one "
            "test method, it runs every time the command 'gradlew test' runs, "
            "alongside every other test in the project, and it costs about "
            "thirty lines. Compare that cost with what it buys: the "
            "difference between a layered architecture and four folders with "
            "layered names. [[slnc 300]] And notice the 'because' clause at "
            "the end. ArchUnit lets you write down why the rule exists, in "
            "plain language, and that sentence is printed to whoever reads "
            "the failure later -- which matters enormously for the next "
            "thing I want to show you."
        ),
    ),
    dict(
        key="08-red",
        kind="console",
        title="Watching It Go Red",
        body="""Architecture Violation [Priority: MEDIUM] -
  Rule 'no classes that reside in a package
  '..presentation..' should depend on classes
  that reside in a package '..infrastructure..''
  was violated (1 time):

Class <...naive.presentation.OrderHistoryScreen>
  depends on class
  <...infrastructure.InMemoryOrderTable>
  in (OrderHistoryScreen.java:24)""",
        narration=(
            "So let's watch it happen. There is a second test in this "
            "project whose only job is to prove the rule actually catches "
            "something, by pointing the exact same sentence at the naive "
            "screen from earlier and asserting that it fails. [[slnc 300]] "
            "Here is what the build prints. Architecture Violation. The rule "
            "was violated one time. And then the part that matters most: it "
            "names the class -- OrderHistoryScreen -- and it names exactly "
            "what that class reached for -- InMemoryOrderTable -- and it even "
            "gives the line number. [[slnc 400]] Sit with what just happened. "
            "'The screen does not touch the database' stopped being something "
            "a team promises at a whiteboard and forgets within a month, and "
            "became something that fails a build, by name, in under a "
            "second. A green test that has never been seen red proves "
            "nothing at all -- this is what makes the green one, on the real "
            "project, worth trusting."
        ),
    ),
    dict(
        key="09-forced-change",
        kind="console",
        title="The Forced Change",
        body="""FORCED CHANGE: replace the storage layer
  a map keyed by order id  ->  an append-only
  log, read backwards

  files added     : 1   AppendOnlyOrderTable.java
  files modified  : 1   PlaceAnOrderDemo.java
  lines changed   : 1
  classes in the four layers : 17
  of those, opened           : 1
  of those, never opened     : 16""",
        narration=(
            "An architecture's whole claim is about the future -- this shape, "
            "it says, makes some future change cheap. So this project does "
            "not describe that. It performs it, on camera, and counts the "
            "cost. [[slnc 350]] The change: orders stop living in a simple "
            "map keyed by order id, and start living in an append-only log, "
            "read backwards to find the newest version of an order. That is "
            "roughly how a real log-structured store behaves, and it is about "
            "as different a storage decision as one page of code can make. "
            "[[slnc 350]] Here is the bill, counted from the real files on "
            "disk at the moment the demo runs, not from memory and not from "
            "an estimate. One file added. One file modified -- the "
            "composition root, the single place in the whole project that is "
            "allowed to say the word 'new' for a concrete storage class. One "
            "line changed. [[slnc 350]] And then the number that actually "
            "carries the argument. Seventeen classes make up the four real "
            "layers. Sixteen of them were never opened. Not the word "
            "'decoupled'. The number."
        ),
    ),
    dict(
        key="10-shortcut-bill",
        kind="console",
        title="And The One That Took The Shortcut",
        body="""AND THE ONE THAT TOOK THE SHORTCUT
  naive/presentation/OrderHistoryScreen.java
  imports InMemoryOrderTable

  it went straight to storage, so the swap
  does not compile for it

  every screen that went through the
  application layer: untouched""",
        narration=(
            "And here is the other half of that same story. [[slnc 250]] "
            "OrderHistoryScreen -- the naive screen from earlier, the one "
            "that took ten minutes instead of an afternoon -- imported "
            "InMemoryOrderTable directly. The concrete class, not the "
            "interface. [[slnc 300]] So when the storage layer is replaced, "
            "that screen does not compile. It cannot be handed the new store, "
            "because it never asked for the interface in the first place. "
            "Every screen that went through the application layer as it was "
            "supposed to: untouched, all sixteen of them. The one that took "
            "the shortcut: broken, by a change it was never even involved "
            "in. [[slnc 350]] That is the bill for the ten minutes, and "
            "notice when it arrives. Not on the Tuesday the shortcut was "
            "written -- on some later day, doing something completely "
            "unrelated, when nobody in the room remembers there ever was a "
            "ten-minute decision to begin with."
        ),
    ),
    dict(
        key="11-pointing-down",
        kind="diagram",
        title="What This Project Does Not Fix",
        body=None,
        narration=(
            "Before the bill for the whole architecture, one honest "
            "admission, because this project should not pretend to have "
            "solved everything. [[slnc 300]] Look at what the application "
            "layer itself is allowed to import. It names the storage "
            "interface, the card network, and the email sender -- all three "
            "defined in the infrastructure layer beneath it. That is allowed, "
            "under this architecture's own rule, because application sits "
            "directly above infrastructure. [[slnc 350]] But say what that "
            "actually means out loud. The application layer still reaches "
            "downward into infrastructure to even know those names exist. "
            "The interface for how orders are stored is defined down there, "
            "with the implementation, rather than up here, with the code that "
            "uses it. [[slnc 350]] That single fact -- domain and application "
            "still depending downward onto infrastructure -- is exactly what "
            "the next project in this category, Hexagonal Architecture, "
            "changes. One interface moves upward into the core, storage "
            "implements it instead of defining it, and the direction of that "
            "one dependency reverses. This project is not that project. It "
            "is one deliberate step before it."
        ),
    ),
    dict(
        key="12-order-matters",
        kind="code",
        title="An Order That Is Not Obvious",
        body="""cards.charge(order.customerId(), order.total());

for (OrderLine line : order.lines()) {
    products.reduceStock(line.sku(),
            line.quantity());
}
orders.save(order);
email.send(customerEmail, confirmationFor(order));

// charge FIRST. nothing below this line
// can be undone for free, and nothing above
// it has changed anything yet.""",
        narration=(
            "One more detail worth a scene of its own, because it lives "
            "inside the application layer and it is easy to walk past. "
            "[[slnc 250]] The card is charged before anything at all is "
            "written down. Not after the stock is reduced, not after the "
            "order is saved -- first. [[slnc 350]] Try the other order for a "
            "moment. Save the order, reduce the stock, then charge the card. "
            "Now a declined card leaves an order sitting in storage and stock "
            "missing off the shelf, and nothing anywhere records that neither "
            "of those should have happened. [[slnc 350]] Charging first means "
            "a decline stops the whole sequence before a single fact has "
            "changed anywhere in the system. That is not an accident of how "
            "this class happened to be typed -- it is exactly the kind of "
            "decision an application layer exists to own, once, in one "
            "place, instead of leaving it to be repeated, and potentially "
            "reordered, at every screen that ever needs a checkout."
        ),
    ),
    dict(
        key="13-bill",
        kind="bullets",
        title="The Bill",
        body=[
            "Indirection.",
            "    A form field touches presentation, application,",
            "    and domain -- one idea, four places.",
            "",
            "Pass-through layers.",
            "    Some methods only forward a call. Real,",
            "    and genuinely tedious.",
            "",
            "The bottom layer is still the database.",
            "    Application still names infrastructure",
            "    by package. Hexagonal exists to fix this.",
        ],
        narration=(
            "A project that only shows what an architecture buys is a sales "
            "pitch, so here is what this one costs, honestly. [[slnc 300]] "
            "First, indirection. Add one field to the checkout form and it "
            "touches the presentation layer's request handling, the "
            "application layer's request object, and possibly a domain "
            "object underneath. One idea from a customer's point of view "
            "becomes four places to edit from yours. [[slnc 300]] Second, "
            "pass-through layers. Some methods on the application layer exist "
            "purely to forward a call and reshape its arguments a little. "
            "That is real work with no payoff of its own, and it is "
            "genuinely tedious, and pretending it is not helps nobody. "
            "[[slnc 350]] And third, the one I already showed you: the "
            "bottom layer is still the database, in the sense that matters. "
            "The application layer still has to name the storage package to "
            "even compile. Layering organises a codebase. It does not, on "
            "its own, invert which way a dependency points -- and that "
            "distinction is worth being precise about before the next video "
            "in this series claims to fix it."
        ),
    ),
    dict(
        key="14-too-much",
        kind="bullets",
        title="When This Is Too Much",
        body=[
            "Worth it: more than one caller of the same logic,",
            "or code expected to outlive its first storage choice.",
            "",
            "Not worth it: a script that reads a file,",
            "does one calculation, and prints a result once.",
            "",
            "The tell: if writing the request object, the result",
            "object and the service method takes longer than",
            "the screen is worth -- stop.",
        ],
        narration=(
            "Every project in this category has to answer this question "
            "plainly, out loud, or it is only ever arguing for more "
            "structure. [[slnc 300]] Four layers and an architecture test are "
            "worth their weight for anything with more than one caller of the "
            "same business logic, or anything you genuinely expect to "
            "outlive its first storage choice. [[slnc 300]] They are not "
            "worth it for a script that reads a file, does one calculation, "
            "and prints a result once. A four-package skeleton wrapped around "
            "fifteen lines of real logic is not layering -- it is packaging, "
            "and the giveaway is exactly the shortcut this video showed you "
            "in reverse. [[slnc 350]] If writing the request object, the "
            "result object and the service method for a new screen would "
            "take longer than the screen itself is worth to anyone, the "
            "layers have already stopped paying for themselves, and the "
            "honest move is to stop building them, not to build them badly."
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository, running offline with nothing",
            "installed but a JDK. Try widening the architecture test",
            "to cover the naive package for real, and watch the build",
            "name every shortcut in the project at once.",
        ],
        narration=(
            "That's layered architecture. [[slnc 250]] If you take one "
            "sentence away, take this one: a layered architecture is not the "
            "four folders. It is the test that fails when somebody reaches "
            "past one. [[slnc 350]] The full source, the written notes, the "
            "diagrams and an animated walkthrough are all in the repository, "
            "and every bit of it runs offline with nothing installed but a "
            "Java development kit -- no database, no web framework, nothing. "
            "[[slnc 300]] If you try one exercise, try this. Widen the "
            "architecture test so it checks the naive package as well as the "
            "real one, run it, and read every violation the build finds in "
            "one go. [[slnc 300]] If this helped, a like genuinely does help "
            "other people find it, and subscribe if you would like the rest "
            "of the series -- this category has four more architectures to "
            "go, and each one is one deliberate step from this project. "
            "[[slnc 250]] Thanks for watching, and I'll see you in the next "
            "one."
        ),
    ),
]
