# Problem Statement

## The Scenario

You are working on an online shop. The product catalogue does not live in
your application — it lives in the warehouse system, and you read it over an
API.

That API will not give you the whole catalogue at once. Nobody's API will:
sending forty thousand products in one response is slow, expensive, and falls
over the first time the catalogue grows. So it gives you a **page** at a time:

```java
List<Product> page(int number)   // page 0, page 1, page 2, ...
```

You ask for page 0. You get three products. You ask for page 1. Three more.
Eventually you ask for a page and get an empty list back, and that is how you
know you have reached the end. There is no `size()`, no `hasMorePages()`,
nothing else to go on.

Meanwhile, the rest of the shop just wants products. The search page wants to
filter them. The sitemap generator wants all of them. The "cheapest in stock"
badge wants the lowest price. None of those three features is about paging.
Paging is an accident of how the warehouse stores things.

## Attempt One: Everybody Writes the Page Loop

The obvious thing is to write the loop where you need it:

```java
public List<Product> allProducts() {
    List<Product> found = new ArrayList<>();
    int pageNumber = 0;
    while (true) {
        List<Product> page = feed.page(pageNumber);
        if (page.isEmpty()) {
            break;
        }
        found.addAll(page);
        pageNumber++;
    }
    return found;
}
```

That is correct. It is also eleven lines to say "look at every product", and
— this is the part that matters — it is eleven lines that the *next* feature
will have to write again.

So the second feature writes it again, and caps the loop at three pages,
because an unbounded `while (true)` against a remote API makes people
nervous:

```java
public int countProducts() {
    int count = 0;
    for (int pageNumber = 0; pageNumber < 3; pageNumber++) {
        count += feed.page(pageNumber).size();
    }
    return count;
}
```

And the third feature writes it again, and starts at page 1, because of a
misreading of the API docs that nobody catches in review:

```java
public Product findCheapest() {
    Product cheapest = null;
    int pageNumber = 1;              // <- pages count from zero
    while (true) {
        ...
    }
}
```

You can run all three. `NaiveCatalogueBrowser` is in this project, and
`NaiveCatalogueBrowserTest` holds their behaviour in place.

## Why That Hurts

**The bugs are silent.** Neither broken method throws. `countProducts()`
returns a number, and the number is even right today — the catalogue has
eight products and three pages, so the cap happens not to bite. It starts
lying the day somebody adds a tenth product, which is to say on a day nobody
is looking at this code.

**The wrong answer is plausible.** `findCheapest()` returns a real product at
a real price. It is simply not the cheapest one. The £4 socks are on page 0,
the page this method never asks for, so the shop advertises "from £8" and
quietly loses the comparison against a competitor.

**The loop is the same every time, and wrong differently every time.** Three
copies, three chances to get the start index, the stop condition or the
increment wrong. Nothing forces the copies to agree.

**Paging leaks into code that has nothing to do with paging.** The method
that finds the cheapest product is now partly about HTTP pagination. If the
warehouse ever switches to cursors, or changes the page size, or starts
signalling the end with a flag instead of an empty page, every one of those
copies has to be found and changed.

**You cannot stop early without wasting work.** A page that shows the first
two products still runs the loop that fetches everything, because the loop
does not know you only wanted two.

## The Question This Project Answers

> How do you let every part of the shop walk through the catalogue, one
> product at a time, without any of them knowing that the catalogue arrives
> in pages — and without writing the page loop more than once?

## The Goal

Make this work, and make it be the whole story:

```java
for (Product product : catalogue) {
    ...
}
```

No page numbers. No stop condition. No copy of anything. And, because the
walk is lazy, no page fetched that the caller never reached.
