# Claim Check with S3 Pattern — Class Diagram

The pattern is two small classes, `Sender` and `Receiver`, and the ticket between them, `Claim`. `Bucket` and `Queue` are thin wrappers over Amazon S3 and SQS; `LocalStack` owns the container.

![Claim Check with S3 Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class LocalStack {
        +IMAGE localstack 4.14.0
        +containerRuntimeAvailable() boolean
        +start()
        +s3() S3Client
        +sqs() SqsClient
        +requests() Map
        +close()
    }
    class Bucket {
        +create(s3, name) Bucket
        +keepEveryVersion() Bucket
        +removeEverythingAfterDays(days) Bucket
        +put(key, bytes) Stored
        +get(key) bytes
        +get(key, versionId) bytes
        +delete(key)
        +delete(key, versionId)
        +keysListed() int
        +versionsStored() int
        +deleteMarkers() int
    }
    class Queue {
        +create(sqs, name) Queue
        +send(text)
        +take() Received
        +delete(received)
        +waiting() int
        +maximumMessageBytes() int
        +keepsUnreadSeconds() int
    }
    class Claim {
        <<record>>
        +bucket
        +key
        +versionId
        +size
        +sha256
        +toText() String
        +read(text) Claim
    }
    class Sender {
        +asMessageText(pdf) String
        +sendWhole(pdf)
        +send(pdf) Claim
        +sendUnder(key, pdf) Claim
    }
    class Receiver {
        +redeemNext() bytes
    }
    class InvoicePdf {
        +of(orderId, bytes, edition) bytes
    }
    LocalStack --> Bucket : S3 client
    LocalStack --> Queue : SQS client
    Sender --> Bucket : stores first
    Sender --> Queue : then sends
    Sender ..> Claim : writes
    Receiver --> Queue : takes a ticket
    Receiver --> Bucket : fetches, deletes
    Receiver ..> Claim : reads and checks
    Sender ..> InvoicePdf : sends
```

</details>
