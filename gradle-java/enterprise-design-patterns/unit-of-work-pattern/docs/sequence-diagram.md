# Unit of Work Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The placement changes each product and registers each change with the unit of work. It registers the lines, then the order. Nothing has touched the database. Then commit is called. The unit of work sorts its changes so the order comes first, opens a transaction, and writes the order, the three lines and the three stock updates. If any write is rejected, it rolls back and the database is exactly as it was.

![Unit of Work pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as placement
    participant U as UnitOfWork
    participant DB as database
    P->>U: registerDirty(product 1..3)
    P->>U: registerNew(lines)
    P->>U: registerNew(order)
    Note over DB: still untouched
    P->>U: commit()
    U->>DB: begin
    U->>DB: insert order, lines, update products
    U->>DB: commit, or rollback if rejected
```

</details>

The load-bearing sentence: **nothing touched the database until commit, and then it was all or nothing.**
