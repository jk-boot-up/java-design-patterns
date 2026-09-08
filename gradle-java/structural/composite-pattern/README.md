# Composite Pattern

Demonstrates the Structural **Composite** design pattern using a product
catalog tree for an e-commerce store as an example.

- `CatalogComponent` — the component. The one interface both leaves and
  composites implement: `name()`, `totalPrice()`, `productCount()`,
  `print(indent)`.
- `Product` — the leaf. No children; every question is answered about
  itself alone. `totalPrice()` returns its own price, `productCount()` is
  always `1` — the base case of the recursion.
- `Category` — the composite. Holds a `List<CatalogComponent>` of children,
  which may themselves be more `Category` nodes. Answers every question by
  delegating to each child and combining the results — no `instanceof`
  anywhere.
- `NaiveProduct` / `NaiveCategory` / `NaiveCatalogPrinter` — the trap, kept
  for contrast. With no shared type, `NaiveCategory` falls back to
  `List<Object>`, and `NaiveCatalogPrinter` repeats an `instanceof` chain
  independently in every operation.
- `CatalogDemo` — runnable entry point that builds a three-level catalog
  tree, prints it, computes totals, and contrasts the composite approach
  with the naive one.

## Run

```bash
./gradlew run
```

Which prints:

```text
== Printing the whole catalog tree ==
+ Electronics/
  - Phone ($599.99)
  + Accessories/
    - Case ($19.99)
    - Charger ($29.99)
    + Cables/
      - USB-C Cable ($9.99)

== Totals, computed uniformly over leaves and composites ==
Total price:  $659.96
Product count: 4

== Uniform treatment: no instanceof anywhere above ==
Phone -> $599.99 across 1 product(s)
Accessories -> $59.97 across 3 product(s)

== The naive alternative, for comparison ==
Total price:  $659.96
Product count: 4
Same result, but every one of those three static methods repeats the same instanceof chain.
```

Expected output:

```
== Printing the whole catalog tree ==
+ Electronics/
  - Phone ($599.99)
  + Accessories/
    - Case ($19.99)
    - Charger ($29.99)
    + Cables/
      - USB-C Cable ($9.99)

== Totals, computed uniformly over leaves and composites ==
Total price:  $659.96
Product count: 4

== Uniform treatment: no instanceof anywhere above ==
Phone -> $599.99 across 1 product(s)
Accessories -> $59.97 across 3 product(s)

== The naive alternative, for comparison ==
Total price:  $659.96
Product count: 4
Same result, but every one of those three static methods repeats the same instanceof chain.
```

## Test

```bash
./gradlew test
```

13 tests, covering the leaf (`ProductTest`), the composite's recursive
summation and unmodifiable children list (`CategoryTest`), the naive
alternative's matching results (`NaiveCatalogPrinterTest`), and the demo's
printed output (`CatalogDemoTest`).

## Learning Material

Start here if you are new to the pattern — the docs are ordered as a
learning path.

| Document | What it covers |
| --- | --- |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What to know and install before you start |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The problem the pattern solves, and why the naive approach hurts |
| [`docs/composite-pattern-explained.md`](docs/composite-pattern-explained.md) | The pattern itself, the code walked through, pitfalls, and comparisons |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Static structure |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Runtime call flow |
| [`docs/animation.html`](docs/animation.html) | Animated, step-by-step walkthrough — open in a browser. Optional narration via the **Narration** button |
| [`docs/session.md`](docs/session.md) | A 60-minute guided session plan for teaching it |
| [`docs/youtube.md`](docs/youtube.md) | Title, description, chapters and thumbnail for publishing the video |
| [`docs/thumbnail.png`](docs/thumbnail.png) | The 1280×720 image to upload as the YouTube thumbnail |
| [`docs/spec.md`](docs/spec.md) | The project specification — problem, code, video and publishing quality bar. Also as [`spec.html`](docs/spec.html) |
| [`video/`](video/) | A narrated ~7.5 minute video, plus the script and build pipeline |

### The pattern in one picture

![Composite pattern class diagram](docs/images/class-diagram.png)

### Video

`video/composite-pattern-explained.mp4` — 1080p, ~7.5 minutes, narrated.
An audio-only version is alongside it. See
[`video/README.md`](video/README.md) to rebuild or re-record it.
