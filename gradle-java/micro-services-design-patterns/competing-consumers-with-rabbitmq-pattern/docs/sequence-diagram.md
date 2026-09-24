# Competing Consumers with RabbitMQ Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Checkout sends five pick orders to the broker and goes back to selling. Picker A starts listening and tells the broker it may hold up to five orders at once. The broker hands it all five straight away. Picker A picks order one and says done, then order two and says done, and the broker forgets each of them. Picker A starts order three: it reserves the stock, and then it crashes, before it says done. The broker notices the connection has gone. It does not know that picker A had started only order three; it knows only that orders three, four and five were handed over and never said done. So it puts all three back in the queue, marked as seen before. Picker B starts listening and is handed all three, each with the mark on it. Picker B picks them and says done for each. Order three's stock has now been reserved twice. Eight deliveries, five orders picked, nothing waiting.

![Competing Consumers with RabbitMQ sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant Q as RabbitMQ queue
    participant A as picker A, prefetch 5
    participant B as picker B
    C->>Q: ORD-1 to ORD-5, then carry on selling
    A->>Q: listening, may hold 5
    Q->>A: ORD-1, ORD-2, ORD-3, ORD-4, ORD-5
    A->>Q: done ORD-1, done ORD-2
    Note over A: reserves stock for ORD-3, then crashes
    Q-->>Q: connection gone. put back ORD-3, ORD-4, ORD-5, marked seen before
    B->>Q: listening
    Q->>B: ORD-3, ORD-4, ORD-5, seen before: 3 of 3
    B->>Q: done, done, done
    Note over Q,B: deliveries 8 for 5 orders. ORD-3 stock reserved 2 times
```

</details>

The load-bearing sentence: **the broker forgets an order only when a picker says it is done, and a picker that dies hands back everything it was holding — which is how much it was allowed to hold, not how much it had started.**

For the default of no limit, the lost orders under automatic acknowledgement and the poison order, see [`uml-diagram.md`](uml-diagram.md).
