# Observer with Spring Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The caller ships an order. The order marks itself shipped, then publishes the event. Inventory runs first and succeeds. Email runs second and throws. The exception travels back up through the publisher and the order, and lands on the caller. Analytics and the warehouse feed never run.

![Observer with Spring pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant O as OrderService
    participant P as publisher
    participant I as inventory
    participant E as email
    C->>O: ship
    O->>P: publishEvent
    P->>I: onChanged
    P->>E: onChanged
    E-->>C: IllegalStateException
    Note over P: analytics and warehouse skipped
```

</details>

The load-bearing sentence: **a synchronous publish is a method call, and a failure travels back to the caller.**
