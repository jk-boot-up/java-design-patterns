# Blue-Green and Canary with Kubernetes Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Canary By Replicas

![A Canary By Replicas](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant D as demo
    participant K as cluster
    D->>K: scale v1 to 9, v2 to 1
    D->>K: selector: app only
    D->>K: 300 requests
    K-->>D: about one in ten to v2
```

</details>

