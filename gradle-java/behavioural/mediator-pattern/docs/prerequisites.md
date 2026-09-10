# Prerequisites

Everything you need before starting the Mediator pattern project. If you have
ever written a class that holds a reference to another class, you are most of
the way there.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, fields, constructors, methods, `new`.
- **Interfaces** — what `implements` means, and that a class can pass `this`
  as an interface.
- **Abstract classes** — `FormWidget` is one. You need to know that a subclass
  inherits its fields and can call its `protected` methods.
- **Collections** — `List`, `List.of(...)`, `List.copyOf(...)`.
- **`switch` expressions** — `case "Express" -> 6;`. Java 14 syntax; read it
  as a lookup table.

### Helpful, but explained as we go

- **Package-private visibility** — a method with no modifier is callable only
  from inside its own package. Four of the widget methods are deliberately
  package-private, and that is load-bearing.
- **Reflection, enough to read it** — one test walks a class's fields with
  `getDeclaredFields()` to prove no widget holds another. You do not have to
  write reflection.
- **Nested classes** — `NaiveCheckoutForm` puts its five tangled widgets
  inside one file as `static` nested classes, so the tangle can be read at a
  glance.
- **Any experience of UI code** — Swing, Android, React, a web form. This is
  the pattern that lives underneath all of them, but no such experience is
  required.

### Explicitly NOT required

- Any GUI toolkit. There is no window; the "widgets" are plain objects with
  values, and the demo prints to the console.
- Threads or concurrency.
- Any other design pattern, though [Observer](../observer-pattern) makes a
  useful contrast if you have already met it.
- Any web or HTTP experience.

## A 60-Second "Mediator" Primer

A **mediator** is an object that owns the rules about how a group of other
objects affect one another.

The objects in the group are called **colleagues**. A colleague holds a
reference to the mediator, and to no other colleague. When something about a
colleague changes, it tells the mediator:

```java
mediator.changed(this);
```

and stops. It does not work out what that change means, because it cannot see
far enough to know. The mediator can see everything, so the mediator decides.

The interface really is that small:

```java
public interface CheckoutMediator {
    void changed(FormWidget source);
}
```

## A 60-Second "n² Wiring" Primer

The reason this pattern exists is arithmetic.

If every one of *n* objects can affect every other, there are up to *n*(*n*−1)
directed relationships to write and maintain. Five objects is twenty. Ten is
ninety.

If every object talks only to a hub, there are *n* relationships. Five objects
is five. Ten is ten.

| Controls on the form | Wired to each other | Wired to a mediator |
| --- | --- | --- |
| 3 | up to 6 | 3 |
| 5 | up to 20 | 5 |
| 10 | up to 90 | 10 |

The naive form in this project has nine real cross-references on five
controls. Nobody sat down and decided to write nine; each one was added on its
own, for a good reason, on a different day. That is how forms like this
happen, and it is why the growth curve matters more than any single line of
code in it.

## A 60-Second "Push, Don't Pull" Primer

There are two ways a mediator can update its colleagues, and only one of them
keeps the coupling gone.

| | What it looks like | What it costs |
| --- | --- | --- |
| **Push** (used here) | mediator calls `total.show(52)` | Colleagues stay dumb; the mediator holds the knowledge |
| **Pull** | widget calls `mediator.getShippingPrice()` | The widget is back to knowing about shipping, via one extra hop |

Every method the mediator calls on a widget here is package-private and does
not announce anything. That is what stops the form reacting to itself.

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

You should see the build succeed with **14 tests**. Then:

```bash
./gradlew run
```

You should see two sections. The first ends with a form charging £42 —
including £2 for gift wrapping that will not happen — and an enabled Place
Order button with no courier selected. Both are wrong, and are meant to be.

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

**The tests fail on `chargesForWrappingItWillNotDo`** — somebody has fixed the
deliberate omission in `NaiveCheckoutForm`. That bug is the lesson; put it
back.

**`WidgetIsolationTest` fails naming a field** — a widget has been given a
reference to another widget. That is the test doing its job.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — nine references on five
   controls, and the two bugs that follow
2. `NaiveCheckoutForm` in the source — the tangle, gathered into one file
3. [`mediator-pattern-explained.md`](mediator-pattern-explained.md) — the
   pattern and the code
4. [`class-diagram.md`](class-diagram.md) and
   [`uml-diagram.md`](uml-diagram.md) — the star shape, then one click through
   it
5. [`animation.html`](animation.html) — the click, step by step, in a browser
6. `./gradlew run`, then read `CheckoutFormDemo` alongside its output
