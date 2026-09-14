"""Scene definitions for the CQRS teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches, so no sentence points at the screen, the
departures board is described in full before any class name is spoken, and the
console slides are read out as a story about what a shopper saw rather than as
columns of numbers. The slides illustrate the narration; they never carry it.

Every number quoted here comes from the real output of `./gradlew run`: ninety
milliseconds and two service calls for one view of a page, five milliseconds
and no service calls for the same page afterwards, a rename that one copy hears
about and the other cannot, and a kettle that is sold once even though the fast
copy says there is still one on the shelf.

Scene order is the argument, and the middle of it is the part that matters.
Scenes five to eight take the cache seriously before taking it apart. A viewer
who thinks the cache was a straw man will hear the rest of the video as
marketing, so the pattern is not introduced until the obvious answer has been
shown working, and then shown to be a different thing.

Two scenes must not be cut or moved earlier. Scene twelve is the frame where an
order is placed, paid for and final, and the customer is looking at a page with
nothing on it -- a viewer who leaves thinking this pattern is free has learned
something worse than nothing. Scene fourteen is the rule with a price tag, and
the video exists as much for that rule as for the mechanism.

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
        title="CQRS",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the C Q R S pattern in "
            "Java — command query responsibility segregation — and it is "
            "written and presented by Jayasekhar Konduru. [[slnc 300]] Let's "
            "start with the simple definition. Changing something and reading "
            "something are two different jobs, so stop making them the same "
            "code path. The side that changes things announces what it did, and "
            "the side that answers questions keeps an answer already prepared. "
            "[[slnc 350]] That is all it says, and the mechanism is small enough "
            "to fit on one slide later on. [[slnc 300]] The rest of the video "
            "builds a real working Java project: an online shop, and one page — "
            "the order history page a shopper opens to see what they have "
            "bought. [[slnc 300]] We are going to build that page three "
            "different ways, and the middle one is the one that matters, "
            "because it is the answer almost everybody reaches for first, and "
            "it is not this pattern. [[slnc 350]] By the end I want you to be "
            "able to say the difference out loud without using the word fast."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Shop, And One Page",
        body=[
            "An online shop. A shopper opens their order history.",
            "",
            "Each line needs an order number, a product code, the",
            "product's name, and how many they bought.",
            "",
            "The order number and the code come from the orders",
            "service. The product's name comes from the catalog.",
            "",
            "So building that page means asking two services.",
            "",
            "One order is placed once. Its page is shown again,",
            "and again, and again.",
        ],
        narration=(
            "Here is the shop, and it is worth picturing before any code. "
            "[[slnc 300]] A shopper opens their order history page. Each line on "
            "it has an order number, a product code, the name of the product, "
            "and how many of them they bought. [[slnc 350]] Now, where do those "
            "things live? The order number and the product code live with the "
            "orders service, because that service is the one that took the "
            "order. The product's name lives with the catalog service, because "
            "that is the service that owns names. [[slnc 300]] So to build one "
            "line of that page, somebody has to ask two different services and "
            "stitch the answers together. That is a perfectly normal thing to do "
            "and it has a name — it is the A P I composition pattern, and there "
            "is a separate project about it. [[slnc 350]] Hold on to one more "
            "thing, because the whole video turns on it. An order is placed "
            "once. The page that shows it is opened by the customer, and then by "
            "the confirmation email, and then by a support agent, and then by "
            "the customer again next week. [[slnc 300]] The facts changed once. "
            "The page is built a thousand times."
        ),
    ),
    dict(
        key="03-every-view",
        kind="code",
        title="Composed On Every View",
        body="""// ComposingOrderHistory.historyFor(customerId)

List<Order> orders = ordersApi.ordersFor(customerId);

Set<String> skus = orders.stream()
        .map(Order::sku).collect(toSet());
Map<String, String> names = catalog.namesFor(skus);

return orders.stream()
        .map(o -> new OrderHistoryRow(
                o.orderId(), o.sku(),
                names.get(o.sku()), o.quantity()))
        .toList();""",
        narration=(
            "This is the first of our three versions, and I want to be generous "
            "about it, because it is good code. [[slnc 300]] It asks the orders "
            "service for this customer's orders. Then it collects every product "
            "code that appeared, and asks the catalog for all of those names in "
            "one single call — not one call per row, one call for the lot. Then "
            "it puts the two together into the finished rows. [[slnc 350]] There "
            "is no loop over the network. There is no duplicated work. Nobody "
            "would object to this in a code review, and I have never heard of "
            "anybody being paged about it. [[slnc 400]] And that is exactly why "
            "it survives for years. [[slnc 300]] Let's run it and see what it "
            "costs."
        ),
    ),
    dict(
        key="04-act-one",
        kind="console",
        title="Act One — Composing On Every View",
        body="""$ ./gradlew run

Act 1 - composing the page on every view
    80ms ->  110ms  Orders   OK   Order[orderId=ord-5001...
   110ms ->  170ms  Catalog  OK   {SKU-KETTLE=Stainless St...
   170ms ->  200ms  Orders   OK   ...
   200ms ->  260ms  Catalog  OK   ...
   260ms ->  290ms  Orders   OK   ...
   290ms ->  350ms  Catalog  OK   ...
  3 views cost 270ms and 6 service calls
  every view rebuilt a page identical to the last one""",
        narration=(
            "The shopper opens that page three times. [[slnc 300]] And the "
            "timeline shows what happened underneath. Ask orders, thirty "
            "milliseconds. Ask catalog, sixty milliseconds. Then ask orders "
            "again. Then catalog again. Then orders, then catalog. [[slnc 350]] "
            "Three views cost two hundred and seventy milliseconds and six "
            "service calls. [[slnc 400]] Now, before anybody says the word slow "
            "— ninety milliseconds for a page is not slow. Nobody is going to "
            "complain about that. [[slnc 350]] Two other things are wrong here, "
            "and they are both worse. [[slnc 300]] The first is the ratio. Every "
            "one of those three pages was identical to the one before it. "
            "Nothing had changed. The shop paid full price, three times, to "
            "produce the same answer. [[slnc 350]] The second is quieter and it "
            "is the one that gets people. Every single view is a live call to "
            "two other services. Which means a page about orders the customer "
            "has already paid for cannot be shown at all if the catalog service "
            "is having a bad afternoon. [[slnc 300]] The customer's own history "
            "depends on somebody else being up."
        ),
    ),
    dict(
        key="05-the-obvious-fix",
        kind="bullets",
        title="So Cache It",
        body=[
            "The page is the same every time. Keep it.",
            "",
            "First view: build it, store it, hand it over.",
            "Second view: hand over what we stored.",
            "",
            "Give it a five minute expiry, and build it again.",
            "",
            "This is a real cache, and it genuinely works.",
            "The second view really is free.",
            "",
            "So is that the pattern? No — and why not is the",
            "most useful thing in this video.",
        ],
        narration=(
            "So what do we do about it? [[slnc 300]] The answer that everybody "
            "reaches for, and I mean everybody, is: the page is the same every "
            "time, so keep it. Cache it. [[slnc 350]] The first view builds the "
            "page, stores it, and hands it over. The second view just hands over "
            "what was stored. Put a five minute expiry on it so it does not go "
            "stale forever, and move on. [[slnc 300]] And I want to be completely "
            "clear about this, because it is easy to set up a straw man here and "
            "I am not going to. This works. It is a real cache, the project has a "
            "real implementation of it, and the second view really is free. If "
            "you shipped that this afternoon, your page would get faster this "
            "afternoon. [[slnc 400]] So — is that C Q R S? [[slnc 350]] No. And "
            "the reason it is not is, I think, the single most useful idea in "
            "this whole video. Let's go and find it."
        ),
    ),
    dict(
        key="06-the-cache",
        kind="code",
        title="The Cache, Honestly",
        body="""// CachedOrderHistory
public static final long EXPIRY_MILLIS = 5 * 60 * 1000L;

List<OrderHistoryRow> historyFor(String customerId) {
    Entry cached = entries.get(customerId);
    if (cached != null && !expired(cached)) {
        hits++;
        return cached.rows();          // never re-checked
    }
    misses++;
    return store(composing.historyFor(customerId));
}""",
        narration=(
            "Here is the cache, and look at how little there is to it. "
            "[[slnc 300]] If we have rows for this customer, and they have not "
            "expired yet, hand them back. Otherwise go and compose the page "
            "properly, store the result, and hand that back. [[slnc 350]] Now ask "
            "yourself a question about those stored rows. Under what "
            "circumstances does that cache ever find out that what it is holding "
            "has become wrong? [[slnc 400]] And the answer is: none. There is no "
            "such circumstance. [[slnc 350]] It stored some rows. It does not "
            "understand them. Nothing in the shop has any way of reaching in and "
            "telling it that the world moved on. The only thing in the entire "
            "universe that will ever correct that copy is the clock running out. "
            "[[slnc 300]] The project has a test with that name — it is called "
            "it is corrected by a timer and nothing else. Let's watch that "
            "happen."
        ),
    ),
    dict(
        key="07-act-four",
        kind="console",
        title="Act Four — The Rename",
        body="""Act 4 - the cache that cannot know it is wrong
  Catalog renamed the kettle
  cache says:      Stainless Steel Kettle
  read model says: Brushed Steel Kettle
  the cache will keep saying that for 300 seconds,
  because nothing tells it otherwise
  the read model was corrected by the same event
  that made it wrong
  cache hits 1, misses 1""",
        narration=(
            "The catalog team renames a product. The stainless steel kettle "
            "becomes the brushed steel kettle. This is an ordinary Tuesday "
            "afternoon change and they are completely entitled to make it — it "
            "is their product and their name. [[slnc 350]] Now there are two "
            "fast copies of that page in this shop, and we ask both of them what "
            "the kettle is called. [[slnc 300]] The cache says stainless steel "
            "kettle. That is the old name. It is wrong. [[slnc 300]] The other "
            "copy says brushed steel kettle. That is right. [[slnc 400]] And here "
            "is the sentence I would like you to take away from this video, if "
            "you take away nothing else. [[slnc 350]] A cache is a copy that "
            "cannot know it is wrong. [[slnc 400]] That cache will go on "
            "confidently telling customers the old name for the next three "
            "hundred seconds, not because three hundred is a bad number, but "
            "because nothing in the shop has any route to tell it otherwise. "
            "[[slnc 350]] The other copy was corrected by the very same event "
            "that made it wrong. The rename arrived, and it updated itself. "
            "[[slnc 300]] So the difference between these two things is not "
            "speed. They are both fast. The difference is whether anybody can "
            "tell it."
        ),
    ),
    dict(
        key="08-cannot-know",
        kind="quote",
        title="A Copy That Is Told",
        body=[
            "A cache is a copy that cannot know it is wrong.",
            "Its only correction is an expiry.",
            "",
            "A read model is a copy that is told. The same event",
            "that makes it wrong is the one that corrects it.",
            "",
            "There is no expiry setting that turns the first",
            "into the second.",
            "",
            "Short expiry, and you threw away the saving.",
            "Long expiry, and you are wrong for longer.",
        ],
        narration=(
            "So let's put the two side by side properly. [[slnc 350]] A cache is "
            "a copy that cannot know it is wrong, and its only correction is an "
            "expiry. [[slnc 300]] A read model — and that is the name for the "
            "second copy — is a copy that is told. The same event that makes it "
            "wrong is the one that corrects it, and it is corrected the moment "
            "that event arrives rather than at some point in the next five "
            "minutes. [[slnc 400]] And notice that there is no expiry setting "
            "anywhere that turns the first thing into the second thing. This is "
            "structural, not a matter of configuration. [[slnc 350]] The project "
            "has a test called there is no free setting, and it makes the point "
            "with numbers. Set the expiry short and you have thrown away the "
            "saving you cached for in the first place. Set it long and you are "
            "confidently wrong for longer. You will tune that number forever and "
            "you will never win. [[slnc 400]] Now here is the question that "
            "actually invents this pattern, and it is worth pausing on. What "
            "would have to be true for the copy to know? [[slnc 400]] It would "
            "have to be told. [[slnc 300]] So: who would tell it?"
        ),
    ),
    dict(
        key="09-the-mechanism",
        kind="code",
        title="The Whole Mechanism",
        body="""// the write side announces what it did
Order order = new Order(...);
events.publish(new OrderPlaced(order));

// the read model listens, and composes once
void apply(ShopEvent event) {
    switch (event) {
        case OrderPlaced e   -> addRows(e);
        case ProductRenamed e -> rename(e);
        case StockChanged e  -> setStock(e);
    }
}""",
        narration=(
            "And this is the entire mechanism. I promised it would be small, and "
            "I would like you to find it slightly disappointing. [[slnc 350]] "
            "When the write side places an order, it does its work — and then it "
            "announces what it did. It publishes a fact: an order was placed. "
            "[[slnc 300]] Something is listening. When a fact arrives, it looks "
            "at what kind of fact it is and updates the rows it is holding. An "
            "order was placed, so add the rows for it. A product was renamed, so "
            "change that name everywhere it appears. The stock level changed, so "
            "record the new number. [[slnc 400]] That is it. A side that "
            "announces, and a side that listens and keeps a prepared answer. "
            "[[slnc 350]] One small detail is worth pointing out because it will "
            "save somebody a bad afternoon. The event type is a sealed type — "
            "which means there is a fixed, known list of the kinds of fact this "
            "shop can produce, and the compiler will refuse to build if somebody "
            "adds a fourth kind and forgets to teach this listener about it. "
            "[[slnc 300]] Without that, a projection quietly ignores facts it "
            "has never heard of, drifts away from the truth, and every test stays "
            "green."
        ),
    ),
    dict(
        key="10-act-two",
        kind="console",
        title="Act Two — The Page Kept Ready",
        body="""Act 2 - the page kept ready by the events
  ord-5001  SKU-KETTLE  Stainless Steel Kettle  x1  £34.99
  ord-5001  SKU-MUG     Blue Stoneware Mug      x4  £35.96
     80ms ->  85ms  ReadModel  SERVED  2 row(s), 0 others
     85ms ->  90ms  ReadModel  SERVED  2 row(s), 0 others
     90ms ->  95ms  ReadModel  SERVED  2 row(s), 0 others
  3 views cost 15ms and 0 service calls
  the work did not vanish: Catalog was called 1 time
  when the order was placed""",
        narration=(
            "Same customer, same page, same three views. [[slnc 300]] The page "
            "itself is identical — a kettle at thirty four ninety nine, four "
            "mugs at thirty five ninety six. That matters, because if the two "
            "versions produced different pages we would not be comparing "
            "anything. [[slnc 350]] Three views now cost fifteen milliseconds "
            "instead of two hundred and seventy. [[slnc 300]] But the number I "
            "actually want you to look at is the other one. Zero service calls. "
            "[[slnc 400]] Not fewer. Zero. Serving that page does not touch the "
            "orders service and does not touch the catalog. There is a test in "
            "the project called reads survive an outage, and it takes the orders "
            "service down completely and then renders the page anyway. The first "
            "version could never have done that, at any speed. [[slnc 400]] And "
            "now the honest line, which the demo prints itself, because I am not "
            "going to pretend work disappeared. [[slnc 350]] The work did not "
            "vanish. The catalog was still called once — when the order was "
            "placed. The composing happened. It just happened at write time "
            "instead of at read time. [[slnc 350]] Which is only a good trade "
            "because of the ratio we talked about at the start. A shop places one "
            "order and shows that page a thousand times. [[slnc 300]] Invert "
            "that ratio — something written constantly and read rarely — and "
            "this pattern is a straight loss. It is not free, it is funded, and "
            "the ratio is what funds it."
        ),
    ),
    dict(
        key="11-what-it-costs",
        kind="bullets",
        title="What You Are Actually Buying",
        body=[
            "Bought: reads that cost one lookup, and a page that",
            "renders when other services are down.",
            "",
            "Paid: work moved to write time, funded by the ratio",
            "of reads to writes.",
            "",
            "Paid: a second copy of the data to keep and to fix.",
            "",
            "Paid: a window where the copy is behind.",
            "",
            "That last one is not a detail. It is the thing",
            "that decides whether you can use this at all.",
        ],
        narration=(
            "So let's total it up honestly, because there is a bill. [[slnc 350]] "
            "What you bought: reads that cost a single lookup, and a page that "
            "still renders when other services are down. Those are both real and "
            "both large. [[slnc 350]] What you paid. First, the work moved to "
            "write time, and it is only affordable because you read far more "
            "often than you write. [[slnc 300]] Second, you now have a second "
            "copy of the data. Somebody has to keep it, and somebody has to fix "
            "it when it breaks. [[slnc 350]] And third — the one that decides "
            "whether you can use this pattern at all — there is now a window of "
            "time in which that copy is behind. [[slnc 400]] People tend to "
            "describe that window in a sentence and move on, which does it no "
            "justice at all. So instead, let's look at it."
        ),
    ),
    dict(
        key="12-act-three",
        kind="console",
        title="Act Three — The Window, Shown",
        body="""Act 3 - eventually consistent, shown honestly
  ord-5001 is placed, paid for, and final
  events still in flight: 3
  rows on the customer's order history page: 0

  the customer is looking at a page that does not
  have their order on it

  events delivered -> rows on the page: 2
  the window is however long delivery takes,
  and it closes by itself""",
        narration=(
            "Read those first three lines together, because this is the most "
            "uncomfortable frame in the project and it is in there on purpose. "
            "[[slnc 400]] The order is placed. It is paid for. It is final. "
            "[[slnc 300]] Three events are still in flight. [[slnc 300]] And the "
            "number of rows on the customer's order history page is zero. "
            "[[slnc 450]] The customer has just given this shop money, and they "
            "are looking at a page that does not have their order on it. "
            "[[slnc 400]] Nothing is broken. Nothing threw an exception. No test "
            "is failing. The facts are true and they simply have not arrived "
            "yet. [[slnc 350]] Two things make that survivable, and you need "
            "both of them. The window is short. And — this is the important one "
            "— it closes by itself. There is no operator, no retry button, no "
            "overnight cleanup job. The events arrive, and the page has two rows "
            "on it. [[slnc 400]] What is not optional is deciding, page by page, "
            "whether you can live with that window. An order history page, "
            "almost certainly yes. The screen a warehouse worker is packing "
            "boxes from — that is a much harder conversation, and you should "
            "have it before you build this, not after."
        ),
    ),
    dict(
        key="13-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let's put the whole cast in one place. [[slnc 350]] On one side is "
            "the design we are replacing: a page composed on every single view, "
            "asking the orders service and the catalog every time, at ninety "
            "milliseconds and two calls a go. And underneath it the cache — the "
            "tempting fix — which is fast and which nothing can correct except a "
            "timer. [[slnc 350]] The important thing about that cache is what is "
            "missing. Nothing connects it to the events. There is no arrow. It "
            "is not a subscriber, it is a box that remembers what it was handed, "
            "and that missing connection is the entire project. [[slnc 400]] On "
            "the other side is the split. The write service reserves stock from "
            "the ledger before it accepts anything, and that is where a sale is "
            "actually decided. It announces what it did. The bus carries three "
            "kinds of fact — an order was placed, a product was renamed, the "
            "stock changed. And the read model listens, and holds rows that are "
            "already assembled. [[slnc 350]] There is one more piece down there, "
            "and it is a genuine consolation: the read model can be rebuilt from "
            "the events. It is a derived thing. If you corrupt it, you throw it "
            "away and replay. [[slnc 400]] And underneath all of it is the one "
            "rule this pattern asks you to keep, which we are about to pay for."
        ),
    ),
    dict(
        key="14-act-five",
        kind="console",
        title="Act Five — The Last Kettle",
        body="""Act 5 - the last kettle
  read model still shows on the shelf: 1
  the ledger actually has: 0
  a second shopper arrives and the read model says yes
  the ledger refused: cannot reserve 1 of SKU-KETTLE,
                      only 0 left
  it was the write side that saved the shop,
  because the sale was decided there
  and a read model is throwaway:
  rebuilt from 6 events, 2 rows back""",
        narration=(
            "One kettle left in the shop. Somebody buys it. [[slnc 300]] For a "
            "moment, the fast copy still says there is one on the shelf, and the "
            "ledger — the actual number — says zero. That is the window again, "
            "and it is doing exactly what we just watched it do. [[slnc 350]] "
            "And in that moment, a second shopper arrives and tries to buy a "
            "kettle. [[slnc 400]] The page they are looking at says yes. "
            "[[slnc 350]] And the shop is fine — because the sale was not "
            "decided by the page. The sale went to the ledger, and the ledger "
            "refused: cannot reserve one, there are zero left. [[slnc 400]] So "
            "here is the rule, and it is the reason this video exists as much as "
            "the mechanism is. [[slnc 350]] Show a read model's number. Never "
            "decide anything with it. [[slnc 400]] Display the stock level, "
            "absolutely. Display the balance, display the entitlement. But the "
            "moment something is being allowed or refused — a sale, a payment, "
            "access to something — that decision goes to the side that owns the "
            "number. [[slnc 350]] And I have to be honest about what enforces "
            "that rule, because it is uncomfortable. Nothing does. Not the type "
            "system, not the compiler. A test, a code review, and people "
            "remembering. [[slnc 400]] One consolation to finish on, and it is a "
            "real one. If the read model is wrong, or corrupted, or you changed "
            "its shape — you throw it away. Six events replayed, two rows back. "
            "It is derived data, and derived data is never precious."
        ),
    ),
    dict(
        key="15-the-rule",
        kind="quote",
        title="What To Remember",
        body=[
            "Commands change things. Queries read things.",
            "They are different jobs.",
            "",
            "A cache is a copy that cannot know it is wrong.",
            "A read model is a copy that is told.",
            "",
            "The work moved to write time. It did not vanish,",
            "and the ratio of reads to writes is what funds it.",
            "",
            "The window is real, sometimes alarming, and it",
            "closes by itself.",
            "Show a read model's number. Never decide with it.",
        ],
        narration=(
            "Five things to carry away. [[slnc 350]] Commands change things, "
            "queries read things, and they are different jobs with different "
            "needs. [[slnc 300]] A cache is a copy that cannot know it is wrong; "
            "a read model is a copy that is told. That difference is structural, "
            "and it is not about speed. [[slnc 350]] The work moved to write "
            "time. It did not vanish, and the ratio of reads to writes is what "
            "pays for it — so if you read a thing rarely, do not do this. "
            "[[slnc 350]] The staleness window is real, it is occasionally "
            "alarming to look at, and the thing that makes it liveable is that "
            "it closes by itself. [[slnc 350]] And the rule. Show a read model's "
            "number. Never decide anything with it."
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the five tests that",
            "take the obvious cache seriously, and then take it apart,",
            "and the one that proves a sale is decided on the write side.",
        ],
        narration=(
            "That's C Q R S. [[slnc 250]] The full source, the written notes, "
            "the diagrams and an animated walkthrough are all in the repository, "
            "and everything runs offline with nothing installed but a Java "
            "development kit. [[slnc 300]] There is no message broker and no "
            "database in this project, and that is deliberate. A broker would "
            "add a container, a topic, and several minutes to every run, and it "
            "would teach you nothing about the actual subject — which is which "
            "copy is allowed to decide, and how each copy finds out it is wrong. "
            "[[slnc 350]] If you try one exercise, try this one. Change the "
            "second shopper so that it checks the read model's stock number and "
            "sells if that number says yes. Watch the test fail. And then sit "
            "with what that failure would have been in a real shop: a customer "
            "charged for a kettle that does not exist. [[slnc 400]] And then the "
            "harder question, which no exercise can answer for you. Take a page "
            "in a system you actually work on. Estimate how many times it is "
            "read for every time the facts behind it change. If that number is "
            "under about ten, ask yourself honestly whether a permanent second "
            "copy of the data is worth keeping. [[slnc 350]] Because the real "
            "lesson here is this. The mechanism is publish, listen, and keep an "
            "answer ready, and you already know how to write all three. "
            "Deciding which of your pages can tolerate being a few seconds "
            "behind, and holding the line that nothing is ever decided from the "
            "fast copy — that is the part that needs a person. [[slnc 300]] If "
            "this helped, a like genuinely does help other people find it, and "
            "subscribe if you would like the rest of the series. [[slnc 250]] "
            "Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
