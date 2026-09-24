# Cache-Aside with Redis Pattern — Class Diagram

The pattern is one class, `ProductService`: look in Redis, and on a miss read the database and fill Redis. `RedisCache` is how a price is written into Redis and read back; `RedisServer` owns the container.

![Cache-Aside with Redis Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class ProductService {
        +get(sku) Product
        +getSharingInsideThisInstance(sku) Product
        +getSharingThroughRedis(sku) Product
        +changePrice(sku, pence)
    }
    class RedisCache {
        +key(sku) String
        +get(sku) Product
        +peek(sku) Product
        +put(product)
        +putWithoutExpiry(product)
        +forget(sku)
        +secondsToLive(sku) long
        +tryLock(sku, holdFor) boolean
        +unlock(sku)
    }
    class RedisServer {
        +IMAGE redis 8.10.2-alpine
        +containerRuntimeAvailable() boolean
        +start()
        +connect() RedisClient
        +cli(command) String
        +close()
    }
    class Database {
        +withTenProducts() Database
        +read(sku) Product
        +put(product)
        +answerSlowly(millis)
        +reads() int
    }
    class Product {
        <<record>>
        +sku
        +pricePence
    }
    class SecondShop {
        +main(mode, host, port)
    }
    class Poll {
        +until(what, condition)
    }
    ProductService --> RedisCache : looks aside at
    ProductService --> Database : reads on a miss
    RedisServer ..> RedisCache : connection for
    RedisCache ..> Product : stores as text
    Database ..> Product : holds
    SecondShop ..> ProductService : a second instance
    ProductService ..> Poll : waits with
```

</details>
