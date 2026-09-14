"""Scene definitions for the API Gateway teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the analogy is spoken in full before any class
name, and the code slides are described in words rather than read out as
syntax. The slides illustrate the narration; they never carry it.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="API Gateway",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the API Gateway pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. An API gateway "
            "means putting one service in front of all the others, so that a "
            "client makes a single call instead of five and only has to know one "
            "address. The gateway takes that one request, asks whichever services "
            "it needs, joins their answers together, and sends back one reply. "
            "[[slnc 350]] That's the idea in a sentence. The rest of the video "
            "does it properly, by building a real working Java project: the "
            "product page of an online shop, which is made out of four different "
            "services' worth of information. [[slnc 250]] By the end you'll know "
            "why one call beats five even when five calls work perfectly, what a "
            "gateway is allowed to do and the one thing it must never start "
            "doing, and how deciding in advance which services matter is what "
            "keeps a shop selling on the day one of them stops answering."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The shop's mobile app shows one product page.",
            "",
            "That page is made of four services' answers:",
            "",
            "    Catalog          the name and description",
            "    Pricing          the price",
            "    Inventory        in stock or not",
            "    Recommendations  customers also bought",
            "",
            "The obvious app calls all four itself.",
            "It works. Every test passes.",
        ],
        narration=(
            "So, imagine an online shop with a mobile app, and one screen in that "
            "app: the product page for an espresso machine. [[slnc 250]] To draw "
            "that page you need four different pieces of information, and in a "
            "shop built out of services, they belong to four different owners. "
            "[[slnc 300]] The name and the description come from the catalog "
            "service. The price comes from the pricing service, because prices "
            "change for reasons that have nothing to do with the product "
            "description. Whether the machine is in stock comes from the inventory "
            "service. And the row of suggestions along the bottom — customers also "
            "bought — comes from a recommendations service. [[slnc 350]] The "
            "obvious thing to write is an app that makes four calls and puts the "
            "four answers together on the screen. And I want to be fair to that "
            "design: it works. It returns the right page. Every test you would "
            "think to write for it passes. [[slnc 300]] The trouble with it is "
            "invisible in the code, and it only shows up in two places: the clock, "
            "and the day something goes wrong."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Four Calls From a Phone on a Train",
        body=[
            "Each round trip over a mobile network: about 200ms.",
            "",
            "    Catalog          0ms  ->  200ms",
            "    Pricing        200ms  ->  400ms",
            "    Inventory      400ms  ->  600ms",
            "    Recommendations 600ms ->  800ms",
            "",
            "800ms of waiting, and four access-token checks,",
            "because every service has to verify the caller.",
            "",
            "The phone also knows four addresses. Move a service,",
            "and you ship a new app — and wait for people to install it.",
        ],
        narration=(
            "Let's put numbers on it. [[slnc 250]] A round trip from a phone on a "
            "train to a data centre and back costs somewhere around two hundred "
            "milliseconds, and most of that is not the work — it is the distance, "
            "the radio, and setting up a secure connection. [[slnc 300]] Four "
            "calls, one after another, is eight hundred milliseconds of a shopper "
            "looking at a half-drawn screen. [[slnc 300]] Second cost. Every one "
            "of those four services has to satisfy itself that the caller is a "
            "signed-in shopper, so the access token is checked four times for one "
            "page. That is four copies of the same security decision, in four "
            "codebases, which is four chances for one of them to be subtly "
            "different from the others. [[slnc 350]] And the third cost is the one "
            "that bites hardest later. The app knows four addresses. So when the "
            "pricing service is split in two, or moved, or renamed, the thing that "
            "has to change is the app on the phone — and you cannot deploy a "
            "phone. You publish a new version and then wait months for people to "
            "install it, while the old version keeps calling an address you wanted "
            "to retire."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — The App Does the Joining",
        body="""public ProductPage productPage(String sku) {
    Product product = services.catalog().invoke(sku);
    Money price = services.pricing().invoke(sku);
    boolean inStock = services.inventory().invoke(sku);
    List<String> also = services.recommendations().invoke(sku);

    return new ProductPage(sku, product.name(), product.description(),
            price, inStock, also);
}
// four crossings of the slowest network in the system,
// and no line of it says which answers the page needs
// and which it could manage without.""",
        narration=(
            "The naive app in this project is called naive mobile app, and its "
            "product page method is four lines of ordinary Java. [[slnc 300]] It "
            "asks the catalog service for the product, the pricing service for the "
            "price, the inventory service for the stock flag, and the "
            "recommendations service for the suggestions. Then it builds one page "
            "object out of the four answers and returns it. [[slnc 350]] Nothing "
            "in that method is badly written. What is wrong with it is what is "
            "missing from it. [[slnc 300]] There is no line anywhere in it that "
            "says which of those four answers the page genuinely needs and which "
            "it could manage without. All four are called the same way, so all "
            "four are treated as equally important — and a method that treats them "
            "equally will fail whenever any one of them fails. [[slnc 300]] The "
            "suggestions row is now load-bearing. Nobody decided that. It is just "
            "what four calls in a row in the same try block means."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "1.  Latency adds up. 4 x 200ms on the slowest link",
            "    in the system, and that link is the phone's.",
            "",
            "2.  The token is checked four times, in four codebases.",
            "",
            "3.  The client is coupled to the service map. Move a",
            "    service and you ship an app — then wait for installs.",
            "",
            "4.  Every client repeats the joining. Web, app, till,",
            "    partner API: four copies of the same assembly code.",
            "",
            "5.  One optional service down takes the whole page.",
            "    Nobody chose that. It is what the code means.",
        ],
        narration=(
            "Let's be precise, because it is five separate costs. [[slnc 300]] "
            "One. The waiting adds up, and it adds up on the worst link in the "
            "system. Calls inside a data centre cost a few milliseconds; calls "
            "from a phone cost hundreds. Four of them is the shopper's whole "
            "patience. [[slnc 300]] Two. The token is checked four times, in four "
            "different codebases, for one page view. [[slnc 300]] Three. The "
            "client is coupled to the shape of the back end. Every time the "
            "services are reorganised, the phone app has to learn the new "
            "arrangement, and the phone app is the slowest thing in the company to "
            "change. [[slnc 300]] Four. Every kind of client repeats the same "
            "work. The web site joins those four answers, the app joins them, the "
            "in-store till joins them, and a partner's integration joins them. "
            "Four copies of one piece of assembly logic, drifting apart. [[slnc "
            "350]] And five, which is the expensive one. When the recommendations "
            "service stops answering, the whole product page is lost. The name "
            "arrived. The price arrived. The stock flag arrived. All three are "
            "thrown away, along with the error, because a feature nobody would "
            "miss did not answer. The shopper wanted to know what an espresso "
            "machine costs, and now they cannot find out."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The API Gateway Pattern",
        body=[
            "Implement a service that is the entry point into the",
            "system from the outside world. It handles requests by",
            "routing them to the appropriate service, and by joining",
            "the results of calls to several services.",
            "",
            "— the pattern as usually stated",
            "",
            "In plain words: one front door.",
            "The client asks once, and asks one address.",
        ],
        narration=(
            "The pattern is usually stated something like this. Implement a "
            "service that is the entry point into the system from the outside "
            "world; it handles a request by routing it to the right service, or by "
            "joining the results of calls to several services. [[slnc 350]] In "
            "plain words: one front door. [[slnc 300]] The client asks once, and it "
            "asks one address. Behind that door, the gateway does whatever asking "
            "around is necessary and comes back with one answer, already in the "
            "shape the client wanted to display. [[slnc 300]] Notice which "
            "problems that one sentence solves. One crossing of the slow network "
            "instead of four. One place to check the access token. One address for "
            "the client to know. And one place where somebody can decide what "
            "happens when a service does not answer. [[slnc 300]] That last one is "
            "not in the definition, and it is the half of this pattern that earns "
            "its keep."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "A hotel reception desk.",
            "",
            "You do not keep phone numbers for housekeeping,",
            "the restaurant and the concierge. You ring reception.",
            "",
            "  One number to remember.",
            "  It does not change when the hotel reorganises.",
            "  Reception checks who you are, once.",
            "  'Towels and a table at eight' is one call, not two.",
            "",
            "And reception does not decide the room rate.",
            "The moment it does, there are two prices for one room.",
        ],
        narration=(
            "The analogy to hold on to is a hotel reception desk. [[slnc 300]] "
            "When you are staying in a hotel and you want fresh towels and a table "
            "in the restaurant at eight, you do not keep a separate phone number "
            "for housekeeping and another one for the restaurant. You ring "
            "reception, and reception deals with whoever needs dealing with. "
            "[[slnc 350]] Look at everything that gets you. One number to "
            "remember. That number does not change when the hotel reorganises its "
            "departments, because reception is the thing that absorbs the "
            "reorganisation. Reception establishes who you are once, from your room "
            "number, rather than every department asking you separately. And your "
            "one request becomes several internal errands that you never see. "
            "[[slnc 350]] Now here is the part of the analogy that matters most, "
            "and it is about restraint. Reception does not decide the room rate. "
            "Reception does not decide whether the kitchen can do a substitution. "
            "The moment a receptionist starts making those decisions, the hotel has "
            "two policies for one question, and the answer you get depends on who "
            "you happened to ask. [[slnc 300]] Keep that sentence. We will come "
            "back to it, because it is the single most common way this pattern is "
            "ruined in real systems."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So, the pieces. [[slnc 250]] At the outside edge there is the client: "
            "the mobile app. It makes one call, over the slow network, and it knows "
            "one address. In the project that class is called mobile app, and it "
            "counts its own remote calls, because the number one is the first thing "
            "worth proving. [[slnc 300]] In the middle sits the gateway itself, the "
            "class called product page gateway. It is the only thing in the system "
            "that knows the product page is made of four parts. [[slnc 300]] "
            "Behind it, on the fast internal network, are the four services: "
            "catalog, pricing, inventory and recommendations. Each one owns its own "
            "data and knows nothing about the page. Beside them is the "
            "authentication service, which the gateway consults once per request. "
            "[[slnc 350]] And there is one more piece worth naming, because it does "
            "not look like a piece: the decision, taken in advance, that "
            "recommendations is optional and the other three are not. That is not a "
            "class. It is a judgement about the product, written down as the one "
            "catch block in the gateway. [[slnc 300]] Finally, kept deliberately "
            "beside the pattern rather than inside it, is the naive mobile app — "
            "the version that calls all four services itself. It stays in the "
            "project so the comparison is something you can run rather than "
            "something I assert."
        ),
    ),
    dict(
        key="09-gateway-code",
        kind="code",
        title="The Gateway — and the One Catch Block",
        body="""public ProductPage productPage(String token, String sku) {
    Customer customer = auth.check(token);          // once, at the edge

    Product product = services.catalog().invoke(sku);
    Money price = services.pricing().invoke(sku);
    boolean inStock = services.inventory().invoke(sku);
    List<String> also = recommendationsOrNone(sku);  // may be empty

    return new ProductPage(sku, product.name(), product.description(),
            price, inStock, also);
}

private List<String> recommendationsOrNone(String sku) {
    try {
        return services.recommendations().invoke(sku);
    } catch (ServiceUnavailableException e) {
        log.note("Gateway", "DEGRADED", "page served without suggestions");
        return List.of();                            // a page, minus a row
    }
}""",
        narration=(
            "The gateway class is short, and it does four things. [[slnc 300]] "
            "First, it checks the access token once, at the edge, and gets back a "
            "customer. Nothing behind it has to ask again. [[slnc 300]] Second, it "
            "calls the services it needs — but over the internal network, where a "
            "call costs about ten milliseconds rather than two hundred. [[slnc "
            "300]] Third, it returns a single object shaped the way the page wants "
            "to be drawn, so the app never learns four response formats. [[slnc "
            "350]] And fourth is the interesting one. There is exactly one try and "
            "catch in this class, and it is wrapped around exactly one call: the "
            "recommendations call. If that service does not answer, the catch block "
            "writes a line into the timeline saying the page is being served "
            "degraded, and returns an empty list of suggestions. [[slnc 300]] Now "
            "ask why that catch is not around all four calls, because the answer is "
            "the whole pattern. Losing the suggestions costs the shopper nothing. "
            "Losing the price would mean showing a product page with no price on "
            "it, which is worse than showing an honest error — so a pricing failure "
            "is allowed to travel all the way out to the client. [[slnc 350]] And "
            "then the restraint. This class does not price anything. It does not "
            "apply a discount, it does not decide whether a product may be sold, it "
            "does not adjust anything it is given. It joins and it forwards. A "
            "gateway that starts making business decisions is a service that owns "
            "no data and makes decisions about everybody else's, and it quietly "
            "becomes the hardest thing in the system to change. That is the "
            "receptionist deciding the room rate."
        ),
    ),
    dict(
        key="10-timeline",
        kind="console",
        title="The Same Outage, Both Ways",
        body="""3. Recommendations is down, and there is no gateway
      0ms ->   200ms  Catalog          OK        Barista Pro Espresso Machine
    200ms ->   400ms  Pricing          OK        £449.99
    400ms ->   600ms  Inventory        OK        true
    600ms ->   800ms  Recommendations  FAILED    no answer
  no page: Recommendations did not answer
  the name, the price and the stock all arrived, and were thrown away.

4. Recommendations is down, and there is a gateway
      0ms ->   240ms  Gateway          OK        Barista Pro ... £449.99 ...
    100ms ->   100ms  Gateway          AUTH      one token check for CUST-001
    100ms ->   110ms  Catalog          OK        Barista Pro Espresso Machine
    110ms ->   120ms  Pricing          OK        £449.99
    120ms ->   130ms  Inventory        OK        true
    130ms ->   140ms  Recommendations  FAILED    no answer
    140ms ->   140ms  Gateway          DEGRADED  page served without suggestions
  page: Barista Pro Espresso Machine  £449.99  in stock  0 suggestions""",
        narration=(
            "Now the same outage, twice, as a timeline — because with these "
            "patterns the answer alone tells you nothing, and the order of events "
            "tells you everything. [[slnc 350]] Without a gateway. At zero "
            "milliseconds the app asks the catalog service, and two hundred "
            "milliseconds later the name arrives. Then the price, at four hundred. "
            "Then the stock flag, at six hundred. Then, at eight hundred "
            "milliseconds, the recommendations service fails to answer, and the "
            "exception comes out of the method. [[slnc 300]] Everything that "
            "arrived is discarded with it. Three correct answers, thrown away "
            "because the fourth was missing, and eight hundred milliseconds spent "
            "to end up with nothing. [[slnc 350]] With a gateway. The token is "
            "checked once, at a hundred milliseconds. The catalog answers at a "
            "hundred and ten, pricing at a hundred and twenty, inventory at a "
            "hundred and thirty — those are internal calls, so they are cheap. At a "
            "hundred and forty the recommendations service fails, exactly as "
            "before. [[slnc 300]] And the next line in the timeline is the gateway "
            "writing the word degraded, and serving the page anyway. The shopper "
            "gets the name, the price, the stock and no suggestions, in two hundred "
            "and forty milliseconds. [[slnc 300]] Nobody tells them anything is "
            "wrong, because from where they are standing, nothing is."
        ),
    ),
    dict(
        key="11-proof",
        kind="code",
        title="The Tests — Asserting the Cost, Not the Page",
        body="""@Test void thePhoneMakesOneCall() {
    assertEquals(1, app.remoteCalls());          // naive app: 4
}

@Test void theTokenIsCheckedOnce() {
    assertEquals(1, auth.checks());              // naive app: 4
}

@Test void theGatewayIsThreeTimesFaster() {
    assertEquals(240, gatewayClock.elapsedMillis());
    assertEquals(800, naiveClock.elapsedMillis());
}

@Test void theGatewayPublishesPricingsAnswer() {
    assertEquals(pricing.priceOf(SKU), page.price());   // no logic here
}

@Test void theNaiveAppLosesThePage() {               // NAIVE - passes
    assertThrows(ServiceUnavailableException.class,
            () -> naiveApp.productPage(SKU));        // pinned on purpose""",
        narration=(
            "Twenty five tests, and the choice of what they assert is the point. "
            "[[slnc 300]] No test in this project asserts that the product page is "
            "correct. Both versions return the same page, so a test like that would "
            "pass on the naive version too, and prove nothing. [[slnc 350]] Every "
            "test asserts something only the gateway gives you. That the phone "
            "makes one remote call, where the naive app makes four. That the token "
            "is checked once, where the naive app checks it four times. That the "
            "page arrives in two hundred and forty milliseconds of simulated time "
            "against eight hundred — and because the clock is simulated, that is an "
            "exact number rather than a measurement that varies with the machine. "
            "[[slnc 350]] There is one test whose only job is to stop a future "
            "change. It asserts that the price on the page is the pricing service's "
            "answer, unmodified. The day somebody adds a discount inside the "
            "gateway, that test goes red and asks them to put it somewhere that "
            "owns pricing. [[slnc 300]] And one test asserts a failure, on purpose: "
            "the naive app losing the whole page when the suggestions service is "
            "down. It passes. Being broken is that class's entire job, and the cost "
            "of its design should be something the build states out loud rather "
            "than something a README claims."
        ),
    ),
    dict(
        key="12-output",
        kind="console",
        title="Running It — Five Acts",
        body="""$ ./gradlew run

1. No gateway: the app calls all four services itself
  four round trips, 4 token checks, shopper waited 800ms

2. With a gateway: the app makes one call
  1 round trip, 1 token check, shopper waited 240ms

3. Recommendations is down, and there is no gateway
  no page: Recommendations did not answer

4. Recommendations is down, and there is a gateway
  page: ... £449.99  in stock  0 suggestions     degraded: true

5. Catalog is down: the gateway refuses instead of degrading
    100ms ->   100ms  Gateway   AUTH      one token check
    100ms ->   110ms  Catalog   FAILED    no answer
  no page: Catalog did not answer
  the shopper is told, in 110ms, that the page cannot be shown.""",
        narration=(
            "Running the project gives five acts. [[slnc 250]] Act one: no "
            "gateway. Four round trips, four token checks, eight hundred "
            "milliseconds. [[slnc 250]] Act two: with a gateway. One round trip, "
            "one token check, two hundred and forty milliseconds, and the same "
            "page. [[slnc 300]] Act three and act four are the outage we just "
            "walked through: the whole page lost without a gateway, and the page "
            "served minus one row with it. [[slnc 350]] Act five is the one I would "
            "most like you to remember, because it is the half everybody quotes "
            "wrongly. This time the catalog service is down — the service that "
            "knows the product's own name — and the gateway does not degrade. It "
            "refuses. The shopper is told, in a hundred and ten milliseconds, that "
            "the page cannot be shown right now. [[slnc 300]] That is correct "
            "behaviour, and it is important. A product page with no product on it "
            "is not a degraded page, it is a blank one, and pretending otherwise "
            "means shipping a screen that looks broken rather than an honest "
            "message. [[slnc 300]] So a gateway is not a machine for making "
            "failures disappear. It is the place where somebody has decided, one "
            "service at a time, whether losing that service costs a section of the "
            "page or the page itself. Recommendations costs a section. The name "
            "costs the page. Making those calls is real product work, and the "
            "pattern's value is that it gives that work somewhere to live."
        ),
    ),
    dict(
        key="13-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "One front door: one crossing, one token check,",
            "one address, and one place to decide what degrades.",
            "",
            "  Facade      one door in front of many CLASSES",
            "  Gateway     one door in front of many SERVICES,",
            "              across a network that can fail",
            "",
            "Backends for Frontends: one gateway per client kind,",
            "when the app and the till want different pages.",
        ],
        narration=(
            "So, what to take away. [[slnc 300]] An API gateway is one front door. "
            "It buys you one network crossing instead of many, one place to check "
            "the token, one address for the client to know, and — most valuable of "
            "all — one place where the question of what to do when a service does "
            "not answer has an owner. [[slnc 350]] On the comparison people always "
            "ask about: how is this different from the facade pattern? The shapes "
            "are the same. Facade puts one simple door in front of many classes, "
            "inside one program. A gateway puts one door in front of many "
            "services, across a network that loses messages and goes slow and "
            "falls over. The structure is borrowed; what is new is that every call "
            "behind the door can fail on its own, which is why the interesting code "
            "in a gateway is about which failures matter. [[slnc 350]] One "
            "variation worth knowing by name: backends for frontends. If the phone "
            "app and the in-store till want genuinely different pages, you give "
            "each of them its own gateway instead of building one gateway with a "
            "flag in it. Same pattern, one per kind of client."
        ),
    ),
    # The costs are a scene of their own rather than the tail of the summary.
    # Held on one slide they ran for two minutes, which is longer than any
    # single picture earns; and this half is the half a beginner most needs to
    # hear said slowly, because it is the part that decides whether they should
    # reach for the pattern at all.
    dict(
        key="14-costs",
        kind="bullets",
        title="The Costs, Honestly",
        body=[
            "It is one more service to deploy, watch and scale.",
            "",
            "Everything goes through it, so it must not be clever.",
            "If the gateway is slow, the whole shop is slow.",
            "",
            "A gateway holding business logic is the worst",
            "outcome — a bottleneck that owns no data.",
            "",
            "And you may not need one yet. One client, three",
            "services, a fast connection — three calls is fine.",
        ],
        narration=(
            "Now the honest bill, because every pattern has one. [[slnc 300]] A "
            "gateway is one more service to deploy, monitor, scale and wake "
            "somebody up for at three in the morning. [[slnc 300]] Every single "
            "request goes through it, so it has to be simple and it has to be "
            "boring. If it gets slow, everything is slow — there is no part of the "
            "shop that routes around it. [[slnc 350]] And the worst outcome, which "
            "is also the most common one, is the gateway that gradually fills up "
            "with business rules. A discount here, a special case there, a little "
            "bit of tax logic because it was convenient — until it is a bottleneck "
            "that owns no data and that nobody dares to change. [[slnc 300]] Keep "
            "it joining and forwarding. That is the whole discipline. [[slnc 350]] "
            "And one last thing, which is knowing when not to. If the shop has one "
            "client and three services, you may not need this yet. Three calls from "
            "a web page on a fast connection is fine. [[slnc 300]] Reach for a "
            "gateway when the clients multiply, when the network is the slow part, "
            "or when you notice that nobody in the room can say what happens to the "
            "product page if one service goes down."
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that moves",
            "the try and catch around all four calls, and quietly",
            "turns an honest error into a page with no price on it.",
        ],
        narration=(
            "That's the API gateway pattern. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in the "
            "repository, and everything runs offline with nothing installed but a "
            "Java development kit — no Docker, no Spring, no message broker. "
            "[[slnc 300]] If you try one exercise, try this one. Move the try and "
            "catch in the gateway so that it wraps all four calls instead of one, "
            "run the tests, and then look at what the product page now shows when "
            "the pricing service is down. You will have turned an honest error into "
            "a page with no price on it, and no test will have complained until you "
            "look. [[slnc 300]] It takes two minutes, and it is the moment that "
            "choosing which failures matter stops being advice and becomes code. "
            "[[slnc 300]] If this helped, a like genuinely does help other people "
            "find it, and subscribe if you would like the rest of the series. "
            "[[slnc 250]] Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
