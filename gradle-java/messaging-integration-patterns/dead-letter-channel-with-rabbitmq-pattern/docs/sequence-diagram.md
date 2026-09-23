# Dead Letter Channel with RabbitMQ Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The shop publishes four orders onto a queue, and that queue was declared with a rule on it: if an order dies here, send it to the parked exchange. The worker asks the broker for the next order and gets the second one, whose address nothing can read. Shipping fails. The worker refuses the order and asks for it back, and the broker puts it at the head of the line. That happens twice more. On the third failure the worker refuses it for good and does not ask for it back. Now the worker does nothing else — it is the broker that acts. The broker takes the order out of the queue, attaches a note saying the queue it died in, the number of deaths, and the reason, which is the word rejected, and hands it to the parked exchange, which puts it on the parked queue. The worker asks for the next order and gets the third one, which ships.

![Dead Letter Channel with RabbitMQ pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant W as worker
    participant B as RabbitMQ broker
    participant S as shipping
    participant P as parked queue
    W->>B: give me the next order
    B-->>W: ORD-1002
    W->>S: ship it
    S-->>W: cannot read the address
    W->>B: refuse it, and give it back to me
    B->>B: back to the head of the queue
    W->>B: give me the next order
    B-->>W: ORD-1002, for the third time
    W->>S: ship it
    S-->>W: cannot read the address
    W->>B: refuse it for good
    B->>B: attach the note: reason rejected, queue orders.work, count 1
    B->>P: ORD-1002, with the note
    W->>B: give me the next order
    B-->>W: ORD-1003, which ships
```

</details>

The load-bearing sentence: **the worker only refuses the order; the broker is what moves it, and the broker is what writes down why.**

The rejected designs and the other failure modes are in [`uml-diagram.md`](uml-diagram.md).
