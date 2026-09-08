# The Problem

## The Scenario

An order in our shop moves through a handful of statuses — placed, paid,
shipped, delivered, and occasionally cancelled. Every one of those moves is
interesting to somebody:

| When the order becomes… | …something has to happen |
| --- | --- |
| `PAID` | the warehouse feed gets a line so picking can start |
| `SHIPPED` | inventory releases the reservation, the customer is emailed, the feed is updated |
| `DELIVERED` | the customer is emailed, and analytics closes the funnel |
| `CANCELLED` | inventory puts the stock back |

Analytics wants every transition, always, including ones that do not exist
yet. And the list is not finished. Next quarter it will include loyalty
points on delivery, a fraud re-check after shipping, and a supplier
notification for drop-shipped items.

## Attempt One: Call Everyone By Name

The obvious version writes the list down in the order service:

```java
public void markShipped(String orderId, OrderStatus from) {
    OrderEvent event = new OrderEvent(orderId, from, OrderStatus.SHIPPED);

    inventory.onStatusChanged(event);
    email.onStatusChanged(event);          // if this throws, the two below never run
    analytics.onStatusChanged(event);
    warehouseFeed.onStatusChanged(event);
}
```

That is `NaiveOrderService`, and it is in this repository, compiled and
tested, because it is worth reading rather than describing. Note what is good
about it: four lines, and you can see the entire consequence of shipping an
order without leaving the method. For one order and two reactions, that is a
better program than the pattern.

## Why That Hurts

**A fifth reaction edits this file.** The fraud team's post-shipping check has
nothing to do with inventory or email, but it lands in the same method, and
everything that depended on that method is re-tested. The order service grows
a dependency on every part of the business that has ever been curious about an
order.

**It cannot be tested without all four.** There is no constructor that leaves
one out. A test of the shipping transition drags in the email client whether
it wants it or not, and every one of those four has to be stubbed before the
first assertion can be written.

**The reactions cannot be reused.** Inventory's "release the reservation"
logic is wired to `markShipped`. When the returns flow needs the same thing,
either it is duplicated or `markShipped` grows a flag.

**Analytics is a standing edit.** Its requirement is "every transition", which
under this design means every method that changes a status must remember to
call it. The one that forgets is a hole in the funnel that nobody notices for
a quarter.

**And then the outage.** There is no `try` in that method. Email clients talk
to a network, so email clients throw. When the mail server times out, the
order has already been marked shipped, inventory has already released the
stock — and analytics and the warehouse feed never run. The warehouse is never
told to pick the order. The caller gets an exception that says `SMTP timeout`
and nothing at all about the parcel that will now never leave the building.

That last one is the point. It is not a design smell you can live with; it is
an incident, and it passes code review, because the method reads perfectly.

## The Question

> How does an order tell the world what happened, without knowing who the
> world is?

## Where We Are Going

The order keeps a list of listeners. It does not know what they are:

```java
Order order = new Order("A-1002");
order.addListener(new InventoryListener(out));
order.addListener(new EmailListener("grace@example.com", out));
order.addListener(new AnalyticsListener(out));
order.addListener(new WarehouseFeedListener(out));

List<ListenerFailure> failures = order.moveTo(OrderStatus.SHIPPED);
// every listener ran; failures names any that threw
```

Search `Order.java` for the word "email". It is not there, and neither is
"inventory", "analytics" or "warehouse". A fifth reaction is a new class and
one more `addListener` call, and this file does not change.

Read [`observer-pattern-explained.md`](observer-pattern-explained.md) next —
including the part where we admit what this design costs, because it is not
free.
