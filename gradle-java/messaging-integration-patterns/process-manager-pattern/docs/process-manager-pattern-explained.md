# Process Manager, Explained

## The pattern in one sentence

A process manager keeps each instance of a multi-step process, sends it to
the next step, and decides what to do after every reply, including undoing
work when a step fails.

## The 5 acts

### 1. Steps chained together

`Chained.fulfil` reserves, charges and ships in a line, each step handing on
to the next. ORD-1 ships. ORD-3's card is declined, so the chain stops at
payments, but the kettle it reserved is never released: stock shows 1 of 3
although only one kettle was shipped. And nothing records where ORD-3 is.

### 2. A process manager

`ProcessManager` starts each order and handles every reply. For ORD-1 it
asks the main warehouse to reserve, gets RESERVED, asks payments, gets PAID,
asks shipping, gets SHIPPED, and marks the order DONE. The services never
talk to each other.

### 3. A branch

ORD-2 is a sofa. The main warehouse replies OUT_OF_STOCK, so the manager
decides the next step is the partner warehouse. It replies RESERVED, and the
order is paid and shipped.

### 4. The unhappy path

ORD-3's card is declined. The manager knows the order reserved a kettle at
the main warehouse, so it releases it, emails the customer, and marks the
order cancelled. Stock is back to 2 of 3.

### 5. The bill

The manager can answer "where is every order?" in one line. But every route
and branch lives in one class that grows with each new step, and its state is
in memory: a restart would forget every order in progress. Real process
managers keep their state in a database.

## The verdict

Use a process manager when routes branch and failures must be undone. Store
its state, keep each step's service unaware of the others, and use a workflow
engine when processes are long or many.

## How to recognise this in code you did not write

- A class or service with a state per order and a handler per reply type.
- Workflow definitions in Camunda, Temporal or Step Functions.
- Compensating actions (release, refund) triggered centrally.

## Where you have already met this

- Workflow engines such as Camunda, Temporal and AWS Step Functions.
- Orchestrated sagas in microservices.
- Order management systems that track every order's status.
