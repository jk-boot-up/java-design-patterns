# Problem Statement

## The Scenario

You are building the catalog browser for an online store. The catalog is a
tree: `Electronics` contains the `Phone` product directly, and also an
`Accessories` category, which itself contains `Case` and `Charger`
products, plus a nested `Cables` category holding a `USB-C Cable` product.
Categories can hold products, and they can hold *more categories*, to
whatever depth merchandising wants.

You need three operations over that tree: the total price of everything
under a node, how many products it contains, and a nicely indented print of
the whole thing.

## Attempt One: Products and Categories Share Nothing

The obvious shape: a plain class for a product, a plain class for a
category that holds a list of children, and — because a product and a
category are unrelated types — a `List<Object>` to hold either kind.

```java
public final class NaiveCategory {
    private final String name;
    private final List<Object> children = new ArrayList<>();   // Product or Category — who knows
    // ...
}
```

Every operation on this tree now has to ask "what kind of `Object` is this?"
before it can do anything:

```java
public static BigDecimal totalPrice(Object item) {
    if (item instanceof NaiveProduct product) {
        return product.price();
    }
    if (item instanceof NaiveCategory category) {
        BigDecimal sum = BigDecimal.ZERO;
        for (Object child : category.children()) {
            sum = sum.add(totalPrice(child));      // recurse
        }
        return sum;
    }
    throw new IllegalArgumentException("Unknown catalog item: " + item);
}
```

## Why That Hurts

That same `instanceof` chain has to be written **again**, separately, for
`productCount` and for `print` — three copies of the same "which type is
this" logic, one per operation:

- **Every new operation repeats the check.** Want to export the catalog to
  JSON tomorrow? Write a fourth method with the same two-branch `instanceof`
  chain.
- **Every new item type touches every operation.** Add a `Bundle` catalog
  item (a discounted group of products) and all three existing methods need
  a new branch, or they fall through to the `IllegalArgumentException` at
  the bottom.
- **The tree has no shared vocabulary.** A `List<Object>` cannot express
  "a list of things that can each be priced, counted, and printed" — that
  fact only exists inside the `instanceof` chains that happen to agree with
  each other, by convention, not by the compiler.
- **Nothing here is a bug.** `NaiveCatalogPrinter.totalPrice` computes the
  right answer. The waste is structural: the recursion is correct but has
  to be re-derived, and re-verified, in every method that walks the tree.

## The Question This Project Answers

> How do we let client code compute a price, a count, or a printed view
> over a tree that mixes single products and whole subcategories — without
> ever asking "which one is this?"

## The Goal

Give the leaf and the branch **the same type**, so every operation is
written once, polymorphically, and works at any depth for free:

```java
CatalogComponent electronics = new Category("Electronics")
        .add(new Product("Phone", new BigDecimal("599.99")))
        .add(accessories);

electronics.totalPrice();     // sums the whole subtree, recursively, with no instanceof
electronics.productCount();   // same
electronics.print("");        // same
```

A `Product` and a `Category` both answer `totalPrice()`, `productCount()`,
and `print(indent)` the same way a caller sees them: as a
`CatalogComponent`. Whether a given `CatalogComponent` turns out to be one
product or an entire subtree is never the caller's problem.

This is precisely the problem the **Composite** design pattern solves. See
[`composite-pattern-explained.md`](composite-pattern-explained.md) for how.
