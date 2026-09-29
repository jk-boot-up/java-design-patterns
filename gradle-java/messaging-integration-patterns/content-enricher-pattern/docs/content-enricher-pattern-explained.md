# Content Enricher, Explained

## The pattern in one sentence

A Content Enricher takes a message that is too thin for its receivers, looks the
missing details up once, and passes on a fuller message, so no receiver has to
ask.

## The 5 acts

### 1. The thin message

Checkout only knows the customer by an identifier, so the `OrderPlaced` message
is thin: `ORD-1`, customer `C-17`, one kettle. It is 59 characters long. The
warehouse cannot pack it and the email service cannot greet anyone with it.

### 2. Every receiver looks it up

Without an enricher, the warehouse and the email service each call the customer
service for every order. Three orders make six calls. Worse, both receivers now
depend on that service: switch it off and the warehouse stops packing with
"customer service unavailable", even though the order itself was fine.

### 3. The enricher

`ContentEnricher` sits between checkout and the receivers. For each order it
finds the customer, and builds an `EnrichedOrder` with the name
`Priya Shah`, the address `4 Mill Lane, Leeds` and the tier `GOLD`. The message
grows from 59 to 117 characters. With a small cache, the three orders need only
two lookups, because two orders are from the same customer. Then the customer
service is switched off, and the warehouse and the email service still work:
everything they need is in the message.

### 4. A customer who cannot be found

Order `ORD-4` names customer `C-99`, who is not in the customer service. The
enricher does not pass on a half-filled message with an empty address, which
the warehouse would only discover later. It puts the order on a problem list
with the reason, `ORD-4: no customer C-99`, where a person or a retry can deal
with it.

### 5. The bill

The added details are a copy, taken at one moment. After order one is enriched,
Priya moves to York. The enriched message still says `4 Mill Lane, Leeds`.
Sometimes that is exactly right (the parcel goes where she asked when she
ordered), and sometimes it is a stale copy. And every enriched message is bigger,
for every receiver, whether it needs the details or not.

## The verdict

Use an enricher when several receivers need the same details that the sender
does not have, and when a copy taken at the moment of sending is acceptable.
Send the messages it cannot fill in to a problem list. Leave details that must
be current, such as stock, for the receiver to ask for at the moment it acts.

## How to recognise this in code you did not write

- A step between a sender and receivers that takes an identifier and adds fields.
- Classes named `...Enricher`, or Camel routes using `enrich`.
- Stream joins between an event stream and a table of reference data.
- Receivers with no client for the service that owns the data they read.

## Where you have already met this

- Apache Camel's `enrich` and `pollEnrich`, and Spring Integration's `<int:enricher>`.
- Kafka Streams joining a stream of orders with a table of customers.
- An API gateway adding a user's details to a request after checking their login token.
- Log shippers that add the host name and region to every log line.
