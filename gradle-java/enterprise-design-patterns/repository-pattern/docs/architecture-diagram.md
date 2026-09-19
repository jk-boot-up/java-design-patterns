# Repository Pattern — Architecture Diagram

The caller sits above the interface; the stores sit below it.

![Repository Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    S["MarketingService"] --> R["CustomerRepository: an interface"]
    R --> M["InMemoryCustomerRepository: a list"]
    R --> D["ToyDatabaseCustomerRepository"]
    D --> DB["toy database: tables"]
```

</details>
