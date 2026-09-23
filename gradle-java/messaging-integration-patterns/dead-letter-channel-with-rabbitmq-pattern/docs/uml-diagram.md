# Dead Letter Channel with RabbitMQ Pattern — UML Sequence Diagrams

Four sequences. The first is the one the README shows, because it is the one that is new: a death nobody chose.

## 1. An Order That Runs Out Of Time

Nobody refuses this order. Nobody even reads it. The queue was declared with a time limit, and when the limit passes the broker parks the order itself, with the reason expired.

![An Order That Runs Out Of Time](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as the shop
    participant B as RabbitMQ broker
    participant P as parked queue
    S->>B: publish ORD-1005 to a queue with a 500 millisecond limit
    B->>B: nobody reads it, and the limit passes
    B->>B: attach the note: reason expired, queue orders.slow
    B->>P: ORD-1005, with the note
```

</details>

## 2. A Queue That Is Full

The queue was declared to hold two orders. A third arrives. To make room the broker pushes the oldest out, and parks it with the reason maxlen.

![A Queue That Is Full](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as the shop
    participant B as RabbitMQ broker
    participant P as parked queue
    S->>B: publish ORD-1006, then ORD-1007
    S->>B: publish ORD-1008, and the queue holds only two
    B->>B: push the oldest out to make room
    B->>B: attach the note: reason maxlen
    B->>P: ORD-1006, with the note
```

</details>

## 3. Asking For It Back, For Ever

The mistake the pattern exists to prevent. The worker refuses the order and asks for it back every time, so the broker keeps returning it to the head of the queue, and nothing behind it moves.

![Asking For It Back, For Ever](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant W as worker
    participant B as RabbitMQ broker
    loop eleven times
        B-->>W: ORD-1002
        W->>W: cannot read the address
        W->>B: refuse it, and give it back to me
        B->>B: return it to the head of the queue
    end
    Note over W,B: ORD-1003 and ORD-1004 are still waiting behind it
```

</details>

## 4. A Replay

An operator fixes the cause and publishes the parked order back onto the working queue. It goes to the back of the line, and the broker's note does not travel with it.

![A Replay](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as operator
    participant P as parked queue
    participant B as RabbitMQ broker
    participant W as worker
    O->>O: fix the address parser
    O->>P: take ORD-1002 off the parked queue
    O->>B: publish it again, as a new message
    B-->>W: ORD-1002, after ORD-1003 and ORD-1004
    W->>B: finished
```

</details>
