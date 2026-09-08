# Prerequisites

What you need to know, and what you need installed, before working through
this Adapter pattern demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Interfaces** | `ShippingRateProvider` is the target type both `AcmeShippingAdapter` and `FlatRateShippingProvider` implement | Can you write an interface and two unrelated classes implementing it? |
| **Composition (wrapping an object)** | `AcmeShippingAdapter` holds an `AcmeShippingSdk` field and delegates to it | Can you explain the difference between wrapping an object and extending it? |
| **`final` fields set in a constructor** | `AcmeShippingAdapter.sdk` and `CheckoutService.shippingRateProvider` are both `private final` | Do you know why a `final` field must be assigned in every constructor path? |
| **`BigDecimal` and rounding modes** | Converting cents to dollars uses `BigDecimal.divide(..., 2, RoundingMode.HALF_UP)` | Do you know why money is usually not stored as `double`, and what `RoundingMode.HALF_UP` does? |
| **Unit conversion arithmetic** | kilograms → pounds, cents → dollars | Comfortable multiplying/dividing by a conversion constant? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **JUnit 5 basics** | Every `*Test.java` file |
| **`System.setOut` / stdout capturing** | `ShippingDemoTest` |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- A real shipping carrier integration — `AcmeShippingSdk` here is a stand-in
  that just does arithmetic, no network calls
- Any UI toolkit
- Any other design pattern

## A 60-Second "Adapter" Primer

If "convert an incompatible interface into the one clients expect" feels
abstract, this is all you need:

```java
public interface ShippingRateProvider {                 // <-- what clients want
    BigDecimal quoteRate(String destinationZip, double weightKg);
}

public final class AcmeShippingSdk {                     // <-- what we're given
    public long fetchCostInCents(String zip, double poundsMass) { ... }
}

public final class AcmeShippingAdapter implements ShippingRateProvider {
    private final AcmeShippingSdk sdk;                    // <-- holds the adaptee

    public BigDecimal quoteRate(String destinationZip, double weightKg) {
        double weightLb = /* convert kg to lb */;
        long cents = sdk.fetchCostInCents(destinationZip, weightLb);
        return /* convert cents to dollars */;
    }
}
```

`AcmeShippingAdapter` is the only class that ever mentions
`AcmeShippingSdk` by name. Everything else in the codebase — checkout,
tests, future callers — only ever sees `ShippingRateProvider`.

## A 60-Second Target vs. Adaptee Primer

- **Target** = the interface your code already depends on —
  `ShippingRateProvider`. This never changes to accommodate a new vendor.
- **Adaptee** = the existing class with the incompatible shape —
  `AcmeShippingSdk`. You typically do not own it and cannot change it.
- **Adapter** = the translator sitting between them, implementing Target
  and holding an Adaptee.

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
./gradlew run      # must print shipping quotes from both providers
```

Expected output from `./gradlew run` (abridged — see
[`../README.md`](../README.md) for the full transcript):

```
== Checkout works with any ShippingRateProvider, adapted or native ==
Acme (adapted):  $63.46
Flat rate (native):  $57.48
...
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| Quoted rate looks off by a cent | Rounding mode differs from `HALF_UP` | Check `RoundingMode` in `AcmeShippingAdapter` |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`adapter-pattern-explained.md`](adapter-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/adapter/`
7. [`session.md`](session.md) — the guided walkthrough
