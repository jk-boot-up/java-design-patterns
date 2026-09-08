# Prerequisites

What you need to know, and what you need installed, before working through
this Decorator pattern demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Interfaces** | `PricedItem` is the shared type both `Product` and every decorator implement | Can you write an interface and two unrelated classes implementing it? |
| **Abstract classes** | `ProductDecorator` is abstract, holding shared state but no `cost()`/`description()` logic | Do you know when to use an abstract class instead of a plain interface? |
| **Composition (wrapping an object)** | Every decorator holds a `PricedItem` field and delegates to it before adding its own effect | Can you explain the difference between wrapping an object and extending it? |
| **`final` fields set in a constructor** | `ProductDecorator.wrapped` and `Product`'s fields are `private`/`protected final` | Do you know why a `final` field must be assigned in every constructor path? |
| **`BigDecimal` and rounding modes** | `InsuranceDecorator` computes a percentage fee with `BigDecimal.multiply(...).setScale(2, RoundingMode.HALF_UP)` | Do you know why money is usually not stored as `double`, and what `RoundingMode.HALF_UP` does? |
| **Recursive delegation** | `wrapped.cost()` may itself be another decorator's `cost()`, however many layers deep | Comfortable tracing a call through several nested wrapper objects? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **JUnit 5 basics** | Every `*Test.java` file |
| **`System.setOut` / stdout capturing** | `PricingDemoTest` |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- A real payment or checkout integration — this project only computes
  numbers, no network calls
- Any UI toolkit
- Any other design pattern

## A 60-Second "Decorator" Primer

If "add responsibilities to an object without changing its interface" feels
abstract, this is all you need:

```java
public interface PricedItem {                            // <-- the shared shape
    BigDecimal cost();
    String description();
}

public final class Product implements PricedItem { ... }  // <-- the plain component

public abstract class ProductDecorator implements PricedItem {
    protected final PricedItem wrapped;                    // <-- holds another PricedItem

    protected ProductDecorator(PricedItem wrapped) {
        this.wrapped = wrapped;
    }
}

public final class GiftWrapDecorator extends ProductDecorator {
    public BigDecimal cost() {
        return wrapped.cost().add(FEE);                    // <-- delegate, then add
    }
}
```

`GiftWrapDecorator` *is a* `PricedItem` and *has a* `PricedItem` at the same
time. That's the whole trick — it lets you wrap a wrapper, as many times as
you like.

## A 60-Second Component vs. Decorator Primer

- **Component** = the shared interface everything (plain or decorated)
  implements — `PricedItem`. Client code depends only on this.
- **Concrete Component** = the plain, undecorated object — `Product`.
- **Decorator** = a wrapper that also implements Component, and holds a
  reference to another Component instance to delegate to.

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
./gradlew run      # must print stacked decorator prices
```

Expected output from `./gradlew run` (abridged — see
[`../README.md`](../README.md) for the full transcript):

```
== Stacking decorators, one feature at a time ==
Wireless Headphones: $79.99
Wireless Headphones, gift-wrapped: $83.49
...
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| Insurance total looks off by a cent | Rounding mode differs from `HALF_UP`, or wrong stacking order | Check `RoundingMode` and decorator order in `InsuranceDecorator` |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`decorator-pattern-explained.md`](decorator-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/decorator/`
7. [`session.md`](session.md) — the guided walkthrough
