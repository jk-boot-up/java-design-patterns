# Identity Map Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The caller asks the session for the order. The session reads the order row, then asks itself for customer seven. It is not in the map, so it reads the customer row, builds the customer and stores it in the map. Later the caller asks for customer seven directly. This time it is in the map, so the session returns the same object with no database call at all.

![Identity Map pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant S as CustomerSession
    participant M as identity map
    participant DB as database
    Caller->>S: findOrder(100)
    S->>DB: select order 100
    S->>M: get(7), missing
    S->>DB: select customer 7
    S->>M: put(7, customer)
    Caller->>S: find(7)
    S->>M: get(7), found
    S-->>Caller: the same object, no database call
```

</details>

The load-bearing sentence: **the second ask cost nothing, and returned the very same object.**
