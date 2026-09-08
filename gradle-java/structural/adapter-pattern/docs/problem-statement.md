# Problem Statement

## The Scenario

You are building checkout for an online store. Checkout needs a shipping
cost for an order, given a destination ZIP code and a package weight in
kilograms — the units the rest of your codebase already uses everywhere
else. Your company has just signed a contract with a third-party carrier,
**Acme Shipping**, and their SDK is the only way to get real rates.

## Attempt One: Talk to the Third-Party SDK Directly

The SDK's shape does not match what checkout needs, at all:

```java
public final class AcmeShippingSdk {
    public long fetchCostInCents(String zip, double poundsMass) {
        // returns a price in integer cents, given weight in POUNDS
    }
}
```

Checkout works in kilograms and dollars. Acme works in pounds and cents,
and calls the method something entirely different from what the rest of
your code calls it. The obvious thing to do is convert, right where you
need the rate:

```java
public final class NaiveCheckoutService {
    private final AcmeShippingSdk sdk = new AcmeShippingSdk();

    public BigDecimal shippingCost(String destinationZip, double weightKg) {
        double weightLb = weightKg * 2.20462;
        long cents = sdk.fetchCostInCents(destinationZip, weightLb);
        return BigDecimal.valueOf(cents).divide(new BigDecimal("100"), 2, RoundingMode.HALF_UP);
    }
}
```

It works. Then a second, unrelated part of the codebase — say, a shipping
cost estimator shown earlier in the funnel, before checkout — also needs a
rate:

```java
public final class NaiveShippingEstimator {
    private final AcmeShippingSdk sdk = new AcmeShippingSdk();

    public BigDecimal estimate(String destinationZip, double weightKg) {
        double weightLb = weightKg * 2.20462;                 // duplicated
        long cents = sdk.fetchCostInCents(destinationZip, weightLb);
        return BigDecimal.valueOf(cents).divide(new BigDecimal("100"), 2, RoundingMode.HALF_UP);
    }
}
```

## Why That Hurts

- **The conversion is duplicated everywhere the SDK is used.** The
  pounds-per-kilogram constant and the cents-to-dollars division appear
  once per call site, copy-pasted, not shared.
- **Every caller is coupled to Acme's exact shape.** `NaiveCheckoutService`
  and `NaiveShippingEstimator` both know the method is called
  `fetchCostInCents`, both know the parameter order, both know the return
  type is `long` cents. If the business ever adds a second carrier as a
  fallback, both classes have to be taught about it individually.
- **Switching providers means touching every caller.** If Acme's contract
  ends and a different carrier (with yet another shape) replaces it, every
  class that called `AcmeShippingSdk` directly needs to change, one at a
  time.
- **Nothing here is a bug.** Both naive classes compute a correct shipping
  rate. The waste is structural: the *unit conversion* — a single,
  mechanical piece of logic — is scattered across every place that happens
  to need a rate.

## The Question This Project Answers

> How do we let checkout code depend on the shape *it* wants — kilograms in,
> dollars out — without checkout, or anything else, needing to know Acme's
> shape at all?

## The Goal

Write the conversion **exactly once**, behind the interface checkout
already expects:

```java
ShippingRateProvider rates = new AcmeShippingAdapter(new AcmeShippingSdk());
BigDecimal cost = rates.quoteRate("94107", 3.5);   // kilograms in, dollars out
```

Every caller — checkout, the estimator, anything written later — depends
only on `ShippingRateProvider`. Not one of them ever imports
`AcmeShippingSdk`.

This is precisely the problem the **Adapter** design pattern solves. See
[`adapter-pattern-explained.md`](adapter-pattern-explained.md) for how.
