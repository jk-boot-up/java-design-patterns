# Leader Election with Kubernetes Pattern — Architecture Diagram

Three copies, each its own process, and one record they all read and write. The record lives in the API server, inside a one-node cluster in the container runtime. The fencing check lives in the inbox, outside Kubernetes altogether.

![Leader Election with Kubernetes Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    subgraph Copies["three copies of the reporting service, three Java processes"]
        A["copy A, elector"]
        B["copy B, elector"]
        C["copy C, elector"]
    end
    subgraph Kind["kind cluster patterns-leader-election, one node, Kubernetes 1.37.0"]
        API["API server"]
        L[("Lease nightly-sales-report: holder, 5 seconds, renew time, holder changes")]
        API --- L
    end
    subgraph Demo["demo process"]
        O["observer: reads the lease"]
        I["manager's inbox: checks the token"]
    end
    A -- "renew every 1 second" --> API
    B -- "is it still fresh?" --> API
    C -- "is it still fresh?" --> API
    O -- "read only" --> API
    A -- "report, with token" --> I
    B -. "report, with token" .-> I
```

</details>
