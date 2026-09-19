# Thread Pool with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. The Default Executor

![The Default Executor](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant B as Spring Boot
    participant E as ThreadPoolTaskExecutor
    B->>E: core 8, max unbounded, queue unbounded
    Note over E: eight workers and a queue that never says no
```

</details>

## 2. A Backlog

![A Backlog](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as callers
    participant E as executor
    C->>E: 8 orders, all running, stuck at a gate
    C->>E: 1000 more
    E-->>C: accepted, all of them
    Note over E: 1000 waiting, 0 refused
```

</details>

## 3. A Refusal

![A Refusal](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant E as executor, 2 threads, queue 3
    C->>E: 5 orders accepted
    C->>E: a sixth
    E-->>C: TaskRejectedException
```

</details>

## 4. A Call On This

![A Call On This](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant M as main thread
    participant S as PackingService
    M->>S: packThroughThis()
    S->>S: this.pack()
    Note over S: no proxy, no pool: runs on main
```

</details>

