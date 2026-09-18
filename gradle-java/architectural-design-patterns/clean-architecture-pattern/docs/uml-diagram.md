# Clean Architecture Pattern — UML Sequence Diagrams

Four sequences: the real graph running, the dependency-inversion moment
isolated, the forced change, and the naive shortcut.

## 1. The Real Graph, Wired By Hand

![Clean Architecture pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Web as CheckoutController «adapters»
    participant UC as PlaceOrderInteractor «usecases»
    participant Prod as ProductRepository «interface»
    participant Pay as PaymentGateway «interface»
    participant Ord as OrderRepository «interface»

    Web->>UC: execute(input)
    UC->>Prod: find + stockOf, each line
    Prod-->>UC: prices and stock
    UC->>Pay: charge(cust-8801, £382.50)
    Pay-->>UC: charged
    UC->>Ord: save(order)
    UC-->>Web: placed, ord-1001, £382.50
```

</details>

## 2. The Dependency-Inversion Moment, Isolated

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant UC as PlaceOrderInteractor «usecases»
    participant Iface as OrderRepository «interface, owned by usecases»
    participant Real as InMemoryOrderRepository «adapters.gateway»

    Note over UC,Iface: source code dependency: UC needs<br/>OrderRepository to exist to compile
    UC->>Iface: save(order)
    Note over Iface,Real: at runtime, resolved to the real class
    Iface->>Real: (the actual implementation)
    Note over UC,Real: CONTROL flowed outward, to Real.<br/>The DEPENDENCY pointed inward, at Iface.<br/>Two different directions, on purpose.
```

</details>

## 3. The Forced Change — Both New, Nothing Old Touched

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Root as PlaceAnOrderDemo «composition root»
    participant Batch as BatchOrderController «new»
    participant UC2 as PlaceOrderInteractor «second instance»
    participant File as FileBackedOrderRepository «new»

    Note over Root: two new files, wired in main() —<br/>PlaceOrderInteractor.java itself: unchanged
    Root->>Batch: new BatchOrderController(new interactor)
    Root->>UC2: new PlaceOrderInteractor(..., fileStore, ...)
    Batch->>UC2: importBatch(csvRows)
    UC2->>File: save(order)
    Note over File: "a flat file, one CSV-shaped line per order"
```

</details>

## 4. The Shortcut — A Use Case That Names Its Gateways

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Demo as PlaceAnOrderDemo
    participant Naive as NaivePlaceOrderInteractor «naive.usecases»
    participant Gw as InMemoryOrderRepository «adapters — two circles out»

    Demo->>Naive: new NaivePlaceOrderInteractor(products, new InMemoryOrderRepository(), payments)
    Note over Naive,Gw: the constructor names the gateway type directly —<br/>ArchitectureRuleCatchesTheShortcutTest widens the rule to catch this
    Naive->>Gw: save(order)
```

</details>
