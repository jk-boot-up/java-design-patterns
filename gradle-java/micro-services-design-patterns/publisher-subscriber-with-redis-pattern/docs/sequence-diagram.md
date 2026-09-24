# Publisher-Subscriber with Redis Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Email and analytics each open their own connection to Redis and subscribe to the name orders dot placed. Then analytics stops reading. The order service publishes the first order of a flash sale, and Redis answers two receivers. Email reads it straight away. Analytics does not, so Redis puts it on a pile it keeps for analytics alone. The order service keeps publishing and never waits. Email keeps reading every order. The pile for analytics keeps growing until it passes the limit of one megabyte. At that moment Redis closes the connection to analytics, throws the pile away, and adds one to its counter of listeners cut off. The next publish is answered with one receiver, not two. Nobody tells the order service.

![Publisher-Subscriber with Redis sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as order service
    participant R as Redis
    participant E as email
    participant A as analytics
    E->>R: subscribe orders.placed
    A->>R: subscribe orders.placed
    Note over A: stops reading
    O->>R: publish ORD-1
    R-->>O: 2 receivers
    R->>E: ORD-1, read at once
    R-->>R: ORD-1 onto the pile for analytics
    O->>R: publish, round after round, never waiting
    R->>E: every order
    R-->>R: pile for analytics passes 1mb
    R-xA: connection closed, pile thrown away
    Note over R: listeners cut off for falling behind: 1
    O->>R: publish the next order
    R-->>O: 1 receiver
```

</details>

The load-bearing sentence: **Redis never waits for a slow subscriber, and past the limit it cuts that subscriber off — the publisher only ever sees a smaller number.**

For the second process, the late subscriber and the patterns, see [`uml-diagram.md`](uml-diagram.md).
