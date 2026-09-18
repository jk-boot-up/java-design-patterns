# Hexagonal Architecture Pattern — Data Flow Diagram

One order, entering through either of two driving adapters, flowing through
one unchanged core, and leaving through the ports it declared.

![Hexagonal Architecture pattern data flow diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    HttpReq(["a simulated JSON body arrives"])
    CliReq(["a simulated command line arrives"])
    Core["PlaceOrderService.place<br/>the same method, either way"]
    Check{"every SKU exists,<br/>with enough stock?"}
    Refuse1["refused — via whichever adapter called"]
    Charge["PaymentGateway.charge"]
    Declined{"accepted?"}
    Refuse2["refused — nothing written down yet"]
    Reduce["ProductCatalog.reduceStock"]
    Save["OrderStore.save"]
    Notify["Notifier.send"]
    HttpResp(["JSON-shaped response string"])
    CliResp(["plain-text response string"])
    Shortcut["NaivePlaceOrderService<br/>constructs InMemoryOrderStore directly"]

    HttpReq --> Core
    CliReq --> Core
    Core --> Check
    Check -- no --> Refuse1
    Check -- yes --> Charge --> Declined
    Declined -- no --> Refuse2
    Declined -- yes --> Reduce --> Save --> Notify
    Notify --> HttpResp
    Notify --> CliResp

    Core -.->|the shortcut skips the port entirely| Shortcut
```

</details>

## Reading The Diagram

**Two arrows enter `Core` from the top, and both go to the same box.**
Whichever driving adapter received the call, `PlaceOrderService.place` runs
identically — there is no branch anywhere in the core asking which adapter
called it, because the core cannot tell.

**Every gate and every write sits inside the one shared path.** A refusal
from either entry point takes the identical route back out, formatted
differently only at the very last step, by the adapter that started the
call.

**The dashed line to `Shortcut` does not pass through any port box.**
`NaivePlaceOrderService` is drawn reaching around the whole diagram to
construct `InMemoryOrderStore` for itself, which is exactly the shortcut
the architecture test exists to catch.
