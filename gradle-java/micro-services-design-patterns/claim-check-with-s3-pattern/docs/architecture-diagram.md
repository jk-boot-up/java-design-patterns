# Claim Check with S3 Pattern — Architecture Diagram

Two services, not one. The invoice lives in S3, the ticket travels through SQS, and both are played by LocalStack in one container that the demo starts and stops.

![Claim Check with S3 Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    subgraph Shop["shop process"]
        C["checkout"]
    end
    subgraph Box["LocalStack 4.14.0, one container the demo starts and stops"]
        S3[("S3 bucket invoice-pdfs: the PDF under a random key")]
        Q[("SQS queue invoice-tickets: at most 1048576 bytes a message")]
    end
    subgraph Mail["email service process"]
        E["email sender"]
    end
    C -- "1. store the 1500000-byte PDF" --> S3
    C -- "2. send a 113-byte ticket" --> Q
    Q -- "3. take the ticket" --> E
    E -- "4. fetch by key, check the checksum" --> S3
    E -- "5. delete the object, then the message" --> S3
```

</details>
