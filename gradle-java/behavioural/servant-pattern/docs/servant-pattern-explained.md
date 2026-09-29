# Servant, Explained

## The pattern in one sentence

A servant is a separate class that performs one job for many unrelated classes,
each of which only offers a small interface with the facts the job needs.

## The 5 acts

### 1. Copied postage

Postage is now 120 pence plus 160 pence for every started kilo. The parcel's
copy of the sum was updated: 2300 grams costs £6.00. The letter's and gift
card's copies still use the old rates and charge £2.50 instead of £2.80. A
shared parent class could have held one copy, but it would tie every item into
one family tree just to be posted.

### 2. One servant

`ShippingServant` holds the rates and the sum, once. Each item only implements
`Shippable`: a name, a weight in grams and a city. The servant prints a label
for each: parcel £6.00, letter £2.80, gift card £2.80. The items hold no
shipping code at all.

### 3. A new kind of item

The shop starts sending pallets. `Pallet` implements `Shippable`, and the same
servant labels it: 180,000 grams to Hull, £289.20. No postage code was written
for pallets.

### 4. Tested alone

Because the servant only needs a `Shippable`, it can be tested with a made-up
item. 1001 grams is two started kilos: £4.40. The servant keeps nothing
between calls, so one instance serves every item in the shop.

### 5. The bill

The behaviour is no longer on the item. A developer typing `parcel.` finds no
postage method and has to know the servant exists. And every item now exposes
its weight and city to anyone who asks, because the servant needs them.

## The verdict

Use a servant when several unrelated classes need the same behaviour and a
shared parent class does not fit. Keep the interface small, keep the servant
stateless, and name it so developers can find it.

## How to recognise this in code you did not write

- Classes named `...Service`, `...Helper` or `...s` (like `Collections`) that take an interface as a parameter.
- Small interfaces such as `Comparable`, `Shippable`, `Printable`.
- Several classes implementing the same small interface only to be handled by one helper.

## Where you have already met this

- `java.util.Collections.sort(list)`: one class that sorts any `List` of `Comparable` things.
- `Files`, `Objects` and other Java utility classes that work on anything with the right interface.
- Printing and export helpers that turn any object with a few getters into a label or a CSV row.
- Service classes in Spring applications that operate on plain data objects.
