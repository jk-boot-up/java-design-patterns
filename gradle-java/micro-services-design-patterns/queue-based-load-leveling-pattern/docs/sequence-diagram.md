# Queue-Based Load Leveling Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A hundred orders arrive at the start of a sale. Each is put in the queue, and each customer is told the order was received. The worker takes ten in the first tick, ten in the next, and so on, so that after ten ticks the queue is empty. The last order waited nine ticks, and nothing was refused.

![Queue-Based Load Leveling pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as 100 orders
    participant Q as queue
    participant W as worker, 10 a tick
    C->>Q: all 100 at tick 0
    Q-->>C: received
    W->>Q: take 10 (tick 0)
    W->>Q: take 10 (tick 1)
    Note over W,Q: ...until empty at tick 9
```

</details>

The load-bearing sentence: **the queue absorbs the difference between the burst and the worker's pace.**
