# Transaction Script Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The request calls the place order script. The script opens a transaction and checks the quantity and the stock. It takes two from the stock and prices the order at sixteen pounds. It charges the card, and the card is declined, so the script throws. The database undoes the stock change. The stock is ten again, and nothing was saved.

![Transaction Script pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant R as request
    participant S as script
    participant D as database
    participant P as payment
    R->>S: run(ada, MUG-BLUE, 2)
    S->>D: begin, take 2 from stock
    S->>P: charge 1600
    P-->>S: declined
    S-->>R: throws
    D->>D: rollback: stock 10, no order
```

</details>

The load-bearing sentence: **one script is one transaction, so a failure leaves nothing half done.**
