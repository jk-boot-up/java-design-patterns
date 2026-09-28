"""Scene definitions for the API Composition teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the sandwich analogy is spoken in full before
any class name appears, and the console slides are read out as a story about
when each call left rather than as columns of numbers. The slides illustrate
the narration; they never carry it.

Every number quoted in these scenes comes from the real output of
`./gradlew run`: Orders answers in 30ms, Catalog in 60ms, Shipping in 120ms,
three calls in a queue cost 210ms, the same three calls with the two that can
leave together leaving together cost 150ms, three services at 99.900% make a
page at 99.700% -- 129.5 minutes of downtime a month against 43.2 -- and
Shipping slowed to 400ms makes the page cost 430ms.

Scene order is the argument, and it has two halves. The first half is
arithmetic and demos beautifully: sum versus maximum, scenes three to nine.
The second half is the one most treatments skip, and it is a product argument
rather than a technical one: what a page is allowed to do when a dependency is
missing, scenes eleven to fourteen. The two halves must stay in this order,
because "make the delivery section optional" is meaningless until the viewer
has seen the fan-out work; and the availability arithmetic in scene fourteen is
what turns the classification from a nicety into the only lever there is. Do
not move scene fourteen earlier -- it is the payoff, not the setup.

Layout limit: on "bullets" and "quote" slides the body starts at y=260 and
steps 60 pixels a line, and the footer sits at y~1022, so twelve body lines
is the maximum.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="API Composition",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the A P '
            'I Composition pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] When one screen needs data '
            'that several different services own, you ask all of them. '
            '[[slnc 300]] And you assemble the answer yourself. [[slnc '
            '600]] Think of making a sandwich, when no shop sells it '
            'ready-made. [[slnc 300]] You need bread from the baker, '
            'tomatoes from the grocer, and cheese from the deli. [[slnc '
            '700]] There are two halves to this pattern. [[slnc 300]] The '
            'easy half: calls made one after another cost the total of '
            'their waiting times. [[slnc 300]] But calls sent together '
            'cost only the longest one. [[slnc 500]] The harder half: for '
            'every service you ask, someone must decide in advance '
            'whether the screen can be shown without it. [[slnc 500]] In '
            'this video, an online shop shows a customer one of their '
            'orders. [[slnc 300]] By the end, you will know why that page '
            'takes two hundred and ten milliseconds, when it could take '
            'one hundred and fifty. [[slnc 300]] And why three excellent '
            'services can combine into a page worse than any one of them.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "A shopper opens one of their orders: the",
            "reference, a line per item with its name and",
            "price, the total, and where the parcel has got to.",
            "",
            "Utterly unremarkable. Except that three",
            "different services own those facts:",
            "",
            "Orders knows what was bought.",
            "Catalog knows what a sku is actually called.",
            "Shipping knows where the parcel is.",
            "",
            "And there is no database join any more.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] A shopper clicks on one '
            'of their past orders. [[slnc 300]] The page shows the order '
            'reference. [[slnc 300]] Then a line for each item: its name, '
            'how many, and what it cost. [[slnc 300]] Then the total. '
            '[[slnc 300]] And finally, where the parcel is now. [[slnc '
            '500]] A completely ordinary page. [[slnc 300]] Except that '
            'three different services own those facts. [[slnc 500]] The '
            'Orders service knows what was bought, and what was paid. '
            '[[slnc 300]] The Catalog service is the only one that knows '
            "a product code's real name. [[slnc 300]] And the Shipping "
            'service is the only one that knows where the parcel is. '
            '[[slnc 500]] Each has its own database, and none can see '
            'into the others. [[slnc 300]] So no single query can build '
            'this page. [[slnc 300]] Someone must ask all three, and put '
            'the answer together.'
        ),
    ),
    dict(
        key="03-three-calls",
        kind="code",
        title="The Obvious Answer — Three Calls",
        body="""Order order = orders.fetch(orderId);

Map<String, String> names =
        catalog.namesFor(order.skus());

DeliveryStatus delivery =
        shipping.statusFor(orderId);

return assemble(order, names, delivery);

// no bug. right page. every test passes.""",
        narration=(
            'Here is what everyone writes first: three ordinary lines of '
            'Java. [[slnc 400]] Fetch the order. [[slnc 300]] Ask Catalog '
            'for the product names. [[slnc 300]] Ask Shipping for the '
            'delivery status. [[slnc 300]] Then build the page from the '
            'three answers. [[slnc 500]] To be fair, there is no bug '
            'here. [[slnc 300]] It is easy to read, it returns exactly '
            'the right page, and every test passes. [[slnc 300]] A code '
            'review would approve it without a comment. [[slnc 500]] '
            'Because the cost of this code is not in the code. [[slnc '
            "300]] Let's run it, and listen to the clock."
        ),
    ),
    dict(
        key="04-act-one",
        kind="console",
        title="Act One — Three Calls, One After Another",
        body="""$ ./gradlew run

1. three calls, one after another
  ord-3001  total £70.95
    SKU-KETTLE   Stainless Steel Kettle   x1  £34.99
    SKU-MUG      Blue Stoneware Mug       x4  £35.96
    delivery: Royal Mail, out for delivery
      0ms ->    30ms  Orders           OK
     30ms ->    90ms  Catalog          OK
     90ms ->   210ms  Shipping         OK

  the shopper waited 210ms: 30 + 60 + 120, added up""",
        narration=(
            'First demo: three calls, one after another. [[slnc 400]] The '
            'call to Orders starts at zero, and returns at thirty '
            'milliseconds. [[slnc 300]] The call to Catalog starts at '
            'thirty, and returns at ninety. [[slnc 300]] The call to '
            'Shipping starts at ninety, and returns at two hundred and '
            'ten. [[slnc 500]] Thirty, plus sixty, plus one hundred and '
            'twenty. [[slnc 300]] The shopper waited two hundred and ten '
            'milliseconds, as each service took its turn. [[slnc 500]] '
            'Now here is the key question. [[slnc 300]] Which of those '
            'three calls actually needed the answer from the one before '
            'it?'
        ),
    ),
    dict(
        key="05-sixty-wasted",
        kind="bullets",
        title="Sixty Of Those Milliseconds Bought Nothing",
        body=[
            "Catalog genuinely had to wait. It needs to be",
            "told WHICH skus to look up, and only the order",
            "knows that.",
            "",
            "But Shipping needs one thing: the order id —",
            "and the order id arrived at 30ms.",
            "",
            "It waited 60ms for Catalog's answer — and then",
            "never looked at it.",
            "",
            "No diff shows you that. It is what a sequence",
            "of statements does.",
        ],
        narration=(
            "Let's answer it. [[slnc 400]] Catalog really did have to "
            'wait. [[slnc 300]] To look up product names, it needs the '
            'product codes. [[slnc 300]] And only the order knows which '
            'products are on it. [[slnc 500]] But what does Shipping '
            'need? [[slnc 300]] Just one thing: the order I D. [[slnc '
            '300]] And the shopper clicked on that order I D before any '
            'call was made. [[slnc 500]] So the call to Shipping waited '
            "sixty milliseconds for Catalog's answer. [[slnc 300]] And "
            'then never even looked at it. [[slnc 300]] Sixty '
            'milliseconds, spent on nothing. [[slnc 500]] No code review '
            'could catch this, because nothing is wrong with any single '
            'line. [[slnc 300]] That is simply what a sequence of '
            'statements does. [[slnc 300]] It does them in sequence.'
        ),
    ),
    dict(
        key="06-sandwich",
        kind="quote",
        title="The Sandwich From Three Shops",
        body=[
            "You want a sandwich. No shop sells the finished",
            "thing, so you need bread from the baker,",
            "tomatoes from the grocer, cheese from the deli.",
            "",
            "Go to each in turn and lunch takes three trips.",
            "Send three people and it takes one — the longest.",
            "",
            "No shop got faster. You stopped queuing.",
            "",
            "And decide NOW what happens if a shop is shut.",
            "No bread is no lunch. No tomatoes is fine —",
            "as long as you don't claim there were tomatoes.",
        ],
        narration=(
            'Forget software for a moment, and think about that sandwich. '
            '[[slnc 400]] You need bread from the baker, tomatoes from '
            'the grocer, and cheese from the deli. [[slnc 500]] Two '
            'things follow, and together they are the whole pattern. '
            '[[slnc 500]] First: go to all three shops at once. [[slnc '
            '300]] Visit them one after another, and lunch takes three '
            'trips. [[slnc 300]] Send three people at the same time, and '
            'lunch takes as long as the slowest trip. [[slnc 300]] No '
            'shop got faster. [[slnc 300]] You simply stopped waiting for '
            'one before starting the next. [[slnc 600]] Second, and this '
            'is the part people skip. [[slnc 300]] Decide, before you '
            'leave the house, what happens if a shop is shut. [[slnc '
            '500]] No bread means no sandwich at all. [[slnc 300]] No '
            'tomatoes means a sandwich without tomatoes. [[slnc 300]] '
            'That is fine, as long as nobody claims there were tomatoes '
            'on it. [[slnc 500]] That second decision has nothing to do '
            'with programming. [[slnc 300]] And it must be made before '
            'you reach the shops.'
        ),
    ),
    dict(
        key="07-not-flat",
        kind="bullets",
        title="It Is Rarely One Flat Fan-Out",
        body=[
            "The tempting fix: send all three at 0ms.",
            "",
            "This page cannot. Catalog has to be told which",
            "skus to name, and only Orders knows them.",
            "",
            "So the real shape is: one call, then two together.",
            "",
            "Working out which calls genuinely depend on",
            "which is most of the job — and it is where",
            "\"just parallelise it\" comes unstuck.",
            "",
            "In real systems: a couple of waves, not a burst.",
        ],
        narration=(
            'So the fix is to stop waiting. [[slnc 300]] But be careful '
            'how far you take that. [[slnc 500]] The tempting version is '
            'to send all three calls at the very start. [[slnc 300]] This '
            'page cannot do that. [[slnc 300]] Catalog must be told which '
            'product codes to look up, and only the order knows them. '
            '[[slnc 500]] So the real shape is one call, and then two '
            'together. [[slnc 300]] Fetch the order first, on its own. '
            '[[slnc 300]] Then send Catalog and Shipping at the same '
            'instant. [[slnc 500]] Working out which calls truly depend '
            'on which is most of the job. [[slnc 300]] In real systems, '
            'it is rarely one flat burst of calls. [[slnc 300]] It is '
            'usually a few waves. [[slnc 300]] What can be asked at once, '
            'and what must wait for the first answers.'
        ),
    ),
    dict(
        key="08-the-fanout",
        kind="code",
        title="One Call, Then Two Together",
        body="""Order order = orders.fetch(orderId);      // alone

Fanout fanout = new Fanout(clock, log);

Branch<Map<String, String>> names = fanout.add(
        "catalog", () -> catalog.namesFor(order.skus()));

Branch<DeliveryStatus> delivery = fanout.add(
        "shipping", () -> shipping.statusFor(orderId));

fanout.awaitAll();     // both left at the same moment""",
        narration=(
            'Here is that shape, in code. [[slnc 400]] The order is '
            'fetched first, on its own, because nothing else can start '
            'without it. [[slnc 500]] Then a fan-out is created. [[slnc '
            '300]] The two remaining calls are handed to it, each with a '
            'name. [[slnc 300]] Not called yet, just handed over. [[slnc '
            '500]] Catalog is given the job of naming the products on the '
            'order. [[slnc 300]] Shipping is given the job of looking up '
            'the delivery status. [[slnc 500]] Then one line says: wait '
            'for all of them. [[slnc 300]] The fan-out starts both jobs '
            'at the same moment. [[slnc 300]] And gives back a handle to '
            'each, called a branch. [[slnc 500]] Remember that word, '
            'branch. [[slnc 300]] The second half of this video is about '
            'what a branch does when its call fails.'
        ),
    ),
    dict(
        key="09-act-two",
        kind="console",
        title="Act Two — The Same Calls, Sent Together",
        body="""2. Orders first, then Catalog and Shipping together
  ord-3001  total £70.95
    SKU-KETTLE   Stainless Steel Kettle   x1  £34.99
    SKU-MUG      Blue Stoneware Mug       x4  £35.96
    delivery: Royal Mail, out for delivery
      0ms ->    30ms  Orders           OK
     30ms ->    90ms  Catalog          OK
     30ms ->   150ms  Shipping         OK
    150ms ->   150ms  Composer   GATHERED  2 calls, 0 failed

  the shopper waited 150ms: 30, then the slower of 60 and 120""",
        narration=(
            'Second demo: the same calls, sent together. [[slnc 400]] '
            'Orders still starts at zero, and returns at thirty '
            'milliseconds. [[slnc 300]] But now Catalog and Shipping both '
            'start at thirty, at the same instant. [[slnc 500]] Catalog '
            'returns at ninety. [[slnc 300]] Shipping returns at one '
            'hundred and fifty. [[slnc 300]] And the page is finished the '
            'moment the slower one arrives. [[slnc 500]] One hundred and '
            'fifty milliseconds, instead of two hundred and ten. [[slnc '
            '500]] And notice that nothing got faster. [[slnc 300]] '
            'Shipping still takes its full one hundred and twenty '
            'milliseconds. [[slnc 300]] What disappeared was the queuing. '
            '[[slnc 600]] So here is the easy half of the pattern, in one '
            'sentence. [[slnc 300]] Calls made one after another cost the '
            'total of their waiting times. [[slnc 300]] Calls sent '
            'together cost only the longest.'
        ),
    ),
    dict(
        key="10-roles",
        kind="diagram",
        title="Who Decides What",
        body=None,
        narration=(
            'There are four pieces, each with one job. [[slnc 500]] The '
            'composer builds the page. [[slnc 300]] It calls Orders '
            'first, then hands the other two calls to the fan-out. [[slnc '
            '300]] It is the only piece that knows anything about '
            'shopping. [[slnc 500]] The fan-out runs several jobs from '
            'the same starting moment. [[slnc 300]] It knows nothing '
            'about orders or parcels. [[slnc 300]] It gives back one '
            'branch for each job. [[slnc 500]] Each branch holds one of '
            'two things: an answer, or the failure that happened instead. '
            '[[slnc 500]] And then there are the three services, '
            'described by what they mean to this page. [[slnc 300]] '
            'Orders is required: without it, there is no page. [[slnc '
            '300]] Catalog is optional: without it, the page shows '
            'product codes instead of names. [[slnc 300]] Shipping is '
            'optional: without it, the delivery section says it cannot '
            'check. [[slnc 600]] That is the most important fact in this '
            'whole system. [[slnc 300]] And it appears nowhere in the '
            'types. [[slnc 300]] Only the composer knows which missing '
            'piece the page can live without.'
        ),
    ),
    dict(
        key="11-act-three",
        kind="console",
        title="Act Three — Shipping Stops Answering",
        body="""3. Shipping is down

  sequential: Shipping did not answer -- no page at all
      the order and the product names had already
      arrived. Both thrown away.

  composed:
  ord-3001  total £70.95
    SKU-KETTLE   Stainless Steel Kettle   x1  £34.99
    SKU-MUG      Blue Stoneware Mug       x4  £35.96
    delivery: unknown, we cannot check this right now
  missing: [delivery status]""",
        narration=(
            'Third demo: Shipping stops answering. [[slnc 400]] The same '
            'failure is given to both versions. [[slnc 500]] The '
            'three-line version fetches the order, which is fine. [[slnc '
            '300]] It gets the product names, which is fine. [[slnc 300]] '
            'Then it calls Shipping, and throws an error. [[slnc 500]] '
            'And look what is lost with it. [[slnc 300]] The order had '
            'already arrived. [[slnc 300]] The product names had already '
            'arrived. [[slnc 300]] Both were perfectly good, and both are '
            'thrown away. [[slnc 300]] The shopper gets an error page. '
            '[[slnc 600]] The composed version works differently. [[slnc '
            '300]] When one job in the fan-out fails, the error is '
            'caught, and kept on that branch. [[slnc 300]] Nothing else '
            'is disturbed. [[slnc 500]] Then the composer asks, one '
            'branch at a time: is this missing piece fatal? [[slnc 300]] '
            'For Shipping, no. [[slnc 500]] So the shopper still sees '
            'what they bought, how many, and what it cost. [[slnc 300]] '
            'And where the delivery section would be, the page says: '
            'unknown, we cannot check this right now. [[slnc 300]] At the '
            'bottom, the page lists delivery status as missing.'
        ),
    ),
    dict(
        key="12-name-the-gap",
        kind="quote",
        title="Name The Gap. Never Fill It In.",
        body=[
            "It would have been easy to write \"in transit\"",
            "instead of \"we cannot check this right now\".",
            "",
            "Nearly always true. Reads better. Nobody complains.",
            "",
            "Don't.",
            "",
            "A shopper told their parcel is in transit will",
            "not ring up about the one that never left.",
            "",
            "The page is allowed to say it does not know.",
            "It is not allowed to make something up.",
        ],
        narration=(
            'This part is worth arguing about in a code review. [[slnc '
            '500]] When Shipping is down, the page says: we cannot check '
            'this right now. [[slnc 300]] It would have been easy to '
            'write something else, like: in transit. [[slnc 500]] That is '
            'tempting. [[slnc 300]] It is nearly always true. [[slnc '
            '300]] It reads better, and looks less broken. [[slnc 500]] '
            "Don't do it. [[slnc 500]] A shopper told their parcel is in "
            'transit will never ring up about the parcel that never left '
            'the warehouse. [[slnc 300]] You have not made the page '
            'nicer. [[slnc 300]] You have hidden the one signal that '
            'something is wrong, from the only person who could notice. '
            '[[slnc 600]] The page is allowed to say it does not know. '
            '[[slnc 300]] It is not allowed to make something up. [[slnc '
            '500]] That is what the missing list is for. [[slnc 300]] '
            'Naming the gap is what makes a partial answer honest, not '
            'just convenient.'
        ),
    ),
    dict(
        key="13-act-four",
        kind="console",
        title="Act Four — And When Orders Is Down",
        body="""4. Orders is down

  composed: Orders did not answer
            -- and that is correct

  a page with no order on it is not a partial page,
  it is a blank one

  Catalog was never called: 0 calls""",
        narration=(
            'Fourth demo: Orders is down. [[slnc 400]] Degrading is not '
            'always the answer. [[slnc 500]] Orders stops answering. '
            '[[slnc 300]] And the composer does not degrade anything. '
            '[[slnc 300]] It throws an error, and the shopper gets an '
            'honest error page. [[slnc 500]] That is correct. [[slnc '
            '300]] A page with no order on it is not a partial page. '
            '[[slnc 300]] It is a blank one, with nothing honest to show. '
            '[[slnc 500]] And Catalog was never called at all. [[slnc '
            '300]] The failure happened before the fan-out even existed. '
            '[[slnc 500]] Knowing which piece is required is as much part '
            'of the pattern as knowing which can be missing. [[slnc 300]] '
            'A composer that treats everything as optional will one day '
            'show someone a page about nothing.'
        ),
    ),
    dict(
        key="14-act-five",
        kind="console",
        title="Act Five — Why Any Of This Matters",
        body="""5. what three dependencies do to availability

  each service up 99.900% -> 43.2 min down a month
  a page needing all three:
        99.700% -> 129.5 min down a month

  availabilities multiply. Three good services make
  a worse page than any of them.

  with only Orders required:
        99.900% -> 43.2 min down a month""",
        narration=(
            'Fifth demo, and this one is arithmetic. [[slnc 400]] It is '
            'the reason the second half of this pattern matters. [[slnc '
            '500]] Suppose each of the three services is up ninety-nine '
            'point nine percent of the time. [[slnc 300]] That is a '
            'genuinely good service: about forty-three minutes of '
            'downtime a month. [[slnc 500]] So how available is a page '
            'that needs all three? [[slnc 300]] Most people guess '
            'ninety-nine point nine. [[slnc 300]] It is not. [[slnc 500]] '
            'The page only works when all three are up at the same '
            'moment. [[slnc 300]] So the chances multiply together. '
            '[[slnc 300]] The result is ninety-nine point seven percent. '
            '[[slnc 300]] That is one hundred and twenty-nine minutes of '
            'downtime a month. [[slnc 300]] Over two hours. [[slnc 600]] '
            'Three services that each behaved perfectly have combined '
            'into a page that is worse than any one of them. [[slnc 500]] '
            'The fix is not better services. [[slnc 300]] The fix is '
            'needing fewer of them. [[slnc 500]] Once only Orders is '
            'required, the page works whenever Orders is up. [[slnc 300]] '
            'Back to forty-three minutes a month. [[slnc 300]] And the '
            'other outages cost a gap on the page, not the whole page.'
        ),
    ),
    dict(
        key="15-costs",
        kind="bullets",
        title="What It Costs",
        body=[
            "The page is only as fast as its slowest",
            "dependency: Shipping at 400ms makes it 430ms.",
            "",
            "One page view became three calls: 10,000 shoppers",
            "are 30,000 calls.",
            "",
            "Somebody must make a product decision per",
            "dependency — and revisit it whenever one is added,",
            "which is exactly when nobody does.",
            "",
            "And a page where everything is optional is a",
            "page that says nothing.",
        ],
        narration=(
            'Now the honest costs. [[slnc 500]] First, the page can never '
            'be faster than its slowest required service. [[slnc 300]] '
            'Sending calls together removed the adding up, but not the '
            'slowest one. [[slnc 300]] Slow Shipping down to four hundred '
            'milliseconds, and the page takes four hundred and thirty. '
            '[[slnc 500]] Second, the fan-out adds load. [[slnc 300]] One '
            'page view is now three calls. [[slnc 300]] Ten thousand '
            'shoppers become thirty thousand calls. [[slnc 500]] Third, '
            'and most expensive: someone must make a business decision '
            'for every single service. [[slnc 300]] Is it required, or '
            'optional? [[slnc 300]] And revisit it every time a service '
            'is added. [[slnc 300]] Which is exactly when nobody '
            'remembers. [[slnc 500]] And a page where everything is '
            'optional says nothing at all. [[slnc 500]] When the numbers '
            'stop working, the answer is to keep a ready-assembled copy '
            'of the data. [[slnc 300]] But that is a different pattern.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the one-line change",
            "that turns an optional dependency into a required one,",
            "and costs the page an hour of uptime a month.",
        ],
        narration=(
            "That's the A P I Composition pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Send '
            'independent calls together, and decide in advance which '
            'missing answers the page can live without, and never invent '
            'what you do not know. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 300]] It runs offline, with '
            'nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Find the '
            'line where the composer asks the Shipping branch for its '
            'answer. [[slnc 300]] Change it so a failure is thrown, '
            'instead of replaced. [[slnc 300]] Two tests will fail. '
            '[[slnc 300]] One line just turned an optional service into a '
            'required one, and cost the page an hour of uptime a month. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
