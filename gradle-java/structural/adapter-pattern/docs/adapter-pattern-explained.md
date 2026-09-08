# The Adapter Pattern, Explained

> "Convert the interface of a class into another interface clients expect.
> Adapter lets classes work together that couldn't otherwise because of
> incompatible interfaces."
> — Gang of Four, *Design Patterns*

## One Seam, All the Conversion

`AcmeShippingSdk` speaks pounds and cents, with a method called
`fetchCostInCents`. Checkout speaks kilograms and dollars, and wants a
method called `quoteRate`. Nothing about either side is wrong — they were
simply designed independently, for different purposes.

The Adapter pattern puts one small class between them:

```java
public final class AcmeShippingAdapter implements ShippingRateProvider {
    private final AcmeShippingSdk sdk;

    @Override
    public BigDecimal quoteRate(String destinationZip, double weightKg) {
        double weightLb = toPounds(weightKg);
        long cents = sdk.fetchCostInCents(destinationZip, weightLb);
        return toDollars(cents);
    }
}
```

Every unit conversion, every method-name translation, lives in this one
class. Callers never see `AcmeShippingSdk` at all.

## Everyday Analogy: The Wall Plug Adapter

A laptop charger built for a UK socket does not change when you travel to
the US — you do not rewire the charger. You plug a small adapter between
the charger and the US wall socket. The adapter's whole job is translating
one physical interface (US prongs) into another (UK prongs) it was never
designed to fit. The charger's own logic never changes; neither does the
wall socket's. Only the thin adapter in between knows about both shapes.

## Participants

| Role | In This Project |
|---|---|
| **Target** | `ShippingRateProvider` — the interface client code expects. |
| **Adaptee** | `AcmeShippingSdk` — the existing, incompatible class we cannot (or should not) change. |
| **Adapter** | `AcmeShippingAdapter` — implements `ShippingRateProvider`, wraps an `AcmeShippingSdk`, and translates every call. |
| **Client** | `CheckoutService` — depends only on `ShippingRateProvider`, never on `AcmeShippingSdk`. |
| **The trap** | `NaiveCheckoutService` / `NaiveShippingEstimator` — call `AcmeShippingSdk` directly, duplicating the conversion at every call site. |

`FlatRateShippingProvider` is a second, *natively* compatible
implementation of `ShippingRateProvider` — written from scratch, no
adapting needed. It exists to prove a point: `CheckoutService` cannot tell
the difference between an adapted implementation and a native one. Both
are just a `ShippingRateProvider` at the call site.

## Code Walkthrough

**The target interface** — this is the shape checkout was written against,
independent of any specific carrier:

```java
public interface ShippingRateProvider {
    BigDecimal quoteRate(String destinationZip, double weightKg);
}
```

**The adaptee** — third-party, cannot be changed, uses different units and
a different method name:

```java
public final class AcmeShippingSdk {
    public long fetchCostInCents(String zip, double poundsMass) { ... }
}
```

**The adapter** — the only class in the codebase that imports
`AcmeShippingSdk`:

```java
public final class AcmeShippingAdapter implements ShippingRateProvider {
    private static final BigDecimal KG_TO_LB = new BigDecimal("2.20462");
    private static final BigDecimal CENTS_PER_DOLLAR = new BigDecimal("100");
    private final AcmeShippingSdk sdk;

    public AcmeShippingAdapter(AcmeShippingSdk sdk) {
        this.sdk = sdk;
    }

    @Override
    public BigDecimal quoteRate(String destinationZip, double weightKg) {
        double weightLb = BigDecimal.valueOf(weightKg).multiply(KG_TO_LB).doubleValue();
        long cents = sdk.fetchCostInCents(destinationZip, weightLb);
        return BigDecimal.valueOf(cents).divide(CENTS_PER_DOLLAR, 2, RoundingMode.HALF_UP);
    }
}
```

**The client** — knows nothing about Acme, pounds, or cents:

```java
public final class CheckoutService {
    private final ShippingRateProvider shippingRateProvider;

    public BigDecimal totalWithShipping(BigDecimal itemsSubtotal, String destinationZip, double weightKg) {
        BigDecimal shipping = shippingRateProvider.quoteRate(destinationZip, weightKg);
        return itemsSubtotal.add(shipping);
    }
}
```

Swap in `new AcmeShippingAdapter(new AcmeShippingSdk())` or
`new FlatRateShippingProvider()` — `CheckoutService` does not change either
way.

## What You Gain

- **The conversion lives in exactly one place.** Fix a rounding bug once,
  and every caller is fixed.
- **Client code is decoupled from the third-party shape.** `CheckoutService`
  never imports `AcmeShippingSdk`; if Acme's SDK version changes its method
  signature, only `AcmeShippingAdapter` needs to change.
- **You can swap providers without touching the client.** A natively
  written `ShippingRateProvider` and an adapted one are interchangeable —
  `CheckoutService` cannot tell them apart, by design.
- **You can adapt a class you don't own.** You never need write access to
  `AcmeShippingSdk`'s source to make it fit your interface.

## What to Watch Out For

- **Adapter is not a place to add new behavior.** If `AcmeShippingAdapter`
  started adding retry logic or caching, it would be doing more than
  adapting — that belongs in a decorator, not here.
- **One adapter per incompatible source.** If you integrate a second
  carrier later, write a second adapter (`OtherCarrierAdapter`) implementing
  the same `ShippingRateProvider` — don't grow one adapter to branch on
  which SDK it's wrapping.
- **Don't adapt what you already control.** If you own both sides of an
  interface mismatch, it is usually cheaper to just change one side to
  match the other, rather than add a permanent translation layer.

## Adapter vs. Bridge vs. Decorator vs. Facade

| Pattern | Purpose | Shape |
|---|---|---|
| **Adapter** | Make an *existing, incompatible* interface fit one clients already expect. | One wrapper class translating calls, applied after the fact. |
| **Bridge** | Let an abstraction and an implementation vary *independently*, designed together up front. | Two hierarchies connected by composition, planned from the start. |
| **Decorator** | Add responsibilities to an object *without changing its interface*. | Same interface in and out, layered, stackable. |
| **Facade** | Simplify a *complex subsystem* behind one easy-to-use entry point. | One class hiding many, not necessarily translating a mismatched shape. |

Bridge is designed in advance, so both hierarchies are shaped for each
other from day one. Adapter is reactive — it exists because two things that
were **not** designed together need to cooperate anyway.

## Where You Have Already Seen It

- **`java.util.Arrays.asList(...)`** adapts an array to the `List`
  interface.
- **`InputStreamReader`** adapts a byte-oriented `InputStream` to the
  character-oriented `Reader` interface.
- **JDBC-ODBC bridges** (historically) adapted ODBC drivers to the JDBC
  `Driver` interface.
- **Every REST client wrapper** you have ever written around a vendor SDK,
  translating their DTOs into your domain objects, is an Adapter.

## Try It Yourself

1. Add a second carrier, `SwiftCourierSdk`, with its own quirky shape (say,
   it wants grams and returns a `String` like `"14.20"`). Write
   `SwiftCourierAdapter implements ShippingRateProvider` and prove
   `CheckoutService` works with it unmodified.
2. Write a test that constructs `CheckoutService` with each of the three
   providers (`AcmeShippingAdapter`, `FlatRateShippingProvider`, your new
   `SwiftCourierAdapter`) and asserts each produces *some* valid total —
   proving the client truly cannot tell them apart.
3. Try adapting in the other direction: write an adapter that makes
   `ShippingRateProvider` usable somewhere that expects Acme's exact
   `fetchCostInCents(String, double)` shape (a "reverse adapter"). Notice
   how much more awkward that is — you'd have to convert dollars back to
   cents and kilograms back to pounds, going the wrong way.

## See Also

- [`problem-statement.md`](problem-statement.md) — the naive code this
  pattern replaces.
- [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
  — the static and dynamic views.
- [`session.md`](session.md) — a guided 60-minute walkthrough.
