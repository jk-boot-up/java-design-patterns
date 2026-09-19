# Claim Check Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The sender puts the invoice in storage and gets an identifier. It builds a claim from the identifier, the size and a checksum of the invoice, and sends only the claim through the broker. The receiver takes the claim, fetches the invoice from storage by its identifier, checks that its checksum matches, uses it, and deletes it.

![Claim Check pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as sender
    participant B as blob storage
    participant Q as broker
    participant R as receiver
    S->>B: put(invoice)
    B-->>S: id
    S->>Q: claim(id, size, checksum)
    R->>Q: receive
    Q-->>R: claim
    R->>B: get(id)
    B-->>R: invoice
    R->>R: check the checksum
    R->>B: delete(id)
```

</details>

The load-bearing sentence: **the broker only ever sees the ticket.**
