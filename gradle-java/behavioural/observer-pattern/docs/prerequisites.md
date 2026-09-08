# Prerequisites

What you need before reading the rest of these notes. If you can follow the
table below, you have enough.

## Java You Need

| Idea | What you must be able to do | Where it shows up here |
| --- | --- | --- |
| **Interfaces** | Write one, implement it in more than one class | `OrderListener` and its four implementations |
| **Polymorphic dispatch** | Understand that `listener.onStatusChanged(e)` runs different code depending on the object | The notification loop in `Order` |
| **Collections** | `List`, adding to one, iterating it | `Order` holds `List<OrderListener>` |
| **Records** | Read a `record` declaration and use its accessors | `OrderEvent`, `ListenerFailure` |
| **Enums** | Declare one, switch over it | `OrderStatus` |
| **Anonymous classes** | `new OrderListener() { ... }` inline | The loyalty-points listener in the demo and the tests |
| **`try`/`catch`** | Catch an exception and carry on | The failure isolation in `moveTo` |
| **`Consumer<String>`** | Pass a method reference such as `System.out::println` as an argument | Every listener takes one, so tests can capture its output |

If the last row is unfamiliar: `Consumer<String>` is a function that takes a
`String` and returns nothing. `System.out::println` is one. So is
`lines::add` for a `List<String> lines`. Passing it in is what lets the same
listener print in the demo and be inspected in a test.

## The Pattern in 60 Seconds

An object that changes — the **subject** — keeps a list of **observers** and
calls a method on each of them when it changes. It does not know what they
are, and they do not know about each other.

That is it. Everything else in these notes is about the consequences.

## Subject Versus Observer

Beginners mix these up in one specific way, so it is worth naming:

- The **subject** owns the state and announces. Here that is `Order`. It is
  the *only* class that has a listener list.
- An **observer** owns a reaction. Here those are the four `*Listener`
  classes. Each one holds its own tallies and knows nothing about orders
  beyond the event it is handed.

If you find yourself giving a listener a reference to the `Order`, stop and
read the "push versus pull" paragraph in
[`observer-pattern-explained.md`](observer-pattern-explained.md).

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
./gradlew build   # compiles and runs all 27 tests
./gradlew run     # runs the demo
```

The run should begin:

```
=== 1. The trap: an order service that calls each system by name ===

Shipping A-1001 through NaiveOrderService, with a broken mail server:
  [inventory] released the reservation for A-1001
  !! SMTP timeout after 30s
  analytics recorded : 0 event(s)
  warehouse feed     : []
  The order shipped. The warehouse was never told.
```

That "never told" line is the bug this project exists to remove. If you see
it, everything is working — including the deliberate failure.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Gradle is using an older JDK | `./gradlew -version` shows which; set `JAVA_HOME` to a 21 install |
| `Permission denied: ./gradlew` | Wrapper lost its execute bit | `chmod +x gradlew` |
| Downloads hang on first run | Gradle fetching the distribution | It is a one-off; behind a proxy, set `HTTPS_PROXY` |
| `SMTP timeout after 30s` in the output | Nothing is wrong | That exception is thrown on purpose, twice, to show the difference between the two designs |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the scenario and the outage
2. [`observer-pattern-explained.md`](observer-pattern-explained.md) — the pattern, and what it costs
3. [`class-diagram.md`](class-diagram.md) — the structure
4. [`uml-diagram.md`](uml-diagram.md) — the two runs, side by side
5. [`animation.html`](animation.html) — step through a notification
6. The source, starting at `Order.java`, then any one listener
