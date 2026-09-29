# Higher-Order Functions, Explained

## The pattern in one sentence

A higher-order function takes a function or returns one, so behaviour can be
passed in, made to order, and combined.

## The 5 acts

### 1. A loop for every question

The catalogue has three methods: products under 10, products in stock, and
mugs. Each has its own loop, and the three loops are identical except for the
one test in the middle. A new question, such as mugs under 10 that are in
stock, would mean copying the loop a fourth time.

### 2. Pass the test in

Now there is one `filter` method, with one loop, and the test is passed in as
a function. `filter(all, p -> p.price() < 10)` returns the blue mug, the mini
lamp and the tea towel, the same answer as before. A function that takes
another function is a higher-order function.

### 3. Functions that make functions

A function can also return a function. `priceBelow(10)` returns a test made
to order, and tests combine with `and` and `negate`. Mugs under 10 that are in
stock is `priceBelow(10).and(inCategory("mug")).and(inStock())`: the blue
mug. Products under 20 that are sold out: the travel mug. New questions, and
no new loop.

### 4. Price rules as values

Price rules are functions too: `percentOff(20)` and `amountOff(5)`. They are
joined with `andThen`. For the 45.00 desk lamp, 20% off then 5 off gives
31.00, and 5 off then 20% off gives 32.00. The order of the functions matters,
and the code makes the order plain.

### 5. The bill

Small functions need good names. A chain of anonymous lambdas can hide the
business rule it implements, and an error inside one shows a generated name
in the stack trace. Give important functions names, like `priceBelow` and
`inStock`, and keep each one short.

## The verdict

Use higher-order functions when the same code shape repeats with a small part
changing. Pass that part in, build rules from small named functions, and
mind the order when composing.

## How to recognise this in code you did not write

- Method parameters typed `Predicate`, `Function` or `Comparator`.
- Factory methods that return lambdas.
- Chains of `and`, `andThen` and `thenComparing`.

## Where you have already met this

- `stream().filter(...)`, `map(...)` and `sorted(Comparator.comparing(...))`.
- `Predicate.and`, `Function.andThen` and `Comparator.thenComparing`.
- Callbacks and event listeners, which pass a function to be called later.
