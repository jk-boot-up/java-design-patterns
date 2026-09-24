# Queue-Based Load Leveling with SQS Pattern — UML Sequence Diagrams

Four sequences. The slow packer comes first, because two parcels for one order is the one thing the hand-built version could never show.

## 1. A Slow Packer Packs An Order Twice

A queue that hides a taken order for 2 seconds. Packer A takes ORD-3001 and is slower than that. SQS hands the same order to packer B, and both pack it. Then packer A takes ORD-3002 and, in time, tells SQS it is still working; packer B's three-second long poll finds nothing.

![A slow packer packs an order twice](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as packer A
    participant Q as SQS, 2 s timeout
    participant B as packer B
    A->>Q: ReceiveMessage
    Q-->>A: ORD-3001, handed out 1 time
    Note over A: still packing when 2 seconds pass
    B->>Q: ReceiveMessage
    Q-->>B: ORD-3001, handed out 2 times
    B->>Q: DeleteMessage
    A->>Q: DeleteMessage
    Note over A,B: ORD-3001 packed 2 times, two parcels
    A->>Q: ReceiveMessage
    Q-->>A: ORD-3002
    A->>Q: ChangeMessageVisibility, 10 seconds more
    B->>Q: ReceiveMessage, wait 3 seconds
    Q-->>B: 0 orders
    A->>Q: DeleteMessage
    Note over A: ORD-3002 packed 1 time
```

</details>

## 2. Taken Is Not Removed

A packer takes ORD-2001 and stops without deleting it. SQS hides it, then hands it out again once the 2 seconds have passed.

![Taken is not removed](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as first packer
    participant Q as SQS, 2 s timeout
    participant S as second packer
    P->>Q: ReceiveMessage
    Q-->>P: ORD-2001
    Note over P: stops, never deletes
    Note over Q: 0 waiting, 1 in flight
    S->>Q: ReceiveMessage
    Q-->>S: 0 orders
    Note over Q: the 2 seconds pass
    S->>Q: ReceiveMessage
    Q-->>S: ORD-2001, handed out 2 times
    S->>Q: DeleteMessage
```

</details>

## 3. The Packer Stops Half Way Through A Round

The packer holds 10 orders, finishes 3, and its process stops. Nothing is lost.

![The packer stops half way through a round](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as packer
    participant Q as SQS, 2 s timeout
    participant N as new packer
    P->>Q: ReceiveMessage, 10
    Q-->>P: 10 orders
    P->>Q: DeleteMessageBatch, the 3 it finished
    Note over P: the process stops
    Note over Q: 90 waiting, 7 in flight
    Note over Q: the timeout runs out, 97 waiting
    loop until the queue is empty
        N->>Q: ReceiveMessage, 10
        Q-->>N: orders, 7 of them handed out a second time
        N->>Q: DeleteMessageBatch
    end
    Note over N: packed 100, lost 0
```

</details>

## 4. No Limit To Set

Checkout asks for a queue that holds at most 50 orders, and SQS does not know the setting. Fed at 15 a round and drained at 10, the queue grows and nothing refuses it.

![No limit to set](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant Q as SQS
    participant P as packer
    C->>Q: CreateQueue with MaximumDepth 50
    Q-->>C: refused, Unknown Attribute MaximumDepth
    C->>Q: CreateQueue with no limit
    loop 20 rounds
        C->>Q: send 15 orders
        P->>Q: take 10, delete 10
    end
    Note over Q: 100 waiting, refused none, and growing
```

</details>
