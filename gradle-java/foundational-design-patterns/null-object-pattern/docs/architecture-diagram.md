# Null Object Pattern — Architecture Diagram

Callers see one interface, whichever discount is behind it.

![Null Object Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["checkout: eight places that price an order"] --> I["Discount"]
    I --> L["LoyaltyDiscount"]
    I --> S["StaffDiscount"]
    I --> N["NoDiscount: returns the price unchanged"]
```

</details>
