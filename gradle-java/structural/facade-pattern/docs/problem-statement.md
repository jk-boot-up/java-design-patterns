# Problem Statement

## The Scenario

You are building the checkout feature for an online store. When a customer
clicks **"Place Order"**, four different things have to happen, in a very
specific order:

1. **Reserve the stock** so nobody else can buy the last item.
2. **Charge the customer's card** — but only after stock is confirmed.
3. **Schedule the shipment** with the warehouse.
4. **Email the customer** a confirmation with a tracking number.

Each of these lives in its own service class, written by a different team:

| Subsystem | Responsibility |
| --- | --- |
| `InventoryService` | Reserves stock for a product |
| `PaymentService` | Charges the customer and returns a payment id |
| `ShippingService` | Schedules a shipment and returns a tracking id |
| `NotificationService` | Sends the confirmation email |

## The Naive Approach (and why it hurts)

Without a facade, every caller has to wire all four services together
itself:

```java
// Inside a web controller, a mobile API, a CLI admin tool, a batch job...
InventoryService inventory = new InventoryService();
PaymentService payment = new PaymentService();
ShippingService shipping = new ShippingService();
NotificationService notification = new NotificationService();

String orderId = "ORD-" + UUID.randomUUID().toString().substring(0, 8);

if (!inventory.reserveStock(productId, quantity)) {
    throw new IllegalStateException("Out of stock");
}
String paymentId = payment.charge(customerId, amount);
String trackingId = shipping.scheduleShipment(orderId, address);
notification.sendOrderConfirmation(customerId, orderId, trackingId);
```

This creates real problems:

- **The client knows too much.** Every caller must know all four services,
  their constructors, and their method signatures.
- **The order is easy to get wrong.** Charge the card before reserving
  stock and you have taken money for something you cannot ship.
- **Duplication.** The web controller, the mobile API and the admin tool
  each repeat the same eight lines — and each can drift out of sync.
- **Change ripples outward.** Add a `FraudCheckService` tomorrow and you
  must edit *every* caller.
- **Hard to test.** Testing "placing an order" means standing up four
  collaborators every single time.

## The Question This Project Answers

> How do we give callers **one simple way** to place an order, without
> deleting or rewriting the four specialised services underneath?

## The Goal

Provide a single entry point:

```java
OrderConfirmation confirmation = orderFacade.placeOrder(request);
```

...where the client:

- calls **one method** on **one object**,
- passes **one simple request object** in,
- gets **one simple confirmation object** back,
- and never learns that four separate subsystems exist.

Meanwhile the four services stay exactly as they are — independently
usable, independently testable, and untouched.

This is precisely the problem the **Facade** design pattern solves. See
[`facade-pattern-explained.md`](facade-pattern-explained.md) for how.
