# Pessimistic Offline Lock, Explained

## The pattern in one sentence

A pessimistic offline lock makes a person take a lock on a record before editing it, so nobody else can edit it until the lock is released.

## The six acts

### Lock First, Then Edit

Clerk A takes the lock. Clerk B asks and is refused, told that A holds it. B never starts an edit that could be lost.

```
  clerk A asks for MUG-BLUE: got the lock.
  clerk B asks for MUG-BLUE: refused, MUG-BLUE is locked by A.
  the clash was stopped before B could start editing.
```

### No Lost Update

A raises the price and lets go. B then takes the lock, reads the new price, and saves the stock count on top of it. Nothing is overwritten.

```
  A raised the price and let go. B then locks and reads: price 1200, stock 50.
  B saves the stock count: Product[sku=MUG-BLUE, pricePence=1200, stock=40]. nothing was overwritten.
```

### The Bill: Waiting

While A edits, B tries once a minute and is refused three times, and has done nothing useful in that time.

```
  B tries once a minute while A edits: 3 refusals, and B has done nothing useful.
  a lock trades lost updates for waiting.
```

### The Bill: A Lock Nobody Let Go Of

A goes to lunch without letting go. B is refused at once, and again after ten minutes. After sixteen minutes the lock expires and B gets it. When A comes back, A's save is refused, because A no longer holds the lock.

```
  A goes to lunch without letting go. B, straight away: refused, MUG-BLUE is locked by A.
  after 10 minutes: refused, MUG-BLUE is locked by A.
  after 16 minutes the lock has expired: got the lock.
  A comes back and saves: A does not hold the lock on MUG-BLUE, so the write is refused.
```

### The Bill: Each Waiting For The Other

A holds the mug and needs the tea. B holds the tea and needs the mug. Neither can move. If everyone takes locks in the same order, one gets both, and the other holds nothing and simply waits.

```
  A holds MUG-BLUE and now needs TEA-050: refused, TEA-050 is locked by B.
  B holds TEA-050 and now needs MUG-BLUE: refused, MUG-BLUE is locked by A.
  neither can move. that is a deadlock, and it lasts until a lock expires.
  taking locks in a fixed order, A took both.
  taking locks in a fixed order, B stopped at MUG-BLUE holding nothing else.
```

### How Much To Lock

One lock on the whole catalogue stops B editing a different product. A lock per product lets both work. Smaller locks mean less waiting, and more locks to forget or deadlock on.

```
  one lock on the whole catalogue: A got the lock. B, editing a different product: refused, catalogue is locked by A.
  a lock per product: A got the lock. B on TEA-050: got the lock.
  the smaller the thing locked, the fewer people wait. the more things locked, the more there is to forget and to deadlock on.
```

## The verdict

Use a pessimistic lock when a conflict would throw away a lot of work, when edits are long, and when it is acceptable that people sometimes wait. Lock the smallest thing that keeps the data safe, always give a lock an expiry, take locks in a fixed order, and refuse a write from anyone who no longer holds the lock. Use an optimistic lock where clashes are rare and retrying is cheap.

## How to recognise this in code you did not write

- A `lock` or `checkout` step before an edit, and an `unlock` or `checkin` after.
- A locks table or a `locked_by` and `locked_until` column.
- `SELECT ... FOR UPDATE` held across a long session, which is a warning sign.
- A message such as 'this record is being edited by someone else'.

## Where you have already met this

Document editors that say who has a file checked out, and ticket systems that warn that someone else is editing.

## When this is too much

Where conflicts are rare and edits short, a lock is waiting and bookkeeping for nothing. A long database lock held across a user's thinking time is almost always a mistake.
