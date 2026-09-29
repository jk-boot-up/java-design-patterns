# Request-Reply with Correlation Identifier, Explained

## The pattern in one sentence

Request-Reply with a correlation identifier gives each request a unique ID
and a return address, and each reply the ID it answers, so replies are matched
whatever order they arrive in.

## The 5 acts

### 1. Replies matched by order

`InOrderRequester` sends "reserve KETTLE-1 x 5" and then "reserve MUG-1 x 2",
and takes replies in the order they arrive. The mug check is fast and replies
first: "RESERVED 2 x MUG-1" is taken as the kettle's answer. The kettle's
real answer, "REFUSED", because only four exist, is taken as the mug's.

### 2. Correlation IDs

`Requester.send` gives each request a unique ID, WEB-1 and WEB-2, and keeps
it in a waiting table. The inventory service copies the ID into its reply as
the correlation identifier. The mug reply still arrives first, but it names
WEB-2, so each answer goes to the right question.

### 3. Return addresses

A second requester, the phone app, uses the same inventory service. Each
request names its own reply queue as its return address, so the app's teapot
reservation (APP-1) comes back to the app and the web's (WEB-3) to the web.

### 4. Many in flight

Checkout sends twenty requests before a single reply has come back. The
inventory service works on them in parallel and replies in whatever order it
finishes. All twenty are matched to their requests, and none is left waiting.

### 5. The bill

The inventory service's reply to WEB-24 is lost. Checkout waits 500
milliseconds and gives up, but the request is still in the waiting table
until something cleans it up. And checkout cannot tell whether the mug was
reserved or not.

## The verdict

Use it whenever services talk through queues and one needs an answer from
another. Always set an ID, a return address and a timeout, clean up the
waiting table, and design for not knowing the outcome of a lost reply.

## How to recognise this in code you did not write

- `correlationId` and `replyTo` headers on messages.
- A map from request ID to a future or callback.
- Temporary reply queues per requester.

## Where you have already met this

- JMS's `JMSCorrelationID` and `JMSReplyTo` headers.
- RabbitMQ's `correlation_id` and `reply_to` properties.
- Tracking numbers and order references on any reply you receive by email.
