# Guaranteed Delivery, Explained

## The pattern in one sentence

Guaranteed delivery stores each message durably before accepting it and
acknowledges it after delivery, so after a crash every unacknowledged message
is delivered again.

## The 5 acts

### 1. Only in memory

`MemoryQueue` holds ten confirmation emails because the email provider is
slow. The server restarts for an update, and a new, empty queue takes its
place: zero emails waiting. Ten customers never receive their confirmation.

### 2. Written to disk first

`Journal.send` appends each message to a file and forces it to the disk
before returning. Ten emails give a journal of ten lines. After a restart, a
new `Journal` on the same file finds all ten waiting.

### 3. Acknowledgements

Each email that is delivered gets an acknowledgement line in the journal. Six
are sent and acknowledged, then the server crashes. After the restart, only
MAIL-7 to MAIL-10 are waiting; they are sent, and all ten customers receive
exactly one email.

### 4. At least once

MAIL-11 is sent, and the server crashes before the acknowledgement is
written. After the restart the journal cannot know it was sent, so it sends it
again. The customer receives two emails. Guaranteed delivery means at least
once, not exactly once.

### 5. The bill

Every message waits for a forced disk write before it is accepted, and every
delivery writes another: ten emails cost ten writes to accept and ten to
acknowledge. The journal grows until acknowledged lines are trimmed, and
receivers must cope with duplicates.

## The verdict

Use guaranteed delivery for messages that must not be lost. Expect duplicates
and make receivers idempotent, trim what has been acknowledged, and leave it
off for messages that are cheap to lose.

## How to recognise this in code you did not write

- Durable queues and persistent delivery modes.
- Append-only logs with acknowledgement or offset records.
- `fsync` or `force(true)` before replying "accepted".

## Where you have already met this

- Persistent messages in JMS, RabbitMQ durable queues, and Kafka's replicated logs.
- Transactional outboxes that store messages in the database first.
- Recorded and signed-for post.
