# Pipes and Filters Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The pipeline takes the line ada, mug blue, two. Parse turns it into a parsed record. Validate checks the quantity, and passes it on. Price works out sixteen hundred pence. Tax adds a fifth. Format writes the confirmation. Then the next line starts. If any step drops a line, it writes the reason, and the pipeline moves on to the next line.

![Pipes and Filters pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as pipeline
    participant A as parse
    participant B as validate
    participant C as price
    participant D as tax
    participant E as format
    P->>A: "ada, MUG-BLUE, 2"
    A-->>P: Parsed
    P->>B: Parsed
    B-->>P: Parsed
    P->>C: Parsed
    C-->>P: Priced 1600
    P->>D: Priced
    D-->>P: Taxed 1920
    P->>E: Taxed
    E-->>P: "ada: 2 x MUG-BLUE = £19.20"
```

</details>

The load-bearing sentence: **each filter sees one item, and knows nothing about the others.**
