# Cache-Aside with Redis Pattern — Data Flow Diagram

What one price read does, from the shop's question to the answer, including the lock that guards a refill.

![Cache-Aside with Redis Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    In(["a customer opens the page for SKU-0"])
    Ask{"does Redis hold product:SKU-0?"}
    Hit(["hit: show the cached price"])
    Lock{"SET lock NX: did this request win?"}
    Wait["wait for the price to appear in Redis"]
    Again{"filled meanwhile?"}
    Read["read the database"]
    Fill["SET the price with its expiry"]
    Free["delete the lock"]
    Show(["show the price"])
    Expire["Redis removes the key when its time is up"]
    In --> Ask
    Ask -- yes --> Hit
    Ask -- no --> Lock
    Lock -- no --> Wait --> Show
    Lock -- yes --> Again
    Again -- yes --> Free
    Again -- no --> Read --> Fill --> Free --> Show
    Fill -. later .-> Expire -.-> Ask
```

</details>
