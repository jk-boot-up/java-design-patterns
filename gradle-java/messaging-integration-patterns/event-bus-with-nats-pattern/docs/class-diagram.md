# Event Bus with NATS Pattern — Class Diagram

A server in a container, services that publish, and listeners that hear only what is announced while they are in the room.

![Event Bus with NATS Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class NatsServer {
        +start()
        +url() String
        +monitorUrl() String
    }
    class StoreBus {
        +publish(subject, event)
        +subscribe(listener, subject) StoreSubscriber
        +onEvent(subject, handler)
        +settle()
        +ask(subject, question) String
    }
    class StoreSubscriber {
        +waitForNext() String
        +received() long
        +stopListening()
    }
    class ServerView {
        +storeListeners() long
        +waitUntilStoreListeners(wanted) long
    }
    class DirectStore {
        +wires() int
        +wiresThroughABus() int
    }
    StoreBus ..> NatsServer : connects to
    StoreBus --> StoreSubscriber : hands back
    ServerView ..> NatsServer : asks on the second port
```

</details>

Said out loud: `StoreBus` is one service's link to the bus. It can publish an event under a name, and it can subscribe, which hands back a `StoreSubscriber` that waits for events with a deadline. `ServerView` is the only thing that can say how many listeners exist, and it has to ask the server. `DirectStore` is the version with no bus at all, and it exists only to count the wiring.
