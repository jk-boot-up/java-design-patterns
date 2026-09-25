# Externalised Configuration with Spring Cloud Config Pattern — UML Sequence Diagrams

Four sequences. The stale banner comes first, because it is the headline find and the one thing a program that reads a map on every quote could never show.

## 1. One Refresh, Two Thresholds

The refresh rebuilds the refresh-scoped settings, and the checkout moves to £35.00. The banner copied £50.00 into a field when the shop started, and nothing rebuilds it.

![One refresh, two thresholds](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as operator
    participant P as shop
    participant D as DeliverySettings, RefreshScope
    participant B as PromotionBanner, copied at startup
    O->>P: POST /actuator/refresh
    P->>D: throw away, rebuild on next use
    Note over B: not refresh-scoped, left alone
    O->>P: quote a 48.00 basket
    P->>D: free-over?
    D-->>P: 35.00
    P-->>O: delivery FREE, threshold 35.00
    O->>P: GET /banner
    P->>B: text?
    B-->>P: over 50.00
    P-->>O: Free delivery on orders over 50.00
```

</details>

## 2. Committed, Not In Force

The server reads git on every request, so it serves the new commit at once. The shop fetched its settings when it started, and keeps them until it is told to fetch again.

![Committed, not in force](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant M as Maya in marketing
    participant G as git repository
    participant S as config server
    participant P as shop
    M->>G: commit free-over 35.00
    Note over S: asked, it would answer 35.0, version 64f6a92
    Note over P: does not ask, still quoting against 50.00
    M->>P: POST /actuator/refresh
    P->>S: GET checkout-service
    S-->>P: 35.0
    Note over P: now quoting against 35.00, restarts 0
```

</details>

## 3. A Range Check With Nothing Behind It

The server serves -1, because it checks nothing. The refresh answers 200. The range check runs when the settings object is rebuilt, on the next quote, and fails; there is nothing to fall back to, so every quote fails until a good value is committed.

![A range check with nothing behind it](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant M as Maya in marketing
    participant S as config server
    participant P as shop
    participant C as customer
    M->>S: commit free-over -1, served as -1
    M->>P: POST /actuator/refresh
    P-->>M: 200, changed: delivery.free-over
    C->>P: quote, 5 times
    P->>P: rebuild settings, -1 is below 5.00, refused
    P-->>C: status 500, 5 times out of 5
    M->>S: Sam commits free-over 35.00
    M->>P: POST /actuator/refresh
    C->>P: quote
    P-->>C: delivery FREE, threshold 35.00
```

</details>

## 4. The Server Stops

A running shop keeps what it fetched; only its refresh fails. A new copy must choose: fail fast and refuse to start, or treat the server as optional and start on the default packed inside it.

![The server stops](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as config server, stopped
    participant P as running shop
    participant F as new shop, fail fast
    participant O as new shop, optional
    P->>S: refresh, fetch again
    S--xP: no answer
    Note over P: refresh answers 500, still quoting against 35.00
    F->>S: fetch at startup
    S--xF: no answer
    Note over F: refuses to start
    O->>S: fetch at startup
    S--xO: no answer
    Note over O: starts on its own default, 50.00, with no error
```

</details>
