# Lazy Load with Hibernate Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The page asks for the orders, and Hibernate loads them, leaving each order's customer as a proxy that holds only an id. The session then closes. Later the page asks a proxy for the customer's name. The proxy needs to select the customer, and it needs the session to do it. The session is gone, so it throws the lazy initialization exception. It fails where it was used, not where it was loaded.

![Lazy Load with Hibernate pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Page
    participant S as Session
    participant P as Customer proxy
    Page->>S: load the orders
    S-->>Page: orders, customers are proxies
    Page->>S: close
    Page->>P: name()
    P->>S: I need to select the customer
    S-->>Page: LazyInitializationException, no session
```

</details>

The load-bearing sentence: **the exception comes from where it was used, not from where it was loaded.**
