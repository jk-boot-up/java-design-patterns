# Session Guide — Clean Architecture Pattern

A 60-minute session built around one moment: control flowing one way while
a dependency points the other.

## Learning Objectives

By the end of the session a participant can:

1. State the concentric rule in one sentence.
2. Point at the exact line in `PlaceOrderInteractor` where control and
   dependency disagree, and explain why.
3. Name the one genuinely new thing this project adds beyond Hexagonal
   Architecture, and the one thing that is the same idea again.
4. Read the ArchUnit layered-architecture rule and say what it forbids.
5. Perform, or trace by hand, the two-at-once forced change.
6. State when Clean Architecture is over-engineering, specifically.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | Setup, and the naive interactor's constructor |
| 0:08–0:20 | Four circles, one rule |
| 0:20–0:32 | The dependency-inversion moment, in code |
| 0:32–0:42 | The forced change, both new at once |
| 0:42–0:50 | The rule, as ArchUnit's own layered-architecture API |
| 0:50–0:57 | Exercises |
| 0:57–1:00 | When this is too much, and wrap-up |

## 0:00–0:08 — Setup

```bash
cd architectural-design-patterns/clean-architecture-pattern
./gradlew -q run
```

Open `NaivePlaceOrderInteractor`'s constructor. Ask: how many circles out
does this class reach?

## 0:08–0:20 — Four Circles, One Rule

Draw the four circles on the board before opening any code. Ask the room to
place each class they have seen so far — `Order`, `PlaceOrderInteractor`,
`CheckoutController`, `InMemoryOrderRepository` — in the right ring.

## 0:20–0:32 — The Dependency-Inversion Moment

Read act three of the demo output aloud, one line at a time. Open
`PlaceOrderInteractor.java` and find `orders.save(order)`. Ask: what type
is `orders`? Where is that type declared? Where is the class that really
implements it? Draw the arrow the source code creates, and draw the arrow
the call at runtime actually travels. They point opposite ways.

## 0:32–0:42 — The Forced Change

Open `BatchOrderController` and `FileBackedOrderRepository` side by side.
Ask: what do both of them depend on that already existed? Run:

```bash
./gradlew test --tests BothAddedAtOnceTest
```

## 0:42–0:50 — The Rule

Open `ArchitectureTest.java`. Note that it uses a different ArchUnit API
than the previous two projects — `Architectures.layeredArchitecture()`
rather than `noClasses().should()`. Ask why a purpose-built API might suit
three ordered layers better than a single pairwise rule.

```bash
./gradlew test --tests ArchitectureRuleCatchesTheShortcutTest
```

## 0:50–0:57 — Exercises

1. **Add a third delivery mechanism.** A `ScheduledReorderController` that
   calls `PlaceOrderInputBoundary` on a timer. Confirm zero changes to
   `usecases`.
2. **Count the files for real.** Pick a fifth, imaginary feature this small
   — "cancel an order" — and estimate how many files it would need in this
   architecture. Compare with how many it would need as one method on one
   class.
3. **Break the rule on purpose.** Add an import of
   `InMemoryOrderRepository` to `PlaceOrderInteractor`, run the tests, read
   the failure, then revert it.

## 0:57–1:00 — When This Is Too Much, And Wrap-Up

Ask the room to count: how many files did this project need for one
feature? Fourteen. Ask when that is worth it, and push for a concrete
answer: long-lived systems, more than one delivery mechanism or data
source, a domain worth protecting.

Close with the sentence worth remembering: control flows outward; the
dependency points inward. Those are allowed to disagree, and that
disagreement is the whole of Clean Architecture.
