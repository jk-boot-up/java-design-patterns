# Publisher-Subscriber with Redis Pattern — Data Flow Diagram

What Redis does with one published order, from the moment the order service publishes it to the moment every copy is gone.

![Publisher-Subscriber with Redis Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    In(["order service publishes ORD-1 to orders.placed"])
    Any{"is anyone listening on that name, or a matching pattern?"}
    Zero(["answer 0. the order is gone. nothing is stored"])
    Copy["put a copy on each listener's pile"]
    Count(["answer the publisher: how many piles"])
    Room{"is this listener's pile past the limit?"}
    Cut(["close that connection. its pile is thrown away. cut-off counter plus 1"])
    Send["send down the connection as fast as the listener reads"]
    Done(["listener handles ORD-1"])
    In --> Any
    Any -- no --> Zero
    Any -- yes --> Copy --> Count
    Copy --> Room
    Room -- yes --> Cut
    Room -- no --> Send --> Done
```

</details>
