# Simple Factory Pattern

Demonstrates the **Simple Factory** creational idiom using an e-commerce
payment selection as an example.

- `PaymentMethod` — the sealed product interface every payment method
  implements.
- `CreditCardPayment`, `UpiPayment`, `PayPalPayment`, `NetBankingPayment` —
  the concrete products, each doing its own specialised work.
- `PaymentMethodFactory` — a single `create(...)` method that turns a
  `PaymentType` (or a `String` from a form) into the right implementation.
  It is the only class in the project that calls `new` on a payment method.
- `PaymentRequest` / `PaymentReceipt` — simple value objects passed to and
  returned from a payment method.
- `CheckoutService` — the client; it names a type and uses the result purely
  through the interface.
- `SimpleFactoryDemo` — runnable entry point that pays for the same order
  four different ways.

## Run

```bash
./gradlew run
```

Which prints:

```text
Checkout: paying for ORD-1001 with Credit Card
Credit Card: authorising 49.98 for order ORD-1001
Credit Card: capturing the authorised amount
Checkout: done, transaction CC-677AF93B
Receipt: PaymentReceipt[transactionId=CC-677AF93B, method=Credit Card, amount=49.98]

Checkout: paying for ORD-1001 with UPI
UPI: sending a collect request to CUST-001
UPI: customer approved 49.98 in the payments app
Checkout: done, transaction UPI-98332C73
Receipt: PaymentReceipt[transactionId=UPI-98332C73, method=UPI, amount=49.98]

Checkout: paying for ORD-1001 with PayPal
PayPal: redirecting CUST-001 to the PayPal checkout
PayPal: payment of 49.98 completed
Checkout: done, transaction PP-424476F7
Receipt: PaymentReceipt[transactionId=PP-424476F7, method=PayPal, amount=49.98]

Checkout: paying for ORD-1001 with Net Banking
Net Banking: opening the bank's login page for CUST-001
Net Banking: bank confirmed a transfer of 49.98
Checkout: done, transaction NB-6B3E0428
Receipt: PaymentReceipt[transactionId=NB-6B3E0428, method=Net Banking, amount=49.98]
```

The identifiers are generated per run, so the transaction, order and
tracking codes differ each time; everything else is stable.

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
| [`docs/simple-factory-pattern-explained.md`](docs/simple-factory-pattern-explained.md) | The pattern itself, the code walked through, pitfalls, and comparisons |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Static structure |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Runtime call flow |
| [`docs/animation.html`](docs/animation.html) | Animated, step-by-step walkthrough — open in a browser. Optional narration via the **Narration** button |
| [`docs/session.md`](docs/session.md) | A 60-minute guided session plan for teaching it |
| [`docs/youtube.md`](docs/youtube.md) | Title, description, chapters and thumbnail for publishing the video |
| [`docs/thumbnail.png`](docs/thumbnail.png) | The 1280×720 image to upload as the YouTube thumbnail |
| [`docs/spec.md`](docs/spec.md) | The project specification — problem, code, video and publishing quality bar. Also as [`spec.html`](docs/spec.html) |
| [`video/`](video/) | A narrated ~8 minute video, plus the script and build pipeline |

### The pattern in one picture

![Simple Factory pattern class diagram](docs/images/class-diagram.png)

### Video

`video/simple-factory-pattern-explained.mp4` — 1080p, ~8 minutes, narrated.
An audio-only version is alongside it. See
[`video/README.md`](video/README.md) to rebuild or re-record it.

### Related

[`../../structural/facade-pattern`](../../structural/facade-pattern) — the Facade pattern, built the
same way. Facade is *structural* (simplifying how things are used); Simple
Factory is *creational* (deciding what gets built).
