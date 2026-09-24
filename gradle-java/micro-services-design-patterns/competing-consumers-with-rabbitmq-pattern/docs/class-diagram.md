# Competing Consumers with RabbitMQ Pattern — Class Diagram

The pattern is one class, `Picker`: one competing consumer, with its prefetch and its choice of when to say done. `OrderQueue` is the queue as checkout sees it, `Broker` owns the container, and the rest is the store's own vocabulary.

![Competing Consumers with RabbitMQ Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Broker {
        +IMAGE rabbitmq 4.3.6-alpine
        +containerRuntimeAvailable() boolean
        +start()
        +address() String
        +connect() Connection
        +close()
    }
    class OrderQueue {
        +send(order)
        +sendOrders(first, last)
        +waiting() int
        +pickersListening() int
    }
    class Picker {
        +NO_LIMIT 0
        +oneAtATime(name, broker, queue, stock)$ Picker
        +holdingUpTo(n, name, broker, queue, stock)$ Picker
        +withNoLimit(name, broker, queue, stock)$ Picker
        +forgettingOnHandover(name, broker, queue, stock)$ Picker
        +stallingOn(which) Picker
        +start() Picker
        +release()
        +handedOver() int
        +markedSeenBefore() int
        +picked() List
        +holding() int
        +crash()
        +close()
    }
    class PickOrder {
        <<record>>
        +orderId
        +quantity
        +item
        +text() String
        +read(text) PickOrder
    }
    class Stock {
        +reserve(order)
        +timesReserved(orderId) int
    }
    class Poll {
        +until(what, condition)
    }
    Broker --> OrderQueue : one connection each
    Broker --> Picker : one connection each
    OrderQueue ..> PickOrder : sends as text
    Picker ..> PickOrder : is handed
    Picker --> Stock : reserves before picking
    Picker ..> Poll : waited on with
```

</details>
