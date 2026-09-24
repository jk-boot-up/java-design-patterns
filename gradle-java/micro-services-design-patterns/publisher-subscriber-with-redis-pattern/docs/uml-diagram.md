# Publisher-Subscriber with Redis Pattern — UML Sequence Diagrams

Four sequences. The cut-off comes first, because it is the one thing a topic inside one program can never show.

## 1. A Subscriber That Cannot Keep Up

Analytics stops reading during a flash sale. Redis keeps its unread orders in a pile, and when the pile passes the limit, closes the connection.

![A subscriber that cannot keep up](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as order service
    participant R as Redis
    participant E as email
    participant A as analytics
    Note over A: stops reading
    O->>R: rounds of 1000 orders
    R-->>O: first order: 2 receivers
    R->>E: every one
    R-->>R: pile for analytics passes 1mb
    R-xA: connection closed
    R-->>O: last order: 1 receiver
    Note over A: reads again, gets some, not all
```

</details>

## 2. Publish Once, To Another Process

Three subscribers in the demo's own program, and a fourth in a second Java process. The order service publishes once each time.

![Publish once, to another process](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as order service
    participant R as Redis
    participant S as inventory, email, analytics
    participant L as loyalty, second process
    O->>R: publish ORD-1
    R-->>O: 3 receivers
    R->>S: ORD-1, three copies
    L->>R: subscribe orders.placed
    O->>R: publish ORD-2
    R-->>O: 4 receivers
    R->>L: ORD-2
    Note over L: prints ORD-2, exits with code 0
```

</details>

## 3. A Subscriber That Arrives Late

Three orders go out while only email listens. Loyalty joins, and sees only what comes after.

![A subscriber that arrives late](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as order service
    participant R as Redis
    participant E as email
    participant L as loyalty
    O->>R: ORD-1, ORD-2, ORD-3
    R-->>O: 1, 1, 1
    R->>E: ORD-1, ORD-2, ORD-3
    L->>R: subscribe orders.placed
    O->>R: ORD-4
    R-->>O: 2 receivers
    R->>E: ORD-4
    R->>L: ORD-4, and nothing before it
    Note over R: keys in the database: 0
```

</details>

## 4. By Name, Or By A Star

Email listens to one exact name. Analytics listens to every name starting with orders.

![By name, or by a star](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as order service
    participant R as Redis
    participant E as email, orders.placed
    participant A as analytics, orders.*
    O->>R: OrderPlaced ORD-1 on orders.placed
    R-->>O: 2 receivers
    R->>E: OrderPlaced ORD-1
    R->>A: OrderPlaced ORD-1
    O->>R: OrderCancelled ORD-1 on orders.cancelled
    R-->>O: 1 receiver
    R->>A: OrderCancelled ORD-1
```

</details>
