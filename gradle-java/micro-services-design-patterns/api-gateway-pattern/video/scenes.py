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
            'Hello, and welcome. [[slnc 400]] This video explains the A P '
            'I Gateway pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An A P I gateway is one '
            'service placed in front of all the others. [[slnc 300]] So a '
            'client makes a single call, instead of five, and only needs '
            'to know one address. [[slnc 300]] The gateway asks whichever '
            'services it needs, joins their answers, and sends back one '
            'reply. [[slnc 600]] Think of a hotel reception desk. [[slnc '
            '300]] You do not phone housekeeping, the restaurant, and the '
            'concierge separately. [[slnc 300]] You ring reception, and '
            'reception deals with the rest. [[slnc 700]] In our online '
            'store, the product page is built from four different '
            'services. [[slnc 500]] By the end, you will know why one '
            'call beats four, even when four calls work perfectly. [[slnc '
            '300]] What a gateway must never start doing. [[slnc 300]] '
            'And how deciding in advance which services matter keeps the '
            'shop selling when one of them stops answering.'
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
            "Here is the scenario. [[slnc 400]] The shop's mobile app has "
            'a product page for an espresso machine. [[slnc 300]] To draw '
            'it, the app needs four pieces of information, owned by four '
            'services. [[slnc 500]] The name and description come from '
            'the catalog service. [[slnc 300]] The price comes from the '
            'pricing service. [[slnc 300]] Whether it is in stock comes '
            'from the inventory service. [[slnc 300]] And the row of '
            'suggestions, customers also bought, comes from a '
            'recommendations service. [[slnc 500]] The obvious design is '
            'an app that makes four calls, and puts the answers together. '
            '[[slnc 300]] To be fair, it works. [[slnc 300]] It shows the '
            'right page, and every test passes. [[slnc 500]] Its problems '
            'only show up on the clock, and on the day something goes '
            'wrong.'
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
            "Let's put numbers on it. [[slnc 400]] A round trip from a "
            'phone on a train to a data centre takes about two hundred '
            'milliseconds. [[slnc 300]] Most of that is distance and '
            'radio, not work. [[slnc 500]] Four calls, one after another, '
            'is eight hundred milliseconds. [[slnc 300]] Eight hundred '
            'milliseconds of a shopper staring at a half-drawn screen. '
            '[[slnc 500]] Second, each service must check that the caller '
            'is a signed-in shopper. [[slnc 300]] So the access token is '
            'checked four times, for one page, in four different '
            'codebases. [[slnc 500]] Third, the app knows four addresses. '
            '[[slnc 300]] So when a service is moved or split, the app on '
            'the phone must change. [[slnc 300]] And you cannot simply '
            'update a phone. [[slnc 300]] You release a new version, and '
            'wait months for people to install it.'
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
            "The naive app's product page method is four ordinary lines "
            'of Java. [[slnc 400]] Ask catalog for the product. [[slnc '
            '300]] Ask pricing for the price. [[slnc 300]] Ask inventory '
            'for the stock. [[slnc 300]] Ask recommendations for the '
            'suggestions. [[slnc 300]] Then build one page from the four '
            'answers. [[slnc 500]] Nothing is badly written. [[slnc 300]] '
            'What is wrong is what is missing. [[slnc 500]] There is no '
            'line saying which answers the page truly needs, and which it '
            'could live without. [[slnc 300]] All four are called the '
            'same way, so all four are treated as equally important. '
            '[[slnc 300]] So the page fails whenever any one of them '
            'fails. [[slnc 500]] The suggestions row has become '
            'essential, and nobody decided that.'
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
            'So what exactly is wrong? [[slnc 300]] Five separate costs. '
            '[[slnc 500]] One. [[slnc 200]] The waiting adds up, on the '
            "slowest link in the system: the phone's connection. [[slnc "
            '400]] Two. [[slnc 200]] The token is checked four times, in '
            'four codebases, for one page. [[slnc 400]] Three. [[slnc '
            '200]] The app is tied to the layout of the back end. [[slnc '
            '300]] Every reorganisation means changing the phone app, the '
            'slowest thing in the company to change. [[slnc 400]] Four. '
            '[[slnc 200]] Every kind of client repeats the same work. '
            '[[slnc 300]] The website, the app, and the in-store till '
            'each join the same four answers. [[slnc 400]] And five, the '
            'expensive one. [[slnc 300]] When the recommendations service '
            'stops answering, the whole product page is lost. [[slnc '
            '300]] The name, price, and stock had all arrived. [[slnc '
            '300]] And all are thrown away, because a feature nobody '
            'would miss did not answer.'
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
            'Here is the pattern, as it is usually stated. [[slnc 400]] A '
            'service that is the entry point into the system from the '
            'outside world. [[slnc 300]] It sends each request to the '
            'right service, or joins the results of several. [[slnc 500]] '
            'In plain words: one front door. [[slnc 500]] The client asks '
            'once, at one address. [[slnc 300]] Behind that door, the '
            'gateway does all the asking around. [[slnc 300]] And returns '
            'one answer, already shaped the way the client wants to show '
            'it. [[slnc 500]] That gives you one trip across the slow '
            'network, instead of four. [[slnc 300]] One place to check '
            'the token. [[slnc 300]] One address for the client to know. '
            '[[slnc 300]] And one place where someone decides what '
            'happens when a service does not answer.'
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
            'Here is the analogy to hold on to: a hotel reception desk. '
            '[[slnc 500]] You want fresh towels, and a table in the '
            'restaurant at eight. [[slnc 300]] You do not phone '
            'housekeeping and the restaurant separately. [[slnc 300]] You '
            'ring reception, and reception handles it. [[slnc 500]] One '
            'number to remember. [[slnc 300]] It does not change when the '
            'hotel reorganises its departments. [[slnc 300]] Reception '
            'checks who you are once, from your room number. [[slnc 300]] '
            'And your one request becomes several errands you never see. '
            '[[slnc 600]] Now the most important part of the analogy: '
            'restraint. [[slnc 300]] Reception does not decide the room '
            'rate. [[slnc 300]] Reception does not decide what the '
            'kitchen can cook. [[slnc 300]] The moment reception starts '
            'making those decisions, the hotel has two policies for one '
            'question. [[slnc 300]] Remember that, because it is the most '
            'common way this pattern is ruined.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'So here are the pieces. [[slnc 500]] On the outside is the '
            'client: the mobile app. [[slnc 300]] It makes one call, over '
            'the slow network, to one address. [[slnc 500]] In the middle '
            'is the gateway, called the product page gateway. [[slnc '
            '300]] It is the only thing that knows the page is built from '
            'four parts. [[slnc 500]] Behind it, on the fast internal '
            'network, are the four services: catalog, pricing, inventory, '
            'and recommendations. [[slnc 300]] Each owns its own data, '
            'and knows nothing about the page. [[slnc 300]] Beside them '
            'is the sign-in service, which the gateway asks once per '
            'request. [[slnc 500]] And one more piece, which does not '
            'look like a piece. [[slnc 300]] The decision, made in '
            'advance, that recommendations is optional, and the other '
            'three are not.'
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
            'The gateway class is short, and it does four things. [[slnc '
            '500]] First, it checks the access token once, at the front '
            'door. [[slnc 300]] Nothing behind it needs to ask again. '
            '[[slnc 400]] Second, it calls the services it needs, over '
            'the fast internal network. [[slnc 300]] About ten '
            'milliseconds each, instead of two hundred. [[slnc 400]] '
            'Third, it returns one object, shaped exactly as the page '
            'wants it. [[slnc 400]] Fourth, and most interesting, there '
            'is exactly one try and catch in the class. [[slnc 300]] It '
            'is wrapped around one call only: recommendations. [[slnc '
            '300]] If that service does not answer, the page is served '
            'without suggestions. [[slnc 600]] Why not wrap all four '
            'calls? [[slnc 300]] Because losing the suggestions costs the '
            'shopper nothing. [[slnc 300]] But losing the price would '
            'mean a product page with no price. [[slnc 300]] That is '
            'worse than an honest error. [[slnc 600]] And notice the '
            'restraint. [[slnc 300]] The gateway does not change prices, '
            'apply discounts, or decide what may be sold. [[slnc 300]] It '
            'only joins, and forwards.'
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
            'Now the same outage, twice, as a timeline. [[slnc 500]] '
            'Without a gateway. [[slnc 300]] The name arrives at two '
            'hundred milliseconds. [[slnc 300]] The price at four '
            'hundred. [[slnc 300]] The stock at six hundred. [[slnc 300]] '
            'Then, at eight hundred, the recommendations service fails to '
            'answer. [[slnc 500]] Everything that arrived is thrown away. '
            '[[slnc 300]] Three correct answers lost, because the fourth '
            'was missing. [[slnc 300]] Eight hundred milliseconds, to end '
            'up with nothing. [[slnc 600]] With a gateway. [[slnc 300]] '
            'The token is checked at one hundred milliseconds. [[slnc '
            '300]] Catalog, pricing, and inventory answer quickly, over '
            'the internal network. [[slnc 300]] At one hundred and forty, '
            'recommendations fails, just as before. [[slnc 500]] And the '
            'gateway serves the page anyway. [[slnc 300]] Name, price, '
            'and stock, with no suggestions, in two hundred and forty '
            "milliseconds. [[slnc 300]] From the shopper's point of view, "
            'nothing is wrong.'
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
            'The project has twenty-five tests. [[slnc 300]] And what '
            'they check is the point. [[slnc 500]] No test checks that '
            'the product page is correct. [[slnc 300]] Both versions '
            'build the same page, so that would prove nothing. [[slnc '
            '500]] Instead, every test checks something only the gateway '
            'gives you. [[slnc 300]] The phone makes one call, not four. '
            '[[slnc 300]] The token is checked once, not four times. '
            '[[slnc 300]] The page arrives in two hundred and forty '
            'milliseconds, instead of eight hundred. [[slnc 500]] One '
            'test exists only to block a future mistake. [[slnc 300]] It '
            'checks that the price on the page is exactly the pricing '
            "service's answer, unchanged. [[slnc 300]] The day someone "
            'adds a discount inside the gateway, that test fails.'
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
            "Let's run the demo, which has five parts. [[slnc 500]] Part "
            'one: no gateway. [[slnc 300]] Four round trips, four token '
            'checks, and eight hundred milliseconds. [[slnc 400]] Part '
            'two: with a gateway. [[slnc 300]] One round trip, one token '
            'check, two hundred and forty milliseconds, and the same '
            'page. [[slnc 400]] Parts three and four are the outage we '
            'just heard. [[slnc 300]] The whole page lost without a '
            'gateway, and the page served minus one row with it. [[slnc '
            '600]] Part five is the one most people get wrong. [[slnc '
            '300]] This time, the catalog service is down. [[slnc 300]] '
            "That is the service that knows the product's name. [[slnc "
            '300]] And the gateway does not carry on. [[slnc 300]] It '
            'refuses, and tells the shopper the page cannot be shown '
            'right now. [[slnc 500]] That is correct. [[slnc 300]] A '
            'product page with no product on it is not a partial page. '
            '[[slnc 300]] It is a blank one. [[slnc 500]] A gateway is '
            'not a machine for hiding failures. [[slnc 300]] It is where '
            'someone has decided, service by service, what each failure '
            'costs.'
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
            'So, what should you remember? [[slnc 400]] An A P I gateway '
            'is one front door. [[slnc 300]] One trip across the network, '
            'one token check, one address, and one place that owns the '
            'decision about failures. [[slnc 600]] People often ask how '
            'this differs from the Facade pattern. [[slnc 300]] The shape '
            'is the same. [[slnc 300]] A facade is one door in front of '
            'many classes, inside one program. [[slnc 300]] A gateway is '
            'one door in front of many services, across a network that '
            'can be slow, and can fail. [[slnc 600]] One variation worth '
            'knowing: Backends for Frontends. [[slnc 300]] If the phone '
            'app and the in-store till want very different pages, give '
            'each its own gateway. [[slnc 300]] The same pattern, one '
            'gateway per kind of client.'
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
            'Now the honest costs. [[slnc 500]] A gateway is one more '
            'service to run, watch, and scale. [[slnc 400]] Every request '
            'goes through it. [[slnc 300]] So if it is slow, the whole '
            'shop is slow. [[slnc 500]] And the worst outcome, which is '
            'also the most common, is a gateway that slowly fills with '
            'business rules. [[slnc 300]] A discount here, a special case '
            'there. [[slnc 300]] Until it is a bottleneck that owns no '
            'data, and that nobody dares to change. [[slnc 300]] Keep it '
            'to joining, and forwarding. [[slnc 600]] And know when you '
            'do not need one. [[slnc 300]] One client and three services, '
            'on a fast connection, may be fine without it. [[slnc 300]] '
            'Reach for a gateway when the clients multiply, when the '
            'network is the slow part. [[slnc 300]] Or when nobody can '
            'say what happens to a page if one service goes down.'
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
            "That's the A P I Gateway pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'gateway is one front door that joins and forwards, and the '
            'place where someone decides which failures cost a section, '
            'and which cost the page. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 300]] It runs offline, with '
            'nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Move the try '
            'and catch in the gateway so it wraps all four calls. [[slnc '
            '300]] Then stop the pricing service, and look at the page. '
            '[[slnc 300]] You will have turned an honest error into a '
            'page with no price on it. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
