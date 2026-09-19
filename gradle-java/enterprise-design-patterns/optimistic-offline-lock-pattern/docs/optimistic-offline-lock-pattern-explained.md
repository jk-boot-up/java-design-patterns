# Optimistic Offline Lock, Explained

## The pattern in one sentence

An optimistic offline lock lets people edit without locking anything, and detects a clash at save time by checking that the row has not changed since it was read.

## The six acts

### No Lock: The Last Write Wins

Both clerks read the same row. Clerk A saves a new price. Clerk B saves the stock count, and writes the whole row, with the old price. The price change is gone, with no error.

```
  clerk A raises the price to 12.00 and saves. clerk B counts 40 in stock and saves.
  the row now: price £10.00, stock 40. clerk A's price has vanished, and no error was raised.
```

### A Version On Every Row

Clerk A saves and the row moves to version two. Clerk B's save, made against version one, is refused, and the price of twelve pounds survives.

```
  clerk A saves: accepted. the row is now at version 2.
  clerk B saves: MUG-BLUE was changed by someone else since you read it.
  the row still says: price £12.00, stock 50.
```

### Reload, Reapply, Save

Clerk B reloads the row, sees the new price, reapplies the stock count and saves. It takes two attempts, and both changes survive.

```
  clerk B is refused, reloads, reapplies the stock count, and saves after 2 attempts.
  the row: price £12.00, stock 40. both changes survived.
```

### The Version Is Per Row

One clerk changed the price and another the stock. Different fields, but the second save is refused, because the version is per row. A finer version would let both through, at more cost.

```
  one clerk changed the price and another changed the stock. different fields. second save refused: true.
  a conflict that was not one. a finer version, per field, would have let both through, at the price of more bookkeeping.
```

### The Bill: A Busy Row

Ten clerks add one to the same row. Nothing is lost and the stock is ten, but nineteen saves were attempted and nine refused, so nine of the ten did their work twice.

```
  10 clerks each add one to the stock of the same product, all having read it at the start.
  final stock: 10. saves attempted: 19. saves refused: 9.
  nothing was lost, and a row that everyone wants is a row where most of the work is repeated.
```

### The Bill: You Find Out At The End

A user makes five changes over a long session, and on saving is told the row changed. All five changes are discarded, and the user learns it only now.

```
  a user makes 5 changes over a long session. on save: MUG-BLUE was changed by someone else since you read it.
  all 5 changes are discarded, and the user learns it only now. the cost of a conflict is paid when it is found.
```

## The verdict

Use an optimistic lock when conflicts are rare, edits are short, and it is cheap to try again: most web applications. Keep the version in the row, check it in the update, retry by reloading, and tell the user honestly when their change cannot be applied. Use a pessimistic lock when a conflict is expensive, or a session is long.

## How to recognise this in code you did not write

- A `version` column, and `WHERE id = ? AND version = ?` in an update.
- `@Version` in JPA and Hibernate.
- An `OptimisticLockException` or an HTTP 409 or 412 in the API.
- `If-Match` and ETag headers on a web request.

## Where you have already met this

JPA's `@Version`, HTTP's `ETag` and `If-Match`, and every database that offers compare-and-set.

## When this is too much

Where conflicts are frequent and costly, retrying wastes work and a lock is kinder. Where only one writer exists, a version is pure overhead.
