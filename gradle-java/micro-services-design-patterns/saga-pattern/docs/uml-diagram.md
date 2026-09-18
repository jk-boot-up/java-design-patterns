# Saga — Sequence Diagrams

Five acts, five sequences. What makes them different is the words on the arrows rather than
the shapes, so read the notes rather than the outlines.

## Act One — Five Steps, No Transaction

![Saga sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    participant S as SagaOrchestrator
    participant St as StockService
    participant P as PaymentService
    participant O as OrderService
    participant Sh as ShippingService
    participant E as EmailService

    S->>St: reserve stock
    St-->>S: res-1 (committed)
    S->>P: take payment
    P-->>S: chg-1 (committed)
    S->>O: create order
    O-->>S: ord-9001 (committed)
    S->>Sh: schedule shipment
    Sh-->>S: shp-1 (committed)
    S->>E: send confirmation email
    E-->>S: sent
    Note over S: COMPLETED for £70.95
```

</details>

Every arrow back says committed, and that is the point of the diagram. By the time payment
is called, the reservation is already final and nothing is holding it open.

## Act Two — The Courier Refuses, And Everything Unwinds

![Act Two — The Courier Refuses, And Everything Unwinds](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    participant S as SagaOrchestrator
    participant St as StockService
    participant P as PaymentService
    participant O as OrderService
    participant Sh as ShippingService

    S->>St: reserve stock
    St-->>S: res-1
    S->>P: take payment
    P-->>S: chg-1
    S->>O: create order
    O-->>S: ord-9002
    S->>Sh: schedule shipment
    Sh--)S: no courier covers the address
    Note over S: stop, and walk backwards
    S->>O: cancel order
    O-->>S: cancelled
    S->>P: refund chg-1
    P-->>S: ref-2
    S->>St: release res-1
    St-->>S: released
    Note over S: COMPENSATED, customer owes nothing
```

</details>

Read the bottom half in the order it happens: order, then payment, then stock — the exact
reverse of the top half. The order is cancelled before the money is refunded so that finance
is never looking at a confirmed order with no money against it.

## Act Three — The Refund Fails Too

![Act Three — The Refund Fails Too](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    participant S as SagaOrchestrator
    participant St as StockService
    participant P as PaymentService
    participant O as OrderService
    participant Sh as ShippingService

    S->>Sh: schedule shipment
    Sh--)S: no courier covers the address
    S->>O: cancel order
    O-->>S: cancelled
    S->>P: refund chg-1
    P--)S: no answer
    Note over S: record it, and carry on unwinding
    S->>St: release res-1
    St-->>S: released
    Note over S: NEEDS_HUMAN_HELP - £70.95 still held
```

</details>

Two things to see. The refund failing does not stop the stock being released. And the saga
still returns, with an outcome naming the step it could not undo.

## Act Four — The Email In The Wrong Place

![Act Four — The Email In The Wrong Place](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    participant S as SagaOrchestrator
    participant O as OrderService
    participant E as EmailService
    participant Sh as ShippingService

    S->>O: create order
    O-->>S: ord-9004
    S->>E: send confirmation email
    E-->>S: in the customer's inbox
    S->>Sh: schedule shipment
    Sh--)S: no courier covers the address
    Note over S,E: no compensation exists for a sent email
    S->>O: cancel order
    O-->>S: cancelled
    Note over S: NEEDS_HUMAN_HELP - the email is still there
```

</details>

The order is cancelled, the money comes back, and the email stays in the inbox. Nothing in
the code is broken; the sequence is.

## Act Five — The Same Failure, Without A Saga

![Act Five — The Same Failure, Without A Saga](images/uml-diagram-5.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    participant N as NaiveCheckoutService
    participant St as StockService
    participant P as PaymentService
    participant O as OrderService
    participant Sh as ShippingService

    N->>St: reserve
    St-->>N: res-1
    N->>P: charge
    P-->>N: chg-1
    N->>O: create
    O-->>N: CONFIRMED
    N->>Sh: schedule
    Sh--)N: no courier covers the address
    Note over N: caught, logged, returns null
    Note over N,Sh: nothing is undone. Money taken, nothing shipped.
```

</details>

There is no second half to this diagram, and that is the whole comparison.

## Notes On Reading These

**Dashed arrows back are failures.** Solid ones are a service doing what it was asked.

**Nothing in these diagrams is a lock.** No participant is holding anything open while it
waits for another. Every call completes and commits before the next one starts, which is
what makes compensation the only available tool.

**The timings are exact.** `SimulatedClock` advances by fixed amounts per service, so the
timeline in the demo output matches these sequences step for step on any machine.
