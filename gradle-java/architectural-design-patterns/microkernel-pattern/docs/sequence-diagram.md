# Microkernel Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The checkout asks the kernel for the total of ten thousand. The kernel asks the member discount plugin, which takes off ten percent. It asks the shipping fee plugin, which adds five hundred. The kernel returns ninety five hundred. The kernel never knew what either plugin did.

![Microkernel pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant K as kernel
    participant D as member discount
    participant F as shipping fee
    C->>K: total(10000)
    K->>D: adjust(10000)
    D-->>K: 9000
    K->>F: adjust(9000)
    F-->>K: 9500
    K-->>C: 9500
```

</details>

The load-bearing sentence: **the kernel passes the total along, and does not know what each plugin does.**
