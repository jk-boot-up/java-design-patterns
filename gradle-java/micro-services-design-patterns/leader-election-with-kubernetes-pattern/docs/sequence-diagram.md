# Leader Election with Kubernetes Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Copy A holds the lease and renews it every second. The store asks A for the nightly sales report. A checks that it leads, and it does. It starts building the report. Then A's whole process freezes, every thread at once, the way a long garbage-collection pause freezes a program. A stops renewing. Copy B, which has been reading the lease every second, sees that the last renewal plus five seconds is now behind its own clock. B writes its own name into the lease, and the count of holder changes goes from zero to one. B sends the report with token one, and the inbox accepts it. Now A wakes up. Its elector sees it missed its deadline and says it no longer leads, but A has already checked, and it finishes the report and sends it with token zero. The lease, read at that moment, names B. The inbox has already seen token one, so it refuses token zero. One report reaches the manager.

![Leader Election with Kubernetes sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as copy A
    participant K as API server, Lease
    participant B as copy B
    participant I as manager's inbox
    A->>K: renew: holder A, holder changes 0
    Note over A: asked for the report. checks: I lead. starts building it
    Note over A: frozen. every thread stops, renewals too
    B->>K: read: renew time plus 5 seconds is behind my clock
    B->>K: write: holder B, holder changes 1
    B->>I: report, token 1
    I-->>B: accepted
    Note over A: wakes. elector: deadline missed, stop leading
    A->>I: report, token 0, from the check made before the freeze
    Note over K: at that moment the lease names B
    I-->>A: refused: token 0 is older than 1
```

</details>

The load-bearing sentence: **the lease can tell everyone else that A is no longer the leader, but only the thing A writes to can stop A acting on the old answer.**

For the clean shutdown, the killed leader, the version check and the loser that never rejoins, see [`uml-diagram.md`](uml-diagram.md).
