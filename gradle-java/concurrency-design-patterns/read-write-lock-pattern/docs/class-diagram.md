# Read–Write Lock Pattern — Class Diagram

The single most important thing on this diagram: three catalogue classes
share the exact same shape — a `read()` and a `write(Price)` — and differ
only in what stands between a caller and the `Price` field itself. The
diagram cannot show which one is fastest; that is the whole reason this
project measures it in code instead of arguing it in prose.

![Read–Write Lock pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Price {
        <<record, domain>>
        +BigDecimal amount
        +String currency
    }

    class UnsynchronizedCatalogue {
        <<naive>>
        -BigDecimal amount
        -String currency
        +read() Price
        +write(price)
    }
    class SingleLockCatalogue {
        <<naive>>
        -ReentrantLock lock
        +read() Price
        +write(price)
    }

    class ReadWriteCatalogue {
        <<pattern>>
        -ReentrantReadWriteLock lock
        +read() Price
        +write(price)
    }
    class SnapshotCatalogue {
        <<pattern>>
        -AtomicReference~Price~ price
        +read() Price
        +write(price)
    }
    class WriterBarging {
        <<pattern, static>>
        +demonstrate(lock) Outcome
    }
    class UpgradeDeadlock {
        <<pattern, static>>
        +attemptUpgrade(lock, timeoutMillis) Outcome
    }

    UnsynchronizedCatalogue ..> Price : two separate field writes, not one
    SingleLockCatalogue ..> Price : one field, guarded by one lock
    ReadWriteCatalogue ..> Price : one field, guarded by two roles of one lock
    SnapshotCatalogue ..> Price : one atomic reference, no lock at all

    WriterBarging ..> ReadWriteCatalogue : demonstrates a cost of the pattern class's own lock
    UpgradeDeadlock ..> ReadWriteCatalogue : demonstrates a second cost of the same lock
```

</details>

## Reading The Diagram

**`UnsynchronizedCatalogue` is the only class with two separate fields
instead of one `Price`.** That is not an implementation detail — it is
the entire reason a torn read is even possible. Every other class holds
exactly one `Price` reference, guarded in a different way, and a `Price`
that has been fully constructed is never itself torn.

**`WriterBarging` and `UpgradeDeadlock` point at `ReadWriteCatalogue`,
not at the other two.** Both costs are specific to holding separate read
and write roles on one lock; a plain mutex has no read role to barge into
and nothing to upgrade from.
