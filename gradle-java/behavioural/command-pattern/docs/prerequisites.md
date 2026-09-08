# Prerequisites

What you need before reading the rest of these notes. If you can follow the
table below, you have enough.

## Java You Need

| Idea | What you must be able to do | Where it shows up here |
| --- | --- | --- |
| **Interfaces** | Write one, implement it in more than one class | `CartCommand` and its four implementations |
| **Polymorphic dispatch** | Understand that `command.undo(cart)` runs different code depending on the object | The undo stack in `CartHistory` |
| **Object state** | Know the difference between a field set in the constructor and one set later | `previousQuantity` is the crux of the whole project |
| **`Deque` as a stack** | `push`, `pop`, `isEmpty` | The undo and redo stacks |
| **Records** | Read a `record` declaration and use its accessors | `CartLine`, `Coupon` |
| **`Optional`** | `orElse`, `orElseThrow`, `isEmpty` | `Cart.line`, `Cart.coupon` |
| **Anonymous classes** | `new CartCommand() { ... }` inline | The gift-wrapping command in the tests |

If the third row feels thin, it is the one to shore up. A command's
constructor takes *what to do*; `execute` discovers *what was there*. Getting
those two backwards is the entire category of undo bug this project is about.

## The Pattern in 60 Seconds

An action is turned into an object with two methods: `execute` does it, and
`undo` reverses it. Something else — an invoker — keeps a stack of the ones
that have run. Undo pops the top one and asks it to reverse itself.

That is it. Everything else in these notes is about the consequences, and
about the one hard part: writing a correct `undo`.

## Command Versus Receiver

Beginners mix these up in one specific way, so it is worth naming:

- The **receiver** owns the state and knows how to change it. Here that is
  `Cart`. It has never heard of a command, and it would work identically if
  this project had no commands in it.
- A **command** owns one edit and its inverse. Here those are the four
  `*Command` classes. Each holds the values it needs and nothing the cart
  might replace underneath it.

If you find yourself giving `Cart` a method called `undo`, stop: the receiver
is not the thing that remembers.

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
./gradlew build   # compiles and runs all 37 tests
./gradlew run     # runs the demo
```

The run should begin:

```
=== 1. The trap: undo notes that record the request, not the cart ===

  The customer has 3 headphones and a 10% code:
    H-100    Wireless headphones     3 x   £89.99 =   £269.97
```

and, a few lines later, show that same cart empty after two undos. That wrong
answer is deliberate — it is the bug the rest of the project removes.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | Gradle is using an older JDK | `./gradlew -version` shows which; set `JAVA_HOME` to a 21 install |
| `Permission denied: ./gradlew` | Wrapper lost its execute bit | `chmod +x gradlew` |
| Downloads hang on first run | Gradle fetching the distribution | It is a one-off; behind a proxy, set `HTTPS_PROXY` |
| Section 1 ends with an empty cart | Nothing is wrong | That is the naive editor losing three headphones, on purpose |
| Amounts print with `£` as `?` | Console is not UTF-8 | On Windows, `chcp 65001` |

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the scenario and the bug
2. [`command-pattern-explained.md`](command-pattern-explained.md) — the pattern, and what it costs
3. [`class-diagram.md`](class-diagram.md) — the structure
4. [`uml-diagram.md`](uml-diagram.md) — the two runs, side by side
5. [`animation.html`](animation.html) — step through the stacks
6. The source, starting at `CartCommand.java`, then `AddItemCommand.java`
