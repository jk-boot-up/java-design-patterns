# The Composite Pattern — Explained

## One-Line Definition

> **Composite** composes objects into tree structures to represent
> part-whole hierarchies. Composite lets clients treat individual objects
> and compositions of objects uniformly.
> — *Gang of Four, Design Patterns*

It is a **structural** pattern: it is about how objects are *composed into
a tree*, not about how they are created (Singleton, Prototype, Builder) or
how they behave over time.

## The One Idea That Matters: Same Type, Different Shape

A `Product` is a single item. A `Category` is a whole subtree of products
and other categories. They could not look more different on the inside —
one has a price, the other has a list of children. The pattern's entire
trick is giving them **the same public type**, `CatalogComponent`, so that
from the outside, a caller cannot tell — and does not need to tell —
whether it is holding one leaf or an entire branch.

> If a caller ever needs to ask "is this a leaf or a composite?" before it
> can act, the pattern has not been applied yet.

## The Everyday Analogy

Think of a company **org chart**. Ask any employee, from an intern to the
CEO, "how many people do you manage, including everyone under everyone
under you?" An individual contributor answers "one — myself." A manager
adds up the same answer from everyone reporting to them, recursively. The
question is identical at every level of the chart; only the answer's
arithmetic changes depending on whether you landed on a leaf or a branch.

`Product.productCount()` always answers `1`. `Category.productCount()`
answers "the sum of my children's answers." Neither needs to know how deep
the org chart goes below it.

## The Participants

| Role | In this project | Job |
| --- | --- | --- |
| **Component** | `CatalogComponent` | Declares the operations every node answers, leaf or branch alike |
| **Leaf** | `Product` | A component with no children; `productCount()` is always `1` |
| **Composite** | `Category` | A component that holds children and delegates every operation to them, then combines the results |
| **The trap** | `NaiveProduct` / `NaiveCategory` / `NaiveCatalogPrinter` | No shared type, so every operation re-derives the same `instanceof` chain |
| **Client** | `CatalogDemo` | Builds a tree and calls the same three methods on it, never checking what kind of node it has |

## How This Project Implements It

### The component declares a shared vocabulary

```java
public interface CatalogComponent {
    String name();
    BigDecimal totalPrice();
    int productCount();
    void print(String indent);
}
```

Every operation the catalog needs is declared exactly once, here — not once
per concrete type.

### The leaf answers for itself, and nothing else

```java
public final class Product implements CatalogComponent {
    private final String name;
    private final BigDecimal price;

    @Override public BigDecimal totalPrice()  { return price; }
    @Override public int productCount()       { return 1; }
}
```

A `Product` has no children, so its answers are trivial: its own price, a
count of one. There is no recursion here because there is nothing left to
recurse into.

### The composite delegates and combines

```java
public final class Category implements CatalogComponent {
    private final List<CatalogComponent> children = new ArrayList<>();

    @Override
    public BigDecimal totalPrice() {
        BigDecimal sum = BigDecimal.ZERO;
        for (CatalogComponent child : children) {
            sum = sum.add(child.totalPrice());   // works whether child is a Product or another Category
        }
        return sum;
    }
}
```

That loop never asks what kind of `CatalogComponent` each child is. A
`Product` child returns its own price; a `Category` child returns the sum
of *its* children, already computed by this same method one level down.
The recursion is implicit in the fact that `Category` is itself a
`CatalogComponent`.

### The trap, for contrast

`NaiveCategory` holds `List<Object>` because `NaiveProduct` and
`NaiveCategory` share no common supertype. `NaiveCatalogPrinter` then has to
write the same `instanceof NaiveProduct` / `instanceof NaiveCategory`
chain three times — once each for `totalPrice`, `productCount`, and
`print` — computing identical results to the composite version, but with
the type-checking logic duplicated across every operation instead of
declared once.

## What You Gain

- **One recursive definition per operation**, not one per concrete type
  times one per operation. `Category.totalPrice()` is the *only* place
  "sum my children" is written.
- **New tree depth is free.** Nesting a `Category` ten levels deep needs no
  new code anywhere — the same `totalPrice()` method already handles it,
  because a `Category`'s children are `CatalogComponent`s, which might
  themselves be `Category`s.
- **Uniform client code.** `CatalogDemo` iterates over
  `electronics.children()` and calls `totalPrice()` / `productCount()` on
  each without ever checking what it got back.
- **The trap and the fix compute identical answers.** `NaiveCatalogPrinter`
  and the composite tree agree on every number — the pattern changes *how
  the logic is organized*, not what it produces.

## What to Watch Out For

- **Adding a child-management method to the Component interface is a
  trap of its own.** If `add(CatalogComponent)` lived on `CatalogComponent`
  instead of just on `Category`, every `Product` would need a meaningless
  implementation (throw, or silently do nothing) purely to satisfy the
  interface. This project keeps `add` on `Category` only, deliberately, at
  the cost of client code needing a `Category` reference (not just a
  `CatalogComponent`) when it wants to build the tree.
- **Composites need real recursion, not just delegation to one child.** A
  `Category.totalPrice()` that only asked its first child would silently
  drop every product past the first one. Test the recursive case, not just
  a category with one leaf.
- **Mutable children lists shared by reference are a hazard.** `Category`
  copies nothing on `add`, but does return an unmodifiable view from
  `children()`, so a caller cannot corrupt the tree structure by mutating
  what they were only supposed to read.
- **Cycles will recurse forever.** Nothing stops a `Category` from
  (accidentally) containing an ancestor of itself; `totalPrice()` would
  recurse until the stack overflows. The pattern assumes a tree, not an
  arbitrary graph.

## Composite vs. Similar Patterns

| Pattern | Intent | Key difference |
| --- | --- | --- |
| **Composite** | Treat a single object and a tree of objects through one interface | About *structure* — part/whole hierarchies of arbitrary depth |
| **Decorator** | Attach responsibilities to one object dynamically | Wraps a single component in a single wrapper; no branching children |
| **Flyweight** | Share intrinsic state across many fine-grained objects | About *identity* — many contexts pointing at few shared instances |
| **Facade** | Simplify a complex subsystem behind one entry point | One-way simplification of unrelated subsystems, not a recursive tree |

The shortest way to remember it: **Decorator wraps one thing in one more
layer. Composite lets one thing *be* many things, arranged in a tree.**

## Where You Have Already Seen It

- The DOM in a browser — every node, from a single `<span>` to an entire
  `<div>` full of children, implements the same `Node` interface
- Filesystems — a file and a directory both answer "what is your size?",
  and a directory's answer sums its contents, recursively
- Swing/AWT and most GUI toolkits — a `Component` and a `Container` (which
  holds `Component`s, including other `Container`s) share one base type
- Organization charts and menu systems — a single dish and a whole combo
  meal both have a price; the combo's price sums its parts

## Try It Yourself

1. Run `./gradlew run` and read the printed tree — notice `print(indent)`
   never checks whether it is printing a `Product` or a `Category`.
2. Add a third level of nesting (a category inside `Cables`) and confirm
   `totalPrice()` and `productCount()` need no code changes to handle it.
3. Try adding an `add(CatalogComponent)` method to the `CatalogComponent`
   interface itself, then implement it on `Product`. Notice there is no
   sensible behavior for a leaf to have — that dead end is why `add` stays
   on `Category` only in this implementation.

## See Also

- [`problem-statement.md`](problem-statement.md) — the problem this solves
- [`class-diagram.md`](class-diagram.md) — static structure
- [`uml-diagram.md`](uml-diagram.md) — runtime call flow
- [`animation.html`](animation.html) — animated walkthrough
