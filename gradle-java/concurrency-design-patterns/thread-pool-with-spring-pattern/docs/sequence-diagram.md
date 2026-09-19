# Thread Pool with Spring Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A caller calls the packing method. What it holds is not the service but a proxy Spring generated. The proxy does not run the method. It hands the call to the executor. If a thread is free, the call runs there. If not, it waits in the queue, and if the queue is full, the caller gets a task rejected exception. The caller gets back a completable future, and the work happens somewhere else.

![Thread Pool with Spring pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant P as Spring proxy
    participant E as executor
    participant W as pool thread
    C->>P: pack(1)
    P->>E: submit
    alt a thread is free
        E->>W: run pack(1)
    else the queue has room
        E->>E: wait in the queue
    else the queue is full
        E-->>C: TaskRejectedException
    end
```

</details>

The load-bearing sentence: **the caller holds a proxy, and the work happens somewhere else.**
