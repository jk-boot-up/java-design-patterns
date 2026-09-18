# Hexagonal Architecture Pattern — Architecture Diagram

Read it as one box in the middle — the core — surrounded by adapters on
every side. Every arrow crossing the boundary of the core box points
**inward**. The core has no arrow leaving it for anything outside itself.

![Hexagonal Architecture pattern architecture diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    Root["PlaceAnOrderDemo<br/>composition root"]

    subgraph Core["core — domain + port + the use case"]
        direction TB
        Service["PlaceOrderService"]
        Ports["OrderStore · PaymentGateway ·<br/>ProductCatalog · Notifier «ports»"]
        Domain["domain — Order, Money, Product<br/>knows nothing outside itself"]
    end

    subgraph Driven["driven adapters — called by the core"]
        direction TB
        Persist["InMemoryOrderStore /<br/>AppendOnlyOrderStore"]
        Pay["InMemoryPaymentGateway"]
        Notify["InMemoryNotifier"]
        Cat["InMemoryProductCatalog"]
    end

    subgraph Driving["driving adapters — call into the core"]
        direction TB
        Http["HttpCheckoutAdapter"]
        Cli["CliCheckoutAdapter"]
    end

    subgraph N["naive.core — outside the real architecture"]
        Naive["NaivePlaceOrderService"]
    end

    Root -.->|wires everything| Core
    Root -.-> Driven
    Root -.-> Driving

    Service --> Ports
    Persist -->|implements| Ports
    Pay -->|implements| Ports
    Notify -->|implements| Ports
    Cat -->|implements| Ports

    Http -->|calls in| Service
    Cli -->|calls in| Service

    Naive -->|names the adapter directly —<br/>the rule this project enforces| Persist
```

</details>

## Reading The Diagram

**Every arrow crossing into the `core` box points inward.** Driven adapters
implement a port; driving adapters call the use case. Neither crossing
originates inside `core` and lands outside it.

**`domain` sits inside `core` with no arrow leaving the box at all.** An
order and a price are true whether or not any adapter, of either kind,
exists.

**The dashed box is not part of the architecture.** `NaivePlaceOrderService`'s
one outward arrow — straight to a concrete adapter — is the line
`ArchitectureRuleCatchesTheShortcutTest` widens the dependency rule to
catch.
