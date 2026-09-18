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
            "Hello, and welcome. This video explains Hexagonal Architecture "
            "in Java -- also called Ports and Adapters -- and it is written "
            "and presented by Jayasekhar Konduru. [[slnc 300]] Let's start "
            "with the plain definition. The core of an application defines "
            "ports -- interfaces, in its own words, for whatever it needs "
            "from the outside world. Adapters, on the outside, either "
            "implement those ports or call in through them. Every "
            "dependency between the core and the world outside it points "
            "inward, into the core, never out of it. [[slnc 350]] This is "
            "the second project in a series building the same online shop "
            "five different ways, and it picks up exactly where the "
            "previous one, Layered Architecture, left off -- that project "
            "ended by admitting one honest cost: its use case still had to "
            "name its storage class to compile. This video inverts exactly "
            "that, and then proves the inversion twice: once by swapping "
            "the storage underneath the core, and once by driving the same "
            "core from somewhere completely different. [[slnc 300]] By the "
            "end you will know the actual test to apply when you are unsure "
            "whether something is a port or an adapter -- which is simply, "
            "who is allowed to name whom."
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
            "Same order as every project in this category, placed the same "
            "way: check stock, take payment, store the order, notify the "
            "customer. Ada Okafor's three hundred and eighty-two pounds "
            "fifty. [[slnc 300]] What changes in this video is not the "
            "feature. It is what the core is allowed to know about how "
            "those four things actually happen. The core needs a "
            "catalogue, a payment gateway, somewhere to store an order, and "
            "a way to notify a customer -- four needs, stated as four "
            "interfaces, all four written by the core itself."
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
            "Here is where this project starts, and it is not a strawman -- "
            "it is the previous project's use case, honestly reproduced. "
            "[[slnc 300]] This class's fields are typed as concrete "
            "adapters: an in-memory order store, an in-memory payment "
            "gateway, an in-memory catalogue. Not interfaces the core "
            "declared -- the actual classes that do the storing and the "
            "charging. [[slnc 350]] It works. It places the order "
            "correctly. And two things follow from those field types that "
            "would not follow from an interface. You cannot unit-test this "
            "class without constructing all three adapters. And the moment "
            "any one of those three classes is replaced, this file must be "
            "opened and edited -- not because its logic changed, but "
            "because a type it named no longer exists."
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
            "So here is the fix, and it is one move, stated precisely. "
            "[[slnc 300]] Four interfaces -- a place to store orders, a way "
            "to take payment, a catalogue, a way to notify -- all four "
            "declared inside the core itself, in a package called core dot "
            "port. Not in the adapter package. Inside the core. [[slnc "
            "350]] An adapter, on the outside, either implements one of "
            "these interfaces -- that is a driven adapter, one the core "
            "calls -- or it holds a reference to the core's use case and "
            "calls into it -- that is a driving adapter, one that calls the "
            "core. [[slnc 300]] And here is the rule that makes this "
            "precise rather than a vibe. The core never names an adapter. "
            "Not a driven one it is calling, and not a driving one that "
            "might be calling it. If you are ever unsure whether something "
            "is a port or an adapter, ask exactly one question: who names "
            "whom?"
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
            "I want to be precise about how small this move actually is, "
            "because it is easy to make hexagonal architecture sound like a "
            "bigger idea than it is. [[slnc 300]] In the layered "
            "architecture project, the storage interface lived in the "
            "bottom layer, called infrastructure, and the use case above it "
            "reached down to name it. That is allowed, under layering's own "
            "rule -- each layer may depend on the one beneath it. [[slnc "
            "350]] Here, the exact same interface -- three methods, save, "
            "find, describe -- lives inside the core instead. And the "
            "adapter that used to define it now reaches up to implement it. "
            "[[slnc 300]] Read that again, because it is the whole trick. "
            "The interface did not change. Only which package it lives in "
            "changed -- and with it, which direction the import points. "
            "That is the entire distance between the project before this "
            "one and this one."
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
            "So let's watch the real core run. A simulated HTTP request "
            "arrives at an adapter, which calls one method on the core's "
            "use case. [[slnc 300]] The core checks stock through the "
            "catalogue port, charges through the payment port, saves "
            "through the storage port, notifies through the notifier port -- "
            "and every single one of those four names is a name the core "
            "chose for itself. [[slnc 300]] Open the core's use case class "
            "and count its imports. Two: the domain, and the port package. "
            "Not one adapter. It genuinely does not know that HTTP, or any "
            "particular way of storing an order, exists."
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
            "Most explanations of this pattern stop here, having shown you "
            "that storage can be swapped, and call it done. This video "
            "insists on the other half. [[slnc 300]] Hexagonal "
            "architecture is usually taught as being entirely about "
            "databases -- swap the driven side, storage, and the core does "
            "not change. That is real, and it is half the claim. [[slnc "
            "350]] The half almost everyone skips is the driving side -- "
            "who is allowed to call in. If the core can genuinely be called "
            "from anywhere, that has to be demonstrated by actually calling "
            "it from somewhere new, not merely asserted. [[slnc 300]] So "
            "this project does both, in the same act. It swaps the storage "
            "underneath the core, and it drives the very same core from a "
            "caller that shares no code at all with the first one."
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
            "Here is the proof. A simulated command line -- one string, "
            "parsed by hand -- calls the identical use case class the HTTP "
            "adapter called two acts ago. [[slnc 300]] Same order. Same "
            "total. And critically: the use case class was not touched to "
            "make this possible. Its constructor takes the same four ports "
            "either way. [[slnc 300]] This is the sentence I want you to "
            "take from this scene. A core that can only be shown accepting "
            "one kind of caller has not actually proven it is decoupled "
            "from callers -- it has proven it works with the one caller "
            "somebody happened to write first."
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
            "One sentence covers all of this. No class in the core package "
            "may depend on any class in the adapter package. [[slnc 300]] "
            "Notice that one rule catches both mistakes at once -- the core "
            "naming a driven adapter it is calling, and the core "
            "accidentally calling back into a driving adapter that called "
            "it. Either direction breaks the same rule, and this one test "
            "covers both. [[slnc 300]] It runs in gradlew test alongside "
            "everything else, and a second test widens the same rule to "
            "the naive package on purpose, to prove it is capable of "
            "failing."
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
            "Here is what the build prints. Architecture violation. And "
            "then the part that matters: it names the naive use case class, "
            "and it names the adapter it reached for. [[slnc 350]] The "
            "difference between a whiteboard promise and this message is "
            "the difference the whole category is built to teach. One of "
            "them is forgotten within a month. The other one fails a build, "
            "by name, in under a second."
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
            "So here is the bill, both halves counted together, because "
            "this project's whole claim is that both are free at once. "
            "[[slnc 300]] Storage changes from a map to an append-only log. "
            "Separately, the calling side changes from a simulated HTTP "
            "request to a simulated command line. [[slnc 350]] Counted from "
            "the real files on disk: two files added, one file modified -- "
            "the composition root, four lines total. And fourteen classes "
            "make up the entire core. Every one of them: never opened, for "
            "either change. [[slnc 300]] Two simultaneous swaps, on "
            "opposite sides of the same hexagon, and the number of core "
            "classes that had to be touched for either one is zero."
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
            "Every project in this category has to pay a bill honestly, "
            "and here is this one's. [[slnc 300]] Interfaces for things "
            "with exactly one implementation. Notifier has one adapter in "
            "this whole project. Writing an interface for a class you will "
            "never swap is ceremony, and this project has some of it, in "
            "the name of demonstrating the shape clearly. [[slnc 350]] And "
            "mapping. Every driving adapter spends real code translating "
            "its own shape -- a JSON body, a command line string -- into "
            "what the core actually wants, and translating the answer back. "
            "That cost is paid once per adapter, and it is genuinely "
            "there."
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
            "So the honest question this project must not dodge. For an "
            "application that will only ever have one database and one way "
            "of being called, is any of this worth building? [[slnc 300]] "
            "Often, no. Four interfaces, each with exactly one "
            "implementation that will never be swapped, is indirection "
            "with nothing behind it but the diagram. [[slnc 350]] It is "
            "worth it the moment a core genuinely needs more than one "
            "caller, or more than one store, or needs to be tested without "
            "any of its real infrastructure existing yet. The question "
            "worth asking honestly before reaching for this: is either "
            "swap ever actually going to happen, or am I building the "
            "seam for a change that is never coming?"
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
            "That's hexagonal architecture. [[slnc 250]] If you take one "
            "sentence away, take this one: hexagonal architecture is not "
            "about databases. It is about who is allowed to name whom. "
            "[[slnc 350]] The full source, the written notes, the diagrams "
            "and an animated walkthrough are all in the repository, running "
            "offline with nothing installed but a Java development kit. "
            "[[slnc 300]] If you try one exercise, try this. Write a third "
            "driving adapter -- a console menu, a scheduled job, anything -- "
            "and confirm that PlaceOrderService dot java needs zero lines "
            "changed to accept it. [[slnc 300]] If this helped, a like "
            "genuinely does help other people find it, and subscribe if "
            "you would like the rest of the series. [[slnc 250]] Thanks for "
            "watching, and I'll see you in the next one."
        ),
    ),
]
