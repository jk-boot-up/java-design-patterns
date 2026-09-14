# Service Discovery Pattern — Class Diagram

Shows the static structure: the registry that holds the leases, the cluster whose
instances register themselves, the discovering client that asks before every call,
and — kept deliberately outside the pattern — the hardcoded client that was told
one address and can never be told another.

![Service Discovery pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class ServiceRegistry {
        +LEASE_MILLIS = 3000
        -Map~String, Lease~ leases
        +register(ServiceInstance instance)
        +heartbeat(String instanceId)
        +deregister(String instanceId)
        +instances(String serviceName) List
        +size() int
    }

    class Lease {
        <<record>>
        +ServiceInstance instance
        +long lastHeartbeatAt
    }

    class ServiceInstance {
        <<record>>
        +String serviceName
        +String instanceId
        +String host
        +int port
        +address() String
    }

    class DiscoveringPricingClient {
        -ServiceRegistry registry
        -PricingCluster cluster
        -CallLog log
        -int lookups
        +price(String sku) Money
        +lookups() int
        +anyInstance() ServiceInstance
    }

    class HardcodedPricingClient {
        -PRICING_INSTANCE = "pricing-1"
        -PricingCluster cluster
        -ServiceInstance pinned
        +price(String sku) Money
    }

    class PricingCluster {
        -Set~String~ running
        -Map~String, Integer~ callsPerInstance
        +start(String id, int port) ServiceInstance
        +kill(String id)
        +stop(String id)
        +heartbeatAll()
        +endpoint(ServiceInstance i) RemoteCall
        +isRunning(String id) boolean
        +callsTo(String id) int
    }

    class RemoteCall~A,T~ {
        -long latencyMillis
        +invoke(A argument) T
        +failNext(int count) RemoteCall
    }

    class ServiceUnavailableException {
        <<exception>>
    }

    class SimulatedClock {
        +millis() long
        +advance(long amount)
    }

    class CallLog {
        +record(...)
        +note(...)
        +timeline() String
    }

    class Money {
        <<record>>
        +long pence
    }

    ServiceRegistry *-- Lease : holds one per instance
    Lease --> ServiceInstance
    ServiceRegistry --> SimulatedClock : asks the time to expire leases
    ServiceRegistry --> CallLog : REGISTER, DEREGISTER, EXPIRED

    DiscoveringPricingClient --> ServiceRegistry : asks on every call
    DiscoveringPricingClient --> PricingCluster : calls whoever it was given
    DiscoveringPricingClient --> CallLog : LOOKUP, STALE
    DiscoveringPricingClient ..> Money : returns

    HardcodedPricingClient --> PricingCluster : calls pricing-1, always
    HardcodedPricingClient --> ServiceInstance : one, pinned at construction

    PricingCluster --> ServiceRegistry : registers and deregisters itself
    PricingCluster ..> RemoteCall : one endpoint per instance
    RemoteCall ..> ServiceUnavailableException : when nothing is listening
    RemoteCall --> SimulatedClock : advances
    RemoteCall --> CallLog : records
```

</details>

## Notes

**Look at what `HardcodedPricingClient` is missing.** It has no arrow to
`ServiceRegistry`. That single absence is the whole bug. Everything else about the
class is fine — it is shorter than the discovering client, it has fewer
dependencies, and every line of it is correct. It simply has no way to ask a
question it was never designed to ask, and no amount of care inside it can add
one.

**`DiscoveringPricingClient` points at the registry, not at an instance.** The
arrow is the pattern. The client holds a *source of addresses* where the naive one
holds an *address*, and that is the difference between a fact it can refresh and a
fact frozen at construction time.

**The instances register themselves.** `PricingCluster.start` calls
`registry.register`, so the arrow from cluster to registry runs the same direction
as the arrow from client to registry — both are outbound. Nothing in this diagram
ever calls *in* to a service to ask if it is alive. That is deliberate: a registry
that polled everybody would need to know who everybody is, which is the problem
again, one level up.

**`Lease` is a private record inside the registry, and it is the only class here
that stores a timestamp.** Registration is a map and would be dull. The
`lastHeartbeatAt` field is what turns the map into something that forgets, and
forgetting is the only defence against an instance that dies without saying
goodbye.

**`ServiceUnavailableException` comes out of `RemoteCall`, not out of the
registry.** The registry never fails; it happily hands back the address of a dead
process. The failure surfaces one layer later, when somebody actually tries to
use it. Read that as the shape of the honest limitation rather than as an
awkwardness in the design — it is exactly what happens with a real DNS entry or a
real Consul lookup.

**`PricingCluster` has both `kill` and `stop`.** Two methods that both take an
instance out of service, differing only in whether the registry is told. That pair
exists so the demo can show a clean deployment and a crash side by side, because
the pattern behaves completely differently in the two cases and a learner who only
ever sees the polite one will think discovery is simpler than it is.

**The harness is four small classes.** `SimulatedClock`, `RemoteCall`, `CallLog`
and `Money`. Every project in this category carries its own copy rather than
sharing a module, so one directory can be read start to finish without a library
in the way.
