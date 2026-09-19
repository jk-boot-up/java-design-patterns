# Repository Pattern — UML Sequence Diagrams

Four sequences.

## 1. Three Services, Three Queries

![Three Services, Three Queries](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant M as marketing
    participant Su as support
    participant DB as database
    M->>DB: city = London, day > 70
    Su->>DB: city = London, day >= 70
    Note over M,Su: off by one, nobody notices
```

</details>

## 2. The Column Is Renamed

![The Column Is Renamed](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant DB as database
    participant M as marketing
    DB->>DB: city becomes town
    M->>DB: city = London
    DB-->>M: no rows, no error
```

</details>

## 3. The Same Service, Two Stores

![The Same Service, Two Stores](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as MarketingService
    participant R1 as in-memory repository
    participant R2 as database repository
    S->>R1: findByCityAndOrderedAfter
    R1-->>S: Ada, Grace
    S->>R2: findByCityAndOrderedAfter
    R2-->>S: Ada, Grace
```

</details>

## 4. A Specification

![A Specification](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant R as repository
    C->>C: inCity(London).and(orderedAfter(70)).and(hasStatus PENDING)
    C->>R: matching(specification)
    R-->>C: Grace
```

</details>

