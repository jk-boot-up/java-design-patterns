# MVC with Spring MVC Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A browser sends a get for an order. The controller finds the order in the store and asks the model to build a summary. The controller puts the summary in the model map and returns the name summary. The framework finds the template with that name, fills it from the summary, and sends the page.

![MVC with Spring MVC pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant B as browser
    participant C as controller
    participant S as store
    participant M as OrderSummary
    participant V as template
    B->>C: GET /orders/ORD-000001
    C->>S: find
    C->>M: of(order)
    C->>V: view name summary, with the summary
    V-->>B: HTML page
```

</details>

The load-bearing sentence: **the controller names a view and never draws it.**
