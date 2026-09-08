# The Decorator Pattern, Explained

> "Attach additional responsibilities to an object dynamically. Decorators
> provide a flexible alternative to subclassing for extending
> functionality."
> — Gang of Four, *Design Patterns*

## Wrapping, Not Subclassing

`Product` knows its own price and name. `GiftWrapDecorator`,
`InsuranceDecorator`, and `ExpressHandlingDecorator` each know how to add
*one* fee and *one* description suffix on top of whatever they wrap. None of
them know or care whether they are wrapping a plain `Product` or another
decorator — they only depend on the shared `PricedItem` interface.

```java
public interface PricedItem {
    BigDecimal cost();
    String description();
}

public abstract class ProductDecorator implements PricedItem {
    protected final PricedItem wrapped;

    protected ProductDecorator(PricedItem wrapped) {
        this.wrapped = wrapped;
    }
}

public final class GiftWrapDecorator extends ProductDecorator {
    private static final BigDecimal FEE = new BigDecimal("3.50");

    @Override
    public BigDecimal cost() { return wrapped.cost().add(FEE); }

    @Override
    public String description() { return wrapped.description() + ", gift-wrapped"; }
}
```

Because `GiftWrapDecorator` implements `PricedItem` *and* wraps a
`PricedItem`, decorators nest arbitrarily deep. Each layer adds its own fee
on top of whatever total the layer beneath it already computed.

## Everyday Analogy: Dressing for Weather

A base outfit (a shirt) can have a sweater put on over it, and a raincoat
put on over the sweater. Each layer adds its own effect — warmth, then
water resistance — without the shirt needing to know a raincoat exists, or
the raincoat needing to know what's underneath it. You can wear any subset
of layers, in the order that makes sense, without owning a distinct garment
for every combination of "shirt+sweater," "shirt+raincoat," and
"shirt+sweater+raincoat."

## Participants

| Role | In This Project |
|---|---|
| **Component** | `PricedItem` — the interface both plain products and decorated products share. |
| **Concrete Component** | `Product` — a plain item with a name and a price, no extras. |
| **Decorator** | `ProductDecorator` — abstract base holding a wrapped `PricedItem` by composition. |
| **Concrete Decorators** | `GiftWrapDecorator`, `InsuranceDecorator`, `ExpressHandlingDecorator` — each adds one fee and one description suffix. |
| **The trap** | `NaiveGiftWrappedProduct` / `NaiveInsuredProduct` / `NaiveGiftWrappedInsuredProduct` — one hardcoded class per combination. |

## Code Walkthrough

**The component interface** — the shape every priceable thing shares,
decorated or not:

```java
public interface PricedItem {
    BigDecimal cost();
    String description();
}
```

**The concrete component** — a plain product, no extras:

```java
public final class Product implements PricedItem {
    private final String name;
    private final BigDecimal price;

    @Override public BigDecimal cost() { return price; }
    @Override public String description() { return name; }
}
```

**The abstract decorator** — holds the wrapped item, implements nothing
else:

```java
public abstract class ProductDecorator implements PricedItem {
    protected final PricedItem wrapped;

    protected ProductDecorator(PricedItem wrapped) {
        this.wrapped = wrapped;
    }
}
```

**A concrete decorator that adds a percentage-based fee** — this one is
worth reading closely:

```java
public final class InsuranceDecorator extends ProductDecorator {
    private static final BigDecimal RATE = new BigDecimal("0.02");

    @Override
    public BigDecimal cost() {
        BigDecimal base = wrapped.cost();
        BigDecimal premium = base.multiply(RATE).setScale(2, RoundingMode.HALF_UP);
        return base.add(premium);
    }
}
```

`InsuranceDecorator` calls `wrapped.cost()` — whatever that returns, insured
or not, gift-wrapped or not. It has no idea what it is wrapping.

## Stacking Order Matters

Because `InsuranceDecorator` prices a *percentage of whatever it wraps*,
wrapping order changes the total. Insuring the gift wrap fee is not the same
as gift-wrapping an already-insured item:

```java
PricedItem giftWrappedThenInsured = new InsuranceDecorator(new GiftWrapDecorator(product));
PricedItem insuredThenGiftWrapped = new GiftWrapDecorator(new InsuranceDecorator(product));

giftWrappedThenInsured.cost();   // $85.16 -- insurance premium includes the gift-wrap fee
insuredThenGiftWrapped.cost();   // $85.09 -- gift-wrap fee is flat, added after insurance
```

Both are legitimate prices for reasonable-sounding but different policies.
Decorator does not hide this — it makes stacking order an explicit,
visible choice at the call site, rather than a decision buried inside one
combination class.

## What You Gain

- **New optional features cost one class, not several.** Adding express
  handling required exactly one new decorator; it works with every existing
  decorator and the plain product, immediately, in any position.
- **Fee logic lives in exactly one place per feature.** Fix the insurance
  rate once, in `InsuranceDecorator`, and every stack that includes it is
  fixed.
- **Combinations are runtime choices, not compile-time classes.** Which
  extras a customer picked becomes a matter of which decorators you
  construct, not which of N pre-written classes you happen to have.
- **Decorators are interchangeable with the component they wrap.** A
  `GiftWrapDecorator` *is a* `PricedItem`, so it can be wrapped again by
  another decorator, or handed to any code that only knows about
  `PricedItem`.

## What to Watch Out For

- **Decorators should not change the interface.** Every decorator here
  still exposes exactly `cost()` and `description()` — nothing more. A
  decorator that bolts on new methods breaks substitutability for existing
  callers.
- **Order-sensitive decorators need documentation.** `InsuranceDecorator`'s
  percentage-based fee makes stacking order visible and meaningful; if that
  is not obvious from the code, say so, the way this project's tests and
  demo do explicitly.
- **Too many stacked decorators can get hard to read.** A `PricedItem`
  wrapped five layers deep is correct, but debugging "which layer added this
  fee" gets harder with each layer. Keep decorators small and named for
  exactly what they add.

## Decorator vs. Adapter vs. Bridge vs. Facade

| Pattern | Purpose | Shape |
|---|---|---|
| **Decorator** | Add responsibilities to an object *without changing its interface*. | Same interface in and out, layered, stackable. |
| **Adapter** | Make an *existing, incompatible* interface fit one clients already expect. | One wrapper class translating calls, applied after the fact. |
| **Bridge** | Let an abstraction and an implementation vary *independently*, designed together up front. | Two hierarchies connected by composition, planned from the start. |
| **Facade** | Simplify a *complex subsystem* behind one easy-to-use entry point. | One class hiding many, not necessarily preserving the wrapped shape. |

Decorator and Adapter both wrap an object, but for opposite reasons:
Adapter changes the interface so two incompatible shapes can work together;
Decorator deliberately keeps the *same* interface so wrapped and unwrapped
objects remain interchangeable.

## Where You Have Already Seen It

- **`java.io` stream wrappers** — `BufferedInputStream`,
  `GZIPInputStream`, and `DataInputStream` all wrap an `InputStream` and
  are themselves `InputStream`s, stackable in any combination.
- **`Collections.unmodifiableList(...)` / `synchronizedList(...)`** wrap a
  `List` and return something that is still a `List`.
- **Servlet filters and HTTP middleware chains** each wrap the next handler,
  adding behavior (logging, auth, compression) before or after delegating.
- **Coffee-shop pricing demos** (a classic teaching example): a base
  beverage decorated with milk, syrup, and whipped cream, each adding a
  cost — structurally identical to this project's `Product` and fee
  decorators.

## Try It Yourself

1. Add a `DiscountDecorator` that subtracts a flat amount from whatever it
   wraps (clamped so cost never goes below zero). Prove it can be placed
   anywhere in an existing stack.
2. Write a test that stacks all four decorators (gift wrap, insurance,
   express handling, your new discount) in two different orders and shows
   the totals differ.
3. Try implementing `NaiveDiscountedGiftWrappedInsuredProduct` by hand for
   the naive classes in this project, and count how many total naive
   classes a fourth feature demands to cover every combination.

## See Also

- [`problem-statement.md`](problem-statement.md) — the naive code this
  pattern replaces.
- [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
  — the static and dynamic views.
- [`session.md`](session.md) — a guided 60-minute walkthrough.
