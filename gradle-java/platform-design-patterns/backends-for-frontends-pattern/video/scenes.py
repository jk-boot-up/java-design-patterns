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
            "Hello, and welcome. This video explains the Backends for Frontends "
            "design pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] Let's start with the simple "
            "definition. Backends for Frontends means giving each kind of client "
            "its own small backend service, owned by the team that owns that "
            "client, whose only job is to turn what the system knows into the "
            "exact shape that one screen draws. [[slnc 350]] Think of a "
            "restaurant with one kitchen and two rooms: a dining room, "
            "where couples settle in for two hours, and a counter by the "
            "window for people who have twenty minutes before a train. Give both "
            "rooms the same waiter working from one script, and that script "
            "becomes everything either room might want — the full wine list, "
            "where the lamb came from, the dessert menu — recited to everybody. "
            "The couple enjoy it. The commuter misses their train. [[slnc 300]] "
            "And notice what the fix is not. It is not a second kitchen, because "
            "the food is the same food and a second kitchen is two places for a "
            "recipe to live. The fix is a second waiter, who is allowed to change "
            "his own script tomorrow morning. "
            "[[slnc 350]] That's the idea in a sentence. The rest of the video "
            "does it properly, by building a real working Java project: an online "
            "shop selling one coffee maker, a phone screen that draws six things, "
            "and a desktop page that draws fifteen. [[slnc 250]] By the end you'll know why "
            "making the response smaller does not solve this, the one question "
            "that separates this pattern from an API gateway, and the three ways "
            "it costs more than it saves."
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
            "So, imagine an online shop, and imagine it sells one copper coffee "
            "maker. We are going to look at that one product for the whole of "
            "this video. [[slnc 300]] On a phone, the product screen draws six "
            "things: the title, the price, one photograph, a star rating, the "
            "number of ratings behind that star, and one line saying when "
            "the parcel will arrive. Six. That is all that fits on a screen four "
            "inches tall. [[slnc 300]] On a desktop, the same product fills a "
            "page with fifteen. The title and the price, yes, but also the "
            "full description, a specification table, five photographs, and three "
            "written reviews. [[slnc 350]] Underneath both of them sit five "
            "services: catalog, pricing, inventory, reviews, and "
            "recommendations, which builds the strip of other things you "
            "might like. [[slnc 350]] Now here is the situation, and it is worth "
            "sitting with. Neither screen is wrong. The phone team is being "
            "reasonable and the desktop team is being reasonable. They simply "
            "disagree about what a product is — and everything in this video "
            "comes out of that disagreement."
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
            "The first design is the one shops arrive at by accident, and it "
            "arrives by accident because it is nobody's decision. Each service "
            "owns its own data and publishes its own endpoint, so the phone just "
            "asks all five of them. [[slnc 300]] Five requests out, five "
            "answers back, every one of them across the "
            "customer's own mobile connection. [[slnc 350]] And they cannot "
            "happen all at once. You cannot ask pricing about a product until the "
            "catalog has said which product it is, so the calls go one after "
            "another. Five waits, end to end, before a single pixel can be "
            "drawn. [[slnc 300]] On office wifi nobody notices. On a train, each "
            "one is a wait of its own. [[slnc 350]] And look at the "
            "arithmetic on the way in. Seventeen hundred and sixty-seven bytes "
            "land on the phone, carrying twenty-nine fields, and six of them "
            "reach the screen. That is wasteful — but hold onto the five, not the "
            "bytes, because the five is what actually hurts here."
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
            "So the shop does the obvious thing. It puts one endpoint in front of "
            "the five services, and every client calls that. [[slnc 300]] And "
            "this genuinely helps. One round trip instead of five, which is the "
            "expensive part gone, and I want to be fair to it: the pattern we end "
            "up with keeps that improvement rather than replacing it. [[slnc "
            "350]] But one endpoint publishes one document. And that document has "
            "to satisfy every client the shop has, which means over time it grows "
            "into everything that anybody has ever needed. The union of all the "
            "screens. [[slnc 350]] So seventeen hundred and fifty-five bytes "
            "arrive on the phone. Two hundred and twelve of them are drawn. "
            "Fifteen hundred and forty-three are thrown away the moment they "
            "arrive — eighty-seven per cent of what the customer's connection was "
            "asked to carry. [[slnc 300]] Now, that number looks like the "
            "problem. It is about to turn out not to be."
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
            "Because there is an obvious fix, and it works completely. [[slnc "
            "300]] Let the client say which fields it wants. Add a list of field "
            "names to the query string, and the endpoint sends back only those. "
            "Seventeen hundred and fifty-five bytes becomes two hundred and "
            "twelve. [[slnc 350]] That is the same saving the finished pattern "
            "gets, achieved with one query parameter, no new services to run, "
            "nothing to deploy and no architecture diagram. [[slnc 400]] So I "
            "want to say this as plainly as I can, because it is the most useful "
            "sentence in this video. If Backends for Frontends were about payload "
            "size, the story would end here. It would not be a pattern. It would "
            "be a query parameter. [[slnc 300]] People do stop here. They add the "
            "parameter, they measure the bytes, they write it up, and they believe "
            "they have applied the pattern. And then the next request comes in."
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
            "The phone team wants one line of text under the price. Free "
            "delivery, arrives Friday. [[slnc 300]] That sentence does not exist "
            "in any service, and it cannot, because it is not a fact — it is "
            "three facts joined together and written out in English. Ask "
            "inventory whether the item is in stock. Ask the delivery rules what "
            "that means for tomorrow. Look at the clock. Then write the "
            "sentence the designer asked for. [[slnc 350]] That is half an hour "
            "of work. It is a small method. [[slnc 400]] But it is a "
            "new field on a shared endpoint, and that document is "
            "also received by five other clients. So it is not half an hour of "
            "work any more. It is a change to a contract, which needs a review "
            "and a place in a queue, behind work that has nothing to "
            "do with the phone. [[slnc 350]] The phone team could have written it "
            "in an afternoon. They wait five weeks. [[slnc 350]] And that is the "
            "real problem. It is not a technical failure — every service here is "
            "well built. It is an organisational failure with a technical cause, "
            "and it is the one this pattern removes."
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
            "Here, then, is the pattern, in one sentence. Give each frontend its "
            "own backend, owned by the team that owns the screen, whose only job "
            "is to turn what the shop knows into the exact shape that one screen "
            "draws. [[slnc 400]] Three words in that sentence are carrying it, "
            "and each one rules out a near miss, so let me pull them apart. "
            "[[slnc 350]] Each. More than one. If you put a single box in front "
            "of your services and every client calls it, you have built a "
            "gateway, which is a fine thing to build and is not this. [[slnc "
            "350]] Own. The team that draws the screen changes the backend. If "
            "the platform team owns something called the mobile API, you have "
            "recreated the five-week queue and given it a nicer name. Ownership "
            "is not a detail of this pattern. It is most of the value. [[slnc "
            "350]] And shape. Only the shape. Which fields, in what order, "
            "formatted how, joined from where. Not rules, not policy, not "
            "arithmetic the shop believes. [[slnc 300]] That third word is the "
            "one that gets broken, and breaking it is the first item on the bill "
            "later in this video."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let me name the pieces, because they are all small and there are "
            "only a handful that matter. [[slnc 300]] At the centre is an "
            "interface called client backend. It says two things: what client am "
            "I for, and give me the product screen for this product. [[slnc 350]] "
            "Two classes implement it — the phone's backend and the "
            "desktop's — and both of them are "
            "live, at the same time, in production, answering the same question "
            "differently on purpose. [[slnc 350]] That is unusual. Most of the "
            "time an interface with two implementations means you will pick one: "
            "this store today, that store tomorrow. Not here. Neither is the "
            "fallback and nobody will ever choose "
            "between them, because the phone always talks to the first and the "
            "desktop always talks to the second. Two arrows pointing at one "
            "interface is not a detail here. It is the pattern "
            "itself. [[slnc 350]] Underneath both sits the shop: the five "
            "services. Both backends can reach all of it, so "
            "neither has anything the other cannot get. What differs is only what "
            "each one chooses to send on. [[slnc 350]] Then there is a class "
            "called screens, which is two lists of field names — the six the phone "
            "draws and the fifteen the desktop draws. That is the ruler. "
            "Everywhere this project says the word waste, it means not on one of "
            "those two lists. [[slnc 300]] And off to one side, connected to "
            "nothing, sit the chatty phone and the shared endpoint: the two "
            "designs this pattern replaces."
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
            "This is the one piece of code worth reading closely, and I will "
            "describe it rather than spell out the syntax. [[slnc 300]] The "
            "phone's backend receives one request. It then makes four calls, "
            "inside the data centre: catalog, pricing, inventory, reviews. [[slnc "
            "300]] And it does not call recommendations at all — not because "
            "recommendations is slow, but because this screen has no "
            "related-products strip, so that data has nowhere to go. A "
            "backend that knows exactly one screen can make that decision. A "
            "shared endpoint never can. [[slnc 400]] Then it builds six flat "
            "fields, and two are worth stopping on. [[slnc 300]] The "
            "price. Pricing returned the number four thousand seven hundred and "
            "ninety-nine — pence, as an integer, which is the right way for a "
            "pricing service to hold money. What the phone is sent is the text: "
            "pound sign, forty-seven, point, ninety-nine. That conversion happened "
            "in a process the phone team can correct this afternoon, rather than "
            "inside an app customers will still be running in two years. "
            "[[slnc 350]] And the last line is the delivery promise. Four "
            "lines of code, in the phone team's own repository, in the phone "
            "team's own deployment. That is the field they waited five weeks for."
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
            "So here are the two documents, and because they are the heart of "
            "this let me read them to you rather than leave them on the screen. "
            "[[slnc 300]] The phone is sent six fields. The title, Copper Filter "
            "Coffee Maker, one litre. The price, as text, forty-seven pounds "
            "ninety-nine. One image, the three-hundred-and-twenty-pixel "
            "one, because that is what a phone needs. A rating of four point six. "
            "A rating count of two hundred and eighteen. And the delivery "
            "sentence: free delivery, arrives on the eighteenth. [[slnc 400]] The "
            "desktop is sent fifteen — everything the phone got, plus the "
            "description, the specification, five images rather than one, and "
            "three written reviews. [[slnc 350]] Now compare the delivery field "
            "across the two, because this is the part people try to tidy up. The "
            "phone was given a whole sentence. The desktop was given the bare "
            "date. [[slnc 300]] That is not an inconsistency. "
            "The desktop page has a delivery panel with its own layout, so it "
            "wants the parts and will write its own sentence. Two backends over "
            "the same data, disagreeing about the shape of a product, is not the "
            "pattern going wrong. It is the pattern working."
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
            "Here are the three designs measured side by side, and I am going to "
            "ignore the byte column for a moment, because the two columns to the "
            "right of it are the honest ones. [[slnc 350]] The calls made from "
            "the phone, across the customer's own connection, go five, then one, "
            "then one. [[slnc 300]] The calls made inside the shop go five, then "
            "five, then four. [[slnc 400]] So the work did not go away. Nothing "
            "was eliminated. Four round trips moved off a mobile network, where "
            "each one might cost a tenth of a second on a train, and onto a "
            "data-centre network, where a call costs well under a millisecond. "
            "This pattern relocates cost; it does not "
            "delete it. [[slnc 350]] And now the bytes, because they are still "
            "good. The phone's own document is a hundred and ninety-six bytes "
            "against the shared endpoint's seventeen hundred and fifty-five. "
            "Eighty-nine per cent less. [[slnc 300]] One more thing, and it "
            "matters if you are thinking about your own system. Those four "
            "internal calls happen one after another in this project. A real "
            "backend would fire them off together and wait once. So everything "
            "you have heard so far understates the benefit rather than "
            "overstating it."
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
            "So that is the pattern, and it works. Now the bill, because there "
            "are three items on it, and all three are the price of the pattern "
            "rather than mistakes made while applying it. [[slnc 350]] Item one. "
            "The pricing team reviews the discount rule and adds a condition: a "
            "higher price may only be advertised as a saving if it was genuinely "
            "in force for long enough first. Otherwise you could put the price up "
            "on Monday and advertise a discount on Tuesday. [[slnc 300]] This "
            "product's price went up eleven days ago, which does not qualify, and "
            "both backends are told so. [[slnc 350]] The desktop reads the "
            "current rule and claims nothing. [[slnc "
            "300]] The phone's backend runs a copy of that rule, taken before the "
            "review. It does the subtraction, and it advertises twelve pounds "
            "off. [[slnc 400]] Same product, same price, same second, and one of "
            "those two screens is making a claim the shop is not allowed to make. "
            "[[slnc 350]] Now, listen to what is not happening. Nothing throws. "
            "Nothing is logged. Both backends have tests and both sets pass. The "
            "copy is not careless — it was correct when it was written, and it is "
            "wrong only in relation to a decision taken "
            "months later by people with no reason to know it existed. "
            "[[slnc 350]] The only person who can see the problem is a customer "
            "with both screens open. [[slnc 300]] So here is the rule, and it is "
            "the thing to write down from this video. A backend for a frontend "
            "may hold the shape. Anything the shop would still believe with every "
            "client switched off belongs behind it — tax, discounts, stock "
            "allocation, what a price means."
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
            "Item two, and it is the confusion this pattern is most often lost "
            "in. [[slnc 300]] There are four things every request needs done to "
            "it, whoever sent it. Verify the customer's token. Refuse traffic "
            "over the rate limit. Terminate the encryption. Write the "
            "access log. [[slnc 350]] The nearest place to put any of those is "
            "inside whichever backend you happen to have open. Do that, and it is "
            "four jobs times two backends — eight copies of work that is "
            "identical by definition. [[slnc 300]] Put a gateway in front and it "
            "is four, and it stays four however many backends you add. In the "
            "project, the method that counts those four takes no argument, "
            "and that absence is the whole answer. [[slnc 400]] So here is the "
            "question that settles every argument about whether something is a "
            "gateway or a backend for a frontend. Ask what the code answers. "
            "[[slnc 300]] If it answers, what does this screen need — it belongs "
            "in a backend for that frontend. If it answers, is this request "
            "allowed in at all — it belongs in front of all of them. [[slnc 350]] "
            "A gateway is about entry. A backend for a frontend is about shape. "
            "They are neighbours, they are often deployed together, and they are "
            "not the same pattern."
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
            "Item three, and this is the one that turns a good idea into a "
            "department. [[slnc 300]] The shop has six clients. A phone app, a "
            "desktop store, a tablet app, a smart television app, an in-store "
            "kiosk, and a nightly feed for a partner. One backend each would be "
            "six. [[slnc 350]] But look at them properly. The tablet shows the "
            "phone's six fields in a wider column — it disagrees about nothing, "
            "so it is the same backend and a different stylesheet. The kiosk is "
            "the desktop page with the basket hidden. The partner feed is not a "
            "screen at all; it is a file, once a night. [[slnc 300]] Three of the "
            "six genuinely disagree about what a product is. Three do not. [[slnc "
            "400]] So the test is not the device, and — this one catches people — "
            "it is not the team either. [[slnc 350]] And the reason to be "
            "strict about it is that every extra backend costs something every "
            "week for as long as it exists. A pipeline. A "
            "place in the on-call rota. A dependency upgrade every time one "
            "of the shop's services changes. And one more process somebody has to "
            "read during an incident at three in the morning. [[slnc "
            "350]] Two backends is a pattern. Nine is a department."
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
            "Four things to take away. [[slnc 300]] First, the question that "
            "identifies this pattern in the wild: is the endpoint named after a "
            "resource, or after a screen? Slash products slash four four one "
            "seven belongs to everybody, and therefore to nobody in particular. "
            "Slash phone slash product screen belongs to one team, and that team "
            "can add a field to it this week. [[slnc 350]] Second, the saving is "
            "not bytes. It is whose queue you are standing in. If somebody says "
            "they applied this pattern and the evidence is a payload "
            "measurement, they may well have added a query parameter. [[slnc "
            "350]] Third, shape goes inside the backend and anything the shop "
            "believes goes behind it. The test is one sentence: would this still "
            "be true with every client switched off? [[slnc 350]] Fourth, one backend per genuine "
            "disagreement about what a product is. Not per device. Not per team. "
            "[[slnc 350]] And one warning to leave you with. Every one of those "
            "four can be got wrong without anything failing. There is no test you "
            "can write inside either backend that notices the two of them have "
            "drifted apart, because from inside each one, each one is right."
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
            "And that is Backends for Frontends. Each screen gets its own "
            "backend, owned by the team that draws the screen, and it holds the "
            "shape and nothing else. [[slnc 350]] The whole project is in the "
            "repository — the source, forty-six tests, the diagrams, and an "
            "interactive animation that shrinks the document one step at a time. "
            "All three costs are in there as running code too, so you can watch "
            "the two backends disagree and then fix it by changing one line. "
            "[[slnc 300]] If this was useful, please like the video and "
            "subscribe. Thanks very much for watching, and I'll see you in the "
            "next one."
        ),
    ),
]
