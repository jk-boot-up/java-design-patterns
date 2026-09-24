# Leader Election with Kubernetes Pattern — Class Diagram

The pattern lives in `Candidate`, which hands the election to Fabric8's `LeaderElector` on a `LeaseLock`. `Inbox` holds the fencing check. Everything else runs the cluster and the copies.

![Leader Election with Kubernetes Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class KubernetesLeaderElectionDemo {
        +LEASE nightly-sales-report
        +main(args)
    }
    class Cluster {
        +NAME patterns-leader-election
        +NODE_IMAGE kindest/node v1.37.0
        +NO_RUNTIME_ADVICE
        +create()
        +client() KubernetesClient
        +close()
    }
    class Candidate {
        +LEASE 5 seconds
        +RENEW_DEADLINE 4 seconds
        +RETRY 1 second
        -leading boolean
        -token int
        +main(name, kubeconfig, lease, mode)
        -report(slowly)
    }
    class ServiceCopy {
        +start(name, kubeconfig, lease, elect, inbox)
        +tell(order)
        +freeze()
        +wake()
        +stopCleanly()
        +kill()
    }
    class LeaseView {
        <<record>>
        +holder
        +transitions
        +renewTime
        +read(client, name)
    }
    class Inbox {
        +receive(sender, token)
        +senders() List
        +refusals() List
    }
    class LeaderElector {
        <<Fabric8>>
        +start() CompletableFuture
    }
    class LeaseLock {
        <<Fabric8>>
    }
    KubernetesLeaderElectionDemo --> Cluster
    KubernetesLeaderElectionDemo --> ServiceCopy : starts three
    KubernetesLeaderElectionDemo --> LeaseView : reads the lease
    ServiceCopy ..> Candidate : a separate process running
    ServiceCopy --> Inbox : delivers each report
    Candidate --> LeaderElector
    LeaderElector --> LeaseLock
```

</details>
