# Recipient List, Explained

## The pattern in one sentence

A recipient list works out, for each message, exactly which destinations need
it, and sends a copy to each of them.

## The 5 acts

### 1. Everything everywhere

Every order is sent to all four warehouses. Five orders make twenty
deliveries, of which only eight are needed; every warehouse sorts through
orders it has nothing to do with.

### 2. A recipient list

`RecipientList` has a table from category to warehouse. For each order it
collects the warehouses for its lines: ORD-1, kitchen and furniture, goes to
north and big-items; ORD-3, chilled, to cold-store. Eight deliveries, exactly
the ones needed.

### 3. Rules add recipients

Rules can add recipients too. Orders over £500 also go to fraud review, so
ORD-4, worth £650, goes to big-items, cold-store and fraud-review. Gift
orders also go to gift wrap, so ORD-2 goes to north and gift-wrap.

### 4. A changed table

North closes for a stocktake, so the table is changed: kitchen items now
come from south. ORD-5 goes to south and cold-store. Checkout, which sends the
orders, was not changed.

### 5. The bill

Big-items is unreachable. ORD-1 is delivered to south but fails for
big-items: half the order is out. The recipient list must retry or undo, and
it must know every destination and its job.

## The verdict

Use a recipient list when each message needs a different set of destinations.
Keep the table and rules in one place, report failed recipients, and decide
how to finish or undo half-sent messages.

## How to recognise this in code you did not write

- `recipientList(...)` in Camel routes.
- Code that builds a list of destinations per message and loops over it.
- Order splitting across several fulfilment centres.

## Where you have already met this

- Apache Camel's `recipientList`.
- Order splitting across fulfilment centres in large shops.
- The To and Cc lines of an email, chosen per message.
