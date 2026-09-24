# Queue-Based Load Leveling with SQS Pattern — Class Diagram

The pattern is three small pieces: `Checkout` puts orders on the queue, `OrderQueue` is the queue on Amazon SQS, and `Packer` takes them off at its own pace and deletes them only after packing. `Warehouse` counts parcels so an order packed twice shows; `LocalStack` owns the container.

![Queue-Based Load Leveling with SQS Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class LocalStack {
        +IMAGE localstack 4.14.0
        +containerRuntimeAvailable() boolean
        +start()
        +sqs() SqsClient
        +requests() Map
        +close()
    }
    class OrderQueue {
        +MOST_PER_REQUEST 10
        +create(sqs, name, visibilityTimeoutSeconds) OrderQueue
        +sendAll(orderIds) int
        +take(most, waitSeconds) List
        +delete(taken)
        +deleteTogether(taken)
        +stillWorking(taken, seconds)
        +waiting() int
        +inFlight() int
        +visibilityTimeoutSeconds() int
    }
    class Taken {
        <<record>>
        +orderId
        +receipt
        +timesHandedOut
    }
    class Packer {
        +round() List
    }
    class Warehouse {
        +pack(orderId)
        +parcelsFor(orderId) int
        +packedTwiceOrMore() int
    }
    class Checkout {
        +orders(first, count) List
    }
    LocalStack --> OrderQueue : SQS client
    Checkout ..> OrderQueue : puts the burst on
    Packer --> OrderQueue : takes up to 10, deletes after
    Packer --> Warehouse : packs
    OrderQueue ..> Taken : hands out
```

</details>
