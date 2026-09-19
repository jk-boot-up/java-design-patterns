# Dependency Injection Pattern — UML Sequence Diagrams

Four sequences.

## 1. Wired By Hand

![Wired By Hand](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant M as Wiring.build
    participant CS as CheckoutService
    participant S as Storefront
    M->>M: new policy, gateway, notifier
    M->>CS: new CheckoutService(policy, gateway, notifier)
    M->>S: new Storefront(checkout, printer, auditor)
```

</details>

## 2. Field Injection

![Field Injection](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as test
    participant F as FieldInjectedCheckout
    participant I as Injector, by reflection
    T->>F: new FieldInjectedCheckout()
    T->>F: place(10000)
    F-->>T: NullPointerException
    T->>I: injectFields(...)
    I->>F: set private fields
```

</details>

## 3. A Container Starts

![A Container Starts](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App
    participant C as MiniContainer
    App->>C: start(beans)
    C->>C: read each constructor, build what it needs
    C-->>App: the graph, built
```

</details>

## 4. A Start-Up Failure

![A Start-Up Failure](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App
    participant C as MiniContainer
    App->>C: start(no Notifier bean)
    C-->>App: ContainerFailure: no bean for Notifier
    Note over App,C: at start-up, before the first order
```

</details>

