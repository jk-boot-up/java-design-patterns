# Abstract Factory Pattern

Demonstrates the **Abstract Factory** creational pattern (Gang of Four) using
an e-commerce checkout that sells into three regional markets.

- `TaxCalculator`, `CurrencyFormatter`, `AddressValidator` — the three
  abstract products. Every market needs one of each, and the three must agree.
- `UkVatCalculator` / `PoundFormatter` / `UkPostcodeValidator`,
  `UsSalesTaxCalculator` / `DollarFormatter` / `UsZipValidator`,
  `IndiaGstCalculator` / `RupeeFormatter` / `IndiaPinValidator` — the nine
  concrete products, arranged as three families.
- `MarketFactory` — the abstract factory. Three creation methods and nothing
  else. It never names a market or a product class.
- `UkMarketFactory`, `UsMarketFactory`, `IndiaMarketFactory` — the concrete
  factories. Each builds one complete, self-consistent family.
- `CheckoutService` — the client. It is handed one factory, collects the three
  products in its constructor, and then works entirely through interfaces.
- `Order` / `Quote` — immutable value objects in and out.
- `AbstractFactoryDemo` — runnable entry point that quotes the same order in
  all three markets, then shows a cross-market order being rejected.

Search `CheckoutService` for "UK", "US" or "India" and you find nothing. That
is the point: a British tax rate cannot end up next to an American ZIP code,
not because anything checks for it, but because no code exists that could
produce it.

## Run

```bash
./gradlew run
```

## Test

```bash
./gradlew test
```

## Learning Material

Start here if you are new to the pattern — the docs are ordered as a learning
path.

| Document | What it covers |
| --- | --- |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What to know and install before you start |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The problem the pattern solves, and why the naive approach hurts |
| [`docs/abstract-factory-pattern-explained.md`](docs/abstract-factory-pattern-explained.md) | The pattern itself, the code walked through, pitfalls, and comparisons |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Static structure, and the three families |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Runtime call flow |
| [`docs/animation.html`](docs/animation.html) | Animated, step-by-step walkthrough — open in a browser. Optional narration via the **Narration** button |
| [`docs/session.md`](docs/session.md) | A 60-minute guided session plan for teaching it |
| [`video/`](video/) | A narrated ~9.5 minute video, plus the script and build pipeline |

### The pattern in one picture

![Abstract Factory pattern class diagram](docs/images/class-diagram.png)

### The three families

![The three market families](docs/images/families.png)

### Video

`video/abstract-factory-pattern-explained.mp4` — 1080p, ~9.5 minutes, narrated.
An audio-only version is alongside it. See
[`video/README.md`](video/README.md) to rebuild or re-record it.

### Related

The three factory patterns in this repository are best read in order:

1. [`../simple-factory-pattern`](../simple-factory-pattern) — one helper class
   with a `switch`, choosing one object. Not in the Gang of Four book, but
   where everyone starts.
2. [`../factory-method-pattern`](../factory-method-pattern) — the choice moves
   into the type system. A creator writes a workflow with a hole in it, and
   subclasses fill the hole with one object each.
3. **This project** — the choice moves up a level again. One decision now
   produces a whole matching *set* of objects.

Simple Factory asks "which one?". Factory Method asks "which one — decided by
my subclass?". Abstract Factory asks "which set?".
