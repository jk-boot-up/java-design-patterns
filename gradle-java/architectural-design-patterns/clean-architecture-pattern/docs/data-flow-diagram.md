# Clean Architecture Pattern — Data Flow Diagram

One order, entering through either of two controllers, flowing through one
unchanged interactor, and leaving through the boundaries it declared.

![Clean Architecture pattern data flow diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    HttpReq(["a simulated JSON body arrives"])
    BatchReq(["a simulated CSV row arrives"])
    UC["PlaceOrderInteractor.execute<br/>the same method, either way"]
    Check{"every SKU exists,<br/>with enough stock?"}
    Refuse1["refused — via whichever controller called"]
    Charge["PaymentGateway.charge"]
    Declined{"accepted?"}
    Refuse2["refused — nothing written down yet"]
    Reduce["ProductRepository.reduceStock"]
    Save["OrderRepository.save"]
    Notify["NotificationGateway.send"]
    HttpResp(["JSON-shaped response string"])
    BatchResp(["IMPORTED / SKIPPED line"])
    Shortcut["NaivePlaceOrderInteractor<br/>constructs InMemoryOrderRepository directly"]

    HttpReq --> UC
    BatchReq --> UC
    UC --> Check
    Check -- no --> Refuse1
    Check -- yes --> Charge --> Declined
    Declined -- no --> Refuse2
    Declined -- yes --> Reduce --> Save --> Notify
    Notify --> HttpResp
    Notify --> BatchResp

    UC -.->|the shortcut skips every boundary| Shortcut
```

</details>

## Reading The Diagram

**Two arrows enter `UC` from the top, and both go to the same box.**
Whichever controller received the call, `PlaceOrderInteractor.execute` runs
identically.

**`Save` has two different gateways it might really be talking to,
depending only on how the composition root wired this particular
instance** — the diagram cannot show that choice, because the interactor
itself cannot see it either.

**The dashed line to `Shortcut` does not pass through `Check`, `Charge`, or
any gate on this page.** `NaivePlaceOrderInteractor` is drawn reaching
around the whole diagram to construct a gateway directly, which is exactly
the shortcut the architecture test exists to catch.
