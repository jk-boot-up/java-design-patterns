# Competing Consumers Pattern — Data Flow Diagram

What happens to one message.

![Competing Consumers Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    Pub(["a message is published"])
    Take["one consumer takes it"]
    Do["the consumer handles it"]
    Ok{"did it finish?"}
    Ack(["acknowledged: gone"])
    Back(["given back to the front of the queue, attempt + 1"])
    Pub --> Take --> Do --> Ok
    Ok -- yes --> Ack
    Ok -- no --> Back
    Back --> Take
```

</details>
