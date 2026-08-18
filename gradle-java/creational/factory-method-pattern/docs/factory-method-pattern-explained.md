# The Factory Method Pattern — Explained

## One-Line Definition

> **Factory Method** defines an interface for creating an object, but lets
> subclasses decide which class to instantiate.

Put less formally: a class writes down *when* an object gets created and
what happens around it, then leaves a blank where the object's type should
be. Subclasses fill in the blank.

The "factory method" is not a class. It is a single method — here,
`createCourier()` — and it is the whole pattern.

It is a **creational** pattern from the original Gang of Four catalogue,
and one of the two factory patterns in that book (the other is Abstract
Factory).

## The Everyday Analogy

Think of a coffee shop chain. Head office writes the recipe card for
"serve a hot drink":

1. Greet the customer.
2. **Make the drink.**
3. Put a lid on it, call out the name, hand it over.

Steps 1 and 3 are identical in every branch worldwide — head office owns
them. Step 2 is deliberately left open: the Tokyo branch makes matcha, the
Rome branch makes espresso. Head office never learns what matcha is. It just
knows there is a step called "make the drink" and that whatever comes back
can have a lid put on it.

The recipe card is `DeliveryService.ship(...)`. "Make the drink" is
`createCourier()`. The branches are the subclasses.

## The Participants

| Role | In this project | Job |
| --- | --- | --- |
| Product | `Courier` | The interface the creator is allowed to see |
| Concrete Product | `PostalCourier`, `AirCourier`, `BikeCourier`, `GlobalCourier` | The real carriers |
| Creator | `DeliveryService` | Owns the workflow, declares the factory method |
| Concrete Creator | `StandardDelivery`, `ExpressDelivery`, `SameDayDelivery`, `InternationalDelivery` | Answers one question: which courier |
| Client | `FactoryMethodDemo` | Holds creators, never couriers |

## How This Project Implements It

### The product interface

```java
public interface Courier {
    String name();
    Shipment dispatch(Order order);
}
```

Two methods, no state, no hint of how any courier works. Note what is
missing: this interface is **not** `sealed`. In the sibling Simple Factory
project the product interface *is* sealed on purpose, so the compiler can
check the factory's `switch`. Here sealing would defeat the point — Factory
Method exists so new products can arrive from code you have never seen.

### The concrete products stay simple and independent

```java
public class AirCourier implements Courier {

    @Override
    public String name() {
        return "SkyLink Air";
    }

    @Override
    public Shipment dispatch(Order order) {
        System.out.println("SkyLink Air: booking " + order.orderId() + " onto tonight's flight");
        return new Shipment(TrackingIds.withPrefix("SL"), name(), 2, 12.50 + order.weightKg() * 1.20);
    }
}
```

Each courier knows its own name, its own tracking-number prefix, its own
speed and its own pricing. None of them knows another exists, and none of
them knows about delivery tiers.

### The creator writes the workflow with a hole in it

This is the heart of the pattern:

```java
public abstract class DeliveryService {

    /** The factory method. Every subclass answers this one question. */
    protected abstract Courier createCourier();

    /** A human-readable name for the service tier. */
    public abstract String tier();

    public final Shipment ship(Order order) {
        if (order.weightKg() <= 0) {
            throw new IllegalArgumentException("Order " + order.orderId() + " has no weight");
        }

        Courier courier = createCourier();

        System.out.println(tier() + ": preparing " + order.orderId()
                + " for " + order.destination() + " via " + courier.name());

        Shipment shipment = courier.dispatch(order);

        System.out.println(tier() + ": booked " + shipment.trackingId()
                + ", arriving in " + shipment.etaDays() + " day(s)");

        return shipment;
    }
}
```

Three things are worth staring at:

1. **`createCourier()` is abstract.** `DeliveryService` calls a method it
   does not implement. At runtime the call lands in the subclass. Control
   flows *down* the hierarchy and the result comes back *up* — that
   inversion is why this feels magical the first time.
2. **The return type is `Courier`, never a concrete class.** The creator can
   only call `name()` and `dispatch(...)`. Even though the object really is
   an `AirCourier`, this code cannot tell and does not care.
3. **`ship(...)` is `final`.** Subclasses vary *which courier*, never the
   steps around it. That guard on weight applies to every tier that will
   ever exist, including ones written next year by someone else.

### The concrete creators are tiny

```java
public class ExpressDelivery extends DeliveryService {

    @Override
    protected Courier createCourier() {
        return new AirCourier();
    }

    @Override
    public String tier() {
        return "Express";
    }
}
```

That is an entire delivery tier. Six lines. All four look like this.

Now count the `switch` statements in this project: zero. Count the `if`
statements that test a tier name: zero. The decision that used to be a
branch is now a class, and choosing a class is something Java's own dispatch
does for free.

### The client holds creators, not couriers

```java
List<DeliveryService> services = List.of(
        new StandardDelivery(),
        new ExpressDelivery(),
        new SameDayDelivery(),
        new InternationalDelivery());

for (DeliveryService service : services) {
    Shipment shipment = service.ship(order);
    System.out.println("Shipment: " + shipment);
}
```

One loop, one method call, four completely different carriers, four
different prices and delivery dates. The loop body has no idea any of that
is happening.

### Java 21 records as the data carriers

```java
public record Order(String orderId, String customerId, String destination, double weightKg) { }
public record Shipment(String trackingId, String carrier, int etaDays, double cost) { }
```

Immutable, with `equals`, `hashCode` and a readable `toString` supplied by
the compiler. That `toString` is what prints the tidy `Shipment[...]` line
in the demo output.

## What You Gain

- **Open/Closed, genuinely.** New tier, new file. No existing class changes.
  Compare with Simple Factory, where a new product means editing the
  factory's `switch`.
- **Shared behaviour has one home.** The weight guard and the log lines are
  written once. Fix a bug there and all tiers are fixed.
- **Extension from outside.** A separate module or jar can subclass
  `DeliveryService` and ship a tier your code has never heard of.
- **Testable in pieces.** You can test the workflow with a stub courier, and
  test each courier without any workflow at all. The test suite in this
  project does exactly that.
- **The compiler enforces the contract.** Forget to override
  `createCourier()` and your subclass will not compile.

## What to Watch Out For

- **A class per variant.** Four tiers means four subclasses. If the only
  difference between them really is one `new` call and nothing else, a
  Simple Factory or a `Supplier<Courier>` may be the honest choice — do not
  build a hierarchy to avoid a two-line `switch`.
- **You still have to pick a creator.** The pattern removes the branch from
  inside the workflow; it does not decide which `DeliveryService` to
  construct. In a real app that decision arrives from configuration or
  dependency injection, and if you write a `switch` to make it, you have
  quietly rebuilt a Simple Factory on top of Factory Method. That is fine —
  just know you did it.
- **Never call the factory method from a constructor.** The subclass's
  fields are not initialised yet, so the override can see `null`s. Call it
  from an ordinary method, as `ship(...)` does.
- **Keep the factory method's return type abstract.** The moment the creator
  declares `AirCourier createCourier()`, the coupling you removed is back.
- **Inheritance is a strong commitment.** A subclass is tied to its parent
  forever. If the workflow itself needs to vary too, look at Strategy
  (composition) before deepening the hierarchy.

## Factory Method vs. the Other Factory Patterns

| | Simple Factory | Factory Method | Abstract Factory |
| --- | --- | --- | --- |
| Is it in the GoF book? | No, an idiom | Yes | Yes |
| Mechanism | One static method with a `switch` | An abstract method, overridden | An interface with several creation methods |
| Adding a product means | Editing the factory | Adding a subclass | Editing every factory implementation |
| Creates | One product | One product | A family of related products |
| Needs inheritance? | No | Yes | Yes, of the factory |

A useful way to remember it: Simple Factory asks *a helper* which object to
build. Factory Method asks *itself*, and inheritance answers. Abstract
Factory asks a helper for a whole matching set.

## Where You Have Already Seen It

- `Collection.iterator()` — every collection creates its own `Iterator`
  implementation; your `for` loop only ever sees the interface.
- `Calendar.getInstance()` and `NumberFormat.getInstance()` in the JDK.
- `javax.xml.parsers.DocumentBuilderFactory.newDocumentBuilder()`.
- Android's `Activity.onCreateView(...)`, JUnit's own extension points, and
  most framework classes named `...Template` or `Abstract...Support`.

Anywhere a framework says "extend this class and override *one* method",
you are probably looking at Factory Method.

## Try It Yourself

1. **Add drone delivery.** Write `DroneCourier` and `DroneDelivery`, add one
   line to the demo's list. Confirm you never opened `DeliveryService`.
2. **Try to break the guard.** Ship an order with `weightKg` of `0` on any
   tier. Note that you did not have to write that check four times.
3. **Feel the difference.** Open the sibling project's
   `PaymentMethodFactory` and add a fifth payment method there. Compare how
   many existing files each change touched.
4. **Break it on purpose.** Delete the `createCourier()` override from
   `SameDayDelivery` and read the compiler error.
5. **Question the pattern.** If every subclass were literally just one
   `new` call and nothing else, would you still use it? Write down your
   answer before reading "What to Watch Out For" again.

## See Also

- [`problem-statement.md`](problem-statement.md) — the pain this removes
- [`class-diagram.md`](class-diagram.md) — the static structure
- [`uml-diagram.md`](uml-diagram.md) — the runtime sequence
- [`animation.html`](animation.html) — the flow, step by step
- [`prerequisites.md`](prerequisites.md) — what to know before you start
- [`../../simple-factory-pattern`](../../simple-factory-pattern) — the
  simpler idiom this pattern grows out of
