# Active Object with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. One Thread, No Lock

![One Thread, No Lock](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as four callers
    participant M as mailbox
    participant W as worker
    C->>M: 20000 restock messages
    M->>W: one at a time
    W->>W: stock += 1, 20000 times, alone
```

</details>

## 2. A Bounded Mailbox

![A Bounded Mailbox](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant M as mailbox of 3
    C->>M: three messages waiting
    C->>M: a fourth
    M-->>C: TaskRejectedException
```

</details>

## 3. A Read As A Message

![A Read As A Message](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant M as mailbox
    participant W as worker
    C->>M: restock(5)
    C->>C: peekStock() says 0
    C->>M: available()
    W->>W: restock, then the read
    W-->>C: 5
```

</details>

## 4. An Error From The Worker

![An Error From The Worker](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant W as worker
    C->>W: failWith("feed down")
    W-->>C: future fails, later, with the worker's stack
```

</details>

