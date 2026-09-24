# Competing Consumers with RabbitMQ Pattern — UML Sequence Diagrams

Four sequences. The default of no limit comes first, because it is the one thing the plain-Java version, whose consumers took one message at a time, could never show.

## 1. No Limit: The First Picker Takes Everything

Twelve orders are waiting. A slow picker starts first with no prefetch set, which in RabbitMQ means no limit. The broker hands it all twelve at once. A fast picker joins a moment later and is handed nothing, because nothing is left waiting.

![No limit: the first picker takes everything](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Q as queue pick-orders-no-limit
    participant S as slow picker, no limit
    participant F as fast picker, no limit
    Note over Q: 12 orders waiting
    S->>Q: listening, no prefetch set
    Q->>S: ORD-1 to ORD-12, all at once
    Note over Q: waiting: 0
    F->>Q: listening
    Note over F: handed 0, stands idle
    S->>Q: done, twelve times, one by one
    Note over S,F: picked by the slow picker 12, by the fast one 0
```

</details>

## 2. Prefetch Ten, Then Prefetch One

The same slow and fast pickers, with a limit. With ten, each is handed ten and the fast one ends up idle while the slow one sits on ten. With one, the slow picker holds one and the fast one picks the other nineteen.

![Prefetch ten, then prefetch one](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Q as queue, 20 orders
    participant S as slow picker
    participant F as fast picker
    Note over Q,F: prefetch 10
    Q->>S: 10 orders
    Q->>F: 10 orders
    F->>Q: done, 10 times
    Note over Q,F: waiting 0. fast idle. slow still holds 10
    Note over Q,F: prefetch 1, a fresh 20
    Q->>S: 1 order, stuck on it
    Q->>F: 1 order at a time
    F->>Q: done, 19 times
    Note over S,F: slow holds 1. fast picked 19
```

</details>

## 3. The Same Crash, Without Saying Done

Picker A tells the broker to count every order as done on handover, which RabbitMQ calls automatic acknowledgement. It is handed five, picks two, and crashes half-way through the third. The broker had already forgotten all five, so three are lost.

![The same crash, without saying done](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Q as queue pick-orders-auto
    participant A as picker A, automatic acknowledgement
    Q->>A: ORD-1 to ORD-5
    Q-->>Q: each counted done on handover. waiting 0
    Note over A: picks ORD-1 and ORD-2
    Note over A: crashes half-way through ORD-3
    Q-->>Q: nothing to put back. waiting 0
    Note over Q,A: picked 2, lost 3
```

</details>

## 4. A Poison Order

ORD-13 crashes every picker that takes it. The broker puts it back each time, marked only as seen before, never with a count. After three pickers it is waiting again, and nothing in a classic queue will ever stop it.

![A poison order](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Q as queue pick-orders-poison
    participant A as picker A
    participant B as picker B
    participant C as picker C
    Q->>A: ORD-13, seen before: false
    Note over A: crashes
    Q->>B: ORD-13, seen before: true
    Note over B: crashes
    Q->>C: ORD-13, seen before: true
    Note over C: crashes
    Note over Q: delivered 3 times, picked 0, waiting again 1
```

</details>
