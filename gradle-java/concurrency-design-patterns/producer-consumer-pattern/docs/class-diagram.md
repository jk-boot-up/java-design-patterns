# Producer–Consumer Pattern — Class Diagram

The single most important thing on this diagram: `BoundedOrderQueue` has a
fixed `capacity`, and nothing in `Checkout` or `Packer` can bypass it —
there is no path onto the queue except through a method that respects the
bound.

![Producer-Consumer pattern class diagram](images/class-diagram.png)

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

    class BoundedOrderQueue {
        <<pattern>>
        -int capacity
        +put(order)
        +offer(order, timeout, unit) boolean
        +take() Order
        +isFull() boolean
    }
    class Packer {
        <<pattern, Runnable>>
        +static Order POISON
        -List~Order~ packedLog
        +run()
        +packed() List
    }

    class InlineCheckout {
        <<naive>>
        +checkout(order) long
    }
    class ThreadPerOrderCheckout {
        <<naive>>
        +checkout(order)
        +liveThreads() int
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

    BoundedOrderQueue o-- Order : holds, up to capacity
    Packer --> BoundedOrderQueue : take()
    Packer ..> Packing : delegates packing to
    Packer ..> Order : names POISON, its own sentinel

    InlineCheckout ..> Packing : calls directly, on the caller's thread
    ThreadPerOrderCheckout ..> Packing : calls on a brand new thread, per order
```

</details>

## Reading The Diagram

**`Packer` depends on `BoundedOrderQueue` and on `Packing` — nothing else.**
It does not know whether it is being driven by the demo, a test, or five
producers at once; it only ever takes one order at a time and does
whatever `Packing` says.

**Neither naive class has any relationship to `BoundedOrderQueue` at all.**
`InlineCheckout` and `ThreadPerOrderCheckout` both talk to `Packing`
directly — one on the caller's own thread, one on a new thread per order —
because neither of them has a queue standing between arrival and packing.
That absence is the entire diagram's argument.
