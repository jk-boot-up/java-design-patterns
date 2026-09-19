# Feature Toggle Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A customer places an order. The checkout asks the toggle table whether gift wrap is on for this customer. The table checks the rule, which is twenty percent, finds the customer inside it, and says yes. The checkout adds the gift wrap fee. If someone changes the rule to off, the next order is answered no, with no new release.

![Feature Toggle pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as checkout
    participant T as toggle table
    K->>T: isOn(gift-wrap, c7)
    T-->>K: yes, in the 20 percent
    K->>K: add gift wrap
    Note over T: someone sets gift-wrap to Off
    K->>T: isOn(gift-wrap, c7)
    T-->>K: no
```

</details>

The load-bearing sentence: **the answer changes with the table, and the checkout does not.**
