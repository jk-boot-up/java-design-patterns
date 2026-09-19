# Blue-Green and Canary with Kubernetes Pattern — Class Diagram

A cluster object drives kubectl. A traffic object sends requests.

![Blue-Green and Canary with Kubernetes Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Cluster {
        +create()
        +scale(deployment, n)
        +selectVersion(v)
        +selectBoth()
        +runningPods() int
        +delete()
    }
    class Traffic {
        +get(path) String
        +send(path, n) Outcome
    }
    class Shell {
        +run(command) String
    }
    Cluster --> Shell : kind, kubectl
    Traffic ..> Cluster : reaches its Service
```

</details>
