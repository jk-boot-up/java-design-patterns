# The Abstract Factory Pattern — Explained

## One-Line Definition

> **Abstract Factory** provides an interface for creating families of related
> or dependent objects without specifying their concrete classes.

Put less formally: instead of choosing objects one at a time and hoping they
go together, you choose a **set** once, and something else hands you every
piece of it.

The word doing the work in that definition is *families*. If your objects
have no reason to match, you do not need this pattern.

It is a **creational** pattern from the original Gang of Four catalogue, and
the more ambitious of the book's two factory patterns.

## The Everyday Analogy

Think of a restaurant's set menu.

You could order à la carte: pick a starter, pick a main, pick a wine. Three
free decisions, and nothing stops you pairing a delicate fish with a heavy
red. The kitchen will serve it. It will simply be wrong.

The set menu removes the freedom on purpose. You choose *one* thing — "the
tasting menu" — and three courses arrive that were designed together. You
never name a dish. And when the chef changes the menu next season, you order
in exactly the same words and get an entirely different dinner.

The set menu is `MarketFactory`. "The British menu" is `UkMarketFactory`. The
three courses are the tax calculator, the currency formatter and the address
validator. And the wrong pairing you can no longer order is British VAT on an
American address.

## The Participants

| Role | In this project | Job |
| --- | --- | --- |
| Abstract Factory | `MarketFactory` | Declares one creation method per product kind |
| Concrete Factory | `UkMarketFactory`, `UsMarketFactory`, `IndiaMarketFactory` | Builds one complete, self-consistent family |
| Abstract Products | `TaxCalculator`, `CurrencyFormatter`, `AddressValidator` | The only types the client is allowed to see |
| Concrete Products | `UkVatCalculator`, `PoundFormatter`, `UkPostcodeValidator`, and the six others | The real, market-specific behaviour |
| Client | `CheckoutService` | Holds one factory, names no market and no product class |

## How This Project Implements It

### The abstract factory

```java
public interface MarketFactory {

    /** The market this family belongs to, for logs and receipts. */
    String market();

    TaxCalculator createTaxCalculator();

    CurrencyFormatter createCurrencyFormatter();

    AddressValidator createAddressValidator();
}
```

Four methods and no implementation. Notice the return types: all three are
interfaces. Nothing here reveals that `PoundFormatter` exists, and nothing
here mentions Britain.

Notice also what the interface makes *impossible*. There is no method that
returns "a tax calculator for a market you name" — the market is not a
parameter anywhere. It was decided when the factory was chosen.

### Three abstract products, not one

```java
public interface TaxCalculator {
    String label();
    double taxOn(double subtotal);
}

public interface CurrencyFormatter {
    String currencyCode();
    String format(double amount);
}

public interface AddressValidator {
    String postcodeLabel();
    boolean isValid(String postcode);
}
```

This is the difference from Factory Method in a single glance. There, one
creator produced one kind of thing. Here, one factory produces three kinds of
thing that must agree with each other.

Each interface exposes not just behaviour but *vocabulary*: `label()` gives
"VAT" or "GST", `postcodeLabel()` gives "postcode" or "ZIP code". That is what
lets the client write market-correct messages without knowing any market.

### The concrete products are small and unaware

```java
public class UkVatCalculator implements TaxCalculator {

    private static final double RATE = 0.20;

    @Override
    public String label() {
        return "VAT";
    }

    @Override
    public double taxOn(double subtotal) {
        return round(subtotal * RATE);
    }

    private static double round(double amount) {
        return Math.round(amount * 100.0) / 100.0;
    }
}
```

```java
public class UkPostcodeValidator implements AddressValidator {

    private static final Pattern FORMAT =
            Pattern.compile("^[A-Z]{1,2}\\d[A-Z\\d]? ?\\d[A-Z]{2}$");

    @Override
    public String postcodeLabel() {
        return "postcode";
    }

    @Override
    public boolean isValid(String postcode) {
        return postcode != null && FORMAT.matcher(postcode.trim().toUpperCase()).matches();
    }
}
```

Neither class mentions the other. Neither mentions pounds. They are family
members that have never met — the factory is the only thing that knows they
belong together.

### The concrete factory is where a family is declared

```java
public class UkMarketFactory implements MarketFactory {

    @Override
    public String market() {
        return "United Kingdom";
    }

    @Override
    public TaxCalculator createTaxCalculator() {
        return new UkVatCalculator();
    }

    @Override
    public CurrencyFormatter createCurrencyFormatter() {
        return new PoundFormatter();
    }

    @Override
    public AddressValidator createAddressValidator() {
        return new UkPostcodeValidator();
    }
}
```

Three `new` calls in a class whose name says "British". That is the entire
consistency guarantee, and it is worth appreciating how cheap it is: the
matching is enforced not by validation, but by there being no code anywhere
that could produce a mismatch.

Read the other two factories and they are the same shape with different nouns.

### The client asks once, then forgets the factory

```java
public class CheckoutService {

    private final String market;
    private final TaxCalculator tax;
    private final CurrencyFormatter money;
    private final AddressValidator addresses;

    public CheckoutService(MarketFactory factory) {
        this.market = factory.market();
        this.tax = factory.createTaxCalculator();
        this.money = factory.createCurrencyFormatter();
        this.addresses = factory.createAddressValidator();
    }
```

Four lines, and the world is set up. After the constructor the factory is
never touched again — it was a decision, not a dependency.

The rest of the class reads as if there were only ever one market:

```java
    public Quote quote(Order order) {
        if (!addresses.isValid(order.postcode())) {
            throw new IllegalArgumentException(
                    "\"" + order.postcode() + "\" is not a valid " + market + " "
                            + addresses.postcodeLabel());
        }

        double taxAmount = tax.taxOn(order.subtotal());
        double total = order.subtotal() + taxAmount;

        return new Quote(market, money.format(order.subtotal()), tax.label(),
                money.format(taxAmount), money.format(total));
    }
}
```

Search that method for "UK", "US" or "India" and you find nothing. Even the
error message is market-correct — "not a valid United States ZIP code" — and
it was assembled from the products themselves, with no branch.

### One line changes, everything changes

```java
CheckoutService uk = new CheckoutService(new UkMarketFactory());
CheckoutService us = new CheckoutService(new UsMarketFactory());
```

Same order, same call, same code path:

```
Checkout: VAT of £24.00 on £120.00
Checkout: total £144.00 GBP

Checkout: Sales Tax of $10.65 on $120.00
Checkout: total $130.65 USD
```

Three products swapped in one constructor argument.

### Java 21 records as the data carriers

```java
public record Order(String orderId, String customerId, double subtotal, String postcode) { }
public record Quote(String market, String subtotal, String taxLabel, String tax, String total) { }
```

`Quote` holds *already formatted* strings rather than numbers. That is
deliberate: the currency decision the factory made travels all the way out to
the caller, so nothing downstream can render £24.00 as $24.00.

## What You Gain

- **A mismatched family becomes unrepresentable.** Not "checked for" —
  unrepresentable. There is no code path that combines products from different
  markets, so there is no bug to test for.
- **One decision instead of three.** The market is chosen in exactly one place,
  in one line, and everything else follows from it.
- **The client shrinks.** `CheckoutService` went from nine class names and
  three country codes to three interface types and no country codes at all.
- **A new market is additive.** Germany means a new factory and three new
  products. No existing class is edited — the test suite in this project
  proves it by inventing a German market inside a single test method.
- **Each family is testable as a unit.** "The British market" is now an object
  you can construct, pass around and assert about.

## What to Watch Out For

- **Adding a new product *kind* is expensive.** Suppose checkout now needs a
  `ReceiptTemplate` too. You add a method to `MarketFactory` — and every
  concrete factory must implement it. Three markets, three edits, and this
  cost grows with every market you have added. This is the pattern's one real
  weakness, and it is the exact mirror of its strength: rows are cheap,
  columns are expensive.
- **The class count grows quickly.** Markets × product kinds. Three by three is
  nine classes plus four interfaces before any business logic. Five markets and
  five product kinds is twenty-five. Be sure the families are real.
- **You still have to choose the factory.** The pattern removes the branching
  from the client, not from the universe. Somewhere a line reads
  `new UkMarketFactory()`, and in a real application that decision comes from
  configuration or dependency injection. If you write a `switch` on a country
  code to make it, you have built a Simple Factory *of* Abstract Factories —
  which is fine and common, but notice that you did it, and keep it in exactly
  one place.
- **Do not use it when the products are unrelated.** If your tax calculator and
  your currency formatter genuinely never need to agree, this is machinery
  around nothing. Ask the question honestly: *would a mismatched pair be a
  bug?* If the answer is no, inject the two objects separately and stop.
- **Do not add parameters to the creation methods.** The moment
  `createTaxCalculator(String market)` appears, the family guarantee is gone
  and you are back to per-call decisions.
- **Beware the one-implementation abstract factory.** An interface with a single
  concrete factory behind it, "in case we go international one day", is a cost
  paid today for a benefit that may never arrive.

## Abstract Factory vs. the Other Factory Patterns

| | Simple Factory | Factory Method | Abstract Factory |
| --- | --- | --- | --- |
| Is it in the GoF book? | No, an idiom | Yes | Yes |
| Mechanism | One static method with a `switch` | An abstract method, overridden | An interface with several creation methods |
| Creates | One product | One product | A family of related products |
| Adding a new *variant* means | Editing the factory | Adding a subclass | Adding a factory and its products |
| Adding a new *product kind* means | Editing the factory | Nothing — there is only one kind | Editing every factory |
| Needs inheritance? | No | Yes, of the creator | Yes, of the factory |
| The question it answers | "Which one?" | "Which one — decided by my subclass?" | "Which set?" |

The progression across those three columns is the reason to learn them in
order. Simple Factory moves a decision into a helper. Factory Method dissolves
the decision into the type system. Abstract Factory raises the decision from a
single object to a whole coordinated set.

A one-sentence test for which you need: **if getting two objects from different
groups would be a bug, you want Abstract Factory.** Otherwise you probably do
not.

## Where You Have Already Seen It

- `javax.xml.parsers.DocumentBuilderFactory` and `SAXParserFactory` — pick an
  implementation once, get a matching parser stack.
- `java.sql.Connection` — one connection hands you the `Statement`,
  `PreparedStatement` and `ResultSet` implementations of a single driver. Mixing
  drivers' objects is exactly the mismatch the pattern prevents.
- Swing's `LookAndFeel` — one choice, and every widget is drawn to match.
- `javax.net.ssl.SSLContext` — one context supplies matching socket, server
  socket and engine factories.
- Any application with a locale, a theme, a cloud provider or a database
  dialect that swaps a whole coordinated set of behaviours at once.

## Try It Yourself

1. **Add Germany.** Write `GermanyMarketFactory`, `GermanVatCalculator`,
   `EuroFormatter` and `GermanPlzValidator`, and add one line to the demo.
   Confirm you never opened `CheckoutService`.
2. **Try to build a mismatch.** Attempt to give the checkout British tax and
   American addresses without editing `CheckoutService`. Notice that the
   constructor does not offer you the opportunity.
3. **Feel the expensive direction.** Add a `createReceiptTemplate()` method to
   `MarketFactory` and count the files you had to touch. Compare that with the
   count from step 1.
4. **Watch the same code produce different money.** Run the demo and read the
   three blocks of output. Every line came from the same method.
5. **Question the pattern.** If the store only ever sold in one country, what
   would all this machinery be buying you? Write your answer down before
   re-reading "What to Watch Out For".

## See Also

- [`problem-statement.md`](problem-statement.md) — the pain this removes
- [`class-diagram.md`](class-diagram.md) — the static structure and the families
- [`uml-diagram.md`](uml-diagram.md) — the runtime sequence
- [`animation.html`](animation.html) — the flow, step by step
- [`prerequisites.md`](prerequisites.md) — what to know before you start
- [`../../factory-method-pattern`](../../factory-method-pattern) — one creator,
  one product, decided by inheritance
- [`../../simple-factory-pattern`](../../simple-factory-pattern) — where the
  whole family of factory patterns starts
