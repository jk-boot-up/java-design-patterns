# Domain Event Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Recorded Event

![A Recorded Event](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant O as Order
    C->>O: place()
    O->>O: status PLACED, record OrderPlaced
    C->>O: pullEvents()
    O-->>C: [OrderPlaced]
```

</details>

## 2. A Retried Handler

![A Retried Handler](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant R as relay
    participant E as email
    R->>E: OrderPlaced (mail server down)
    E-->>R: fails, stays pending
    R->>E: OrderPlaced (server back)
    E-->>R: sent, delivered
```

</details>

## 3. A Stop Between Save And Relay

![A Stop Between Save And Relay](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant R as repository
    participant X as the process
    R->>R: save order and event
    X--xX: stops
    X->>R: restarts, relay()
    R-->>X: delivers the kept event
```

</details>

