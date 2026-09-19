# Producer–Consumer Pattern — Data Flow Diagram

One order, from arrival to being packed — or to being rejected, or to
being lost at shutdown.

![Producer-Consumer pattern data flow diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    Arrive(["an order arrives at checkout"])
    TryPut{"is there room in the queue<br/>within the patience window?"}
    Rejected(["rejected — act three's fourth order"])
    Queued["sitting in BoundedOrderQueue"]
    Taken{"does the packer take() it,<br/>or is it interrupted first?"}
    Packed(["packed — added to packedLog"])
    Lost(["lost — still in the queue,<br/>never taken, act five"])
    Poison{"is the next item POISON?"}
    Stopped(["packer stops cleanly, act four"])

    Arrive --> TryPut
    TryPut -- no --> Rejected
    TryPut -- yes --> Queued --> Taken
    Taken -- taken, packing completes --> Packed
    Taken -- packer interrupted first --> Lost
    Packed --> Poison
    Poison -- yes --> Stopped
    Poison -- no --> Taken
```

</details>

## Reading The Diagram

**Two different arrows leave `Taken`, and they lead to opposite outcomes
from the same state.** An order sitting in the queue is either packed or
lost depending on nothing about the order itself — only on whether the
packer reaches it before something stops the packer first.

**`Rejected` is reached without the order ever touching the queue at all.**
The patience window in `offer` is checked before anything is enqueued,
which is the diagram's way of showing that a rejection is a decision made
at the door, not a later cleanup.
