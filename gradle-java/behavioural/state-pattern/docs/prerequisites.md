# Prerequisites

What you need before reading the rest of these notes. If you can follow the
table below, you have enough.

## Java You Need

| Idea | What you must be able to do | Where it shows up here |
| --- | --- | --- |
| **Interfaces** | Declare one, implement it | `OrderState` and its seven implementations |
| **`default` methods** | Know that an interface can carry a body, and that not overriding it is a decision | Every refusal in this project is an un-overridden default |
| **`private` interface methods** | Know Java 9 added them, and that they are invisible to implementors | `OrderState.because()` |
| **Polymorphic dispatch** | Predict which body runs for `state.cancel(order)` | This *is* the pattern |
| **Static constants** | `public static final X INSTANCE` with a private constructor | The states hold no data, so there is one of each |
| **Anonymous classes** | `new OrderState() { ... }` inline | The eighth state, added in the demo without touching `Order` |
| **Records** | Read a `record` declaration and use its accessors | `OrderLine`, `OrderEvent`, `Ledger.Entry` |
| **Unchecked exceptions** | Throw one, catch one, read what it carries | `IllegalTransitionException` |

If one row is worth shoring up first, it is the second. The whole design rests
on the idea that *silence is a refusal*: `CancelledState` does not override
`refund`, and that absence is the rule.

## The Pattern in 60 Seconds

An object's behaviour depends on some internal condition, and the usual way to
write that is a conditional in every method. Instead, give the condition a
type. Make one class per state, put all the behaviour for that state in it,
and have the object delegate every request to whichever state it currently
holds. The states decide what happens next, including which state comes next.

The conditionals do not move. They disappear, and are replaced by dispatch.

## State Versus Strategy

These two have **the same class diagram**. A context holds an interface, and
concrete classes implement it. If you compare the pictures you will not be
able to tell them apart, and any explanation that leans on structure is
wasting your time.

The difference is intent and control:

| | Strategy | State |
| --- | --- | --- |
| Who picks the object? | The caller, from outside | The object itself, as a consequence of what it just did |
| Does it change during the object's life? | Usually not | That is the entire point |
| Do the implementations know about each other? | No | Yes — they hand control to one another |
| What varies? | *How* one job is done | *What* the object will accept at all |

In the [Strategy project](../../strategy-pattern/README.md) the checkout picks
a shipping calculator and the calculator does its sum, forever unaware that
any other calculator exists. Here, `PaidState.pack` ends by making the order a
`PackedState` — a state names its successors, and that reference is why the
two patterns are not interchangeable even though they look identical.

## State Versus An Enum

You do not need this pattern for every status field, and reaching for it
automatically is a mistake in the other direction. An enum plus a map of
permitted transitions is smaller, keeps the whole table in one readable place,
and is easy to serialise.

Use State when the **behaviour** varies, not just the permissions — when
cancelling a `PAID` order and cancelling a `PACKED` one do genuinely different
work, as they do in this project. If every state's version of a method is the
same body behind a different guard, you wanted the enum.

## Domain You Need

Nothing specialist. An order has lines, a total, and a ledger of money taken
and given back. The lifecycle is the one every shop has: placed, paid, packed,
shipped, delivered, with cancellation and refunds hanging off the side.

Money is pence-accurate (`Money` wraps a `long`), so a ledger that ends at
`-£97.49` really is the shop being out of pocket by that amount.

## Tooling

| Thing | Version |
| --- | --- |
| Java | 21 |
| Gradle | 9.2.1 (wrapper included) |
| JUnit | 5.10.2 |

Run it with `./gradlew run`, test it with `./gradlew test`. Nothing else is
needed.
