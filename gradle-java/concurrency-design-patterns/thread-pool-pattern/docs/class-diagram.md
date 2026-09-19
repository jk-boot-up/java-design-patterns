# Thread Pool Pattern — Class Diagram

The single most important thing on this diagram: `BoundedPackingPool` owns
two bounds, not one — `workers` and `queueCapacity` — and both are
constructor arguments, chosen on purpose, rather than defaults buried
inside a factory method.

![Thread Pool pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Order {
        <<record, domain>>
        +String id
        +String sku
    }
    class Packing {
        <<interface, domain>>
        +pack(order)
    }

    class BoundedPackingPool {
        <<pattern>>
        -int workers
        -int queueCapacity
        +submit(order, packing)
        +queueDepth() int
        +rejectedCount() int
    }
    class PoolStarvation {
        <<pattern, static>>
        +attemptNestedSubmit(pool, timeoutMillis) Outcome
    }
    class VirtualThreadFlood {
        <<pattern, static>>
        +floodSafely(count, gate) FloodResult
    }

    class ThreadPerOrderPacking {
        <<naive>>
        +submit(order)
        +liveThreads() int
    }
    class UnboundedPoolPacking {
        <<naive>>
        -int workers
        +submit(order, packing)
        +backlog() int
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

    BoundedPackingPool ..> Packing : delegates every submitted order to
    BoundedPackingPool o-- Order : wraps each order in a queued task

    UnboundedPoolPacking ..> Packing : same delegation, no bound on the queue
    ThreadPerOrderPacking ..> Packing : calls on a brand new thread, per order

    PoolStarvation ..> BoundedPackingPool : demonstrates the deadlock any fixed pool can reach
    VirtualThreadFlood ..> ThreadPerOrderPacking : same measurement, virtual threads instead of platform ones
```

</details>

## Reading The Diagram

**`BoundedPackingPool` has two bounds where `UnboundedPoolPacking` has
one.** Both wrap the same idea — a fixed set of workers — but only the
pattern version also bounds what is allowed to wait behind them. That
second bound is the entire diagram's argument: a class with a worker count
and nothing else has fixed one leak and left another one open.

**`PoolStarvation` and `VirtualThreadFlood` are not alternatives to
`BoundedPackingPool` — they are static demonstrations about pools in
general**, which is why neither one is a wrapper around a queue the way
the other three classes are. One shows a failure any fixed pool can reach;
the other shows what changed, and what did not, about the cost `ThreadPerOrderPacking`
measures.
