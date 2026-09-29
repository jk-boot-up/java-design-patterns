# Request-Reply with RabbitMQ, Explained

## The pattern in one sentence

With RabbitMQ, request-reply uses the `replyTo` and `correlationId` properties,
and an expiry so a request nobody waits for is dropped.

## The 5 acts

### 1. Replies taken in arrival order

Checkout asks for five kettles and then two mugs, without correlation IDs,
and takes replies in the order they come back. The inventory service answers
the mug first, from its cache. So the kettle request is paired with the mug
reply, RESERVED 2 x MUG-1, and the mug request with the kettle refusal.

### 2. Correlation IDs

Now each request carries a correlation ID, and the inventory service copies it
onto the reply. The mug reply still comes first, but its ID says it answers
WEB-2. WEB-1, the kettles, is refused; WEB-2, the mugs, is reserved.

### 3. Return addresses

Each request names where its reply should go. The phone app uses RabbitMQ's
direct reply-to, `amq.rabbitmq.reply-to`, which needs no reply queue declared
at all. The web checkout uses its own exclusive, server-named queue. One
inventory service, and each reply goes where its request said.

### 4. Many in flight

Twenty requests are sent before any reply comes back. The inventory service
handles all twenty, and every reply is matched by its correlation ID. None is
left in the requester's waiting table.

### 5. A reply that never comes

The inventory service is busy. WEB-24 waits half a second, gets no reply, and
sits in the waiting table until the requester times it out. Was the mug
reserved? Because the request was sent with a half-second expiry, RabbitMQ
dropped it from the queue: when the service returns, it handles nothing. The
mug was not reserved late behind the requester's back.

## The verdict

Use request-reply over a broker when callers and services are decoupled and
replies may be slow. Always set a correlation ID, time out in the requester,
and give requests an expiry that matches that time-out.

## How to recognise this in code you did not write

- `AMQP.BasicProperties.Builder().replyTo(...).correlationId(...)`.
- `amq.rabbitmq.reply-to` or a server-named exclusive queue.
- A map of waiting requests keyed by correlation ID.

## Where you have already met this

- RabbitMQ RPC tutorials and Spring AMQP's `RabbitTemplate.convertSendAndReceive`.
- JMS `JMSReplyTo` and `JMSCorrelationID`.
- Email threads, where a reply carries a reference to the original.
