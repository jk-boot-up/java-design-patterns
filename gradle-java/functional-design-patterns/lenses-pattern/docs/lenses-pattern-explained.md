# Lenses for Immutable Updates, Explained

## The pattern in one sentence

A lens pairs a getter and a setter for one part of an immutable whole, and
lenses join to update deep inside, returning a new whole.

## The 5 acts

### 1. Rebuilding by hand

To change the postcode, the code builds a new address, a new customer around
it, and a new order around that: three constructors, copying every other
field. Street and city are both strings, and here they were passed the wrong
way round. The compiler cannot tell, and the result says street Leeds, city 1
High Street.

### 2. One lens

A lens is a getter and a setter for one field, written once and tested.
`ADDRESS_POSTCODE.get` reads LS1 4AP. `ADDRESS_POSTCODE.set` returns a new
address with LS2 7HY, and the original address is unchanged.

### 3. Lenses join

Lenses join with `andThen`. Order to customer, then customer to address, then
address to postcode, gives one lens: `ORDER_POSTCODE`. Setting the postcode of
the whole order is now one line, and it rebuilds all three levels correctly,
every time. The old order still says LS1 4AP.

### 4. Change with a function

`modify` applies a function to the part: a postcode typed as "ls2 7hy" becomes
"LS2 7HY" with `String::toUpperCase`. And lenses are ordinary values, so a
city lens and a postcode lens used together move the delivery to York, YO1 7HH,
with the street untouched.

### 5. The bill

Lenses are code to write: four field lenses by hand for three levels, because
Java has no built-in way to make them. Each set makes three new objects, but
unchanged parts are shared rather than copied: the updated order holds the very
same list of lines. For one or two flat records, a small `with` method is
simpler.

## The verdict

Use lenses for deeply nested immutable data with many different updates.
Write one small lens per field, join them for deep paths, test the three laws,
and prefer simple `with` methods when the data is flat.

## How to recognise this in code you did not write

- Objects with `get` and `set` (or `replace`) functions that return new values.
- Chains like `address.andThen(postcode)`.
- Optics libraries: Monocle, Arrow, Functional Java.

## Where you have already met this

- Monocle in Scala and Arrow Optics in Kotlin.
- Immutable-update helpers such as Immer in JavaScript.
- Generated `with...` methods in Lombok (`@With`) and Immutables.
