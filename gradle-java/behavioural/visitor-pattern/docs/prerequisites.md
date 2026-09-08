# Prerequisites — Visitor

What you need before starting, and the two comparisons that cause the most
trouble.

## Tools

| Tool | Version | Check |
| --- | --- | --- |
| JDK | 21 | `java -version` |
| Gradle | wrapper, no install needed | `./gradlew --version` |

Everything else — JUnit 5, the test runner — is fetched by the wrapper on the
first build.

```bash
./gradlew run     # the walkthrough
./gradlew test    # 70 tests
```

## Do Composite First

This project reuses the catalog tree from
[`structural/composite-pattern`](../../../structural/composite-pattern): the
same Electronics root, the same Accessories and Cables branches, the same
phone, case, charger and cable at the same prices. Three things are added —
stock levels, a restriction flag, and a `Bundle` node — and nothing is taken
away.

That is deliberate. If the structure is already familiar, the whole of your
attention goes on the traversal, which is the only new idea here. If tree
recursion over a `Component` interface is new to you, read Composite first;
this project takes it as given.

## Java You Should Recognise

| Feature | Where it appears | Why it is there |
| --- | --- | --- |
| overloading | `visit(Product)`, `visit(Bundle)`, `visit(Category)` | three methods with one name, picked by the compiler — the mechanism the pattern runs on |
| `default` method | `CatalogVisitor.leave` | most reports do not care about leaving a category, and an empty method that must be written is a place for a mistake to hide |
| `Deque` as a stack | `CategoryPathVisitor` | push on the way in, pop on the way out |
| `LinkedHashMap` | `CategoryCountVisitor` | a report in tree order, so it can be diffed between runs |
| `enum` with fields | `Restriction` | the label and the obligation belong to the value |
| local and nested classes | the demo's `LowStockVisitor`, the tests' visitors | a report written in the file that needs it, proving the model was not touched |
| reflection in tests | `CatalogVisitorTest`, `NaiveCatalogTest` | "the model has no report methods" is a claim about shape, so it is asserted as one |

## The One Thing To Understand First: Overload Resolution

Java picks between overloaded methods using the **static** type of the
argument — what the compiler can see — not the runtime type. Given:

```java
CatalogComponent node = new Product("PHN-900", "Phone", Money.pounds(599.99), 74);
visitor.visit(node);   // does not compile
```

there is no `visit(CatalogComponent)`, and the compiler will not guess. It
does not matter that the object really is a `Product`.

Now move the call inside `Product`:

```java
public void accept(CatalogVisitor visitor) {
    visitor.visit(this);   // here, `this` is a Product
}
```

and it compiles, because in that file the static type is known. That is the
whole trick. `accept` exists to get the call into a place where the compiler
knows the type, and the two hops — `node.accept(v)` then `v.visit(node)` — are
what "double dispatch" names.

If that feels like a lot of ceremony to avoid `instanceof`, hold on to the
feeling. It is a fair objection and the explainer answers it directly.

## Visitor vs Putting The Method On The Composite

The comparison that decides whether you should use this pattern at all, and
the honest answer is *usually not*.

**The question to ask yourself:** *which axis is growing — the node types, or
the operations?*

| | A method on the node | A visitor |
| --- | --- | --- |
| New operation costs | one method × every node class | one new file |
| New node type costs | one new class | one method on the interface × every visitor |
| Where an operation's logic lives | spread across the node classes | in one class, readable end to end |
| Where a node's logic lives | in one class, readable end to end | spread across the visitors |
| Traversal | written once per operation | written once, in the structure |

The table is symmetrical on purpose. Neither column is better; they are the
same trade seen from two ends, and the only thing that breaks the tie is which
axis your codebase is actually growing along.

For a catalog, the answer is clear: the node types have been products and
categories since the shop opened, and finance asks for a new report every
month. For an AST in a language that is still gaining syntax, or a UI toolkit
still gaining widget types, the answer is the other way and Visitor will cost
you a sprint every time you add one.

## Visitor vs `instanceof` And A Switch

Modern Java has pattern-matching switches, and the obvious question is whether
they make Visitor obsolete:

```java
String describe(CatalogComponent node) {
    return switch (node) {
        case Product p  -> p.name();
        case Bundle b   -> b.name() + " (kit)";
        case Category c -> c.name() + "/";
    };
}
```

That is a real and reasonable answer, and for a one-off report it is the
better one — it is shorter, it needs no `accept` method, and if the node
types are `sealed` the compiler will still tell you when you have missed one.

What it does not give you is the traversal. Every report written this way
walks the tree itself, which is the fourth problem in
[`problem-statement.md`](problem-statement.md) with a nicer syntax. And
without `sealed`, the exhaustiveness check goes away and a missed node type
becomes a runtime default rather than a compile error.

Reach for the switch when the operation is small and local. Reach for Visitor
when there are many operations, they need shared traversal and shared state
across the walk, and you want the compiler to enumerate every one of them the
day a node type is added.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the four reports, and the two copies that drifted
2. `NaiveBundle.java` — read its `appendCsvTo` and `auditInto` against `NaiveProduct`'s
3. `CatalogVisitor.java` — the interface, and the paragraph on what it costs
4. `Product.java` and `Category.java` — one line each, and it is the same line
5. [`visitor-pattern-explained.md`](visitor-pattern-explained.md)
6. `./gradlew run`, with [`class-diagram.md`](class-diagram.md) open — section 3 prints the dispatch
7. [`animation.html`](animation.html) — the walk, step by step
