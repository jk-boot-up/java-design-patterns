# The Problem

Our online store needs to place purchase orders. Every order has two facts
that never change: who is buying, and where it ships. But the options pile
up fast:

- most orders are plain
- some are gift-wrapped, and some of those carry a message
- some are marked priority
- some carry a coupon code
- some need a note for the warehouse

Something has to build a `PurchaseOrder` out of all of that. The obvious
tool is a constructor. Let us try.

## Attempt one: a constructor with a parameter for everything

```java
public class PurchaseOrder {

    public PurchaseOrder(String orderId, String customerId, List<LineItem> items,
                          Address shippingAddress, boolean giftWrapped, String giftMessage,
                          String couponCode, boolean priority, String notes) {
        ...
    }
}
```

It compiles. Now look at what calling it looks like.

```java
new PurchaseOrder("ORD-9001", "CUST-100", items, home,
        true, "Happy birthday!", "WELCOME10", false, null);

new PurchaseOrder("ORD-9004", "CUST-103", items, home,
        false, null, null, true, "Ship same-day if received before 2pm.");
```

It works. It is also awful, and it is worth being precise about why.

## Why That Hurts

**1. Nobody can read the call sites.** Which argument is `giftWrapped` and
which is `priority`? Both are `boolean`, they sit four and five slots from
the end, and a reader has to open `PurchaseOrder` and count parameters to
find out. Swap the two `true`/`false` values by accident and the order
ships gift-wrapped instead of priority, and the compiler will not say a
word.

**2. Most calls are mostly `null` and `false`.** The plain order above
spends five of its nine arguments saying "nothing here" — `null`, `null`,
`false`, `null` — just to reach the one it actually wants to set. That is
not a fluke of this example; it is what happens whenever a handful of
callers each want a different one or two options out of many.

**3. Order matters, and it is arbitrary.** `giftWrapped` before
`giftMessage` before `couponCode` before `priority` before `notes` — there
is no natural reason for that sequence, which means there is nothing to
help a reader remember it, and nothing stops a ninth caller demanding a
different one.

**4. Every new option widens the constructor, everywhere.** Marketing asks
for a delivery time window. That is a tenth parameter, and every existing
call site — plain orders included — needs another `null` or `false`
inserted in the right place, whether or not it cares.

**5. There is no room to enforce a rule between two options.** Suppose a
gift message should always imply gift wrap — nobody writes a card for a box
that is not wrapped. A constructor either trusts every caller to set both
correctly, or buries an `if` inside itself that quietly overrides one
argument based on another, which is worse: now the constructor lies about
what it was handed.

## Attempt two: telescoping constructors

The traditional patch is to write an overload for every common
combination:

```java
public PurchaseOrder(String orderId, String customerId, List<LineItem> items, Address address) { ... }
public PurchaseOrder(String orderId, String customerId, List<LineItem> items, Address address,
                      boolean giftWrapped) { ... }
public PurchaseOrder(String orderId, String customerId, List<LineItem> items, Address address,
                      boolean giftWrapped, String giftMessage) { ... }
// ...and so on, one overload per combination anyone has needed so far
```

This is *Effective Java*'s name for it — **the telescoping constructor
pattern** — and the name is not a compliment. Five optional pieces have
thirty-two possible combinations. You will never write all of them, so you
pick a handful, and the day a caller needs a combination you did not
anticipate, they either take an overload that sets something they did not
want and then cannot unset it, or you add overload number nine.

## The Question This Project Answers

> How do we assemble an object with a couple of required facts and a
> long, growing tail of optional ones, so that a caller sets only the
> options it actually wants, in any order, in a way a reader can follow at
> the call site — and without a combinatorial explosion of constructors?

The answer is a pattern that is both a Gang of Four pattern and *Effective
Java*'s Item 2: give the type a **builder** — a companion object with one
chainable method per piece, and a `build()` that assembles and validates
the whole thing at the end.

Read on in
[`builder-pattern-explained.md`](builder-pattern-explained.md).
