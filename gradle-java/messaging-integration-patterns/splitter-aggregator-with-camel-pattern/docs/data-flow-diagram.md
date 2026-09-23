# Splitter and Aggregator with Camel Pattern — Data Flow Diagram

What happens to one shipment when it reaches the aggregator, and what the clock does when no shipment reaches it at all.

![Splitter and Aggregator with Camel Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    In(["a shipment arrives"])
    Key["read the order number off it"]
    Fold["fold it into that order's half-finished answer"]
    Dup{"already have this place in the order?"}
    Note["count a duplicate, keep the first"]
    Store["file it under its place"]
    Size{"as many messages as the order expected?"}
    Emit(["send out one answer, completed by size"])
    Hold["keep holding the order"]
    Clock{"deadline passed?"}
    Partial(["send out what there is, completed by timeout"])
    In --> Key --> Fold --> Dup
    Dup -- yes --> Note --> Size
    Dup -- no --> Store --> Size
    Size -- yes --> Emit
    Size -- no --> Hold --> Clock
    Clock -- no --> Hold
    Clock -- yes --> Partial
```

</details>
