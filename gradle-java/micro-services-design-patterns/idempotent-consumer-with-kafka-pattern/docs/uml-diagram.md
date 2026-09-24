# Idempotent Consumer with Kafka Pattern — UML Sequence Diagrams

Four sequences. Two copies at once comes first, because it is the one thing the plain-Java version, which ran on one thread, could never show.

## 1. Two Copies At Once

Copy A is handed ORD-1 and holds its transaction open for longer than Kafka's patience of 3 seconds. Kafka hands ORD-1 to copy B. Postgres makes B wait on A's lock, then tells B the id is taken. Kafka refuses A's request to move the bookmark.

![Two copies at once](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant A as copy A, patience 3 seconds
    participant B as copy B
    participant P as Postgres
    K->>A: ORD-1
    A->>P: begin, insert id, insert email
    Note over K: A is judged stuck
    K->>B: ORD-1 again
    B->>P: insert the same id
    Note over B,P: sessions waiting on a lock: 1
    A->>P: commit
    P-->>B: 0 rows, skip. queued by B: 0
    A->>K: move the bookmark
    K-->>A: CommitFailedException
    Note over A,P: emails for ORD-1: 1
```

</details>

## 2. Kafka Sends It Again

Copy A handles three orders with no memory of any kind and stops before moving the bookmark. Copy B is handed the same three at the same places, with no mark on them.

![Kafka sends it again](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant K as Kafka
    participant A as copy A
    participant B as copy B
    participant P as Postgres
    C->>K: ORD-1, ORD-2, ORD-3 at places 0, 1, 2
    K->>A: places 0, 1, 2
    A->>P: 3 emails
    Note over A: crashes. place written down: none
    K->>B: places 0, 1, 2 again, no mark on them
    B->>P: 3 emails
    B->>K: move the bookmark to 3
    Note over K,P: deliveries 6 for 3 orders. emails 6
```

</details>

## 3. Where The Crash Lands

The same crash, first between two steps and then inside one transaction.

![Where the crash lands](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant A as copy A
    participant B as copy B
    participant P as Postgres
    Note over A,P: id written after the email, as a second step
    K->>A: ORD-1
    A->>P: email, committed
    Note over A: dies before writing the id. emails 1, ids 0
    K->>B: ORD-1 again
    B->>P: no id found. email again
    Note over P: emails for ORD-1: 2
    Note over A,P: id and email in one transaction
    K->>A: ORD-1
    A->>P: begin, id, email
    Note over A: dies before the commit
    Note over P: connection dropped. emails 0, ids 0
    K->>B: ORD-1 again
    B->>P: begin, id, email, commit
    Note over P: emails 1, ids 1
```

</details>

## 4. The Replay

Three orders placed two days ago are handled and their ids stored. The cleanup keeps ids for 24 hours; the topic keeps orders for 168. An operator replays the group.

![The replay](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as operator
    participant K as Kafka, keeps orders 168 hours
    participant A as copy A
    participant B as copy B
    participant P as Postgres
    K->>A: 3 orders, placed two days ago
    A->>P: 3 ids, 3 emails
    A->>K: move the bookmark to 3
    Note over P: cleanup keeps ids 24 hours. deletes 3
    O->>K: move the group back to the start
    K->>B: handed again: 3
    B->>P: no ids found. 3 more emails
    Note over P: emails queued: 6
```

</details>
