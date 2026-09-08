# Video Narration Script

Narration for the Flyweight pattern teaching video. Each scene below maps to
one slide. The narration is spoken by macOS `Samantha`, a female US English
voice, at 145 words per minute.

Total scenes: 15. Approximate runtime: about 7 minutes.

The first and last scenes carry the channel branding: scene 1 credits
the author out loud over the poster, and the final scene asks for the
thumbs up and the subscribe.

The script is written to be spoken rather than read, and carries `[[slnc NNN]]`
pause markers in [`scenes.py`](scenes.py) that insert NNN milliseconds of
silence. Those are instructions to the synthesiser, not words: they are
stripped from the text below and from the subtitles.

---

## Scene 1 — The Flyweight Pattern

Hello, and welcome. This video explains the Flyweight pattern in Java, and
it is written and presented by Jayasekhar Konduru. Let's start with the
simple definition. The flyweight pattern stops you paying for the same data
twice. The parts of an object that are identical across thousands of
instances are stored once and shared between all of them, and everything
that actually differs is passed in from outside at the moment it is needed.
That's the idea in a sentence, and it's a pattern that only shows up once
your object count gets large. The rest of the video does it properly, by
building a real working Java project: badge rendering across an e-commerce
catalog. By the end you'll know what a flyweight is, what intrinsic and
extrinsic state actually mean, and how to write one yourself.

## Scene 2 — The Scenario

So, imagine an online store with one hundred thousand product listings.
Every single listing shows a small badge in the corner. New. Sale.
Bestseller. Low stock. Here's the thing to notice already. There are only
four distinct badge designs in the whole catalog. But a hundred thousand
listings each need one drawn.

## Scene 3 — What a Badge Design Actually Is

Look at what actually makes up one badge design. An icon. A background
colour. A text colour. Whether it's bold. And a rendered artwork bitmap,
sixty four kilobytes. And here's the key observation. Every single SALE
badge in the entire catalog looks completely identical. Same icon, same
colours, same artwork. Only the listing underneath it changes.

## Scene 4 — The Naive Approach — One Badge Object Per Listing

So here's the naive approach. Every time we build a badge for a listing, we
allocate a brand new sixty four kilobyte artwork array, and we rebuild the
icon and the colours from scratch, based on a switch over the type. That
constructor runs once per listing. One hundred thousand times. And every
single SALE badge ends up holding its own private, identical copy of the
exact same data.

## Scene 5 — Why That Hurts

And that does real damage, purely on memory. One hundred thousand listings,
each with a sixty four kilobyte artwork, comes to roughly six point two
five gigabytes. For four distinct designs. Every one of those bytes past
the first four copies is a pure duplicate. And the garbage collector has to
work through all those repeated allocations. To be clear, no individual
badge object is wrong. It renders correctly. The waste is structural, not a
bug.

## Scene 6 — The Flyweight Pattern

The flyweight pattern fixes exactly this. And the definition, in Gang of
Four terms, is that a flyweight uses sharing to support large numbers of
fine grained objects efficiently, by factoring out state that is shared,
called intrinsic, from state supplied by the caller, called extrinsic. In
plain language? Stop paying for the same data twice.

## Scene 7 — Remember It With a Rubber Stamp

Here's how to remember it forever. Think about a rubber stamp. The stamp
itself carries fixed ink, and a fixed shape. That never changes, no matter
how many times you use it. But where you press it down on the page? That's
different every single time. The stamp is the flyweight. It gets shared.
The position on the page is extrinsic. You supply it fresh, every time you
stamp.

## Scene 8 — The Four Roles

Every flyweight setup has four roles. The flyweight itself, which here is
BadgeStyle. The flyweight factory, BadgeStyleFactory, which is the only
place a BadgeStyle ever gets built. The context, CatalogBadge, which is
cheap and plentiful, one per listing. And the client, BadgeDemo, which asks
the factory for styles. Here's the single most important idea in this
whole video. The factory hands out the same shared instance to every
caller asking for the same type. One BadgeStyle object. A hundred thousand
listings pointing at it.

## Scene 9 — The Flyweight — Only Intrinsic State, No Setters

This is the flyweight itself, BadgeStyle. Every field on it — the icon, the
colours, the bold flag, the artwork — is intrinsic. Identical for every
SALE badge, no matter which listing is asking. And look closely at render.
listingId and customLabel arrive as parameters, not fields. That's
extrinsic state, supplied fresh by the caller every time, and never stored
on the shared object. There are no setters here, on purpose. Mutating a
shared instance would corrupt every listing sharing it.

## Scene 10 — The Factory — computeIfAbsent Does All the Work

And this is the factory. One line does the entire pattern's work. Cache
dot computeIfAbsent, keyed by badge type. The very first time anyone asks
for SALE, the lambda runs, build constructs a brand new BadgeStyle, and it
goes into the cache. Every single call after that — for any listing, from
any thread — finds SALE already there, and gets back that exact same
instance. Using a ConcurrentHashMap means this is safe under concurrent
access with no extra locking at all.

## Scene 11 — What the Flyweight Gives You

So the flyweight is giving us three things. Sharing — one BadgeStyle per
badge type, not per listing. Correctness — thread-safe caching, with no
locks we had to write ourselves. And separation — intrinsic fields and
extrinsic parameters, cleanly kept apart. Now notice what it doesn't
contain. There is no per-listing state anywhere on BadgeStyle. A flyweight
shares. It never remembers who asked.

## Scene 12 — The Client — This Is the Whole Thing

And here's the context object that ties it together, CatalogBadge. Its
constructor doesn't build a style. It asks the factory for one, and holds
a shared reference. It owns exactly two things itself: the listing id and
an optional custom label. Everything else, it borrows. So you can create a
hundred thousand of these CatalogBadge objects, and behind them, as few as
four actual BadgeStyle instances doing all the heavy lifting.

## Scene 13 — Running It

When we run the project, the proof is right there in the output. styleFor
SALE, called twice, returns true for equals equals — the exact same
object, both times. Two different listings share one style instance. Now
compare that to the naive alternative. naive A equals naive B, for two
identical SALE badges, is false. Same input, opposite identity. And at the
bottom, the arithmetic that makes it matter. Six thousand two hundred fifty
megabytes, down to two hundred fifty six kilobytes, just by sharing four
instances instead of a hundred thousand.

## Scene 14 — Wrap Up

So, to recap. Use a flyweight when your object count is huge, and most of
each object's state repeats across instances. Keep intrinsic state as
fields, extrinsic state as parameters, and never give a flyweight a
setter. And remember, this pattern is only worth it at scale — five
listings do not need a cache. And if you remember one sentence from today,
make it this one. Prototype hands out copies. Flyweight hands out the same
instance, again and again.

## Scene 15 — Thanks for Watching

And that's the flyweight pattern. If you got something out of this, do
give it a thumbs up, and subscribe. It genuinely helps the channel, and
it's what makes more of these possible. And if there's a pattern you'd
like me to cover next, drop it in the comments. I read every one. All the
source code, the written notes and an interactive animation are in the
repository. Thanks for watching, and I'll see you in the next one.
