# Dependency Injection with Spring Pattern — Architecture Diagram

Spring is the composition root. Everything else is given what it needs.

![Dependency Injection with Spring Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    subgraph Spring["Spring ApplicationContext: reads constructors, builds beans"]
        P["LoyaltyPolicy"]
        G["RecordingGateway"]
        N["RecordingNotifier"]
    end
    Spring -->|constructor arguments| CS["CheckoutService"]
    Spring -->|constructor arguments| RP["ReceiptPrinter"]
    Spring -->|constructor arguments| AU["Auditor"]
    CS --> SF["Storefront"]
    RP --> SF
    AU --> SF
```

</details>
