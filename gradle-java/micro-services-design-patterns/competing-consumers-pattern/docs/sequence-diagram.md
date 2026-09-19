# Competing Consumers Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A message is published. Consumer A takes it and charges the card. Before it can say it has finished, consumer A crashes. The broker never got an acknowledgement, so it gives the message back. Consumer B takes it. It charges the card again, and acknowledges. The message is gone, and the card has been charged twice.

![Competing Consumers pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Q as broker
    participant A as consumer A
    participant B as consumer B
    Q->>A: message 1, attempt 1
    A->>A: charge the card
    A--xQ: crashes, no acknowledgement
    Q->>B: message 1, attempt 2
    B->>B: charge the card again
    B->>Q: acknowledge
```

</details>

The load-bearing sentence: **a queue cannot give exactly once. The consumer has to.**
