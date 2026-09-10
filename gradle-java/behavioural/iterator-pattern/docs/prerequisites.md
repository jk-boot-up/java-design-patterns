# Prerequisites

Everything you need before starting the Iterator pattern project. If you can
already write a `for` loop over a `List`, you are most of the way there.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, fields, constructors, methods, `new`.
- **Interfaces** — what `implements` means, and that a variable can be typed
  as an interface while holding an instance of a class.
- **Collections** — `List`, `ArrayList`, `List.of(...)`, and `list.get(i)`.
- **The for-each loop** — `for (String s : names) { ... }`. You will find out
  in this project what that syntax actually does.
- **Generics, enough to read them** — `List<Product>` means "a list of
  products". You will not have to write a generic class.

### Helpful, but explained as we go

- **Records** — `Product` is one. Think "a class whose only job is to hold a
  few final values", with the constructor, getters, `equals` and `toString`
  written for you.
- **`java.util.Iterator`** — the two-method interface at the centre of the
  project. If you have never used it directly, that is fine; the whole point
  of the project is where it comes from.
- **Package-private visibility** — a class with no `public` on it is visible
  only inside its own package. `CatalogueIterator` is deliberately one.
- **Paged APIs** — the idea that a remote system hands you results a chunk at
  a time rather than all at once.

### Explicitly NOT required

- Streams, `Spliterator`, or anything in `java.util.stream`.
- Threads or concurrency. `ConcurrentModificationException` gets a mention
  and no more.
- Any other design pattern.
- Any web, HTTP or database experience — `CatalogueFeed` fakes the paged API
  with a list, so there is nothing to install or connect to.

## A 60-Second "Iterator" Primer

An **iterator** is a small object whose entire job is to remember *where you
are* in a collection. It answers two questions:

```java
boolean hasNext();   // is there another one?
Product  next();     // give me it, and move on
```

That is the whole interface. `java.util.Iterator` adds one optional method
(`remove()`) and nothing else.

An **iterable** is anything that can hand you a fresh iterator:

```java
Iterator<Product> iterator();
```

The pay-off is that Java's for-each loop is defined in terms of `Iterable`.
When you write

```java
for (Product product : catalogue) {
    ...
}
```

the compiler turns it into roughly this:

```java
Iterator<Product> it = catalogue.iterator();
while (it.hasNext()) {
    Product product = it.next();
    ...
}
```

So implementing one interface with one method gets you the nice syntax — and
gets your class into every API in the JDK that accepts an `Iterable`.

## A 60-Second "Aggregate vs. Iterator" Primer

The split that people get wrong on their first attempt:

| | Holds | Analogy |
| --- | --- | --- |
| **Aggregate** (`ProductCatalogue`) | What is in the collection | The book |
| **Iterator** (`CatalogueIterator`) | Where *one reader* has got to | The bookmark |

Put the position on the aggregate and you have one bookmark glued into the
book: two readers fight, and a loop inside a loop breaks. Keep the position
on the iterator and each reader gets their own.

## Software Prerequisites

| Tool | Version | Why |
| --- | --- | --- |
| JDK | 21 | The project is built against Java 21 |
| Gradle | none needed | The wrapper (`./gradlew`) downloads it |
| An IDE | any | IntelliJ IDEA, VS Code, Eclipse — all fine |

### Installing JDK 21

**macOS** (Homebrew):

```bash
brew install openjdk@21
```

**Linux** (Debian/Ubuntu):

```bash
sudo apt install openjdk-21-jdk
```

**Windows** — download a build from
[Adoptium](https://adoptium.net/temurin/releases/?version=21) and run the
installer.

Verify:

```bash
java -version
```

You want to see `21` at the start of the version string.

### Gradle

Do not install it. Every command in this project uses the wrapper script
checked in alongside the source:

```bash
./gradlew build      # macOS / Linux
gradlew.bat build    # Windows
```

The first run downloads the right Gradle version and takes a minute. Later
runs are quick.

## Verify Your Setup

From the project directory:

```bash
./gradlew test
```

You should see the build succeed with **13 tests**. Then:

```bash
./gradlew run
```

You should see four numbered sections, starting with the naive browser
reporting a cheapest product of `SKU-005 Coffee Mug` — which is the wrong
answer, and is meant to be.

If both work, you are ready.

## Troubleshooting

**`./gradlew: Permission denied`** — mark it executable:

```bash
chmod +x gradlew
```

**`Unsupported class file major version`** — Gradle picked up an older JDK.
Check `java -version`, and point Gradle at 21 explicitly if you have several
installed:

```bash
./gradlew test -Dorg.gradle.java.home=/path/to/jdk-21
```

**The tests fail on `findCheapestMissesTheFirstPage`** — somebody has fixed
the deliberate off-by-one in `NaiveCatalogueBrowser`. That bug is the lesson;
put it back.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why the page loop keeps
   going wrong
2. `NaiveCatalogueBrowser` in the source — the three copies, two of them
   broken
3. [`iterator-pattern-explained.md`](iterator-pattern-explained.md) — the
   pattern and the code
4. [`class-diagram.md`](class-diagram.md) and
   [`uml-diagram.md`](uml-diagram.md) — structure, then call flow
5. [`animation.html`](animation.html) — the walk, step by step, in a browser
6. `./gradlew run`, then read `CatalogueDemo` alongside its output
