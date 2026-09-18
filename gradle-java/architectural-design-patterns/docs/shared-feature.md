# The Shared Feature — one order, built five times

Every project in this category implements **the same feature**, against **the same
seed data**, checked by **the same acceptance assertions**. Only the shape
changes.

That is the whole reason the category can say anything concrete. If each project
demonstrated its architecture on a different problem, the comparison between them
would be rhetoric — five authors each claiming their arrangement is cleaner, with
nothing to check. Holding the feature still means a reader can put project 63 and
project 66 side by side and see that the *only* difference is the direction of the
arrows and the number of files.

This document is written **before any project**, deliberately. Written afterwards
it would have to be retrofitted into five codebases, and the temptation to bend
the feature to flatter whichever architecture was built first would be
irresistible.

---

## 1. The feature, as a sentence

> **A customer places an order for three products. Stock is checked. Payment is
> taken. A confirmation is sent.**

That is it. It is deliberately small, and it is deliberately the same checkout the
Service Layer project (§57) implements, the Saga (§35) orchestrates and the
Strangler Fig (§47) replaces. A reader arriving here already knows what placing an
order involves, so every bit of their attention is free for the shape.

Four steps is the right size for this category. Three would not have enough
structure to arrange; ten would be an application, and an architecture spread
across an application cannot be read on a slide or held in the head while
listening.

---

## 2. The seed data

Identical in all five projects, so the five demos print recognisably the same run.
Anything a project prints that differs from this is a bug in that project, not a
property of its architecture.

**The catalogue.** Three products, with a price and a stock level.

| SKU | Name | Price | Stock |
| --- | --- | --- | --- |
| `ESP-001` | Espresso Machine | £249.00 | 4 |
| `GRD-014` | Burr Grinder | £89.50 | 2 |
| `BNS-220` | Coffee Beans, 1kg | £22.00 | 40 |

**The customer.** `cust-8801`, Ada Okafor, `ada@example.com`, with a card that has
funds.

**The order.** Three lines:

| SKU | Quantity | Line total |
| --- | --- | --- |
| `ESP-001` | 1 | £249.00 |
| `GRD-014` | 1 | £89.50 |
| `BNS-220` | 2 | £44.00 |
| | | **£382.50** |

**£382.50 is the number to remember.** It appears in every project's demo output,
in every project's tests, and — in the MVC project — twice, which is where that
project's bug lives.

Money is held in pence as a `long`, never as a `double`, and formatted once at the
edge. A course that taught architecture while quietly losing a penny to binary
floating point would be teaching the wrong lesson well.

---

## 3. The acceptance assertions

Six of them. They are phrased as **observable outcomes** rather than as calls on
particular classes, because they have to run against five different structures.
That phrasing rule is load-bearing: if an assertion cannot be written without
naming a class that exists in only one of the five projects, the feature has been
specified in terms of a shape, and it needs rewording rather than special-casing.

Each project writes these in its own package, against its own entry point. The
wording below is the contract; the call that satisfies it differs per project and
that difference is exactly the thing being taught.

### A1 — The order is stored, once, as placed

After a successful checkout there is exactly one stored order, its status is
`PLACED`, it belongs to `cust-8801`, and it has three lines.

### A2 — The total is £382.50

The stored order's total is 38250 pence. Not "about", not "as displayed" —
the stored number.

### A3 — Stock falls by exactly what was bought

`ESP-001` goes 4 → 3, `GRD-014` goes 2 → 1, `BNS-220` goes 40 → 38. No other
product moves.

### A4 — Payment is taken once, for the order total

Exactly one charge, of 38250 pence, against `cust-8801`. Not two, not one of a
different amount.

### A5 — One confirmation is sent, naming the order and the total

Exactly one notification goes to `ada@example.com`, and its text contains the
stored order's id and the total as `£382.50`.

### A6 — The three refusals leave nothing behind

Three separate runs, each of which must change nothing:

- **Not enough stock.** Ask for three grinders when two exist. No order is
  stored, no payment is taken, no confirmation is sent, and stock is untouched.
- **Unknown product.** Ask for `XXX-999`. Same: nothing stored, nothing charged,
  nothing sent.
- **Payment declined.** The card refuses. No order is left in `PLACED`, stock is
  back where it started, and no confirmation goes out.

A6 is the assertion that catches architectures which have quietly let the
ordering of the four steps drift, and it is the one most likely to fail first when
a project is refactored into a new shape. That is why it is here rather than left
to each project's judgement.

---

## 4. What is deliberately *not* in the feature

**No concurrency.** Two customers racing for the last grinder is a genuine and
interesting problem, and it belongs to the concurrency category. Here it would
add a lock to every project and teach nothing about shape.

**No persistence beyond a map.** Every project stores orders and stock in memory.
The forced changes in this category *swap the store*, and the swap is only
visible if setting up the store is not a distraction. A reader who has to install
a database before seeing the point has been failed by the example, not taught by
it.

**No network, no HTTP server, no container, in four of the five projects.** The
"web" side of these architectures is a plain method call taking a request object
and returning a response object. That is what a controller is, underneath; the
routing is not the pattern. The fifth project, §67, takes Spring, because
Spring — specifically, who assembles the object graph — is that project's entire
subject.

**No user interface.** MVC's two views are a text screen and a plain-text email,
both of which are strings a test can assert on. A UI toolkit would add days of
setup in exchange for the same lesson.

---

## 5. The architecture test, settled once

Every project in this category ships a test that asserts its own dependency rule,
and the rule is asserted with [ArchUnit](https://www.archunit.org/) rather than by
hand.

This is the one place in the category where a library is worth taking, and the
reason is the category's whole thesis. A dependency rule written as an ArchUnit
test *is* the architecture, executably:

```java
noClasses().that().resideInAPackage("..domain..")
    .should().dependOnClassesThat().resideInAPackage("..infrastructure..")
```

That reads as English, it runs in `./gradlew test`, and when it fails it names the
offending class and the class it reached for. Hand-rolled package inspection would
produce a worse message and would spend the reader's attention on reflection
instead of on architecture.

**Every project must show the rule failing, not just passing.** A green test that
has never been seen red is indistinguishable from a test that asserts nothing.
Each project therefore keeps a deliberately non-compliant class in its test
sources and a test that asserts the rule *catches* it — so the red message is
itself under test, and the video can show it.

| | |
| --- | --- |
| Library | ArchUnit |
| Version | 1.5.0 |
| Scope | `testImplementation` only — it never reaches a production classpath |
| Artefact | `com.tngtech.archunit:archunit-junit5` |

---

## 6. The forced change, and how its cost is counted

Every project makes a change its architecture claims to make cheap, and **prints
the cost**. The format is settled here so the five numbers are comparable:

```
  FORCED CHANGE: replace the storage layer
    files added     : 1
    files modified  : 1
    files untouched : 9
    lines changed   : 3
```

Counted from the real diff, never estimated. The untouched count is the one that
carries the argument, so it is always printed alongside.

| Project | The forced change |
| --- | --- |
| §63 Layered | Replace the storage layer |
| §64 MVC | Add a second view over the same model |
| §65 Hexagonal | Swap the store for an in-memory adapter **and** drive the same core from a CLI |
| §66 Clean | Add a new delivery mechanism and a new data source at once |
| §67 Clean with Spring | The same change as §66, to show the count is identical and only the wiring moved |

---

## 7. How to check the five agree

The claim "these five projects do the same thing" is checkable, so it gets
checked. Run all five demos and compare the block each one prints under the
heading `ACCEPTANCE`:

```
ACCEPTANCE
  order ord-1001 for cust-8801: PLACED, 3 lines, £382.50
  stock ESP-001 3, GRD-014 1, BNS-220 38
  charged cust-8801 £382.50 once
  sent 1 confirmation to ada@example.com
  refused: not enough stock, unknown product, payment declined
```

**Those five lines must be byte-identical across all five projects.** If they are
not, the comparison the category rests on is not valid, and the project that
differs is wrong — no matter how good its architecture looks.

§66 and §67 must agree exactly, since the only difference between them is who
calls the constructors.
