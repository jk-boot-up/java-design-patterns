# Problem Statement

## The Scenario

You are building the catalog page for an online store. Every listing can
carry a badge — `NEW`, `SALE`, `BESTSELLER`, `LOW_STOCK` — and a badge is
more than a coloured label: it carries an icon, a background colour, a text
colour, a bold/plain rule, and the rasterised artwork a design system hands
over for that icon. There are only **four** distinct badge designs. There
are, this quarter, **one hundred thousand** listings.

## Attempt One: A Badge Object Per Listing

The obvious shape: each listing owns its own badge, built from its type.

```java
public final class NaiveListingBadge {
    private final BadgeType type;
    private final String icon;
    private final String backgroundColor;
    private final String textColor;
    private final boolean bold;
    private final byte[] artwork;   // the rasterised icon, 64 KB

    public NaiveListingBadge(BadgeType type, String listingId) {
        this.artwork = new byte[64 * 1024];
        // ...fill in icon / colours / bold for this type, from scratch
    }
}
```

Every one of the four badge *designs* is correct. The waste is in how many
times it gets rebuilt: 100,000 listings means 100,000 copies of the same
four artworks, the same four colour pairs, the same four icons — because
`SALE` looks identical on every listing that has it, yet nothing here shares
that fact.

## Why That Hurts

Do the arithmetic on just the artwork field:

```
100,000 listings × 64 KB artwork each  ≈  6,250 MB
         4 badge types × 64 KB each    ≈  256 KB
```

Six gigabytes of pixels, when the actual number of distinct pictures being
drawn is four. And it is not only memory:

- **Construction cost multiplies too.** Whatever it took to build one
  `SALE` badge — reading a colour palette, decoding an icon — now happens
  100,000 times instead of once.
- **Nothing here is a bug.** Every `NaiveListingBadge` renders correctly.
  The waste is structural: the type carries state that does not vary per
  listing, but a new copy of that state is paid for on every listing anyway.
- **It gets worse with scale, not better.** Double the catalog and the
  naive cost doubles with it. The actual number of *distinct* badge designs
  never changes.

## The Question This Project Answers

> How do we let 100,000 listings each display a badge, while actually
> keeping only **four** badge objects in memory — one per distinct design —
> no matter how large the catalog grows?

## The Goal

Separate what a badge design *is* (its type, icon, colours, artwork — the
same for every listing of that type) from which *listing* is wearing it
(a value that is different every time):

```java
BadgeStyle style = BadgeStyleFactory.styleFor(BadgeType.SALE);   // shared, built once
style.render("LST-1002", null);                                  // this listing's own text
style.render("LST-1003", "Flash Sale");                           // a different listing, same style
```

`styleFor(BadgeType.SALE)` returns the *same* object every time, no matter
how many listings ask for it. The listing id and any custom label are
supplied at render time — they are never stored on the shared object.

This is precisely the problem the **Flyweight** design pattern solves. See
[`flyweight-pattern-explained.md`](flyweight-pattern-explained.md) for how.
