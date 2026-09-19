# Read–Write Lock Pattern — Architecture Diagram

Where each piece runs, and the one shared value every approach in this
project protects a different way.

![Read–Write Lock pattern architecture diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    subgraph Readers["many reader threads — page views"]
        direction TB
        R1["reader"]
        R2["reader"]
        R3["reader"]
    end

    subgraph Writer["one writer thread — a price change"]
        direction TB
        W["writer"]
    end

    subgraph Guard["what stands between them"]
        direction TB
        RWL["ReadWriteCatalogue<br/>read lock shared, write lock exclusive"]
        SNAP["SnapshotCatalogue<br/>AtomicReference, no lock at all"]
    end

    subgraph Failure["two costs specific to the read-write lock"]
        direction TB
        Barge["WriterBarging<br/>a queued writer, barged by a new reader"]
        Upgrade["UpgradeDeadlock<br/>read-to-write, self-deadlocked"]
    end

    R1 -->|readLock| RWL
    R2 -->|readLock| RWL
    R3 -->|readLock| RWL
    W -->|writeLock, excludes everyone| RWL

    R1 -.->|get, no lock needed| SNAP
    W -.->|set, atomic swap| SNAP

    RWL -.-> Barge
    RWL -.-> Upgrade
```

</details>

## Reading The Diagram

**Three arrows converge on `RWL` from the readers, and one from the
writer — but the diagram cannot show that this is where the coordination
cost also concentrates.** That cost is exactly what act three and act
six measure in code, because a static picture would make the pattern
look strictly better than the plain mutex, which this project's own
numbers say is not always true.

**`SNAP` has no incoming arrow from `Failure` at all.** Neither writer
starvation nor the upgrade deadlock is possible against an
`AtomicReference` — there is no read role and no write role to barge
between or upgrade from, only one atomic swap.
