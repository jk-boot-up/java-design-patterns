# Idempotent Consumer with Kafka Pattern — Architecture Diagram

Two containers and two copies of one service. Kafka holds the orders and each group's bookmark; Postgres holds the emails and the ids. The only memory that survives a copy stopping is the memory in a container — which is why the ids live in Postgres, beside the emails, and not in either copy.

![Idempotent Consumer with Kafka Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["checkout"]
    subgraph K["Kafka 4.3.1, in a container"]
        T[("topic of orders, places 0, 1, 2")]
        BM["group bookmark: the place written down"]
    end
    subgraph N["notifications service, group notifications"]
        A["copy A"]
        B["copy B"]
    end
    subgraph P["Postgres 18.6, in a container"]
        HM[("handled_messages: id is the primary key")]
        CF[("confirmations: one row per email")]
    end
    C -- "OrderPlaced, with its own id" --> T
    T -- "hands out from the bookmark" --> A
    T -- "hands out again, if A stopped first" --> B
    A -- "one transaction: id first, then email" --> HM
    A --> CF
    B -- "same id: Postgres writes nothing" --> HM
    A -- "after the commit: move the bookmark" --> BM
```

</details>
