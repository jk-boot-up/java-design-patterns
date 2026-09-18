# Prerequisites

## Knowledge Prerequisites

### Required

- **Java basics** — interfaces, packages, and what it means for one class to
  import another.
- **Records** — Java 16's `record`.
- **[`../layered-architecture-pattern`](../layered-architecture-pattern)** —
  strongly recommended first. This project's naive version is that
  project's application layer, honestly reproduced, and the explained
  document assumes you already know why an application layer naming its
  storage interface is the normal, allowed shape of layering.

### Explicitly NOT required

- **No real HTTP, no real database.** `HttpCheckoutAdapter` simulates a
  JSON request as a `Map`; there is no socket, no server, no client
  anywhere in this project.
- **No dependency injection framework.** Wiring is six lines in the
  composition root, by hand.

## A 60-Second "Ports And Adapters" Primer

A **port** is an interface, declared by the core, in the core's own
vocabulary — "I need something that can store an order", not "I need a SQL
table". An **adapter** is a class outside the core that either implements a
port (a **driven** adapter — the core calls it) or calls into the core
through its use case (a **driving** adapter — it calls the core).

The test worth applying to any class you are unsure about: **who names
whom?** If the core names the adapter, something is wrong. If the adapter
names the core — either by implementing an interface the core declared, or
by holding a reference to the core's use case and calling it — that is
correct, in both directions.

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | Records, the Gradle toolchain |
| Gradle | none to install | The wrapper (`./gradlew`) fetches what it needs |

### Verify Your Setup

```bash
java -version
cd architectural-design-patterns/hexagonal-architecture-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 17 tests
./gradlew -q run       # expect five acts of output, then ACCEPTANCE
```

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md)
2. Run `./gradlew -q run` and read all five acts
3. [`hexagonal-architecture-pattern-explained.md`](hexagonal-architecture-pattern-explained.md)
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
5. [`animation.html`](animation.html)
6. The source, starting with `core/port/OrderStore.java`, then `core/PlaceOrderService.java`
7. `ArchitectureRuleCatchesTheShortcutTest` and `BothSidesAgreeTest`
