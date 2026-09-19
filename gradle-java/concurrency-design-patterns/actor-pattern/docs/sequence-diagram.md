# Actor Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. An order thread asks the inventory actor to reserve three mugs. The message goes into the mailbox. The inventory actor takes it, works on its own private stock, finds enough, takes three away, and puts a reserved message in the reply. The order thread, which has been waiting on the promise of a reply, gets the reserved message. Meanwhile another thread's message sits in the mailbox, and is handled next. The stock was only ever touched by the inventory actor's thread.

![Actor pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as order thread
    participant M as mailbox
    participant I as inventory actor
    O->>M: ask(Reserve MUG-BLUE 3)
    I->>M: take
    M-->>I: Reserve MUG-BLUE 3
    I->>I: stock 5, take 3, stock 2
    I-->>O: Reserved MUG-BLUE 3
```

</details>

The load-bearing sentence: **the stock is touched only by the actor's own thread.**
