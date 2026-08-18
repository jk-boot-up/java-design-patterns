# Prerequisites

What you need to know, and what you need installed, before working through
this Abstract Factory demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java — in particular, with interfaces and with
programming against a type rather than a class.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Classes and objects** | Every participant is a plain class | Can you write a class with a constructor and call it with `new`? |
| **Interfaces** | There are four of them, and they carry the whole design | Can you say what `implements` gives you? |
| **Implementing several interfaces** | Nine products across three interfaces | Can you name two classes in the JDK that implement `List`? |
| **Polymorphism** | The client calls `taxOn(...)` without knowing whose | Do you know why an interface-typed field can hold different objects? |
| **Constructor injection** | The factory is handed in, never constructed inside | Can you explain why passing a dependency in beats creating it? |
| **`final` fields** | The client's three products never change after construction | Do you know when a `final` field must be assigned? |
| **Exceptions** | `quote(...)` throws `IllegalArgumentException` on a bad address | Do you know what `throw new SomeException(...)` does? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **Java `record`** (Java 16+) | `Order`, `Quote` |
| **`String.format`** and format specifiers | `PoundFormatter`, `DollarFormatter`, `RupeeFormatter` |
| **Regular expressions** | The three address validators |
| **Anonymous classes** | The "new market" test in `MarketFactoryTest` |
| **Local records** | `AbstractFactoryDemo` declares one inside `main` |
| **JUnit 5 basics**, including `@ParameterizedTest` | `MarketFactoryTest`, `CheckoutServiceTest` |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- Databases, web servers, or real tax APIs
- Generics, threading, or reflection
- Deep knowledge of regular expressions — the three used here are read-only
  scenery, and the doc explains what each one accepts
- Real tax law. The rates here are plausible round numbers chosen to make the
  arithmetic easy to follow, not advice.
- Any other design pattern — though reading the two siblings first,
  [`../../simple-factory-pattern`](../../simple-factory-pattern) then
  [`../../factory-method-pattern`](../../factory-method-pattern), makes this
  one land much harder

## A 60-Second `record` Primer

If you have never seen a Java `record`, this is all you need:

```java
public record Order(String orderId, String customerId, double subtotal, String postcode) { }
```

That single line gives you:

- a constructor: `new Order("ORD-3001", "CUST-001", 120.00, "EH1 1YZ")`
- accessors: `order.subtotal()` (note: **no** `get` prefix)
- sensible `equals()`, `hashCode()` and `toString()`
- immutability — the fields cannot be changed after construction

Think of it as "a class whose only job is to carry data", with the
boilerplate removed.

## A 60-Second "Family" Primer

This pattern rests on one idea, and it is worth being sure of it before you
read any code.

Three interfaces, three implementations each. That is a **grid**:

| | `TaxCalculator` | `CurrencyFormatter` | `AddressValidator` |
| --- | --- | --- | --- |
| **UK** | `UkVatCalculator` | `PoundFormatter` | `UkPostcodeValidator` |
| **US** | `UsSalesTaxCalculator` | `DollarFormatter` | `UsZipValidator` |
| **India** | `IndiaGstCalculator` | `RupeeFormatter` | `IndiaPinValidator` |

Reading it **down a column** gives you an ordinary interface and its
implementations — nothing new.

Reading it **across a row** gives you a *family*: three objects that were
designed to be used together. Nine cells, but only three legal selections.

Abstract Factory exists so that a client can pick a row and never see a cell.
Everything else in this project is detail.

## A 60-Second "Program to the Interface" Primer

```java
private final TaxCalculator tax;    // the type is the interface
...
this.tax = factory.createTaxCalculator();   // the object is whatever arrived
```

The field's *declared* type is `TaxCalculator`, so this code may only call
`label()` and `taxOn(...)`. The object at runtime really is a
`UkVatCalculator`, but nothing here can find that out, and nothing here wants
to.

That gap between "what the code can see" and "what the object actually is" is
where every factory pattern does its work. If the field were declared
`UkVatCalculator`, there would be no pattern and no point.

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

### A note on the currency symbols

The output contains `£`, `$` and `₹`. If your terminal prints question marks
or boxes instead, your console is not using UTF-8. On Windows, run
`chcp 65001` first; on Linux, check that your locale ends in `.UTF-8`. The
program is fine — only the display is not.

## Verify Your Setup

Run these three commands from the project directory. All three must succeed
before the session.

```bash
java -version      # must report 21
./gradlew build    # must end with BUILD SUCCESSFUL
./gradlew run      # must print three market runs, then a rejection
```

Expected output from `./gradlew run` (the first of three blocks):

```
Checkout: United Kingdom order ORD-3001 to postcode EH1 1YZ
Checkout: VAT of £24.00 on £120.00
Checkout: total £144.00 GBP
Quote: Quote[market=United Kingdom, subtotal=£120.00, taxLabel=VAT, tax=£24.00, total=£144.00]
```

Unlike the sibling projects, nothing here is random — your output should match
exactly. The United States and India blocks follow in the same shape, and the
run ends with:

```
Rejected: "EH1 1YZ" is not a valid United States ZIP code
```

That last line is the demo deliberately trying to mix markets and being
stopped.

## Verify the Tests

```bash
./gradlew test
```

Eighteen tests should pass. Open
`build/reports/tests/test/index.html` for the readable report.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `record` not recognised | JDK older than 16 | Install JDK 21 |
| `£` prints as `?` or a box | Console is not UTF-8 | `chcp 65001` on Windows; check your locale elsewhere |
| `MarketFactory is abstract; cannot be instantiated` | You wrote `new MarketFactory()` | Construct a concrete factory instead |
| `does not override abstract method createAddressValidator()` | A factory is missing a method | Add it — this is the compiler enforcing the family |
| A valid postcode is rejected | Wrong market's validator | Check which factory the checkout was built with |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`abstract-factory-pattern-explained.md`](abstract-factory-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure and the families
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/abstractfactory/`
7. [`session.md`](session.md) — the guided walkthrough
