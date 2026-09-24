# Idempotent Consumer with Kafka Pattern — Data Flow Diagram

What one copy does with one order, and the three places a crash can land. Only one order of steps makes every crash safe: the id and the email committed together, and the Kafka bookmark moved after that.

![Idempotent Consumer with Kafka Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    In(["Kafka hands ORD-1 to a copy"])
    Begin["open a database transaction"]
    Insert["insert the message id, on conflict do nothing"]
    Wait{"another copy holds this id, not committed?"}
    Lock["Postgres makes this copy wait"]
    Rows{"rows written?"}
    Skip["0 rows: handled already, write nothing"]
    Email["1 row: queue the email in the same transaction"]
    Commit["commit: the id and the email together"]
    Mark["ask Kafka to move the bookmark"]
    Done(["ORD-1 handled, exactly once"])
    Crash1["crash before the commit: Postgres keeps neither, Kafka hands ORD-1 out again"]
    Crash2["crash after the commit: Kafka hands ORD-1 out again, the id is found, nothing written"]
    In --> Begin --> Insert --> Wait
    Wait -- yes --> Lock --> Rows
    Wait -- no --> Rows
    Rows -- "0" --> Skip --> Mark
    Rows -- "1" --> Email --> Commit --> Mark --> Done
    Email -.-> Crash1
    Commit -.-> Crash2
```

</details>
