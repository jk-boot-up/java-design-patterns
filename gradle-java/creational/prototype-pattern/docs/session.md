# Session Plan — The Prototype Pattern

A guided session for teaching this project to people who are new to design
patterns.

- **Audience:** anyone comfortable writing a Java class. No pattern
  knowledge assumed, though having done the builder-pattern session first
  helps for contrast, not prerequisite.
- **Duration:** ~50 minutes
- **Format:** live coding and discussion. Slides optional; the code is the
  material.
- **Group size:** works from 1 to about 20. Beyond that, the exercises need
  pairs.

> **Optional pre-work.** Ask participants to watch the video
> ([`../video/`](../video/)) beforehand. If they do, you can compress the
> first two blocks and spend the time on the exercises instead.

## Before You Start

Check that every machine can run:

```bash
./gradlew build
```

Have open in tabs: `ProductListing.java`, `Prototype.java`,
`ListingRegistry.java`, `ProductListingDemo.java`, `animation.html`.

## The One Thing They Should Leave With

If they remember nothing else:

> **When you already have one fully-assembled object and need another
> that's almost the same, copy it instead of rebuilding it from scratch —
> and decide, field by field, what "copy" should mean: a fresh copy for
> anything mutable, a shared reference for anything that can't change.**

Everything in the session is in service of that sentence.

## Timings

| Time | Block | Goal |
| --- | --- | --- |
| 0:00–0:08 | The repeated eleven-argument call | Make them feel the duplication |
| 0:08–0:16 | The `Cloneable` trap | Show why Java's own answer disappoints |
| 0:16–0:28 | The fix, live | `Prototype<T>` and `copy()` |
| 0:28–0:34 | Deep copy vs. shared reference | The judgment call at the heart of the pattern |
| 0:34–0:40 | The registry | Connect to the GoF book's named variant |
| 0:40–0:48 | Exercises | Hands on keyboard |
| 0:48–0:50 | Wrap up | The one sentence |

## 0:00–0:08 — The Repeated Eleven-Argument Call

Open a scratch file. Type the black earbuds listing in front of them, then
the white one right below it:

```java
ProductListing black = new ProductListing("EARBUD-BLK", "Wireless Earbuds",
        longDescription, "Electronics", "Acme Audio", Money.pounds(59.99),
        List.of("black-1.jpg"), Map.of("color", "Black"), standardShipping, 30, 12);

ProductListing white = new ProductListing("EARBUD-WHT", "Wireless Earbuds (White)",
        longDescription, "Electronics", "Acme Audio", Money.pounds(59.99),
        List.of("white-1.jpg"), Map.of("color", "White"), standardShipping, 30, 12);
```

Ask: *"How many of these eleven arguments actually changed?"* Count them
together — two, maybe three. Then: *"What happens when the compliance team
edits `longDescription`?"* Every call site needs the same edit, and it is
only a matter of time before one is missed.

## 0:08–0:16 — The `Cloneable` Trap

Ask: *"Java already has a way to copy an object — who's used
`clone()`?"* Usually a few hands. Write `Object.clone()` on the board and
ask what's odd about it: it's `protected`, it throws a checked exception
that can never actually happen, and it copies fields shallowly.

Draw the shallow-copy problem concretely:

```java
List<String> images = original.getImages();   // via a hypothetical clone()
copy.getImages().add("extra.jpg");
// now original.getImages() has "extra.jpg" too — same List, two names
```

This is the moment to cite *Effective Java* Item 13 by name: it exists
because `Cloneable` disappoints almost everyone who tries to use it
correctly.

## 0:16–0:28 — The Fix, Live

Show `Prototype<T>`:

```java
public interface Prototype<T> {
    T copy();
}
```

One method. No exception, no protected access, no marker interface doing
invisible work. Then show `ProductListing.copy()`:

```java
@Override
public ProductListing copy() {
    return new ProductListing(sku, title, description, category, brand, price,
            images, attributes, shippingProfile, returnWindowDays, warrantyMonths);
}
```

Ask: *"Where's the deep-copying logic in this method?"* Let them look —
there isn't any. Walk up to the constructor and point at:

```java
this.images = new ArrayList<>(images);
this.attributes = new LinkedHashMap<>(attributes);
```

*"This line was already here, to protect the constructor's own caller.
`copy()` just gets it for free by calling the constructor again."*

## 0:28–0:34 — Deep Copy vs. Shared Reference

Point at `shippingProfile` — passed straight through, no copy:

```java
this.shippingProfile = shippingProfile;
```

Ask: *"Why is this one safe to share, when `images` isn't?"* Work towards:
`ShippingProfile` is a `record` — immutable, no setters, nothing can change
it out from under either listing. Run the demo and point at:

```
shippingProfile is the same instance: true
```

*"Same object, in memory, on both listings. That's not a bug — sharing an
immutable value costs nothing and loses nothing."*

## 0:34–0:40 — The Registry

Open `ListingRegistry.create(key)`. Tell them plainly: the Gang of Four
book names this variant too — sometimes called a Prototype Manager — for
when the set of templates is decided at runtime rather than known in the
caller's source code.

Ask: *"Does `create()` ever write `new ProductListing(...)`?"* It does not
— it only ever calls `.copy()` on whatever was registered. Compare with
`PurchaseOrderPresets` from the builder-pattern project if they've seen it:
same idea, a caller asks by name and never sees the construction details.

## 0:40–0:48 — Exercises

### Exercise 1 — Add a mutable field (about 5 minutes)

> Add `List<String> tags` to `ProductListing`, defensively copied in the
> constructor the same way `images` is.

Draw out: `copy()` needs zero changes. It already forwards every
constructor argument.

### Exercise 2 — Break the deep copy on purpose (about 5 minutes)

> Change `this.images = new ArrayList<>(images)` to `this.images = images`.
> Write a test that mutates a copy's `images()` and asserts the original
> is unaffected.

Watch it fail. Ask: *"Which single line was protecting you?"* Put it back,
watch the test pass.

## 0:48–0:50 — Wrap Up

Back to the one sentence:

> When you already have one fully-assembled object and need another that's
> almost the same, copy it instead of rebuilding it from scratch — and
> decide, field by field, what "copy" should mean.

Then send them somewhere:

- [`../README.md`](../README.md) to run it themselves
- [`animation.html`](animation.html) to step through it again slowly
- [`../video/`](../video/) if they want it narrated
- [`../../builder-pattern`](../../builder-pattern) for the contrast — one
  object assembled piece by piece, versus one object cloned and tweaked

## Facilitator Notes

- **The `Cloneable` block is the hook.** Most Java developers have typed
  `implements Cloneable` at some point without reading Item 13. Naming the
  specific complaints — protected method, checked exception, shallow copy
  — turns a vague unease into something concrete.
- **Expect "isn't this just a copy constructor?"** Worth taking seriously.
  The answer: yes, mechanically — `copy()` here *is* a copy constructor
  wearing an interface. The value of `Prototype<T>` is the shared method
  name and the shared contract ("fully independent"), which lets code that
  doesn't know the concrete type still ask for a copy — exactly what
  `ListingRegistry` relies on.
- **If you are running short**, cut the registry block (0:34–0:40). It is
  a real GoF variant but the core pattern survives without it.
