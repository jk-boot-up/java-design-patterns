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
            'Hello, and welcome. [[slnc 400]] This video explains Clean '
            'Architecture with Spring, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Clean Architecture keeps the '
            'business rules in the middle of a program, and the technical '
            'details on the outside. [[slnc 300]] Spring is a framework '
            "that builds your program's objects, and connects them for "
            'you. [[slnc 600]] Think of flat-pack furniture. [[slnc 300]] '
            'You can assemble it yourself, by hand. [[slnc 300]] Or a '
            'fitter can assemble it for you. [[slnc 300]] The furniture '
            'is the same either way. [[slnc 300]] What changes is who '
            'does the assembly, and when you find out a piece is missing. '
            '[[slnc 700]] That is this video. [[slnc 300]] We take the '
            'online shop from the Clean Architecture video, unchanged, '
            'and let Spring assemble it instead of a person. [[slnc 400]] '
            'If you have not seen that video, watch it first. [[slnc '
            '400]] Here, we prove one thing. [[slnc 300]] Wiring by hand '
            'fails while you are still typing. [[slnc 300]] Wiring by '
            'Spring fails only when the program starts.'
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
            "Before we begin, let's be clear about what this video "
            'covers. [[slnc 400]] It covers one comparison. [[slnc 300]] '
            'A wiring mistake caught when the code compiles, against a '
            'wiring mistake caught when the program starts. [[slnc 500]] '
            'It does not teach Clean Architecture again. [[slnc 300]] The '
            'earlier video does that completely. [[slnc 300]] And it does '
            'not teach Spring from the very beginning. [[slnc 300]] That '
            'is a separate video. [[slnc 400]] Everything that follows '
            'serves that one comparison.'
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
            'So, what does Spring actually do? [[slnc 400]] Spring builds '
            "your program's objects for you, and connects them. [[slnc "
            '300]] You no longer write every "new" call yourself. [[slnc '
            '500]] At its centre is something called the application '
            'context. [[slnc 300]] Think of it as a workshop with a list '
            'of instructions. [[slnc 300]] In this project, the '
            'instructions are one class, with one method for each object '
            'to build. [[slnc 400]] The context builds each object. '
            '[[slnc 300]] Then it hands each one to whichever other '
            'object asked for that type. [[slnc 500]] This is called '
            'dependency injection. [[slnc 300]] If you have ever marked a '
            'class with the at Service or at Autowired annotation, you '
            'have already used it.'
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
            'A practical note, if you want to run this yourself. [[slnc '
            '400]] You do not install anything by hand. [[slnc 300]] The '
            'Gradle wrapper downloads everything the first time you '
            'build. [[slnc 500]] The version is Spring Boot four point '
            'one point one. [[slnc 300]] That was the newest full release '
            'when this was built. [[slnc 300]] Early preview releases are '
            'not used. [[slnc 500]] And only one Spring library is used: '
            'the core starter. [[slnc 300]] There is no web library and '
            'no database library, because this project is not a web '
            'application.'
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
            'Here is the heart of the video. [[slnc 500]] In the '
            'hand-wired version, one line creates the use case. [[slnc '
            '300]] It calls the constructor, and passes four things: the '
            'product store, the order store, the payment gateway, and the '
            'notification gateway. [[slnc 500]] In the Spring version, '
            'the same constructor is called, with the same four things. '
            '[[slnc 300]] The only difference is that the call sits '
            'inside a method marked with the at Bean annotation. [[slnc '
            '500]] So what really changed? [[slnc 300]] Who makes the '
            'call, and when. [[slnc 400]] By hand, the main method makes '
            'the call, as the program starts. [[slnc 300]] With Spring, '
            'the container makes the call, once. [[slnc 300]] It matches '
            'the four parameter types to the other bean methods, in '
            'whatever order works. [[slnc 500]] So remember this. [[slnc '
            "300]] Spring's annotations are not magic. [[slnc 300]] They "
            'are those same twenty lines of wiring, found and called by '
            'the container, instead of typed by a person.'
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
            "Let's run it, and list what Spring builds. [[slnc 400]] "
            'Seven objects, which Spring calls beans. [[slnc 300]] Four '
            'gateways. [[slnc 200]] One use case. [[slnc 200]] And two '
            'controllers. [[slnc 500]] Each of those seven is exactly the '
            'same class the hand-wired project built. [[slnc 300]] '
            'Connected to the same partners. [[slnc 400]] The program '
            'itself has not changed at all. [[slnc 300]] Only the one '
            'assembling it has.'
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
            'Next, a quick check. [[slnc 300]] The earlier video added a '
            'new way in, and a new place to store orders. [[slnc 400]] '
            'Does Spring make that change more expensive? [[slnc 300]] '
            'No. [[slnc 300]] It costs one more bean method, wired just '
            'like the others. [[slnc 300]] The imported order still '
            'arrives, for two hundred and forty-nine pounds. [[slnc 300]] '
            'Using a container did not change that cost.'
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
            'Now, the comparison, in two parts. [[slnc 500]] Part one: '
            'the hand-wired version. [[slnc 300]] Remove one argument '
            'from the constructor call. [[slnc 300]] Say, the '
            'notification gateway. [[slnc 500]] What happens? [[slnc '
            '300]] The program does not start and then misbehave. [[slnc '
            '300]] It does not compile at all. [[slnc 400]] Your editor '
            'warns you straight away, before you even save the file. '
            '[[slnc 300]] The compiler catches the mistake before the '
            'program can ever run.'
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
            'Part two: the Spring version. [[slnc 400]] This time, delete '
            'the bean method that builds the notification gateway. [[slnc '
            '500]] The code compiles. [[slnc 300]] The build succeeds, '
            'with no warnings at all. [[slnc 500]] The mistake stays '
            'hidden until the program starts. [[slnc 300]] Then Spring '
            'tries to build the use case. [[slnc 300]] It needs a '
            'notification gateway, and finds none. [[slnc 400]] So it '
            'stops, with a message: startup failed, no qualifying bean of '
            'type Notification Gateway. [[slnc 500]] Not while typing. '
            '[[slnc 300]] At startup, a few seconds into a run that '
            'looked completely normal.'
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
            "Why can't Spring see this coming? [[slnc 400]] A compiler "
            'checks the types at a call it can see, in the source code, '
            'while you type. [[slnc 500]] A container checks the types '
            'against objects it has not built yet. [[slnc 300]] And it '
            'only checks when something asks for them. [[slnc 500]] Think '
            'of a hole in a floor, covered by a rug. [[slnc 300]] Nothing '
            'seems wrong, until someone steps on that exact spot. [[slnc '
            '400]] By then, the program has already started, printed its '
            'banner, and looked perfectly healthy.'
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
            "Every convenience has a cost, so let's name it honestly. "
            '[[slnc 500]] One. [[slnc 200]] Anyone running this project '
            'now needs to know what Spring is. [[slnc 300]] The entities '
            'and use cases need nothing new, but the setup and the '
            'starting point do. [[slnc 500]] Two. [[slnc 200]] Startup is '
            'slower. [[slnc 300]] Spring must build the context, call '
            'every bean method, and connect everything. [[slnc 300]] The '
            'hand-wired version never pays for that. [[slnc 500]] Three. '
            '[[slnc 200]] A wiring mistake shows up when the program '
            'runs, not when it compiles. [[slnc 300]] You just heard '
            'exactly that happen.'
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
            'So when is a container worth it? [[slnc 400]] When a real '
            'application has so many objects that wiring them all in one '
            'method becomes hard to read. [[slnc 300]] Honestly, that is '
            'most real applications beyond a handful of classes. [[slnc '
            '500]] It is not worth it for learning the architecture. '
            '[[slnc 300]] That lesson is clearer with no framework in the '
            'way. [[slnc 300]] That is exactly why Clean Architecture has '
            'its own video, built first.'
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
            'One more thing, to keep this video focused. [[slnc 400]] '
            'Every entity, use case and adapter here comes from the '
            'earlier video. [[slnc 300]] None of it is taught again. '
            '[[slnc 400]] Spring in general is a separate video. [[slnc '
            '400]] And there is no web application here. [[slnc 300]] No '
            'web server, and no web library. [[slnc 300]] This is a '
            'comparison of two ways to wire a program, and nothing more.'
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
            "That's Clean Architecture with Spring. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Wiring '
            'by hand fails when you compile, and wiring by a container '
            'fails when the program starts. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Delete a different bean method from the '
            'one in this video. [[slnc 300]] Run the project, and read '
            'the error it gives. [[slnc 300]] Then check whether it says '
            'what you expected. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
