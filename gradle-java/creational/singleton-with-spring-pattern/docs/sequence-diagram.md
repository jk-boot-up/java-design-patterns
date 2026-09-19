# Singleton with Spring Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Two containers are started in the same program. The checkout in container A asks its generator for a number and gets order one. The checkout in container B asks its own generator, a different object, and also gets order one. Two customers hold the same order number.

![Singleton with Spring pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as checkout in A
    participant GA as generator A
    participant B as checkout in B
    participant GB as generator B
    A->>GA: nextOrderNumber
    GA-->>A: ORD-000001
    B->>GB: nextOrderNumber
    GB-->>B: ORD-000001
```

</details>

The load-bearing sentence: **the guarantee stops at the edge of the container.**
