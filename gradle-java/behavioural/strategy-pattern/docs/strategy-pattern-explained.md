# The Strategy Pattern, Explained

> "Define a family of algorithms, encapsulate each one, and make them
> interchangeable. Strategy lets the algorithm vary independently from
> clients that use it."
> — Gang of Four, *Design Patterns*

## One Interface, Four Rules, No Branches

`CheckoutService` needs a delivery charge. It does not need to know how one
is arrived at. So the calculation is pulled out into an interface with a
single job:

```java
public interface ShippingCostRule {
    String name();
    Money costFor(Shipment shipment);
}
```

Each rule implements it and knows only its own arithmetic:

```java
public final class WeightBandedRule implements ShippingCostRule {
    @Override
    public Money costFor(Shipment shipment) {
        for (Band band : bands) {                     // lightest band first
            if (shipment.weightKg() <= band.upToKg()) {
                return band.cost();
            }
        }
        return overweightCost;
    }
}
```

And the client holds one, without ever asking which:

```java
public final class CheckoutService {
    private final ShippingCostRule shippingRule;

    public Quote quote(Shipment shipment) {
        Money delivery = shippingRule.costFor(shipment);   // the only line that matters
        return new Quote(shippingRule.name(), shipment.orderSubtotal(), delivery);
    }
}
```

That is the whole pattern. The `switch` did not move somewhere else and it
did not get smaller — it is *gone*, replaced by a method call on an object
that was chosen earlier by somebody else.

## Everyday Analogy: Getting Across Town

You want to get from the office to the station. You can walk, take a bus,
cycle, or get a taxi. *You* do not change: the same person, the same
starting point, the same destination. What changes is the method, and each
method has its own rules — a bus has a timetable, a taxi has a meter, a
bike needs somewhere to lock up.

The decision "which one today?" is made once, in the morning, based on the
weather and how late you are. It is not re-made at every street corner.
That separation — pick the approach once, then just *use* it — is Strategy.

## Participants

| Role | In This Project |
|---|---|
| **Strategy** | `ShippingCostRule` — the interface every pricing rule implements. |
| **Concrete Strategies** | `FlatRateRule`, `WeightBandedRule`, `DistanceBasedRule`, `FreeOverThresholdRule` — one algorithm each. |
| **Context** | `CheckoutService` — holds one rule, calls it, and never inspects it. |
| **Data passed to the strategy** | `Shipment` — everything any rule might need, so the interface never has to change. |
| **Selection** | `ShippingRules` — maps a configuration name onto the rule it selects. |
| **The trap** | `NaiveCheckoutService` + `ShippingMethod` — one method branching on an enum. |

## Code Walkthrough

**The strategy interface** — deliberately tiny. Two methods, no state:

```java
public interface ShippingCostRule {
    String name();
    Money costFor(Shipment shipment);
}
```

`name()` is there so the receipt can say which rule priced it. A strategy
that can describe itself saves the client from a lookup table of display
names, which would be the branch coming back in disguise.

**The parameter object** — one type carrying everything any rule could
want:

```java
public record Shipment(String destination, double weightKg,
                       int distanceMiles, Money orderSubtotal) { }
```

`FlatRateRule` reads none of these fields. `FreeOverThresholdRule` reads
only `orderSubtotal`. That is intentional: if `costFor` took just a weight,
the distance rule could not exist, and adding it would change the interface
and therefore every rule. Passing a whole `Shipment` is what makes new
rules cost one class.

**A rule that ignores everything** — the simplest possible strategy, and
worth keeping for exactly that reason:

```java
public final class FlatRateRule implements ShippingCostRule {
    private final Money fee;

    @Override
    public Money costFor(Shipment shipment) {
        return fee;                                   // reads nothing
    }
}
```

**The context** — note what is *not* here:

```java
public Quote quote(Shipment shipment) {
    Objects.requireNonNull(shipment, "shipment");
    Money delivery = shippingRule.costFor(shipment);
    return new Quote(shippingRule.name(), shipment.orderSubtotal(), delivery);
}
```

No `if`. No `instanceof`. No enum. `CheckoutService` cannot behave
differently depending on which rule it holds, because it has no way to find
out.

## Where the Branch Actually Went

The honest version of the story: something still has to turn a
configuration value into an object. In this project that is
`ShippingRules`:

```java
BY_NAME.put("flat", new FlatRateRule(Money.pounds(4.99)));
BY_NAME.put("weight", WeightBandedRule.standard());
```

At a glance this looks like the `switch` we just deleted. The difference is
what it does and how often:

- The naive `switch` ran **inside the pricing logic, on every quote**, and
  tangled the decision with the arithmetic so neither could be tested
  alone.
- The registry runs **once, at the edge**, and answers a different
  question: which rule is configured today. Nothing downstream branches
  again.

In a real store this lookup is a database table or a feature flag, which is
the same point made more plainly: the mapping is *data*, and the pricing
code never sees it.

## Why the Tests Are the Proof

Any test of the form "a 6.5 kg parcel costs £12.00" passes against the
naive design too. It says nothing about whether the pattern was applied.
The tests that would actually fail if somebody put the `switch` back are
the interaction tests:

```java
@Test
void acceptsARuleDefinedEntirelyInThisTest() {
    ShippingCostRule pricePerKilo = new ShippingCostRule() {
        public String name() { return "Per kilo"; }
        public Money costFor(Shipment s) { return Money.pounds(s.weightKg()); }
    };

    assertEquals(Money.pounds(6.50), new CheckoutService(pricePerKilo).quote(PARCEL).delivery());
}
```

Nothing in `src/main` knows this rule exists. That it works unchanged is
the property the pattern buys, and it is not something arithmetic tests can
demonstrate.

## What You Gain

- **A new rule is one new class.** No existing file is edited, so nothing
  that already works can be broken by adding to the family.
- **Each algorithm is separately testable.** `DistanceBasedRule`'s
  round-up-to-the-next-hundred-miles rule gets its own named test, instead
  of being an unexplained `+ 99` in a shared method.
- **Rules can come from outside.** A test, a region module or a partner
  integration can supply a rule the core code has never heard of.
- **The choice is a runtime value.** Swapping the campaign rule in and out
  is a configuration change, not a deployment of new branching logic.
- **There is no `default` to fall off.** The naive version's `default`
  charged nothing; here, an unrecognised rule name is rejected loudly by
  the registry before any pricing happens.

## What to Watch Out For

- **Strategies must be stateless with respect to a single call.** A rule
  that remembers the last shipment it priced cannot be shared between
  concurrent checkouts. `ShippingCostRule`'s contract says so explicitly,
  and the registry hands out shared instances on that basis.
- **Do not let the client ask what it is holding.** The moment somebody
  writes `if (rule instanceof FreeOverThresholdRule)`, the branch is back
  and the pattern is decoration.
- **The interface should not grow per rule.** If a new rule needs a field
  no other rule has, add it to `Shipment`, not to `ShippingCostRule` — a
  method that only one implementation meaningfully implements is a sign the
  family has stopped being a family.
- **Four classes instead of one method is a real cost.** For two rules that
  will never change, the `switch` is the better answer. Strategy pays for
  itself when the family is open-ended, which delivery pricing genuinely
  is.
- **In modern Java a strategy is often a lambda.** `ShippingCostRule` has
  two methods here so rules can name themselves; a single-method strategy
  would be a `Function<Shipment, Money>` and needs no classes at all. That
  is still the pattern.

## Strategy vs. State vs. Template Method vs. Simple Factory

| Pattern | Purpose | Tell |
|---|---|---|
| **Strategy** | Interchangeable algorithms for one job, chosen from outside. | The client is handed the strategy and never changes it on its own. |
| **State** | Behaviour that changes as an object moves through a lifecycle. | The objects *replace each other*, and they decide the successor. |
| **Template Method** | One fixed sequence of steps with some steps overridden. | Inheritance, and the skeleton is in the base class. |
| **Simple Factory** | Choosing which object to build. | It returns an object; it does not do the work. |

Strategy and State are the same *shape* — an interface, several
implementations, a context holding one. The distinction is who chooses and
how often: with Strategy the choice comes from outside and stays put; with
State the object swaps itself for another as events arrive. That comparison
is worked through properly in the State project.

## Where You Have Already Seen It

- **`Comparator`** — the archetype. `List.sort(comparator)` is a context
  taking an ordering algorithm it knows nothing about.
- **`java.util.concurrent.RejectedExecutionHandler`** — what a thread pool
  should do when its queue is full, supplied as an object.
- **Spring's `PasswordEncoder`** — BCrypt, Argon2 or PBKDF2, chosen by
  configuration, behind one interface.
- **`javax.servlet.Filter` ordering, layout managers, cache eviction
  policies (LRU, LFU, FIFO)** — all the same move.

## Try It Yourself

1. Add a `LockerCollectionRule` that charges nothing when the destination
   is a locker and £3.00 otherwise. Register it under `"locker"`. Notice
   that no existing file changes except the registry.
2. Now do the same thing to `NaiveCheckoutService` and count the files you
   had to open.
3. Write a rule that combines two others — a weight-banded charge capped at
   the flat rate. Ask yourself whether it is still a strategy, and where
   the line is between this and a decorator.
4. Replace `FlatRateRule` with a lambda at the call site. Work out what you
   lost by doing so (hint: read the output of `checkout.ruleName()`).

## See Also

- [`problem-statement.md`](problem-statement.md) — the naive code this
  pattern replaces.
- [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
  — the static and dynamic views.
- [`session.md`](session.md) — a guided 60-minute walkthrough.
