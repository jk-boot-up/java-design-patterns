# Cell-Based Architecture, Explained

## The pattern in one sentence

Cell-based architecture runs several complete, independent copies of a
system, each serving a fixed share of customers behind a thin router, so
failures and releases only reach one cell at a time.

## The 5 acts

### 1. One shared stack

Every customer is served by the same stack. A release with a checkout bug
goes out, and every one of the thirty customers fails to check out until it is
rolled back.

### 2. Cells

The shop now runs as three cells, each a complete copy of the back end. The
`CellRouter` places the thirty customers evenly, ten per cell, and sends each
customer's requests to their cell: C-1 to cell-1, C-2 to cell-2. Everyone
checks out.

### 3. A small blast radius

The same buggy release goes to cell-1 only. Its ten customers cannot check
out; the other twenty can. The release is rolled back in cell-1, failures drop
to zero, and cells 2 and 3 never noticed anything.

### 4. Add a cell

The shop grows. Instead of enlarging the existing cells, a fourth cell is
added and the router places new customers there. Six newcomers go to cell-4;
C-1 is still in cell-1, and no existing customer was moved.

### 5. The bill

Every cell is a separate world. A question about all customers, such as
today's total sales, means asking all four cells and adding up: £1,760.00. And
there are now four copies of every service and database to run, watch and
pay for.

## The verdict

Use cells for large systems where limiting the blast radius of failures and
releases is worth running many copies. Keep the router thin, release one cell
at a time, and plan how cross-cell questions and customer moves will work.

## How to recognise this in code you did not write

- Customers or tenants assigned to a numbered pod, shard, stamp or cell.
- A routing layer that looks up a customer's home before forwarding.
- Deployments that go cell by cell.

## Where you have already met this

- AWS's cell-based architecture guidance, used in services such as DynamoDB.
- Slack's and Salesforce's "pods" and "cells", each serving a set of customers.
- Staged rollouts that release to one region or one cell first.
