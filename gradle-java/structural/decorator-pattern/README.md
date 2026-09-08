# Decorator Pattern

Demonstrates the Structural **Decorator** design pattern using checkout
pricing with stackable, optional extras as an example.

- `PricedItem` — the component. The interface both plain and decorated
  products share: `cost()` returns a `BigDecimal`, `description()` returns
  a `String`.
- `Product` — the concrete component. A plain item with a name and a
  price, no extras.
- `ProductDecorator` — the abstract decorator. Implements `PricedItem` and
  holds a wrapped `PricedItem` by composition, without adding a fee of its
  own.
- `GiftWrapDecorator` / `InsuranceDecorator` / `ExpressHandlingDecorator` —
  concrete decorators. Each adds exactly one fee (a flat fee, a
  percentage-based premium, and another flat fee respectively) and one
  description suffix on top of whatever it wraps.
- `NaiveGiftWrappedProduct` / `NaiveInsuredProduct` /
  `NaiveGiftWrappedInsuredProduct` — the trap, kept for contrast. One
  hardcoded class per feature combination, each duplicating its own fee
  calculation independently.
- `PricingDemo` — runnable entry point that stacks decorators one feature
  at a time, shows how reversing the gift-wrap/insurance order changes the
  total, and contrasts the decorator approach with the naive one.

## Run

```bash
./gradlew run
```

Which prints:

```text
== Stacking decorators, one feature at a time ==
Wireless Headphones: $79.99
Wireless Headphones, gift-wrapped: $83.49
Wireless Headphones, gift-wrapped, insured: $85.16
Wireless Headphones, gift-wrapped, insured, express handling: $95.15

== Stacking order changes the result -- insurance prices whatever it wraps ==
Wireless Headphones, insured, gift-wrapped: $85.09
(compare to gift-wrapped-then-insured above: same two decorators, different total)

== The naive alternative, for comparison ==
Wireless Headphones, gift-wrapped, insured: $85.16
Same result as gift-wrapped-then-insured, but a whole new class was needed --
adding express handling to this combination would mean four more naive classes.
```

Expected output:

```
== Stacking decorators, one feature at a time ==
Wireless Headphones: $79.99
Wireless Headphones, gift-wrapped: $83.49
Wireless Headphones, gift-wrapped, insured: $85.16
Wireless Headphones, gift-wrapped, insured, express handling: $95.15

== Stacking order changes the result -- insurance prices whatever it wraps ==
Wireless Headphones, insured, gift-wrapped: $85.09
(compare to gift-wrapped-then-insured above: same two decorators, different total)

== The naive alternative, for comparison ==
Wireless Headphones, gift-wrapped, insured: $85.16
Same result as gift-wrapped-then-insured, but a whole new class was needed --
adding express handling to this combination would mean four more naive classes.
```

## Test

```bash
./gradlew test
```

8 test classes, covering the plain component (`ProductTest`), each
concrete decorator's fee and description (`GiftWrapDecoratorTest`,
`InsuranceDecoratorTest`, `ExpressHandlingDecoratorTest`), three-deep
stacking and order-dependence (`DecoratorStackingTest`), the naive
alternative's matching output (`NaiveProductClassesTest`), and the demo's
printed output (`PricingDemoTest`).

## Learning Material

Start here if you are new to the pattern — the docs are ordered as a
learning path.

| Document | What it covers |
| --- | --- |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What to know and install before you start |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The problem the pattern solves, and why the naive approach hurts |
| [`docs/decorator-pattern-explained.md`](docs/decorator-pattern-explained.md) | The pattern itself, the code walked through, pitfalls, and comparisons |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Static structure |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Runtime call flow |
| [`docs/animation.html`](docs/animation.html) | Animated, step-by-step walkthrough — open in a browser. Optional narration via the **Narration** button |
| [`docs/session.md`](docs/session.md) | A 60-minute guided session plan for teaching it |
| [`docs/youtube.md`](docs/youtube.md) | Title, description, chapters and thumbnail for publishing the video |
| [`docs/thumbnail.png`](docs/thumbnail.png) | The 1280×720 image to upload as the YouTube thumbnail |
| [`docs/spec.md`](docs/spec.md) | The project specification — problem, code, video and publishing quality bar. Also as [`spec.html`](docs/spec.html) |
| [`video/`](video/) | A narrated ~6.5 minute video, plus the script and build pipeline |

### The pattern in one picture

![Decorator pattern class diagram](docs/images/class-diagram.png)

### Video

`video/decorator-pattern-explained.mp4` — 1080p, ~6.5 minutes, narrated.
An audio-only version is alongside it. See
[`video/README.md`](video/README.md) to rebuild or re-record it.
