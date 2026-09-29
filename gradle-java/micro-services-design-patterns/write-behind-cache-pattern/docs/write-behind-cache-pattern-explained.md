# Write-Behind Cache, Explained

## The pattern in one sentence

A write-behind cache answers every change from memory at once and saves the
changed records to the database later, in batches, one write per record.

## The 5 acts

### 1. Write every change

`WriteThroughStore` saves every change to the database before answering. Three
customers each change their cart ten times: thirty database writes, and each
customer waits twenty milliseconds on every click, six hundred in total. Most
of those writes are overwritten a moment later by the next change to the same
cart.

### 2. Write behind

`WriteBehindStore` changes the cart in memory and marks it as changed, or
dirty. The customer gets an answer at once. After five seconds, `flush` writes
each dirty cart once: three writes instead of thirty, each holding the latest
contents. Priya's cart arrives in the database as ten mugs and nine teas, her
final choice.

### 3. The database goes down

The database goes down. Customers keep changing their carts, because changes
only touch memory. The flush fails, and the two changed carts stay dirty. When
the database comes back, the next flush writes both. The customers never
noticed.

### 4. A crash before the flush

Priya adds a teapot and raises her mugs to twelve; Ana changes her tea. The
flush is five seconds away when the server crashes. Memory is gone, and so are
all three changes: the database still holds the carts from the last flush.
This is the price of write-behind, and why it is only for data you can afford
to lose.

### 5. The bill

Priya's kettle count goes from one to three in memory. Checkout, reading the
cache, sees three. A stock report that reads the database directly still sees
one, until the next flush. So everything that must be right, and everything
another system reads from the database, stays out of write-behind: orders,
payments and stock.

## The verdict

Use it for data that changes often, is read mostly through the same service,
and can be lost without harm: carts, counters, drafts, last-seen times. Flush
often, flush on shutdown, retry when the database is down. Never use it for
orders, payments, stock, or anything another system reads from the database.

## How to recognise this in code you did not write

- A `dirty` set or flag next to a cache.
- A scheduled `flush`, `persist` or `sync` job.
- Cache settings named `write-behind`, `write-back` or `write-delay`.
- Batch updates that write the latest value of many records at once.

## Where you have already met this

- Operating systems keep file writes in memory and flush them to disk a little later.
- Redis, Hazelcast and Ehcache offer write-behind to a backing database.
- Autosave in editors and web forms.
- Counters such as page views, collected in memory and saved in batches.
