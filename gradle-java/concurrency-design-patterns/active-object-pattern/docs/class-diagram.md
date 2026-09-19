# Active Object Pattern — Class Diagram

`InventoryActiveObject` is the assembly: a mailbox, a worker thread, and a
`CompletableFuture` returned for every call. The state field is private to
the worker.

![Active Object pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class MonitorInventory {
        <<naive>>
        -ReentrantLock lock
        +reserve(amount) int
        +importCorrection(stock, slowWork)
    }
    class InventoryActiveObject {
        <<pattern>>
        -BlockingQueue mailbox
        -Thread worker
        -int stock
        +reserve(amount) CompletableFuture
        +restock(amount) CompletableFuture
        +importCorrection(stock, slowWork) CompletableFuture
        +pendingMessages() int
    }
    class Mailbox {
        <<pattern, static>>
        +backlogWhileWorkerIsBusy(n) int
        +throughput(callers, each, work) Throughput
    }
    Mailbox ..> InventoryActiveObject : measures its two costs
    InventoryActiveObject ..> MonitorInventory : replaces its lock with a queue
```

</details>

## Reading The Diagram

The `stock` field has no lock beside it. That absence is the pattern.
