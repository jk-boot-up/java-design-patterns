# Transactional Outbox with Debezium Pattern — Data Flow Diagram

One order from checkout to Kafka, and the three places a crash can land. Only the crash in the last gap costs anything, and what it costs is a duplicate, never a loss.

![Transactional Outbox with Debezium Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    In(["a customer checks out ORD-1"])
    Begin["open a transaction"]
    Order["insert the order"]
    Row["insert the outbox row, and delete it again if you like"]
    Commit{"commit?"}
    Gone["rolled back: neither row, nothing in the log to send"]
    Log["Postgres writes the commit to its log"]
    Read["Debezium is sent the change through the slot"]
    Route["outbox router: key ORD-1, header id ORD-1/OrderPlaced"]
    Send["Kafka accepts it on the key's partition"]
    Write["Debezium writes down its position and confirms it to the slot"]
    Done(["ORD-1 announced"])
    Crash1["checkout dies before the commit: nothing saved, nothing sent"]
    Crash2["Debezium down: the slot keeps the log, and it is sent on restart"]
    Crash3["Debezium dies after the send, before writing down: sent again, same id"]
    In --> Begin --> Order --> Row --> Commit
    Commit -- "no" --> Gone
    Commit -- "yes" --> Log --> Read --> Route --> Send --> Write --> Done
    Row -.-> Crash1
    Log -.-> Crash2
    Send -.-> Crash3
```

</details>
