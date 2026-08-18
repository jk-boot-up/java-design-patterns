# Facade Pattern

Demonstrates the Structural **Facade** design pattern using an e-commerce
order checkout as an example.

- `InventoryService`, `PaymentService`, `ShippingService`,
  `NotificationService` — the subsystem classes with their own independent,
  more complex APIs.
- `OrderFacade` — provides a single simplified `placeOrder(OrderRequest)`
  method that hides the coordination logic required to reserve stock, take
  payment, schedule shipping and notify the customer.
- `OrderRequest` / `OrderConfirmation` — simple value objects passed to and
  returned from the facade.
- `FacadeDemo` — runnable entry point that exercises the facade.

## Run

```bash
./gradlew run
```

## Test

```bash
./gradlew test
```

## Learning Material

Start here if you are new to the pattern — the docs are ordered as a
learning path.

| Document | What it covers |
| --- | --- |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What to know and install before you start |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The problem the pattern solves, and why the naive approach hurts |
| [`docs/facade-pattern-explained.md`](docs/facade-pattern-explained.md) | The pattern itself, the code walked through, pitfalls, and comparisons |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Static structure |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Runtime call flow |
| [`docs/animation.html`](docs/animation.html) | Animated, step-by-step walkthrough — open in a browser. Optional narration via the **Narration** button |
| [`docs/session.md`](docs/session.md) | A 60-minute guided session plan for teaching it |
| [`video/`](video/) | A narrated ~6 minute video, plus the script and build pipeline |

### The pattern in one picture

![Facade pattern class diagram](docs/images/class-diagram.png)

### Video

`video/facade-pattern-explained.mp4` — 1080p, ~6 minutes, narrated.
An audio-only version is alongside it. See
[`video/README.md`](video/README.md) to rebuild or re-record it.
