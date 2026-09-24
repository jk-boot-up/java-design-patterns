# Transactional Outbox with Debezium Pattern — Class Diagram

The pattern is one class with something missing: `OutboxCheckout` writes the order and an outbox row in one Postgres transaction and has no Kafka code at all. `ChangeDataCapture` is Debezium's embedded engine, reading the outbox changes from Postgres's log and forwarding them to Kafka. `DualWriteCheckout` is the way of getting it wrong, and `OrdersDatabase` and `Broker` own the two containers.

![Transactional Outbox with Debezium Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class OrdersDatabase {
        +IMAGE postgres 18.6-alpine
        +connect() Connection
        +orders() int
        +outboxRows() int
        +walLevel() String
        +slotActive(slot) boolean
        +logHeldForSlot(slot) long
        +dropSlot(slot)
    }
    class Broker {
        +IMAGE apache/kafka 4.3.1
        +TOPIC order-events, 3 partitions
        +containerRuntimeAvailable() boolean
        +mark() Map
        +countSince(mark) int
        +readSince(mark) List
    }
    class DualWriteCheckout {
        +saveThenSend(order, dieBetween)
        +sendThenSave(order, dieBetween)
    }
    class OutboxCheckout {
        +place(order)
        +placeButCardDeclined(order)
        +moveOn(orderId, status, type)
    }
    class ChangeDataCapture {
        +SLOT orders_outbox
        +DEBEZIUM_VERSION 3.6.3.Final
        +start()
        +stop()
        +crashAfterSending(n)
        +awaitCrash()
    }
    class Order {
        <<record>>
        +orderId
        +customer
        +totalPence
    }
    class OrderEvent {
        <<record>>
        +partition
        +place
        +orderId
        +type
        +eventId
    }
    DualWriteCheckout --> OrdersDatabase : saves
    DualWriteCheckout --> Broker : sends, separately
    OutboxCheckout --> OrdersDatabase : order and outbox row, one transaction
    ChangeDataCapture ..> OrdersDatabase : reads the log through a slot
    ChangeDataCapture --> Broker : sends each event, keyed by order
    Broker ..> OrderEvent : reads back
    OutboxCheckout ..> Order : places
```

</details>
