# Interpreter with SpEL Pattern — Architecture Diagram

Text is parsed once into trees. Each order is evaluated against the trees.

![Interpreter with SpEL Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    T["rule text"] --> P["SpelExpressionParser"]
    P --> E["parsed tree, kept"]
    O["order"] --> X["evaluation context"]
    E --> X
    X --> R["promotions that match"]
```

</details>
