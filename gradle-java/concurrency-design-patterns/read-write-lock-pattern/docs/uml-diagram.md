# Read–Write Lock Pattern — UML Sequence Diagrams

Four sequences: several readers held at once, a queued writer barged, the
upgrade deadlock, and the harness's own lost-update proof, copied
unchanged from §46.

## 1. Several Readers, Proven Held At The Same Moment

![Read–Write Lock pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Main as Test thread
    participant Lock as ReentrantReadWriteLock
    participant R1 as reader 1
    participant R2 as reader 2
    participant R3 as reader 3
    participant R4 as reader 4

    R1->>Lock: readLock().lock()
    R2->>Lock: readLock().lock()
    R3->>Lock: readLock().lock()
    R4->>Lock: readLock().lock()
    Note over Main: CountDownLatch confirms all four now hold the read lock
    Main->>Lock: getReadLockCount()
    Lock-->>Main: 4 -- reported by the lock itself, not inferred
```

</details>

## 2. A Queued Writer, Barged By A Fresh Reader

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Main as Test thread
    participant Lock as ReentrantReadWriteLock
    participant Writer as writer thread

    Main->>Lock: readLock().lock() -- reader A holds it
    Writer->>Lock: writeLock().lock() -- blocks, reader A still holds it
    Note over Main: spin-wait on hasQueuedThreads() -- proves the writer is genuinely queued
    Main->>Lock: readLock().tryLock()
    Lock-->>Main: true -- barges past the queued writer, by design
    Main->>Lock: readLock().unlock() (both acquisitions)
    Writer->>Lock: write lock finally granted
```

</details>

## 3. Upgrading Read To Write Deadlocks The Same Thread

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as one thread

    T->>T: readLock().lock() -- acquired
    T->>T: writeLock().tryLock(timeout) -- blocks
    Note over T: no other thread holds the read lock --<br/>only this thread's own read lock is in the way
    T->>T: tryLock() times out -- rescued, not resolved
    T->>T: readLock().unlock()
    Note over T: left alone, with no timeout, this thread waits on itself forever
```

</details>

## 4. The Harness's Own Proof — A Lost Update, Every Run

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T1 as Thread 1
    participant T2 as Thread 2
    participant R as Rendezvous «2 parties»
    participant S as shared int, starts at 10

    T1->>S: read -> 10
    T2->>S: read -> 10
    T1->>R: meet()
    T2->>R: meet()
    Note over R: both released together, only once both have arrived
    T1->>S: write 10 - 1 = 9
    T2->>S: write 10 - 1 = 9
    Note over S: final value: 9, not 8 — one decrement is lost, every run
```

</details>

This is the same mechanism §46 built and this project's `HarnessSelfTest`
proves again, copied unchanged, before act one relies on the same
determinism idea to force a torn read.
