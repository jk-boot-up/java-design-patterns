# Future/Promise Pattern — Class Diagram

The single most important thing on this diagram: `FutureAndPromise` is the
only class that touches a `CompletableFuture` directly — every other
pattern class works through the plain `Future` returned by
`ExecutorService.submit`, because the reader/writer split is this
project's own lesson, not something every future-using class needs to
know about.

![Future/Promise pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Lookup~T~ {
        <<interface, domain>>
        +fetch(sku) T
    }
    class ProductPageView {
        <<record, domain>>
        +BigDecimal price
        +int stock
        +double rating
        +long elapsedNanos
    }

    class ConcurrentProductPage {
        <<pattern>>
        +render(sku) ProductPageView
    }
    class FutureAndPromise {
        <<pattern, static>>
        +handOff(writerWork) T
    }
    class AsyncFailure {
        <<pattern, static>>
        +attempt(pool, doomedTask) Outcome
    }
    class UnboundedWait {
        <<pattern, static>>
        +attemptGet(pool, gate, timeoutMillis) Outcome
    }
    class CooperativeCancellation {
        <<pattern, static>>
        +attempt(pool) Outcome
    }

    class SequentialProductPage {
        <<naive>>
        +render(sku) ProductPageView
    }

    class Gate {
        <<harness>>
        +open()
        +awaitOpen()
    }
    class Rendezvous {
        <<harness>>
        +meet()
    }
    class StepExecutor {
        <<harness, Executor>>
        +runNext() boolean
    }

    ConcurrentProductPage ..> Lookup : submits each lookup, in parallel
    ConcurrentProductPage ..> ProductPageView : assembles from three Futures

    SequentialProductPage ..> Lookup : calls each lookup, one after another
    SequentialProductPage ..> ProductPageView : assembles after all three return

    UnboundedWait ..> Gate : parks the doomed task on one, never opened
```

</details>

## Reading The Diagram

**`ConcurrentProductPage` and `SequentialProductPage` share every
dependency except one another.** Both take the same three `Lookup`
instances and produce the same `ProductPageView`; the only difference the
diagram cannot show directly is *when* each lookup's call happens
relative to the others — which is exactly the point [`sequence-diagram.md`](sequence-diagram.md)
exists to carry instead.

**Three classes have no relationship to `Lookup` or `ProductPageView` at
all.** `AsyncFailure`, `UnboundedWait` and `CooperativeCancellation` are
not about the product page — they are static demonstrations about
`Future` itself, each proving one honest cost the pattern does not
advertise on its own.
