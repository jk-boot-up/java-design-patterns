# Aggregate, Explained

## The pattern in one sentence

An aggregate is a cluster of objects treated as one unit, with a single root that is the only way in, so its rules can never be broken from outside.

## The six acts

### A Loose Order

With a public list, a line of minus three mugs goes in, the same machine goes on two lines, the total passes six thousand pounds, and a line is added after the order was placed.

```
  a line of -3 mugs: in. the same machine on two lines: in. total: £5988.50, past the £1000 limit: in.
  a line added to an order already placed: in.
  every rule is true in the head of the person who wrote the caller.
```

### The Root Guards The Rules

Every operation goes through the root. Nought and eleven mugs are refused, a second batch that would make eleven is refused, a total over a thousand pounds is refused, a change after placing is refused, and an empty order cannot be placed.

```
  0 mugs:            refused, a line has between 1 and 10 of an item
  11 mugs:           refused, a line has between 1 and 10 of an item
  6 mugs:            accepted. 5 more of the same: refused, a line has between 1 and 10 of an item
  two more machines: refused, the order total may not pass £1000.00.
  after place():     refused, a placed order cannot change
  an empty order:    refused, an order cannot be placed empty
```

### There Is Only One Door

The list of lines seen from outside is read-only, and a line has no public constructor, so no line exists that the order has not checked.

```
  order.lines().clear(): UnsupportedOperationException.
  an OrderLine has no public constructor, so none can exist that the order has not checked.
  lines seen from outside: 1, total £16.00.
```

### Other Aggregates By Id

Three orders that hold the whole customer load the customer three times. Three that hold only an id load none.

```
  three orders that hold the whole customer: 3 customer loads.
  three orders that hold only a CustomerId: 0 customer loads.
```

### Saved Whole, Or Not At All

Two clerks read the same order and each add a line. The first save is accepted. The second is refused, because the order changed since it was read.

```
  clerk A adds beans and saves: accepted.
  clerk B adds tea and saves: ORD-5 was changed by someone else since it was read.
  the order was read whole, changed whole and saved whole, so a half-updated order cannot exist.
```

### An Aggregate Drawn Too Big

If one aggregate holds the customer and all their orders, two clerks changing different orders collide. With one aggregate per order, both saves are accepted.

```
  one aggregate holding the customer and all their orders. two clerks change two different orders.
  the second save: refused, changed by someone else.
  one aggregate per order: both saves accepted.
  the boundary is a choice, and a boundary drawn too wide costs you false conflicts.
```

## The verdict

Draw the aggregate around what must be consistent together, and no wider. Make one class the root and the only way in. Keep the rules in it. Refer to other aggregates by id. Save and load the whole thing. When two things can change independently, they are two aggregates.

## How to recognise this in code you did not write

- A class with private collections and methods that add to them.
- A read-only view returned instead of the list itself.
- A repository that saves an `Order`, and never an `OrderLine`.
- Ids of other aggregates held instead of the objects.

## Where you have already met this

Every well-designed `Order` class. Frameworks name it too: Axon's `@Aggregate`, and Spring Data's `@AggregateRoot`, for one.

## When this is too much

For a plain record with no rules across its parts, a single class is enough. An aggregate earns its place when rules span several objects.
