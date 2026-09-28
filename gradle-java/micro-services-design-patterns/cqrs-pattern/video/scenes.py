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
            'Hello, and welcome. [[slnc 400]] This video explains the C Q '
            'R S pattern, in Java. [[slnc 300]] C Q R S stands for '
            'command query responsibility segregation. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Changing something '
            'and reading something are two different jobs. [[slnc 300]] '
            'So stop making them the same code. [[slnc 300]] The side '
            'that changes things announces what it did. [[slnc 300]] And '
            'the side that answers questions keeps an answer already '
            'prepared. [[slnc 600]] Think of a restaurant. [[slnc 300]] '
            'The kitchen cooks the food. [[slnc 300]] But the menu board '
            'by the door is kept up to date separately, so guests can '
            'read it without asking the chef. [[slnc 700]] In our online '
            'store, we look at one page: the order history page, where a '
            'shopper sees what they have bought. [[slnc 500]] We build '
            'that page three ways. [[slnc 300]] The middle way is the '
            'answer almost everybody reaches for first. [[slnc 300]] And '
            'it is not this pattern. [[slnc 500]] By the end, you will be '
            'able to explain the difference without using the word fast.'
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
            'Here is the shop. [[slnc 400]] A shopper opens their order '
            'history page. [[slnc 300]] Each line shows an order number, '
            "a product code, the product's name, and how many they "
            'bought. [[slnc 600]] Where does that information live? '
            '[[slnc 300]] The order number and product code live in the '
            'orders service, which took the order. [[slnc 300]] The '
            "product's name lives in the catalog service, which owns "
            'names. [[slnc 500]] So to build one line, someone has to ask '
            'two services, and join the answers together. [[slnc 300]] '
            'That is normal, and it has its own name: the A P I '
            'Composition pattern. [[slnc 600]] Now remember one more '
            'thing, because the whole video turns on it. [[slnc 300]] An '
            'order is placed once. [[slnc 300]] But the page that shows '
            'it is opened by the customer, by the confirmation email, by '
            'a support agent, and by the customer again next week. [[slnc '
            '500]] The facts changed once. [[slnc 300]] The page is built '
            'a thousand times.'
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
            'Here is the first version, and it is good code. [[slnc 400]] '
            "It asks the orders service for this customer's orders. "
            '[[slnc 300]] Then it collects every product code. [[slnc '
            '300]] And it asks the catalog for all the names in one '
            'single call, not one call per line. [[slnc 300]] Then it '
            'joins the two into finished lines. [[slnc 500]] There is no '
            'wasted work. [[slnc 300]] Nobody would object to this in a '
            'code review. [[slnc 500]] And that is exactly why it '
            "survives for years. [[slnc 300]] Let's run it, and see what "
            'it costs.'
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
            'The shopper opens the page three times. [[slnc 400]] '
            'Underneath, each view asks the orders service, which takes '
            'thirty milliseconds. [[slnc 300]] Then asks the catalog, '
            'which takes sixty. [[slnc 300]] And the same again, for '
            'every view. [[slnc 500]] Three views cost two hundred and '
            'seventy milliseconds, and six service calls. [[slnc 600]] '
            'Now, ninety milliseconds per page is not slow. [[slnc 300]] '
            'Nobody will complain about that. [[slnc 300]] Two other '
            'things are wrong, and both are worse. [[slnc 500]] The first '
            'is waste. [[slnc 300]] All three pages were identical. '
            '[[slnc 300]] Nothing had changed. [[slnc 300]] The shop paid '
            'full price, three times, for the same answer. [[slnc 500]] '
            'The second is quieter. [[slnc 300]] Every view is a live '
            'call to two other services. [[slnc 300]] So if the catalog '
            'service is having a bad afternoon, the page cannot be shown '
            "at all. [[slnc 300]] The customer's own history depends on "
            'somebody else being up.'
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
            'So what do we do? [[slnc 400]] The answer almost everybody '
            'reaches for is this. [[slnc 300]] The page is the same every '
            'time, so keep a copy. [[slnc 300]] Cache it. [[slnc 500]] '
            'The first view builds the page, stores it, and hands it '
            'over. [[slnc 300]] The second view just hands over what was '
            'stored. [[slnc 300]] Add a five-minute expiry, so it does '
            'not stay out of date forever. [[slnc 500]] And to be clear, '
            'this works. [[slnc 300]] It is a real cache, and the second '
            'view really is free. [[slnc 500]] So, is that C Q R S? '
            '[[slnc 400]] No. [[slnc 300]] And the reason why is the most '
            'useful idea in this video.'
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
            'Here is the cache, and there is very little to it. [[slnc '
            '400]] If there are stored lines for this customer, and they '
            'have not expired, hand them back. [[slnc 300]] Otherwise, '
            'build the page properly, store it, and hand it back. [[slnc '
            '600]] Now ask one question about those stored lines. [[slnc '
            '300]] How would this cache ever find out that what it holds '
            'has become wrong? [[slnc 500]] The answer is: it never '
            'would. [[slnc 500]] It stored some lines, but it does not '
            'understand them. [[slnc 300]] Nothing in the shop can tell '
            'it that the world has moved on. [[slnc 300]] The only thing '
            'that will ever correct it is the clock running out. [[slnc '
            "500]] Let's watch that happen."
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
            'The catalog team renames a product. [[slnc 300]] The '
            'Stainless Steel Kettle becomes the Brushed Steel Kettle. '
            '[[slnc 300]] That is an ordinary change, and they are '
            'entitled to make it. [[slnc 600]] Now there are two fast '
            'copies of the page in this shop. [[slnc 300]] We ask both '
            'what the kettle is called. [[slnc 500]] The cache says: '
            'Stainless Steel Kettle. [[slnc 300]] That is the old name, '
            'and it is wrong. [[slnc 500]] The other copy says: Brushed '
            'Steel Kettle. [[slnc 300]] That is right. [[slnc 600]] Here '
            'is the sentence to take away from this video. [[slnc 300]] A '
            'cache is a copy that cannot know it is wrong. [[slnc 600]] '
            'That cache will keep showing the old name for the next five '
            'minutes. [[slnc 300]] Not because five minutes is a bad '
            'number. [[slnc 300]] But because nothing in the shop can '
            'tell it otherwise. [[slnc 500]] The other copy was corrected '
            'by the same event that made it wrong. [[slnc 300]] The '
            'rename arrived, and it updated itself. [[slnc 500]] So the '
            'difference is not speed. [[slnc 300]] Both are fast. [[slnc '
            '300]] The difference is whether anybody can tell it.'
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
            "Let's put the two side by side. [[slnc 400]] A cache is a "
            'copy that cannot know it is wrong. [[slnc 300]] Its only '
            'correction is an expiry. [[slnc 500]] The second copy is '
            'called a read model. [[slnc 300]] A read model is a copy '
            'that is told. [[slnc 300]] The same event that makes it '
            'wrong is the one that corrects it. [[slnc 300]] At once, not '
            'sometime in the next five minutes. [[slnc 600]] And no '
            'expiry setting can turn the first into the second. [[slnc '
            '300]] Set the expiry short, and you lose the saving you '
            'wanted. [[slnc 300]] Set it long, and you are wrong for '
            'longer. [[slnc 300]] You can tune that number forever, and '
            'never win. [[slnc 600]] So here is the question that leads '
            'to this pattern. [[slnc 300]] What would have to be true for '
            'the copy to know? [[slnc 500]] It would have to be told. '
            '[[slnc 300]] So, who would tell it?'
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
            'Here is the whole mechanism, and it is small. [[slnc 500]] '
            'When the write side places an order, it does its work. '
            '[[slnc 300]] Then it announces what it did. [[slnc 300]] It '
            'publishes a fact, called an event: an order was placed. '
            '[[slnc 600]] Something is listening: the read model. [[slnc '
            '300]] When a fact arrives, it updates the lines it holds. '
            '[[slnc 300]] An order was placed, so add its lines. [[slnc '
            '300]] A product was renamed, so change that name everywhere. '
            '[[slnc 300]] The stock changed, so record the new number. '
            '[[slnc 600]] That is all. [[slnc 300]] One side announces. '
            '[[slnc 300]] The other side listens, and keeps a prepared '
            'answer. [[slnc 600]] One small detail saves real trouble. '
            '[[slnc 300]] The list of event types is fixed, and Java '
            'knows it. [[slnc 300]] So if someone adds a fourth kind of '
            'event, and forgets to teach the listener, the code will not '
            'compile. [[slnc 300]] Without that, the read model would '
            'quietly ignore new facts, drift away from the truth, and '
            'every test would still pass.'
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
            'Same customer, same page, same three views. [[slnc 400]] The '
            'page itself is identical. [[slnc 300]] A kettle at '
            'thirty-four pounds ninety-nine, and four mugs at thirty-five '
            'pounds ninety-six. [[slnc 600]] Three views now cost fifteen '
            'milliseconds, instead of two hundred and seventy. [[slnc '
            '300]] But the more important number is this one. [[slnc '
            '300]] Zero service calls. [[slnc 500]] Not fewer. [[slnc '
            '200]] Zero. [[slnc 300]] Showing the page touches neither '
            'the orders service nor the catalog. [[slnc 300]] One test '
            'switches the orders service off completely, and the page '
            'still shows. [[slnc 300]] The first version could never do '
            'that, at any speed. [[slnc 600]] Now, to be honest, the work '
            'did not vanish. [[slnc 300]] The catalog was still called '
            'once, when the order was placed. [[slnc 300]] The joining '
            'still happened. [[slnc 300]] It just happened when writing, '
            'not when reading. [[slnc 600]] That is only a good trade '
            'because of the ratio from the start. [[slnc 300]] One order '
            'is placed, and the page is shown a thousand times. [[slnc '
            '300]] If something is written constantly and read rarely, '
            'this pattern is a loss.'
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
            "So let's add up the bill. [[slnc 400]] What you bought. "
            '[[slnc 300]] Reads that cost one lookup. [[slnc 300]] And a '
            'page that still works when other services are down. [[slnc '
            '600]] What you paid. [[slnc 300]] First, the work moved to '
            'write time. [[slnc 300]] It is only affordable because you '
            'read far more often than you write. [[slnc 500]] Second, you '
            'now have a second copy of the data. [[slnc 300]] Somebody '
            'has to keep it, and fix it when it breaks. [[slnc 500]] And '
            'third, the one that decides whether you can use this pattern '
            'at all. [[slnc 300]] There is now a window of time in which '
            "that copy is behind. [[slnc 500]] Let's look at that window."
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
            'This is the most uncomfortable moment in the project, and it '
            'is here on purpose. [[slnc 500]] An order is placed. [[slnc '
            '300]] It is paid for. [[slnc 300]] It is final. [[slnc 500]] '
            'Three events are still on their way. [[slnc 300]] And the '
            "customer's order history page shows no lines at all. [[slnc "
            '600]] The customer has just given this shop money. [[slnc '
            '300]] And they are looking at a page without their order on '
            'it. [[slnc 500]] Nothing is broken. [[slnc 300]] No error '
            'was raised. [[slnc 300]] The facts are true. [[slnc 300]] '
            'They just have not arrived yet. [[slnc 600]] Two things make '
            'this acceptable, and you need both. [[slnc 300]] The window '
            'is short. [[slnc 300]] And it closes by itself. [[slnc 300]] '
            'No operator, no retry button, no overnight job. [[slnc 300]] '
            'The events arrive, and the page shows two lines. [[slnc '
            '600]] So decide, page by page, whether you can live with '
            'that window. [[slnc 300]] For an order history page, almost '
            'certainly yes. [[slnc 300]] For the screen a warehouse '
            'worker packs boxes from, that is a much harder question. '
            '[[slnc 300]] Ask it before you build, not after.'
        ),
    ),
    dict(
        key="13-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            'Here are all the pieces, in one place. [[slnc 500]] On one '
            'side is the design we are replacing. [[slnc 300]] A page '
            'built on every single view, asking two services every time. '
            '[[slnc 300]] And beside it, the cache: fast, but corrected '
            'only by a timer. [[slnc 500]] What matters about the cache '
            'is what is missing. [[slnc 300]] Nothing connects it to the '
            'events. [[slnc 300]] It does not listen. [[slnc 300]] It '
            'only remembers what it was handed. [[slnc 600]] On the other '
            'side is the split. [[slnc 300]] The write service first '
            'reserves stock from the ledger, the true record of stock. '
            '[[slnc 300]] That is where a sale is really decided. [[slnc '
            '300]] Then it announces what it did. [[slnc 500]] The events '
            'carry three kinds of fact. [[slnc 300]] An order was placed. '
            '[[slnc 200]] A product was renamed. [[slnc 200]] The stock '
            'changed. [[slnc 500]] And the read model listens, and holds '
            'lines that are already put together. [[slnc 600]] One more '
            'comfort. [[slnc 300]] The read model can be rebuilt from the '
            'events. [[slnc 300]] If it breaks, you throw it away, and '
            'replay the events.'
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
            'There is one kettle left in the shop. [[slnc 300]] Somebody '
            'buys it. [[slnc 500]] For a moment, the read model still '
            'says one is on the shelf. [[slnc 300]] But the ledger, the '
            'true number, says zero. [[slnc 300]] That is the window '
            'again. [[slnc 600]] At that moment, a second shopper tries '
            'to buy a kettle. [[slnc 300]] The page they see says yes. '
            '[[slnc 500]] And the shop is still fine. [[slnc 300]] '
            'Because the page did not decide the sale. [[slnc 300]] The '
            'sale went to the ledger. [[slnc 300]] And the ledger '
            'refused: there are none left. [[slnc 600]] So here is the '
            "rule. [[slnc 300]] Show a read model's number. [[slnc 300]] "
            'Never decide anything with it. [[slnc 500]] Show the stock '
            'level, the balance, or what someone is allowed. [[slnc 300]] '
            'But when something is being allowed or refused, a sale, a '
            'payment, or access, ask the side that owns the number. '
            '[[slnc 600]] And to be honest, nothing enforces that rule. '
            '[[slnc 300]] Not the compiler. [[slnc 300]] Only a test, a '
            'code review, and people remembering. [[slnc 600]] One real '
            'comfort to finish. [[slnc 300]] If the read model is wrong, '
            'or broken, you throw it away. [[slnc 300]] Six events are '
            'replayed, and the two lines come back.'
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
            'Here are five things to remember. [[slnc 500]] One. [[slnc '
            '200]] Commands change things, and queries read things. '
            '[[slnc 300]] They are different jobs. [[slnc 400]] Two. '
            '[[slnc 200]] A cache is a copy that cannot know it is wrong. '
            '[[slnc 300]] A read model is a copy that is told. [[slnc '
            '400]] Three. [[slnc 200]] The work moved to write time. '
            '[[slnc 300]] It did not vanish. [[slnc 300]] So if something '
            'is rarely read, do not do this. [[slnc 400]] Four. [[slnc '
            '200]] The window where the copy is behind is real. [[slnc '
            '300]] It is only acceptable because it closes by itself. '
            "[[slnc 400]] Five. [[slnc 200]] Show a read model's number. "
            '[[slnc 300]] Never decide anything with it.'
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
            "That's the C Q R S pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] A cache is a copy '
            'that cannot know it is wrong, a read model is a copy that is '
            'told, and nothing is ever decided from the fast copy. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 300]] '
            'It runs offline, with nothing installed except a Java '
            'development kit. [[slnc 300]] There is no message broker and '
            'no database, on purpose, so the lesson stays on which copy '
            'may decide. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Change the second shopper so it checks the read '
            "model's stock number, and sells if it says yes. [[slnc 300]] "
            'Watch the test fail. [[slnc 300]] In a real shop, that '
            'failure is a customer charged for a kettle that does not '
            'exist. [[slnc 500]] And one question to think about. [[slnc '
            '300]] Pick a page in your own system. [[slnc 300]] How many '
            'times is it read, for every time its facts change? [[slnc '
            '300]] If that number is small, is a second copy of the data '
            'really worth keeping? [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
