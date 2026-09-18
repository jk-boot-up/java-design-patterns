# Hexagonal Architecture Pattern — UML Sequence Diagrams

Four sequences: the core driven by HTTP, the same core driven by a CLI
instead, the driven-side storage swap, and the naive shortcut.

## 1. The Core, Driven By A Simulated HTTP Request

![Hexagonal Architecture pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Web as HttpCheckoutAdapter «driving»
    participant Core as PlaceOrderService «core»
    participant Catalog as ProductCatalog «port»
    participant Pay as PaymentGateway «port»
    participant Store as OrderStore «port»

    Web->>Core: place(request, "ada@example.com")
    Core->>Catalog: find + stockOf, each SKU
    Catalog-->>Core: prices and stock
    Core->>Pay: charge(cust-8801, £382.50)
    Pay-->>Core: charged
    Core->>Store: save(order)
    Core-->>Web: placed, ord-1001, £382.50
    Web-->>Web: {"status":201,"orderId":"ord-1001",...}
```

</details>

Every arrow out of `Core` lands on a port, never on `Web`. The adapter
called in; the core never calls back out to it.

## 2. The Same Core, Driven By A Simulated Command Line Instead

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Cli as CliCheckoutAdapter «driving — the forced change»
    participant Core as PlaceOrderService «core, byte-for-byte unchanged»

    Cli->>Cli: parse "checkout cust-8801 ada@example.com ESP-001:1,..."
    Cli->>Core: place(request, "ada@example.com")
    Core-->>Cli: placed, ord-1001, £382.50
    Cli-->>Cli: "OK  ord-1001  £382.50"
```

</details>

Compare this with sequence 1. `PlaceOrderService` is called with the same
method, the same argument types, from a caller that shares no code with the
first one at all.

## 3. The Driven Side Swapped — Storage Changes, The Core Does Not

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Root as PlaceAnOrderDemo «composition root»
    participant Core as PlaceOrderService
    participant Old as InMemoryOrderStore
    participant New as AppendOnlyOrderStore

    Note over Root: the forced change — new AppendOnlyOrderStore()<br/>instead of new InMemoryOrderStore()
    Root->>Core: wire OrderStore = new AppendOnlyOrderStore()
    Note over Old: never constructed — 0 references from here on
    Core->>New: save(order)
    Note over Core: PlaceOrderService.java: zero lines changed
```

</details>

## 4. The Shortcut — The Core's Own Use Case Names An Adapter

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Demo as PlaceAnOrderDemo
    participant Naive as NaivePlaceOrderService «naive.core»
    participant Store as InMemoryOrderStore «adapter»

    Demo->>Naive: new NaivePlaceOrderService(catalog, new InMemoryOrderStore(), payments)
    Note over Naive,Store: the constructor names the adapter type directly —<br/>this is the line ArchitectureTest is scoped to allow past,<br/>and ArchitectureRuleCatchesTheShortcutTest widens to catch
    Naive->>Store: save(order)
```

</details>

Swap `InMemoryOrderStore` for `AppendOnlyOrderStore` here, and this class
fails to compile — not because its logic is wrong, but because its
constructor named a type instead of an interface.
