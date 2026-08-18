# The Facade Pattern — Explained

## One-Line Definition

> **Facade** provides a simplified, unified interface to a set of
> interfaces in a subsystem, making the subsystem easier to use.
> — *Gang of Four, Design Patterns*

It is a **structural** pattern: it is about how classes are *composed*,
not about how objects are created or how they behave over time.

## The Everyday Analogy

Think of a **restaurant waiter**.

You do not walk into the kitchen and speak to the grill chef, the sauce
chef, the pastry chef and the dishwasher individually. You talk to **one
person** — the waiter — and say *"I'll have the steak."*

The waiter knows:

- which chefs to talk to,
- in what order,
- and what to bring back to you.

The kitchen staff still exist and still do specialised work. You are simply
shielded from that complexity. **The waiter is a facade.**

In this project, `OrderFacade` is the waiter and the four services are the
kitchen staff.

## The Participants

| Role | In this project | Job |
| --- | --- | --- |
| **Facade** | `OrderFacade` | Exposes one simple method; knows which subsystems to call and in what order |
| **Subsystem classes** | `InventoryService`, `PaymentService`, `ShippingService`, `NotificationService` | Do the real specialised work; know *nothing* about the facade |
| **Client** | `FacadeDemo` | Talks only to the facade |

A crucial detail: **the dependency arrow points one way only.** The facade
knows about the subsystems. The subsystems do not know about the facade.
This is what keeps them independently reusable.

## How This Project Implements It

### The subsystems stay simple and independent

Each service does exactly one thing and has no idea a facade exists:

```java
public class InventoryService {
    public boolean reserveStock(String productId, int quantity) {
        System.out.println("Inventory: reserving " + quantity + " unit(s) of " + productId);
        return true;
    }
}
```

`PaymentService`, `ShippingService` and `NotificationService` follow the
same shape. You could use any of them on their own tomorrow.

### The facade owns and orchestrates them

```java
public class OrderFacade {

    private final InventoryService inventoryService;
    private final PaymentService paymentService;
    private final ShippingService shippingService;
    private final NotificationService notificationService;

    public OrderConfirmation placeOrder(OrderRequest request) {
        String orderId = "ORD-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();

        if (!inventoryService.reserveStock(request.productId(), request.quantity())) {
            throw new IllegalStateException("Product " + request.productId() + " is out of stock");
        }

        String paymentId = paymentService.charge(request.customerId(), request.amount());
        String trackingId = shippingService.scheduleShipment(orderId, request.shippingAddress());
        notificationService.sendOrderConfirmation(request.customerId(), orderId, trackingId);

        return new OrderConfirmation(orderId, paymentId, trackingId);
    }
}
```

Notice what the facade is really providing:

- **Sequencing** — stock first, payment second, shipping third, email last.
- **A guard rail** — if stock cannot be reserved, it stops before charging
  anyone's card.
- **Assembly** — it gathers three separate results into one
  `OrderConfirmation`.

### The client stays blissfully ignorant

```java
OrderFacade orderFacade = new OrderFacade();
OrderRequest request = new OrderRequest("CUST-001", "SKU-1234", 2, 49.98, "221B Baker Street, London");

OrderConfirmation confirmation = orderFacade.placeOrder(request);
```

Three lines. No knowledge of inventory, payment, shipping or email.

### Java 21 records as the data carriers

`OrderRequest` and `OrderConfirmation` are `record` types — immutable data
holders with automatic constructors, accessors, `equals`, `hashCode` and
`toString`:

```java
public record OrderConfirmation(String orderId, String paymentId, String trackingId) { }
```

Records keep the facade's signature clean: one object in, one object out,
instead of a method with five parameters returning three values.

## What You Gain

- **Loose coupling.** The client depends on one class instead of four.
- **A single place for the workflow.** Change the order of operations once,
  and every caller benefits.
- **Freedom to refactor.** Swap `PaymentService` for a new provider and no
  client code changes.
- **Easy testing.** Test the workflow through one entry point.
- **A readable API.** `placeOrder(request)` says what it does.

## What to Watch Out For

- **A facade is not a god object.** If `OrderFacade` starts holding
  business rules, validation, tax logic and reporting, it has stopped being
  a facade. Keep it thin — its job is *delegation and sequencing*.
- **Do not forbid direct access.** The subsystems should remain public and
  usable. A facade is a convenience, not a wall. An admin tool that only
  needs to check stock should be free to call `InventoryService` directly.
- **One facade per workflow, not one per application.** If checkout,
  returns, and refunds are all different flows, they may deserve their own
  facades.

## Facade vs. Similar Patterns

| Pattern | Intent | Key difference |
| --- | --- | --- |
| **Facade** | Simplify a complex subsystem | Wraps *many* objects; interface is new and simpler |
| **Adapter** | Make an incompatible interface usable | Wraps *one* object; interface is dictated by the client's expectation |
| **Mediator** | Coordinate peer objects | Peers *know* the mediator and talk back to it; subsystems never know a facade |
| **Proxy** | Control access to one object | Same interface as the object it wraps, not a simpler one |

The shortest way to remember it: **Adapter changes an interface. Facade
simplifies many of them.**

## Where You Have Already Seen It

- `javax.faces.context.FacesContext` in Java EE
- Spring's `JdbcTemplate` — hides `Connection`, `Statement`, `ResultSet`
  and all the exception handling behind a few simple methods
- SLF4J's `LoggerFactory`
- A REST controller that calls several services and returns one response is
  usually acting as a facade

## Try It Yourself

1. Run `./gradlew run` and read the output — each line is one subsystem
   speaking.
2. Add a `FraudCheckService` and call it from the facade *before* payment.
   Notice that `FacadeDemo` needs **zero** changes.
3. Make `InventoryService.reserveStock` return `false` and confirm the
   customer is never charged.

## See Also

- [`problem-statement.md`](problem-statement.md) — the problem this solves
- [`class-diagram.md`](class-diagram.md) — static structure
- [`uml-diagram.md`](uml-diagram.md) — runtime call flow
- [`animation.html`](animation.html) — animated walkthrough
