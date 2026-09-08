# Problem Statement

## The Scenario

You are building delivery pricing for an online store. The shop has to
quote a delivery charge at checkout, and the rule it charges by is a
business decision that changes:

- a **flat rate** — the same charge on everything, easy to explain;
- **weight bands** — under 1 kg, under 5 kg, under 20 kg, over that;
- **distance** — a base fee plus so much per hundred miles;
- **free over a threshold** — nothing to pay on orders of £50 or more,
  otherwise a flat charge.

All four are live at some point. Marketing turns the free-delivery
campaign on for a fortnight and off again. Two of them may run in
different regions at the same time. None of them is "the" rule.

## Attempt One: One Method, One Switch

The obvious first move is an enum for the method and a `switch` inside
the checkout code:

```java
public Quote quote(Shipment shipment) {
    Money delivery;
    String name;

    switch (method) {
        case FLAT_RATE -> {
            name = "Flat rate";
            delivery = Money.pounds(4.99);
        }
        case WEIGHT_BANDED -> {
            name = "Weight banded";
            if (shipment.weightKg() <= 1) {
                delivery = Money.pounds(3.50);
            } else if (shipment.weightKg() <= 5) {
                delivery = Money.pounds(6.00);
            } else if (shipment.weightKg() <= 20) {
                delivery = Money.pounds(12.00);
            } else {
                delivery = Money.pounds(25.00);
            }
        }
        case DISTANCE_BASED -> {
            name = "Distance based";
            int units = (shipment.distanceMiles() + 99) / 100;
            delivery = Money.pounds(2.00);
            for (int i = 0; i < units; i++) {
                delivery = delivery.plus(Money.pounds(1.50));
            }
        }
        case FREE_OVER_THRESHOLD -> {
            name = "Free over £50.00";
            delivery = shipment.orderSubtotal().compareTo(Money.pounds(50.00)) >= 0
                    ? Money.zero()
                    : Money.pounds(4.99);
        }
        default -> {
            name = "Unknown";
            delivery = Money.zero();
        }
    }

    return new Quote(name, shipment.orderSubtotal(), delivery);
}
```

It works. Every price it produces is correct. That is precisely what makes
it worth looking at carefully: this is not a bug report, it is a design
complaint.

## Why That Hurts

- **Four unrelated policies share one method.** The weight bands, the
  per-hundred-miles rounding and the campaign threshold have nothing to do
  with each other, and none of them can be read, reasoned about or changed
  without scrolling past the other three.
- **A fifth rule means editing code that already works.** Adding
  "collection from a locker" means opening `NaiveCheckoutService`,
  adding an enum constant, and adding a branch — touching a method that
  four working rules depend on, every time.
- **Testing one rule means going through checkout.** There is no way to
  ask "what does the weight-banded rule charge for 6.5 kg?" without
  constructing a whole `Shipment`, choosing an enum value, and calling the
  checkout method. The arithmetic is not separately reachable.
- **The `default` branch is a trap.** It charges nothing. Add a fifth enum
  constant and forget the branch, and the shop silently ships for free —
  the compiler says nothing, and neither does any test that does not
  already know to look.
- **Rules cannot be supplied from outside.** A test, a region-specific
  module, or a partner integration cannot introduce a pricing rule of its
  own without being added to the enum first.

## The Question This Project Answers

> How do we let the delivery charge be computed by a rule chosen at
> runtime, so that adding a rule means adding a class rather than editing
> the checkout?

## The Goal

Make each rule a small object behind one interface, and let checkout hold
one of them without knowing which:

```java
CheckoutService checkout = new CheckoutService(WeightBandedRule.standard());
Quote quote = checkout.quote(shipment);   // £12.00 delivery

checkout = new CheckoutService(FreeOverThresholdRule.standard());
quote = checkout.quote(shipment);         // free -- same code, same call
```

`CheckoutService.quote` has no branches in it at all. Adding a fifth rule
is one new class implementing one interface; nothing that already works
gets edited.

This is precisely the problem the **Strategy** design pattern solves. See
[`strategy-pattern-explained.md`](strategy-pattern-explained.md) for how.
