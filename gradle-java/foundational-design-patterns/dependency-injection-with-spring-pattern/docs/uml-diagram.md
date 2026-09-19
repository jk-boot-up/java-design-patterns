# Dependency Injection with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. The Graph Is Built

![The Graph Is Built](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as Spring
    participant CS as CheckoutService
    S->>S: new LoyaltyPolicy, RecordingGateway, RecordingNotifier
    S->>CS: new CheckoutService(policy, gateway, notifier)
```

</details>

## 2. A Missing Bean

![A Missing Bean](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App
    participant S as Spring
    App->>S: refresh, no Notifier bean
    S-->>App: UnsatisfiedDependencyException, constructor parameter 2
```

</details>

## 3. A Circular Dependency

![A Circular Dependency](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as Spring
    S->>S: build chicken, needs egg
    S->>S: build egg, needs chicken
    S-->>S: BeanCurrentlyInCreationException
```

</details>

## 4. Field Injection

![Field Injection](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as test
    participant F as FieldInjectedCheckout
    participant S as Spring
    T->>F: new, place(10000)
    F-->>T: NullPointerException
    S->>F: fills the private fields
```

</details>

