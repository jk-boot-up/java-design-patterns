# Problem Statement

## The Scenario

You are building the checkout page of an online shop. It has five controls,
which is a small checkout page:

| Control | What the shopper does with it |
| --- | --- |
| Country | picks where the order is going |
| Shipping method | picks a courier from the ones that serve that country |
| Gift wrap | ticks a box, if the order qualifies |
| Total | reads the price — they cannot change it |
| Place Order | presses it, once everything is filled in |

Those five are not independent. Change the country and the courier list has
to be refilled, because the courier that delivers in the United Kingdom is not
the one that ships to the United States. Gift wrapping is done by hand in the
London warehouse, so it is only offered on domestic orders. The total follows
the shipping method and the gift wrap. And Place Order may only be pressed
when there is both a country and a courier.

Write those rules down and there are only four of them. The difficulty is not
the rules. The difficulty is *where they live*.

## Attempt One: Each Widget Updates the Ones It Affects

The obvious place to put "when the country changes, refill the shipping list"
is in the country widget, because that is where the country changes. So the
country widget is given a reference to the shipping widget:

```java
public void select(String country) {
    this.country = country;
    shipping.showOptions("UK".equals(country)
            ? List.of("Standard", "Express")
            : List.of("International"));
}
```

Then gift wrap depends on the country too, so it needs a reference to that as
well. And the total moved, so it needs the total. And the button might need
re-checking, so it needs the button. The country widget now holds four other
widgets:

```java
country.wire(shipping, giftWrap, total, placeOrder);
shipping.wire(giftWrap, total, placeOrder);
giftWrap.wire(shipping, total);
```

Nine references, on a form with five controls. You can run this —
`NaiveCheckoutForm` is in this project, and `NaiveCheckoutFormTest` holds its
behaviour in place.

## Why That Hurts

**Nobody can see the whole form.** The rules of the page are spread across
three widgets. To answer "what happens when the country changes?" you have to
read `NaiveCountry.select`, and then read every method it calls, and hope
none of them calls something else. There is no file you can open that tells
you what the page does.

**The bugs are omissions, and omissions are silent.** Changing the country
withdraws gift wrapping but leaves the box ticked, so the shopper is charged
£2 for wrapping the warehouse will never do. Changing the country clears the
shipping method but nobody re-checks the button, so the order can be placed
with no courier on it. Neither throws. Neither logs. Both are a line that was
never written, and you cannot review code that is not there.

**The wiring grows faster than the form.** Five widgets, nine references. Add
a voucher code field that affects the total, and the discount that affects
whether gift wrap is free, and you are adding references in both directions to
several widgets at once. This is the *n*² in "*n*² wiring" — it is why forms
like this are fine at five controls and unmaintainable at twelve.

**No widget can be reused or tested alone.** `NaiveCountry` cannot be
constructed without four other widgets to hand it, so there is no such thing
as a test of the country selector. Every test is a test of the whole form.

**The dependencies are circular.** Shipping holds gift wrap, gift wrap holds
shipping. Neither can be understood, changed or moved without the other.

## The Question This Project Answers

> How do you let five controls on a page react to each other, without any of
> them holding a reference to any of the others — and without the rules of the
> page ending up scattered across all five?

## The Goal

Make the wiring look like this, and make it stay looking like this when the
sixth control arrives:

```
country  ─┐
shipping ─┤
giftWrap ─┼──►  CheckoutForm
total    ─┤
button   ─┘
```

Five widgets, five references, one place where the rules live. Adding a sixth
control adds one reference, not five.
