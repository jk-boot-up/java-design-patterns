# Aggregate Pattern — UML Sequence Diagrams

Four sequences.

## 1. Adding A Line

![Adding A Line](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant O as Order
    C->>O: addLine("MUG-BLUE", 8.00, 6)
    O->>O: checks quantity, credit limit, placed
    O-->>C: done
```

</details>

## 2. Two Clerks

![Two Clerks](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as clerk A
    participant B as clerk B
    participant S as store
    A->>S: load (version 1)
    B->>S: load (version 1)
    A->>S: save (version 1): accepted, now 2
    B->>S: save (version 1): refused
```

</details>

## 3. By Id

![By Id](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as Order
    participant C as Customer aggregate
    O->>O: holds CustomerId only
    Note over C: loaded only when someone asks for the customer
```

</details>

## 4. Too Big

![Too Big](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as clerk A
    participant B as clerk B
    participant S as store, one aggregate per customer
    A->>S: change order 1, save
    B->>S: change order 2, save
    S-->>B: refused: the customer changed
```

</details>

