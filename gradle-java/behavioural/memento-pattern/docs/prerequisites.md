# Prerequisites

Everything you need before starting the Memento pattern project. If you have
ever pressed Ctrl-Z, you already understand what we are building; the work is
all in building it without opening the basket up.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, fields, constructors, methods, `new`.
- **References versus values** — that `a = b` on two objects makes both names
  point at the *same* object. This is the single idea the whole project turns
  on; if it is shaky, read the primer below twice.
- **Collections** — `List`, `ArrayList`, `List.copyOf(...)`, and `Deque` used
  as a stack (`push`, `pop`).
- **Records** — `record BasketLine(String product, int pounds, int quantity)`.
  Read it as "a small immutable class with the constructor and accessors
  written for you".

### Helpful, but explained as we go

- **Package-private visibility** — a member with no modifier is visible only
  inside its own package. That is the entire mechanism by which a snapshot
  stays sealed, so it is worth being comfortable with.
- **Immutability** — why a thing that cannot change is safe to share, and why
  that makes a shallow copy sufficient here.
- **Reflection, enough to read it** — one test walks a class's declared methods
  to prove nothing public gives up the basket's state. You do not have to write
  reflection.
- **Any experience of an undo button**, from the user's side. That is enough.

### Explicitly NOT required

- Serialization, `Serializable`, JSON, or any storage library. Snapshots here
  are ordinary objects held in memory.
- Threads or concurrency.
- Any other design pattern, though [Command](../command-pattern) makes a
  useful contrast if you have already met it.
- Any database or transaction experience.

## A 60-Second "Reference vs. Copy" Primer

This is the idea the naive version gets wrong, so it is worth sixty seconds.

```java
List<String> live  = new ArrayList<>(List.of("a", "b"));
List<String> saved = live;              // NOT a copy
live.add("c");
System.out.println(saved);              // [a, b, c]
```

`saved` and `live` are two names for one list. Changing it through either name
changes it, because there is only one of it.

```java
List<String> saved = List.copyOf(live);  // a copy
live.add("d");
System.out.println(saved);               // [a, b, c]
```

Now there are two lists, and later edits to one cannot reach the other. A
snapshot must be the second kind. A photograph, not a window.

## A 60-Second "Memento" Primer

A **memento** is a sealed copy of another object's state.

- The **originator** — here, `Basket` — is the only class that knows what its
  state is, so it is the only class that makes a memento and the only class
  that reads one back.
- The **memento** — `BasketSnapshot` — holds the copy. It is public enough to
  be passed around and opaque enough that passing it around gives nothing away.
- The **caretaker** — `BasketHistory` — holds mementos and hands them back. It
  never opens one, and does not need to.

```java
BasketSnapshot before = basket.save("removed the laptop stand");
// ... the shopper changes their mind ...
basket.restore(before);
```

## A 60-Second "Wide and Narrow Interface" Primer

The pattern asks a memento to show two different faces: a **wide** one to the
originator, which needs the state back, and a **narrow** one to everybody else,
who must not have it. Java gives you that with access modifiers alone:

| Member | Visibility | Who can use it |
| --- | --- | --- |
| `label()` | `public` | anyone — a history list, a menu, a log |
| `lines()` | package-private | `Basket`, and nothing else |
| `voucher()` | package-private | `Basket`, and nothing else |
| the constructor | package-private | `Basket`, so snapshots come from baskets |

`SnapshotEncapsulationTest` asserts this by reflection, so a public getter
added in a hurry fails the build rather than quietly widening the crack.

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

You should see the build succeed with **16 tests**. Then:

```bash
./gradlew run
```

You should see two sections. In the first, the shopper presses undo and the
basket comes back **empty** — no exception, no log, just a £0 basket. That is
wrong, and it is meant to be. In the second, the same undo puts back the line,
the voucher and the total.

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

**The tests fail on `undoEmptiesTheBasketInstead`** — somebody has fixed the
deliberate bug in `NaiveBasket`. That bug is the lesson; put it back.

**`SnapshotEncapsulationTest` fails naming a method** — a public accessor has
been added to `BasketSnapshot`, so the caretaker could now read the basket out
of it. That is the test doing its job.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — undo written the obvious
   way, and the two ways it fails
2. `NaiveBasket` in the source — six lines, two bugs, no exceptions
3. [`memento-pattern-explained.md`](memento-pattern-explained.md) — the
   pattern and the code
4. [`class-diagram.md`](class-diagram.md) and
   [`uml-diagram.md`](uml-diagram.md) — the three roles, then one undo through
   them
5. [`animation.html`](animation.html) — the same undo, step by step, in a
   browser
6. `./gradlew run`, then read `BasketUndoDemo` alongside its output
