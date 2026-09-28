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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Layered Architecture pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A layered '
            'architecture splits a program into stacked groups of '
            'classes, called layers. [[slnc 300]] Each layer may only '
            'depend on the layer directly beneath it. [[slnc 300]] The '
            'promise is that changing one layer should not force changes '
            'in the layers above it. [[slnc 600]] Think of a restaurant. '
            '[[slnc 300]] The customer talks to the waiter. [[slnc 300]] '
            'The waiter talks to the chef. [[slnc 300]] The chef takes '
            'food from the store room. [[slnc 300]] The customer never '
            'walks into the store room. [[slnc 700]] But here is what '
            'people rarely say. [[slnc 300]] Drawing four boxes on a '
            'whiteboard costs nothing. [[slnc 300]] And nothing stops a '
            'busy developer adding one import that skips a box. [[slnc '
            '500]] So in this video, we build a real online shop with '
            'four layers. [[slnc 300]] We watch someone take a shortcut, '
            'and see that nothing complains. [[slnc 300]] Then we write '
            'the rule as a test, and watch it catch the shortcut. [[slnc '
            '300]] And finally, we make a real change, and count exactly '
            'what it touched.'
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
            'Here is the job, and it stays the same for the whole video. '
            '[[slnc 400]] A customer called Ada Okafor orders three '
            'things from an online shop. [[slnc 300]] One espresso '
            'machine, for two hundred and forty-nine pounds. [[slnc 300]] '
            'One coffee grinder, for eighty-nine pounds fifty. [[slnc '
            '300]] And two bags of coffee beans, at twenty-two pounds '
            'each. [[slnc 300]] The total is three hundred and eighty-two '
            'pounds fifty. [[slnc 500]] Placing that order takes four '
            'steps, in order. [[slnc 300]] Check the stock, so nobody '
            'buys the last grinder twice. [[slnc 300]] Take the payment. '
            '[[slnc 300]] Reduce the stock and save the order. [[slnc '
            '300]] And send a confirmation email. [[slnc 500]] Every '
            'version of the code in this video places exactly this order. '
            '[[slnc 300]] So you can compare them fairly.'
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
            'We start with no layers at all. [[slnc 400]] Just one class. '
            '[[slnc 300]] It keeps the prices, the stock levels, the '
            'orders, and the sent emails, all as fields. [[slnc 300]] And '
            'one method does the whole checkout. [[slnc 300]] It works '
            'out the total, checks stock, takes the money, reduces stock, '
            'saves the order, and sends the email. [[slnc 400]] '
            'Seventy-four lines, and each line is easy to read. [[slnc '
            '600]] But here is the problem. [[slnc 300]] Try to test just '
            'the arithmetic, that the three items really add up to three '
            "hundred and eighty-two pounds fifty. [[slnc 300]] You can't "
            'do it on its own. [[slnc 300]] To create this class, you '
            'must also create its stock, its orders, and its email list. '
            '[[slnc 400]] Pricing and storage are welded together, with '
            'no seam to pull them apart.'
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
            'So we split it into four layers. [[slnc 300]] The names '
            'matter less than what each layer is not allowed to know. '
            '[[slnc 600]] Layer one, at the top: presentation. [[slnc '
            '300]] It turns what the customer typed into one call. [[slnc '
            '300]] And it turns the answer back into words. [[slnc 500]] '
            'Layer two: application. [[slnc 300]] It runs the checkout as '
            'a fixed list of steps. [[slnc 300]] Check stock, charge the '
            'card, reduce stock, save the order, send the confirmation. '
            '[[slnc 500]] Layer three: domain. [[slnc 300]] These are the '
            'business nouns, like an order, a price, and a product. '
            '[[slnc 300]] They know nothing about the layers above or '
            'below them. [[slnc 500]] Layer four, at the bottom: '
            'infrastructure. [[slnc 300]] This is where orders, products, '
            'card payments and emails really live. [[slnc 600]] And the '
            'rule that makes this an architecture. [[slnc 300]] Each '
            'layer depends only on the layer directly beneath it. [[slnc '
            '300]] Nothing reaches back up. [[slnc 300]] And nothing '
            'skips past its neighbour.'
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
            'Now for the moment this whole video is about. [[slnc 500]] '
            "Someone needs a new screen that lists a customer's past "
            'orders. [[slnc 300]] The application layer has no method for '
            'that yet. [[slnc 300]] Adding one properly means three new '
            'files. [[slnc 400]] So the new screen talks to the order '
            'storage directly. [[slnc 300]] Ten minutes, instead of an '
            'afternoon. [[slnc 500]] It compiles. [[slnc 200]] It looks '
            'tidy. [[slnc 200]] The reviewer approves it. [[slnc 200]] '
            'The tests pass. [[slnc 200]] It ships. [[slnc 600]] And here '
            'is the lesson. [[slnc 300]] Nothing in the build objected. '
            '[[slnc 400]] The four layers still exist, and the folder '
            'names are still right. [[slnc 300]] But one screen has '
            'quietly skipped a layer, and no tool told anyone. [[slnc '
            '500]] A rule that nothing checks does not break all at once. '
            '[[slnc 300]] It decays, one reasonable shortcut at a time.'
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
            'Why does this keep happening? [[slnc 300]] Not because '
            'people are careless. [[slnc 500]] Architecture is usually '
            'taught with diagrams, and with words like decoupled, '
            'maintainable, and clean. [[slnc 300]] They sound like facts '
            'about the code. [[slnc 300]] But a build cannot check any of '
            'them. [[slnc 500]] A dependency rule is different. [[slnc '
            '300]] Presentation may not touch infrastructure. [[slnc '
            '300]] That is a sentence about imports. [[slnc 300]] And a '
            'program can check imports, every single time it builds. '
            '[[slnc 600]] A diagram cannot fail. [[slnc 300]] A test can.'
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
            'So here is the architecture, written as a test. [[slnc 400]] '
            'It uses a small open-source library called ArchUnit. [[slnc '
            '300]] And it reads almost like English. [[slnc 500]] No '
            'classes in the presentation package should depend on classes '
            'in the infrastructure package. [[slnc 600]] That is one test '
            'method. [[slnc 300]] It runs every time the other tests run. '
            '[[slnc 300]] And it costs about thirty lines. [[slnc 500]] '
            'The rule also carries a reason, written in plain words. '
            '[[slnc 300]] It says that a screen reading storage directly '
            'must be changed every time storage changes, and nothing '
            'warns you. [[slnc 300]] Whoever sees the failure later reads '
            'that reason too.'
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
            "Let's watch the rule catch the shortcut. [[slnc 400]] A "
            'second test points the same rule at the shortcut screen from '
            'earlier. [[slnc 300]] And it expects the rule to fail. '
            '[[slnc 500]] Here is what the build reports. [[slnc 300]] An '
            'architecture violation, found once. [[slnc 300]] It names '
            'the class, Order History Screen. [[slnc 300]] It names what '
            'that class reached for, the In Memory Order Table. [[slnc '
            '300]] And it even gives the line number. [[slnc 600]] So a '
            'promise made at a whiteboard has become a check that fails '
            'the build, by name, in under a second. [[slnc 400]] And '
            'because we have seen it fail, we can trust it when it '
            'passes.'
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
            'An architecture claims that some future change will be '
            "cheap. [[slnc 300]] So let's make that change, and count the "
            'cost. [[slnc 500]] The change: orders stop living in a '
            'simple map, looked up by order I D. [[slnc 300]] Instead, '
            'they live in an append-only log, read backwards to find the '
            'latest version of each order. [[slnc 300]] That is a very '
            'different way to store data. [[slnc 600]] Here is the bill, '
            'counted from the real files. [[slnc 300]] One file added. '
            '[[slnc 300]] One file modified: the setup code, which is the '
            'only place allowed to create the storage class. [[slnc 300]] '
            'And one line changed. [[slnc 600]] The four layers contain '
            'seventeen classes. [[slnc 300]] Sixteen of them were never '
            'opened. [[slnc 400]] Not the word decoupled. [[slnc 300]] A '
            'number.'
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
            'And what about the shortcut screen? [[slnc 400]] Remember, '
            'it used the in-memory storage class directly. [[slnc 300]] '
            'The concrete class, not the interface. [[slnc 500]] So when '
            'the storage is replaced, that screen no longer compiles. '
            '[[slnc 300]] It cannot accept the new storage, because it '
            'never asked for the interface. [[slnc 500]] Every screen '
            'that went through the application layer was untouched. '
            '[[slnc 300]] The one that took the shortcut is broken, by a '
            'change it had nothing to do with. [[slnc 600]] That is the '
            'real bill for those ten minutes. [[slnc 300]] And it arrives '
            'much later, on some unrelated day, when nobody remembers the '
            'shortcut was ever taken.'
        ),
    ),
    dict(
        key="11-pointing-down",
        kind="diagram",
        title="What This Project Does Not Fix",
        body=None,
        narration=(
            'Now, one honest admission. [[slnc 300]] This project does '
            'not solve everything. [[slnc 500]] Think about what the '
            'application layer imports. [[slnc 300]] The storage '
            'interface, the card payment interface, and the email '
            'interface. [[slnc 300]] All three are defined down in the '
            'infrastructure layer. [[slnc 300]] The rule allows that, '
            'because application sits directly above infrastructure. '
            '[[slnc 600]] But it means the application layer still '
            'reaches down into infrastructure, just to know those names. '
            '[[slnc 300]] The interface for storing orders lives down '
            'there, next to its implementation. [[slnc 300]] Not up here, '
            'next to the code that uses it. [[slnc 600]] Hexagonal '
            'Architecture, which has its own video, changes exactly this. '
            '[[slnc 300]] It moves that interface up into the core, so '
            'the dependency points the other way. [[slnc 300]] This '
            'project is one deliberate step before that.'
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
            'One more detail inside the application layer, because it is '
            'easy to miss. [[slnc 500]] The card is charged first. [[slnc '
            '300]] Before the stock is reduced, and before the order is '
            'saved. [[slnc 500]] Why? [[slnc 300]] Imagine the other way '
            'round. [[slnc 300]] Save the order, reduce the stock, and '
            'then charge the card. [[slnc 300]] If the card is declined, '
            'you are left with a saved order, and missing stock, that '
            'should never have happened. [[slnc 500]] Charging first '
            'means a declined card stops everything, before anything has '
            'changed. [[slnc 500]] This is exactly the kind of decision '
            'the application layer exists to own. [[slnc 300]] Once, in '
            'one place, instead of repeated on every screen that needs a '
            'checkout.'
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
            "Every pattern has a cost, so let's be honest about this one. "
            '[[slnc 500]] First, indirection. [[slnc 300]] Add one field '
            'to the checkout form, and it may touch three or four places. '
            '[[slnc 300]] One small idea for the customer becomes several '
            'edits for you. [[slnc 500]] Second, pass-through layers. '
            '[[slnc 300]] Some methods in the application layer only pass '
            'a call along. [[slnc 300]] That is real, and it is tedious. '
            '[[slnc 500]] Third, the problem we just heard about. [[slnc '
            '300]] The application layer still has to name the storage '
            'package to compile. [[slnc 300]] Layers organise the code. '
            '[[slnc 300]] On their own, they do not reverse which way a '
            'dependency points.'
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
            'So when is this too much? [[slnc 400]] Four layers and an '
            'architecture test are worth it when more than one caller '
            'uses the same business logic. [[slnc 300]] Or when the code '
            'will outlive its first choice of storage. [[slnc 500]] They '
            'are not worth it for a small script that reads a file, does '
            'one calculation, and prints the result. [[slnc 300]] Four '
            'packages around fifteen lines of logic is not layering. '
            '[[slnc 300]] It is just packaging. [[slnc 500]] Here is a '
            'simple test. [[slnc 300]] If adding the extra layer files '
            'for a new screen takes longer than the screen is worth, the '
            'layers have stopped paying for themselves.'
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
            "That's Layered Architecture. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A layered '
            'architecture is not the four folders, it is the test that '
            'fails when someone skips one. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 300]] It runs offline, '
            'with nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Widen the '
            'architecture test, so it also checks the shortcut package. '
            '[[slnc 300]] Run it, and read every violation the build '
            'finds. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
