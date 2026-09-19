# Null Object Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Null Check

![A Null Check](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant D as directory
    C->>D: find(2)
    D-->>C: null
    C->>C: if discount != null
    C-->>C: price unchanged
```

</details>

## 2. The Forgotten Check

![The Forgotten Check](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as taxBase
    participant D as directory
    T->>D: find(2)
    D-->>T: null
    T->>T: discount.apply(...)
    Note over T: NullPointerException at checkout
```

</details>

## 3. A Failure Turned Into Full Price

![A Failure Turned Into Full Price](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant F as ForgivingDirectory
    participant S as discount service
    C->>F: find(1)
    F->>S: look up
    S-->>F: down
    F-->>C: NoDiscount
    Note over C: charged 10000, not 9000, silently
```

</details>

## 4. Optional Keeps Them Apart

![Optional Keeps Them Apart](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant O as OptionalDirectory
    C->>O: find(2)
    O-->>C: Optional.empty, absence is normal
    C->>O: find(1), service down
    O-->>C: exception, a failure is not absence
```

</details>

