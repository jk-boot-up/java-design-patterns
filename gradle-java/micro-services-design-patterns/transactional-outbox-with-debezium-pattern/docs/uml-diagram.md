# Transactional Outbox with Debezium Pattern — UML Sequence Diagrams

Four sequences. The log, not the table, comes first, because it is the one thing the plain-Java version, whose relay read a table, could never show.

## 1. The Log, Not The Table

Each transaction writes the order, writes the outbox row, and deletes the row before committing. The table ends empty. Debezium reads the inserts from the log and sends all three.

![The log, not the table](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant P as Postgres
    participant D as Debezium
    participant K as Kafka
    loop ORD-1, ORD-2, ORD-3
        C->>P: begin, insert order, insert outbox row, delete it, commit
        P->>D: the insert, from the log
        D->>K: one event
    end
    Note over P: orders 3. outbox rows 0
    Note over K: events in Kafka 3
```

</details>

## 2. Two Writes, One Crash

With no outbox, the checkout talks to both systems itself. Saving first and dying leaves an order nobody hears about. Sending first and dying announces an order that does not exist.

![Two writes, one crash](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant P as Postgres
    participant K as Kafka
    C->>P: save ORD-1, commit
    Note over C: dies before sending
    Note over P,K: ORD-1 in Postgres yes. events in Kafka 0
    C->>K: send ORD-2
    Note over C: dies before saving
    Note over P,K: events in Kafka 1. ORD-2 in Postgres no
```

</details>

## 3. Debezium Is Down

Debezium stops and lets go of the slot. The checkout takes three orders anyway. Postgres keeps the log for the slot, with no limit. Debezium starts again and is sent all three.

![Debezium is down](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant P as Postgres and slot
    participant D as Debezium
    participant K as Kafka
    D->>P: stop. slot active no
    C->>P: ORD-1, ORD-2, ORD-3, each with its outbox row
    Note over P: orders 3. log kept for the slot grew. limit -1
    Note over K: events in Kafka 0
    D->>P: start. carry on from the slot
    P->>D: the 3 changes it kept
    D->>K: ORD-1, ORD-2, ORD-3
```

</details>

## 4. Sent, But Not Written Down

Debezium sends ORD-1 and ORD-2 and dies before writing down its position. It starts again from the last position it wrote down, and is sent both again.

![Sent, but not written down](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as Postgres and slot
    participant D as Debezium
    participant K as Kafka
    P->>D: ORD-1, ORD-2
    D->>K: ORD-1/OrderPlaced, ORD-2/OrderPlaced
    Note over D: dies before writing down its position
    Note over K: events in Kafka 2
    D->>P: start again from the last position written down
    P->>D: ORD-1, ORD-2 again
    D->>K: the same two, the same ids
    Note over K: events in Kafka 4 for 2 orders
```

</details>
