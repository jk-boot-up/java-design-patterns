# Prerequisites

What you need to know, and what you need installed, before working through
this Factory Method demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java — in particular, with inheritance.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Classes and objects** | Every participant is a plain class | Can you write a class with a constructor and call it with `new`? |
| **Interfaces** | `Courier` is the product interface | Can you say what `implements` gives you? |
| **Abstract classes** | `DeliveryService` is one | Do you know why you cannot write `new DeliveryService()`? |
| **Inheritance and `extends`** | Each tier is a subclass | Can you explain what a subclass inherits? |
| **Overriding and `@Override`** | The factory method is overridden four times | Do you know the difference between overriding and overloading? |
| **Polymorphism** | The creator calls `dispatch()` without knowing which courier runs | Do you know why an interface-typed variable can hold different objects? |
| **Exceptions** | `ship(...)` throws `IllegalArgumentException` on a weightless order | Do you know what `throw new SomeException(...)` does? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **Java `record`** (Java 16+) | `Order`, `Shipment` |
| **`abstract` methods** | `createCourier()`, `tier()` |
| **`final` methods** | `ship(...)` |
| **`protected` visibility** | `createCourier()` |
| **Anonymous classes** | The "new tier" test in `DeliveryServiceTest` |
| **JUnit 5 basics**, including `@ParameterizedTest` | `DeliveryServiceTest`, `CourierTest` |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- Databases, web servers, or real carrier APIs
- Generics, threading, or reflection
- Any other design pattern — though reading the sibling
  [`../../simple-factory-pattern`](../../simple-factory-pattern) first makes
  this one land harder

## A 60-Second `record` Primer

If you have never seen a Java `record`, this is all you need:

```java
public record Shipment(String trackingId, String carrier, int etaDays, double cost) { }
```

That single line gives you:

- a constructor: `new Shipment("SL-1A2B", "SkyLink Air", 2, 15.50)`
- accessors: `shipment.trackingId()` (note: **no** `get` prefix)
- sensible `equals()`, `hashCode()` and `toString()`
- immutability — the fields cannot be changed after construction

Think of it as "a class whose only job is to carry data", with the
boilerplate removed.

## A 60-Second `abstract` Primer

```java
public abstract class DeliveryService {

    protected abstract Courier createCourier();   // no body: subclasses must supply one

    public final Shipment ship(Order order) {     // has a body, and cannot be overridden
        Courier courier = createCourier();
        ...
    }
}
```

Three keywords are doing the work:

- **`abstract` on the class** means you cannot write `new DeliveryService()`.
  It exists only to be extended.
- **`abstract` on a method** means "there is a method here, but I refuse to
  say what it does". Any concrete subclass must override it or it will not
  compile.
- **`final` on a method** means the opposite: "this is settled, subclasses
  may not change it".

The surprising part, and the one worth pausing on: `ship(...)` *calls* a
method that has no body. At runtime the call lands in whichever subclass you
actually constructed. The parent wrote the call; the child chose the answer.

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
./gradlew run      # must print four delivery runs
```

Expected output from `./gradlew run` (the first of four blocks):

```
Standard: preparing ORD-2001 for Edinburgh via Royal Post
Royal Post: dropping ORD-2001 into the postal network
Standard: booked RP-XXXXXXXX, arriving in 5 day(s)
Shipment: Shipment[trackingId=RP-XXXXXXXX, carrier=Royal Post, etaDays=5, cost=5.24]
```

The `XXXXXXXX` parts are randomly generated, so yours will differ. That is
expected. Express, Same Day and International follow in the same shape.

## Verify the Tests

```bash
./gradlew test
```

Seventeen tests should pass. Open
`build/reports/tests/test/index.html` for the readable report.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `record` not recognised | JDK older than 16 | Install JDK 21 |
| `DeliveryService is abstract; cannot be instantiated` | You wrote `new DeliveryService()` | Construct a concrete tier instead |
| `does not override abstract method createCourier()` | A subclass is missing the override | Add it — this is the compiler enforcing the pattern |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`factory-method-pattern-explained.md`](factory-method-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/factorymethod/`
7. [`session.md`](session.md) — the guided walkthrough
