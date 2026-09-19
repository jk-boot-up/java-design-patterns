# Fork-Join Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The root task is asked for the sum of a hundred thousand totals. It is too big, so it makes a left task and a right task. It forks the left, which another worker may pick up, and computes the right itself. The right splits again in the same way. Eventually a piece is small enough, and is added directly. Each task then joins its left half, adds the two answers, and returns the sum to its parent, until the root has the total.

![Fork-Join pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant R as root task
    participant L as left task (another worker)
    participant M as right task (this worker)
    R->>L: fork the left half
    R->>M: compute the right half
    M-->>R: sum of the right
    L-->>R: join: sum of the left
    R->>R: left + right
```

</details>

The load-bearing sentence: **each task forks one half, does the other, then joins.**
