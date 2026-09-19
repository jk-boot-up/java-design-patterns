# Gateway Pattern — Architecture Diagram

The shop never sees the provider.

![Gateway Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    S["Checkout, renewals, gift cards"] --> G["PaymentGateway"]
    G --> A["AcmeGateway"]
    G --> B["BetaGateway"]
    G --> F["FakeGateway, for tests"]
    A --> C["Acme's client and network"]
```

</details>
