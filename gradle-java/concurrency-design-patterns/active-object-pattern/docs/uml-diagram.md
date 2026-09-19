# Active Object Pattern — UML Sequence Diagrams

Four sequences: a monitor blocking, the call that returns first, an error
from the worker, and the mailbox backing up.

## 1. A Monitor Blocks The Caller

![A monitor blocks the caller](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant I as import thread
    participant L as MonitorInventory
    participant C as checkout thread
    I->>L: importCorrection, takes the lock
    C->>L: reserve(1)
    Note over C,L: checkout WAITING on the lock
    I->>L: slow work ends, lock released
    C->>L: reserve proceeds
```

</details>

## 2. The Call That Returns First

![The call that returns first](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout thread
    participant A as InventoryActiveObject
    participant W as worker
    C->>A: reserve(1)
    A-->>C: future, not done
    A->>W: message in the mailbox
    W-->>C: future completes, stock 49
```

</details>

## 3. An Error From The Worker

![An error from the worker](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant A as InventoryActiveObject
    participant W as worker
    C->>A: failWith("feed down")
    A-->>C: future
    A->>W: message
    W->>W: throws, stack is the worker's
    W-->>C: future fails, later
```

</details>

## 4. The Mailbox Backs Up

![The mailbox backs up](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as callers
    participant M as mailbox
    participant W as worker
    Note over W: parked on a slow message
    C->>M: 10000 messages
    Note over M: 10000 waiting, none refused
    W->>M: gate opens, works through them one by one
```

</details>
