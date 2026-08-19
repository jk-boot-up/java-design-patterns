"""Scene definitions for the Abstract Factory pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "title" | "bullets" | "quote" | "code" | "console" | "diagram" | "grid"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="The Abstract Factory Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This one is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] Today we're doing the abstract factory. It's "
            "the most ambitious of the factory patterns in the Gang of Four book. "
            "[[slnc 250]] It sounds intimidating, and honestly, I think that's "
            "entirely the name's fault, because the idea underneath is simple, "
            "and you'll recognise it straight away from real life. [[slnc 250]] "
            "We'll learn it by building a real working Java project. The checkout "
            "step of an online store that sells into three countries. And by the "
            "end you'll know what an abstract factory is, why it exists, and, "
            "just as importantly, when not to use it."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "Your store has been selling in one country. Now it sells in three.",
            "",
            "Checkout is not one piece of logic. It is three:",
            "",
            "   United Kingdom    20% VAT           £1,234.50   postcode",
            "   United States     8.875% Sales Tax  $1,234.50   ZIP code",
            "   India             18% GST           ₹1,234.50   PIN code",
            "",
            "Tax, money, and addresses. All three change together.",
        ],
        narration=(
            "So, imagine your online store has been selling in one country, and "
            "now it sells in three. [[slnc 250]] And you quickly discover that "
            "checkout isn't one piece of logic. It's three. There's the tax to "
            "work out. There's the money to format. And there's the delivery "
            "address to validate. [[slnc 300]] In Britain that's twenty percent "
            "value added tax, prices in pounds, and a postcode. In America, sales "
            "tax, dollars, and a zip code. In India, goods and services tax, "
            "rupees, and a pin code. [[slnc 250]] Three countries, three sets of "
            "rules. And all three parts change together."
        ),
    ),
    dict(
        key="03-grid",
        kind="grid",
        title="Nine Classes, Three Legal Combinations",
        body=None,
        narration=(
            "So you write the classes. Three tax calculators, three currency "
            "formatters, three address validators. Nine small classes, and each "
            "one of them is easy. [[slnc 250]] Here they all are, laid out as a "
            "grid. [[slnc 250]] Now read the grid downwards. Each column is just "
            "an ordinary interface with three implementations. Nothing new there. "
            "[[slnc 300]] But read it across, and each row is something more "
            "interesting. A row is a family. Three objects that were designed to "
            "be used together. [[slnc 300]] And here's the whole problem, in one "
            "sentence. There are nine classes, but only three combinations of "
            "them are legal."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Problem",
        body="""public Quote quote(Order order, String market) {

    TaxCalculator tax;
    if (market.equals("UK")) {
        tax = new UkVatCalculator();
    } else if (market.equals("US")) {
        tax = new UsSalesTaxCalculator();
    } else {
        tax = new IndiaGstCalculator();
    }

    CurrencyFormatter money;
    if (market.equals("UK")) {
        money = new PoundFormatter();
    } else if (market.equals("US")) {
        money = new DollarFormatter();
    } else {
        money = new RupeeFormatter();
    }

    // ...and a third chain for the address validator""",
        narration=(
            "Without a pattern, the checkout picks each piece for itself. Here's "
            "what that looks like. [[slnc 250]] One chain of conditions to choose "
            "the tax calculator. Another chain, on the very same string, to "
            "choose the currency formatter. And a third one, off the bottom of "
            "the screen, for the address validator. [[slnc 300]] Now, none of "
            "this is wrong, exactly. It compiles. It runs. [[slnc 250]] But look "
            "at what you've built. Three separate decisions, that all have to "
            "agree with each other, and nothing whatsoever checking that they do."
        ),
    ),
    dict(
        key="05-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗  Reorder one chain and not the others → VAT charged in dollars",
            "✗  A mismatched family is one copy-paste away",
            "✗  Adding Germany means editing working code, three times",
            "✗  The checkout is a directory of nine class names",
            "✗  There is no object that means \"the British market\"",
            "",
            "And the worst part: it compiles, it runs,",
            "and it quietly produces a wrong invoice.",
        ],
        narration=(
            "And that costs you. [[slnc 250]] Reorder the cases in the middle "
            "chain, forget the other two, and you've built a checkout that "
            "charges British tax and prints it in dollars. A mismatched family is "
            "one copy and paste away. [[slnc 300]] When Germany arrives, you're "
            "opening a class that handles real money and editing it in three "
            "separate places. And your checkout, which should be about totals and "
            "receipts, has turned into a directory of nine class names. [[slnc "
            "300]] But here's the worst part. None of this fails loudly. It "
            "compiles, it runs, and it quietly produces a wrong invoice."
        ),
    ),
    dict(
        key="06-definition",
        kind="quote",
        title="The Abstract Factory Pattern",
        body=[
            "\"Provide an interface for creating families of",
            "related or dependent objects without specifying",
            "their concrete classes.\"",
            "",
            "— Gang of Four",
            "",
            "In plain English:",
            "choose a whole set at once, not a piece at a time.",
        ],
        narration=(
            "And this is exactly the problem the abstract factory solves. [[slnc "
            "250]] The formal definition goes like this. Provide an interface for "
            "creating families of related or dependent objects, without "
            "specifying their concrete classes. [[slnc 250]] The word doing all "
            "the work in that sentence is families. [[slnc 300]] In plain "
            "English, the pattern says, choose a whole set at once, instead of a "
            "piece at a time. [[slnc 250]] And if your objects have got no reason "
            "to match each other, then you don't need this pattern at all."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="The Set Menu",
        body=[
            "À la carte — three free choices:",
            "   starter, main, wine   ←   nothing stops a bad pairing",
            "",
            "The set menu — one choice:",
            "   you say \"the tasting menu\"",
            "   three courses arrive, designed together",
            "   you never name a dish",
            "",
            "The set menu takes the freedom away on purpose.",
            "That is what you are paying for.",
        ],
        narration=(
            "Here's how to remember it forever. Think about ordering dinner. "
            "[[slnc 250]] You can order a la carte. Pick a starter, pick a main, "
            "pick a wine. Three free decisions, and nothing at all stops you "
            "putting a delicate fish next to a heavy red. The kitchen will serve "
            "it. It'll simply be wrong. [[slnc 300]] Or, you order the set menu. "
            "And you choose one thing. You say, the tasting menu, please. And "
            "three courses arrive that were designed together. You never named a "
            "single dish. [[slnc 300]] The set menu takes your freedom away on "
            "purpose. And that's exactly what you're paying for."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So let's map that onto code. There are five roles. [[slnc 200]] At "
            "the top is the client, our checkout service. It holds one factory, "
            "and it names no country anywhere. In the middle is the abstract "
            "factory, market factory, which declares one creation method per "
            "product kind. Below that are the concrete factories, one per "
            "country, and each one builds a complete family. And then the "
            "products themselves. Three interfaces, the abstract products, and "
            "nine classes behind them, the concrete products. [[slnc 350]] Now "
            "watch the arrows. Every creates arrow leaves exactly one factory. "
            "There's no path in this picture that puts a British tax rate next to "
            "an American address."
        ),
    ),
    dict(
        key="09-interface",
        kind="code",
        title="The Abstract Factory",
        body="""public interface MarketFactory {

    String market();

    TaxCalculator createTaxCalculator();

    CurrencyFormatter createCurrencyFormatter();

    AddressValidator createAddressValidator();
}""",
        narration=(
            "Here's the abstract factory itself, and it's smaller than you'd "
            "expect. Four methods, and not one line of implementation. [[slnc "
            "250]] Look at the return types. All three are interfaces, so nothing "
            "here even reveals that a pound formatter exists. [[slnc 300]] But "
            "the really important thing about this interface is what's missing "
            "from it. Find me the parameter that says which country. There isn't "
            "one. [[slnc 250]] The country isn't an argument anywhere, because it "
            "was already decided, at the moment somebody chose which factory to "
            "use."
        ),
    ),
    dict(
        key="10-factory",
        kind="code",
        title="A Concrete Factory",
        body="""public class UkMarketFactory implements MarketFactory {

    public String market() {
        return "United Kingdom";
    }

    public TaxCalculator createTaxCalculator() {
        return new UkVatCalculator();
    }

    public CurrencyFormatter createCurrencyFormatter() {
        return new PoundFormatter();
    }

    public AddressValidator createAddressValidator() {
        return new UkPostcodeValidator();
    }
}""",
        narration=(
            "And here's one concrete factory. Three new calls, in a class whose "
            "name says British. [[slnc 250]] That's the entire consistency "
            "guarantee, and it's worth pausing for a second to appreciate how "
            "cheap it is. [[slnc 300]] Ask yourself, how many lines of code in "
            "here check that these three products match? [[slnc 250]] Zero. "
            "Nothing is validated. They match because this is the only place the "
            "choice is made, and there's nowhere else that could get it wrong. "
            "[[slnc 250]] The American and Indian factories are the same shape, "
            "with different nouns."
        ),
    ),
    dict(
        key="11-client",
        kind="code",
        title="The Client",
        body="""public CheckoutService(MarketFactory factory) {
    this.market     = factory.market();
    this.tax        = factory.createTaxCalculator();
    this.money      = factory.createCurrencyFormatter();
    this.addresses  = factory.createAddressValidator();
}

public Quote quote(Order order) {
    if (!addresses.isValid(order.postcode())) {
        throw new IllegalArgumentException(
                order.postcode() + " is not a valid "
                        + market + " " + addresses.postcodeLabel());
    }

    double taxAmount = tax.taxOn(order.subtotal());
    double total = order.subtotal() + taxAmount;
    ...
}""",
        narration=(
            "Now the client. And this is the part I really want you to look at. "
            "[[slnc 250]] Four lines in the constructor, and the whole world is "
            "set up. After that last line, the factory has done its job, and it's "
            "never touched again. It was a decision, not a dependency. [[slnc "
            "300]] And then read the method underneath. Search it for the letters "
            "U, K. Search it for India. There's nothing. Not one branch on the "
            "country. [[slnc 250]] Even the error message is correct in every "
            "market, because the words in it, United States, zip code, came from "
            "the products themselves."
        ),
    ),
    dict(
        key="12-gain",
        kind="bullets",
        title="What You Gain",
        body=[
            "✓  A mismatched family is not caught — it is impossible",
            "✓  One decision instead of three",
            "✓  The client shrinks: no class names, no country codes",
            "✓  A new market is purely additive — add files, edit none",
            "✓  \"The British market\" is now an object you can test",
            "",
            "Nothing is validated. There is simply no code",
            "that could produce a mismatch.",
        ],
        narration=(
            "So what did all of that buy us? [[slnc 250]] The headline is this. A "
            "mismatched family isn't caught. It's impossible. Nothing is being "
            "validated. There's simply no code anywhere that could produce one. "
            "[[slnc 300]] There's one decision now, instead of three. The client "
            "shrank from nine class names down to three interfaces, and no "
            "country codes at all. Adding a new market is purely additive, you "
            "add files and you edit none. [[slnc 250]] In fact the test suite in "
            "this project invents a German market inside a single test method, "
            "and the unchanged checkout quotes it correctly. [[slnc 250]] And "
            "finally, the British market is now an actual object. Something you "
            "can build, pass around, and write a test about."
        ),
    ),
    dict(
        key="13-cost",
        kind="bullets",
        title="The Honest Cost",
        body=[
            "Adding a market  →  add 1 factory + 3 products, edit nothing",
            "Adding a product kind  →  edit every factory you have",
            "",
            "✗  Class count is markets × product kinds",
            "✗  Something still has to choose the factory",
            "✗  Useless if the products never need to agree",
            "",
            "Rows are cheap. Columns are expensive.",
        ],
        narration=(
            "But I'd be doing you a disservice if I stopped there, because this "
            "pattern has a real cost, and you should know it before you reach for "
            "it. [[slnc 300]] Adding a new country is cheap. One factory, three "
            "products, nothing edited. [[slnc 250]] But suppose checkout now "
            "needs a receipt template as well. That's a new kind of product, so "
            "you have to add a method to the abstract factory, which means "
            "editing every single factory you've got. [[slnc 300]] Rows are "
            "cheap. Columns are expensive. [[slnc 250]] Beyond that, your class "
            "count is countries multiplied by product kinds, so do be sure the "
            "families are real. And something, somewhere, still has to choose "
            "which factory to use. [[slnc 300]] And here's the honest test for "
            "whether you need this at all. Would a mismatched pair be a bug? If "
            "the answer's no, inject the objects separately and walk away."
        ),
    ),
    dict(
        key="14-running",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

Checkout: United Kingdom order ORD-3001 to postcode EH1 1YZ
Checkout: VAT of £24.00 on £120.00
Checkout: total £144.00 GBP

Checkout: United States order ORD-3001 to ZIP code 10001
Checkout: Sales Tax of $10.65 on $120.00
Checkout: total $130.65 USD

Checkout: India order ORD-3001 to PIN code 560001
Checkout: GST of ₹21.60 on ₹120.00
Checkout: total ₹141.60 INR

Rejected: "EH1 1YZ" is not a valid United States ZIP code""",
        narration=(
            "Here's the program actually running. The same order, worth one "
            "hundred and twenty, quoted in three countries. [[slnc 250]] Britain "
            "adds twenty percent and prints pounds. America adds its sales tax "
            "and prints dollars. India adds eighteen percent and prints rupees. "
            "[[slnc 300]] Now, the important thing. Those nine lines were "
            "produced by one method. And that method contains no condition on the "
            "country at all. Only the factory changed. [[slnc 300]] And look at "
            "the last line. The demo deliberately sends a British postcode to the "
            "American market, and it gets turned away, because the validator came "
            "from the same family as the money."
        ),
    ),
    dict(
        key="15-wrap",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use it when several objects must agree with each other.",
            "Skip it when they don't — you are only adding classes.",
            "",
            "Simple Factory chooses with a switch.",
            "Factory Method chooses with inheritance.",
            "Abstract Factory chooses a whole family at once.",
            "",
            "One sentence to remember:",
            "if getting two objects from different groups",
            "would be a bug, you want Abstract Factory.",
        ],
        narration=(
            "So, to wrap up. Reach for the abstract factory when several objects "
            "have to agree with each other. And skip it when they don't, because "
            "then you're only adding classes. [[slnc 300]] If you've seen the "
            "other two factory patterns, here's how they line up. A simple "
            "factory chooses with a switch. A factory method chooses with "
            "inheritance. And an abstract factory chooses a whole family, all at "
            "once. [[slnc 350]] If you remember one sentence from this video, "
            "make it this one. If getting two objects from different groups would "
            "be a bug, you want an abstract factory."
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "If this helped, a thumbs up and a subscribe go a long way",
            "towards keeping more videos like it coming.",
            "",
            "Full source code, notes and an animation are in the repository.",
        ],
        narration=(
            "And that's the abstract factory. [[slnc 300]] If you got something "
            "out of this, do give it a thumbs up, and subscribe. It genuinely "
            "helps the channel, and it's what makes more of these possible. "
            "[[slnc 250]] And if there's a pattern you'd like me to cover next, "
            "drop it in the comments. I read every one. [[slnc 250]] All the "
            "source code, the written notes and an interactive animation are in "
            "the repository. Thanks for watching, and I'll see you in the next "
            "one."
        ),
    ),
]
