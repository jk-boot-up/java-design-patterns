# Prerequisites

What you need to know, and what you need installed, before working through
this Composite pattern demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Interfaces** | `CatalogComponent` is the shared type both `Product` and `Category` implement | Can you write an interface and two classes implementing it? |
| **Recursion** | `Category.totalPrice()` calls `totalPrice()` on its own children | Can you trace what `Category.totalPrice()` returns for a category containing another category? |
| **Collections (`List`)** | `Category` holds its children in a `List<CatalogComponent>` | Can you loop over a `List` and call a method on each element? |
| **`instanceof` and its cost** | The naive trap uses `instanceof` chains; the pattern removes them | Do you understand why `instanceof NaiveProduct` / `instanceof NaiveCategory` has to be repeated in three separate methods? |
| **`BigDecimal`** | Prices are `BigDecimal`, not `double`, to avoid floating-point rounding | Do you know why money is usually not stored as `double`? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **Fluent builder-style methods** | `Category.add(...)` returns `this` so calls can be chained |
| **`Collections.unmodifiableList`** | `Category.children()`, so callers cannot mutate the tree by accident |
| **JUnit 5 basics** | Every `*Test.java` file |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- A real database or persistence layer — the catalog tree lives entirely
  in memory, built by one method in `CatalogDemo`
- Any UI toolkit
- Any other design pattern

## A 60-Second Recursion Primer

If tree recursion feels unfamiliar, this is all you need:

```java
int countAll(Category c) {
    int count = 0;
    for (CatalogComponent child : c.children()) {
        if (child instanceof Product) {
            count += 1;
        } else if (child instanceof Category nested) {
            count += countAll(nested);   // the function calls itself, one level down
        }
    }
    return count;
}
```

Composite's whole point is that you never have to write the `if`/`else if`
above. `Category.productCount()` calls `child.productCount()` regardless of
what `child` actually is — a `Product` answers `1` directly, a nested
`Category` answers by running this exact same logic on its own children.
The recursion is still happening; it is just hidden inside a single
polymorphic method call instead of spelled out with `instanceof`.

## A 60-Second Leaf vs. Composite Primer

- **Leaf** = "the recursion stops here" = an object with no children, whose
  answer to every question is about itself alone (`Product`).
- **Composite** = "the recursion continues" = an object that holds other
  `CatalogComponent`s and answers every question by asking each of them the
  same question, then combining the results (`Category`).

Both implement the exact same interface, which is the only reason a caller
can treat them the same way.

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
./gradlew run      # must print the catalog tree and the totals
```

Expected output from `./gradlew run` (abridged — see
[`../README.md`](../README.md) for the full transcript):

```
== Printing the whole catalog tree ==
+ Electronics/
  - Phone ($599.99)
  + Accessories/
...
== Totals, computed uniformly over leaves and composites ==
Total price:  $659.96
Product count: 4
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| `UnsupportedOperationException` from `children().add(...)` | `Category.children()` returns an unmodifiable view, on purpose | Call `category.add(child)` instead |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`composite-pattern-explained.md`](composite-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/composite/`
7. [`session.md`](session.md) — the guided walkthrough
