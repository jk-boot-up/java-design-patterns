# Repository with Spring Data Pattern — UML Sequence Diagrams

Four sequences.

## 1. No Implementation

![No Implementation](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Spring
    participant I as CustomerRepository
    Spring->>I: scan the interface at start-up
    Spring->>Spring: generate a proxy, parse each method name
    Spring-->>I: inject the proxy
```

</details>

## 2. A Query From A Name

![A Query From A Name](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant P as proxy
    participant DB as H2
    C->>P: findDistinctByCityAndOrdersDayGreaterThan(London, 70)
    P->>DB: one SELECT, with a join
    P-->>C: Ada, Grace
```

</details>

## 3. N Plus One, And A Graph

![N Plus One, And A Graph](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant P as proxy
    participant DB as H2
    C->>P: findAll()
    P->>DB: select customers
    loop each of 6 customers
        C->>DB: select that customer's orders
    end
    Note over C,DB: 7 statements, or 1 with an entity graph
```

</details>

## 4. The Leak

![The Leak](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant EM as persistence context
    participant DB as H2
    C->>EM: findAll(), Ada is managed
    C->>EM: ada.moveTo(Manchester)
    alt inside a transaction
        EM->>DB: UPDATE at commit
    else no transaction
        Note over EM,DB: nothing written, no error
    end
```

</details>

