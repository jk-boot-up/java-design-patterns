# Event Bus with NATS Pattern — Data Flow Diagram

What happens to one published event.

![Event Bus with NATS Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    Pub(["checkout publishes OrderPlaced under store.orders.placed"])
    Ret["the call returns at once, with no result"]
    Srv["the server looks at who is listening right now"]
    Any{"anybody listening for that name?"}
    Send["send a copy to each of them"]
    Drop["drop it: no error, no record, no log"]
    React["each listener reacts on its own"]
    Gone["gone for good"]
    Pub --> Ret
    Pub --> Srv --> Any
    Any -- yes --> Send --> React
    Any -- no --> Drop --> Gone
```

</details>

Said out loud: checkout publishes the event, and its own call returns immediately with no result of any kind. Meanwhile the server looks at who is listening for that name at that instant. If somebody is, each of them gets a copy and reacts on its own. If nobody is, the server drops it. There is no error, no record and no log, so it is gone for good. Checkout's call returned successfully either way, which is the whole trap.
