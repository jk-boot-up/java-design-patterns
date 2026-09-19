# Content-Based Router Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. An order for a gift card worth fifteen hundred pounds reaches the router. The router tries its first rule, high value, and the order satisfies it, so the router sends it to fraud review and stops. It never tries the gift card rule. If the rules had been the other way round, the gift card rule would have matched first, and the order would have gone to digital delivery.

![Content-Based Router pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as sender
    participant R as router
    participant F as fraud review
    S->>R: gift card, 1500.00
    R->>R: rule 1, high value: matches
    R->>F: send
    Note over R: rule 2 is never tried
```

</details>

The load-bearing sentence: **the order of the rules decides where a message goes.**
