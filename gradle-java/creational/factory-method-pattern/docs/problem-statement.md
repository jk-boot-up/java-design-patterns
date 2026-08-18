# Problem Statement

## The Scenario

You are building the shipping step of an online store. The store offers
several delivery tiers, and each tier hands the parcel to a different
carrier:

| Delivery tier | Carrier | Arrives in |
| --- | --- | --- |
| Standard | `PostalCourier` — Royal Post | 5 days |
| Express | `AirCourier` — SkyLink Air | 2 days |
| Same Day | `BikeCourier` — CityRide Bikes | today |
| International | `GlobalCourier` — TransWorld Freight | 9 days |

The carriers all do the same job from the outside — take an `Order`, give
back a `Shipment` — so they share one interface:

```java
public interface Courier {
    String name();
    Shipment dispatch(Order order);
}
```

Here is the part that matters. Shipping is not just "pick a carrier". Every
tier runs the *same workflow*: validate the order, log that the parcel is
being prepared, hand it to the carrier, then log the tracking number and the
promised date. Only one step in the middle differs.

## The Naive Approach (and why it hurts)

Without the pattern, one shipping class does everything and branches in the
middle:

```java
public class ShippingService {

    public Shipment ship(Order order, String tier) {
        if (order.weightKg() <= 0) {
            throw new IllegalArgumentException("Order has no weight");
        }

        Courier courier;
        if (tier.equals("STANDARD")) {
            courier = new PostalCourier();
        } else if (tier.equals("EXPRESS")) {
            courier = new AirCourier();
        } else if (tier.equals("SAME_DAY")) {
            courier = new BikeCourier();
        } else if (tier.equals("INTERNATIONAL")) {
            courier = new GlobalCourier();
        } else {
            throw new IllegalArgumentException("Unknown tier");
        }

        System.out.println("preparing " + order.orderId());
        Shipment shipment = courier.dispatch(order);
        System.out.println("booked " + shipment.trackingId());
        return shipment;
    }
}
```

This creates real problems:

- **Adding a tier means editing working code.** Drone delivery arrives and
  you have to open `ShippingService` — a class that already works, already
  ships real parcels — and change it. Every edit is a chance to break the
  four tiers that were fine.
- **The branch and the workflow are tangled.** The `if` chain sits *inside*
  the method it varies. You cannot read the workflow without reading the
  choosing, and you cannot change the choosing without touching the workflow.
- **Tiers cannot differ in anything else.** Suppose International also needs
  a customs check before dispatch. Now the method grows a second `if` chain
  on the same `tier` string, and the two chains have to stay in step.
- **Extension is closed to other teams.** A partner module cannot add a tier
  at all — the string values are baked into a class it does not own.
- **Hard to test in isolation.** There is no way to test "the shared
  workflow" separately from "which carrier", because they are one method.

Notice what is *not* the problem: the four courier classes are fine. The
workflow is fine. The mess is entirely in the seam between them.

## What About the Simple Factory?

The sibling project, [`../../simple-factory-pattern`](../../simple-factory-pattern),
solves the choosing by moving the `switch` into a dedicated factory class.
That genuinely helps — but the `switch` still exists, and adding a tier still
means editing that one central file. Simple Factory relocates the problem
where Factory Method dissolves it.

## The Question This Project Answers

> How do we write the shipping workflow **once**, in a class that never names
> a single courier, and still let each tier decide **which courier** to use —
> without a `switch` anywhere, and without editing existing code to add a new
> tier?

## The Goal

Give the workflow a hole in it, and let subclasses fill the hole:

```java
DeliveryService service = new ExpressDelivery();
Shipment shipment = service.ship(order);
```

...where:

- `ship(...)` is written once, in the abstract base class,
- the base class never names `AirCourier` or any other courier,
- each tier is a small subclass whose only real job is one `createCourier()`
  method,
- and adding drone delivery means **adding a file**, never editing one.

This is precisely the problem the **Factory Method** pattern solves. See
[`factory-method-pattern-explained.md`](factory-method-pattern-explained.md)
for how it works and where its costs are.
