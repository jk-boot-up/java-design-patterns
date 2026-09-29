# Immutable Object, Explained

## The pattern in one sentence

An immutable object never changes after it is made; to change something, you
make a new object, so every holder of the old one keeps seeing exactly what
it saw.

## The 5 acts

### 1. Shared, then changed

Order `ORD-1` is placed and keeps a reference to Priya's profile address,
`4 Mill Lane, Leeds`. Later she moves and updates her profile for future
orders, calling `setStreet` and `setCity`. There was only ever one address
object, so `ORD-1` now says `12 High Street, York`, for a parcel she ordered
before moving.

### 2. Changed while being read

The shared `MutablePriceList` holds a kettle at £30, a mug at £10 and a teapot
at £25: £65.00 for the basket. A ten percent sale is applied one price at a
time. A checkout that reads after the first change sees the new kettle and the
old mug and teapot: £62.00. After the sale the basket is £58.50. The customer
paid a price that never existed.

### 3. Lost in a set

Tom's address goes into a `HashSet` of failed deliveries. A hash set files each
object under a number worked out from its contents. Then someone tidies the
spelling, `Road` to `Rd`. The object's number changes, but it is still filed
under the old one, so `contains` answers false, while the set's size is still
one.

### 4. Immutable objects

`Address` is a record with no setters. `withStreet` and `withCity` return a
new address, so Priya's profile moves to York and `ORD-2` still ships to
Leeds. `PriceList` is immutable too: `withSale(10)` builds a whole new list on
the side while checkout keeps reading £65.00, then `Shop.publish` swaps it in
with one step, and checkout reads £58.50. There is no moment in between. The
constructor copies the map it is given, so changing that map later has no
effect, and an immutable address in a set is always found.

### 5. The bill

Every change is a copy. Changing one price in a catalogue of a thousand items
makes a new list of a thousand entries. And every field you might want to
change needs its own `with...` method. For values that are small or change
rarely, this is cheap; for something that changes constantly, it may not be.

## The verdict

Make every value immutable by default: addresses, prices, dates, identifiers,
messages, settings. Use records, copy collections in with `List.copyOf` and
`Map.copyOf`, and replace whole objects instead of editing them. Keep mutation
for the few objects that exist to change, and give each of those one owner.

## How to recognise this in code you did not write

- `record` declarations and classes with only `final` fields.
- `with...` methods that return a new object.
- `List.copyOf`, `Map.copyOf`, `Collections.unmodifiableList` in constructors or getters.
- An `AtomicReference` or `volatile` field swapped to a new object instead of edited.

## Where you have already met this

- `String`, `Integer`, `LocalDate` and `BigDecimal` are all immutable.
- Java `record`s, and `List.of`, `Map.of`, `List.copyOf`.
- The Value Object pattern in domain-driven design.
- Immutable state in React and Redux, and in functional languages.
