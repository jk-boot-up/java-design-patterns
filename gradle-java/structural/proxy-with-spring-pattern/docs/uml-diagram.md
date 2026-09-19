# Proxy with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Refused Call

![A Refused Call](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as shopper
    participant P as proxy
    participant A as RoleAspect
    S->>P: render
    P->>A: check
    A-->>S: AccessDenied
```

</details>

## 2. A Lazy Image

![A Lazy Image](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as catalogue
    participant L as lazy stand-in
    participant I as HighResolutionImage
    C->>L: pixels (first call)
    L->>I: build it now
    I-->>C: pixels
```

</details>

