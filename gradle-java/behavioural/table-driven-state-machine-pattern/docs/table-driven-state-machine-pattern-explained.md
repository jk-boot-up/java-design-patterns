# Table-Driven State Machine, Explained

## The pattern in one sentence

A table-driven state machine keeps every allowed move, from a status on an
action to a new status, in one table, and refuses every move that is not in it.

## The 5 acts

### 1. Rules in if statements

`IfElseOrder` has one method per action, each with its own check. `cancel` only
refuses a shipped order, so a delivered order is cancelled without complaint.
`refund` only refuses an order that was never paid, so the same order is
refunded twice and £63.44 is paid out twice. Each method looks fine on its
own; the missing checks are invisible.

### 2. The table

`TransitionTable.orders()` holds every allowed move: from PLACED, pay goes to
PAID and cancel to CANCELLED; from PAID, ship goes to SHIPPED and refund to
REFUNDED; from SHIPPED, deliver goes to DELIVERED. `Order.apply` looks the move
up and nothing else. `ORD-1` is paid, shipped and delivered.

### 3. Wrong moves refused

The same two mistakes are tried again. Cancel on a delivered order is not in
the table, so it is refused: "cannot cancel a DELIVERED order". A second refund
is refused: "cannot refund a REFUNDED order". And because the table knows the
allowed moves, it can tell a page which buttons to show: for a paid order,
ship and refund.

### 4. A new rule

The shop starts accepting returns. Two rows are added: from DELIVERED, return
goes to RETURNED; from RETURNED, refund goes to REFUNDED. No method changes.
A delivered order now shows one button, return, and `ORD-1` is returned and
refunded.

### 5. The bill

Seven statuses and six actions make 42 cells, of which only seven are allowed
moves: a bigger shop's table can be hard to read, so draw it as a diagram. And
the table only says where an order may go. Paying the refund, restocking the
item and emailing the customer are still code, attached to each move.

## The verdict

Use a table whenever something has a handful of statuses and rules about which
can follow which: orders, payments, tickets, bookings. Keep the table in one
place, generate a diagram from it, attach side effects to moves, and let the
table tell the page which buttons to show.

## How to recognise this in code you did not write

- An enum of statuses and a map from (status, action) to status.
- Errors like "cannot ship a PLACED order".
- A `transitions` or `workflow` configuration file.
- A diagram of boxes and arrows in the documentation for an entity's status.

## Where you have already met this

- Spring State Machine and similar libraries configure transitions as a table.
- Workflow and ticket systems such as Jira, where an admin edits the allowed transitions.
- Order, payment and shipment statuses in almost every shop.
- Parsers and network protocols, which are built on state tables.
