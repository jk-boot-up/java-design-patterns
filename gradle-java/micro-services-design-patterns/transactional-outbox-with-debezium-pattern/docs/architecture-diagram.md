# Transactional Outbox with Debezium Pattern — Architecture Diagram

Two containers and one program. The checkout writes only to Postgres. Postgres writes every change to its log first; Debezium, inside the demo's program, is sent the outbox changes from that log through a replication slot and forwards each one to Kafka. There is no arrow from the checkout to Kafka, and that missing arrow is the pattern.

![Transactional Outbox with Debezium Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["checkout: OutboxCheckout"]
    subgraph P["Postgres 18.6, in a container, wal_level=logical"]
        O[("orders")]
        OB[("outbox")]
        W[["write-ahead log"]]
        S["replication slot orders_outbox: keeps the log until confirmed"]
    end
    subgraph J["the demo's own Java program"]
        D["Debezium 3.6.3 embedded engine: Postgres connector and outbox event router"]
        F[("offsets file: how far it has read")]
    end
    subgraph K["Kafka 4.3.1, in a container"]
        T[("order-events: partitions 0, 1, 2")]
    end
    C -- "one transaction" --> O
    C -- "same transaction" --> OB
    O --> W
    OB --> W
    W --> S
    S -- "committed outbox changes, in commit order" --> D
    D -- "key = order id, headers id and eventType" --> T
    D -- "after Kafka accepts" --> F
    D -. "confirms its position" .-> S
```

</details>
