# Database per Service with Containers Pattern — Class Diagram

The pattern is two constructors. `OrderService` is given Postgres and nothing else; `CatalogService` is given MongoDB and nothing else. `OrderHistoryPage` is the join, rewritten in Java. `SharedDatabase` is the arrangement before the split, kept for the first two acts. Look for the arrows that are not there: no service reaches the other's engine.

![Database per Service with Containers Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Engines {
        +NO_RUNTIME_ADVICE
        +containerRuntimeAvailable() boolean
        +start()
        +postgres() Postgres
        +mongo() Mongo
        +close()
    }
    class Postgres {
        +IMAGE postgres 18.6-alpine
        +connectTo(database) Connection
        +createDatabase(name)
    }
    class Mongo {
        +IMAGE mongo 8.3.11-noble
        +newClient() MongoClient
        +stop()
    }
    class SharedDatabase {
        +orderHistory(customer) rows, one join
        +deleteProduct(sku) refused by the foreign key
        +renameProductNameColumnTo(name)
    }
    class OrderService {
        +ordersFor(customer) orders
        +tryToRun(sql) the error, or nothing
        +begin()
        +rollback()
    }
    class CatalogService {
        +namesFor(skus) names, one find
        +renameNameFieldTo(field) documents changed
        +delete(sku) documents deleted
        +takeFromStock(sku, quantity)
        +tryToJoinOrders() orders per product
    }
    class OrderHistoryPage {
        +forCustomer(customer) rows
    }
    class RoundTrips {
        +one()
        +count() int
    }
    Engines *-- Postgres
    Engines *-- Mongo
    SharedDatabase ..> Postgres : database shop
    OrderService ..> Postgres : database orders, only
    CatalogService ..> Mongo : database catalog, only
    OrderHistoryPage --> OrderService : ask for orders
    OrderHistoryPage --> CatalogService : ask for names
    OrderService ..> RoundTrips
    CatalogService ..> RoundTrips
```

</details>
