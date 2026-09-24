# Claim Check with S3 Pattern — UML Sequence Diagrams

Four sequences. The delete that deletes nothing comes first, because it is the one thing the hand-built version could never show.

## 1. A Delete That Deletes Nothing

A bucket that keeps every version. The same key is stored twice, and the ticket names the first version, so it gets the first invoice back. Then the email service deletes the key as it always does. A listing shows no keys, but both versions are still stored, behind one delete marker.

![A delete that deletes nothing](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant S as versioned S3 bucket
    participant E as email service
    C->>S: PutObject invoices/ORD-1042.pdf, first invoice
    S-->>C: version one
    C->>S: PutObject same key, corrected invoice
    S-->>C: version two
    E->>S: GetObject, key and version one
    S-->>E: the first invoice, identical true
    E->>S: DeleteObject by key only
    Note over S,E: keys listed 0, versions still stored 2, delete markers 1
    E->>S: DeleteObject each version by its id
    Note over S: 0 stored
```

</details>

## 2. Too Big For The Queue

The whole PDF, as base64 text, sent to SQS. The service refuses it with its own words. The edge is three quarters of the limit.

![Too big for the queue](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant Q as SQS queue
    C->>Q: GetQueueAttributes
    Q-->>C: MaximumMessageSize 1048576
    C->>Q: SendMessage, 1500000-byte PDF as 2000000 characters
    Q-->>C: refused, Message must be shorter than 1048576 bytes
    C->>Q: SendMessage, 786432-byte PDF as 1048576 characters
    Q-->>C: accepted
    C->>Q: SendMessage, 786433-byte PDF as 1048580 characters
    Q-->>C: refused
```

</details>

## 3. The Same Key, Twice

A bucket keyed by order number, with no versions kept. The corrected invoice replaces the first, and the checksum on the first ticket catches it.

![The same key, twice](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant S as S3 bucket
    participant Q as SQS queue
    participant E as email service
    C->>S: PutObject invoices/ORD-1042.pdf, first invoice
    C->>Q: ticket one, checksum of the first
    C->>S: PutObject same key, corrected invoice
    Note over S: S3 keeps 1 object, the corrected one
    C->>Q: ticket two
    E->>Q: take ticket one
    E->>S: GetObject by key
    S-->>E: the corrected invoice
    Note over E: the checksum does not match, refuse, delete nothing
```

</details>

## 4. The Ticket Outlives Its Luggage

The bucket removes invoices one day after they are stored; the queue keeps an untaken ticket for 345600 seconds, which is four days. The demo removes the invoice the way the rule would.

![The ticket outlives its luggage](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant S as S3 bucket with a 1-day rule
    participant Q as SQS queue
    participant E as slow email service
    C->>S: PutObject
    S-->>C: stamped to expire at a midnight UTC, 24 to 48 hours away
    C->>Q: SendMessage, the ticket
    Note over Q: keeps it for 345600 seconds
    S-->>S: the rule removes the invoice
    Note over Q: tickets still waiting 1
    E->>Q: take the ticket
    E->>S: GetObject by key
    S-->>E: NoSuchKey, The specified key does not exist
```

</details>
