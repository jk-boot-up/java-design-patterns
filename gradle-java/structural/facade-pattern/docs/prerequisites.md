# Prerequisites

What you need to know, and what you need installed, before working through
this Facade pattern demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Classes and objects** | Every participant is a plain class | Can you write a class with a constructor and call it with `new`? |
| **Methods, parameters, return values** | The facade delegates by calling methods | Can you read a method signature and say what goes in and comes out? |
| **Fields and `private`/`public`** | The facade holds its subsystems in private fields | Do you know why a field would be `private final`? |
| **Interfaces vs. classes (basic)** | Helps you see why subsystems stay independent | Can you say what "coupling" loosely means? |
| **Exceptions** | The facade throws `IllegalStateException` when stock fails | Do you know what `throw new SomeException(...)` does? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **Java `record`** (Java 16+) | `OrderRequest`, `OrderConfirmation` |
| **`final` fields / immutability** | Facade's subsystem references |
| **Composition ("has-a")** | `OrderFacade` *has* four services |
| **JUnit 5 basics** | `OrderFacadeTest`, `SubsystemsTest` |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- Databases, web servers, or real payment APIs
- Threading, reactive programming, or generics beyond the basics
- Any other design pattern

## A 60-Second `record` Primer

If you have never seen a Java `record`, this is all you need:

```java
public record OrderConfirmation(String orderId, String paymentId, String trackingId) { }
```

That single line gives you:

- a constructor: `new OrderConfirmation("ORD-1", "PMT-1", "TRK-1")`
- accessors: `confirmation.orderId()` (note: **no** `get` prefix)
- sensible `equals()`, `hashCode()` and `toString()`
- immutability — the fields cannot be changed after construction

Think of it as "a class whose only job is to carry data", with the
boilerplate removed.

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

Run these four commands from the project directory. All four must succeed
before the session.

```bash
java -version      # must report 21
./gradlew build    # must end with BUILD SUCCESSFUL
./gradlew test     # 18 tests, across OrderFacadeTest and SubsystemsTest
./gradlew run      # must print the four subsystem lines
```

Expected output from `./gradlew run`:

```
Inventory: reserving 2 unit(s) of SKU-1234
Payment: charged $49.98 to customer CUST-001 (paymentId=PMT-XXXXXXXX)
Shipping: scheduled shipment for order ORD-XXXXXXXX to 221B Baker Street, London (trackingId=TRK-XXXXXXXX)
Notification: emailed customer CUST-001 confirmation for order ORD-XXXXXXXX (trackingId=TRK-XXXXXXXX)
Order placed: OrderConfirmation[orderId=ORD-XXXXXXXX, paymentId=PMT-XXXXXXXX, trackingId=TRK-XXXXXXXX]
```

The `XXXXXXXX` parts are randomly generated, so yours will differ. That is
expected.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`facade-pattern-explained.md`](facade-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/facade/`
7. [`session.md`](session.md) — the guided walkthrough
