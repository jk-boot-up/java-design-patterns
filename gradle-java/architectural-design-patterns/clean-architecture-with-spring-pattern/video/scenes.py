"""Scene definitions for the Clean Architecture with Spring teaching video.

Written to stand on its own with the screen off. No sentence says "as you
can see".

This project names §66, Clean Architecture, in its own opening scene, and
owns exactly one comparison rather than re-teaching an architecture already
taught completely. It is the fifth and final project in this category.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Clean Architecture with Spring",
        body=None,
        narration=(
            "Hello, and welcome. This video is about Clean Architecture "
            "with Spring, and it is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] This is the fifth and final project in "
            "a series that has built the same online shop five different "
            "ways, and it is unlike the other four in one important "
            "respect. It does not teach a new architecture. It takes the "
            "identical object graph a previous video, Clean Architecture, "
            "already built and taught -- the same entities, the same use "
            "cases, the same adapters, copied unchanged -- and has a "
            "container assemble it instead of a person. [[slnc 350]] If "
            "you have not watched that video, pause this one and watch it "
            "first. Everything here assumes you already know what a use "
            "case and a port are, and spends none of its time re-teaching "
            "them. [[slnc 300]] What this video actually owns is one "
            "comparison, proven rather than described: hand-wiring an "
            "object graph fails the moment you make a mistake, while you "
            "are still typing. Wiring the same graph with a container "
            "fails only once the program tries to run -- and by then, "
            "everything else about the program looked completely normal."
        ),
    ),
    dict(
        key="02-scope",
        kind="bullets",
        title="What This Video Owns, And What It Does Not",
        body=[
            "OWNS:",
            "    the one contrast -- compile-time wiring",
            "    failure against startup wiring failure.",
            "",
            "DOES NOT OWN:",
            "    Clean Architecture itself. Already taught,",
            "    completely, in the video this one names first.",
            "",
            "    Spring, from first principles.",
        ],
        narration=(
            "Let me be precise about scope before anything else, because "
            "a video that tries to do everything ends up teaching nothing "
            "well. [[slnc 300]] This video owns one contrast: compile-time "
            "wiring failure against startup wiring failure. [[slnc 350]] "
            "It does not own Clean Architecture itself -- that is already "
            "taught, completely, in the video this one names in its very "
            "first sentence. And it does not own Spring as a general "
            "subject. If you want dependency injection explained from "
            "first principles, that is a different, dedicated video. "
            "[[slnc 300]] Everything in the next twelve minutes is in "
            "service of that one comparison, and nothing else."
        ),
    ),
    dict(
        key="03-what-spring-is",
        kind="quote",
        title="What Spring Actually Does",
        body=[
            "Spring builds your program's objects for you,",
            "and connects them, instead of you writing",
            "the new calls yourself.",
            "",
            "At its centre: an application context, reading",
            "instructions -- one class, one method per object --",
            "and matching each one to whatever asked for it.",
        ],
        narration=(
            "Before the comparison, the plain-language definition, for "
            "anyone meeting this for the first time. [[slnc 300]] Spring "
            "builds your program's objects for you, and connects them, "
            "instead of you writing the new calls yourself. [[slnc 350]] "
            "At its centre is something called an application context -- a "
            "registry that reads a set of instructions, in this project "
            "one class with a method per object it needs to build, "
            "constructs every object those instructions describe, and "
            "wires each one into whichever other object asked for it, by "
            "type. [[slnc 300]] The everyday word for this is dependency "
            "injection, and if you have ever written a class annotated at "
            "Service or at Autowired, you have already met it."
        ),
    ),
    dict(
        key="04-install",
        kind="bullets",
        title="What This Project Installs",
        body=[
            "Nothing you fetch by hand. gradlew does it.",
            "",
            "Spring Boot 4.1.1",
            "    newest generally available release --",
            "    a milestone is not a release.",
            "",
            "spring-boot-starter only.",
            "    no web starter, no database starter.",
        ],
        narration=(
            "One practical note before the comparison, for anyone who "
            "wants to run this alongside the video. [[slnc 300]] There is "
            "nothing to install by hand -- the Gradle wrapper fetches "
            "everything on first run, the same as every other project in "
            "this repository. [[slnc 300]] The version is Spring Boot "
            "four point one point one, the newest generally available "
            "release at the time this was built -- a milestone release is "
            "not a release, and this category pins real ones only. "
            "[[slnc 300]] And the dependency is deliberately narrow: "
            "spring-boot-starter, core dependency injection, nothing "
            "else. No web starter, no database starter, because this "
            "project builds no web application."
        ),
    ),
    dict(
        key="05-recognition",
        kind="code",
        title="Recognition: @Bean Is Those Twenty Lines",
        body="""// by hand, in Clean Architecture:
new PlaceOrderInteractor(
    products, orders, payments, notifications);

// by container, here:
@Bean
public PlaceOrderInputBoundary placeOrder(
        ProductRepository products,
        OrderRepository orders,
        PaymentGateway payments,
        NotificationGateway notifications) {
    return new PlaceOrderInteractor(
        products, orders, payments, notifications);
}""",
        narration=(
            "Here is the moment this whole video exists for. Read these "
            "two side by side. [[slnc 300]] The hand-wired version: four "
            "arguments, one constructor call, written by a person, in a "
            "method that runs top to bottom. The Spring version: the "
            "identical four arguments, the identical constructor, the "
            "identical class -- wrapped in one method, marked as "
            "producing a bean. [[slnc 350]] The difference is entirely "
            "about who calls it, and when. There, a line in main, the "
            "moment the program starts. Here, Spring, once, when the "
            "context is built -- matching this method's four parameter "
            "types against other methods' return types, in whatever order "
            "satisfies them. [[slnc 300]] Say this plainly, because it is "
            "worth being able to say without a slide in front of you. At "
            "Component is not magic. It is those twenty lines, discovered "
            "and called by a container instead of typed by a person."
        ),
    ),
    dict(
        key="06-wired",
        kind="console",
        title="Seven Beans, The Same Seven Objects",
        body="""THREE. Recognition: @Bean is those twenty lines.
  startup log (abridged):
    productRepository -> InMemoryProductRepository
    orderRepository -> InMemoryOrderRepository
    paymentGateway -> InMemoryPaymentGateway
    notificationGateway -> InMemoryNotificationGateway
    placeOrderInputBoundary -> PlaceOrderInteractor
    checkoutController -> CheckoutController
    batchOrderController -> BatchOrderController""",
        narration=(
            "Run the project, and here is what actually gets built. Seven "
            "beans: four gateways, the interactor, and two controllers. "
            "[[slnc 300]] Every one of those seven names is the same "
            "class the hand-wired project's composition root already "
            "constructed, in the same order, wired to the same "
            "collaborators. Nothing about the object graph is different. "
            "Only who is holding the wrench."
        ),
    ),
    dict(
        key="07-forced-change",
        kind="console",
        title="The Forced Change Still Costs Nothing Extra",
        body="""FOUR. The forced change still costs nothing extra.
  IMPORTED ord-1002 £249.00
  BatchOrderController was already wired -- one more
  @Bean method, same as one more line of new(...).""",
        narration=(
            "Quickly, because this was already proven in the previous "
            "video and this one is not going to re-argue it. The forced "
            "change -- a new delivery mechanism, a new data source -- "
            "costs exactly as little here as it did by hand. One more "
            "bean method, wired the same way as everything else. Nothing "
            "about using a container changed that cost."
        ),
    ),
    dict(
        key="08-compile-fails",
        kind="code",
        title="Hand-Wiring Fails At Compile Time",
        body="""new PlaceOrderInteractor(
    products, orders, payments);
    // ^ missing the 4th argument.
    // this is a compile error.
    // it will not build. full stop.""",
        narration=(
            "Now the contrast, in two parts. First, the hand-wired "
            "project. Delete one argument from that constructor call -- "
            "say, the notifications collaborator. [[slnc 300]] This does "
            "not run and fail. It does not start and then misbehave. It "
            "does not compile, at all. Your editor tells you immediately, "
            "before you have even saved the file, that this call no "
            "longer matches any constructor that exists. The compiler "
            "catches the mistake before the program has any chance to "
            "run."
        ),
    ),
    dict(
        key="09-startup-fails",
        kind="console",
        title="Container Wiring Fails At Startup",
        body="""FIVE. Hand-wiring fails at compile time.
  Container wiring fails at startup.

  STARTUP FAILED: No qualifying bean of type
  'NotificationGateway' available: expected at
  least 1 bean which qualifies as autowire
  candidate.""",
        narration=(
            "Now delete the equivalent bean method instead -- "
            "notificationGateway, gone. [[slnc 300]] The file compiles. "
            "Every other bean method compiles. Gradlew build succeeds, "
            "cleanly, with no warning anywhere. [[slnc 350]] The mistake "
            "is invisible until something actually asks the context to "
            "build the interactor -- and only then does Spring discover "
            "that one of its four parameters has nothing to satisfy it, "
            "and throw. Not at compile time. At startup, seconds into what "
            "looked, right up until that message, like an entirely normal "
            "run."
        ),
    ),
    dict(
        key="10-why-invisible",
        kind="bullets",
        title="Why The Container Cannot See It Coming",
        body=[
            "A compiler checks types against a call site",
            "it can see, while you are typing.",
            "",
            "A container checks types against beans it has",
            "not built yet, and only once asked.",
            "",
            "The container will happily accept a graph",
            "with a hole in it, until something falls in.",
        ],
        narration=(
            "Here is the mechanism, stated plainly. A compiler checks "
            "types against a call site it can see, right there in the "
            "source, while you are still typing. [[slnc 300]] A container "
            "checks types against a set of beans it has not built yet, "
            "and it only performs that check once something actually asks "
            "for the result. [[slnc 350]] The container will happily "
            "accept a configuration with a hole in it. It says nothing, "
            "objects to nothing, until the one moment something falls "
            "into the hole -- and by then, the process has already "
            "started, logged its banner, and looked, to anyone watching, "
            "completely healthy."
        ),
    ),
    dict(
        key="11-bill",
        kind="bullets",
        title="The Cost, Honestly Priced",
        body=[
            "A reader now needs to know Spring to run",
            "this project at all.",
            "",
            "Startup is slower -- real work, paid once,",
            "that the hand-wired project never does.",
            "",
            "A wiring mistake surfaces at run time,",
            "not compile time.",
        ],
        narration=(
            "So here is the bill for the convenience, and it is worth "
            "pricing honestly rather than waving away. [[slnc 300]] A "
            "reader now needs to know what Spring is to run this project "
            "at all -- entities and use cases need nothing new, but the "
            "configuration and the entry point do. [[slnc 300]] Startup "
            "is slower: the context has to be built, every bean method "
            "invoked, every dependency resolved -- real work the "
            "hand-wired project never pays for. [[slnc 350]] And a wiring "
            "mistake surfaces at run time instead of compile time, which "
            "you have just watched happen. That is the entire cost of the "
            "convenience, and it is a real one."
        ),
    ),
    dict(
        key="12-when-worth-it",
        kind="bullets",
        title="When This Is Worth The Extra Dependency",
        body=[
            "Worth it: a real application, past a handful",
            "of classes, where hand-wiring stops being",
            "readable in one method.",
            "",
            "Not worth it for LEARNING the architecture.",
            "That lesson is complete with no framework",
            "in the way at all -- which is why that is a",
            "separate video from this one.",
        ],
        narration=(
            "So when does reaching for a container actually pay off? "
            "[[slnc 300]] The moment a real application has enough "
            "objects that wiring them all in one hand-written method stops "
            "being readable -- which, honestly, is most real applications "
            "past a handful of classes. [[slnc 350]] It is not worth it "
            "for learning the architecture itself. That lesson is "
            "complete, and arguably clearer, with no framework in the way "
            "at all -- which is exactly why Clean Architecture is its own "
            "video, built first, rather than a single scene inside this "
            "one."
        ),
    ),
    dict(
        key="13-what-not",
        kind="bullets",
        title="What This Project Deliberately Skips",
        body=[
            "Every entity, use case and adapter --",
            "already taught. This video re-teaches none of it.",
            "",
            "Spring from first principles -- a different,",
            "dedicated video.",
            "",
            "A web application. There is no web starter",
            "anywhere in this project.",
        ],
        narration=(
            "One more thing worth saying plainly, because it is easy for "
            "a video like this to sprawl. [[slnc 300]] Every entity, use "
            "case and adapter in this project is a file already taught, "
            "completely, in the video before this one -- nothing here "
            "re-teaches any of it. Spring, as a general subject, is a "
            "different, dedicated video, not this one. And there is no "
            "web application anywhere in this project -- no web starter, "
            "no HTTP server, because this is a wiring comparison, not a "
            "web tutorial wearing an architecture's name."
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try deleting a bean method",
            "yourself, and read the exception it produces before",
            "checking whether it matches what this video showed.",
        ],
        narration=(
            "That's Clean Architecture with Spring. [[slnc 250]] If you "
            "take one sentence away, take this one: hand-wiring fails at "
            "compile time; container wiring fails at startup. [[slnc "
            "350]] The full source, the written notes, the diagrams and "
            "an animated walkthrough are all in the repository. [[slnc "
            "300]] If you try one exercise, try this. Delete a different "
            "bean method than the one this video deleted, run the "
            "project, and read the exception it produces before checking "
            "whether it says what you expected. [[slnc 300]] If this "
            "helped, a like genuinely does help other people find it, and "
            "subscribe if you would like the rest of the series. [[slnc "
            "250]] Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
