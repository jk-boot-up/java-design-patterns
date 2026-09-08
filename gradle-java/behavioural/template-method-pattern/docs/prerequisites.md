# Prerequisites

What you need before reading the rest of these notes. If you can follow the
table below, you have enough.

## Java You Need

| Idea | What you must be able to do | Where it shows up here |
| --- | --- | --- |
| **Abstract classes** | Write one, extend it, implement its abstract methods | `FulfilmentProcess` and its three routes |
| **`final` methods** | Know that a `final` method cannot be overridden | `fulfil` — this is the pattern |
| **Access modifiers** | Tell `private`, `protected` and `public` apart, and know that `private` methods are not inherited into the override-able surface | `validate` is private on purpose |
| **Overriding vs. overloading** | Know which one `@Override` is checking | Every step in every route |
| **`super.method()`** | Call the base class's version from an override | `RecordingRoute` in the tests |
| **Records** | Read a `record` declaration and use its accessors | `Order`, `OrderLine`, `FulfilmentReport.Step` |
| **Anonymous subclasses** | `new FulfilmentProcess() { ... }` inline | The routes defined inside the tests |

If the second and third rows feel thin, they are the ones to shore up. This
whole pattern is a statement about what a subclass is *allowed* to do, and
`final` and `private` are how that statement is written down.

## The Pattern in 60 Seconds

A base class writes out an algorithm as a sequence of calls, and marks that
method `final`. Some of the calls are abstract, so a subclass must supply
them. Some have a default, so a subclass may replace them. Some do nothing at
all, so a subclass can hook in if it needs to.

The subclass decides *how* each step behaves. It never decides *when* the
steps run.

That is it. Everything else in these notes is about which kind of hole to use
where, and about what the inheritance costs you.

## Template Method Versus Factory Method

If you have already read the [Factory Method
project](../../../creational/factory-method-pattern/README.md), these two will
feel similar, because they are related — and mixing them up is the single
most common confusion in this corner of the catalogue.

- **Factory Method** is a hole in a workflow whose answer is **an object**.
  There is one hole, it returns a product, and the workflow's job is to use
  that product.
- **Template Method** is a workflow with **several** holes. They return
  nothing in particular, they can have defaults, and some of them exist only
  as opt-in hooks.

The shortest way to hold them apart: **Factory Method is Template Method
narrowed down to object creation.** Every Factory Method is a Template Method
with exactly one step, and that step makes something.

## Template Method Versus Strategy

Also worth naming, because it is the comparison that decides whether you
should use this pattern at all:

- **Template Method** varies steps by **subclassing**, fixed at compile time.
  It can guarantee an order, because one `final` method owns it.
- **Strategy** varies behaviour by **composition**, swappable at run time. It
  guarantees nothing about ordering, because there is no single method that
  owns the sequence.

Reach for Template Method when the *sequence* is the thing you are protecting.
Reach for Strategy when the *steps* are independent and you want to change
them without a new class.

## Tools

**Java 21.** Check with:

```bash
java -version
```

If it prints something older than 21, install a JDK — on macOS,
`brew install openjdk@21`; elsewhere, [Adoptium](https://adoptium.net) has
builds for everything.

Gradle itself does not need installing. The `./gradlew` wrapper in this
project downloads the right version on first use.

## Verify Your Setup

From the project directory:

```bash
./gradlew build   # compiles and runs all 46 tests
./gradlew run     # runs the demo
```

The run should begin:

```
=== 1. The trap: three hand-written copies of the same sequence ===

  A download, fulfilled by NaiveFulfilment.fulfilDigital:
    validate       2 line(s), no address needed
```

and, a few lines later, show an email quoting `Key: (not dispatched)`. That
wrong answer is deliberate — it is the bug the rest of the project removes.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Gradle is using an older JDK | `./gradlew -version` shows which; set `JAVA_HOME` to a 21 install |
| `Permission denied: ./gradlew` | Wrapper lost its execute bit | `chmod +x gradlew` |
| Downloads hang on first run | Gradle fetching the distribution | It is a one-off; behind a proxy, set `HTTPS_PROXY` |
| Section 1 emails a key that reads `(not dispatched)` | Nothing is wrong | That is the naive route, with two steps the wrong way round, on purpose |
| `cannot override validate` if you try | It is `private` | That is the design — answer `requiresShippingAddress()` instead |
| Amounts print with `£` as `?` | Console is not UTF-8 | On Windows, `chcp 65001` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the scenario and the bug
2. [`template-method-pattern-explained.md`](template-method-pattern-explained.md) — the pattern, and what it costs
3. [`class-diagram.md`](class-diagram.md) — the structure
4. [`uml-diagram.md`](uml-diagram.md) — the two runs, side by side
5. [`animation.html`](animation.html) — step through one `fulfil` call
6. The source, starting at `FulfilmentProcess.java`, then `DigitalFulfilment.java`
