# Lazy Load with Hibernate Pattern — UML Sequence Diagrams

Four sequences.

## 1. The Exception

![The Exception](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Page
    participant S as Session
    participant P as proxy
    Page->>S: find orders, close
    Page->>P: name()
    P-->>Page: LazyInitializationException
```

</details>

## 2. Fix One: Keep The Session Open

![Fix One: Keep The Session Open](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant View
    participant S as Session
    participant DB as H2
    View->>S: orders
    S->>DB: select orders
    loop each order rendered
        View->>S: lines
        S->>DB: select lines
    end
```

</details>

## 3. Fix Two: Join Fetch

![Fix Two: Join Fetch](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Page
    participant DB as H2
    Page->>DB: select orders join fetch lines
    DB-->>Page: 80 rows
    Note over Page: Hibernate folds them into 20 orders
```

</details>

## 4. Fix Three: A Projection

![Fix Three: A Projection](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Page
    participant DB as H2
    Page->>DB: select id, customer name
    DB-->>Page: 20 rows, no entities
```

</details>

