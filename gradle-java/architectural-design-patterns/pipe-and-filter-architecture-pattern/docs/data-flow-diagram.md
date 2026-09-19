# Pipe and Filter Architecture Pattern — Data Flow Diagram

What a stage does on each tick.

![Pipe and Filter Architecture Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    Tick(["tick"])
    Work["each worker counts down its order"]
    Fin{"finished?"}
    Next{"room in the next line?"}
    Pass["pass it on"]
    Hold["hold it, and wait"]
    Take["an idle worker takes the next waiting order"]
    Tick --> Work --> Fin
    Fin -- yes --> Next
    Next -- yes --> Pass --> Take
    Next -- no --> Hold
    Fin -- no --> Take
```

</details>
