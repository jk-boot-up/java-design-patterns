# Leader Election with Kubernetes Pattern — UML Sequence Diagrams

Four sequences. The frozen leader comes first, because it is the one thing a lease inside one program could never really show.

## 1. Two Who Think They Lead

A checks that it leads, then freezes. B takes the lease. A wakes and sends anyway. With no token check, both reports arrive.

![Two who think they lead](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as copy A
    participant K as Lease
    participant B as copy B
    participant I as inbox, no check
    Note over A: checks: I lead. starts the report
    Note over A: frozen with the stop signal
    B->>K: last renewal plus 5 seconds has passed
    B->>K: holder B, holder changes 1
    B->>I: report
    Note over A: woken with the continue signal
    A->>I: report, from the old check
    Note over I: sent by B, A
    Note over K: holder B, renewed after A's last renewal
```

</details>

## 2. Two Writes From One Version

Two writers read the lease at the same version and both try to put their own name in it. The API server takes the first and refuses the second.

![Two writes from one version](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant W1 as first writer
    participant K as API server
    participant W2 as second writer
    W1->>K: read the lease, version v
    W2->>K: read the lease, version v
    W1->>K: holder B, based on version v
    K-->>W1: accepted, now version v plus 1
    W2->>K: holder C, based on version v
    K-->>W2: 409 Conflict
```

</details>

## 3. Stopped Cleanly, Then Killed

A is shut down cleanly and hands the lease back; a copy takes it at its next check. That copy is then killed outright; the last copy waits out the whole lease.

![Stopped cleanly, then killed](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as copy A
    participant K as Lease
    participant N as new leader, B or C
    participant L as last copy
    A->>K: shutting down: clear the holder
    N->>K: lease is empty, take it
    Note over N,K: within a couple of seconds
    Note over N: killed outright, hands nothing back
    L->>K: holder still the dead copy, not run out yet
    L->>K: run out by my clock, take it
    Note over L,K: about one whole 5-second lease
```

</details>

## 4. The Loser Never Rejoins

After losing the lease, A's elector has stopped for good. B is killed. The lease stays expired, naming B, for two whole leases. Only a new elector brings A back.

![The loser never rejoins](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as copy A, lost earlier
    participant K as Lease
    participant B as copy B
    Note over A: elector stopped when the lease was lost
    Note over B: killed
    Note over K: holder B, two whole leases old, nobody leads
    A->>A: start a new elector
    A->>K: run out, take it: holder A, holder changes 2
```

</details>
