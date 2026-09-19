# Thread Pool Pattern — Architecture Diagram

Where each piece runs, and the two separate bounds that stand between an
order arriving and it actually being packed.

![Thread Pool pattern architecture diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    subgraph Submitter["submitter side — checkout thread(s)"]
        direction TB
        Checkout["Checkout / test thread"]
    end

    subgraph Boundary["two bounds, both chosen on purpose"]
        direction TB
        Q["queue<br/>fixed capacity"]
        W["worker pool<br/>fixed count"]
    end

    subgraph Naive["naive — one bound, or none"]
        direction TB
        PerOrder["ThreadPerOrderPacking<br/>no worker bound, no queue at all"]
        Unbounded["UnboundedPoolPacking<br/>worker bound, queue unbounded"]
    end

    subgraph Failure["a failure every fixed pool can reach"]
        direction TB
        Starve["PoolStarvation<br/>a task waits on a task<br/>in this same pool"]
    end

    Checkout -->|submit, rejected on the spot if full| Q
    Q -->|handed to a free worker| W

    PerOrder -.->|no bound at all| W
    Unbounded -.->|bounded workers, unbounded queue| Q

    W -.->|nested submit + wait, no free worker left| Starve
```

</details>

## Reading The Diagram

**Two boxes sit between submission and packing, not one.** §46's diagram
had a single bounded queue; this one adds the worker pool itself as a
second, separate bound — and the naive path shows what happens with only
one of the two in place, or neither.

**`PoolStarvation` points back into the worker box, not around it.** The
deadlock it demonstrates is not a missing bound — the pool in that
scenario is bounded correctly. It is what a bounded pool does when a task
already inside it asks the same pool for a second worker that does not
exist.
