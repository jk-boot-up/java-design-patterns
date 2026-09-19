# Retry with Resilience4j Pattern — Data Flow Diagram

What the retry decides after a failure.

![Retry with Resilience4j Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    Fail(["the call failed"])
    Kind{"is it on the retry list?"}
    Left{"attempts left?"}
    Wait["wait, doubling each time"]
    Again(["call again"])
    Stop(["rethrow to the caller"])
    Fail --> Kind
    Kind -- no --> Stop
    Kind -- yes --> Left
    Left -- no --> Stop
    Left -- yes --> Wait --> Again
```

</details>
