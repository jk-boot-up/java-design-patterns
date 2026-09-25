# Externalised Configuration with Spring Cloud Config Pattern — Architecture Diagram

Three places, and the value passes through all of them. A git repository in a temporary folder holds the file. The config server, a separate Java process, reads it on every request. The shop fetches from the server at startup and on a refresh, and inside the shop only the refresh-scoped settings are rebuilt.

![Externalised Configuration with Spring Cloud Config Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    subgraph Repo["git repository, created by the demo"]
        F[("checkout-service.yml<br/>free-over 35.00<br/>4 commits, each with who and when")]
    end
    subgraph Server["config server, a second Java process"]
        CS["Spring Cloud Config Server<br/>reads git on every request"]
    end
    subgraph ShopBox["the shop, Spring Boot"]
        DS["DeliverySettings<br/>RefreshScope: rebuilt after a refresh"]
        PB["PromotionBanner<br/>copied at startup: never rebuilt"]
        Q["/quote"]
        B["/banner"]
        R["POST /actuator/refresh"]
    end
    F -- "read with JGit" --> CS
    CS -- "HTTP, at startup and on a refresh" --> DS
    CS -- "HTTP, at startup only" --> PB
    DS --> Q
    PB --> B
    R -. "fetch again" .-> CS
```

</details>
