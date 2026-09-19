# Future/Promise Pattern — UML Sequence Diagrams

Four sequences: three lookups running at once, the Future/Promise
handoff, an exception surfacing wrapped, and the harness's own
lost-update proof, copied unchanged from §46.

## 1. Three Lookups, Submitted At Once, Read In Order

![Future/Promise pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Page as page thread
    participant Pool as worker pool
    participant P as price future
    participant S as stock future
    participant R as rating future

    Page->>Pool: submit(price lookup)
    Pool-->>Page: price future returned immediately
    Page->>Pool: submit(stock lookup)
    Pool-->>Page: stock future returned immediately
    Page->>Pool: submit(rating lookup)
    Pool-->>Page: rating future returned immediately
    Note over Pool: all three lookups now running at once
    Page->>P: get()
    P-->>Page: price, once its lookup finishes
    Page->>S: get()
    S-->>Page: stock, once its lookup finishes
    Page->>R: get()
    R-->>Page: rating, once its lookup finishes
```

</details>

## 2. Future And Promise — One Object, Two Threads

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Reader as reader thread
    participant F as CompletableFuture
    participant Writer as writer thread

    Reader->>F: new CompletableFuture()
    Reader->>Writer: start()
    Reader->>F: get() -- blocks here
    Writer->>Writer: does its own work
    Writer->>F: complete(result)
    F-->>Reader: get() returns, unblocked
```

</details>

## 3. An Exception Surfaces Later, Wrapped

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller as calling thread
    participant Pool as worker pool
    participant Task as doomed task

    Caller->>Pool: submit(doomed task)
    Pool->>Task: runs it on a worker thread
    Task->>Task: throws IllegalStateException
    Note over Task: stack trace captured here --<br/>the worker thread's call stack only
    Caller->>Pool: future.get()
    Pool-->>Caller: ExecutionException, wrapping the original cause
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
proves again, copied unchanged, before act two or act three relies on it.
