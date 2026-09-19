# Optimistic Offline Lock Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Both clerks load the product at version one. Clerk A saves a new price. The store sees version one, matches, writes it, and moves to version two. Clerk B saves the stock count, still holding version one. The store sees the row is at version two, and refuses with a stale write error. Clerk B reloads, gets version two with the new price, reapplies the count, and saves at version two. It is accepted.

![Optimistic Offline Lock pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as clerk A
    participant B as clerk B
    participant S as store
    A->>S: load (v1)
    B->>S: load (v1)
    A->>S: save price (v1)
    S-->>A: ok, now v2
    B->>S: save stock (v1)
    S-->>B: StaleWrite
    B->>S: load (v2), save stock (v2)
    S-->>B: ok, now v3
```

</details>

The load-bearing sentence: **a clash is found when someone saves, not before.**
