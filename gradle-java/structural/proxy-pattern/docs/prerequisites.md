# Prerequisites

What you need to know, and what you need installed, before working through
this Proxy pattern demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Interfaces** | `ProductImage` is the shared type the real image and every proxy implement identically | Can you write an interface and two unrelated classes implementing it? |
| **Composition (wrapping an object)** | `RestrictedProductImage` holds a `ProductImage` field and delegates to it after checking a rule | Can you explain the difference between wrapping an object and extending it? |
| **Lazy initialization** | `LazyProductImage` defers constructing `HighResolutionProductImage` until `render()` is first called | Do you know the `if (field == null) { field = ...; }` pattern and when it's safe? |
| **`final` fields set in a constructor** | `LazyProductImage.sku` and `RestrictedProductImage.image`/`role` are `final` | Do you know why a `final` field must be assigned in every constructor path? |
| **Static state (`static` fields/methods)** | `HighResolutionProductImage.LOAD_COUNT` is a static counter shared by every instance, standing in for "expensive to create" | Do you understand why static state is shared across all instances, not per-object? |
| **Exceptions for control flow** | `RestrictedProductImage.render()` throws `SecurityException` when the role check fails | Comfortable reading `assertThrows` in a test and reasoning about what didn't happen (no load) as well as what did (the throw)? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **JUnit 5 basics** | Every `*Test.java` file |
| **`System.setOut` / stdout capturing** | `ProductImageDemoTest` |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- A real image-decoding or networking library — this project only counts
  constructor calls, no actual files or network calls
- Any UI toolkit
- Any other design pattern

## A 60-Second "Proxy" Primer

If "a stand-in that controls access to another object" feels abstract,
this is all you need:

```java
public interface ProductImage {                                  // <-- the shared shape
    String render();
    String sku();
}

public final class HighResolutionProductImage implements ProductImage { ... }  // <-- expensive to build

public final class LazyProductImage implements ProductImage {
    private final String sku;
    private HighResolutionProductImage realImage;                 // <-- not built yet

    public LazyProductImage(String sku) {
        this.sku = sku;
    }

    public String render() {
        if (realImage == null) {
            realImage = new HighResolutionProductImage(sku);  // <-- built on first use
        }
        return realImage.render();                         // <-- then delegate
    }
}
```

`LazyProductImage` *is a* `ProductImage` and *has a* `ProductImage`-shaped real subject at the
same time — the same trick Decorator uses. The difference is what it does
with that shape: it decides *whether and when* to touch the real object,
rather than adding anything new to what it returns.

## A 60-Second Proxy vs. Decorator Primer

Both wrap an object behind the same interface. Ask this one question to
tell them apart:

- **Does the wrapper change what comes back, or add a new capability?**
  → That's a **Decorator** (`GiftWrapDecorator` adds a fee).
- **Does the wrapper decide whether/when the call even reaches the real
  object?** → That's a **Proxy** (`LazyProductImage` decides *when* to build it;
  `RestrictedProductImage` decides *whether* to allow it).

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
./gradlew run      # must print the listing's proxy walkthrough
```

Expected output from `./gradlew run` (abridged — see
[`../README.md`](../README.md) for the full transcript):

```
== Naive listing -- eagerly loads every image, even ones never shown ==
Images loaded eagerly, before rendering anything: 3
...
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Load count keeps climbing across tests | `HighResolutionProductImage.LOAD_COUNT` is static and not reset | Call `HighResolutionProductImage.resetLoadCount()` in `@BeforeEach` |
| `SecurityException` thrown when you expected success | Role passed is not `Role.CATALOG_ADMIN` | Check which `Role` is passed to the proxy's constructor |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`proxy-pattern-explained.md`](proxy-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/proxy/`
7. [`session.md`](session.md) — the guided walkthrough
