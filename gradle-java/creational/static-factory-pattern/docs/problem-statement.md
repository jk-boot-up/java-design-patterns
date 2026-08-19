# The Problem

Our online store needs discounts. Marketing has asked for four kinds, and
promises there will be more:

- a percentage off the subtotal — "10% off"
- a flat amount off — "£5 off"
- free shipping
- and, for most orders, no discount at all

Something has to turn a coupon code into one of those. The obvious tool is a
constructor. Let us try.

## Attempt one: two constructors

```java
public class Discount {

    public Discount(double percent) {      // 10% off
        ...
    }

    public Discount(double amountOff) {    // £10 off
        ...
    }
}
```

This does not compile.

```
error: constructor Discount(double) is already defined in class Discount
```

Both take one number. Java tells the two apart by their parameter *types*,
and both are `double`. There is no way to say "this one means a percentage
and that one means pounds", because a constructor's name is fixed — it is
the class name, and a class has only one of those.

That is the whole problem in one line: **a constructor cannot be named.**

## Attempt two: one constructor with a parameter for everything

So we widen it until every case fits:

```java
public class Discount {

    private final double percent;
    private final double amountOff;
    private final boolean freeShipping;

    public Discount(double percent, double amountOff, boolean freeShipping) {
        this.percent = percent;
        this.amountOff = amountOff;
        this.freeShipping = freeShipping;
    }

    public double appliedTo(Order order) {
        if (freeShipping) {
            return order.shipping();
        }
        if (amountOff > 0) {
            return Math.min(amountOff, order.subtotal());
        }
        return order.subtotal() * percent;
    }
}
```

And here is what the call sites look like:

```java
Discount tenPercent   = new Discount(0.10, 0, false);
Discount fiverOff     = new Discount(0, 5.00, false);
Discount freeShipping = new Discount(0, 0, true);
Discount nothing      = new Discount(0, 0, false);
```

It compiles. It even works. It is also awful, and it is worth being precise
about why.

## Why That Hurts

**1. Nobody can read the call sites.** `new Discount(0, 5.00, false)` — is
that 5% or £5? What is the `false`? A reader has to open `Discount` and count
parameters. Worse, `new Discount(0.10, 0, false)` and
`new Discount(0, 0.10, false)` are both legal, look almost identical, and one
of them charges the customer £119.90 instead of £108.

**2. Illegal objects are constructible.** `new Discount(0.10, 5.00, true)`
asks for all three at once. Nothing stops it. The class has to *decide* what
that means, which is why `appliedTo` is a chain of `if`s: it is not computing
a discount, it is guessing which field the caller actually meant.

**3. Every new kind of discount widens the constructor.** Marketing asks for
"buy one get one free" and "£10 off orders over £100". Two more parameters,
and every one of the four existing call sites has to be edited to pass
another `0` or `false`. None of them changed behaviour; they changed because
the constructor did.

**4. Every discount allocates.** There are millions of orders and almost all
of them have no discount. `new Discount(0, 0, false)` creates a fresh object
each time to represent *nothing*. A constructor is required to return a new
instance — that is what `new` means — so there is no way to hand back a
shared one.

**5. The class is welded to its callers.** `Discount` is public, so its
constructor is public, so its shape is now a promise. Splitting it into
`PercentageDiscount` and `FreeShippingDiscount` — the design it obviously
wants — would break every caller in the codebase, because they all say
`new Discount(...)`.

Every one of those five traces back to the same root. The caller is being
made to specify **how to build the object** when all it wanted to say was
**what it wants**.

## What About a Separate Factory Class?

You could write a `DiscountFactory` with `createPercentage(...)` and
`createFlat(...)`. That is the Simple Factory idiom, and it is covered in
[`../../simple-factory-pattern`](../../simple-factory-pattern). It fixes the
naming problem.

But look at what it costs: a second class that exists only to build the
first, a name every caller must learn, and a decision about where it lives.
For a type whose creation logic is *its own business*, that class is
ceremony. `Discount` already knows what a discount is. It is the natural
home.

## The Question This Project Answers

> How do we let callers say *what they want* — "10% off", "free shipping",
> "whatever this coupon code means" — without a separate factory class, and
> without promising anything about which class comes back?

The answer is the oldest and least glamorous creational technique in Java,
and by far the most used: give the type some **static factory methods**, make
the constructor private, and let the type create itself.

Read on in
[`static-factory-pattern-explained.md`](static-factory-pattern-explained.md).
