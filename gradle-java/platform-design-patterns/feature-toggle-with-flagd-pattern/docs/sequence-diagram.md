# Feature Toggle with flagd Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Someone edits the flags file and turns gift wrap on. Flagd sees the file change, and reads it again, with no restart. The next order asks flagd whether gift wrap is on for this customer. Flagd checks its rule, which is on for everyone, and says yes. The checkout adds the fee.

![Feature Toggle with flagd pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant E as editor
    participant F as flags.json
    participant D as flagd
    participant C as checkout
    E->>F: gift-wrap: on
    D->>F: sees the change, reads it
    C->>D: is gift-wrap on for c7?
    D-->>C: yes
    C->>C: add gift wrap
```

</details>

The load-bearing sentence: **the file is the switch, and flagd reads it live.**
