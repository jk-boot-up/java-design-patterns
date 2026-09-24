# Competing Consumers with RabbitMQ Pattern — Data Flow Diagram

What the broker does with one pick order, from the moment it is sent to the moment the broker may forget it. The two questions the plain-Java version never asked are the prefetch check and the acknowledgement mode.

![Competing Consumers with RabbitMQ Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    In(["checkout sends ORD-3"])
    Wait["ORD-3 waits in the queue"]
    Who{"is any listening picker holding fewer than its prefetch?"}
    Hold["keep waiting"]
    Hand["hand ORD-3 to that picker"]
    Mode{"does the picker say done?"}
    Gone(["forgotten at once: automatic acknowledgement"])
    Held["held by the picker, the broker keeps a copy"]
    Ack{"done, or did the picker die first?"}
    Forget(["forget it: picked"])
    Back["put it back, marked seen before, started or not"]
    Lost(["if the picker dies now, ORD-3 is lost"])
    In --> Wait --> Who
    Who -- no --> Hold --> Who
    Who -- yes --> Hand --> Mode
    Mode -- no --> Gone --> Lost
    Mode -- yes --> Held --> Ack
    Ack -- done --> Forget
    Ack -- died --> Back --> Wait
```

</details>
