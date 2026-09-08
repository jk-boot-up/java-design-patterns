# Prerequisites

What you need to know, and what you need installed, before working through
this Flyweight pattern demo.

## Knowledge Prerequisites

You do **not** need prior design-pattern experience. You do need comfortable
familiarity with core Java.

### Required

| Topic | Why it matters here | Quick self-check |
| --- | --- | --- |
| **Classes and objects** | Every participant is a plain class | Can you write a class with a constructor and call it with `new`? |
| **`==` vs. `.equals()`** | The whole pattern is proven with `==` (same object) checks | Do you know why `new String("a") == new String("a")` is `false`? |
| **`Map` / `HashMap`** | `BadgeStyleFactory`'s cache is a `Map<BadgeType, BadgeStyle>` | Can you read `map.computeIfAbsent(key, k -> build(k))`? |
| **Fields and `private`/`public`** | `BadgeStyle` has no setters, on purpose | Do you know why a field would be `private final`? |
| **Enums** | `BadgeType` is the cache key | Can you write a basic `enum` with a few constants? |

### Helpful, but explained as we go

| Topic | Where it appears |
| --- | --- |
| **`ConcurrentHashMap` and `computeIfAbsent`** | `BadgeStyleFactory`, for thread-safe sharing |
| **`AtomicInteger`** | Counting real constructions in `BadgeStyleFactory` |
| **`CountDownLatch`** | The concurrency test, coordinating threads to race on purpose |
| **JUnit 5 basics** | Every `*Test.java` file |
| **Gradle basics** | `build.gradle`, `./gradlew run` |
| **UML class & sequence diagrams** | The diagram docs |

### Explicitly NOT required

- Spring, Spring Boot, or any framework
- Real image decoding, rendering, or a UI toolkit — `artwork` is a plain
  `byte[]`, standing in for a rasterised icon
- Databases or web servers
- Any other design pattern

## A 60-Second `computeIfAbsent` Primer

If you have never used this `Map` method, this is all you need:

```java
Map<String, Integer> cache = new HashMap<>();
cache.computeIfAbsent("a", key -> {
    System.out.println("building " + key);
    return 1;
});
cache.computeIfAbsent("a", key -> {
    System.out.println("building " + key);   // never printed the second time
    return 1;
});
```

The lambda only runs if the key is **absent**. Call it a hundred times with
the same key and the expensive part — whatever is inside the lambda — runs
exactly once. That single method is most of `BadgeStyleFactory`.

## A 60-Second Intrinsic vs. Extrinsic Primer

- **Intrinsic** = "part of the shared object" = a *field*.
- **Extrinsic** = "supplied by the caller, differs every time" = a *method
  parameter*.

If you are ever unsure which one a piece of data is, ask: *"if this changes,
does the object I'm sharing need to change with it?"* If yes, it is
extrinsic — it belongs in a parameter, not a field.

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
./gradlew run      # must print the badge renders and the memory arithmetic
```

Expected output from `./gradlew run` (abridged — see
[`../README.md`](../README.md) for the full transcript):

```
== Rendering badges for five listings ==
[NEW] ✨ NEW on LST-1001 (bg=#2563EB, fg=#FFFFFF)
...
== Proving the sharing ==
styleFor(SALE) == styleFor(SALE): true
BadgeStyle instances actually created: 4
...
== Memory arithmetic for a 100000-listing catalog ==
Naive:      100,000 badges x 64 KB artwork each = 6,250 MB
Flyweight:  4 styles x 64 KB artwork each     = 256 KB
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Wrong JDK on `PATH` | Point `JAVA_HOME` at JDK 21 |
| `permission denied: ./gradlew` | Wrapper not executable | `chmod +x gradlew` |
| Wrapper download times out | Offline / proxy | Install Gradle and run `gradle build` |
| Icons show as `?` or boxes in the console | Terminal font lacks emoji glyphs | Cosmetic only — the badge logic is unaffected |
| Diagrams show as raw text | Viewer lacks Mermaid support | Open the PNGs in `docs/images/` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why we need this
2. [`flyweight-pattern-explained.md`](flyweight-pattern-explained.md) — the pattern
3. [`class-diagram.md`](class-diagram.md) — static structure
4. [`uml-diagram.md`](uml-diagram.md) — runtime flow
5. [`animation.html`](animation.html) — watch it happen
6. The source code in `src/main/java/com/jk/explore/flyweight/`
7. [`session.md`](session.md) — the guided walkthrough
