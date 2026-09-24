# Publisher-Subscriber with Redis Pattern — Class Diagram

The pattern is two classes: `OrderService` publishes, `Subscriber` listens. `RedisServer` owns the container and reads Redis's counters; `LoyaltyProcess` is a subscriber that runs as a program of its own.

![Publisher-Subscriber with Redis Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class RedisServer {
        +IMAGE redis 8.10.2-alpine
        +containerRuntimeAvailable() boolean
        +start()
        +connect() Jedis
        +limitEachListenerTo(size)
        +listenerLimit() String
        +listenersCutOff() long
        +listenersOn(channel) long
        +keysStored() long
        +close()
    }
    class OrderService {
        +PLACED orders.placed
        +CANCELLED orders.cancelled
        +publish(event) long
        +publishPlaced(first, howMany) List
    }
    class Subscriber {
        +listen(server, name, channels) Subscriber
        +listenToPattern(server, name, pattern) Subscriber
        +stopReading()
        +startReading()
        +received() List
        +wasCutOff() boolean
        +close()
    }
    class LoyaltyProcess {
        +main(host, port, wanted)
    }
    class SeparateProcess {
        +ordersReceived() List
        +awaitExit() int
    }
    class OrderEvent {
        <<record>>
        +kind
        +orderId
        +channel() String
        +text() String
        +read(text) OrderEvent
    }
    class DirectOrderService {
        +placeOrder(event)
        +servicesKnownByName() int
    }
    RedisServer --> OrderService : connection for
    RedisServer --> Subscriber : connection for each
    OrderService ..> OrderEvent : publishes as text
    Subscriber ..> OrderEvent : reads back
    SeparateProcess --> LoyaltyProcess : starts in a second JVM
```

</details>
