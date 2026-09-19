# MVP and MVVM Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. In M V V M, the screen binds to the view model once, at the start. Later, the customer adds an item. The view model updates the cart, and sets its total. The total has a listener, which is the screen's label, and it changes. The view model never knew the screen existed.

![MVP and MVVM pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as screen
    participant M as view model
    participant C as cart
    S->>M: bind(total)
    M-->>S: current value
    S->>M: add(1600)
    M->>C: add(1600)
    M->>M: total.set(£16.00)
    M-->>S: total changed: £16.00
```

</details>

The load-bearing sentence: **the view model pushes to whoever bound, and does not know who.**
