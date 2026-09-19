# Future/Promise with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. Concurrency Is The Pool's

![Concurrency Is The Pool's](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant Pool as pool of 8, or of 1
    C->>Pool: three lookups
    Pool-->>C: 3 in flight, or 1 at a time
```

</details>

## 2. An Exception, Two Ways

![An Exception, Two Ways](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant F as future method
    participant V as void method
    C->>F: call, exception thrown on the pool
    F-->>C: CompletionException, on get
    C->>V: call, exception thrown on the pool
    V-->>C: nothing, only a registered handler
```

</details>

## 3. A Lost Thread-Local

![A Lost Thread-Local](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller thread
    participant D as TaskDecorator
    participant T as pool thread
    C->>C: CustomerContext = 7
    C->>D: submit
    D->>T: copy the customer, then run
    T-->>C: customer 7
```

</details>

## 4. Give Up And Cancel

![Give Up And Cancel](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant T as pool thread
    C->>C: orTimeout(200ms) fires
    C->>C: cancel(true), the flag is set
    T->>T: keeps going to the end
```

</details>

