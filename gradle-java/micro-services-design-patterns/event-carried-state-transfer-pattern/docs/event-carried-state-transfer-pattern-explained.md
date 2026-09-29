# Event-Carried State Transfer, Explained

## The pattern in one sentence

Event-Carried State Transfer puts the changed data in the event, so listeners
keep their own copies and never call the owner back.

## The 5 acts

### 1. A thin event, and a call back

The customer service publishes a thin event that only says a customer
changed. The shipping service keeps nothing, so for every label it calls the
customer service for the address. A hundred labels mean a hundred calls. When
the customer service is down, not a single label can be printed.

### 2. The event carries the address

Now each event carries the new address. Shipping keeps its own copy of the
ten addresses it has heard about. A hundred labels need no calls at all, and
when the customer service goes down, all hundred labels are still printed.

### 3. The copy lags behind

Customer C1 moves from Leeds to York. The event is still on its way when
shipping prints a label, so the label goes to the old address in Leeds. Once
the event arrives, labels go to York. The copy is always a little behind the
owner: this is eventual consistency.

### 4. Events out of order

Customer C2 moves to Hull, then to Bristol, but the two events arrive in the
wrong order. A copy that simply takes the last event it received ends up
with Hull, the older address. Each event carries a version number, and a copy
that ignores anything older than what it holds keeps Bristol.

### 5. The bill

Every service that cares keeps its own copy. Shipping, invoicing and
marketing each hold every customer's address. Events are bigger, copies are
briefly stale, and personal data now lives in many places, each of which must
protect it and delete it when asked.

## The verdict

Carry state in events when many services read the data often and must keep
working when its owner is down. Include a version, accept brief staleness,
copy only the fields each service needs, and remember every copy is data to
protect.

## How to recognise this in code you did not write

- Events named `...Changed` carrying full records.
- A service's own table of another service's data, filled by a listener.
- Compacted Kafka topics used as the source of a local copy.

## Where you have already met this

- Kafka topics carrying full records, often compacted to the latest per key.
- Change data capture, such as Debezium, publishing row changes.
- Read models in [CQRS](../cqrs-pattern), built from events.
