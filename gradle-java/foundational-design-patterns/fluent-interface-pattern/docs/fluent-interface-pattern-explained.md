# Fluent Interface, Explained

## The pattern in one sentence

A fluent interface lets calls be chained so that code reads like a sentence, each call returning something to call the next on.

## The six acts

### A Long List Of Arguments

The find call with mugs, twenty five hundred, true, true and ten gives the blue mug and the big mug. With the two booleans the other way round, it gives three mugs, including one that is not in stock. Both compile. Which is in stock, and which is the sort? You must count the arguments to know.

```
  find("mugs", 2500, true, true, 10): [Blue Mug, Big Mug].
  find("mugs", 2500, false, true, 10) has the two booleans the other way round: [Blue Mug, Gift Mug, Big Mug].
  both compile. which is in stock, and which is the sort? you must count the arguments to know.
```

### A Sentence

Search, category mugs, under twenty five hundred, in stock, cheapest first, first ten. The same answer as the long call, and every part names itself.

```
  search().category("mugs").under(2500).inStock().cheapestFirst().first(10): [Blue Mug, Big Mug].
  the same answer as the long call, and every part names itself.
```

### Leave Out What You Do Not Need

Category only: green tea. Under a thousand, any category: the blue mug, and green tea. And the order of the optional parts does not matter.

```
  category only: [Green Tea].
  under 1000, any category: [Blue Mug, Green Tea].
  the order of the optional parts does not matter: [Blue Mug, Big Mug].
```

### Does A Call Change The Query?

A query that never changes: cheap gives the blue mug, dear gives three mugs, and the base still gives four. A query that changes itself: cheap and dear give the same three mugs. They are the same object. The cheap query was spoiled by the dear one.

```
  never changing: cheap [Blue Mug], dear [Blue Mug, Big Mug, Gift Mug], the base still [Blue Mug, Big Mug, Gift Mug, Travel Mug].
  changing itself: cheap [Blue Mug, Big Mug, Gift Mug], dear [Blue Mug, Big Mug, Gift Mug]. they are the same object: true. the cheap query was spoiled by the dear one.
```

### Guided Steps

At the start, the only thing offered is category. Then, under. Then, cheapest first, in stock, or run. A call out of order does not compile.

```
  at the start, the only thing offered is: [category].
  then: [under]. then: [cheapestFirst, inStock, run].
  [Blue Mug, Big Mug]. a call out of order does not compile.
```

### The Bill

Under minus five was accepted, and nothing complained. It failed at run, saying the price limit is below zero. The mistake and the report are on different steps of one long line. A debugger cannot stop between the calls of one chain, and a stack trace names the line, not the step. And it is a small language that someone designed: this one has seven methods to learn, and to keep.

```
  under(-5) was accepted. nothing complained.
  it failed at run(): "the price limit is below zero: -5". the mistake and the report are on different steps of one long line.
  a debugger cannot stop between the calls of one chain, and a stack trace names the line, not the step.
  and it is a small language that someone designed: this one has 7 methods to learn, and to keep.
```

## The verdict

Use a fluent interface where many optional settings make a plain call hard to read. Make each call return a new object, unless the object is a builder used once. Check values in each call, not at the end. Use staged types when order matters. Keep it small, since it is a language you must maintain.

## How to recognise this in code you did not write

- Java streams: `list.stream().filter(...).map(...).toList()`.
- `StringBuilder.append(...).append(...)`.
- jOOQ, QueryDSL, AssertJ and Mockito's `when(...).thenReturn(...)`.
- Builders with `.name(...).age(...).build()`.

## Where you have already met this

Java streams, AssertJ assertions, Spring's `WebClient` and `HttpSecurity`, and query builders such as jOOQ.

## When this is too much

For two or three obvious arguments, a plain call is shorter. A fluent API costs a class, a design and its upkeep.
