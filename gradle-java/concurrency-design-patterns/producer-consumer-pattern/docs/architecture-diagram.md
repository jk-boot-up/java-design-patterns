# Producer–Consumer Pattern — Architecture Diagram

Where each piece runs, and what stands between the producer side and the
consumer side.

![Producer-Consumer pattern architecture diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    subgraph Producer["producer side — checkout thread(s)"]
        direction TB
        Checkout["Checkout / test thread"]
    end

    subgraph Boundary["the bound — the whole pattern"]
        direction TB
        Q["BoundedOrderQueue<br/>fixed capacity"]
    end

    subgraph Consumer["consumer side — packer thread"]
        direction TB
        Packer["Packer.run()<br/>one order at a time"]
    end

    subgraph Naive["naive — no boundary at all"]
        direction TB
        Inline["InlineCheckout<br/>packs on the caller's own thread"]
        PerOrder["ThreadPerOrderCheckout<br/>a brand new thread, per order,<br/>no limit anywhere"]
    end

    Checkout -->|put / offer, respects capacity| Q
    Q -->|take, blocks if empty| Packer

    Inline -.->|no queue, no other thread| Packer
    PerOrder -.->|no queue, unlimited threads| Packer
```

</details>

## Reading The Diagram

**Exactly one box sits between the producer side and the consumer side,
and it has a capacity.** That is the pattern in its entirety: not a queue,
a *bounded* queue.

**The naive box has no line into the boundary at all.** `InlineCheckout`
runs packing on the same thread as checkout — there is no second side to
have a boundary between. `ThreadPerOrderCheckout` has a second side, but no
boundary — every order gets a thread, with nothing capping how many exist
at once.
