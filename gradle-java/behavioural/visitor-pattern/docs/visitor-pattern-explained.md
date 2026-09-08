# The Visitor Pattern

> Represent an operation to be performed on the elements of an object
> structure. Visitor lets you define a new operation without changing the
> classes of the elements on which it operates.
>
> — *Design Patterns*, Gamma, Helm, Johnson and Vlissides, 1994

Two sentences, and the second one is a promise about *change*, not about
structure. That is the right way to hold this pattern: it is not a way of
walking a tree — Composite already walks the tree — it is a way of deciding
which of your two axes of change is going to be cheap.

## The Shape

```java
public interface CatalogComponent {
    String name();
    void accept(CatalogVisitor visitor);
}

public interface CatalogVisitor {
    void visit(Product product);
    void visit(Bundle bundle);
    void visit(Category category);
    default void leave(Category category) { }
}
```

Every node implements `accept` with the same single line:

```java
@Override
public void accept(CatalogVisitor visitor) {
    visitor.visit(this);
}
```

Copied verbatim into `Product`, `Bundle` and `Category` — and it is not
redundant, because `this` means something different in each file.

`Category` adds the walk:

```java
@Override
public void accept(CatalogVisitor visitor) {
    visitor.visit(this);
    for (CatalogComponent child : children) {
        child.accept(visitor);
    }
    visitor.leave(this);
}
```

That is the whole pattern. Everything else in this project is a report.

## Why `accept` Exists

The question everybody asks first: why not just call `visitor.visit(node)`?

```java
CatalogComponent node = someProduct();
visitor.visit(node);   // does not compile
```

Java resolves overloads at compile time from the **static** type of the
argument. At that call site the static type is `CatalogComponent`, there is no
`visit(CatalogComponent)`, and the compiler refuses to guess — it does not
matter that at runtime the object is a `Product`.

Inside `Product.accept`, the static type of `this` is `Product`. The same call
now compiles, and it compiles to `visit(Product)` permanently, when
`Product.java` is compiled.

So the two hops do two different jobs:

| Hop | Chooses | When | Using |
| --- | --- | --- | --- |
| `node.accept(v)` | which `accept` | runtime | the node's class |
| `v.visit(this)` | which `visit` | compile time | the enclosing class |

Together they pick a method from the combination of two types, which is what
*double dispatch* names. Java gives you single dispatch — on the receiver —
and `accept` is the trick that gets you the second one.

**This is genuinely awkward to read.** Two calls to reach one method, and the
reason is a fact about overload resolution rather than a fact about catalogs.
A reader who does not already know the pattern will not derive it from the
code. That is a real cost, it is paid on every read, and the only thing that
justifies it is the number of reports on the other side of the ledger.

## The Four Reports

Each is a class, and none of them required a line of change to the model.

**Inventory value.** The simplest one, and the clearest illustration that one
method per node type lets each rule be a plain sentence:

```java
@Override
public void visit(Product product) {
    total = total.plus(product.price().times(product.stockOnHand()));
}

@Override
public void visit(Bundle bundle) {
    // The kit price, not the contents.
    total = total.plus(bundle.price().times(bundle.stockOnHand()));
}
```

A kit sells for less than its parts, so valuing it at the sum of its contents
reports stock the shop cannot realise. Two methods, two sentences, no `if`.

**Count by category.** The report that could not have been a method on
`Product`, because in this tree nothing points upwards. A product does not
know its category; the answer exists only during the walk. `visit(Category)`
pushes the name, `leave(Category)` pops it, and counting is what is left.

**CSV export.** Read what is in this class: a header, a quoting rule, and a
decision about how a bundle is rendered. Three facts about spreadsheets, none
of them a fact about a product — and in the naive design all three live on the
domain classes, the quoting rule twice.

**Compliance audit.** The report `Bundle` exists for. A product is restricted
or it is not; a bundle is restricted by what is in the box:

```java
@Override
public void visit(Bundle bundle) {
    for (Product content : bundle.contents()) {
        if (content.restriction().isRestricted()) {
            record(...);
        }
    }
}
```

There is nowhere else that loop could go. The bundle carries no restriction of
its own to read — which is exactly the mistake `NaiveBundle` makes, by reading
a field it copied from `NaiveProduct` and never sets.

## Where The Traversal Lives, And What That Costs

The walk is in `Category.accept`, not in the visitors. Written once, it cannot
be written differently the fourth time, and every report gets depth-first,
parents-first, insertion-ordered traversal for free — including the report you
write next year. `CatalogVisitorTest.traversalIsNotInTheVisitor` makes the
point by counting: a visitor with no loop and no recursion in it sees all
seventeen calls of the demo tree.

The cost is that **a visitor cannot prune**. A report interested only in
Accessories still walks all of Electronics and filters, because there is no
exit from the walk that a report controls.

The alternative — an *external* iterator that the visitor drives — hands
control back and lets a report stop early, at the price of every report
writing its own walk, which is the problem this pattern was brought in to
solve. There is a middle road, a `boolean` return from `visit(Category)`
meaning "do not descend", and it is worth knowing about; it is left out here
because it makes the interface harder to explain and this catalog is small.

## The Cost, Stated As Plainly As The Benefit

Adding a fourth node type — a gift card, a digital download — means adding a
method to `CatalogVisitor`, and **every implementation stops compiling until
it is written**. Six today:

```
    InventoryValueVisitor
    CategoryCountVisitor
    CsvExportVisitor
    ComplianceAuditVisitor
    DispatchTraceVisitor
    LowStockVisitor
```

and the list only ever grows, because reports are never deleted. The naive
design takes a new node type in its stride: one new class, and nothing else
recompiles.

Some people call the compile errors a feature — the compiler enumerating every
report that now has a decision to make — and when the new node type genuinely
does need a rule in every report, that is fair. When it does not, you are
writing five empty methods to satisfy the compiler, and five empty methods is
where a real one goes missing.

**Visitor is only correct when you are confident the structure is settled.**
In a catalog it is: products and categories have been the node types since the
shop opened, and finance asks for a new report every month. In an AST for a
language still gaining syntax, or a UI toolkit still gaining widgets, the
answer is the other way round and this pattern will cost you a sprint every
time a type is added.

## Pitfalls

**Putting a method on the node "just this once".** The fifth report is always
smaller than the fourth, and a method on `Product` is always quicker than a
new file. Do it twice and the model is back to knowing about spreadsheets.
`CatalogVisitorTest.theModelHasNoReportingMethods` is a guard against exactly
this, and it fails with a message that says why.

**A visit method that recurses.** If a visitor loops over
`category.children()` itself, the tree is walked twice — once by
`Category.accept` and once by the visitor — and the totals silently double.
Let the structure walk.

**Visiting a bundle's contents as nodes.** `Bundle.accept` does not descend
into the box, on purpose: the phone in the Starter Kit is already a node
elsewhere in the catalog, and walking into the box would count its stock
twice. The compliance audit reads `contents()` directly because it wants to
inspect them, not to visit them, and those are different things.

**Stateful visitors reused carelessly.** A visitor accumulates. Walking two
trees with one instance adds them together, which is a feature —
`aVisitorAccumulatesAcrossTrees` asserts it — and a bug the moment you meant
to ask two separate questions. Make a new one per report.

**Reaching for it too early.** Two operations over a stable structure do not
need this. Write the two methods. The demo agrees: sections 1 and 2 show the
naive inventory value and category counts agreeing to the penny, and that part
of the naive design is not criticised anywhere in this project.

## Comparisons

### Visitor vs putting the method on the Composite

The comparison that decides whether to use the pattern at all.

**The question to ask yourself:** *which axis is growing — the node types, or
the operations?*

| | A method on the node | A visitor |
| --- | --- | --- |
| New operation costs | one method × every node class | one new file |
| New node type costs | one new class | one method × every visitor |
| An operation's logic is | spread across the node classes | in one class, end to end |
| A node's logic is | in one class, end to end | spread across the visitors |
| Traversal | once per operation | once, in the structure |

Neither column is better. It is the same trade from two ends, and the tie is
broken only by which axis your codebase actually grows along. Count the two
numbers in your own repository — node types, and operations over them — and
pick the cheap direction. In this project they are 3 and 6, and moving in one
direction.

### Visitor vs `instanceof` and a pattern-matching switch

```java
return switch (node) {
    case Product p  -> ...;
    case Bundle b   -> ...;
    case Category c -> ...;
};
```

Shorter, needs no `accept`, and with `sealed` types the compiler still catches
a missed case. For a single local operation it is the better answer, and
saying otherwise would be pattern-worship.

What it does not give you is the shared traversal or the shared state across
the walk, so every report written this way walks the tree itself. Reach for
the switch when the operation is small and local; reach for Visitor when there
are many operations that need the same walk.

### Visitor vs Composite

Composite is the tree. Visitor is what you do to it. This project's model is
[`structural/composite-pattern`](../../../structural/composite-pattern)'s
model with `accept` added and the report methods taken away — the two patterns
are neighbours, not alternatives, and Visitor is the usual answer to what
Composite's `Component` interface should do when the operations keep coming.

### Visitor vs Strategy

Both hand behaviour to an object passed in. A
[Strategy](../../strategy-pattern) is chosen for *one* call and knows nothing
about structure; a visitor is carried across a whole walk and has a method per
node type. If your "strategy" has grown one method per subclass of the thing
it operates on, it has become a visitor and may as well say so.

## Further Reading

- *Design Patterns*, chapter 5 — the original, and the source of the
  "structure must be stable" warning, which is usually quoted less often than
  the benefit
- [`structural/composite-pattern`](../../../structural/composite-pattern) —
  the tree this project reports on
- `CatalogVisitorTest` — the mechanism asserted, including the cost
- `NaiveCatalogTest` — the two drifted copies, pinned as passing tests
