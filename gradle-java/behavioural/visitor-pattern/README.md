# Visitor Pattern

Demonstrates the Behavioural **Visitor** design pattern using the reports an
online shop runs over its product catalog as an example. The catalog itself is
the tree from [`composite-pattern`](../../structural/composite-pattern) — read
that project first if you have not; this one adds nothing to the structure but
the question of what to *do* with it.

- `CatalogComponent` — the Element role, and the smaller half of the pattern.
  Two methods: `name()`, and `accept(CatalogVisitor)`. That second one is the
  last method this interface ever needs, because every future report arrives as
  a new visitor rather than as a new method here.
- `Product` / `Bundle` / `Category` — the three node types, and the reason
  double dispatch earns its keep. A product is worth its price times its stock;
  a `Bundle` is a kit sold at its own price, so it is worth *that* times its
  stock and not the sum of its parts. A product is restricted or it is not; a
  bundle has no restriction of its own and is restricted by what is in the box.
  Two node types, two genuinely different rules, twice over. `Category` is the
  Composite, and it is where the traversal lives — written once, for every
  report there will ever be.
- `CatalogVisitor` — the Visitor role: one `visit` overload per node type, plus
  a `leave(Category)` default for reports that track where they are. Its
  Javadoc states the cost as plainly as the benefit, because a fourth node type
  breaks every implementation of it.
- `InventoryValueVisitor` / `CategoryCountVisitor` / `CsvExportVisitor` /
  `ComplianceAuditVisitor` — the four reports the business asked for. None of
  them contains a loop over children, an `instanceof`, or a `switch` on type.
  `CsvExportVisitor` holds the RFC 4180 quoting rule in one place;
  `ComplianceAuditVisitor` is the one whose `visit(Bundle)` walks the contents,
  which is a rule that in the naive design had nowhere to live.
- `CategoryPathVisitor` — an abstract base that tracks the current path using
  `visit(Category)` and `leave(Category)`. It is a convenience, and its Javadoc
  says so: it is **not** part of the pattern, and `InventoryValueVisitor`
  deliberately does not extend it.
- `DispatchTraceVisitor` — a report whose only output is the shape of the walk,
  so section 3 of the demo can show `accept` and `visit` interleaving.
- `NaiveCatalogNode` / `NaiveProduct` / `NaiveBundle` / `NaiveCategory` — the
  trap, kept for contrast. Five methods on the interface: `name()`, and one per
  report. Its inventory total is correct to the penny on purpose — the argument
  is drift, not incompetence. `NaiveBundle` was copied from `NaiveProduct` and
  lost the CSV quoting on the way, and it reads a `restriction` field that came
  across with the copy and is never set. Both are pinned by *passing* tests.
- `Catalog` — the demo tree, built twice and identically, so the comparison is
  a comparison of designs rather than of data.
- `Restriction` / `Money` — the supporting types.
- `CatalogReportDemo` — runnable entry point: the four reports on the model,
  the same four as visitors, the dispatch trace, a fifth report written this
  morning inside the demo file, and an honest section on what the pattern cost.

## Run

```bash
./gradlew run
```

```
=== 1. The trap: four reports, written on the model ===

  Report 1 - inventory value: £78,609.86
  Report 2 - lines in Electronics/Accessories: 4
  Both correct. Two methods on three classes, and nobody minded.

  Report 3 - the CSV export, two rows of it:
    Electronics/Accessories,CLN-003,"Screen Cleaner, 200ml",product,6.50,190,flammable   (7 fields)
    Electronics/Kits,KIT-01,Starter Kit, 3 items,bundle,639.00,25,   (8 fields)
  NaiveProduct quotes its fields. NaiveBundle was copied
  from it and the quoting was dropped, because on that day
  no kit had a comma in its name. Marketing added one.

  Report 4 - the compliance audit, 2 findings:
    Electronics/Accessories/Spare Battery Pack BAT-014  lithium cell   UN3481 declaration required for air freight
    Electronics/Accessories/Screen Cleaner, 200ml CLN-003  flammable      road freight only, no air
  The Starter Kit has a lithium cell in the box and is not
  on the list. NaiveBundle.auditInto reads a restriction
  field it copied from NaiveProduct and never sets. The
  shipment is filed as clear for air freight.

=== 2. The pattern: the same four reports, as visitors ===

  Report 1 - inventory value: £78,609.86 across 7 lines, 1229 units

  Report 2 - lines by category:
    Electronics                     1 here   7 in total
    Electronics/Accessories         4 here   5 in total
    Electronics/Accessories/Cables  1 here   1 in total
    Electronics/Kits                1 here   1 in total
    Electronics/Clearance           0 here   0 in total
  Clearance is empty and still on the report, because the
  category is registered on the way in rather than by a
  product mentioning it.

  Report 3 - the CSV export, the same two rows:
    Electronics/Accessories,CLN-003,"Screen Cleaner, 200ml",product,6.50,190,flammable   (7 fields)
    Electronics/Kits,KIT-01,"Starter Kit, 3 items",bundle,639.00,25,   (7 fields)
  One quoting rule, in one class, applied to every node.

  Report 4 - the compliance audit, 3 findings from 7 lines:
    Electronics/Accessories/Spare Battery Pack BAT-014  lithium cell   UN3481 declaration required for air freight
    Electronics/Accessories/Screen Cleaner, 200ml CLN-003  flammable      road freight only, no air
    Electronics/Kits/Starter Kit, 3 items KIT-01   lithium cell   UN3481 declaration required for air freight (from Spare Battery Pack in the box)
  clear for air freight: false
  The kit is on the list. visit(Bundle) is a different
  method from visit(Product), so the rule that a bundle
  inherits what is in the box had somewhere to be written.

  Four reports. Product.java, Bundle.java and Category.java
  have one method between them about reporting, and it is
  the same method on all three: accept.

=== 3. How each node found its method ===

  visit(Category)  Electronics/
  visit(Product)   Phone
  visit(Category)    Accessories/
  visit(Product)     Case
  visit(Product)     Charger
  visit(Product)     Spare Battery Pack
  visit(Product)     Screen Cleaner, 200ml
  visit(Category)      Cables/
  visit(Product)       USB-C Cable
  leave(Category)      Cables/
  leave(Category)    Accessories/
  visit(Category)    Kits/
  visit(Bundle)      Starter Kit, 3 items
  leave(Category)    Kits/
  visit(Category)    Clearance/
  leave(Category)    Clearance/
  leave(Category)  Electronics/

  5 categories, 6 products, 1 bundle, and no instanceof.
  Each node called visitor.visit(this) from inside its own
  class, where the compiler knows what this is. That bounce
  through accept is the double dispatch, and it is the price
  of the type test never being written.

  The order came from Category.accept, once, and every
  report above walked the tree in exactly this order.

=== 4. A fifth report, asked for this morning ===

    Phone                   74 left, £599.99 a unit
    Spare Battery Pack      62 left, £34.99 a unit
    Starter Kit, 3 items    25 left, £639.00 a unit

  £64,854.36 of cover to buy back to 100 units.

  LowStockVisitor is a private class inside this demo file.
  Adding it changed no interface, no node type and no other
  report. In the naive design it is a fifth method on
  NaiveCatalogNode and three more implementations of it.

=== 5. What it cost ===

  Add one node type -- a gift card, say -- and CatalogVisitor
  gains a method. These stop compiling until it is written:
    InventoryValueVisitor
    CategoryCountVisitor
    CsvExportVisitor
    ComplianceAuditVisitor
    DispatchTraceVisitor
    LowStockVisitor
  Six today, and the list only ever grows. The naive design
  takes a new node type in its stride: one new class, and
  nothing else recompiles. That is the trade, and it is not
  a small one.

  A visitor cannot stop early: 0 lines from an empty category,
  but a report wanting only Accessories still walks all of
  Electronics. The traversal lives in Category.accept, which
  is what stops six reports each getting it slightly wrong,
  and it is also what takes pruning away from them.

  And node.accept(v) calling v.visit(node) straight back is
  not obvious code. Two calls to reach one method, and the
  reason is a fact about how Java picks overloads.

  Use this when the node types are settled and the reports
  are not. In a catalog that is true. Reach for it in a
  hierarchy that is still growing types and you will spend
  every sprint editing every visitor.
```

Sections 1 and 2 answer the same four questions about the same catalog. The
CSV row and the audit are where they differ, and neither difference is a bug
anybody wrote — they are what four near-identical implementations of one idea
do over eighteen months. Section 5 is the other half of the story: the six
class names printed there are the ones a single new node type would break.

## Test

```bash
./gradlew test
```

70 tests across three classes.

`CatalogVisitorTest` asserts the things only Visitor gives you, using a
recording visitor declared in the file. `aReportWrittenLaterStillWorks`
declares a whole report class *inside the test method* and walks a tree whose
classes were compiled long before it existed — if that passes, "extension
without modification" is a property rather than a slogan.
`traversalIsNotInTheVisitor` makes the same point by counting: a visitor with
no loop and no recursion in it still receives all 17 calls.
`theModelHasNoReportingMethods` is a reflection test with an allow-list, and it
fails the build if anybody ever adds a report method back onto `Product`.

And `aVisitorSeesTheWholeTree` asserts the **cost**: a report that only wants
Accessories is offered 7 nodes and wants 5, because the walk belongs to the
structure and no report can prune it.

`ReportVisitorTest` pins each of the four reports — the £78,609.86 total across
7 lines and 1,229 units, the empty `Clearance` category that still appears on
the count report, the quoted bundle name, and the 3 audit findings including
the one inside the kit.

`NaiveCatalogTest` pins the two seeded bugs as passing tests, each paired with
the visitor answering the same question correctly. That pairing is what makes
the README's comparison checkable rather than rhetorical.

## Learning Material

Start here if you are new to the pattern — the docs are ordered as a
learning path.

| Document | What it covers |
| --- | --- |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What to know and install first — including why Composite comes before this |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The problem the pattern solves, and why the naive approach hurts |
| [`docs/visitor-pattern-explained.md`](docs/visitor-pattern-explained.md) | The pattern itself, the code walked through, pitfalls, and comparisons |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Static structure — two hierarchies, and the one arrow between them |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Runtime call flow — the two hops of double dispatch, and the audit finding the naive version misses |
| [`docs/animation.html`](docs/animation.html) | Animated, step-by-step walkthrough — open in a browser. Optional narration via the **Narration** button |
| [`docs/session.md`](docs/session.md) | A 60-minute guided session plan for teaching it |
| [`docs/youtube.md`](docs/youtube.md) | Title, description, chapters and thumbnail for publishing the video |
| [`docs/thumbnail.png`](docs/thumbnail.png) | The 1280×720 image to upload as the YouTube thumbnail |
| [`docs/spec.md`](docs/spec.md) | The project specification — problem, code, video and publishing quality bar. Also as [`spec.html`](docs/spec.html) |
| [`video/`](video/) | A narrated video, plus the script and build pipeline |

### The pattern in one picture

![Visitor class diagram](docs/images/class-diagram.png)

### Video

`video/visitor-pattern-explained.mp4` — 1080p, narrated. An audio-only version
is alongside it. See [`video/README.md`](video/README.md) to rebuild or
re-record it.
