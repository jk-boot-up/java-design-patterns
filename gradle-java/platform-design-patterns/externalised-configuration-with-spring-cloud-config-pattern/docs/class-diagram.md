# Externalised Configuration with Spring Cloud Config Pattern — Class Diagram

The pattern sits in two classes in the shop. `DeliverySettings` holds the threshold and is marked `@RefreshScope`, so a refresh rebuilds it; `PromotionBanner` copies the same threshold once, at startup, and keeps it. The config server is one annotation. The rest starts, stops and talks to the two programs.

![Externalised Configuration with Spring Cloud Config Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class ShopController {
        +quote(goods) String
        +banner() String
    }
    class DeliverySettings {
        <<RefreshScope>>
        +freeOver 5.00 to 200.00
        +standard 0.00 to 50.00
    }
    class PromotionBanner {
        -text copied at startup
        +text() String
    }
    class ConfigServerApplication {
        <<EnableConfigServer>>
    }
    class ConfigRepository {
        +createIn(folder)
        +commit(freeOver, standard, who, when, message) String
        +log() List
        +uri() String
    }
    class ConfigServerProcess {
        +start(repositoryUri, workFolder)
        +settingsFor(application, profile) String
        +close()
    }
    class Shop {
        +start(serverUrl, whenServerIsDown) Shop
        +quote(goods) Reply
        +banner() String
        +refresh() Reply
        +close()
    }
    class SpringCloudConfigDemo {
        +main(args)
    }
    ShopController --> DeliverySettings : reads on every quote
    ShopController --> PromotionBanner : hands back its text
    ConfigServerProcess ..> ConfigServerApplication : runs as a second Java process
    ConfigServerApplication ..> ConfigRepository : reads over git
    Shop ..> ConfigServerProcess : fetches settings over HTTP
    SpringCloudConfigDemo --> ConfigRepository : commits
    SpringCloudConfigDemo --> ConfigServerProcess : starts and stops
    SpringCloudConfigDemo --> Shop : starts, asks, refreshes, stops
```

</details>
