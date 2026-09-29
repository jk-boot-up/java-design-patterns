# Currying, Explained

## The pattern in one sentence

Currying turns a function of several arguments into a chain of one-argument
functions, so early arguments can be fixed once.

## The 5 acts

### 1. Repeated arguments

The EU warehouse prices three parcels: half a kilo, two kilos and ten kilos.
Each call is `price(EU, STANDARD, weight)`: 7.00, 10.00 and 26.00. The zone and
service never change, but every call must repeat them, and every call could
get them wrong.

### 2. A curried function

The curried version takes one argument at a time. Applying it to EU returns a
function that wants a service; applying that to STANDARD returns a function
that wants only a weight. Call it `euStandard`. `euStandard.apply(2.0)` is
10.00, exactly what the three-argument call gave.

### 3. Ready-made functions

At start-up, the shop builds one ready-made function per zone for standard
post. A two-kilo parcel costs 5.00 to the UK, 10.00 to the EU and 20.00 to the
rest of the world. And because a ready-made function takes one argument, it
drops straight into `map`: checkout's parcels, EU express, cost 14.00, 20.00
and 52.00.

### 4. Argument order matters

A helper, `curry`, turns any two-argument function into a curried one, fixing
the first argument first. With `discount(percent, price)`, applying 20 makes a
"20% off" function, and 45.00 becomes 36.00. Written the other way round,
`(price, percent)`, applying 20 fixes the price instead, and "applying 45"
gives 11.00, nonsense. Order arguments from least to most often changing.

### 5. The bill

Java makes currying noisy: the curried type is
`Function<Zone, Function<Service, Function<Double, Double>>>`, and calls are
chains of `.apply`. A plain lambda, `kg -> price(EU, STANDARD, kg)`, gives the
same 10.00 and is often clearer. Use currying where functions are built in
stages and passed around; use a lambda where one fixed call is enough.

## The verdict

Curry when some arguments are known long before others and the smaller
function is reused or passed on. Order arguments from least to most changing,
and prefer a plain lambda when it reads better.

## How to recognise this in code you did not write

- Types like `Function<A, Function<B, R>>`.
- Calls like `f.apply(a).apply(b)`.
- Helpers named `curry`, `curried` or `partial`.

## Where you have already met this

- Every function in Haskell and F# is curried.
- `Function<A, Function<B, R>>` in Java libraries such as Vavr, with `curried()`.
- Configured objects and factories: fixing settings once, then calling with the changing part.
