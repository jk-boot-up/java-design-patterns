# Serverless Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. An order is placed, and the platform gets an event. There is no warm instance, so it starts one, which takes five ticks. It runs the send receipt function. Ten ticks later, with nothing more to do, it throws the instance away. The next order starts another.

![Serverless pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant E as event
    participant P as platform
    participant F as function instance
    E->>P: order placed
    P->>F: start (cold, 5 ticks)
    P->>F: send receipt
    F-->>P: done
    Note over P,F: 10 quiet ticks
    P->>F: drop
```

</details>

The load-bearing sentence: **the platform starts and drops instances, and the function only handles the event.**
