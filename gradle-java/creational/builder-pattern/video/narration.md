# Builder Pattern — Video Narration Script

The full spoken script, scene by scene. This is the human-readable copy;
the authoritative text lives in the `narration` field of each scene in
[`scenes.py`](scenes.py), next to the slide it belongs to.

**Voice:** female (macOS `Samantha`, US English), rate 165 wpm.
**Runtime:** approximately 12 minutes.

The script is written to be spoken, not read: contractions, short
sentences, and `[[slnc NNN]]` pause markers in `scenes.py` that the
synthesiser turns into breathing room. The markers are stripped below
and from the subtitles.

Currency and symbols are written out in words, because the synthesiser
reads them poorly. Keep that habit if you edit the script.

The first scene carries the author credit and the last carries the
subscribe call to action; keep both if you re-record.

---

## Scene 1 — Builder Pattern

Hello, and welcome. This video explains the Builder pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The builder pattern constructs an object one piece at a time. Instead of a constructor taking a long list of arguments, you call a named method for each part you want to set, in whatever order suits you, and then one final method that validates the lot and hands back the finished object. That's the idea in a sentence. It's in the original Gang of Four book, and it's also item two in Effective Java, and by the end you'll know exactly why both books claim it. The rest of the video does it properly, by building a real working Java project: a purchase order in an online store, in Java 21, picking up right where the static factory method left off. And you'll see the two of them compose, because one of them returns the other.

## Scene 2 — The Job

So here's the job. We're building a purchase order. Two things about it are always true. It needs an order id and a customer id, and it needs at least one item and a shipping address. But on top of that, there are five completely independent optional pieces. Gift wrap, which can carry a message. A coupon code. Priority shipping. And a free-text note. Any order might have none of those, or all of them, in any combination.

## Scene 3 — The Constructor With Nine Parameters

So you write the constructor everyone starts with. Nine parameters, one for every fact this order might need. Now look at the call underneath it, and tell me, quickly, is this the priority order, or the gift order? You have to count commas and cross-check against the parameter list to know. And there are two booleans in there. Swap them by accident, and the compiler says absolutely nothing.

## Scene 4 — Telescoping Constructors

The next instinct is to add smaller constructors on top, one for the common cases. But look what happens. A gift order without priority needs one overload. A gift order with a coupon needs another. Every new combination either needs a brand new overload, or you fall back to the nine-parameter one anyway. Effective Java actually has a name for this. The telescoping constructor pattern. And it's named as the chapter's cautionary tale, not as something to reach for.

## Scene 5 — Why That Hurts

And that costs you, in five specific ways. One. The call site stops saying what it means. Two. Most calls are mostly null, or mostly false, because most orders don't use most of the options. Three. The parameter order is completely arbitrary, and nothing in the language enforces it. Four. Every new option widens the constructor, and every existing caller has to be touched, even the ones that never wanted the new option. And five, the one people miss: there is nowhere to put a rule like "a gift message implies gift wrap". A constructor just assigns fields. But notice, again, what isn't wrong. The type itself is fine. It's the way in that's the problem.

## Scene 6 — The Builder Pattern

The fix has a name, and this time it really is a Gang of Four pattern. Separate the construction of a complex object from its representation, so the same construction process can create different representations. In plain words? You decide the object a piece at a time, in whatever order suits you, and it only gets checked for completeness the moment you say you're done. And it's also item two in Effective Java. Same technique, described from two angles — one as a design pattern for building complex objects, the other as the fix for the telescoping constructor we just saw. Both books are talking about the same code.

## Scene 7 — A Made-to-Order Sandwich Counter

Think about ordering at a made-to-order sandwich counter. You don't shout the entire order through the hatch in one go. You say the bread. Then a filling. Then another. Then maybe some extras, and you only mention the ones you actually want — nobody says "no pickles, no mustard, no onions" for every topping that isn't there. And crucially, they don't start making the sandwich until you say "that's everything". If you say that with no fillings at all, they can quite reasonably say no. That's the whole shape of a builder. You build it up, a piece at a time, and completeness only gets checked at the very end.

## Scene 8 — The Shape of It

So here's the shape of it. There's exactly one door in: PurchaseOrder dot builder, taking the two facts every order truly needs. That hands back a Builder. Every chainable method on that Builder returns the very same Builder, so the calls read as one flowing statement. And only the final build call does two things at once: it checks the order is actually complete, and it constructs the immutable PurchaseOrder. PurchaseOrder's own constructor is private. The Builder is the only path in, from anywhere outside this class.

## Scene 9 — Required Facts, Optional Pieces

Here's the code. The two facts that are always required — order id, and customer id — are the only two arguments the Builder's constructor takes, and that constructor is private, reached only through the static builder method. Every optional piece, by contrast, starts at a sensible default and has no constructor argument at all. There's nothing to skip past, because there was never a positional slot for it in the first place.

## Scene 10 — One Method, One Piece

Every method follows the same shape: set one piece, then return this. Returning the same builder is what lets the next call chain straight off the end of it, with no temporary variable anywhere. And look at that call underneath. Compare it to the nine-parameter constructor from scene three. You don't have to ask which argument is which any more — every piece announces itself by name, in whatever order you happened to write it.

## Scene 11 — A Rule That Lives in One Place

Here's the part a plain bag of setters could never give you. Setting a gift message also sets gift wrapped to true, because a gift message on a box that isn't wrapped makes no sense in this domain. And that rule lives in exactly one place. Not repeated at every call site, not left to a comment saying "remember to also wrap it" — it's enforced, once, inside the one method that can enforce it.

## Scene 12 — Checked Only When You Say You're Done

And this is the moment completeness gets checked. Not addItem, not shippingAddress — build. Why can't an earlier method check this instead? Because addItem has no way of knowing whether you're about to call shippingAddress next, or whether you're finished. Only build marks the moment you've declared yourself done, so it's the only method that can honestly ask "is this actually complete?"

## Scene 13 — The Product Stops Watching the Builder

One more detail, easy to miss and important. The constructor takes List dot copyOf of the builder's items — a snapshot, not the same list. So keep the same builder around, add another item, and build a second order from it. The first order you built does not silently gain the new item. It already took its own copy. The product stops watching the builder the instant build returns.

## Scene 14 — The Director, the Java Way

The Gang of Four book gives builder a fourth role, a Director, usually its own interface and class, whose whole job is to know fixed recipes for common configurations. In idiomatic Java, that's usually just a static method, and that's exactly what PurchaseOrderPresets is here. Look closely: expressOrder never touches a PurchaseOrder field, or the constructor. It only ever calls Builder's public methods. Which means PurchaseOrder can change its private representation tomorrow, and not one preset has to change with it.

## Scene 15 — Running It

Let's run it, and see the whole story on one screen. One order built by hand, with a gift message and a coupon chained straight on. Three presets, each reading exactly like what it configures. The reused-builder proof, one order with one item, the next with two, neither reaching into the other. And at the bottom, two orders rejected on purpose — one with no items, one with no address — both caught as IllegalStateException before a single PurchaseOrder object was ever created.

## Scene 16 — Where It Stops

Now the honest part. Every pattern has a ceiling. A builder is a second object. Briefly, for every PurchaseOrder you build, a Builder exists too. For an order placed a few times a second, that's nothing. For something constructed millions of times in a hot loop, it's a real allocation to weigh. It's also more typing, for a type that has nothing to decide. And the required fields don't disappear — the Builder's own constructor still takes them positionally, it's just a much shorter list. Which is exactly why LineItem and Address in this project are plain records, with ordinary public constructors. Two or three required fields, no options, no rules between them — a builder there would be ceremony around a non-problem.

## Scene 17 — How It Relates to the Others

So where does builder sit next to the other creational patterns? Static factory answers "give me one that does this", with no factory class at all. Simple factory moves "which one?" into a helper with a switch. Abstract factory answers "which whole matching set?", one choice producing several related objects. And builder answers a different question entirely: not which object, but which pieces, assembled in what order, for one object. And here's the nice part. They're not rivals. PurchaseOrder dot builder is itself a static factory method — it just happens to return something whose whole job is collecting more information before it builds anything.

## Scene 18 — One Sentence to Keep

If you keep one sentence from all of this, keep this one. A constructor makes you decide the whole object in one call. A builder lets you decide it a piece at a time, and checks it is complete only when you say you are done. There's a full set of notes in the project, an animated walkthrough you can step through at your own pace, and a session plan if you fancy teaching this to somebody else. Go add an option of your own to PurchaseOrder. That's the best way to make it stick.

## Scene 19 — Thanks for Watching

And that's the builder pattern. If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. All the source code, the written notes and the diagrams are in the repository. Thanks for watching, and I'll see you in the next one.
