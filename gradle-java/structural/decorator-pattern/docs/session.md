# Session Guide — Decorator Pattern

A 60-minute guided session for teaching or self-studying the Decorator
pattern using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/decorator-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Decorator pattern solves.
2. Explain why `ProductDecorator` holds a `PricedItem` field instead of
   subclassing `Product` for every feature combination.
3. Identify the four roles — component, concrete component, decorator,
   concrete decorator — in real code.
4. Predict how stacking order changes the total when a percentage-based
   decorator is involved.
5. Distinguish Decorator from Adapter.

## Timetable

| Time | Segment | Mode |
| --- | --- | --- |
| 0:00–0:05 | Setup check | Hands-on |
| 0:05–0:15 | The problem | Discussion |
| 0:15–0:25 | The pattern | Explanation |
| 0:25–0:40 | Code walkthrough | Live coding |
| 0:40–0:50 | Exercises | Hands-on |
| 0:50–0:58 | Pitfalls & comparisons | Discussion |
| 0:58–1:00 | Wrap-up | — |

## 0:00–0:05 — Setup Check

Everyone runs:

```bash
java -version
./gradlew run
```

Anyone whose build fails pairs up with a neighbour. Do not debug installs
during the session — that is what the prerequisites doc is for.

## 0:05–0:15 — The Problem

**Do not show `PricedItem`/`ProductDecorator` yet.** Start with the pain.

Put `NaiveGiftWrappedProduct`, `NaiveInsuredProduct`, and
`NaiveGiftWrappedInsuredProduct` from
[`problem-statement.md`](problem-statement.md) side by side and ask:

> *"These three classes cover gift wrap alone, insurance alone, and both
> together. What happens when a customer wants express handling too?"*

Land on: four *more* classes are needed to cover every combination with
express handling, and the gift-wrap fee and insurance premium calculations
are already duplicated across the three that exist.

**Key question to land:** *"If the insurance rate changes from 2% to 2.5%,
how many classes need to change?"* Every naive class that computed a
premium — and that count grows combinatorially as more optional features
are added.

## 0:15–0:25 — The Pattern

Introduce the dressing-for-weather analogy from
[`decorator-pattern-explained.md`](decorator-pattern-explained.md). Ask the
group: *"Does your shirt need to know a raincoat exists before you put one
on over a sweater?"* Land on: no — each layer adds its own effect without
knowing what's underneath or on top of it.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the four roles. Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and trace a single
`cost()` call cascading down through three decorators to `Product` and
back up with fees accumulating.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice.

**The one point that must land:**

> If `InsuranceDecorator` ever needs to know whether it's wrapping a
> `Product` directly or another decorator, the pattern has not been
> applied — the whole point is that every layer only ever calls
> `wrapped.cost()`, blind to what's beneath it.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The component — `PricedItem.java`**
Point out this interface declares exactly the shape both plain and
decorated products share: `cost()` and `description()`. Ask: *"Why does a
decorator need to expose the exact same interface as the thing it wraps?"*

**2. The concrete component — `Product.java`**
Point out this is the plain, undecorated case — no fees, no wrapping.

**3. The abstract decorator — `ProductDecorator.java`**
This is the heart of the session. Point at the `wrapped` field and ask:
*"Is this inheritance or composition?"* Composition — and this abstract
class implements `PricedItem` without implementing `cost()` or
`description()` itself, leaving that to its subclasses.

**4. A concrete decorator — `InsuranceDecorator.java`**
Trace exactly one line: `wrapped.cost()`. Ask: *"Does this line know if
`wrapped` is a `Product` or another decorator?"* No — and that's what lets
decorators stack in any order.

**5. The trap — `NaiveGiftWrappedProduct.java` / `NaiveInsuredProduct.java` / `NaiveGiftWrappedInsuredProduct.java`**
Put the fee-calculation blocks from all three naive classes side by side.
Ask: *"How much of this is copy-pasted?"* Nearly all of it — and none of
these three classes share a common supertype.

**6. Run it — `PricingDemo.java`**
Run `./gradlew run` live. Point at the section stacking gift wrap,
insurance, and express handling one at a time, then the section that
reverses the gift-wrap/insurance order and gets a *different* total. Ask
the group to predict the number before it prints.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a fourth decorator (everyone)

Add a `DiscountDecorator` that subtracts a flat amount from whatever it
wraps (clamp so cost never goes below zero). Confirm it can be placed
anywhere in an existing stack — first, last, or in the middle — with zero
changes to any existing class.

> **The payoff:** a whole new optional feature cost exactly one class. Say
> this out loud when someone finishes.

### Exercise 2 — Prove stacking order matters (everyone)

Write a small test that stacks `GiftWrapDecorator` and
`InsuranceDecorator` in both orders and asserts the two totals are
different. Confirm the difference is exactly the insurance premium on the
$3.50 gift-wrap fee.

### Exercise 3 — Break the abstraction on purpose (discussion)

Add an `unwrap()` method to `ProductDecorator` that returns `wrapped`, and
have `PricingDemo` call it to peek at what's underneath a decorator.
Discuss: *"What did we just throw away?"* The whole point of every layer
staying blind to what it wraps — now client code can start branching on
concrete decorator types instead of treating the whole stack as one
`PricedItem`.

### Exercise 4 — Stretch (for fast finishers)

Count how many naive classes a fourth optional feature (on top of gift
wrap and insurance) would require to cover every combination by hand.
Compare that count to the one new decorator class the pattern actually
needs.

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- Decorators should never add new methods beyond the component interface —
  that breaks substitutability for callers expecting a plain `PricedItem`.
- Order-sensitive decorators (like `InsuranceDecorator`) need their
  behavior documented, since stacking order silently changes the result.
- Too many stacked layers can make debugging "which layer added this fee"
  harder — keep each decorator small and precisely named.

Then the comparison table. The line worth memorising:

> **Decorator keeps the same interface in and out so wrapped and unwrapped
> objects stay interchangeable. Adapter deliberately changes the interface
> to reconcile two shapes that disagree.**

Close with real-world sightings: `java.io` stream wrappers
(`BufferedInputStream`, `GZIPInputStream`), `Collections.unmodifiableList`,
and servlet filter chains.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one place in your own codebase where a fixed set of subclasses
> covers every combination of two or three optional behaviors — a
> notification service with channel + priority variants is a common one —
> and sketch what a decorator stack would look like instead.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "Isn't this the same as Adapter?" | No — Adapter changes the interface to reconcile two shapes that disagree; Decorator deliberately keeps the *same* interface so wrapped and unwrapped objects stay interchangeable |
| "Why not just add a `giftWrapped` boolean flag to `Product`?" | That scales to one flag; the moment you have two or three independent optional features, you're back to a combinatorial explosion of `if` branches inside one class instead of classes |
| "Doesn't stacking order being significant mean the pattern is broken?" | No — it's an honest reflection of the domain. A percentage fee genuinely does depend on what it's a percentage *of*. The pattern makes that visible instead of hiding it |
| "Shouldn't `InsuranceDecorator` always price off the original product?" | That's a valid design choice, but a different one — it would mean `InsuranceDecorator` needs a reference to the base `Product`, not just `wrapped`, which changes what it depends on |

**If you are running short on time:** cut Exercise 4 and shorten the
pitfalls discussion. Never cut Exercise 3 — hitting the "what did we throw
away" moment is where the value of keeping every layer blind to what it
wraps actually lands.

**If you have extra time:** have participants implement
`DiscountDecorator` from Exercise 1 fully, with its own test class
mirroring `GiftWrapDecoratorTest`.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/decorator-pattern-explained.mp4`) — useful
      as a recap for anyone who joins late, or to send round afterwards
- [ ] The printed stacked-pricing output from `./gradlew run` ready to put
      on the board
- [ ] IDE font size raised for screen sharing
