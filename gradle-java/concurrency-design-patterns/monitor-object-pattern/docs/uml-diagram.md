# Monitor Object Pattern — UML Sequence Diagrams

Four sequences: the lost update, waiting and signalling, `if` instead of
`while`, and the nested-monitor deadlock.

## 1. The Lost Update

![The lost update](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as checkout 1
    participant S as PlainStock
    participant B as checkout 2
    A->>S: read count, sees 10
    B->>S: read count, sees 10
    Note over A,B: rendezvous holds both until both have read
    A->>S: write 9
    B->>S: write 9
    Note over S: two sales, count says 9
```

</details>

## 2. Waiting And Signalling

![Waiting and signalling](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as taker
    participant M as StockMonitor
    participant D as delivery
    T->>M: take(3)
    Note over T,M: count is 0, so await
    D->>M: add(3)
    M-->>T: signalAll
    T->>M: re-check, takes 3
```

</details>

## 3. if Instead Of while

![if instead of while](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as taker 1
    participant B as taker 2
    participant S as BrokenStock
    A->>S: take(1), waits
    B->>S: take(1), waits
    S-->>A: add(1) wakes both
    S-->>B: add(1) wakes both
    A->>S: skips the check, count 0
    B->>S: skips the check, count -1
```

</details>

## 4. Nested Monitors

![Nested monitors](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T1 as transfer a to b
    participant A as monitor a
    participant B as monitor b
    participant T2 as transfer b to a
    T1->>A: lock a
    T2->>B: lock b
    Note over T1,T2: rendezvous, both hold their first
    T1->>B: lock b, waits
    T2->>A: lock a, waits
    Note over T1,T2: deadlock, broken by interrupting both
```

</details>
