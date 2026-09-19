# Registry Pattern — Data Flow Diagram

One `get`: a thing, or a failure that nothing in the signature warned about.

![Registry Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    Ask(["Registry.get(PaymentGateway.class)"])
    Has{"has anything registered it yet?"}
    Ret(["return whatever is there, from whichever test or class put it"])
    Fail(["IllegalStateException at the first call"])
    Ask --> Has
    Has -- yes --> Ret
    Has -- no --> Fail
```

</details>
