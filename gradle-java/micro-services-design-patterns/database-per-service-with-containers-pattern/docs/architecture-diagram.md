# Database per Service with Containers Pattern — Architecture Diagram

Two services, two containers, two engines. Each service has a connection to its own database and to nothing else. The only way from one side to the other is through the order history page, in Java, one question to each service.

![Database per Service with Containers Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    Page["order history page, cust-7: asks both, puts the answers together"]
    subgraph Java["the demo's JVM"]
        OS["Orders service: a JDBC connection, nothing else"]
        CS["Catalog service: a MongoDB client, nothing else"]
    end
    subgraph PG["Postgres 18.6 container"]
        DBO[("database orders: 1 table, SQL")]
        DBS[("database shop: before the split, both teams' tables")]
    end
    subgraph MG["MongoDB 8.3.11 container"]
        DBC[("database catalog: products, 1 document each, any shape")]
    end
    Page --> OS
    Page --> CS
    OS -- "SQL" --> DBO
    CS -- "find, update, delete" --> DBC
    DBO -. "no join, no foreign key, no shared transaction" .- DBC
```

</details>
