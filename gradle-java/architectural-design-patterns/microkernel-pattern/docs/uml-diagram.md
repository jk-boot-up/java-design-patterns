# Microkernel Pattern — UML Sequence Diagrams

Four sequences.

## 1. Adding A Plugin

![Adding A Plugin](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as admin
    participant K as kernel
    participant G as gift wrap
    A->>K: register(gift wrap)
    K->>G: start()
    K->>K: add to the list
    A->>K: unregister(gift-wrap)
    K->>G: stop()
```

</details>

