# Lazy Load Pattern — UML Sequence Diagrams

Four sequences.

## 1. Eager: Everything Reachable

![Eager: Everything Reachable](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant L as EagerOrderLoader
    participant DB as database
    L->>DB: order 1
    L->>DB: customer, and their other orders
    L->>DB: lines, products, categories
    Note over L,DB: 37 objects, 26 operations
```

</details>

## 2. A Proxy Loads On First Use

![A Proxy Loads On First Use](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant P as CustomerProxy
    participant DB as database
    C->>P: name()
    P->>DB: select customer
    P-->>C: Customer 2
    C->>P: name()
    P-->>C: cached, no query
```

</details>

## 3. N Plus One

![N Plus One](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant L as OrderList
    participant DB as database
    L->>DB: select all orders
    L->>DB: select customer 1
    L->>DB: select customer 1
    Note over L,DB: and so on, once per order
```

</details>

## 4. The Session Has Closed

![The Session Has Closed](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Page
    participant P as CustomerProxy
    participant S as Session
    Page->>S: close()
    Page->>P: name()
    P->>S: select customer
    S-->>Page: SessionClosedException
```

</details>

