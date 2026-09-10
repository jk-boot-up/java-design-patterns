# Iterator Pattern

Demonstrates the Behavioural **Iterator** design pattern using a shop's
product catalogue as an example. The catalogue arrives from the warehouse one
page at a time; the pattern is what lets the rest of the shop forget that.

- `CatalogueFeed` — the awkward source. You cannot ask it for "all products";
  you ask for page 0, then page 1, and you know you have finished when a page
  comes back empty. It counts the pages it hands out, which is how two of the
  tests prove the walk is lazy.
- `CatalogueIterator` — the iterator, and the only page loop in the project.
  It holds the position, fetches a page the first time somebody reaches it,
  and answers `hasNext()` / `next()`. Package-private: callers only ever see
  it as a `java.util.Iterator`.
- `ProductCatalogue` — the aggregate. Implements `Iterable<Product>` in four
  lines, which is what buys you the for-each loop. It holds no position of
  its own, so every call to `iterator()` starts an independent walk.
- `Product` — a record: SKU, name, category, price in whole pounds.
- `NaiveCatalogueBrowser` — the trap, kept for contrast. Three methods, three
  hand-written copies of the page loop, and two of the copies are wrong: one
  caps itself at three pages, the other starts at page 1 and never sees the
  cheapest product in the shop.
- `CatalogueDemo` — runnable entry point showing the naive bugs, the for-each
  replacement, the laziness, and two independent walks over one catalogue.

## Run

```bash
./gradlew run
```

Which prints:

```text
========================================================================
1. The naive way: every caller writes the page loop
========================================================================
allProducts()  -> 8 products (correct)
countProducts()-> 8 products (WRONG: the loop stops after 3 pages)
findCheapest() -> SKU-005  Coffee Mug             home      £8
                 (WRONG: it starts at page 1, so the £4 socks are invisible)

Three methods, three copies of the page loop, two of them broken.
Nothing threw. The shop just quietly shows the wrong thing.

========================================================================
2. The pattern: the catalogue is just a thing you loop over
========================================================================
for (Product p : catalogue) { ... }

counted        -> 8 products (correct)
cheapest       -> SKU-002  Cotton Socks           clothing  £4 (correct)

No page numbers anywhere in that loop. There is nothing to get wrong,
because the only page loop in the project lives in CatalogueIterator.

========================================================================
3. Pages are fetched only when you reach them
========================================================================
The feed hands out 3 products per page, 8 products in total.

Showing the first 2 products, then stopping:
  SKU-001  Cotton T-Shirt         clothing  £12
  SKU-002  Cotton Socks           clothing  £4

pages fetched  -> 1 of 3
The customer looked at the first two products, so the warehouse was
asked for one page. The rest of the catalogue was never requested.

========================================================================
4. Two walks at once do not interfere
========================================================================
Two iterators from the same catalogue:
  outer.next() -> Cotton T-Shirt
  outer.next() -> Cotton Socks
  inner.next() -> Cotton T-Shirt   <- still at the start
  outer.next() -> Wool Scarf

Each iterator keeps its own position, so they cannot disturb each
other. That is why a loop inside a loop over the same catalogue works.
```

## Test

```bash
./gradlew test
```

13 tests across 3 classes. `ProductCatalogueTest` covers what a caller may
rely on: for-each visits every product once, in order, and crossing a page
boundary is invisible. `CatalogueIteratorTest` holds the two properties a
hand-written loop does not give you free — pages are fetched only when
reached, and two iterators over one catalogue keep separate positions — plus
the end-of-catalogue and empty-catalogue edges. `NaiveCatalogueBrowserTest`
pins the naive bugs in place rather than fixing them, so the "before" picture
is something you can run instead of something you have to take on trust.

## Learning Material

Start here if you are new to the pattern — the docs are ordered as a
learning path.

| Document | What it covers |
| --- | --- |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What to know and install before you start |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The problem the pattern solves, and why the naive approach hurts |
| [`docs/iterator-pattern-explained.md`](docs/iterator-pattern-explained.md) | The pattern itself, the code walked through, pitfalls, and comparisons |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Static structure |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Runtime call flow |
| [`docs/animation.html`](docs/animation.html) | Animated, step-by-step walkthrough — open in a browser. Optional narration via the **Narration** button |
| [`docs/session.md`](docs/session.md) | A 60-minute guided session plan for teaching it |
| [`docs/youtube.md`](docs/youtube.md) | Title, description, chapters and thumbnail for publishing the video |
| [`docs/thumbnail.png`](docs/thumbnail.png) | The 1280×720 image to upload as the YouTube thumbnail |
| [`docs/spec.md`](docs/spec.md) | The project specification — problem, code, video and publishing quality bar. Also as [`spec.html`](docs/spec.html) |
| [`video/`](video/) | A narrated video, plus the script and build pipeline |

### The pattern in one picture

![Iterator pattern class diagram](docs/images/class-diagram.png)

### Video

`video/iterator-pattern-explained.mp4` — 1080p, narrated. An audio-only
version is alongside it. See [`video/README.md`](video/README.md) to
rebuild or re-record it.
