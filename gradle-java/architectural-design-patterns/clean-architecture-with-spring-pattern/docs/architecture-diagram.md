# Clean Architecture with Spring — Architecture Diagram

Two ways of producing the identical graph, side by side. The three inner
circles — entities, use cases, adapters — are the same boxes either way;
only the outermost box, the one that builds them, differs.

![Clean Architecture with Spring architecture diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    subgraph Hand["clean-architecture-pattern — by hand"]
        direction TB
        Main["PlaceAnOrderDemo.shop()<br/>twenty lines of new(...)"]
        Graph1["entities + usecases + adapters<br/>(the same seven objects)"]
        Main -->|calls new, at your own pace| Graph1
    end

    subgraph Container["clean-architecture-with-spring — by container"]
        direction TB
        Ctx["Spring ApplicationContext<br/>reads AppConfig at startup"]
        Graph2["entities + usecases + adapters<br/>(byte-for-byte the same files)"]
        Ctx -->|calls @Bean methods, once, at refresh| Graph2
    end

    Broken["BrokenAppContext<br/>one @Bean missing"]
    Fail(["UnsatisfiedDependencyException<br/>at startup, not at compile time"])
    Broken -.->|the one contrast this project owns| Fail
```

</details>

## Reading The Diagram

**The inner boxes are identical, and labelled as such.** This diagram does
not repeat what is inside them — see the hand-wired project's own
architecture diagram for that.

**Only the outer box changed shape.** `PlaceAnOrderDemo.shop()` is a method
a person wrote and reads top to bottom. `AppConfig`, read by a container,
is discovered and invoked in whatever order satisfies its own dependencies
— which is exactly the freedom that lets a missing bean go unnoticed until
something actually asks for it.
