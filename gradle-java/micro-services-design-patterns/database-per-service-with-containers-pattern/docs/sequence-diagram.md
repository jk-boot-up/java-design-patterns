# Database per Service with Containers Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Customer cust-7 opens the order history page. The page first asks the Orders service. The Orders service sends one SQL query to its own Postgres database, and Postgres answers with two orders: ord-101, one of SKU-KETTLE, and ord-102, four of SKU-MUG. The page collects the two skus. Then it asks the Catalog service for both names in one call. The Catalog service sends one find to its own MongoDB database, and MongoDB answers with two documents: the Stainless Steel Kettle and the Blue Stoneware Mug. The page puts each name beside its order and shows two rows. Two round trips, one to each engine, where the shared database needed one join. Neither service ever touched the other's database; neither could.

![Database per Service with Containers sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as order history page
    participant O as Orders service
    participant PG as Postgres orders db
    participant C as Catalog service
    participant M as MongoDB catalog db
    P->>O: orders for cust-7
    O->>PG: SELECT ... WHERE customer_id = cust-7
    PG->>O: ord-101 SKU-KETTLE x1, ord-102 SKU-MUG x4
    O->>P: 2 orders
    P->>C: names for SKU-KETTLE and SKU-MUG
    C->>M: find, _id in both skus
    M->>C: 2 documents
    C->>P: Stainless Steel Kettle, Blue Stoneware Mug
    Note over P: 2 rows, 2 round trips, one to each engine
```

</details>

The load-bearing sentence: **each service asks only its own engine, and the page does the join in Java, because no engine holds both halves.**

For the old join tried from both sides, the delete nothing refuses, and the rollback that reaches one engine, see [`uml-diagram.md`](uml-diagram.md).
