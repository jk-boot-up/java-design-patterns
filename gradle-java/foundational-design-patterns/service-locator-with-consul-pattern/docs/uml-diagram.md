# Service Locator with Consul Pattern — UML Sequence Diagrams

Four sequences.

## 1. Register And Discover

![Register And Discover](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as service instance
    participant K as Consul
    participant C as caller
    S->>K: register name, address, port, TTL check
    S->>K: check passes
    C->>K: healthy instances of payment-gateway?
    K-->>C: the registered, passing ones
```

</details>

## 2. An Instance Fails Its Check

![An Instance Fails Its Check](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as Consul
    participant L as ConsulLocator
    K->>K: gateway-1 check fails
    L->>K: healthy instances?
    K-->>L: gateway-2 only
    Note over L: the caller's code did not change
```

</details>

## 3. A Stale Cache

![A Stale Cache](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant CL as CachingLocator
    participant I as instance
    C->>CL: find, cached
    Note over I: the instance dies
    C->>CL: find
    CL-->>C: the same cached address
    C->>I: call, ConnectException
```

</details>

## 4. Server-Side Discovery

![Server-Side Discovery](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant N as nginx in Docker
    participant A as gateway-2
    participant B as gateway-3
    C->>N: request, the only address it knows
    N->>A: forward, connection refused
    N->>B: retry the next instance
    B-->>C: response, via nginx
```

</details>

