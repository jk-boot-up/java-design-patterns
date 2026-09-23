# Message Channel with RabbitMQ Pattern — Data Flow Diagram

What the broker does with one pick order, from the moment checkout sends it to the moment the broker is allowed to forget it.

![Message Channel with RabbitMQ Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    In(["checkout sends ORD-1"])
    Room{"is the queue full?"}
    Refuse(["refused, and the receipt says so"])
    Keep["the order waits in the queue"]
    Disk{"marked to be written down?"}
    Write["written to disk as well"]
    Mem["held in memory only"]
    Rcv{"is a receiver there?"}
    Hold["keep waiting, however long"]
    Hand["hand it to the receiver, and keep a copy"]
    Ack{"did the receiver say done?"}
    Forget(["forget it: picked once"])
    Back["put it back, marked as seen before"]
    In --> Room
    Room -- yes --> Refuse
    Room -- no --> Keep --> Disk
    Disk -- yes --> Write --> Rcv
    Disk -- no --> Mem --> Rcv
    Rcv -- no --> Hold --> Rcv
    Rcv -- yes --> Hand --> Ack
    Ack -- yes --> Forget
    Ack -- "no, it crashed" --> Back --> Rcv
```

</details>
