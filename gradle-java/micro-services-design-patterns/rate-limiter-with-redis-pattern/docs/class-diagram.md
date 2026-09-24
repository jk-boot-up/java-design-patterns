# Rate Limiter with Redis Pattern — Class Diagram

The pattern is one class, `ServerSharingRedis`: a server that keeps no bucket of its own and asks Redis, through Bucket4j, on every search. `ServerWithOwnBuckets` is the twin's limiter, kept for the first act. `PlainCounter` exists only to show the mistake Bucket4j avoids.

![Rate Limiter with Redis Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Redis {
        +IMAGE redis 8.10.2-alpine
        +containerRuntimeAvailable() boolean
        +start()
        +uri() String
        +keys() long
        +minutesUntilItForgets(key) long
        +forgetEverything()
        +stop()
    }
    class SearchLimit {
        +TOKENS 10
        +REFILL_EVERY 1 hour
        +configuration() BucketConfiguration
        +inMemoryBucket() Bucket
        +keyFor(clientId) String
    }
    class ServerSharingRedis {
        +ServerSharingRedis(redis, name)
        +ServerSharingRedis(redis, name, clockAhead)
        +search(clientId) boolean
        +searchAndHearWhen(clientId) ConsumptionProbe
        +connected() boolean
        +close()
    }
    class ServerWithOwnBuckets {
        +search(clientId) boolean
        +bucketsHeld() int
    }
    class PlainCounter {
        +fill(tokens)
        +read() int
        +writeBlindly(tokens)
        +writeIfStill(read, tokens) boolean
    }
    class ProxyManager {
        <<Bucket4j>>
        +getProxy(key, configuration) BucketProxy
    }
    class Poll {
        +until(what, condition)
    }
    ServerSharingRedis --> ProxyManager : compare-and-swap, own clock
    ProxyManager ..> Redis : one key per client
    ServerSharingRedis ..> SearchLimit : the rule
    ServerWithOwnBuckets ..> SearchLimit : a bucket in memory
    PlainCounter ..> Redis : GET, then SET
    Redis ..> Poll : waits with
```

</details>
