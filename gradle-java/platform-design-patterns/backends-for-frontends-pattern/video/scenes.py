"""Scene definitions for the Backends for Frontends teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the analogy is spoken in full before any class
name, and the two documents are described field by field in words rather than
left to the picture. The slides illustrate the narration; they never carry it.

Every figure spoken aloud comes from the captured output of `./gradlew run`,
which is deterministic by construction: the shop returns fixed data, the byte
counts are measured from the documents themselves, and nothing is random or
timed. DemoRunsTest pins the exact strings, so a change to the program that
moved a number would fail the build rather than quietly make this video wrong.

The running order mirrors the project. Scenes 2 to 6 are the problem, and they
take their time on purpose: the shared endpoint has to be given its due, and
the `?fields=` fix has to be shown *working*, or the audience leaves believing
this pattern is about payload size. Scenes 7 to 11 are the pattern. Scenes 12
to 14 are the bill: a rule copied into two backends, four jobs done twice, and
six clients that do not need six backends. None of the three raises an error,
which is why they get a third of the video rather than a footnote.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Backends for Frontends",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Backends for Frontends pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Each kind of client '
            'gets its own small backend service. [[slnc 300]] It is owned '
            'by the team that owns that client. [[slnc 300]] And its only '
            'job is to shape the data for that one screen. [[slnc 600]] '
            'Think of a restaurant with one kitchen and two rooms. [[slnc '
            '300]] A dining room, where couples stay two hours, and a '
            'counter for commuters with twenty minutes. [[slnc 300]] One '
            'waiter with one script cannot serve both well. [[slnc 300]] '
            'The fix is not a second kitchen. [[slnc 300]] It is a second '
            'waiter, with his own script. [[slnc 700]] In our online '
            'store, one coffee maker is shown on a phone screen with six '
            'things, and a desktop page with fifteen. [[slnc 500]] By the '
            'end, you will know why a smaller response does not solve '
            'this. [[slnc 300]] The one question that separates this '
            'pattern from an A P I gateway. [[slnc 300]] And three ways '
            'it costs more than it saves.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online shop. One product: a copper coffee maker.",
            "",
            "    the phone's product screen draws        6 things",
            "    the desktop product page draws         15 things",
            "",
            "Five services hold the data between them:",
            "",
            "    catalog      pricing      inventory",
            "    reviews      recommendations",
            "",
            "Both screens are correct.",
            "They disagree about what a product is.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] An online shop sells a '
            'copper coffee maker. [[slnc 500]] On a phone, the product '
            'screen shows six things. [[slnc 300]] The title, the price, '
            'one photo, a star rating, the number of ratings, and when it '
            'will arrive. [[slnc 500]] On a desktop, the same product '
            'shows fifteen things. [[slnc 300]] Including a full '
            'description, a specification table, five photos, and three '
            'written reviews. [[slnc 500]] Underneath sit five services: '
            'catalog, pricing, inventory, reviews, and recommendations. '
            '[[slnc 600]] Neither screen is wrong. [[slnc 300]] The two '
            'teams simply disagree about what a product is. [[slnc 300]] '
            'And everything in this video comes from that disagreement.'
        ),
    ),
    dict(
        key="03-chatty",
        kind="console",
        title="The First Design — The Phone Calls Everybody",
        body="""Act 1 - each service publishes its own endpoint, so the phone
        asks all five of them itself.

  calls from the phone:   5
    -> catalog
    -> pricing
    -> inventory
    -> reviews
    -> recommendations
  downloaded:             1767 bytes
  fields available:       29
  fields drawn on screen:  6

  Five round trips before a single pixel — and in sequence, because
  the later calls need the earlier answers.""",
        narration=(
            'First demo: the phone calls every service itself. [[slnc '
            '400]] Each service has its own endpoint, so the phone asks '
            "all five. [[slnc 300]] Five requests, over the customer's "
            'own mobile connection. [[slnc 500]] And they must happen one '
            'after another. [[slnc 300]] Five waits before anything '
            'appears on screen. [[slnc 300]] On a train, each one is '
            'slow. [[slnc 500]] About seventeen hundred bytes arrive, '
            'with twenty-nine fields. [[slnc 300]] And only six are '
            'shown. [[slnc 300]] But the real pain here is the five '
            'calls, not the bytes.'
        ),
    ),
    dict(
        key="04-shared",
        kind="console",
        title="The Second Design — One Endpoint For Everybody",
        body="""Act 2 - one endpoint in front of the five services, called by
        every client the shop has.

  calls from the phone:    1
  downloaded:             1755 bytes
  of that, actually drawn: 212 bytes
  thrown away on arrival: 1543 bytes  (87%)

  One round trip instead of five. That is a real win, and the
  pattern we end up with keeps it.

  But one endpoint publishes one document, and that document has
  to satisfy the fussiest client it has.""",
        narration=(
            'Second demo: one endpoint for everybody. [[slnc 400]] The '
            'shop puts one endpoint in front of the five services, and '
            'every client calls it. [[slnc 300]] One round trip instead '
            'of five. [[slnc 300]] That is a real win, and the final '
            'pattern keeps it. [[slnc 500]] But one endpoint returns one '
            'document for every client. [[slnc 300]] So it grows to hold '
            'everything any screen ever needed. [[slnc 500]] About '
            'seventeen hundred bytes reach the phone. [[slnc 300]] Only '
            'about two hundred are shown. [[slnc 300]] Eighty-seven '
            'percent is thrown away. [[slnc 500]] That looks like the '
            'problem. [[slnc 300]] It is about to turn out not to be.'
        ),
    ),
    dict(
        key="05-fields",
        kind="console",
        title="And the Obvious Fix Works",
        body="""  Ask for only the fields you want:

    GET /api/products/4417?fields=title,price,image,rating,ratingCount
        -> 212 bytes

  1755 bytes  ->  212 bytes.  One query parameter.
  No new services. Nothing to deploy. No pattern applied.

  If this were a story about payload size,
  it would end on this slide.""",
        narration=(
            'Because there is an obvious fix, and it works. [[slnc 400]] '
            'Let the client list the fields it wants, in the request. '
            '[[slnc 300]] Seventeen hundred bytes becomes about two '
            'hundred. [[slnc 500]] No new services, nothing to deploy. '
            '[[slnc 600]] So here is the most useful sentence in this '
            'video. [[slnc 300]] If this pattern were about payload size, '
            'the story would end here. [[slnc 300]] It would just be a '
            'query parameter. [[slnc 500]] People stop here, and think '
            'they have applied the pattern. [[slnc 300]] Then the next '
            'request arrives.'
        ),
    ),
    dict(
        key="06-delivery",
        kind="quote",
        title="The Request That Cannot Be Served",
        body=[
            '"Free delivery, arrives Friday."',
            "",
            "One line of text. It exists in no service.",
            "Ask inventory, ask the delivery rules,",
            "look at the clock, join the three.",
            "",
            "so half an hour of work — and five weeks of waiting",
            "",
            "— a new field on a shared endpoint changes a document",
            "   five other clients also receive, so it joins their queue",
        ],
        narration=(
            'The phone team wants one line under the price. [[slnc 300]] '
            'Free delivery, arrives Friday. [[slnc 500]] That sentence '
            'exists in no service. [[slnc 300]] It joins three facts: '
            "whether it is in stock, the delivery rules, and today's "
            'date. [[slnc 300]] Then it writes them as a sentence. [[slnc '
            '500]] That is half an hour of work. [[slnc 600]] But it is a '
            'new field on a shared endpoint, which five other clients '
            'also receive. [[slnc 300]] So it becomes a contract change, '
            "with a review, and a place in someone else's queue. [[slnc "
            '500]] The phone team waits five weeks. [[slnc 600]] That is '
            'the real problem. [[slnc 300]] Not a technical failure, but '
            'an organisational one. [[slnc 300]] And it is the one this '
            'pattern removes.'
        ),
    ),
    dict(
        key="07-pattern",
        kind="quote",
        title="The Pattern",
        body=[
            "Give each frontend its own backend,",
            "owned by the team that owns the screen,",
            "whose only job is to turn what the shop knows",
            "into the shape that one screen draws.",
            "",
            "each · more than one, or it is a gateway",
            "own · the screen's team changes it",
            "shape · and nothing but the shape",
        ],
        narration=(
            'Here is the pattern, in one sentence. [[slnc 300]] Give each '
            'frontend its own backend, owned by the team that owns the '
            'screen, whose only job is to shape the data for that screen. '
            '[[slnc 600]] Three words matter. [[slnc 500]] Each. [[slnc '
            '200]] There must be more than one. [[slnc 300]] A single box '
            'in front of everything is a gateway, not this. [[slnc 500]] '
            "Own. [[slnc 200]] The screen's team changes the backend. "
            '[[slnc 300]] If another team owns it, you have rebuilt the '
            'five-week queue. [[slnc 500]] Shape. [[slnc 200]] Only the '
            'shape: which fields, in what order, and how they are '
            'written. [[slnc 300]] Not business rules. [[slnc 300]] '
            'Breaking that third word is the first cost, later in this '
            'video.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 500]] At the centre is one "
            'interface, called client backend. [[slnc 300]] It says which '
            'client it is for, and returns the product screen for a '
            "product. [[slnc 500]] Two classes implement it: the phone's "
            "backend, and the desktop's. [[slnc 300]] And both run at the "
            'same time, answering the same question differently, on '
            'purpose. [[slnc 300]] Neither is a fallback. [[slnc 300]] '
            'The phone always talks to one, and the desktop always talks '
            'to the other. [[slnc 500]] Underneath both are the five shop '
            'services. [[slnc 300]] Both backends can reach all of them. '
            '[[slnc 300]] They only differ in what they choose to send. '
            '[[slnc 500]] Then there are two lists of fields: the six the '
            'phone shows, and the fifteen the desktop shows. [[slnc 300]] '
            'Those lists define what counts as waste.'
        ),
    ),
    dict(
        key="09-mobile",
        kind="code",
        title="A Backend That Knows One Screen",
        body="""// inside MobileBff.productScreen(sku)

Doc catalog   = shop.catalog(sku, Origin.INTERNAL);
Doc pricing   = shop.pricing(sku, Origin.INTERNAL);
Doc stock     = shop.inventory(sku, Origin.INTERNAL);
Doc reviews   = shop.reviews(sku, Origin.INTERNAL);
// and no call to recommendations: this screen has no strip

return Doc.of(
    "title",       catalog.text("title"),
    "price",       Money.format(pricing.number("amountPence")),
    "image",       catalog.firstImage(320),
    "rating",      reviews.number("average"),
    "ratingCount", reviews.number("count"),
    "delivery",    deliveryPromise(stock, clock));       // the 5-week field""",
        narration=(
            "Here is the phone's backend, in words. [[slnc 400]] It "
            'receives one request. [[slnc 300]] Then it makes four calls '
            'inside the data centre: catalog, pricing, inventory, and '
            'reviews. [[slnc 300]] It does not call recommendations at '
            'all, because the phone screen has nowhere to show them. '
            '[[slnc 300]] Only a backend that knows one screen can make '
            'that choice. [[slnc 600]] Then it builds six simple fields. '
            '[[slnc 500]] The price arrives from pricing as a whole '
            'number of pence. [[slnc 300]] The phone is sent ready-made '
            'text: forty-seven pounds ninety-nine. [[slnc 300]] So the '
            'phone team can change that formatting this afternoon, not in '
            'an app update. [[slnc 500]] And the last field is the '
            'delivery sentence. [[slnc 300]] Four lines of code, in the '
            "phone team's own project. [[slnc 300]] The field they waited "
            'five weeks for.'
        ),
    ),
    dict(
        key="10-two-docs",
        kind="console",
        title="Two Backends, Two Documents",
        body="""Act 3 - the phone app asks its own backend, and is sent:

    { "title":       "Copper Filter Coffee Maker, 1 Litre",
      "price":       "£47.99",
      "image":       "https://img.shop.example/4417/hero-320.jpg",
      "rating":      4.6,
      "ratingCount": 218,
      "delivery":    "Free delivery, arrives 2026-09-18" }

  the desktop store asks its own backend, and is sent 15 fields
  including the description, the specification, five images and
  three reviews -- and `delivery` as the bare date, not a sentence.

  Same five services underneath. Different shape.""",
        narration=(
            'Here are the two documents, read aloud. [[slnc 500]] The '
            'phone gets six fields. [[slnc 300]] The title: Copper Filter '
            'Coffee Maker, one litre. [[slnc 300]] The price: forty-seven '
            'pounds ninety-nine. [[slnc 300]] One small image. [[slnc '
            '300]] A rating of four point six, from two hundred and '
            'eighteen ratings. [[slnc 300]] And a sentence: free '
            'delivery, arrives on the eighteenth. [[slnc 600]] The '
            'desktop gets fifteen fields. [[slnc 300]] Everything the '
            'phone got, plus the description, the specification, five '
            'images, and three reviews. [[slnc 600]] Notice the delivery '
            'field. [[slnc 300]] The phone gets a whole sentence. [[slnc '
            '300]] The desktop gets just the date, because its page '
            'writes its own sentence. [[slnc 500]] Two backends '
            'disagreeing about the shape of a product is not a mistake. '
            '[[slnc 300]] It is the pattern working.'
        ),
    ),
    dict(
        key="11-three-ways",
        kind="console",
        title="The Same Product, Three Ways",
        body="""Act 4 - and the two right-hand columns are the point.

  design                          bytes   device internal
  five calls from the phone        1767        5        5
  one shared endpoint             1755        1        5
  a backend for the phone          196        1        4

  device calls:    5  ->  1  ->  1      the customer's connection
  internal calls:  5  ->  5  ->  4      a data-centre network

  The work did not go away.
  It moved onto a network where a call costs nothing.""",
        narration=(
            'Now the three designs, side by side. [[slnc 500]] Calls made '
            "from the phone, over the customer's connection: five, then "
            'one, then one. [[slnc 300]] Calls made inside the shop: '
            'five, then five, then four. [[slnc 600]] So the work did not '
            'disappear. [[slnc 300]] Four slow trips over a mobile '
            'network moved into the data centre, where each call takes '
            'well under a millisecond. [[slnc 300]] The pattern moves '
            'cost. [[slnc 300]] It does not delete it. [[slnc 600]] And '
            "the bytes are still good. [[slnc 300]] The phone's own "
            'document is under two hundred bytes. [[slnc 300]] About '
            'eighty-nine percent smaller than the shared one.'
        ),
    ),
    dict(
        key="12-divergence",
        kind="console",
        title="The Bill, Part One — One Rule, Two Answers",
        body="""Act 5 - pricing reviews the discount rule and adds a condition:
        a higher price may only be advertised as a saving if it was
        genuinely in force long enough. This one went up 11 days ago.
        Both backends are told so.

  desktop store says:  (nothing - no saving may be claimed for this price)
  phone app says:      Save £12.00

  Nothing throws. Nothing is logged. Both test suites pass.
  The only witness is a customer with both screens open.

  A backend for a frontend may hold the shape. Anything the shop
  would still believe with every client switched off belongs behind it.""",
        narration=(
            'That is the pattern, and it works. [[slnc 300]] Now the '
            'bill, with three items. [[slnc 600]] Item one. [[slnc 300]] '
            'The pricing team changes the discount rule. [[slnc 300]] A '
            'higher price may only be advertised as a saving if it was in '
            "force long enough first. [[slnc 300]] This product's price "
            'went up eleven days ago, which does not qualify. [[slnc '
            '600]] The desktop uses the current rule, and claims no '
            "saving. [[slnc 300]] But the phone's backend has its own old "
            'copy of the rule. [[slnc 300]] So it advertises twelve '
            'pounds off. [[slnc 600]] Same product, same moment, and one '
            'screen makes a claim the shop is not allowed to make. [[slnc '
            '300]] Nothing fails. [[slnc 300]] Both sets of tests pass. '
            '[[slnc 600]] So here is the rule to remember. [[slnc 300]] A '
            'backend for a frontend may hold the shape. [[slnc 300]] '
            'Anything the shop would still believe with every screen '
            'switched off belongs behind it. [[slnc 300]] Tax, discounts, '
            'stock, and what a price means.'
        ),
    ),
    dict(
        key="13-gateway",
        kind="console",
        title="The Bill, Part Two — Where the Shared Jobs Go",
        body="""Act 6 - four jobs every request needs, whoever sent it:

    verify the customer's token       refuse traffic over the limit
    terminate TLS                    write the access log

  each backend doing it itself:  8 copies across 2 backends
  a gateway in front:            4 copies, whatever the number

  copiesBehindAGateway() takes no argument.
  That absence is the answer.

  "what does this screen need?"      -> a backend for that frontend
  "is this request allowed in?"      -> in front of all of them""",
        narration=(
            'Item two: where do the shared jobs go? [[slnc 500]] Every '
            'request needs four things done, whoever sent it. [[slnc '
            "300]] Check the customer's login. [[slnc 200]] Refuse too "
            'much traffic. [[slnc 200]] Handle the encryption. [[slnc '
            '200]] And write the access log. [[slnc 600]] Put those '
            'inside each backend, and there are eight copies across two '
            'backends. [[slnc 300]] Put a gateway in front, and there are '
            'four, however many backends you add. [[slnc 600]] So here is '
            'the question that settles it. [[slnc 300]] What does this '
            'code answer? [[slnc 300]] If it answers: what does this '
            'screen need? [[slnc 300]] It belongs in a backend for that '
            'frontend. [[slnc 300]] If it answers: is this request '
            'allowed in at all? [[slnc 300]] It belongs in a gateway in '
            'front of all of them. [[slnc 500]] A gateway is about entry. '
            '[[slnc 300]] A backend for a frontend is about shape.'
        ),
    ),
    dict(
        key="14-howmany",
        kind="console",
        title="The Bill, Part Three — How Many Is Too Many",
        body="""Act 7 - the shop has six clients.

  phone app        own backend     six fields, one sentence, a small screen
  desktop store    own backend     description, spec, five images, reviews
  tablet app       shares one      the phone's fields in a wider column
  smart TV app     own backend     no keyboard, so no search; pictures work
  in-store kiosk   shares one      the desktop page with the basket hidden
  partner feed     shares one      not a screen at all - a nightly file

  one per client:               6 backends
  one per genuine disagreement: 3 backends

  Each extra one costs, every week: a pipeline, a place in the
  on-call rota, an upgrade whenever a shop service changes, and
  one more process to look at during an incident.""",
        narration=(
            'Item three: how many is too many? [[slnc 500]] The shop has '
            'six clients. [[slnc 300]] A phone app, a desktop store, a '
            'tablet app, a smart television app, an in-store kiosk, and a '
            'nightly partner feed. [[slnc 600]] But the tablet shows the '
            "phone's six fields in a wider column. [[slnc 300]] So it "
            "shares the phone's backend. [[slnc 300]] The kiosk is the "
            'desktop page, with the basket hidden. [[slnc 300]] And the '
            'partner feed is not a screen at all. [[slnc 500]] Only three '
            'of the six really disagree about what a product is. [[slnc '
            '600]] Every extra backend costs something every week. [[slnc '
            '300]] A build pipeline, an on-call rota, upgrades, and one '
            'more thing to read during a night-time incident. [[slnc '
            '500]] Two backends is a pattern. [[slnc 300]] Nine is a '
            'department.'
        ),
    ),
    dict(
        key="15-takeaway",
        kind="bullets",
        title="What to Take Away",
        body=[
            "Is the endpoint named after a resource, or after a screen?",
            "/api/products/4417 belongs to everybody, so to nobody.",
            "",
            "The saving is not bytes. It is whose queue you are in.",
            "A ?fields= parameter gets the bytes and changes nothing else.",
            "",
            "Shape inside. Anything the shop believes, behind.",
            "Ask: would this still be true with every client switched off?",
            "",
            "One per genuine disagreement — not per device, not per team.",
            "And no test you can write will notice when you get this wrong.",
        ],
        narration=(
            'Here are four things to remember. [[slnc 500]] One. [[slnc '
            '200]] Is the endpoint named after a resource, or after a '
            'screen? [[slnc 300]] An endpoint for products belongs to '
            'everybody, and so to nobody. [[slnc 300]] An endpoint for '
            "the phone's product screen belongs to one team. [[slnc 400]] "
            'Two. [[slnc 200]] The saving is not bytes. [[slnc 300]] It '
            'is whose queue you are standing in. [[slnc 400]] Three. '
            '[[slnc 200]] Shape goes inside the backend. [[slnc 300]] '
            'Anything the shop believes goes behind it. [[slnc 400]] '
            'Four. [[slnc 200]] One backend per real disagreement about '
            'what a product is. [[slnc 300]] Not per device, and not per '
            'team. [[slnc 600]] And one warning. [[slnc 300]] All four '
            'can go wrong without anything failing. [[slnc 300]] Because '
            'from inside each backend, each one is right.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, tests, diagrams and an interactive animation",
            "are in the repository — including all three costs.",
            "",
            "Run it yourself:  ./gradlew run",
        ],
        narration=(
            "That's the Backends for Frontends pattern. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] '
            'Each screen gets its own backend, owned by the team that '
            'draws the screen, and it holds the shape, and nothing else. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 300]] All three costs are there as running code, too. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            "Update the phone backend's copy of the discount rule. [[slnc "
            '300]] Then check that both screens agree again. [[slnc 500]] '
            'If this helped, a like really does help other people find '
            "it. [[slnc 300]] And subscribe, if you'd like the rest of "
            'the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
