# Process Manager with Apache Camel, Explained

## The pattern in one sentence

With Camel, a process manager can be a saga: one route runs the journey, each
step names its undo, and Camel calls the undo steps and a final completion or
cancellation route.

## The 5 acts

### 1. Steps hand on to each other

Without a manager, reserve hands on to pay, which hands on to ship. ORD-1 is
shipped. ORD-3's card is declined and the chain stops at payments, but the
kettle reserved for it is never given back: one kettle left of three, though
only one was shipped. And nothing knows where ORD-3 is.

### 2. A saga

Now one route runs each order's journey as a saga. ORD-1 is reserved at the
main warehouse, paid and shipped. When the journey ends well, Camel calls the
completion route, which marks the order DONE.

### 3. A branch

ORD-2 is for a teapot, which the main warehouse has run out of. The reserve
step asks the partner warehouse instead, which has two. Then payment and
shipping go ahead, and the saga completes: DONE.

### 4. Camel runs the undo steps

ORD-3's card is declined. The reserve step had named its compensation, a
release route, so Camel calls it: the kettle goes back to the main warehouse.
Then Camel calls the saga's cancellation route, which marks the order
cancelled and emails the customer. Two kettles of three remain, as they
should.

### 5. The bill

The shop can now say where every order is: two done, one cancelled with its
stock released. The costs: every step that changes something needs an undo
written for it, and an undo is not the same as never having happened. And
the in-memory saga service forgets every journey on a restart; production
needs a durable coordinator.

## The verdict

Use a saga when a journey crosses services that each change something and a
later failure must undo earlier changes. Write an undo for every step, design
for undo not being rewind, and use a durable coordinator in production.

## How to recognise this in code you did not write

- `.saga().completion(...).compensation(...)`.
- Step routes with `propagation(SagaPropagation.MANDATORY)`.
- Routes named release, refund or cancel that undo earlier steps.

## Where you have already met this

- Camel's Saga EIP, with the in-memory service or an LRA coordinator.
- Axon, Temporal and other workflow engines that run long business processes.
- Travel bookings, where a failed step cancels the earlier ones.
