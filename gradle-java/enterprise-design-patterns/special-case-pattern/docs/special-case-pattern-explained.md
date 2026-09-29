# Special Case, Explained

## The pattern in one sentence

A special case is an object that stands in for an unusual but normal
situation, such as a guest or a deleted account, and answers every question
the ordinary object would, in the way that fits.

## The 5 acts

### 1. Null checks everywhere

`Directory.findOrNull` returns `null` for a guest. `Checkout.withNullChecks`
checks for null when reading the name, the discount and the marketing flag,
but not before adding loyalty points. Priya, a registered customer, pays
£38.00 after her member discount. The first guest causes a
`NullPointerException`.

### 2. A guest special case

`Directory.find` never returns null. With no ID it returns a `Guest`, which
implements `Customer`: name "Guest", no discount, no points, no newsletter.
`Checkout.run` has no null checks. Priya pays £38.00 and earns points; the
guest pays £40.00 and earns none.

### 3. An unknown customer

An old order belongs to `C-99`, an account that was deleted. The lookup
returns an `Unknown` special case that remembers the old ID. The order history
report runs, shows "Former customer", and still records who it was.

### 4. Behaviour, not type checks

The newsletter step asks each customer `canReceiveMarketing()`. Priya says yes;
the guest and the former customer say no. Nowhere does code ask
`instanceof Guest`: each case answers for itself.

### 5. The bill

Special cases can hide mistakes. A mistyped ID, `C-71`, quietly becomes a
former customer and checkout carries on, where a crash would at least have
been noticed. And each new method on `Customer` must be written for every
special case too.

## The verdict

Return special cases for situations that are normal and meaningful, so callers
never check for null. Keep real errors as errors, and make sure every special
case implements every method sensibly.

## How to recognise this in code you did not write

- Classes named `Guest...`, `Unknown...`, `Missing...`, `Anonymous...` or `Empty...`.
- Lookups documented as "never returns null".
- `Collections.emptyList()` and similar ready-made empty values.

## Where you have already met this

- `Collections.emptyList()`, a special case for "no items".
- Anonymous users in web frameworks, such as Spring Security's `AnonymousAuthenticationToken`.
- "Unknown" or "Deleted user" shown in place of a removed account on forums and shops.
