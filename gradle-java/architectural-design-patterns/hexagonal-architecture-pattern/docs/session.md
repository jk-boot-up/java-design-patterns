# Session Guide — Hexagonal Architecture Pattern

A 60-minute session built around the question "who is allowed to name
whom?"

## Learning Objectives

By the end of the session a participant can:

1. Define a port and an adapter, and say which one names the other.
2. Explain the one-move difference between this project and Layered
   Architecture.
3. Distinguish a driving adapter from a driven one.
4. Read the ArchUnit rule and say what it forbids.
5. Perform, or trace by hand, both halves of the forced change.
6. State one honest reason this architecture is sometimes not worth it.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | Setup, and the naive service's constructor |
| 0:08–0:20 | Ports and adapters, and the one-move difference |
| 0:20–0:32 | The driving side — HTTP and CLI, same core |
| 0:32–0:42 | The forced change, both halves |
| 0:42–0:50 | The rule, as a test |
| 0:50–0:57 | Exercises |
| 0:57–1:00 | When this is too much, and wrap-up |

## 0:00–0:08 — Setup

```bash
cd architectural-design-patterns/hexagonal-architecture-pattern
./gradlew -q run
```

Open `NaivePlaceOrderService`'s constructor. Ask: what would you have to
construct to unit-test this class? Three concrete adapters, every time.

## 0:08–0:20 — Ports And Adapters

Open `core/port/OrderStore.java`, then `adapter/persistence/InMemoryOrderStore.java`.
Ask which one was written first, conceptually — the answer the project
insists on is the port, because the core should never be waiting on an
adapter to know what it needs.

Put `layered-architecture-pattern`'s `OrderTable` interface next to this
project's `OrderStore` side by side, if the room has seen that project.
Same three methods. Different package. That is the whole move.

## 0:20–0:32 — The Driving Side

Open `HttpCheckoutAdapter` and `CliCheckoutAdapter`. Ask the room: which one
does `PlaceOrderService` know about? Neither — it has no import of either
class. Run:

```bash
./gradlew test --tests BothSidesAgreeTest
```

## 0:32–0:42 — The Forced Change, Both Halves

Read act three and act four of the demo output together. Ask: how many
lines of `PlaceOrderService.java` changed for either swap? Zero, both
times. Put the count on the board: fourteen core classes, none of them
opened, for two independent swaps.

## 0:42–0:50 — The Rule, As A Test

```bash
./gradlew test --tests ArchitectureRuleCatchesTheShortcutTest
```

Read the failure and find `NaivePlaceOrderService` in it by name.

## 0:50–0:57 — Exercises

1. **Write a third driving adapter.** A `ConsoleMenuAdapter` that reads one
   hard-coded selection and calls the same `PlaceOrderService`. Confirm
   `PlaceOrderService.java` needs no change.
2. **Add a port on purpose, without an adapter yet.** Declare
   `LoyaltyPoints` in `core.port` and leave it unimplemented. Discuss:
   is an unused port a cost, or a promise?
3. **Break the rule on purpose.** Add an import of
   `InMemoryOrderStore` to `PlaceOrderService`, run the tests, read the
   failure, then revert it.

## 0:57–1:00 — When This Is Too Much, And Wrap-Up

Ask directly: for an application that will only ever have one database and
one caller, is this worth building? Push for "often, no" as the honest
answer, and ask what has to be true for the answer to flip to yes — a real
second adapter, on either side, that is actually going to be built.

Close with the sentence worth remembering: hexagonal architecture is not
about databases. It is about who is allowed to name whom.
