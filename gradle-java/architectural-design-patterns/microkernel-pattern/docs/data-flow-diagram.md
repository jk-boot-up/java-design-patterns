# Microkernel Pattern — Data Flow Diagram

What the core does to price an order.

![Microkernel Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    Start(["base total"])
    Next["next plugin, in order"]
    Run["plugin adjusts the total"]
    Fail["record the failure, keep the total"]
    Done(["final total"])
    Start --> Next --> Run --> Next
    Run -. throws .-> Fail --> Next
    Next -- none left --> Done
```

</details>
