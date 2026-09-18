# Clean Architecture Pattern — Architecture Diagram

Read it as three concentric rings around one centre, drawn here as nested
boxes because Mermaid draws boxes rather than circles: entities innermost,
use cases around them, adapters around those. Every arrow crossing a
boundary points inward.

![Clean Architecture pattern architecture diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    Root["PlaceAnOrderDemo<br/>composition root — frameworks & drivers"]

    subgraph Adapters["interface adapters"]
        direction TB
        Ctrl1["CheckoutController"]
        Ctrl2["BatchOrderController «new»"]
        Gw1["InMemoryOrderRepository"]
        Gw2["FileBackedOrderRepository «new»"]

        subgraph UseCases["use cases"]
            direction TB
            UC["PlaceOrderInteractor"]
            Bounds["OrderRepository · ProductRepository ·<br/>PaymentGateway · NotificationGateway"]

            subgraph Entities["entities"]
                direction TB
                Ent["Order · Money · Product<br/>knows nothing outside itself"]
            end
        end
    end

    subgraph N["naive.usecases — outside the real architecture"]
        Naive["NaivePlaceOrderInteractor"]
    end

    Root -.->|wires everything by hand| Adapters

    Ctrl1 -->|calls in| UC
    Ctrl2 -->|calls in| UC
    UC --> Bounds
    Gw1 -->|implements| Bounds
    Gw2 -->|implements| Bounds
    UC -.->|builds| Ent

    Naive -->|names the gateway directly —<br/>the rule this project enforces| Gw1
```

</details>

## Reading The Diagram

**Three rings, nested, and every arrow that crosses a ring boundary points
toward the centre.** Controllers call the use case; gateways implement its
boundaries. Nothing inside `usecases` has an arrow reaching out to
`adapters`.

**Two controllers and two gateways sit in the same outer ring, and both
pairs point at the same inner boundary.** That is the forced change,
drawn: addition, not replacement — the originals are still there, still
working.

**The dashed box sits entirely outside the rings.**
`NaivePlaceOrderInteractor`'s one outward arrow is the line
`ArchitectureRuleCatchesTheShortcutTest` widens the dependency rule to
catch.
