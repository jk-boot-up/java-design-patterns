# Identity Map with JPA Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The caller asks the entity manager for customer seven. The persistence context has nothing yet, so Hibernate runs one select and keeps the customer in the context. The caller asks again. This time the context already has it, so the same object comes back with no SQL at all. If a second entity manager is asked, it has its own, empty context, so it runs its own select and builds its own, different object.

![Identity Map with JPA pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant EM as EntityManager one
    participant DB as H2
    participant EM2 as EntityManager two
    Caller->>EM: find(Customer, 7)
    EM->>DB: select
    EM-->>Caller: customer A
    Caller->>EM: find(Customer, 7)
    EM-->>Caller: customer A, no SQL
    Caller->>EM2: find(Customer, 7)
    EM2->>DB: select
    EM2-->>Caller: customer B, a different object
```

</details>

The load-bearing sentence: **the map belongs to one entity manager, so two of them give two objects.**
