# The Problem

A seller on our marketplace lists "Wireless Earbuds" in black. Getting that
one listing right is real work:

- pick a category from the taxonomy (`Electronics > Audio > Earbuds`)
- write a description that satisfies the platform's compliance rules
- choose a shipping profile — carrier, weight, whether shipping is free
- set a return window and a warranty length that match the category's policy
- upload photos, fill in a dozen attributes

Now the seller wants the same earbuds in white, and again in blue. Nothing
about the category, the compliance text, the shipping profile, the return
window or the warranty changed. Only the sku, the title, one attribute and
the photos did.

## Attempt one: build each variant from scratch

```java
ProductListing black = new ProductListing(
        "EARBUD-BLK", "Wireless Earbuds", longCompliantDescription,
        "Electronics", "Acme Audio", Money.pounds(59.99),
        List.of("earbuds-black-1.jpg", "earbuds-black-2.jpg"),
        Map.of("color", "Black", "connectivity", "Bluetooth 5.3"),
        standardShipping, 30, 12);

ProductListing white = new ProductListing(
        "EARBUD-WHT", "Wireless Earbuds (White)", longCompliantDescription,
        "Electronics", "Acme Audio", Money.pounds(59.99),
        List.of("earbuds-white-1.jpg"),
        Map.of("color", "White", "connectivity", "Bluetooth 5.3"),
        standardShipping, 30, 12);
```

It works, but look at what got repeated: the description, the category, the
brand, the price, the shipping profile, the return window, the warranty —
eight of eleven arguments are copy-pasted, character for character, between
two calls that differ in exactly two facts. Add a blue variant and the
seller pastes the same eight arguments a third time. Fix a typo in the
compliant description and every call site needs the same edit, and it is
only a matter of time before one of them is missed.

## Attempt two: `Cloneable`

Java already ships a way to copy an object — `Object.clone()` — so why not
use it?

```java
public class ProductListing implements Cloneable {
    @Override
    public ProductListing clone() throws CloneNotSupportedException {
        return (ProductListing) super.clone();
    }
}
```

*Effective Java*, Item 13, spends an entire chapter explaining why this is
worth avoiding. `Cloneable` is an interface with no methods of its own — it
is a marker that changes what `Object.clone()` does, which is a strange way
to opt in to anything. `clone()` itself is `protected`, so it has to be
overridden and re-exposed as `public` just to be usable. It throws a
checked `CloneNotSupportedException` that can never actually happen once a
class implements `Cloneable`, so every caller ends up catching an exception
that means nothing. And worst of all: `super.clone()` performs a **shallow**
copy — it copies each field's value, which for `images` and `attributes`
here means copying the *reference* to the same `List` and the same `Map`
the original holds. Mutate the "copy's" image list and the original's list
changes too, silently.

## The Question This Project Answers

> How do we take an object that is expensive to assemble correctly, and
> produce independent variants of it — different in a handful of fields,
> identical everywhere else — without re-typing the shared fields at every
> call site, and without inheriting `Cloneable`'s baggage?

The answer is the Gang of Four's **Prototype** pattern: give the type its
own `copy()` method, built on a plain interface with none of `Cloneable`'s
history, that returns a fully independent clone a caller can then tweak.

Read on in
[`prototype-pattern-explained.md`](prototype-pattern-explained.md).
