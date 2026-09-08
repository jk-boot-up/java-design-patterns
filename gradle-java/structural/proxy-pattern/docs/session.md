# Session Guide — Proxy Pattern

A 60-minute guided session for teaching or self-studying the Proxy pattern
using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/proxy-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Proxy pattern solves.
2. Explain why `LazyProductImage` holds a SKU instead of a
   `HighResolutionProductImage` until `render()` is called.
3. Identify the four roles — subject, real subject, proxy, client — in
   real code.
4. Explain why `RestrictedProductImage` takes a `ProductImage`, not a
   `HighResolutionProductImage`, in its constructor, and what that buys.
5. Distinguish Proxy from Decorator.

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

**Do not show `ProductImage`/`LazyProductImage` yet.** Start with the pain.

Put `NaiveProductListing` from [`problem-statement.md`](problem-statement.md)
on screen and ask:

> *"This listing is built with ten SKUs but only ever shows the
> first one. How many images get expensively loaded?"*

Land on: all ten, every time, no matter how many actually get shown.

Then put `NaiveAdminImageViewer` alongside it and ask:

> *"A second screen — a thumbnail grid — also needs to check who's
> allowed to see an image. Where does that check go?"*

Land on: copy-pasted into the new screen, with nothing stopping a third
screen from forgetting it entirely.

**Key question to land:** *"If the loading strategy or the access rule
ever needs to change, how many places does that change have to be made?"*
Every call site that duplicated the logic — and that count grows with
every new screen.

## 0:15–0:25 — The Pattern

Introduce the bouncer analogy from
[`proxy-pattern-explained.md`](proxy-pattern-explained.md). Ask the group:
*"Does the guest see a different club, or the same one reached through a
checkpoint?"* Land on: the same one — the proxy adds a decision-maker in
front of the real thing, not a new thing.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the four roles. Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and trace a single
`render()` call through the protection proxy, into the virtual proxy,
and only then into the real subject — once.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice.

**The one point that must land:**

> Strip the proxies away and the *visible result is identical* —
> `render()` still returns the same string. That's the tell that this is
> Proxy, not Decorator: nothing new was added, access was just controlled.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The subject — `ProductImage.java`**
Point out this interface declares exactly the shape the real image and
every proxy share: `render()` and `sku()`. Ask: *"Why does a proxy
need to expose the exact same interface as the thing it stands in for?"*

**2. The real subject — `HighResolutionProductImage.java`**
Point out the static `LOAD_COUNT` — a stand-in for "this is expensive."
Ask: *"If this constructor actually decoded a file from disk, what would
happen if a naive listing built ten of these it never rendered?"*

**3. The virtual proxy — `LazyProductImage.java`**
This is the heart of the session. Point at the `realImage == null` check
in `render()` and ask: *"What happens the first time this runs? What
happens the second time?"* First: builds and caches. Second: reuses.

**4. The protection proxy — `RestrictedProductImage.java`**
Point at the constructor signature: `ProductImage image`, not
`HighResolutionProductImage image`. Ask: *"What does that one detail make
possible?"* Composing proxies — wrapping this around a `LazyProductImage` gets
lazy loading and access control at once.

**5. The traps — `NaiveProductListing.java` / `NaiveAdminImageViewer.java`**
Put the eager-loading loop and the inline role check side by side. Ask:
*"What has to change in every caller if the access rule changes?"*
Everything that copy-pasted the check — versus one class, if it went
through the proxy instead.

**6. Run it — `ProductImageDemo.java`**
Run `./gradlew run` live. Point at the load-count numbers before and after
each `render()` call, and the moment an admin's proxy loads an image while
a denied shopper's identical-looking proxy never does. Ask the group to
predict the count before it prints.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a logging proxy (everyone)

Add a `LoggingLazyProductImage` that records every `render()` call to a
`List<String>` before delegating to a wrapped `ProductImage`. Confirm it can be
composed with the existing proxies in any order.

> **The payoff:** a whole new concern (auditing) added with zero changes
> to `LazyProductImage` or `RestrictedProductImage`. Say this out loud when
> someone finishes.

### Exercise 2 — Prove denial short-circuits loading (everyone)

Write a test that wraps a fresh `LazyProductImage` in an
`RestrictedProductImage` with `Role.SHOPPER`, calls `render()`
expecting a `SecurityException`, and then asserts
`HighResolutionProductImage.loadCount()` is still zero.

### Exercise 3 — Break the cache on purpose (discussion)

Add an `invalidate()` method to `LazyProductImage` that sets `realImage` back to
`null`. Discuss: *"When would you actually want to call this?"* Land on:
whenever the underlying file can change during the program's life — the
cache is only safe because nothing here ever mutates the real image.

### Exercise 4 — Stretch (for fast finishers)

Design a `RemoteLazyProductImage` (on paper, no code needed) that fetches a
image from a network service instead of local disk. Discuss which parts of
`LazyProductImage` change (the loading mechanism) and which stay identical (the
interface, the caching idea).

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- A proxy that needs to load the real subject just to answer a cheap
  question (like `sku()`) has defeated its own purpose — keep enough
  state in the proxy itself to avoid that.
- Caching hides staleness — `LazyProductImage` is only safe to cache forever
  because the underlying image never changes mid-run.
- Reaching for Proxy to add a new feature is a sign Decorator was the
  pattern actually needed.

Then the comparison table. The line worth memorising:

> **Proxy keeps the same interface and delegates to control *access* —
> when to create, whether to allow, where the real thing lives. Decorator
> keeps the same interface and delegates to add *new behaviour* on top.**

Close with real-world sightings: Hibernate/JPA lazy-loading entity
proxies, `java.rmi` remote proxies, and Spring's `@Transactional` proxies.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one place in your own codebase where a client either eagerly builds
> something expensive it may never use, or re-implements the same access
> check at more than one call site — and sketch what a proxy would look
> like instead.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "Isn't this the same as Decorator?" | No — Decorator adds new behaviour that wasn't there before (a fee, a suffix); Proxy adds no new behaviour at all, it decides whether/when the call reaches the real object |
| "Why not just add an `if (!loaded)` check inline wherever an image is used?" | That's exactly what the naive traps do, scattered across every call site — the proxy centralises the check once, behind the same interface, so no caller can forget it |
| "Doesn't checking `role != Role.CATALOG_ADMIN` belong in the real image, not a wrapper?" | Putting it in `HighResolutionProductImage` would mean every subject needs to know about roles, even when no caller cares — the proxy keeps that concern out of the subject entirely |
| "Isn't caching forever a bug?" | Only if the underlying data can change. Here it's a deliberate, documented assumption — the pitfalls section calls this out explicitly |

**If you are running short on time:** cut Exercise 4 and shorten the
pitfalls discussion. Never cut Exercise 2 — proving that denial stops the
load *before* it happens is the moment composability actually lands.

**If you have extra time:** have participants implement
`LoggingLazyProductImage` from Exercise 1 fully, with its own test class
mirroring `LazyProductImageTest`.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/proxy-pattern-explained.mp4`) — useful
      as a recap for anyone who joins late, or to send round afterwards
- [ ] The printed load-count output from `./gradlew run` ready to put
      on the board
- [ ] IDE font size raised for screen sharing
