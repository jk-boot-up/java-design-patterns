# Service Locator Pattern — UML Sequence Diagrams

Four sequences.

## 1. Lifetimes

![Lifetimes](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant L as ServiceLocator
    C->>L: find(PaymentGateway) x 3
    L-->>C: the same instance, made once
    C->>L: find(Notifier) x 3
    L-->>C: a new instance each time
```

</details>

## 2. Swapped For A Test

![Swapped For A Test](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as test
    participant L as ServiceLocator
    participant C as LocatorCheckout
    T->>L: configure a fake gateway
    T->>C: place(10000)
    C->>L: find(PaymentGateway)
    L-->>C: the fake
```

</details>

## 3. A Missing Registration

![A Missing Registration](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as LocatorCheckout
    participant L as ServiceLocator
    C->>L: find(Notifier)
    L-->>C: IllegalStateException
    Note over C: after the customer was charged
```

</details>

## 4. ServiceLoader

![ServiceLoader](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as application
    participant S as ServiceLoader
    participant F as META-INF/services
    A->>S: load(PaymentMethod)
    S->>F: read the listed providers
    S-->>A: card, bank transfer
```

</details>

