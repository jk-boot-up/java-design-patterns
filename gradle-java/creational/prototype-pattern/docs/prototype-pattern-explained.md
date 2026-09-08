# The Prototype Pattern, Explained

## First, an Honest Note

This one is squarely in the Gang of Four book, in the creational chapter,
alongside Builder and Abstract Factory. Unlike Builder, there is no
matching *Effective Java* item pushing the same idea from a different
angle — instead, *Effective Java* Item 13 spends its energy warning against
Java's own built-in attempt at this pattern, `Cloneable`. This project
implements Prototype's actual intent while deliberately avoiding
`Cloneable`, which is the honest way to teach both at once.

## The Definition

> Specify the kinds of objects to create using a prototypical instance, and
> create new objects by copying this prototype.
>
> — *Design Patterns* (Gamma, Helm, Johnson, Vlissides)

In plainer words:

> **Instead of describing how to build an object from scratch every time,
> keep one fully-assembled example around, and produce new ones by copying
> it and changing only what's different.**

## The Participants

| Role | In this project | What it does |
| --- | --- | --- |
| Prototype | `Prototype<T>` | An interface with one method, `copy()` |
| Concrete Prototype | `ProductListing` | Implements `copy()`, knows how to duplicate its own state |
| Client | `ProductListingDemo` | Builds one listing, then clones and tweaks it |
| Prototype Manager *(GoF's own name for it)* | `ListingRegistry` | A named shelf of templates, cloned by key |

## The Code, Walked Through

### `Prototype<T>` — not `Cloneable`

```java
public interface Prototype<T> {
    T copy();
}
```

One method, unchecked, public by construction — nothing to override from a
protected superclass method, nothing to catch. Any type that wants to be
copyable implements this and writes `copy()` however makes sense for its
own fields. The interface does not — cannot — provide a default
implementation, because only the type itself knows which of its fields need
a deep copy and which can be shared.

### `ProductListing` — deciding what to copy deeply, and what to share

```java
public ProductListing(String sku, String title, String description, String category,
        String brand, Money price, List<String> images, Map<String, String> attributes,
        ShippingProfile shippingProfile, int returnWindowDays, int warrantyMonths) {
    ...
    this.images = new ArrayList<>(Objects.requireNonNull(images, "images"));
    this.attributes = new LinkedHashMap<>(Objects.requireNonNull(attributes, "attributes"));
    this.shippingProfile = Objects.requireNonNull(shippingProfile, "shippingProfile");
    ...
}

@Override
public ProductListing copy() {
    return new ProductListing(sku, title, description, category, brand, price,
            images, attributes, shippingProfile, returnWindowDays, warrantyMonths);
}
```

Two things to notice, and they are the whole pattern:

**`copy()` has no copying logic of its own.** It just calls the constructor
again, passing this instance's own fields as arguments. That works because
the constructor already defensively deep-copies `images` and `attributes`
into a fresh `ArrayList` and `LinkedHashMap` — a rule that exists to protect
*any* caller of the constructor, not specifically to support `copy()`. One
piece of defensive-copying code ends up doing double duty. There is no
second deep-copy routine to keep in sync with the first.

**Not everything gets deep-copied.** `shippingProfile` is passed straight
through, unchanged, and both the original and the copy end up holding the
exact same `ShippingProfile` instance:

```java
public record ShippingProfile(String carrier, int weightGrams, boolean freeShipping) { }
```

That is safe only because `ShippingProfile` is immutable — a `record` with
no setters. Nothing can mutate it out from under either listing, so there
is nothing to protect by copying it. Contrast with `images`, a mutable
`List<String>`: sharing the same list between the original and a copy would
mean editing one edits the other, which defeats the entire point of making
a copy.

This is Prototype's real design work — not the mechanical "call the
constructor again" part, but the field-by-field judgment call: **deep-copy
what's mutable, share what's immutable.**

### Using it

```java
ProductListing master = new ProductListing("EARBUD-BLK", "Wireless Earbuds", ...);

ProductListing white = master.copy();
white.setSku("EARBUD-WHT");
white.setTitle("Wireless Earbuds (White)");
white.attributes().put("color", "White");
white.images().clear();
white.images().add("earbuds-white-1.jpg");
```

Five lines instead of an eleven-argument constructor call repeating eight
values that never changed. `master` is untouched — `white.attributes()` and
`white.images()` are its own independent map and list, not `master`'s.

### `ListingRegistry` — the Prototype Manager, for when keys beat types

```java
public ProductListing create(String key) {
    ProductListing template = templates.get(key);
    if (template == null) {
        throw new NoSuchElementException("no listing template registered under: " + key);
    }
    return template.copy();
}
```

The GoF book describes exactly this as a variant of Prototype — sometimes
called a **Prototype Manager** — for when the set of "kinds of thing to
copy" is decided at runtime (loaded from a database, configured by a
catalog admin) rather than known and spelled out in the caller's source
code. A caller here never writes `new ProductListing(...)` and never even
imports it by name in spirit — it asks the registry for `"earbuds-template"`
and gets back an independent copy, the same way `PurchaseOrderPresets` in
the builder-pattern project lets a caller ask for `"expressOrder"` without
knowing `PurchaseOrder`'s constructor.

## What You Gain

**No re-typing the shared fields.** Every variant pays only for what makes
it different — a sku, a title, one attribute, a photo list.

**A single, honest place for the deep-copy decision.** `copy()` in this
project reuses the constructor's own defensive copy, so there is exactly
one piece of code responsible for "which fields need their own list or
map" — not two copies of that logic that could quietly drift apart.

**None of `Cloneable`'s baggage.** No protected method to re-expose, no
checked exception that can never fire, no shallow-copy-by-default trap.
`copy()` is just a method, typed and documented like any other.

**A runtime-keyed shelf of templates, when that's what the domain needs.**
`ListingRegistry` turns "which kind of listing" from a compile-time
decision (which concrete class to `new`) into a runtime one (which string
key to pass).

## What to Watch Out For

**Deep-copy judgment doesn't come for free.** Every mutable field a
concrete prototype adds is one more thing its author must remember to
deep-copy in the constructor. Miss one, and `copy()` silently produces two
listings sharing a list — exactly the bug this pattern exists to prevent.

**Not a substitute for validation.** `copy()` reproduces whatever state the
original had, valid or not. If `master` was somehow built with contradictory
data, every clone inherits that.

**Registries add a lookup failure mode.** `ListingRegistry.create("typo")`
throws at runtime instead of failing to compile, the price every
string-keyed lookup pays. Reach for a registry when the set of keys is
genuinely decided outside the caller's code — not as a way to avoid naming
a constructor.

## How This Relates to the Other Creational Patterns

| | Prototype | Builder | Static Factory Method | Abstract Factory |
| --- | --- | --- | --- | --- |
| In the GoF book? | Yes | Yes | No | Yes |
| The problem it solves | Cheaply producing near-duplicates of an expensive-to-assemble object | Many optional pieces, one object | Naming and hiding a constructor | Which whole matching set? |
| What the caller writes | `template.copy()`, then a few setters | A chain of calls, one per piece | One named call | One call, gets a family back |
| Extra classes needed | One interface (`Prototype<T>`) | One builder | None | One per family |

The honest summary: Prototype answers a question none of the others do —
*"I already have one of these; how do I get another that's almost the
same?"* Builder answers "how do I assemble one piece by piece the first
time?" A real system often uses both: a `ListingRegistry` template might
itself have been assembled with a builder before being registered.

## Try It Yourself

1. **Add a mutable field.** Give `ProductListing` a `List<String> tags`.
   Wire it through the constructor with the same `new ArrayList<>(...)`
   defensive copy the other collections use. Confirm `copy()` needs no
   changes at all — it already forwards every field to the constructor.
2. **Break the deep copy on purpose.** Change `this.images = new
   ArrayList<>(images)` to `this.images = images`. Write a test that
   mutates a copy's `images()` and asserts the original is unaffected.
   Watch it fail, and see exactly which line stopped protecting you.
3. **Register a second template.** Add a `"phone-case-template"` to
   `ListingRegistry` in `ProductListingDemo` and create two independent
   instances from it.
4. **Feel the alternative.** Implement `Cloneable` on a copy of
   `ProductListing` instead, using `super.clone()`. Try to make `images`
   independent between the original and the clone without writing your own
   `copy()`-shaped logic inside `clone()` anyway.
