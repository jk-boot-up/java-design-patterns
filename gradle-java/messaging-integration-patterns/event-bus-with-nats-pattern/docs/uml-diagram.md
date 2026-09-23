# Event Bus with NATS Pattern — UML Sequence Diagrams

Four sequences: the miss, the fan-out, a subscriber that throws, and asking instead of telling.

## 1. The Event Nobody Hears

Nobody is listening. Checkout publishes ORD-1 and the server drops it. The warehouse then starts listening and waits for the server to confirm. Checkout publishes ORD-2, and that is the first event the warehouse ever sees.

![The event nobody hears](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant N as NATS
    participant W as warehouse
    C->>N: publish OrderPlaced ORD-1
    Note over N: no listeners, so it is dropped
    W->>N: subscribe to store.orders.placed
    N-->>W: confirmed
    C->>N: publish OrderPlaced ORD-2
    N->>W: OrderPlaced ORD-2
```

</details>

## 2. One Announcement, Three Listeners

Checkout publishes once. The server sends a copy to each service listening for that name. Checkout is never told how many there were.

![One announcement, three listeners](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant N as NATS
    participant E as email
    participant W as warehouse
    participant A as analytics
    C->>N: publish OrderPlaced ORD-1
    N->>E: OrderPlaced ORD-1
    N->>W: OrderPlaced ORD-1
    N->>A: OrderPlaced ORD-1
    N-->>C: nothing
```

</details>

## 3. A Subscriber That Throws

The email service's handler fails. The warehouse, on its own connection, still reacts. Checkout had already moved on before either of them ran.

![A subscriber that throws](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant N as NATS
    participant E as email
    participant W as warehouse
    C->>N: publish OrderPlaced ORD-1
    N->>E: OrderPlaced ORD-1
    E->>E: throws, mail server timed out
    N->>W: OrderPlaced ORD-1
    W->>W: reserves the stock
    Note over C: never told about either
```

</details>

## 4. Asking Instead Of Telling

A request is a question with a reply address on it. When nobody is listening for that name, the server says so at once rather than leaving the caller waiting.

![Asking instead of telling](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant N as NATS
    C->>N: request on store.orders.cancelled
    N->>N: looks for listeners, finds none
    N-->>C: no responders
    Note over C: the one time a publisher learns the truth
```

</details>
