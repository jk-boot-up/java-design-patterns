# Prototype with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. Fresh From The Definition

![Fresh From The Definition](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as caller
    participant C as container
    K->>C: getBean(Listing)
    C-->>K: new Listing, Untitled
    K->>C: getBean(Listing)
    C-->>K: another new Listing, Untitled
```

</details>

## 2. A Copy Of An Edited Draft

![A Copy Of An Edited Draft](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as caller
    participant D as draft
    K->>D: setTitle Blue Mug
    K->>D: copy()
    D-->>K: a new Listing, Blue Mug
```

</details>

## 3. Asking Through A Provider

![Asking Through A Provider](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as Storefront
    participant P as ObjectProvider
    S->>P: getObject
    P-->>S: a new Listing
    S->>P: getObject
    P-->>S: another new Listing
```

</details>

