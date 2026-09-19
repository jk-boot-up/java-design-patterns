# Onion Architecture Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The console gets a line of text and calls the use case. The use case builds an order, asks the pricing rule to price it, and gives it to the repository, which it knows only as an idea. The real storage, on the outside, keeps it. The storage refers to the order, and the order never refers to the storage.

![Onion Architecture pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant U as console
    participant A as place order
    participant P as pricing
    participant R as repository
    U->>A: place(ORD-1, lines)
    A->>P: price(order)
    P-->>A: discount applied
    A->>R: save(order)
    R-->>A: stored
    A-->>U: order
```

</details>

The load-bearing sentence: **the repository is an idea to the inside, and a real store on the outside.**
