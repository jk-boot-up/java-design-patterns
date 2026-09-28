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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Abstract Factory pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An abstract factory is one '
            'object that creates a whole family of related objects. '
            '[[slnc 300]] You choose the factory once. [[slnc 300]] And '
            'everything it gives you afterwards is guaranteed to belong '
            'together. [[slnc 300]] You can never accidentally mix one '
            "family with another. [[slnc 600]] Think of a restaurant's "
            'set menu. [[slnc 300]] You choose one menu, and every course '
            'that arrives was designed to go together. [[slnc 700]] In '
            "this video, an online store's checkout sells into three "
            'countries. [[slnc 500]] By the end, you will know what an '
            'abstract factory is, why it exists, and, just as '
            'importantly, when not to use it.'
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
            'Here is the scenario. [[slnc 400]] Your online store used to '
            'sell in one country. [[slnc 300]] Now it sells in three. '
            '[[slnc 500]] And checkout turns out to be three separate '
            'jobs. [[slnc 300]] Working out the tax. [[slnc 200]] '
            'Formatting the money. [[slnc 200]] And checking the delivery '
            'address. [[slnc 600]] In Britain, that means twenty percent '
            'value added tax, prices in pounds, and a postcode. [[slnc '
            '300]] In America, sales tax, dollars, and a zip code. [[slnc '
            '300]] In India, goods and services tax, rupees, and a pin '
            'code. [[slnc 500]] Three countries, three sets of rules. '
            '[[slnc 300]] And the three parts always change together.'
        ),
    ),
    dict(
        key="03-grid",
        kind="grid",
        title="Nine Classes, Three Legal Combinations",
        body=None,
        narration=(
            'So you write the classes. [[slnc 300]] Three tax '
            'calculators, three money formatters, and three address '
            'checkers. [[slnc 300]] Nine small classes, each one easy. '
            '[[slnc 500]] Picture them in a grid. [[slnc 300]] Three '
            'columns: tax, money, and address. [[slnc 300]] And three '
            'rows: Britain, America, and India. [[slnc 500]] Each column '
            'is just an ordinary interface, with three versions. [[slnc '
            '300]] Nothing new there. [[slnc 500]] But each row is more '
            'interesting. [[slnc 300]] A row is a family: three objects '
            'designed to be used together. [[slnc 600]] And here is the '
            'whole problem, in one sentence. [[slnc 300]] There are nine '
            'classes, but only three combinations are legal.'
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
            'Without a pattern, the checkout picks each piece for itself. '
            '[[slnc 500]] One chain of if statements, checking the '
            'country name, to choose the tax calculator. [[slnc 300]] '
            'Another chain, on the very same name, to choose the money '
            'formatter. [[slnc 300]] And a third chain, to choose the '
            'address checker. [[slnc 500]] None of this is exactly wrong. '
            '[[slnc 300]] It compiles, and it runs. [[slnc 500]] But you '
            'have built three separate decisions that must always agree. '
            '[[slnc 300]] And nothing checks that they do.'
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
            'And that costs you. [[slnc 500]] Reorder the cases in one '
            'chain, forget the other two, and the checkout charges '
            'British tax, but prints it in dollars. [[slnc 300]] A '
            'mismatched family is one copy and paste away. [[slnc 500]] '
            'When Germany arrives, you must open a class that handles '
            'real money, and edit it in three places. [[slnc 500]] Your '
            'checkout should be about totals and receipts. [[slnc 300]] '
            'Instead, it has become a list of nine class names. [[slnc '
            '500]] And the worst part? [[slnc 300]] None of this fails '
            'loudly. [[slnc 300]] It compiles, it runs, and it quietly '
            'produces a wrong invoice.'
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
            'This is exactly the problem the Abstract Factory solves. '
            '[[slnc 400]] Here is its definition, from the famous Gang of '
            'Four book. [[slnc 300]] Provide an interface for creating '
            'families of related objects, without naming their concrete '
            'classes. [[slnc 500]] The key word is families. [[slnc 500]] '
            'In plain words: choose a whole set at once, instead of one '
            'piece at a time. [[slnc 500]] And if your objects have no '
            'reason to match each other, you do not need this pattern at '
            'all.'
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
            'Here is an easy way to remember it: ordering dinner. [[slnc '
            '500]] You can order from the full menu. [[slnc 300]] Pick a '
            'starter, pick a main course, pick a wine. [[slnc 300]] Three '
            'free choices. [[slnc 300]] And nothing stops you putting a '
            'delicate fish next to a heavy red wine. [[slnc 300]] The '
            'kitchen will serve it. [[slnc 300]] It will just be wrong. '
            '[[slnc 600]] Or, you order the set menu. [[slnc 300]] You '
            'make one choice: the tasting menu, please. [[slnc 300]] And '
            'three courses arrive that were designed together. [[slnc '
            '300]] You never named a single dish. [[slnc 500]] The set '
            'menu takes away your freedom, on purpose. [[slnc 300]] And '
            'that is exactly what you are paying for.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "Now let's map that onto code. [[slnc 300]] There are five "
            'roles. [[slnc 500]] The client is our Checkout Service. '
            '[[slnc 300]] It holds one factory, and never mentions a '
            'country. [[slnc 500]] The abstract factory is an interface '
            'called Market Factory. [[slnc 300]] It has one creation '
            'method for each kind of product. [[slnc 500]] The concrete '
            'factories are one per country. [[slnc 300]] Each one builds '
            'a complete family. [[slnc 500]] The abstract products are '
            'three interfaces: tax calculator, money formatter, and '
            'address checker. [[slnc 300]] And the concrete products are '
            'the nine classes behind them. [[slnc 600]] Here is the key '
            'point. [[slnc 300]] Every product is created by exactly one '
            'factory. [[slnc 300]] So there is no path that puts a '
            'British tax rate next to an American address.'
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
            'Here is the abstract factory itself, and it is smaller than '
            'you might expect. [[slnc 400]] Four methods, and not one '
            "line of real code. [[slnc 500]] One returns the market's "
            'name. [[slnc 300]] The other three create a tax calculator, '
            'a money formatter, and an address checker. [[slnc 300]] All '
            'three return interfaces. [[slnc 600]] And notice what is '
            'missing. [[slnc 300]] There is no parameter saying which '
            'country. [[slnc 300]] The country is not an argument '
            'anywhere. [[slnc 300]] Because it was already decided, the '
            'moment someone chose which factory to use.'
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
            'Here is one concrete factory: the UK market factory. [[slnc '
            '400]] It creates three things. [[slnc 300]] A UK tax '
            'calculator. [[slnc 200]] A pound formatter. [[slnc 200]] And '
            'a postcode checker. [[slnc 500]] That is the entire '
            'consistency guarantee. [[slnc 300]] And it is remarkably '
            'cheap. [[slnc 500]] How many lines check that these three '
            'products match? [[slnc 300]] Zero. [[slnc 300]] They match '
            'because this is the only place the choice is made. [[slnc '
            '300]] There is nowhere else that could get it wrong. [[slnc '
            '500]] The American and Indian factories have exactly the '
            'same shape, with different products.'
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
            'Now the client, and this is the part to really listen to. '
            '[[slnc 500]] In its constructor, the checkout asks the '
            'factory for four things. [[slnc 300]] The market name, the '
            'tax calculator, the money formatter, and the address '
            'checker. [[slnc 300]] After that, the factory is never '
            'touched again. [[slnc 300]] It was a decision, not a '
            'dependency. [[slnc 600]] And the method that quotes an order '
            'never mentions a country. [[slnc 300]] Not Britain, not '
            'India, not anywhere. [[slnc 300]] No if statements on the '
            'country at all. [[slnc 500]] Even the error message is right '
            'in every market. [[slnc 300]] Because words like zip code '
            'come from the products themselves.'
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
            'So what did all that buy us? [[slnc 500]] The headline: a '
            'mismatched family is not caught. [[slnc 300]] It is '
            'impossible. [[slnc 300]] Nothing is checked, because no code '
            'anywhere could produce one. [[slnc 500]] There is now one '
            'decision, instead of three. [[slnc 300]] The checkout shrank '
            'from nine class names to three interfaces, and no country '
            'codes. [[slnc 300]] Adding a new market means adding files, '
            'and editing none. [[slnc 500]] In fact, one test invents a '
            'German market, inside a single test method. [[slnc 300]] And '
            'the unchanged checkout quotes it correctly. [[slnc 500]] And '
            'finally, the British market is now a real object. [[slnc '
            '300]] Something you can build, pass around, and test.'
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
            'But this pattern has a real cost, and you should know it '
            'before you use it. [[slnc 500]] Adding a new country is '
            'cheap. [[slnc 300]] One factory, three products, and nothing '
            'edited. [[slnc 500]] But suppose checkout now needs a '
            'receipt template too. [[slnc 300]] That is a new kind of '
            'product. [[slnc 300]] So you must add a method to the '
            'abstract factory, and then edit every single factory. [[slnc '
            '500]] In the grid, new rows are cheap. [[slnc 300]] New '
            'columns are expensive. [[slnc 500]] Also, the number of '
            'classes is countries times product kinds, so be sure the '
            'families are real. [[slnc 300]] And something, somewhere, '
            'still has to choose which factory to use. [[slnc 600]] Here '
            'is the honest test for whether you need this. [[slnc 300]] '
            'Would a mismatched pair be a bug? [[slnc 300]] If not, just '
            'pass the objects in separately.'
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
            "Let's run the demo. [[slnc 400]] The same order, worth one "
            'hundred and twenty, is quoted in three countries. [[slnc '
            '500]] Britain adds twenty percent, and shows the total in '
            'pounds: one hundred and forty-four. [[slnc 300]] America '
            'adds its sales tax, and shows dollars: one hundred and '
            'thirty dollars sixty-five. [[slnc 300]] India adds eighteen '
            'percent, and shows rupees. [[slnc 500]] All of that came '
            'from one method, with no condition on the country at all. '
            '[[slnc 300]] Only the factory changed. [[slnc 500]] And '
            'finally, the demo sends a British postcode to the American '
            'market. [[slnc 300]] It is rejected, because the address '
            'checker came from the same family as the money.'
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
            'So, to wrap up. [[slnc 400]] Use the Abstract Factory when '
            'several objects must agree with each other. [[slnc 300]] And '
            'skip it when they do not, because then you are only adding '
            'classes. [[slnc 500]] If you know the other factory '
            'patterns, here is how they compare. [[slnc 300]] A simple '
            'factory chooses with a switch statement. [[slnc 300]] A '
            'factory method chooses through inheritance. [[slnc 300]] And '
            'an abstract factory chooses a whole family, all at once. '
            '[[slnc 600]] And one sentence to remember. [[slnc 300]] If '
            'mixing objects from different groups would be a bug, you '
            'want an abstract factory.'
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
            "That's the Abstract Factory pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Choose '
            'a whole family of objects at once, and a mismatched family '
            'becomes impossible. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] If there is a pattern you '
            'would like to see covered, suggest it in the comments. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
