# Session Guide — Visitor

A 60-minute guided session for teaching or self-studying the Visitor pattern
using this project.

- **Audience:** developers comfortable with core Java and with tree recursion
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md), and ideally
  [`structural/composite-pattern`](../../../structural/composite-pattern)
  first — this project reports on that project's tree

> **Optional pre-work.** Ask participants to watch the video
> (`video/visitor-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises, which are the part of this session that actually lands.

## Learning Objectives

By the end of this session a participant should be able to:

1. Explain what double dispatch is, and why `visitor.visit(node)` does not
   compile when `node` is declared as a `CatalogComponent`.
2. Say why `accept` is not redundant even though every implementation of it is
   the same line of code.
3. State the trade in both directions — cheap operations, expensive node
   types — and name which axis their own codebase is growing along.
4. Point at where the traversal lives and say what that buys and what it takes
   away.
5. Decide, out loud and with reasons, when *not* to use this pattern.

## Timetable

| Time | Segment | Mode |
| --- | --- | --- |
| 0:00–0:05 | Setup check | Hands-on |
| 0:05–0:16 | The problem | Discussion |
| 0:16–0:28 | Double dispatch | Explanation |
| 0:28–0:41 | Code walkthrough | Live coding |
| 0:41–0:52 | Exercises | Hands-on |
| 0:52–0:58 | The cost | Discussion |
| 0:58–1:00 | Wrap-up | — |

## 0:00–0:05 — Setup Check

Everyone runs:

```bash
java -version
./gradlew run
```

Anyone whose build fails pairs up with a neighbour. Do not debug installs
during the session.

## 0:05–0:16 — The Problem

Put `NaiveCatalogNode` on the screen. **Do not** say it is bad. Ask the room
to read the five methods and say which of them is about a catalog.

The answer they will converge on is `name()`, and possibly `inventoryValue()`.
Nobody defends `appendCsvTo`. That is the moment: a class about a thing on a
shelf has a private method that knows a comma means the field needs quoting.

Then run section 1 of the demo and show the two rows:

```
    Electronics/Accessories,CLN-003,"Screen Cleaner, 200ml",product,6.50,190,flammable   (7 fields)
    Electronics/Kits,KIT-01,Starter Kit, 3 items,bundle,639.00,25,   (8 fields)
```

Ask: *how did this happen?* Let them find it. The answer is in `NaiveBundle` —
copied from `NaiveProduct`, quoting dropped, and no kit had a comma in its
name that year.

Then show the compliance finding that is missing, and let it sit. An
undeclared lithium cell on an aircraft is the strongest version of "the fourth
copy drifted", and it is worth more than any argument about coupling.

**Point to make before moving on:** the naive inventory value is *correct*, and
so are the category counts. This project does not claim the naive design is
incompetent. It claims it does not survive the fourth report.

## 0:16–0:28 — Double Dispatch

This is the segment people get wrong by rushing. Budget the full twelve
minutes and do it at the keyboard.

Write this live, in a scratch file, and let it fail to compile:

```java
CatalogComponent node = new Product("PHN-900", "Phone", Money.pounds(599.99), 74);
CatalogVisitor visitor = new InventoryValueVisitor();
visitor.visit(node);   // watch it fail
```

Read the compiler error out loud. Ask why — the object *is* a `Product`.

Draw the distinction on the board: **overloads are picked by the compiler from
the static type; overrides are picked by the JVM from the runtime type.** Java
gives you dynamic dispatch on the receiver and nothing else.

Now open `Product.accept` and show that the same call compiles there, because
in that file `this` is a `Product`. Then run section 3 of the demo, which
prints which method each node reached.

Finish the segment by saying the awkward part yourself, before someone else
does: two calls to reach one method, and the reason is a fact about Java, not
about catalogs. If you defend it as elegant you will lose the room.

## 0:28–0:41 — Code Walkthrough

In this order, and no other:

1. `CatalogComponent` — two methods, one of which is `accept`.
2. `Product.accept` and `Bundle.accept` — the same line, twice, and ask again
   why it is not redundant.
3. `Category.accept` — the walk, plus `leave`. Ask what `leave` is for before
   telling them; someone will get to "the visitor needs to know it came back
   out".
4. `InventoryValueVisitor` — the two `visit` methods side by side. **The
   teaching moment:** a kit is not worth the sum of its parts, and here that is
   a sentence rather than an `if`.
5. `ComplianceAuditVisitor.visit(Bundle)` — the loop over `contents()`. Ask
   where else that loop could have gone. There is nowhere.
6. `CategoryPathVisitor` — and say clearly that this is *not* part of the
   pattern. It is a base class four visitors happen to share.

Skip `CsvExportVisitor` unless there is time; it makes the same point as the
compliance one, less dramatically.

## 0:41–0:52 — Exercises

Pairs. Ten minutes. Nobody finishes all three, and that is fine.

**Exercise 1 — write a report (everyone does this one).** In
`ReportVisitorTest`, write a visitor that finds the most expensive single line
in the catalog. Rule: you may not open any file in the model. Time it — most
pairs are done in four minutes, and that speed is the point of the pattern.

**Exercise 2 — feel the cost.** Add a `GiftCard` node type: a class, a
`visit(GiftCard)` on `CatalogVisitor`, and then fix everything that stops
compiling. Do not let them skip the compiling; the six errors *are* the
lesson. Ask afterwards how many of the six needed a real rule and how many got
an empty method.

**Exercise 3 — try to prune.** Write a visitor that reports only on
Accessories and stop the walk from descending into Kits. They cannot. Ask what
they would have to change, and steer to two answers: a `boolean` return from
`visit(Category)`, or an external iterator — and what each costs.

## 0:52–0:58 — The Cost

Run section 5 of the demo. Read the list of six class names off the screen.

Then put the table up and ask the room to fill in the numbers for a codebase
they actually work on:

| | Node types | Operations |
| --- | --- | --- |
| How many today? | | |
| How many added last year? | | |

Whichever number is growing is the axis that should be cheap. In this catalog
it is operations, 3 against 6. In a language front end it is usually the other
way and Visitor is a poor fit there — say so explicitly, because the pattern's
reputation for being over-used is deserved.

Close the segment with the honest summary: *this pattern makes one kind of
change free and another kind expensive, and it is your job to know which one
you are going to be doing.*

## 0:58–1:00 — Wrap-Up

Ask for the answer to one question, from anyone: **when would you not use
this?** Acceptable answers include: two operations; node types still being
added; a single local operation that a `switch` handles; a team that has never
seen `accept` before and a codebase nobody has time to explain it in.

Point them at [`animation.html`](animation.html) for the walk step by step,
and at [`visitor-pattern-explained.md`](visitor-pattern-explained.md) for the
comparisons.

## Common Questions

**"Why not just use `instanceof`?"** You can, and for one report it is better.
Show the pattern-matching switch from `prerequisites.md`. What it does not give
you is the shared traversal, so every report walks the tree itself — which is
the fourth problem in the problem statement with nicer syntax.

**"Why is `leave` a default method?"** Because half the reports do not care,
and an empty method that must be written is a place for a real one to go
missing.

**"Can a visitor return a value instead of accumulating?"** Yes — a generic
`CatalogVisitor<R>` with `R visit(...)` is a common variant. It reads well for
a leaf and badly for a composite, because the results of the children have to
be combined somewhere and `accept` is the wrong place for that rule to live.
This project accumulates in a field and exposes a getter, which is the plainer
of the two.

**"Isn't `accept` boilerplate?"** It is one line per node type, written once,
in a hierarchy the project has already committed to being stable. Compare it
with the alternative it replaces: one method per node type per report.
