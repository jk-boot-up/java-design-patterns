# Session Guide — Flyweight Pattern

A 60-minute guided session for teaching or self-studying the Flyweight
pattern using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/flyweight-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Flyweight pattern solves.
2. Tell intrinsic state from extrinsic state in a piece of code they have
   never seen before.
3. Identify the four roles — flyweight, factory, context, client — in real
   code.
4. Explain why a flyweight must never hold extrinsic state.
5. Say when Flyweight is the *wrong* choice.
6. Distinguish Flyweight from Singleton and Prototype.

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

**Do not show `BadgeStyleFactory` yet.** Start with the pain.

Put `NaiveListingBadge` from
[`problem-statement.md`](problem-statement.md) on screen and ask:

> *"There are four badge designs and one hundred thousand listings. How
> many times does the SALE artwork get built?"*

Land on: one hundred thousand times, for four designs. Then do the
arithmetic together on the board:

```
100,000 × 64 KB  ≈  6,250 MB
      4 × 64 KB  ≈  256 KB
```

**Key question to land:** *"Is any individual `NaiveListingBadge` wrong?"*
No — every one renders correctly. The waste is structural, not a bug.

## 0:15–0:25 — The Pattern

Introduce the rubber-stamp analogy from
[`flyweight-pattern-explained.md`](flyweight-pattern-explained.md). Ask the
group: *"What does the stamp know about the page? What does the page know
that the stamp doesn't?"* Land on intrinsic (the stamp) vs. extrinsic (the
position on the page) before showing any code.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the four roles. Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and trace the second
`styleFor(SALE)` call with a finger — the one that hits the cache.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice.

**The one point that must land:**

> If a piece of data varies per caller, it is a method parameter. If it
> would be identical no matter who's asking, it can be a shared field.
> Getting this backwards is the only real way to misuse this pattern.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The flyweight — `BadgeStyle.java`**
Point out every field is intrinsic, and `render()` takes `listingId` and
`customLabel` as *parameters*, never as fields. Ask: *"Why no setters?"*
Because mutating a shared instance would corrupt every listing sharing it.

**2. The factory — `BadgeStyleFactory.java`**
This is the heart of the session. Point at
`CACHE.computeIfAbsent(type, BadgeStyleFactory::build)` and ask the group to
predict what happens on the second call for the same type. Then run it and
prove them right (or wrong).

**3. The context — `CatalogBadge.java`**
Ask: *"What does this class own, and what does it borrow?"* It owns
`listingId` and `customLabel`; it borrows `style` from the factory.

**4. The trap — `NaiveListingBadge.java`**
Put it side by side with `BadgeStyle`. Same fields, same `switch`, but no
factory in front of it. Ask: *"What's different about how many times this
runs?"*

**5. The client — `BadgeDemo.java`**
Run `./gradlew run` live. Point at `styleFor(SALE) == styleFor(SALE): true`
and `naiveA == naiveB (both SALE): false` — same input, opposite identity —
and let that contrast land before moving to the memory arithmetic at the
bottom of the output.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a fifth badge type (everyone)

Add `BadgeType.CLEARANCE` and a case in `BadgeStyleFactory.build`. Run
`./gradlew run` and confirm `instancesCreated()` becomes 5, not 100,004.

> **The payoff:** the cache scales with *distinct designs*, not with how
> many listings use them. Say this out loud when someone finishes.

### Exercise 2 — Break the sharing on purpose (everyone)

Move `listingId` from `CatalogBadge` onto `BadgeStyle` as a field, set once
in the constructor. Run the existing tests. Watch
`renderCombinesTheSharedStyleWithThisBadgesOwnListingAndLabel` and the
identity tests start failing or producing the wrong listing id. Ask: *"What
category of state did we just turn into a field by mistake?"*

### Exercise 3 — Spot the anti-pattern (discussion)

Present a flyweight factory with an unbounded cache key — one entry per
distinct search query, say, in a system with millions of unique queries.
Ask: *"Is this still saving memory?"* No — an unbounded cache of
per-instance objects is just a memory leak with a pattern name attached.

### Exercise 4 — Stretch (for fast finishers)

Make `BadgeStyleFactory.build` print a timestamp, then call `styleFor` for
all four types from twenty threads at once (borrow the shape of
`concurrentLookupsForTheSameTypeAllReceiveTheSameInstance`). Confirm each
type's build timestamp appears exactly once even under concurrent load.

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- Getting intrinsic and extrinsic backwards is the whole risk.
- Only worth it at scale — five listings don't need this.
- Mutable flyweights corrupt every caller sharing them.
- An unbounded cache key turns the fix into the leak.

Then the comparison table. The line worth memorising:

> **Prototype hands out copies. Flyweight hands out the same instance,
> again and again.**

Close with real-world sightings: `Integer.valueOf(-128..127)`, string
interning, and font-glyph caches in text renderers.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one place in your own codebase where many objects carry an identical
> copy of the same data, and sketch the flyweight that would replace it.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "So it's just a cache?" | A cache remembers *results*; a flyweight shares *identity* deliberately, and the whole design is built around what can and can't be shared |
| "Isn't this the same as Singleton?" | Singleton is one instance, period. Flyweight is one instance *per category*, shared by many contexts |
| "Why not just copy the object, it's simpler?" | That's Prototype, and it's the opposite goal — more instances, not fewer |
| "This feels like premature optimisation" | Fair, if the object count is small. Say so — the doc says the same thing |

**If you are running short on time:** cut Exercise 4 and shorten the
pitfalls discussion. Never cut Exercise 2 — breaking the sharing on purpose
is where the concept actually lands.

**If you have extra time:** have participants add a `RATING` badge type
(intrinsic: star icon and colour) with an extrinsic numeric score passed to
`render`, and discuss why the score itself must never live on `BadgeStyle`.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/flyweight-pattern-explained.mp4`) — useful as
      a recap for anyone who joins late, or to send round afterwards
- [ ] The memory arithmetic from `./gradlew run` ready to put on the board
- [ ] IDE font size raised for screen sharing
