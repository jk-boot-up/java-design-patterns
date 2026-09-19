# Monitor Object Pattern — Class Diagram

Three naive classes share one shape, `sellOne()` and `available()`, and
differ only in where the protection lives. `StockMonitor` is the only one
whose lock is private.

![Monitor Object pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class PlainStock {
        <<naive>>
        -int count
        +sellOne()
        +available() int
    }
    class VolatileStock {
        <<naive>>
        -volatile int count
        +sellOne()
        +available() int
    }
    class CallerLockedStock {
        <<naive>>
        -ReentrantLock lock
        +lock() ReentrantLock
        +sellOne()
    }
    class StockMonitor {
        <<pattern>>
        -ReentrantLock lock
        -Condition stockAdded
        +sellOne()
        +take(wanted)
        +add(amount)
        +available() int
    }
    class IfInsteadOfWhile {
        <<pattern, static>>
        +twoTakersOneItem(stock) int
    }
    class MonitorHazards {
        <<pattern, static>>
        +nestedMonitors() NestedOutcome
        +calloutWhileHoldingLock(ms) CalloutOutcome
    }
    MonitorHazards ..> StockMonitor : two hazards of a correct monitor
    IfInsteadOfWhile ..> StockMonitor : the wait mistake, on a copy
```

</details>

## Reading The Diagram

`CallerLockedStock` exposes its lock through a public method. That one
method is the whole difference from `StockMonitor`, whose lock is private.
