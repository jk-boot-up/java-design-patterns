# Transaction Script, Explained

## The pattern in one sentence

A transaction script organises business logic as one procedure per request, run as one transaction, with no domain objects behind it.

## The six acts

### One Request, One Procedure

Two mugs are ordered: sixteen pounds, and the stock falls to eight. The whole action is one method, read from top to bottom.

```
  ORD-1 for £16.00. stock of MUG-BLUE: 8.
  the whole business action is one method, read from the top to the bottom.
```

### One Transaction

The card is declined after the stock was taken. The transaction undoes the stock change together with everything else, so the stock is back to ten and no order exists.

```
  card declined after the stock was taken.
  stock of MUG-BLUE: 10. orders saved: 0. the script's changes were undone together.
```

### A Second Script Copies The Rule

The bulk discount moved from ten items to five. One script was told. Seven mugs cost fifty pounds forty when placed, and fifty six pounds when the same order is amended.

```
  7 mugs placed: £50.40. the same 7 mugs amended: £56.00.
  the bulk discount changed from 10 items to 5. one script was told, the other was not.
```

### Share A Procedure

The pricing moves into one helper function that both scripts call. They agree again, and the design is still procedural.

```
  7 mugs priced by the shared helper: £50.40 in both scripts.
  it is still procedural. there is no Order object, only a function both scripts call.
```

### The Bill: Growth

The first script has three decisions, so eight paths. After a year of new rules it has seven decisions, so one hundred and twenty eight paths, and every rule went in the middle of one method.

```
  decisions in the first script: 3, so 8 paths to test.
  decisions after three more rules: 7, so 128 paths to test.
  every new rule went in the middle of one method.
```

### Where A Script Is Right

A month-end job that adds up the orders is a dozen lines, read once and changed rarely. That is a script at its best.

```
  month end: 2 orders, £316.00 taken.
  a job with one purpose and a few rules is clearer as a script than as a set of objects.
```

## The verdict

Use a transaction script when the logic is simple, mostly sequential and unlikely to grow, and when a team wants the shortest path from request to result. Keep shared rules in helper functions. Move to a domain model when the same rules start to appear in several scripts, or when a script's decisions outgrow what anyone can test.

## How to recognise this in code you did not write

- A method named for a use case, such as `placeOrder`, that does everything from validation to saving.
- Service classes with long methods and no domain objects, only data holders.
- Two methods that each contain the same price calculation.
- `@Transactional` on a method that contains most of the business logic.

## Where you have already met this

Most small Spring and Java EE services, and nearly every report or batch job.

## When this is too much

A script is the opposite of too much. Its risk is too little structure as the rules grow, so watch the decisions in the middle of the method.
