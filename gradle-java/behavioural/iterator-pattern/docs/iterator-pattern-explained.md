# The Iterator Pattern, Explained

> **Provide a way to access the elements of an aggregate object sequentially
> without exposing its underlying representation.**
> — *Design Patterns*, Gamma, Helm, Johnson and Vlissides, 1994

The second half of that sentence is the whole pattern. Anybody can hand out
elements one at a time. The point is that the caller never finds out *how the
collection is stored* — in pages, in a tree, in a file, over a network — and
so never writes code that breaks when the storage changes.

## One Loop, Written Once

Before:

```java
int pageNumber = 0;
while (true) {
    List<Product> page = feed.page(pageNumber);
    if (page.isEmpty()) break;
    for (Product product : page) { ... }
    pageNumber++;
}
```

After:

```java
for (Product product : catalogue) { ... }
```

Both walk the same eight products out of the same paged feed. The difference
is where the page loop lives. In the first, it lives at the call site, and
there is a copy of it at every call site. In the second, it lives in
`CatalogueIterator`, once, and there is nothing at the call site to get
wrong.

## Everyday Analogy: A Bookmark

You are reading a book that a friend also wants to read. You do not tell the
book where you are up to — the *bookmark* holds that. Your friend gets their
own bookmark, and the two of you can be on different pages of the same copy
without interfering.

That is exactly the division of labour here. `ProductCatalogue` is the book:
it knows what is in it and nothing about who is reading. `CatalogueIterator`
is the bookmark: it knows where one particular reader has got to. Ask the
catalogue for a second iterator and you get a second bookmark.

This is why `ProductCatalogue` has no `currentPage` field. If it did, two
readers would fight over it, and a loop inside a loop over the same catalogue
would silently produce nonsense.

## Participants

| Role | In the GoF book | Here |
| --- | --- | --- |
| Iterator | `Iterator` | `java.util.Iterator<Product>` — the JDK's, not one we wrote |
| ConcreteIterator | `ConcreteIterator` | `CatalogueIterator` — holds the position, does the paging |
| Aggregate | `Aggregate` | `java.lang.Iterable<Product>` — again the JDK's |
| ConcreteAggregate | `ConcreteAggregate` | `ProductCatalogue` — creates iterators, holds no position |
| Element | — | `Product` |
| The awkward storage | — | `CatalogueFeed` — the paged source being hidden |
| The trap | — | `NaiveCatalogueBrowser` — the page loop, written three times |

Notice that two of the four pattern roles are interfaces Java already ships.
That is unusual and it is worth saying out loud: **Iterator is the one GoF
pattern that is built into the language.** You are not implementing it from
scratch so much as plugging into it.

## Code Walkthrough

### The source being hidden

```java
public List<Product> page(int number) {
    pagesFetched++;
    int from = number * PAGE_SIZE;
    if (from >= everything.size()) {
        return List.of();
    }
    return new ArrayList<>(everything.subList(from, Math.min(from + PAGE_SIZE, everything.size())));
}
```

`CatalogueFeed` is deliberately unpleasant to use. Page numbers from zero, an
empty list for "no more", no count. It also increments `pagesFetched`, which
is not decoration — it is how the tests prove laziness.

### The aggregate

```java
public class ProductCatalogue implements Iterable<Product> {
    private final CatalogueFeed feed;

    @Override
    public Iterator<Product> iterator() {
        return new CatalogueIterator(feed);
    }
}
```

Four lines of real code. Implementing `Iterable` is what buys the for-each
loop: when the compiler sees `for (Product p : catalogue)` over an
`Iterable`, it calls `iterator()` once and then `hasNext()` / `next()` until
told to stop. There is no magic — you can write that loop by hand and get the
identical bytecode.

The other thing `Iterable` buys you is everything else in the ecosystem that
takes one. Enhanced for, `Iterable.forEach`, and a one-liner to a stream if
you want it.

### The iterator

```java
@Override
public boolean hasNext() {
    if (!started) {
        currentPage = feed.page(pageNumber);
        started = true;
    }
    while (indexInPage >= currentPage.size()) {
        if (currentPage.isEmpty()) {
            return false;
        }
        pageNumber++;
        indexInPage = 0;
        currentPage = feed.page(pageNumber);
    }
    return true;
}
```

This is the only page loop in the project, and it is worth reading slowly.

The `while` rather than an `if` matters: it is what makes the iterator
correct if the feed ever returns a *short* page in the middle. The `started`
flag is what makes the walk lazy — nothing is fetched when you call
`iterator()`, only when you first ask whether there is anything there.

`next()` is then three lines, because `hasNext()` has already done the work:

```java
@Override
public Product next() {
    if (!hasNext()) {
        throw new NoSuchElementException("the catalogue has no more products");
    }
    return currentPage.get(indexInPage++);
}
```

Calling `hasNext()` from inside `next()` looks redundant and is not. It is
what makes `next()` safe to call on its own, and it is why `hasNext()` had to
be written so that calling it twice changes nothing.

### The class is package-private

`CatalogueIterator` is not `public`. Callers get one from
`ProductCatalogue.iterator()` and only ever hold it as a
`java.util.Iterator`. The name, the fields and the paging are all invisible
from outside the package, which is the "without exposing its underlying
representation" clause made concrete.

## Why the Tests Are the Proof

Three of the thirteen tests are the ones that would fail if somebody
"simplified" the pattern away.

**Laziness.** Walk two products out of an eight-product catalogue and exactly
one page should have been fetched:

```java
assertEquals(1, feed.pagesFetched());
```

Move the fetching into `ProductCatalogue`'s constructor and this fails
immediately.

**Independent positions.** Two iterators from one catalogue:

```java
outer.next();
outer.next();
assertEquals("SKU-001", inner.next().sku());
```

Put the position in `ProductCatalogue` instead of the iterator and `inner`
starts at SKU-003. This is the test that catches the single most common
mistake people make when writing their first iterator.

**The naive bug, pinned.** `NaiveCatalogueBrowserTest` asserts that
`findCheapest()` returns SKU-005 while the real cheapest is SKU-002 — and
says in the message that if these ever match, the off-by-one has been fixed
and the lesson is gone.

## What You Gain

- **One page loop instead of N.** The paging is written once and reviewed
  once.
- **Callers become readable.** "For each product" says what it means.
- **The storage can change.** Move to cursors, change the page size, switch
  to a local cache — one class changes, and no caller does.
- **Laziness for free.** Stop early and the pages you did not reach are never
  fetched.
- **Nesting works.** Independent positions mean a loop inside a loop over the
  same catalogue is fine.

## What to Watch Out For

**Don't put the position on the aggregate.** If `ProductCatalogue` had
`currentPage` and `next()`, it would be an iterator pretending to be a
collection, and two readers would corrupt each other. The split is the
pattern.

**`hasNext()` must be repeatable.** Callers will call it twice. If your
`hasNext()` consumes something, code that looks obviously correct will skip
elements.

**Don't fetch in the constructor.** It is tempting and it throws the laziness
away.

**Don't reach for it when a `List` will do.** If the collection is already
fully in memory and is a plain list, `List` already gives you an iterator.
Writing one by hand there is ceremony, not design. The pattern earns its keep
when the storage is awkward — paged, remote, lazy, or a tree.

**Modification during iteration is a real question.** The JDK collections
throw `ConcurrentModificationException` rather than silently misbehaving.
This example sidesteps it by copying each page, which is the honest simple
answer for a beginner project; a production iterator over mutable state has
to decide the policy deliberately.

## Iterator vs. Streams vs. for-i

| | Use when |
| --- | --- |
| **Index loop** (`for (int i = 0; ...)`) | You genuinely need the index, and the thing is random-access |
| **Iterator / for-each** | You want each element in turn and do not care how they are stored |
| **Stream** | You want to *describe a pipeline* — filter, map, collect — rather than write the loop |

Streams are built on top of this idea, not opposed to it: `Iterable` and
`Spliterator` are how a stream gets its elements. Understanding the iterator
is what makes the stream stop being magic.

## Where You Have Already Seen It

Every time you have written `for (String s : list)`. Every `Scanner`. Every
`BufferedReader.lines()`. `ResultSet` in JDBC is an iterator with a different
vocabulary (`next()` returning a boolean). Paging iterators over cloud APIs —
the AWS SDK's paginators, for one — are precisely this example with a real
network behind them.

## Try It Yourself

1. Add a ninth and tenth product to `CatalogueFeed.sampleShop()`. Watch
   `NaiveCatalogueBrowserTest.countProductsStopsEarly` start failing while
   every test of the pattern keeps passing.
2. Move the position fields from `CatalogueIterator` onto `ProductCatalogue`
   and see which test catches you.
3. Add a `CategoryCatalogue` that wraps the same feed but only hands out
   products in one category. Nothing outside it should have to change.

## See Also

- [`problem-statement.md`](problem-statement.md) — the problem in full
- [`class-diagram.md`](class-diagram.md) — static structure
- [`uml-diagram.md`](uml-diagram.md) — the call sequence
- [Composite](../../structural/composite-pattern) — iterators over trees are
  where this pattern stops being obvious
- [Strategy](../strategy-pattern) — the other pattern that is mostly "one
  small interface, held by something bigger"
