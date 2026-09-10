# Session Guide — Iterator Pattern

A 60-minute session plan for teaching the Iterator pattern from this project.
Written for a facilitator working with beginners; every timing is a
suggestion, and the exercises are the part worth protecting if you run late.

**Audience:** developers who can write a `for` loop and have used `List`, but
have never implemented `Iterator` or wondered where for-each comes from.

**Setup:** everyone has the project cloned and `./gradlew test` passing before
the session starts. See [`prerequisites.md`](prerequisites.md).

## Learning Objectives

By the end, participants can:

1. Explain what the for-each loop actually compiles to.
2. Name the two roles — aggregate and iterator — and say which one holds the
   position, and why.
3. Implement `Iterable` and `Iterator` for a source that is awkward to walk.
4. Recognise when the pattern is *not* worth it (a plain `List` already has
   one).
5. Explain laziness in terms of when the next page is fetched.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check |
| 0:05–0:15 | The problem |
| 0:15–0:25 | The pattern |
| 0:25–0:40 | Code walkthrough |
| 0:40–0:50 | Exercises |
| 0:50–0:58 | Pitfalls and comparisons |
| 0:58–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check

Have everyone run:

```bash
./gradlew test    # 13 tests
./gradlew run
```

Anyone whose tests fail should pair for the session rather than debug.

Ask, before showing anything: **"What does `for (String s : list)` actually
do?"** Collect answers. Most rooms produce "it loops over the list" and stop
there. Note the answers down; you will come back to them at 0:15.

## 0:05–0:15 — The Problem

Open [`problem-statement.md`](problem-statement.md) and set the scene: the
catalogue lives in the warehouse system and arrives one page at a time.

Then open `NaiveCatalogueBrowser` and read the three methods side by side.
Do not explain the bugs yet. Ask the room to find them.

Run section 1 of the demo:

```bash
./gradlew run
```

The three lines to sit with:

- `allProducts() -> 8 products (correct)`
- `countProducts() -> 8 products` — right today, wrong the day a tenth
  product is added
- `findCheapest() -> SKU-005 Coffee Mug £8` — a real product, a real price,
  and not the cheapest one

The teaching point is not "loops are hard". It is that **all three bugs are
the same bug**: the page loop was written three times, so it could be got
wrong three ways, and none of the ways throws.

## 0:15–0:25 — The Pattern

Go back to the question from the setup check and answer it properly. Write
this on the board:

```java
for (Product product : catalogue) { ... }
```

```java
Iterator<Product> it = catalogue.iterator();
while (it.hasNext()) {
    Product product = it.next();
    ...
}
```

These are the same program. The compiler writes the second from the first,
and it will do that for *any* type that implements `Iterable`.

Then the bookmark analogy, which does most of the work with beginners: the
catalogue is the book, the iterator is the bookmark. Two people reading one
book need two bookmarks, not one glued to the spine.

Ask: **"So where does the current page number live?"** The answer — on the
bookmark, never on the book — is the single idea people most often get wrong
the first time they write an iterator.

## 0:25–0:40 — Code Walkthrough

Read the code in this order. Resist jumping to `hasNext()` first.

1. **`CatalogueFeed`** — the awkward thing being hidden. Point at
   `pagesFetched`; say it is there for the tests, and that it will matter in
   ten minutes.

2. **`ProductCatalogue`** — four lines. Ask what is *missing* before saying
   anything about what is there. There is no page number and no position.
   That absence is the design.

3. **`CatalogueIterator` fields** — every one of them is position. Contrast
   with the previous file: all the state that is not in the catalogue is
   here.

4. **`hasNext()`** — the only page loop in the project. Walk it with concrete
   numbers: eight products, three per page. Ask why the `while` is not an
   `if`. (A short page in the middle, or an empty first page.)

5. **`next()`** — three lines, because `hasNext()` did the work. Ask why it
   calls `hasNext()` again rather than trusting the caller.

6. **`CatalogueIteratorTest.fetchingIsLazy`** — now `pagesFetched` pays off.
   Two products consumed, one page fetched. Run just this test and change
   `ProductCatalogue` to fetch page 0 in its constructor; watch it fail.

7. **`CatalogueIteratorTest.positionsAreIndependent`** — two iterators, one
   catalogue. This is the test that catches the "position on the aggregate"
   mistake. Section 4 of the demo prints the same thing if you would rather
   show it running.

## 0:40–0:50 — Exercises

### Exercise 1 — Grow the catalogue (everyone)

Add two more products to `CatalogueFeed.sampleShop()`, then run the tests.

`NaiveCatalogueBrowserTest.countProductsStopsEarly` fails; every test of the
pattern still passes. The discussion: the naive code did not break *today*,
it broke on the day someone did something completely unrelated.

### Exercise 2 — Move the position (everyone)

Move `pageNumber` and `indexInPage` from `CatalogueIterator` onto
`ProductCatalogue`, and make `iterator()` return `this`-ish behaviour.

`positionsAreIndependent` fails. Ask what a nested loop over the catalogue
would now do in production, and how long it would take anyone to notice.

### Exercise 3 — A filtered catalogue (most people)

Write `CategoryCatalogue implements Iterable<Product>` that wraps the same
feed and yields only products in one category.

The point to draw out: nothing else in the project changes, and the for-each
loop at the call site is identical. Also that `hasNext()` gets harder — you
have to look ahead — which is a genuine and instructive difficulty.

### Exercise 4 — Stretch (for fast finishers)

Make `CatalogueIterator.remove()` throw `UnsupportedOperationException` with
a useful message, then discuss what it *would* have to do to work. Where
would the removal go? What happens to the position? What if the feed is
remote?

## 0:50–0:58 — Pitfalls and Comparisons

Cover briefly, from
[`iterator-pattern-explained.md`](iterator-pattern-explained.md):

- **Position on the aggregate** — the mistake from Exercise 2.
- **`hasNext()` that consumes** — callers will call it twice; if that changes
  anything, code that looks right will skip elements.
- **Fetching in the constructor** — throws the laziness away.
- **Reaching for it when a `List` would do** — the pattern earns its keep
  when the storage is awkward. Over an `ArrayList` it is ceremony.

Then the comparison table: index loop when you need the index, iterator when
you want each element in turn, stream when you want to describe a pipeline.
Say explicitly that streams are *built on* this, not opposed to it.

## 0:58–1:00 — Wrap-Up

One sentence to leave in the room:

> **The collection knows what is in it. The iterator knows where you are.
> Keep those two facts in different objects and the for-each loop is free.**

Point at [`animation.html`](animation.html) for anyone who wants to walk it
again, and at the video for anyone who wants it narrated.

## Facilitator Notes

- **The bookmark analogy is worth the time.** It is the fastest route to why
  the position lives on the iterator, and people remember it.
- **Do not skip running the naive demo.** "Returns the wrong product without
  throwing" lands much harder as output than as a claim.
- **Expect the question "why not just return a `List`?"** It is a good
  question. The answer is laziness and size: `allProducts()` fetches
  everything even when the caller wanted two, and on a real catalogue that is
  the difference between one request and four hundred.
- **Expect "isn't this what streams are for?"** Yes, and streams need
  exactly this underneath. If the room is comfortable, show
  `StreamSupport.stream(catalogue.spliterator(), false)` and move on.
- **Watch the clock at 0:25.** The walkthrough is the section that overruns,
  and the exercises are where the learning happens.

## Materials Checklist

- [ ] Project cloned, `./gradlew test` green for everyone
- [ ] `docs/animation.html` open in a browser tab
- [ ] `docs/images/class-diagram.png` on screen for 0:15–0:25
- [ ] A whiteboard for the for-each / while equivalence
- [ ] The video queued as optional follow-up
