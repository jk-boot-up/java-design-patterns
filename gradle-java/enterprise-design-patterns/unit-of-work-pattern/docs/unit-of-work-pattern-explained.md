# Unit of Work, Explained

## The pattern in one sentence

Register what changed, new, dirty and removed, and write it all at commit.

## How it works

`UnitOfWorkPlacement.prepare` changes the domain objects and registers each
change in a `UnitOfWork`. Nothing is written.

```
THREE. The pattern — nothing touches the database until commit.
  after changing every object: 0 database operations, 7 changes registered.
```

`commit` then puts the changes in an order the database accepts, inserts of
parents before children, and applies them inside one short transaction. If a
write is rejected, the transaction rolls back to exactly what was there.

```
FOUR. The same failure, through a unit of work.
  orders: 0, lines: 0, stock: keyboard 10, mouse 10, monitor 10
  all of the order, or none of it.
```

The slow checks happen before the commit, so the database is locked for 7
ticks rather than 22.

## The bill

**Order of writes matters.** Written in the order they were registered, the
lines came before their order, and the foreign key failed. The unit of work
has to work the order out.

```
FIVE. The bill — order of writes matters.
  foreign key: order_lines.order_id=100 has no row in orders
```

**It must know what is dirty.** Either by checking every field or by being
told. This project is told, through `registerDirty`.

**Memory disagrees with the database until commit.**

```
SIX. Memory disagrees with the database until commit.
  in memory, the keyboard has 8 in stock.
  in the database, it still has 10.
```

**The whole change set lives in memory.** A bulk update is a memory problem.

## Where you have already met this

`@Transactional` is a unit of work, and a flush is its commit. The JPA
persistence context tracks what changed and writes it when the transaction
ends, in an order it works out for you.

## When this is too much

For a single write, a unit of work is ceremony. It earns its place when one
business action must write several rows together.
