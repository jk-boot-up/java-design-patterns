# Registry Pattern — UML Sequence Diagrams

Four sequences.

## 1. Passed Down

![Passed Down](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as Storefront
    participant C as CartService
    participant O as OrderCoordinator
    participant P as PricingStage
    participant Y as PaymentStage
    participant H as Charger
    S->>C: gateway
    C->>O: gateway
    O->>P: gateway
    P->>Y: gateway
    Y->>H: gateway, and only here is it used
```

</details>

## 2. Asked Of The Registry

![Asked Of The Registry](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as RegistryCheckout
    participant R as Registry
    C->>R: get(DiscountPolicy)
    C->>R: get(PaymentGateway)
    C->>R: get(Notifier)
    Note over C,R: no constructor arguments, no visible dependencies
```

</details>

## 3. An Unregistered Dependency

![An Unregistered Dependency](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as caller
    participant C as RegistryCheckout
    participant R as Registry
    T->>C: new RegistryCheckout(), compiles
    T->>C: place(10000)
    C->>R: get(DiscountPolicy)
    R-->>T: IllegalStateException, nothing registered
```

</details>

## 4. Order Dependence

![Order Dependence](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as refund test
    participant R as Registry
    participant B as checkout test
    A->>R: register(gateway with 1 charge)
    B->>R: get(PaymentGateway)
    R-->>B: the leftover
    B->>B: FAILED, saw 2 charges
```

</details>

