# Sidecar Pattern — UML Sequence Diagrams

Five sequences. The first is the night that went wrong. The second is the same night with
the pattern in place. The last three are the bill: the second thing that can be down, the
extra hop, and the process boundary that is the only real difference between this pattern
and Decorator.

Watch the **boxes** rather than the arrows in every one of these. The boxes are processes,
and this is the one pattern in the course where which process a line of code runs in is the
entire point.

## 1. The Night: Four Copies, Three Updated

Subscription billing is already running, because it is always running at two in the
morning. It reaches the wobbling gateway first, on the policy everybody used before March,
and spends six of the shop's twelve attempts. The three services that *were* updated behave
perfectly and succeed. Marketplace payouts arrives fourth, makes one attempt, and is
refused.

![Sidecar pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Bill as subscription-billing<br/>(6 attempts, 10ms)
    participant Chk as checkout<br/>(3 attempts, 200ms)
    participant Ref as refunds<br/>(3 attempts, 200ms)
    participant Pay as marketplace-payouts<br/>(3 attempts, 200ms)
    participant GW as payment gateway<br/>allowance: 12

    Note over GW: 02:00 — the gateway wobbles for 300ms

    Bill->>GW: charge SUB-90118 (t=0)
    GW-->>Bill: 503 declined (1 of 12)
    Bill->>GW: t=10
    GW-->>Bill: 503 declined (2 of 12)
    Bill->>GW: t=30
    GW-->>Bill: 503 declined (3 of 12)
    Bill->>GW: t=70
    GW-->>Bill: 503 declined (4 of 12)
    Bill->>GW: t=150
    GW-->>Bill: 503 declined (5 of 12)
    Bill->>GW: t=310
    GW-->>Bill: charged (6 of 12)
    Note over Bill: succeeded — dashboard green

    Chk->>GW: charge ORD-4417, 3 attempts
    GW-->>Chk: charged (9 of 12)
    Ref->>GW: charge REF-3820, 3 attempts
    GW-->>Ref: charged (12 of 12)

    Pay->>GW: charge PAY-7741 (t=0)
    GW--xPay: 429 refused — allowance spent
    Note over Pay: the sellers are not paid<br/>every line of this service is correct
```

</details>

The arrow to watch is the last one. It is a cross, not a dash, and it belongs to a service
that did nothing wrong. The six arrows at the top belong to a service that succeeded. **The
failure and the cause are in different lanes**, which is why the incident review on Monday
morning looks at the wrong service for a day and a half.

## 2. The Same Night, With A Proxy Beside Each Service

Every service now sends to `localhost`. The retry loop runs in the proxy, and all four
proxies read one configuration.

![Sidecar Pattern — The Same Night, With A Proxy Beside Each Service](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Bill as subscription-billing
    box rgb(30,41,59) same machine
    participant SC1 as sidecar
    end
    participant Cfg as SidecarConfig<br/>maxAttempts=3, backoff=200ms
    participant GW as payment gateway<br/>allowance: 12

    Note over SC1,Cfg: read once, at start-up
    Cfg-->>SC1: 3 attempts, 200ms, TLS1.3

    Note over GW: 02:00 — the same 300ms wobble

    Bill->>SC1: send SUB-90118
    SC1->>GW: attempt 1 (t=1)
    GW-->>SC1: 503 declined
    SC1->>GW: attempt 2 (t=202)
    GW-->>SC1: 503 declined
    SC1->>GW: attempt 3 (t=603)
    GW-->>SC1: charged
    SC1-->>Bill: receipt, 3 attempts

    Note over Bill: the service never knew<br/>there was more than one attempt

    Note over GW: checkout, refunds and payouts<br/>do exactly the same: 3 each<br/>12 of 12 used, 0 refused
```

</details>

Two things to notice, and neither of them is the happy ending.

The first is that **`Bill` sends one arrow and receives one arrow.** Everything between
them happened in a process it cannot see. The service did not become more careful; it
became ignorant, deliberately.

The second is that the arrow from `Cfg` happens **once, at start-up**, and it is the same
arrow for all four proxies. That is the difference between four copies and one statement,
drawn.

## 3. The Bill, Part One: The Proxy Is Down

![Sidecar Pattern — The Bill, Part One: The Proxy Is Down](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Chk as checkout
    box rgb(76,29,29) same machine
    participant SC as sidecar (not running)
    end
    participant GW as payment gateway<br/>(perfectly healthy)

    Note over GW: nothing is wrong out here

    Chk->>SC: send ORD-4418
    SC--xChk: connection refused to localhost

    Note over Chk: no retry code left — we deleted it<br/>attempts that reached the gateway: 0

    Chk->>SC: send ORD-4419
    SC--xChk: connection refused to localhost
    Chk->>SC: send ORD-4420
    SC--xChk: connection refused to localhost
```

</details>

There is no arrow to the gateway on this diagram at all. That empty right-hand side is the
cost: the request never left the machine, and the service has nothing left to fall back on
because the fallback was the thing we moved out.

Three requests, three identical failures. **When a sidecar goes, it does not take one call
with it — it takes every call that service makes.** The failure is not smaller than the
network's, it is rarer and wider.

## 4. The Bill, Part Two: The Hop

![Sidecar Pattern — The Bill, Part Two: The Hop](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Chk as checkout
    participant SC as sidecar
    participant GW as payment gateway

    Note over Chk,GW: retry code inside the service — 600ms

    Note over Chk,GW: retry code in the proxy — 603ms

    Chk->>SC: +1ms
    SC->>GW: attempt 1
    GW-->>SC: 503
    SC->>SC: wait 200ms
    Chk->>SC: +1ms
    SC->>GW: attempt 2
    GW-->>SC: 503
    SC->>SC: wait 400ms
    Chk->>SC: +1ms
    SC->>GW: attempt 3
    GW-->>SC: charged
    SC-->>Chk: receipt
```

</details>

One millisecond per attempt, three milliseconds on this call. On a payment that already
takes six hundred, that is nothing. On an internal call that takes two milliseconds it is a
fifty per cent increase — and in a system where every service talks through a proxy, every
hop between two services is paid twice: once leaving one and once entering the next.

**That is the arithmetic that decides whether a service mesh belongs in your system.** It
is arithmetic, not taste.

## 5. The Only Difference From Decorator

![Sidecar Pattern — The Only Difference From Decorator](images/uml-diagram-5.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App as service code

    box rgb(30,58,95) one process, one jar, one language
    participant Dec as RetryingDecorator
    end
    participant GW1 as payment gateway

    App->>Dec: pay(payment)
    Dec->>GW1: charge
    GW1-->>Dec: charged
    Dec-->>App: receipt
    Note over App,Dec: change the policy → rebuild,<br/>retest and redeploy the service

    participant App2 as service code
    box rgb(30,58,95) process A
    participant Svc as (nothing but the call)
    end
    box rgb(120,53,15) process B — any language
    participant SC as sidecar
    end
    participant GW2 as payment gateway

    App2->>SC: pay → localhost
    SC->>GW2: charge
    GW2-->>SC: charged
    SC-->>App2: receipt
    Note over App2,SC: change the policy → restart the proxy<br/>the service is not opened
```

</details>

The arrows are the same shape in both halves. The boxes are not.

That is the honest summary of this pattern: **the structure is Decorator, the decision is
about deployment.** Everything you gain and everything you pay comes from the second box
being a different process — the policy change that does not touch the service, the extra
thing that can be down, and the millisecond on every call.

So the question is never "wrapper or no wrapper". It is: does this concern need to change
without rebuilding the service, or apply to a service written in a language your library
does not support? Yes to either, and it goes next door. No to both, and the top half of
this diagram is cheaper, faster and has one fewer thing that can fail.
