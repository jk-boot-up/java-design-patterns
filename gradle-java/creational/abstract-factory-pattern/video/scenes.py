"""Scene definitions for the Abstract Factory pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "title" | "bullets" | "quote" | "code" | "console" | "diagram" | "grid"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    dict(
        key="01-title",
        kind="title",
        title="The Abstract Factory Pattern",
        body=["A beginner's guide, in Java 21",
              "Learn it by building an online store's regional checkout"],
        narration=(
            "Hello, and welcome. In this short video we are going to learn the Abstract "
            "Factory, the most ambitious of the factory patterns in the Gang of Four "
            "book. It sounds intimidating, and I think that is entirely the name's fault. "
            "The idea underneath is simple and you will recognise it from real life. So "
            "we will learn it by building a real, working Java project, the checkout step "
            "of an online store that sells into three countries. By the end you will know "
            "what an abstract factory is, why it exists, and honestly, when not to use it."
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
            "Imagine your online store has been selling in one country, and now it sells "
            "in three. You quickly discover that checkout is not one piece of logic. It is "
            "three. There is the tax to work out. There is the money to format. And there "
            "is the delivery address to validate. In Britain that is twenty percent value "
            "added tax, prices in pounds, and a postcode. In America it is sales tax, "
            "dollars, and a zip code. In India it is goods and services tax, rupees, and a "
            "pin code. Three countries, three sets of rules, and all three parts change "
            "together."
        ),
    ),
    dict(
        key="03-grid",
        kind="grid",
        title="Nine Classes, Three Legal Combinations",
        body=None,
        narration=(
            "So you write the classes. Three tax calculators, three currency formatters, "
            "three address validators. Nine small classes, and each one is easy. Here they "
            "all are, laid out as a grid. Now read the grid downwards, and each column is "
            "just an ordinary interface with three implementations. Nothing new there. But "
            "read it across, and each row is something more interesting. A row is a family. "
            "Three objects that were designed to be used together. And here is the whole "
            "problem in one sentence. There are nine classes, but only three combinations "
            "of them are legal."
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
            "Without a pattern, the checkout picks each piece for itself. Here is what "
            "that looks like. One chain of conditions to choose the tax calculator. "
            "Another chain, on the very same string, to choose the currency formatter. "
            "And a third one, off the bottom of the screen, for the address validator. "
            "Now, none of this is wrong exactly. It compiles. It runs. But look at what "
            "you have built. Three separate decisions, that must all agree with each other, "
            "and nothing whatsoever checking that they do."
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
            "And that costs you. Reorder the cases in the middle chain and forget the "
            "other two, and you have built a checkout that charges British tax and prints "
            "it in dollars. A mismatched family is one copy and paste away. When Germany "
            "arrives, you open a class that takes real money and edit it in three separate "
            "places. And your checkout, which should be about totals and receipts, has "
            "become a directory of nine class names. But here is the worst part. None of "
            "this fails loudly. It compiles, it runs, and it quietly produces a wrong "
            "invoice."
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
            "This is exactly the problem the Abstract Factory pattern solves. The formal "
            "definition goes like this. Provide an interface for creating families of "
            "related or dependent objects, without specifying their concrete classes. "
            "The word doing all the work in that sentence is families. In plain English, "
            "the pattern says this. Choose a whole set at once, instead of a piece at a "
            "time. And if your objects have no reason to match each other, then you do "
            "not need this pattern at all."
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
            "Here is the way to remember it forever. Think about ordering dinner. You can "
            "order à la carte. Pick a starter, pick a main, pick a wine. Three free "
            "decisions, and nothing at all stops you putting a delicate fish next to a "
            "heavy red. The kitchen will serve it. It will simply be wrong. Or, you can "
            "order the set menu. You choose one thing. You say, the tasting menu, please. "
            "And three courses arrive that were designed together. You never named a "
            "single dish. The set menu takes your freedom away on purpose, and that is "
            "exactly what you are paying for."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So let us map that onto code. There are five roles. At the top is the client, "
            "our checkout service. It holds one factory and it names no country anywhere. "
            "In the middle is the abstract factory, market factory, which declares one "
            "creation method per product kind. Below it are the concrete factories, one "
            "per country, and each of those builds one complete family. And then there are "
            "the products themselves. Three interfaces, the abstract products, and nine "
            "classes behind them, the concrete products. Now watch the arrows. Every "
            "creates arrow leaves exactly one factory. There is no path in this picture "
            "that puts a British tax rate next to an American address."
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
            "Here is the abstract factory itself, and it is smaller than you might expect. "
            "Four methods, and not one line of implementation. Look at the return types. "
            "All three are interfaces, so nothing here reveals that a pound formatter even "
            "exists. But the really important thing about this interface is what is "
            "missing from it. Find me the parameter that says which country. There isn't "
            "one. The country is not an argument anywhere, because it was already decided, "
            "at the moment somebody chose which factory to use."
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
            "And here is one concrete factory. Three new calls, in a class whose name says "
            "British. That is the entire consistency guarantee, and it is worth pausing to "
            "appreciate how cheap it is. Ask yourself, how many lines of code here check "
            "that these three products match? Zero. Nothing is validated. They match "
            "because this is the only place the choice is made, and there is nowhere else "
            "that could get it wrong. The American and Indian factories are the same shape "
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
            "Now the client, and this is the part I want you to really look at. Four lines "
            "in the constructor, and the whole world is set up. After that last line, the "
            "factory has done its job and is never touched again. It was a decision, not a "
            "dependency. And then read the method underneath. Search it for the letters "
            "U, K. Search it for India. There is nothing. Not one branch on the country. "
            "Even the error message is correct in every market, because the words in it, "
            "United States, zip code, came from the products themselves."
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
            "So what did all that buy us? The headline is this. A mismatched family is not "
            "caught, it is impossible. Nothing is being validated. There is simply no code "
            "anywhere that could produce one. There is one decision now instead of three. "
            "The client shrank from nine class names down to three interfaces and no "
            "country codes at all. Adding a new market is purely additive, you add files "
            "and edit none. In fact the test suite in this project invents a German market "
            "inside a single test method, and the unchanged checkout quotes it correctly. "
            "And finally, the British market is now an actual object, that you can build, "
            "pass around, and write a test about."
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
            "But I would be doing you a disservice if I stopped there, because this pattern "
            "has a real cost and you should know it before you reach for it. Adding a new "
            "country is cheap. One factory, three products, nothing edited. But suppose "
            "checkout now needs a receipt template as well. That is a new kind of product, "
            "and you have to add a method to the abstract factory, which means editing "
            "every single factory you have. Rows are cheap. Columns are expensive. Beyond "
            "that, your class count is countries multiplied by product kinds, so be sure "
            "the families are real. Something, somewhere, still has to choose which factory "
            "to use. And here is the honest test for whether you need this at all. Would a "
            "mismatched pair be a bug? If the answer is no, inject the objects separately "
            "and walk away."
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
            "Here is the program actually running. The same order, worth one hundred and "
            "twenty, quoted in three countries. Britain adds twenty percent and prints "
            "pounds. America adds its sales tax and prints dollars. India adds eighteen "
            "percent and prints rupees. Now, the important thing. Those nine lines were "
            "produced by one method, and that method contains no condition on the country "
            "at all. Only the factory changed. And look at the last line. The demo "
            "deliberately sends a British postcode to the American market, and it is "
            "turned away, because the validator came from the same family as the money."
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
            "So, to wrap up. Reach for the Abstract Factory when several objects have to "
            "agree with each other. Skip it when they do not, because then you are only "
            "adding classes. And if you have seen the other two factory patterns, here is "
            "how they line up. A simple factory chooses with a switch. A factory method "
            "chooses with inheritance. An abstract factory chooses a whole family at once. "
            "If you remember one sentence from this video, make it this one. If getting "
            "two objects from different groups would be a bug, you want an abstract "
            "factory. The full source code, the written notes and an interactive animation "
            "are all in the repository. Thank you for watching, and enjoy the pattern."
        ),
    ),
]
