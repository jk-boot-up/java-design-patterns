# Problem Statement

## The Scenario

You are building checkout pricing for an online store. A product has a base
price, but customers can add optional extras at checkout: gift wrapping,
shipment insurance, and express handling. Any combination of these should be
selectable — gift wrap alone, insurance alone, all three together, or none
at all.

## Attempt One: One Class Per Combination

The obvious first move is a class for each combination you need today:

```java
public final class NaiveGiftWrappedProduct {
    private static final BigDecimal GIFT_WRAP_FEE = new BigDecimal("3.50");
    public BigDecimal cost() { return price.add(GIFT_WRAP_FEE); }
    public String description() { return name + ", gift-wrapped"; }
}

public final class NaiveInsuredProduct {
    private static final BigDecimal RATE = new BigDecimal("0.02");
    public BigDecimal cost() { return price.add(price.multiply(RATE).setScale(2, RoundingMode.HALF_UP)); }
    public String description() { return name + ", insured"; }
}
```

Then a customer wants *both* gift wrap and insurance, so a third class shows
up:

```java
public final class NaiveGiftWrappedInsuredProduct {
    private static final BigDecimal GIFT_WRAP_FEE = new BigDecimal("3.50");
    private static final BigDecimal RATE = new BigDecimal("0.02");

    public BigDecimal cost() {
        BigDecimal wrapped = price.add(GIFT_WRAP_FEE);
        BigDecimal premium = wrapped.multiply(RATE).setScale(2, RoundingMode.HALF_UP);
        return wrapped.add(premium);
    }

    public String description() { return name + ", gift-wrapped, insured"; }
}
```

Both the gift-wrap fee and the insurance premium calculation are now
duplicated across three classes.

## Why That Hurts

- **The number of classes grows combinatorially.** Two optional features
  need up to three classes (one for each, one for both). Add a third
  feature — express handling — and covering every combination needs *four
  more* classes: express alone, express+gift-wrap, express+insurance,
  express+gift-wrap+insurance. Four optional features would need fifteen
  classes just to cover every subset.
- **Every fee calculation is duplicated.** The gift-wrap fee constant and
  the insurance percentage-and-rounding logic are copy-pasted into every
  class that needs that feature, not shared.
- **A pricing bug fix means hunting down every copy.** If the insurance rate
  changes from 2% to 2.5%, or the rounding mode needs to change, every class
  that computed a premium has to be found and fixed individually.
- **Nothing here is a bug.** Each naive class computes a correct price. The
  waste is structural: optional, combinable behavior is being modeled as a
  fixed set of subclasses instead of something that can be composed at
  runtime.

## The Question This Project Answers

> How do we let a customer pick any combination of optional pricing
> features, in any order, without writing a new class for every
> combination?

## The Goal

Make each optional feature a small, independent wrapper that can be stacked
on top of anything else that already knows how to price itself:

```java
PricedItem product = new Product("Wireless Headphones", new BigDecimal("79.99"));
PricedItem priced = new ExpressHandlingDecorator(
        new InsuranceDecorator(
                new GiftWrapDecorator(product)));

priced.cost();          // every fee applied, no combination-specific class
priced.description();   // "Wireless Headphones, gift-wrapped, insured, express handling"
```

Adding a fourth optional feature means writing **one** new class, not
several. Every existing feature keeps working with it, in any stacking
order.

This is precisely the problem the **Decorator** design pattern solves. See
[`decorator-pattern-explained.md`](decorator-pattern-explained.md) for how.
