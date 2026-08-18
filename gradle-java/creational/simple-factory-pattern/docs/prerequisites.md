# Prerequisites

What you need to know, and what you need installed, before working through
this Simple Factory demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Classes and objects** | Every participant is a plain class | Can you write a class with a constructor and call it with `new`? |
| **Interfaces** | The whole pattern rests on one | Can you say what `implements` gives you? |
| **Polymorphism** | The client calls `pay()` without knowing which class runs | Do you know why an interface-typed variable can hold different objects? |
| **Enums** | `PaymentType` names the choice | Can you loop over `SomeEnum.values()`? |
| **`switch`** | The factory is one switch | Have you seen `case X ->` arrow syntax? |
| **Exceptions** | The factory throws `IllegalArgumentException` on bad input | Do you know what `throw new SomeException(...)` does? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **Java `record`** (Java 16+) | `PaymentRequest`, `PaymentReceipt` |
| **`sealed` interfaces** (Java 17+) | `PaymentMethod` |
| **Switch expressions** (Java 14+) | `PaymentMethodFactory.create` |
| **`static` methods** | The factory's entry points |
| **JUnit 5 basics**, including `@ParameterizedTest` | `PaymentMethodFactoryTest` |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- Databases, web servers, or real payment APIs
- Generics, threading, or reflection
- Any other design pattern

## A 60-Second `record` Primer

If you have never seen a Java `record`, this is all you need:

```java
public record PaymentReceipt(String transactionId, String method, double amount) { }
```

That single line gives you:

- a constructor: `new PaymentReceipt("UPI-1", "UPI", 49.98)`
- accessors: `receipt.transactionId()` (note: **no** `get` prefix)
- sensible `equals()`, `hashCode()` and `toString()`
- immutability — the fields cannot be changed after construction

Think of it as "a class whose only job is to carry data", with the
boilerplate removed.

## A 60-Second `sealed` Primer

```java
public sealed interface PaymentMethod
        permits CreditCardPayment, UpiPayment, PayPalPayment, NetBankingPayment { }
```

`sealed` means *these four and nobody else may implement this interface*.
Each listed type must then be `final`, `sealed`, or `non-sealed`.

Why it earns its place here: because the compiler knows the complete list,
a `switch` covering every case needs no `default`. Add a fifth payment type
and the factory refuses to compile until you handle it — the mistake you
would otherwise find in production.

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
./gradlew run      # must print four payment runs
```

Expected output from `./gradlew run` (the first of four blocks):

```
Checkout: paying for ORD-1001 with Credit Card
Credit Card: authorising 49.98 for order ORD-1001
Credit Card: capturing the authorised amount
Checkout: done, transaction CC-XXXXXXXX
Receipt: PaymentReceipt[transactionId=CC-XXXXXXXX, method=Credit Card, amount=49.98]
```

The `XXXXXXXX` parts are randomly generated, so yours will differ. That is
expected. UPI, PayPal and Net Banking follow in the same shape.

## Verify the Tests

```bash
./gradlew test
```

Fourteen tests should pass. Open
`build/reports/tests/test/index.html` for the readable report.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `sealed`/`permits` not recognised | JDK older than 17 | Install JDK 21 |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`simple-factory-pattern-explained.md`](simple-factory-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/simplefactory/`
7. [`session.md`](session.md) — the guided walkthrough
