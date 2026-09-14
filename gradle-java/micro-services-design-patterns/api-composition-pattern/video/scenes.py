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
            "Hello, and welcome. This video explains the API Composition "
            "pattern in Java, and it is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] Let's start with the simple definition. When "
            "one screen needs data that several different services own, you ask "
            "all of them, and you assemble the answer yourself. [[slnc 350]] "
            "That is it, and the mechanical half of it is a single sentence: "
            "calls made one after another cost the sum of their waiting times, "
            "while calls sent together cost only the longest one. [[slnc 300]] "
            "But there is a second half that most explanations leave out, and "
            "it is the harder half. For every service you ask, somebody has to "
            "have decided, in advance, whether the screen can be shown without "
            "it. [[slnc 300]] The rest of the video does both, by building a "
            "real working Java project: an online shop, and one perfectly "
            "ordinary page showing a shopper one of their orders. [[slnc 300]] "
            "By the end you'll know why that page takes two hundred and ten "
            "milliseconds when it could take a hundred and fifty; why sixty of "
            "those milliseconds buy absolutely nothing; why a failure in the "
            "last call throws away two perfectly good answers that had already "
            "arrived; and why three excellent services combine into a page that "
            "is worse than any one of them."
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
            "Here is the situation, and it is worth picturing before any code. "
            "[[slnc 300]] A shopper clicks on one of their past orders. The page "
            "that comes back shows the order reference at the top, then a line "
            "for each thing they bought — the name of it, how many, what it "
            "cost — then the total, and underneath all of that, where the parcel "
            "currently is. [[slnc 300]] You have seen this page a hundred times. "
            "It is completely unremarkable. [[slnc 350]] Except for one thing. "
            "Three different services own those facts. [[slnc 250]] The Orders "
            "service knows what was bought and what was paid. The Catalog "
            "service is the only thing that knows what a product code actually "
            "means, so it is the only thing that can turn sku dash kettle into "
            "stainless steel kettle. And the Shipping service is the only thing "
            "that knows which carrier has the parcel and where it has got to. "
            "[[slnc 350]] Each of those services has its own database, and none "
            "of them can see into the others. So there is no join any more. "
            "Nobody can write one query that produces this page. [[slnc 300]] "
            "Somebody has to ask all three, and put the answer together. That "
            "somebody is what this pattern is about."
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
            "So here is what everybody writes first, and it is three lines of "
            "entirely ordinary Java. [[slnc 300]] Fetch the order. Ask Catalog "
            "for the product names. Ask Shipping for the delivery status. Then "
            "assemble the page out of the three answers. [[slnc 350]] I want to "
            "be completely fair to this code, because it is going to be the "
            "villain of the next few minutes and it does not deserve to be. "
            "[[slnc 300]] There is no bug in it. It is easy to read. It returns "
            "exactly the right page. Every test written against it passes. "
            "[[slnc 250]] And a code review waves it through without a single "
            "comment — because the cost of this code is not in the code at all. "
            "[[slnc 350]] Let's run it, and watch the clock."
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
            "Read the left-hand column, because that is the whole story. "
            "[[slnc 300]] The call to Orders leaves at zero and comes back at "
            "thirty. The call to Catalog leaves at thirty and comes back at "
            "ninety. The call to Shipping leaves at ninety and comes back at "
            "two hundred and ten. [[slnc 300]] Thirty, plus sixty, plus a "
            "hundred and twenty. The shopper waited two hundred and ten "
            "milliseconds, and every one of those milliseconds is one of the "
            "three services taking its turn. [[slnc 350]] Now here is the "
            "question I would like you to sit with for a second, and it is the "
            "question this whole first half turns on. [[slnc 250]] Which of "
            "those three calls actually needed the answer from the one before "
            "it?"
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
            "Let's answer it. [[slnc 300]] Catalog genuinely had to wait. To "
            "look up product names it has to be told which product codes you "
            "mean, and the only thing that knows which products are on this "
            "order is the order itself. So that call could not have gone any "
            "earlier. [[slnc 350]] But look at Shipping. What does Shipping "
            "actually need in order to answer? One thing. The order id. "
            "[[slnc 300]] And the order id is what the shopper clicked on. It "
            "was available before we made a single call. Certainly by thirty "
            "milliseconds. [[slnc 350]] So the call to Shipping sat and waited "
            "sixty milliseconds for Catalog's answer, and then never so much as "
            "glanced at it. [[slnc 300]] Sixty milliseconds of a shopper's life, "
            "spent on nothing at all. [[slnc 250]] And nobody could have caught "
            "that in a code review, because there is nothing wrong with any of "
            "those three lines. That is simply what a sequence of statements "
            "does. It does them in sequence. [[slnc 300]] Which is exactly why "
            "nobody ever notices the day a page got slower."
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
            "Forget software for thirty seconds. You want a sandwich. "
            "[[slnc 300]] And there is no shop that sells the finished thing, so "
            "you need bread from the baker, tomatoes from the grocer, and cheese "
            "from the deli. [[slnc 350]] Two things follow immediately, and "
            "between them they are the entire pattern. [[slnc 300]] First: go to "
            "all three at once. If you walk to the baker, come home, walk to the "
            "grocer, come home, walk to the deli, come home — lunch takes three "
            "trips. Send three people at the same time and lunch takes one trip, "
            "the longest one. [[slnc 300]] Notice what did not happen there. No "
            "shop got any faster. You simply stopped waiting for one before "
            "starting the next. [[slnc 350]] Second, and this is the one people "
            "skip: decide now, before you leave the house, what happens if a "
            "shop is shut. [[slnc 300]] No bread means no sandwich. That is not "
            "a partial lunch, it is no lunch. No tomatoes means a sandwich "
            "without tomatoes, which is fine — as long as you do not tell "
            "anybody there were tomatoes on it. [[slnc 350]] That second "
            "decision is the difficult one, it has nothing whatsoever to do with "
            "programming, and it has to be made before you get to the shops. "
            "[[slnc 300]] I would rather you remembered the sandwich than any of "
            "the class names coming up."
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
            "So the fix is to stop waiting. But be careful about how far that "
            "goes, because there is a tempting version of it that is wrong. "
            "[[slnc 300]] The tempting version is: send all three calls at zero "
            "milliseconds. [[slnc 250]] This page cannot do that. Catalog has to "
            "be told which product codes to look up, and the only thing that "
            "knows them is the order. [[slnc 350]] So the real shape is one "
            "call, and then two together. Fetch the order on its own; then send "
            "Catalog and Shipping off at the same instant. [[slnc 300]] And this "
            "is where I would push back on the phrase just parallelise it, "
            "because working out which calls genuinely depend on which is most "
            "of the job. [[slnc 300]] In a real system the honest answer is "
            "almost never one flat burst of calls. It is a couple of waves: "
            "here is what we can ask immediately, here is what we can only ask "
            "once the first answers come back. [[slnc 350]] Drawing that "
            "dependency out — on paper, before writing anything — is the part "
            "worth doing slowly."
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
            "Here is that shape as code. [[slnc 300]] The order is fetched "
            "first, on its own, because nothing else can start without it. "
            "[[slnc 250]] Then a fan-out is created, and the two remaining calls "
            "are handed to it — not called, handed over. Each one is given a "
            "name and a piece of work that has not been run yet. [[slnc 300]] "
            "Catalog is given the job of naming the product codes from the "
            "order. Shipping is given the job of looking up the delivery status "
            "for the order id. [[slnc 350]] And then one line says: wait for "
            "all of them. [[slnc 300]] The fan-out runs both pieces of work from "
            "the same starting moment, and hands back a handle to each — which "
            "the code calls a branch. Hold on to that word, because the second "
            "half of this video is entirely about what a branch does when its "
            "call fails. [[slnc 300]] For now, let's just run it and look at the "
            "clock again."
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
            "One column changed, and it is the left one. [[slnc 300]] Orders "
            "still leaves at zero and comes back at thirty. But now Catalog "
            "leaves at thirty — and so does Shipping. They departed at the same "
            "instant. [[slnc 300]] Catalog comes back at ninety. Shipping comes "
            "back at a hundred and fifty. And the page is finished the moment "
            "the slower of the two lands. [[slnc 350]] A hundred and fifty "
            "milliseconds, instead of two hundred and ten. [[slnc 300]] And "
            "notice what did not happen. Nothing got faster. Shipping still "
            "takes its full hundred and twenty milliseconds, exactly as before. "
            "What went away is the queuing. [[slnc 350]] So here is the whole "
            "mechanical content of this pattern, in one sentence, and it is "
            "worth memorising. [[slnc 250]] Calls made one after another cost "
            "the sum of their waiting times. Calls sent together cost the "
            "maximum. [[slnc 300]] And the sixty milliseconds we got back are "
            "precisely the sixty that Shipping used to spend waiting for an "
            "answer it never used."
        ),
    ),
    dict(
        key="10-roles",
        kind="diagram",
        title="Who Decides What",
        body=None,
        narration=(
            "Let me name the pieces, because there are only four that matter "
            "and each one has exactly one job. [[slnc 300]] The composer is the "
            "thing that builds the page. It calls Orders first, alone, and then "
            "hands the other two calls to the fan-out. It is the only piece that "
            "knows anything about shopping. [[slnc 350]] The fan-out runs "
            "several pieces of work from the same starting moment. It has never "
            "heard of orders, or parcels, or money. It takes named work, runs "
            "it, and hands back a handle to each one. [[slnc 300]] Each of those "
            "handles is a branch, and a branch holds one of two things: an "
            "answer, or the failure that happened instead. [[slnc 350]] And then "
            "the three services, described not by what they do but by what they "
            "mean to this page. [[slnc 300]] Orders is required. Without it "
            "there is no page. Catalog is optional: without it the page shows "
            "product codes instead of product names. Shipping is optional: "
            "without it the delivery section says it cannot check. [[slnc 350]] "
            "That is the most important fact about this whole system, and I want "
            "you to notice something uncomfortable about it. It appears nowhere "
            "in the types. Nothing in the compiler knows that Shipping is "
            "optional. [[slnc 300]] The fan-out certainly does not — it parks "
            "every failure and judges none of them. Only the composer can know "
            "which absence the page can live with."
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
            "Now the same outage, given to both versions. Shipping has stopped "
            "answering. [[slnc 300]] The three-line version fetches the order — "
            "fine. Gets the product names — fine. Calls Shipping, and throws. "
            "[[slnc 250]] And look at what goes down with it. The order had "
            "already arrived. The product names had already arrived. Both of "
            "them, sitting in local variables, perfectly good. Both thrown away. "
            "[[slnc 350]] The shopper is shown an error page that was assembled "
            "out of two entirely correct answers that nobody ever looked at. "
            "[[slnc 300]] The composed version does something different, and the "
            "mechanism is four lines. Each piece of work in the fan-out runs "
            "inside a try, and when one throws, the exception is caught and "
            "parked on that branch instead of being allowed to escape. Nothing "
            "else is disturbed. [[slnc 350]] Which lets the composer ask, "
            "afterwards, one branch at a time: is this particular absence fatal? "
            "[[slnc 300]] For Shipping, no. So the shopper still sees what they "
            "bought, how many, and what it cost — because none of that was ever "
            "Shipping's to know. And where the delivery section would be, the "
            "page says: unknown, we cannot check this right now. [[slnc 300]] "
            "And then, at the bottom, the page lists delivery status as missing. "
            "That list matters more than it looks, and the next slide is about "
            "why."
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
            "This is the part worth arguing about in a review, and it is the "
            "reason I made this video. [[slnc 350]] When Shipping is down, the "
            "page says: we cannot check this right now. [[slnc 300]] It would "
            "have been very easy to write something else there. In transit. "
            "[[slnc 250]] Think about how attractive that is. It is nearly "
            "always true. It reads better. It looks less broken. Nobody "
            "complains about it. [[slnc 350]] Don't. [[slnc 300]] A shopper who "
            "is told their parcel is in transit will not ring up about the "
            "parcel that never left the warehouse. You have not made the page "
            "nicer. You have taken away the one signal that something is wrong, "
            "from the only person who was in a position to notice. [[slnc 350]] "
            "The page is allowed to say it does not know. It is not allowed to "
            "make something up. [[slnc 300]] And the same rule applies to the "
            "whole page, which is what that missing list is for. A page that "
            "quietly drops the delivery section when Shipping is down looks "
            "exactly like a page for an order that has not shipped yet, and the "
            "shopper cannot tell those two things apart. [[slnc 350]] Naming the "
            "gap is what makes a partial answer honest rather than merely "
            "convenient. [[slnc 300]] There is a test in this project whose "
            "entire job is to stop somebody being helpful here."
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
            "Now the classification working in the other direction, because it "
            "would be easy to come away from this thinking that degrading is "
            "always the answer. [[slnc 300]] Orders has stopped answering. And "
            "the composer does not degrade anything at all. It throws, and the "
            "shopper gets an honest error page. [[slnc 350]] That is correct. It "
            "is not a gap in the pattern and it is not laziness. A page with no "
            "order on it is not a partial page — it is a blank one. There is "
            "nothing honest to show. [[slnc 300]] And notice the last line. "
            "Catalog was never called. Zero calls. Because the failure happened "
            "before the fan-out even existed, nothing else was troubled at all. "
            "[[slnc 350]] Being able to say this one is required is as much a "
            "part of the pattern as being able to degrade. [[slnc 300]] A "
            "composer that degrades everything is a composer that will "
            "eventually show somebody a page about nothing."
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
            "Last act, and this one is arithmetic rather than code. It is also "
            "the reason the second half of this video exists. [[slnc 350]] "
            "Suppose each of these three services is up ninety-nine point nine "
            "percent of the time. That is a genuinely good service — about "
            "forty-three minutes of downtime in a month. [[slnc 300]] So how "
            "available is a page that needs all three? [[slnc 350]] Most people "
            "say ninety-nine point nine. It is not. [[slnc 300]] The page works "
            "only when all three services are up at the same moment, and "
            "probabilities of independent things all holding at once get "
            "multiplied together. Ninety-nine point nine percent, three times "
            "over, is ninety-nine point seven. [[slnc 300]] Which is a hundred "
            "and twenty-nine minutes of downtime a month. Over two hours. "
            "[[slnc 350]] Sit with that for a second. Three services that each "
            "behaved impeccably have combined into a page that is worse than "
            "any one of them, because their outages mostly do not overlap. "
            "[[slnc 300]] So how do you fix it? Make the services better? "
            "[[slnc 250]] There is no realistic amount of engineering that takes "
            "three separate teams from ninety-nine point nine to ninety-nine "
            "point nine seven. [[slnc 300]] The fix is needing fewer of them. "
            "[[slnc 350]] And that is exactly what the required-and-optional "
            "decision bought us. Once only Orders is required, the page renders "
            "whenever Orders is up — back to forty-three minutes — and the other "
            "two outages cost a gap on the page instead of the page."
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
            "Let's be honest about the bill, because this pattern is not free. "
            "[[slnc 300]] First, the page can never be faster than its slowest "
            "dependency. Parallelism removed the addition; it did not remove the "
            "maximum. There is a test in the project that slows Shipping to four "
            "hundred milliseconds, and the page immediately costs four hundred "
            "and thirty. No rearranging of calls will beat that while Shipping "
            "is on the critical path. [[slnc 350]] Second, the fan-out is load. "
            "One page view just became three calls. Ten thousand shoppers "
            "became thirty thousand calls, and Catalog now has to be sized for "
            "traffic it never used to see. [[slnc 300]] Third, and this is the "
            "expensive one: somebody has to make a product decision for every "
            "single dependency. That is real work, it does not compress into a "
            "configuration file, and it has to be revisited every time a new "
            "dependency is added — which is precisely the moment nobody "
            "remembers to. [[slnc 350]] And there is a limit to how much of a "
            "page can honestly be optional. A page where everything is optional "
            "is a page that says nothing. [[slnc 300]] When the timing or the "
            "arithmetic stops working — six services, or one that is "
            "unavoidably slow, or a page read a thousand times more often than "
            "the data changes — then the answer is to stop assembling on demand "
            "and keep a copy that is already assembled. But that is a different "
            "pattern, not a failure of this one."
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
            "That's API composition. [[slnc 250]] The full source, the written "
            "notes, the diagrams and an animated walkthrough are all in the "
            "repository, and everything runs offline with nothing installed but "
            "a Java development kit. There is no network in this project, and "
            "no threads either — the fan-out winds a fake clock backwards "
            "between calls, which produces exactly the timeline real parallel "
            "calls would produce, with nothing to reason about concurrently. "
            "[[slnc 300]] If you try one exercise, try this one. Find the line "
            "where the composer asks its shipping branch for a value, and change "
            "it from the version that substitutes a fallback to the version that "
            "rethrows. [[slnc 300]] Two tests go red, and that is the point: one "
            "line just turned an optional dependency into a required one, and "
            "cost the page an hour of uptime a month. Then ask yourself whether "
            "a code review would have caught it. [[slnc 350]] And then sit with "
            "the harder question, the one no exercise can answer. Somewhere in "
            "the system you work on, there is a screen that shows something "
            "reassuring when a service behind it is down. [[slnc 300]] Is what "
            "it says true? [[slnc 350]] Because that is the real lesson here. "
            "Sending the calls together is arithmetic, and you now know it: sum "
            "versus maximum. Deciding what the page may do without, and refusing "
            "to invent what you do not know, is the part that needs a person. "
            "[[slnc 300]] If this helped, a like genuinely does help other "
            "people find it, and subscribe if you would like the rest of the "
            "series. [[slnc 250]] Thanks for watching, and I'll see you in the "
            "next one."
        ),
    ),
]
