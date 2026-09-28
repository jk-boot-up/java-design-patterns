"""Scene definitions for the Hexagonal Architecture teaching video.

Written to stand on its own with the screen off. No sentence says "as you
can see"; architecture is described as rules and directions in words.

One step from Layered Architecture: the same shared feature, the same
four-step checkout, with the one thing that project admitted it had not
fixed -- the use case naming its storage by import -- inverted here.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Hexagonal Architecture",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains '
            'Hexagonal Architecture, in Java. [[slnc 300]] It is also '
            'called Ports and Adapters. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The core of the program says '
            'what it needs from the outside world, as interfaces, in its '
            'own words. [[slnc 300]] Those interfaces are called ports. '
            '[[slnc 400]] Outside the core, adapters plug into those '
            'ports. [[slnc 300]] Some adapters do work for the core, like '
            'storing data. [[slnc 300]] Others call into the core, like a '
            'web request. [[slnc 400]] And every dependency points into '
            'the core, never out of it. [[slnc 600]] Think of the sockets '
            'on a wall. [[slnc 300]] The wall decides the shape of the '
            'socket. [[slnc 300]] A lamp, a kettle, or a charger just '
            'plugs in. [[slnc 300]] You can change the lamp without '
            'rewiring the house. [[slnc 700]] The previous video, Layered '
            'Architecture, ended with one honest problem. [[slnc 300]] '
            'Its use case still had to name its storage class. [[slnc '
            '300]] This video fixes exactly that, and proves it twice. '
            '[[slnc 400]] By the end, you will have one simple test for '
            'telling a port from an adapter: who is allowed to name whom?'
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
            "The core needs: a catalogue, a payment gateway,",
            "somewhere to store the order, and a way to notify.",
        ],
        narration=(
            'Here is the job. [[slnc 300]] It is the same order as every '
            'project in this series. [[slnc 300]] A customer called Ada '
            'Okafor buys an espresso machine, a coffee grinder, and two '
            'bags of coffee beans, for three hundred and eighty-two '
            'pounds fifty. [[slnc 500]] The steps are the same too. '
            '[[slnc 300]] Check the stock, take the payment, store the '
            'order, and notify the customer. [[slnc 500]] What changes is '
            'how much the core knows about how those steps happen. [[slnc '
            '400]] The core needs four things: a catalogue, a payment '
            'gateway, somewhere to store orders, and a way to notify. '
            '[[slnc 300]] Each one is an interface, and the core writes '
            'all four itself.'
        ),
    ),
    dict(
        key="03-naive",
        kind="code",
        title="The Naive Version",
        body="""public class NaivePlaceOrderService {

    private final InMemoryOrderStore orders;
    private final InMemoryPaymentGateway payments;
    private final InMemoryProductCatalog catalog;
    // three ADAPTER types, named directly.
    // swap one, and this class must be edited.
}""",
        narration=(
            "Let's start with the naive version. [[slnc 300]] It is the "
            'use case from the previous project, copied honestly. [[slnc '
            '500]] Its fields are three concrete classes. [[slnc 300]] An '
            'in-memory order store. [[slnc 200]] An in-memory payment '
            'gateway. [[slnc 200]] And an in-memory product catalogue. '
            '[[slnc 300]] Not interfaces. [[slnc 200]] The real classes '
            'that do the work. [[slnc 500]] Does it work? [[slnc 200]] '
            'Yes, it places the order correctly. [[slnc 400]] But two '
            'problems follow. [[slnc 300]] One. [[slnc 200]] You cannot '
            'test this class without building all three of those classes '
            'first. [[slnc 300]] Two. [[slnc 200]] If any of them is '
            'replaced, this file must be edited, even though its logic '
            'did not change.'
        ),
    ),
    dict(
        key="04-ports",
        kind="bullets",
        title="Ports, Declared By The Core",
        body=[
            "OrderStore, PaymentGateway,",
            "ProductCatalog, Notifier",
            "",
            "    all four declared INSIDE core.port --",
            "    in the core's own words, not the adapter's.",
            "",
            "An adapter implements a port, or calls through one.",
            "The core never names an adapter. Either direction.",
        ],
        narration=(
            'Here is the fix, and it is one single move. [[slnc 500]] The '
            'core declares four interfaces. [[slnc 300]] Order Store, '
            'Payment Gateway, Product Catalog, and Notifier. [[slnc 300]] '
            'All four live inside the core, in a package called core dot '
            'port. [[slnc 300]] Not in the adapter package. [[slnc 600]] '
            'Outside the core, there are two kinds of adapter. [[slnc '
            '400]] A driven adapter implements a port. [[slnc 300]] The '
            'core calls it, for example, to store an order. [[slnc 400]] '
            'A driving adapter calls into the core. [[slnc 300]] For '
            'example, a web request that asks the core to place an order. '
            '[[slnc 600]] And here is the rule. [[slnc 300]] The core '
            'never names an adapter. [[slnc 300]] Not one it calls, and '
            'not one that calls it. [[slnc 500]] So if you are unsure '
            'whether something is a port or an adapter, ask one question. '
            '[[slnc 300]] Who names whom?'
        ),
    ),
    dict(
        key="05-one-move",
        kind="quote",
        title="One Move From The Project Before It",
        body=[
            "Layered: the interface lived in infrastructure,",
            "the bottom layer. The use case reached DOWN.",
            "",
            "Hexagonal: the interface lives in the core.",
            "The adapter reaches UP to implement it.",
            "",
            "Same three methods on the interface. Only the",
            "package it lives in changed -- and the direction",
            "of the import with it.",
        ],
        narration=(
            "This move is smaller than it sounds, so let's be precise. "
            '[[slnc 500]] In the layered project, the storage interface '
            'lived in the bottom layer, called infrastructure. [[slnc '
            '300]] The use case, above it, reached down to use it. [[slnc '
            '300]] Layering allows that. [[slnc 500]] Here, the very same '
            'interface, with the same three methods, lives inside the '
            'core instead. [[slnc 300]] And the storage class, outside, '
            'reaches in to implement it. [[slnc 600]] So the interface '
            'itself did not change at all. [[slnc 300]] Only the package '
            'it lives in changed. [[slnc 300]] And with it, the direction '
            'the dependency points. [[slnc 500]] That is the whole '
            'distance between the previous project and this one.'
        ),
    ),
    dict(
        key="06-driven-http",
        kind="console",
        title="The Core, Driven By HTTP",
        body="""TWO. The real core, driven by HTTP.
  {"status":201,"orderId":"ord-1001",
   "total":"£382.50"}
  the core has two imports: core.domain
  and core.port.
  it does not know HTTP, or any adapter, exists.""",
        narration=(
            "Let's watch the real core run. [[slnc 400]] A pretend web "
            'request arrives at an adapter. [[slnc 300]] The adapter '
            'calls one method on the core. [[slnc 500]] The core checks '
            'stock through the catalogue port. [[slnc 300]] It takes '
            'payment through the payment port. [[slnc 300]] It saves the '
            'order through the storage port. [[slnc 300]] And it notifies '
            'the customer through the notifier port. [[slnc 400]] The '
            'order is created, with status two hundred and one, for three '
            'hundred and eighty-two pounds fifty. [[slnc 500]] Now think '
            "about the core's use case class. [[slnc 300]] It imports "
            'from only two places: the domain, and the port package. '
            '[[slnc 300]] Not one adapter. [[slnc 400]] It truly does not '
            'know that the web, or any particular storage, exists.'
        ),
    ),
    dict(
        key="07-driving-matters",
        kind="bullets",
        title="The Half Most Treatments Skip",
        body=[
            "Hexagonal is usually taught as being about databases.",
            "",
            "    swap the driven side -- storage -- and the",
            "    core does not change. Good. Half the claim.",
            "",
            "The other half: who calls IN.",
            "",
            "    the same core, driven from somewhere",
            "    completely different. No change either.",
        ],
        narration=(
            'Many explanations stop here. [[slnc 300]] They show that '
            'storage can be swapped, and call it done. [[slnc 400]] That '
            'is only half the story. [[slnc 500]] Hexagonal architecture '
            'is often taught as being all about databases. [[slnc 300]] '
            'Swap the storage, and the core does not change. [[slnc 300]] '
            'That is true. [[slnc 500]] The other half is about who calls '
            'into the core. [[slnc 300]] If the core can really be called '
            'from anywhere, we should prove it, by calling it from '
            'somewhere new. [[slnc 500]] So this project does both. '
            '[[slnc 300]] It swaps the storage underneath the core. '
            '[[slnc 300]] And it drives the same core from a completely '
            'different caller.'
        ),
    ),
    dict(
        key="08-driving-cli",
        kind="console",
        title="The Same Core, Driven By A CLI Instead",
        body="""FOUR. The driving side swapped — a CLI calls in.
  $ OK  ord-1001  £382.50

  the same PlaceOrderService instance shape,
  called from a shape as different from
  HTTP as this project has.""",
        narration=(
            'Here is the proof. [[slnc 400]] Instead of a web request, a '
            'pretend command line calls the core. [[slnc 300]] It is just '
            'one line of text, read by hand. [[slnc 400]] It calls '
            'exactly the same use case class that the web adapter called. '
            '[[slnc 500]] The result is the same order, with the same '
            'total. [[slnc 400]] And the use case class was not touched. '
            '[[slnc 300]] It takes the same four ports either way. [[slnc '
            '600]] Here is the lesson. [[slnc 300]] If a core has only '
            'ever been called one way, it has not proven it is '
            'independent of its callers. [[slnc 300]] It has only proven '
            'it works with the first caller someone wrote.'
        ),
    ),
    dict(
        key="09-rule-as-test",
        kind="code",
        title="The Rule, Written Where A Build Can Read It",
        body="""ArchRule rule = noClasses()
    .that().resideInAPackage(CORE)
    .should().dependOnClassesThat()
        .resideInAPackage(ADAPTER);

rule.check(everything);
// covers BOTH driven and driving
// adapters in one sentence.""",
        narration=(
            'All of this fits in one rule, written as a test with a '
            'library called ArchUnit. [[slnc 500]] No class in the core '
            'package may depend on any class in the adapter package. '
            '[[slnc 500]] That one rule catches two mistakes. [[slnc '
            '300]] The core naming an adapter it calls. [[slnc 300]] And '
            'the core calling back into an adapter that called it. [[slnc '
            '500]] The test runs with every other test in the build. '
            '[[slnc 400]] And a second test points the same rule at the '
            'naive version, on purpose, to prove the rule can fail.'
        ),
    ),
    dict(
        key="10-red",
        kind="console",
        title="Watching It Go Red",
        body="""Architecture Violation [Priority: MEDIUM] -
  Rule 'no classes that reside in a package
  'core..' should depend on classes that
  reside in a package 'adapter..'' was
  violated (1 time):

Class <...naive.core.NaivePlaceOrderService>
  depends on class
  <...adapter.persistence.InMemoryOrderStore>""",
        narration=(
            'So what does a failure sound like? [[slnc 400]] The build '
            'reports an architecture violation. [[slnc 300]] It says the '
            'rule, no core class may depend on an adapter, was broken '
            'once. [[slnc 300]] Then it names the naive use case class, '
            'and the in-memory order store it reached for. [[slnc 500]] A '
            'promise on a whiteboard is forgotten within a month. [[slnc '
            '300]] This message fails the build, by name, in under a '
            'second.'
        ),
    ),
    dict(
        key="11-forced-change",
        kind="console",
        title="The Forced Change, Both Halves At Once",
        body="""FORCED CHANGE: swap storage, AND swap
  who calls in
  a map  ->  an append-only log  (driven)
  HTTP   ->  a command line      (driving)

  files added     : 2
  files modified  : 1 (composition root)
  lines changed   : 4
  classes in the core : 14
  of those, never opened : 14""",
        narration=(
            'Now, the big change, with both halves at once. [[slnc 500]] '
            'On one side, storage changes from a simple map to an '
            'append-only log. [[slnc 400]] On the other side, the caller '
            'changes from a web request to a command line. [[slnc 500]] '
            "Let's count what changed, from the real files. [[slnc 300]] "
            'Two files were added. [[slnc 300]] One file was modified: '
            'the main setup code, and only four lines of it. [[slnc 500]] '
            'The core is fourteen classes. [[slnc 300]] Not one of them '
            'was opened, for either change. [[slnc 500]] Two swaps, on '
            'opposite sides of the core, and zero core classes touched.'
        ),
    ),
    dict(
        key="12-bill",
        kind="bullets",
        title="The Bill",
        body=[
            "Interfaces for one implementation.",
            "    Notifier has exactly one adapter. That is",
            "    ceremony, in the name of the shape.",
            "",
            "Mapping.",
            "    Every driving adapter translates its own",
            "    shape into the core's, and back. Real work.",
        ],
        narration=(
            "Every pattern has a cost, so let's name this one honestly. "
            '[[slnc 500]] First, interfaces for things that have only one '
            'implementation. [[slnc 300]] The Notifier has exactly one '
            'adapter in this project. [[slnc 300]] Writing an interface '
            'for a class you will never swap is ceremony. [[slnc 300]] '
            'This project has some of that, to show the shape clearly. '
            '[[slnc 500]] Second, translation. [[slnc 300]] Every driving '
            'adapter must translate its own input, like a web body or a '
            'line of text, into what the core wants. [[slnc 300]] And '
            'then translate the answer back. [[slnc 300]] That is real '
            'code, for every adapter.'
        ),
    ),
    dict(
        key="13-too-much",
        kind="bullets",
        title="When This Is Too Much",
        body=[
            "Worth it: a core that genuinely needs more",
            "than one caller, or more than one store.",
            "",
            "Not worth it: an application that will only",
            "ever have one database and one way in.",
            "",
            "Ask honestly: is either swap ever going",
            "to actually happen?",
        ],
        narration=(
            'So, is this worth it for an application with one database '
            'and one way in? [[slnc 500]] Often, no. [[slnc 300]] Four '
            'interfaces, each with one implementation that will never '
            'change, is extra complexity with nothing behind it. [[slnc '
            '500]] It becomes worth it when the core truly needs more '
            'than one caller. [[slnc 300]] Or more than one store. [[slnc '
            '300]] Or must be tested before any real infrastructure '
            'exists. [[slnc 500]] So ask yourself honestly. [[slnc 300]] '
            'Will either swap ever really happen? [[slnc 300]] Or are you '
            'building for a change that is never coming?'
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try writing a third driving",
            "adapter of your own, and confirm PlaceOrderService.java",
            "needs zero lines changed to accept it.",
        ],
        narration=(
            "That's Hexagonal Architecture. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Hexagonal '
            'architecture is not about databases, it is about who is '
            'allowed to name whom. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 300]] It runs offline, with '
            'nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Write a '
            'third driving adapter, such as a console menu or a scheduled '
            'job. [[slnc 300]] Then check that the Place Order Service '
            'class needs zero lines changed to accept it. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
