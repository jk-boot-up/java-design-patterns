# Prerequisites

What you need to know, and what you need installed, before working through
this Strategy pattern demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need
comfortable familiarity with core Java.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Interfaces** | `ShippingCostRule` is the whole pattern — one interface, four implementations | Can you write an interface and two unrelated classes implementing it? |
| **Polymorphic dispatch** | `shippingRule.costFor(...)` runs different code depending on the object, with no branch in sight | Can you explain why the caller does not need to know the concrete type? |
| **Composition and constructor injection** | `CheckoutService` is handed its rule; it never creates one | Do you know why taking a collaborator as a constructor argument makes a class testable? |
| **`final` fields** | Every rule's constants and the context's rule reference are `private final` | Do you know why a `final` field must be assigned on every constructor path? |
| **Records** | `Shipment` and `Quote` are records with compact-constructor validation | Do you know what a record generates for you, and what a compact constructor is for? |
| **Anonymous classes** | The tests define a rule inline that `src/main` has never heard of | Can you implement an interface without naming a class? |
| **`switch` on enums** | The naive alternative is one, including its `default` trap | Do you know what happens when an enum gains a constant and a `switch` does not? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **JUnit 5 basics, including `@Nested`** | Every `*Test.java` file |
| **`AtomicInteger` as a call counter** | `CheckoutServiceTest` |
| **Integer arithmetic that rounds up** | `DistanceBasedRule` |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework — the "injection" here is a
  constructor argument and nothing more
- A real courier or payments integration; this project only computes
  numbers
- Any other design pattern. If you have met Simple Factory, `ShippingRules`
  will look familiar, but nothing depends on that

## A 60-Second "Strategy" Primer

If "define a family of algorithms and make them interchangeable" feels
abstract, this is all you need:

```java
public interface ShippingCostRule {                  // <-- the strategy
    String name();
    Money costFor(Shipment shipment);
}

public final class FlatRateRule implements ShippingCostRule {   // <-- one algorithm
    public Money costFor(Shipment shipment) { return fee; }
}

public final class CheckoutService {                 // <-- the context
    private final ShippingCostRule shippingRule;     // <-- holds one, chosen outside

    public Quote quote(Shipment shipment) {
        Money delivery = shippingRule.costFor(shipment);   // <-- no branch, ever
        return new Quote(shippingRule.name(), shipment.orderSubtotal(), delivery);
    }
}
```

`CheckoutService` cannot behave differently depending on which rule it
holds, because it has no way of finding out which one that is. That is the
whole trick.

## A 60-Second Context vs. Strategy Primer

- **Strategy** = the interface describing the job to be done —
  `ShippingCostRule`. One method that matters, no state carried between
  calls.
- **Concrete Strategy** = one way of doing that job — `WeightBandedRule`.
  It knows its own arithmetic and nothing about checkout.
- **Context** = the class that needs the job done — `CheckoutService`. It
  holds a strategy, calls it, and never inspects it.
- **The choice** is made by whoever constructs the context. In this project
  that is `ShippingRules`; in a real store it is configuration.

## Software Prerequisites

| Tool | Minimum version | Check with |
| --- | --- | --- |
| **JDK** | 21 | `java -version` |
| **Gradle** | 8.x+ (or use the bundled wrapper) | `gradle -v` |
| **Git** | any recent | `git --version` |
| **IDE** | IntelliJ IDEA / VS Code / Eclipse | — |

### Installing JDK 21

**macOS (Homebrew)**
```bash
brew install --cask temurin@21
java -version
```

**Linux (SDKMAN)**
```bash
curl -s "https://get.sdkman.io" | bash
sdk install java 21-tem
```

**Windows** — download the Temurin 21 MSI from
[adoptium.net](https://adoptium.net) and run the installer.

Expected output:
```
openjdk version "21.0.1" 2023-10-17 LTS
```

### Gradle

You do not need to install Gradle — the project ships a wrapper:

```bash
./gradlew build     # macOS / Linux
gradlew.bat build   # Windows
```

The first run downloads the correct Gradle version automatically, so an
internet connection is needed once. If you already have Gradle installed,
plain `gradle build` works too.

## Verify Your Setup

Run these three commands from the project directory. All three must succeed
before the session.

```bash
java -version      # must report 21
./gradlew build    # must end with BUILD SUCCESSFUL
./gradlew run      # must print four rules priced against three shipments
```

Expected output from `./gradlew run` (abridged — see
[`../README.md`](../README.md) for the full transcript):

```
Four rules, priced against the same three shipments.

Rule "flat" -> Flat rate
  Edinburgh, 0.4kg, 45 miles, order £18.00
    Flat rate: subtotal £18.00 + delivery £4.99 = £22.99
...
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| Pound signs print as `?` or mojibake | Console is not UTF-8 | `chcp 65001` on Windows, or set `-Dfile.encoding=UTF-8` |
| `no shipping rule called "..."` | A rule name that is not registered | Use one of `flat`, `weight`, `distance`, `campaign` — the failure is deliberate, see `ShippingRules` |
| Distance prices look one unit high | Part-hundreds round **up** by design | Read `DistanceBasedRule` and its test |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`strategy-pattern-explained.md`](strategy-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/strategy/`
7. [`session.md`](session.md) — the guided walkthrough
