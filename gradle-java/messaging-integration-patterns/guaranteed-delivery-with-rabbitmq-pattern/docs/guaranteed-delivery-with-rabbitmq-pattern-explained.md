# Guaranteed Delivery with RabbitMQ, Explained

## The pattern in one sentence

With RabbitMQ, guaranteed delivery takes a durable queue, persistent
messages, publisher confirms and acknowledgements after the work is done.

## The 5 acts

### 1. Durable queue, transient messages

The queue is durable, but the ten emails are sent as not persistent. Before
the restart, ten are waiting. The demo restarts the broker: the queue is
still there, and nothing is in it. A durable queue is not enough; each
message must be marked persistent too.

### 2. Persistent and confirmed

Now each email is sent as persistent, and the sender turns on publisher
confirms: it waits for the broker to say each message is stored on disk.
After the broker restarts, all ten emails are still waiting.

### 3. Acknowledged after sending

The email sender takes messages with manual acknowledgement: it sends each
email, then tells the broker it is done. It sends six and stops; four are
still waiting. A new sender takes the rest: ten of ten sent, each once, and
the queue is empty.

### 4. A crash before the acknowledgement

The sender takes MAIL-11, sends it, and dies before acknowledging. RabbitMQ
sees the connection drop and puts MAIL-11 back on the queue. The next sender
gets it again, marked as redelivered, and the customer receives it twice.
Guaranteed delivery means at least once; the redelivered flag lets a receiver
check before sending again.

### 5. The bill

Every email now waits for a disk write and a confirm from the broker before
checkout moves on. And the broker is one more system to run, back up and
watch; a single node is still a single disk, so production uses replicated
queues across several nodes.

## The verdict

Use all four settings for messages whose loss someone would notice. Expect
duplicates and make receivers able to cope, and replicate queues in
production.

## How to recognise this in code you did not write

- `queueDeclare(name, true, ...)` and `MessageProperties.PERSISTENT_TEXT_PLAIN`.
- `confirmSelect()` and `waitForConfirms...`.
- `basicAck` after the work, and checks of `isRedeliver()`.

## Where you have already met this

- RabbitMQ durable queues, persistent messages, confirms and manual acks.
- Kafka's `acks=all` with replicated partitions.
- Amazon SQS, which keeps a message until it is deleted by the receiver.
