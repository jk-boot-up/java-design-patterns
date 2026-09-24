# Idempotent Consumer with Kafka Pattern — Class Diagram

The pattern is one class, `RecordIdInSameTransaction`: it writes the message's id first, inside a transaction, and queues the email only if Postgres says the id was new. `Notifications` is one running copy of the service in its consumer group, `Broker` and `Database` own the two containers, and the other three handlers are the ways of getting it wrong.

![Idempotent Consumer with Kafka Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Broker {
        +IMAGE apache/kafka 4.3.1
        +containerRuntimeAvailable() boolean
        +createTopic(topic)
        +placeWrittenDown(group, topic) long
        +moveGroupBackToTheStart(group, topic)
        +hoursTheTopicKeepsOrders(topic) long
    }
    class Database {
        +IMAGE postgres 18.6-alpine
        +connect() Connection
        +confirmations() int
        +handledIds() int
        +waitingOnALock() int
        +forgetIdsOlderThanHours(h) int
    }
    class Checkout {
        +place(order) long
    }
    class Notifications {
        +take(n) List
        +takeAndHandle(n, handler) int
        +sayDone()
        +crash()
        +placesHandedOver() List
    }
    class Handler {
        <<interface>>
        +handle(order) boolean
    }
    class JustSend
    class RememberInMemory {
        -Set handled
    }
    class RecordIdAfterwards
    class RecordIdInSameTransaction {
        +handle(order) boolean
        +begin(order) Open
    }
    class OrderPlaced {
        <<record>>
        +messageId
        +orderId
        +pence
        +placedAt
    }
    Checkout ..> Broker : writes to a topic
    Notifications ..> Broker : reads as a group
    Notifications ..> Handler : hands each order to
    Handler <|.. JustSend
    Handler <|.. RememberInMemory
    Handler <|.. RecordIdAfterwards
    Handler <|.. RecordIdInSameTransaction
    RecordIdInSameTransaction --> Database : id and email, one transaction
    Handler ..> OrderPlaced : is handed
```

</details>
