# Load Balancing with Spring Cloud LoadBalancer Pattern — Class Diagram

A client, a strategy of our own, and the copies.

![Load Balancing with Spring Cloud LoadBalancer Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class CatalogueClient {
        <<@Service>>
        +get(service, path) String
    }
    class LeastWorkBalancer {
        <<ReactorServiceInstanceLoadBalancer>>
        +choose(request) Mono
    }
    class LeastWorkConfiguration {
        <<per service name>>
    }
    class Backend {
        <<a real HTTP server>>
        +hits() int
        +work() int
        +goDown()
    }
    CatalogueClient ..> LeastWorkBalancer : for catalogue-fast
    LeastWorkConfiguration --> LeastWorkBalancer
    LeastWorkBalancer ..> Backend : picks one
```

</details>
