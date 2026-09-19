# Data Mapper Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The caller asks the mapper to find customer one. The mapper
asks the customers table for row one, then asks the addresses table for row
one. It builds an address from the second row, builds a customer from the
first, and hands the customer back. The customer never spoke to a table.

![Data Mapper pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant M as CustomerMapper
    participant T1 as customers table
    participant T2 as addresses table
    Caller->>M: find(1)
    M->>T1: select id=1
    T1-->>M: row
    M->>T2: select id=1
    T2-->>M: row
    M-->>Caller: Customer
```

</details>

The load-bearing sentence: **the customer never spoke to a table.**
