# Problem Statement

## The Scenario

Your online store has been selling to one country. It is about to sell to
three. Checkout, it turns out, is not one piece of logic — it is three, and
all three change together when the market changes:

| Market | Tax | Money | Address |
| --- | --- | --- | --- |
| United Kingdom | 20% VAT | £1,234.50 · GBP | postcode — `EH1 1YZ` |
| United States | 8.875% Sales Tax | $1,234.50 · USD | ZIP code — `10001` |
| India | 18% GST | ₹1,234.50 · INR | PIN code — `560001` |

Each column is easy on its own. Three tax calculators, three currency
formatters, three address validators — nine small classes, three interfaces:

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

Here is the part that matters. **The three must agree.** A receipt showing
British VAT next to a dollar sign is not a small bug, it is a wrong invoice.
A checkout that accepts an American ZIP code and then charges Indian GST is
worse. The nine classes are fine individually; the danger lives in how they
are combined.

## The Naive Approach (and why it hurts)

Without the pattern, the client picks each piece for itself:

```java
public class CheckoutService {

    public Quote quote(Order order, String market) {

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

        AddressValidator addresses;
        if (market.equals("UK")) {
            addresses = new UkPostcodeValidator();
        } else if (market.equals("US")) {
            addresses = new UsZipValidator();
        } else {
            addresses = new IndiaPinValidator();
        }

        // ...and only now does the actual work start
    }
}
```

Read that and the problems announce themselves:

- **Three branches that must stay in step, forever.** They all switch on the
  same string, and nothing checks that they agree. Change the order of the
  cases in one and not the others and you have built a checkout that charges
  VAT in dollars. It compiles. The tests you happen to have may even pass.
- **A mismatched family is one typo away.** Copy-paste the currency block to
  make the address block, forget to change one line, and `UkPostcodeValidator`
  starts validating American addresses. Nothing in the language stops you.
- **Adding a market means editing working code, three times.** Germany
  arrives and you open a class that already takes real money, and change it in
  three separate places. Miss one and the fourth market silently falls through
  to whatever the `else` branch happens to be.
- **The client knows every market and every product class.** `CheckoutService`
  should be about tax, totals and receipts. Instead it is a directory of nine
  class names and three country codes.
- **Testing a market means testing the whole method.** There is no object that
  represents "the British market", so there is nothing you can build, hand
  around, or assert about on its own.

Note what is *not* the problem here. The nine product classes are small and
correct. The checkout arithmetic is fine. The mess is entirely in the seam:
the code that decides which three objects to use together.

## What About Factory Method?

The sibling project,
[`../../factory-method-pattern`](../../factory-method-pattern), removes a
branch like this by giving the workflow a hole and letting a subclass fill it.
That works beautifully — for **one** product. Here we have three, and the
whole difficulty is that the three choices are not independent. A creator with
three separate factory methods on it, each overridden freely, still lets a
subclass return a mismatched trio.

What we need is not three decisions made well. It is **one** decision that
produces three objects.

## The Question This Project Answers

> How do we let a client use a market's tax rules, currency and address format
> together — without the client naming any of them, and without any way for a
> British tax rate to end up next to an American ZIP code?

## The Goal

Make the family the unit of choice:

```java
CheckoutService checkout = new CheckoutService(new UkMarketFactory());
Quote quote = checkout.quote(order);
```

...where:

- one line names the market, and nothing after it does,
- the client asks a single object for all three products,
- the three always match, because a factory only knows how to build its own,
- and adding Germany means **adding a factory and three products**, never
  editing the checkout.

This is precisely the problem the **Abstract Factory** pattern solves. See
[`abstract-factory-pattern-explained.md`](abstract-factory-pattern-explained.md)
for how it works and where its costs are.
