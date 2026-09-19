# Registry with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. Injected Versus Asked

![Injected Versus Asked](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as Spring
    participant I as InjectedCheckout
    participant L as LocatorStyleCheckout
    S->>I: new InjectedCheckout(policy, gateway, notifier)
    S->>L: new LocatorStyleCheckout(), then setApplicationContext
    L->>S: getBean, three times
```

</details>

## 2. The Cached Context

![The Cached Context](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as test A
    participant Cache as Spring test cache
    participant B as test B
    A->>Cache: context for this configuration
    Cache-->>A: new context
    B->>Cache: context for this configuration
    Cache-->>B: the same one, cached
```

</details>

## 3. DirtiesContext

![DirtiesContext](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as test A
    participant Cache as Spring test cache
    participant B as test B
    A->>Cache: run, then @DirtiesContext
    Cache->>Cache: discard the context
    B->>Cache: context for this configuration
    Cache-->>B: a new context, clean
```

</details>

## 4. A Typo In A Property

![A Typo In A Property](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant E as Environment
    C->>E: getProperty("checkout.curency")
    E-->>C: null, silently
    Note over C,E: an injected @Value fails at start-up instead
```

</details>

