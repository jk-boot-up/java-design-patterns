# DTO Pattern — UML Sequence Diagrams

Four sequences.

## 1. The Domain Object Is Serialised

![The Domain Object Is Serialised](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant E as endpoint
    participant J as MiniJson
    participant C as Customer
    E->>J: write(customer)
    J->>C: every field, including passwordHash
    J->>C: orders, which loads the history
    J-->>E: 5297 characters
```

</details>

## 2. A Private Field Is Renamed

![A Private Field Is Renamed](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Dev
    participant C as Customer
    participant Cl as client
    Dev->>C: rename name to fullName
    Cl->>Cl: read the key name
    Note over Cl: null, nothing failed to compile
```

</details>

## 3. The Mapper Builds A DTO

![The Mapper Builds A DTO](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant M as CustomerMapper
    participant C as Customer
    participant D as CustomerDto
    M->>C: id, name, city
    M->>D: new CustomerDto
    Note over D: 46 characters of JSON
```

</details>

## 4. A Detail DTO Loads The History

![A Detail DTO Loads The History](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant M as CustomerMapper
    participant C as Customer
    participant O as LazyOrders
    M->>C: orders().size()
    C->>O: load 25 orders
    M-->>M: CustomerDetailDto with orderCount 25
```

</details>

