# Session Guide — Composite Pattern

A 60-minute guided session for teaching or self-studying the Composite
pattern using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/composite-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Composite pattern solves.
2. Explain why a Leaf and a Composite must implement the same interface.
3. Trace a recursive call (like `totalPrice()`) through a multi-level tree
   by hand.
4. Identify the three roles — component, leaf, composite — in real code.
5. Say why child-management methods usually stay off the shared interface.
6. Distinguish Composite from Decorator.

## Timetable

| Time | Segment | Mode |
| --- | --- | --- |
| 0:00–0:05 | Setup check | Hands-on |
| 0:05–0:15 | The problem | Discussion |
| 0:15–0:25 | The pattern | Explanation |
| 0:25–0:40 | Code walkthrough | Live coding |
| 0:40–0:50 | Exercises | Hands-on |
| 0:50–0:58 | Pitfalls & comparisons | Discussion |
| 0:58–1:00 | Wrap-up | — |

## 0:00–0:05 — Setup Check

Everyone runs:

```bash
java -version
./gradlew run
```

Anyone whose build fails pairs up with a neighbour. Do not debug installs
during the session — that is what the prerequisites doc is for.

## 0:05–0:15 — The Problem

**Do not show `Category`/`Product` yet.** Start with the pain.

Put `NaiveCatalogPrinter.totalPrice` from
[`problem-statement.md`](problem-statement.md) on screen and ask:

> *"If I want to add a fourth operation — say, exporting to JSON — what do
> I have to write?"*

Land on: another method, with the exact same two-branch `instanceof` chain
as `totalPrice`, `productCount`, and `print` already have.

**Key question to land:** *"Is `NaiveCatalogPrinter.totalPrice` wrong?"*
No — it computes the correct total. The waste is that the same
"which type is this" logic gets re-derived in every method that walks the
tree.

## 0:15–0:25 — The Pattern

Introduce the org-chart analogy from
[`composite-pattern-explained.md`](composite-pattern-explained.md). Ask the
group: *"If I ask any employee how many people they manage including
everyone below them, does an intern answer differently in kind, or just in
number, compared to a manager?"* Land on: same question, same interface,
different (but uniform) computation.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the three roles. Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and trace the single
client call fanning out through three levels of the tree with a finger.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice.

**The one point that must land:**

> If client code ever has to ask "is this a leaf or a composite?" before it
> can act, the pattern has not been applied — the whole point is that a
> `Product` and a `Category` answer the same questions the same way.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The component — `CatalogComponent.java`**
Point out this interface declares every operation the tree supports, and
ask: *"Why is `add(child)` not declared here?"* Because a `Product` has no
sensible way to implement it — that's covered again in the pitfalls
section.

**2. The leaf — `Product.java`**
Ask: *"What does `productCount()` return, and why is that always correct
no matter where in the tree this `Product` sits?"* It has no children, so
the answer is always `1` — the base case of the recursion.

**3. The composite — `Category.java`**
This is the heart of the session. Point at the `totalPrice()` loop and ask
the group to predict what happens when a child in that loop is itself a
`Category` with its own children. Then run it and prove them right (or
wrong).

**4. The trap — `NaiveProduct` / `NaiveCategory` / `NaiveCatalogPrinter`**
Put `NaiveCatalogPrinter.totalPrice` and `Category.totalPrice()` side by
side. Ask: *"Which one needs to change if I add a `Bundle` catalog item
tomorrow?"*

**5. The client — `CatalogDemo.java`**
Run `./gradlew run` live. Point at the "uniform treatment" loop that calls
`totalPrice()` and `productCount()` on each child of `electronics` without
ever checking what kind of `CatalogComponent` it received.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a fourth level of nesting (everyone)

Nest another `Category` inside `Cables` with one more `Product`. Run
`./gradlew run` and confirm `totalPrice()` and `productCount()` pick up the
new product with zero code changes.

> **The payoff:** the tree can grow arbitrarily deep and the same three
> methods on `CatalogComponent` keep working. Say this out loud when
> someone finishes.

### Exercise 2 — Break the uniformity on purpose (everyone)

Add an `if (child instanceof Category)` check inside `CatalogDemo`'s
"uniform treatment" loop that does something different for categories than
for products. Discuss: *"What did we just throw away by adding that
check?"* The whole benefit of the shared interface — the loop no longer
needs to know, and now it does anyway.

### Exercise 3 — Try to add `add()` to the interface (discussion)

Move `add(CatalogComponent)` from `Category` onto `CatalogComponent`
itself, then try to implement it on `Product`. Ask: *"What should this
method actually do on a `Product`?"* There is no good answer — throw,
silently ignore, or something else unsatisfying. That dead end is exactly
why this project keeps `add` off the shared interface.

### Exercise 4 — Stretch (for fast finishers)

Add a `Bundle` catalog item that behaves like a `Category` but applies a
10% discount to `totalPrice()`. Confirm it can be added anywhere a
`CatalogComponent` is accepted — inside `Category.add()`, inside another
`Bundle` — with no changes to `Category` or `Product`.

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- Putting child-management methods on the shared Component interface forces
  meaningless implementations on every Leaf.
- Composites need real recursion into every child, not just the first one.
- Mutable, shared children lists are a hazard — return unmodifiable views.
- Cycles turn a tree into a graph, and recursion into a stack overflow.

Then the comparison table. The line worth memorising:

> **Decorator wraps one thing in one more layer. Composite lets one thing
> *be* many things, arranged in a tree.**

Close with real-world sightings: the DOM, filesystems, GUI toolkit
`Component`/`Container` hierarchies, and menu/combo pricing.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one tree-shaped structure in your own codebase — a menu, a
> permission hierarchy, a file tree — and sketch what its Component
> interface would need to declare.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "Isn't this just a tree data structure?" | Yes, structurally — the pattern's contribution is that every node, leaf or branch, answers the *same* interface, so client code never branches on node type |
| "Why not just use `instanceof` everywhere, it's simpler?" | It works for three methods. Ask what happens at ten methods and three catalog item types — the naive approach becomes thirty near-identical branches |
| "Shouldn't `Product` support `add()` too, for consistency?" | Consistency at the interface level, yes. But a meaningless method body is worse than an asymmetric interface — see Exercise 3 |
| "This feels like overkill for four items" | Fair, for four items. The payoff scales with tree depth and the number of operations, not the current catalog size |

**If you are running short on time:** cut Exercise 4 and shorten the
pitfalls discussion. Never cut Exercise 3 — hitting the dead end of adding
`add()` to the interface is where the "why not put everything on one
interface" question actually gets answered.

**If you have extra time:** have participants implement `print(indent)` for
a hypothetical `Bundle` type that lists its contained products with a
"(bundle discount applied)" suffix, and discuss whether that breaks the
uniformity the pattern promises.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/composite-pattern-explained.mp4`) — useful
      as a recap for anyone who joins late, or to send round afterwards
- [ ] The printed catalog tree from `./gradlew run` ready to put on the
      board
- [ ] IDE font size raised for screen sharing
