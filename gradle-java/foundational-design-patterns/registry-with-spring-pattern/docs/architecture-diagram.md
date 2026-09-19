# Registry with Spring Pattern — Architecture Diagram

One context, cached and shared by every test with the same configuration.

![Registry with Spring Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    T1["test A"] --> C
    T2["test B"] --> C
    subgraph C["cached ApplicationContext"]
        G["RecordingGateway: a singleton that remembers"]
        N["RecordingNotifier"]
    end
```

</details>
