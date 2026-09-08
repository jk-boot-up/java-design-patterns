# Problem Statement — Catalog Reports

The catalog is a tree. Categories hold products, bundles and other
categories, and it has looked like that since
[`structural/composite-pattern`](../../../structural/composite-pattern) built
it — the same Electronics root, the same Accessories and Cables branches, the
same phone, case, charger and cable.

What changes is not the tree. It is what the business wants to know about it:

| Asked by | Report |
| --- | --- |
| finance, at year end | what is the stock in the warehouse worth? |
| merchandising | how many lines sit in each category? |
| finance, every Monday | a CSV of the whole catalog for the spreadsheet |
| shipping | which items need a dangerous-goods declaration? |

Four questions over one structure. Written the obvious way, that is four
methods on the nodes:

```java
public interface NaiveCatalogNode {
    String name();
    Money inventoryValue();
    void countInto(Map<String, Integer> counts, String path);
    void appendCsvTo(StringBuilder out, String path);
    void auditInto(List<String> findings, String path);
}
```

Read it on its own and there is nothing wrong with it. Each method is the
shortest correct way to answer its question, they are all in the classes they
are about, and there is no indirection anywhere. **For two reports this is the
right answer**, and the demo says so out loud: sections 1 and 2 agree to the
penny on inventory value and on the category counts. What follows is what
happened by the fourth report and the third year.

## What Goes Wrong

### 1. A report is a change to the domain model

`inventoryValue` is arguably about a product. `appendCsvTo` is not. It is
about RFC 4180 — that a field containing a comma is wrapped in double quotes,
and a quote inside it is doubled — and it lives in a class whose job is to
describe a thing on a shelf.

So a private `quote` method appears on `NaiveProduct`. And on `NaiveBundle`,
because it needed one too. The rule is now in the codebase twice, in two
classes that have no other reason to know it exists.

### 2. Knowing it twice is how it gets known differently

`NaiveBundle` was written eighteen months after `NaiveProduct`, by copying it.
The copy dropped the `quote` calls. Nothing failed: no kit had a comma in its
name that year.

```
    Electronics/Accessories,CLN-003,"Screen Cleaner, 200ml",product,6.50,190,flammable   (7 fields)
    Electronics/Kits,KIT-01,Starter Kit, 3 items,bundle,639.00,25,   (8 fields)
```

Marketing renamed the kit to "Starter Kit, 3 items". Finance's spreadsheet
gained a column, silently, in one row.

### 3. And the copy that matters is the compliance one

`NaiveProduct.auditInto` reads the product's restriction field. `NaiveBundle`
was copied from it, so it reads *its* restriction field — a field that was
copied across with the rest of the class and is never set.

A bundle has no restriction of its own. It is restricted by what is in the
box, and the Starter Kit contains a lithium cell:

```
  Report 4 - the compliance audit, 2 findings:
    Electronics/Accessories/Spare Battery Pack BAT-014  lithium cell   UN3481 declaration required for air freight
    Electronics/Accessories/Screen Cleaner, 200ml CLN-003  flammable      road freight only, no air
```

The kit is not on the list. The shipment is filed as clear for air freight
with an undeclared lithium cell in it. `NaiveCatalogTest` pins this as a
passing test, because it is what the code does today.

### 4. The traversal is written once per report

Every report method on `NaiveCategory` is the same loop over the same
children with a different body. Four reports, four loops. A fifth report is a
fifth chance to recurse in a different order from its neighbours, or to
forget to recurse at all — and nothing about the interface would notice.

### 5. Adding a report edits three files that were finished

`NaiveCatalogNode` gains a method and every implementation must supply one.
The fifth report is a fifth method on the interface and three more
implementations of it, all in classes whose last real change was to the
domain.

## What We Actually Want

- **A new report to be a new file**, and nothing else.
- **One traversal**, written once, that every report gets for free.
- **One quoting rule**, in the class that is about CSV.
- **Different node types handled differently on purpose** — a bundle valued at
  its kit price and audited by what is inside it — without an `instanceof`
  chain in every report.
- **The domain classes to stay about the domain.** A `Product` should have no
  opinion about spreadsheets.

## What This Costs

Visitor buys all five, and the price is real and is charged to the node types.
Adding a fourth kind of node — a gift card, a digital download — means a new
method on `CatalogVisitor`, and *every* visitor stops compiling until it is
written. Six visitors exist in this project today and the list only ever
grows. The naive design takes a new node type in its stride: one new class,
and nothing else recompiles.

That is the trade, and it only comes out in your favour when the node types
are settled and the reports are not. In a catalog that is true — the shape of
a shop's catalog changes about once a decade, and the reports finance asks for
change monthly. It is genuinely not true everywhere.

Two smaller costs, stated rather than buried. A visitor cannot prune: the walk
lives in `Category.accept`, so a report that wants only Accessories still
sees all of Electronics and filters. And `node.accept(visitor)` calling
`visitor.visit(node)` straight back is two calls to reach one method, for a
reason that is a fact about Java overload resolution rather than about
catalogs. Nobody finds that obvious the first time.

Section 5 of the demo prints the whole bill, including the names of the six
classes a new node type would break.
