"""Scene definitions for the Clean Architecture teaching video.

Written to stand on its own with the screen off. No sentence says "as you
can see"; architecture is described as rules and directions in words.

One step from Hexagonal Architecture, and honest about being a close
relative rather than something unrecognisable: the same inversion,
generalised into three named rings instead of one core/adapter split, with
the dependency-inversion moment shown in code and a forced change that adds
two things at once instead of swapping one.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Clean Architecture",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains Clean '
            'Architecture, in Java. [[slnc 300]] This video is presented '
            'by Jayasekhar Konduru. [[slnc 600]] First, a simple '
            'definition. [[slnc 300]] Clean Architecture arranges a '
            'program in rings, like the layers of an onion. [[slnc 300]] '
            'The most important rules sit in the middle. [[slnc 300]] The '
            'technical details sit on the outside. [[slnc 400]] And there '
            'is one rule. [[slnc 300]] Code may only depend on things '
            'further in. [[slnc 300]] Never on things further out. [[slnc '
            '700]] Think of a castle. [[slnc 300]] The treasure is in the '
            'keep, at the centre. [[slnc 300]] The walls and the gates '
            'are outside it. [[slnc 300]] You can rebuild a gate without '
            'touching the treasure. [[slnc 700]] In this video, we apply '
            'that to an online shop that places an order. [[slnc 300]] It '
            'is a close relative of Hexagonal Architecture, and we will '
            'say plainly what is new. [[slnc 400]] By the end, you will '
            'know the one trick the whole pattern rests on, in a single '
            'sentence.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The same order this whole category places.",
            "",
            "    Ada Okafor, customer cust-8801, buys:",
            "    1 Espresso Machine        £249.00",
            "    1 Burr Grinder             £89.50",
            "    2 Coffee Beans, 1kg        £44.00",
            "                       Total  £382.50",
            "",
            "The use case needs: a catalogue, a payment way,",
            "somewhere to store, and a way to notify.",
        ],
        narration=(
            'Here is the job. [[slnc 300]] It is the same order as every '
            'project in this series. [[slnc 300]] A customer called Ada '
            'Okafor buys an espresso machine, a coffee grinder, and two '
            'bags of coffee beans. [[slnc 300]] The total is three '
            'hundred and eighty-two pounds fifty. [[slnc 500]] To place '
            'that order, the program needs four things. [[slnc 300]] A '
            'catalogue, to check stock. [[slnc 200]] A payment gateway, '
            'to take the money. [[slnc 200]] Somewhere to store the '
            'order. [[slnc 200]] And a way to notify the customer. [[slnc '
            '500]] Each of those four needs is written as an interface. '
            '[[slnc 300]] And the use case itself, the code that places '
            'the order, owns all four.'
        ),
    ),
    dict(
        key="03-naive",
        kind="code",
        title="The Naive Version",
        body="""public class NaivePlaceOrderInteractor {

    private final InMemoryOrderRepository orders;
    private final InMemoryProductRepository catalog;
    private final InMemoryPaymentGateway payments;
    // a "use case" naming three GATEWAY types --
    // two circles further out than it should reach.
}""",
        narration=(
            "Let's start with the naive version. [[slnc 400]] It is a "
            'class that calls itself a use case. [[slnc 300]] But its '
            'constructor asks for three concrete classes: an in-memory '
            'order store, an in-memory product list, and an in-memory '
            'payment gateway. [[slnc 300]] Not interfaces. [[slnc 200]] '
            'Real, specific classes. [[slnc 500]] Does it work? [[slnc '
            '200]] Yes. It places the order correctly. [[slnc 400]] The '
            'problem is where it reaches. [[slnc 300]] It sits near the '
            'centre, but it names classes from the outer rings. [[slnc '
            '400]] So to test it, you must build all three of those '
            'classes first. [[slnc 300]] And to swap any one of them, you '
            'must open and edit this file.'
        ),
    ),
    dict(
        key="04-four-circles",
        kind="bullets",
        title="Four Circles, One Rule",
        body=[
            "Entities        the nouns, true on their own",
            "Use cases       the interactor, and its own",
            "                boundary interfaces",
            "Interface adapters   controllers in, gateways out",
            "Frameworks & drivers   the composition root",
            "",
            "Source code dependencies point only inward.",
            "Not mostly. Never outward. At any boundary.",
        ],
        narration=(
            'Now, the four rings, from the inside out. [[slnc 500]] Ring '
            'one, at the centre: entities. [[slnc 300]] These are the '
            'business nouns, like an order, a price, and a product. '
            '[[slnc 300]] They are true even if nothing else is running. '
            '[[slnc 500]] Ring two: use cases. [[slnc 300]] This is the '
            'code that does the job, like placing an order. [[slnc 300]] '
            'It declares interfaces for everything it needs. [[slnc 500]] '
            'Ring three: interface adapters. [[slnc 300]] Controllers '
            'bring requests in. [[slnc 300]] Gateways take calls out, to '
            'real storage. [[slnc 500]] Ring four, on the outside: '
            'frameworks and drivers. [[slnc 300]] In this project, that '
            'is just the main method that wires everything together. '
            '[[slnc 600]] And the one rule. [[slnc 300]] Code may only '
            'depend on things further in. [[slnc 300]] Not mostly. [[slnc '
            '200]] Always. [[slnc 300]] Even late on a Friday, when a '
            'shortcut looks tempting.'
        ),
    ),
    dict(
        key="05-not-hexagonal",
        kind="quote",
        title="This Is Not Hexagonal Again",
        body=[
            "Same centre, same inward rule. Four real differences:",
            "",
            "One ring becomes three -- adapters split from use cases.",
            "Inversion shown as two directions disagreeing, in code.",
            "The forced change ADDS two things. It swaps nothing.",
            "",
            "The fourth difference is this project's honesty",
            "about being the most over-applied pattern here.",
        ],
        narration=(
            'Is this just Hexagonal Architecture again? [[slnc 400]] '
            'Partly, yes. [[slnc 300]] The centre is the same, and so is '
            'the rule about which way dependencies point. [[slnc 500]] '
            'But there are four real differences. [[slnc 400]] One. '
            '[[slnc 200]] The single outside world of Hexagonal is split '
            'into named rings. [[slnc 300]] Translating between the use '
            'case and the outside world is treated as its own job, with '
            'its own ring. [[slnc 400]] Two. [[slnc 200]] We will see the '
            'key idea, called dependency inversion, happen in real code, '
            'not just in a picture. [[slnc 400]] Three. [[slnc 200]] The '
            'big change later in this video adds two new things at once, '
            'instead of swapping one. [[slnc 400]] And four. [[slnc 200]] '
            'This pattern is used far more often than it should be. '
            '[[slnc 300]] So later on, we will count its real cost.'
        ),
    ),
    dict(
        key="06-real-graph",
        kind="console",
        title="The Real Graph, Wired By Hand",
        body="""TWO. The real graph, wired by hand.
  {"status":201,"orderId":"ord-1001",
   "total":"£382.50"}
  PlaceOrderInteractor has two imports: entities
  and usecases. main() wired four gateways to it
  by hand -- no container anywhere in this project.""",
        narration=(
            'Now the proper version, running. [[slnc 400]] A pretend web '
            'request arrives at a controller. [[slnc 300]] The controller '
            "calls one method on the use case's own interface. [[slnc "
            '300]] The order is created, with status two hundred and one, '
            'and a total of three hundred and eighty-two pounds fifty. '
            '[[slnc 500]] Now think about the use case class itself. '
            '[[slnc 300]] It imports from only two places: the entities, '
            'and its own use-case package. [[slnc 300]] Not a single '
            'adapter. [[slnc 500]] So who connects it to the real '
            'gateways? [[slnc 300]] The main method does. [[slnc 300]] It '
            'creates four real gateways, and hands them to the use case, '
            'by hand. [[slnc 300]] About twenty lines of code. [[slnc '
            '200]] No framework, and nothing hidden.'
        ),
    ),
    dict(
        key="07-inversion",
        kind="code",
        title="The Dependency-Inversion Moment",
        body="""orders.save(order);

// orders : usecases.OrderRepository (interface)
// declared HERE. implemented two rings out,
// by InMemoryOrderRepository.
//
// CONTROL flows OUT, to the real class.
// The DEPENDENCY points IN, at this interface.""",
        narration=(
            "This is the most important idea in the video, so let's go "
            'slowly. [[slnc 500]] The use case calls orders dot save. '
            '[[slnc 300]] Here, orders is an interface called Order '
            'Repository. [[slnc 300]] That interface is declared in the '
            "use case's own package, in the inner ring. [[slnc 400]] The "
            'class that really stores orders lives two rings further out. '
            '[[slnc 300]] It implements that interface. [[slnc 600]] Now, '
            'ask two separate questions. [[slnc 400]] First question. '
            '[[slnc 200]] When this line runs, where does the program go? '
            '[[slnc 300]] Outward, into the outer class. [[slnc 300]] '
            'That is the direction of control. [[slnc 500]] Second '
            'question. [[slnc 200]] What must exist for this file to '
            'compile? [[slnc 300]] Only the interface, which lives in the '
            'inner ring. [[slnc 300]] So the dependency points inward. '
            '[[slnc 600]] Control flows out. [[slnc 300]] The dependency '
            'points in. [[slnc 400]] Letting those two directions '
            'disagree is the whole trick of this architecture.'
        ),
    ),
    dict(
        key="08-no-container",
        kind="bullets",
        title="Wired By Hand, On Purpose",
        body=[
            "Twenty lines of constructor calls in main().",
            "",
            "    reach into the outermost ring for a concrete",
            "    class, hand it to an interactor that only",
            "    knows an interface.",
            "",
            "No container here. An annotation that did this",
            "invisibly could not teach what watching it does.",
        ],
        narration=(
            'One choice in this project deserves an explanation. [[slnc '
            '400]] There is no dependency injection framework here at '
            'all. [[slnc 500]] Instead, the main method builds everything '
            'by hand, in about twenty lines. [[slnc 300]] It takes a real '
            'gateway from the outer ring. [[slnc 300]] And it hands it to '
            'a use case that only knows the interface. [[slnc 500]] Why '
            'do it by hand? [[slnc 300]] Because you can read those '
            'twenty lines, and see the inversion happen. [[slnc 300]] A '
            'framework annotation would do the same wiring invisibly, and '
            'the lesson would disappear with it. [[slnc 500]] If you want '
            'to see the same program wired by a framework instead, there '
            'is a companion project that does exactly that.'
        ),
    ),
    dict(
        key="09-forced-change",
        kind="console",
        title="Add Two Things At Once",
        body="""FOUR. Add a delivery mechanism AND a data
  source, at once.
  IMPORTED ord-1001 £249.00
  store: a flat file, one CSV-shaped line
  per order

  PlaceOrderInteractor.java: zero lines changed.
  CheckoutController.java: zero lines changed.""",
        narration=(
            'Now, the biggest change in this series. [[slnc 400]] And '
            'listen for the word: we add, we do not swap. [[slnc 500]] '
            'First new thing: a batch controller. [[slnc 300]] It reads '
            'orders from rows of a file, the way a nightly import would. '
            '[[slnc 400]] Second new thing: a store that keeps orders in '
            'a flat file, instead of in memory. [[slnc 400]] Both are '
            'added at the same time, as new files. [[slnc 500]] And the '
            'original path, the web controller and the in-memory store, '
            'is still there, and still works. [[slnc 400]] The imported '
            'order comes through, for two hundred and forty-nine pounds. '
            '[[slnc 400]] And the use case file? [[slnc 200]] Zero lines '
            'changed. [[slnc 300]] The web controller? [[slnc 200]] Zero '
            'lines changed. [[slnc 400]] The architecture grew by adding, '
            'which is the harder and more useful promise.'
        ),
    ),
    dict(
        key="10-both-work",
        kind="console",
        title="Both Paths, Proven Rather Than Narrated",
        body="""files added     : 2   BatchOrderController.java,
                       FileBackedOrderRepository.java
files modified  : 1   PlaceAnOrderDemo.java
lines changed   : 5
classes in entities + use cases : 15
of those, never opened          : 15""",
        narration=(
            "Let's count exactly what changed. [[slnc 400]] Two files "
            'were added: the batch controller, and the file-based store. '
            '[[slnc 300]] One file was modified: the main method, and '
            'only five lines of it. [[slnc 500]] Together, the entities '
            'and the use cases are fifteen classes. [[slnc 300]] Not one '
            'of those fifteen was opened for either change. [[slnc 500]] '
            'And this is not just a claim. [[slnc 300]] A test in the '
            'project runs both paths, the old one and the new one, in the '
            'same run. [[slnc 300]] And it checks that both succeed.'
        ),
    ),
    dict(
        key="11-rule-as-test",
        kind="code",
        title="The Rule, As ArchUnit's Own API",
        body="""Architectures.layeredArchitecture()
    .layer("Entities").definedBy(ENTITIES)
    .layer("UseCases").definedBy(USE_CASES)
    .layer("Adapters").definedBy(ADAPTERS)
    .whereLayer("Entities")
        .mayOnlyBeAccessedByLayers(
            "UseCases", "Adapters")
    .whereLayer("UseCases")
        .mayOnlyBeAccessedByLayers("Adapters");""",
        narration=(
            'How do we stop someone breaking the rule by accident? [[slnc '
            '400]] We turn the rule into a test, using a library called '
            'ArchUnit. [[slnc 500]] The test names three layers, by '
            'package. [[slnc 300]] Entities, use cases, and adapters. '
            '[[slnc 400]] Then it says who may use whom. [[slnc 300]] '
            'Entities may be used by use cases and by adapters, but they '
            'use neither. [[slnc 300]] Use cases may be used by adapters, '
            'but they only use entities. [[slnc 500]] One test holds the '
            'whole ring rule. [[slnc 400]] And a second test points the '
            'same rule at the naive version from the start. [[slnc 300]] '
            'That test is expected to fail, and to name the class that '
            'broke the rule.'
        ),
    ),
    dict(
        key="12-red",
        kind="console",
        title="Watching It Go Red",
        body="""Architecture Violation [Priority: MEDIUM] -
  Class <...naive.usecases
    .NaivePlaceOrderInteractor>
  depends on class
  <...adapters.gateway
    .InMemoryOrderRepository>""",
        narration=(
            'So what does a failure sound like? [[slnc 400]] The build '
            'reports an architecture violation. [[slnc 300]] It names the '
            'naive use case class. [[slnc 300]] And it names the '
            'in-memory order store that the class reached out for. [[slnc '
            '500]] That message is the real product of this whole series. '
            '[[slnc 300]] Not a diagram on a wiki page that nobody reads. '
            '[[slnc 300]] A clear sentence from the build, the moment the '
            'rule stops being true.'
        ),
    ),
    dict(
        key="13-bill",
        kind="bullets",
        title="The Bill",
        body=[
            "Fourteen files, for one checkout feature.",
            "",
            "    two DTOs, four boundaries, one interactor,",
            "    two controllers, four gateways.",
            "",
            "A CRUD screen built this way has more",
            "interfaces than behaviour.",
            "",
            "This is the most over-applied pattern here.",
        ],
        narration=(
            'Every pattern has a cost, and this one has the biggest bill '
            "in the series. [[slnc 500]] Let's count the files for this "
            'one feature, placing an order. [[slnc 300]] Two data '
            'transfer objects. [[slnc 200]] Four boundary interfaces. '
            '[[slnc 200]] One use case. [[slnc 200]] Two controllers. '
            '[[slnc 200]] And four gateways. [[slnc 300]] Fourteen files, '
            'to place an order. [[slnc 500]] A simple screen that just '
            'reads and writes records would end up with more interfaces '
            'than actual behaviour. [[slnc 400]] Honestly, this is the '
            'most over-used pattern in the series. [[slnc 300]] And '
            'without a team that understands the rule, it slowly decays '
            'into folders with impressive names, and nothing enforcing '
            'them.'
        ),
    ),
    dict(
        key="14-too-much",
        kind="bullets",
        title="When This Is Too Much",
        body=[
            "Worth it: long-lived systems, more than one",
            "delivery mechanism or data source, a domain",
            "genuinely worth protecting.",
            "",
            "Not worth it: almost everything smaller",
            "than that.",
        ],
        narration=(
            'So when are fourteen files worth it? [[slnc 400]] For '
            'systems that will live for many years. [[slnc 300]] For '
            'systems with more than one way in, or more than one place to '
            'store data, for real, not just in theory. [[slnc 300]] And '
            'for business rules worth protecting from whatever framework '
            'is popular this year. [[slnc 500]] And when is it not worth '
            'it? [[slnc 300]] Almost everything smaller than that. [[slnc '
            '400]] If you cannot name a second way in, or a second data '
            'store, that will actually exist, you are paying fourteen '
            'files for a change that will never come.'
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try adding a third delivery",
            "mechanism of your own, and confirm the use case layer",
            "needs zero lines changed to accept it.",
        ],
        narration=(
            "That's Clean Architecture. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Control flows '
            'outward, the dependency points inward, and letting those two '
            'disagree is the whole pattern. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 300]] It runs offline, '
            'with nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Add a third '
            'way into the program, of your own. [[slnc 300]] Then check '
            'that the use case layer needs zero lines changed to accept '
            'it. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
