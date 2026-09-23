# Splitter and Aggregator with Camel Pattern — Architecture Diagram

One order becomes three shipments. A closed warehouse is where a shipment stops, and nothing downstream is told.

![Splitter and Aggregator with Camel Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    O["order ORD-4471, 3 lines"] --> S["Camel split"]
    S --> L["Leeds picks: 2 x MUG-BLUE"]
    S --> R["Reading picks: 1 x ESP-001"]
    S --> G["Glasgow: closed, never answers"]
    L --> A["Camel aggregate, keyed on the order number"]
    R --> A
    G -. nothing sent .-> A
    A --> C{"completion condition"}
    C -- "size: 3 of 3" --> D["one answer, total GBP 283.42"]
    C -- "timeout: 600 ms" --> P["partial answer, missing Glasgow"]
```

</details>
