# Leader Election with Kubernetes Pattern — Data Flow Diagram

How one copy decides, every second or so, whether it leads. Note where the clock is read: in the copy, never in the API server.

![Leader Election with Kubernetes Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    Start(["the elector wakes, every 1 to 2 seconds"])
    Read["read the Lease from the API server"]
    None{"is there a lease?"}
    Create["create it with my name: holder changes 0"]
    Mine{"is my name in it?"}
    Renew["write it again with a fresh renew time"]
    Deadline{"4 seconds since my last good renewal?"}
    Stop(["stop leading, and never ask again"])
    Fresh{"renew time plus 5 seconds, still ahead of MY clock?"}
    Wait(["the other copy leads; wait"])
    Take["write my name, holder changes plus one"]
    Version{"was the lease rewritten since I read it?"}
    Refused(["409 Conflict: someone else got there first"])
    Lead(["I lead; my token is the holder changes"])
    Start --> Read --> None
    None -- no --> Create --> Lead
    None -- yes --> Mine
    Mine -- yes --> Deadline
    Deadline -- yes --> Stop
    Deadline -- no --> Renew --> Version
    Mine -- no --> Fresh
    Fresh -- yes --> Wait
    Fresh -- "no, it ran out" --> Take --> Version
    Version -- yes --> Refused
    Version -- no --> Lead
```

</details>
