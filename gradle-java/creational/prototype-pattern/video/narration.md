# Prototype Pattern — Video Narration Script

The full spoken script, scene by scene. This is the human-readable copy;
the authoritative text lives in the `narration` field of each scene in
[`scenes.py`](scenes.py), next to the slide it belongs to.

**Voice:** female (macOS `Samantha`, US English), rate 165 wpm.
**Runtime:** approximately 11 minutes.

The script is written to be spoken, not read: contractions, short
sentences, and `[[slnc NNN]]` pause markers in `scenes.py` that the
synthesiser turns into breathing room. The markers are stripped below
and from the subtitles.

Currency and symbols are written out in words, because the synthesiser
reads them poorly. Keep that habit if you edit the script.

The first scene carries the author credit and the last carries the
subscribe call to action; keep both if you re-record.

---

## Scene 1 — Prototype Pattern

Hello, and welcome. This video explains the Prototype pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The prototype pattern makes a new object by copying one that already exists, rather than building it from nothing. You keep a fully configured instance to hand and, whenever you need another, you ask that instance for a copy of itself and change only the parts that differ. That's the idea in a sentence, and it answers a question that neither builder nor a static factory method actually solves. The rest of the video does it properly, by building a real working Java project: a marketplace product listing, in Java twenty one. And along the way we'll take a hard look at Java's own built-in attempt at this, clone, and why Effective Java spends a whole chapter warning you off it.

## Scene 2 — The Job

So here's the job. A seller lists wireless earbuds, in black. Getting that one listing right is real work — picking a category from the taxonomy, writing description text that satisfies the compliance rules, choosing a shipping profile, setting a return window and a warranty that match the category's policy. Now they want the same earbuds in white. And then in blue. Nothing about the category, the compliance text, the shipping profile, the return window or the warranty changed. Only the sku, the title, and one attribute did.

## Scene 3 — The Repeated Eleven-Argument Call

So you write it out, twice. Look at these two calls side by side. Eleven arguments each, and only two or three of them actually differ between black and white. Everything else — the description, the category, the brand, the price, the shipping profile, the return window, the warranty — is copied, character for character, between calls. Add a blue variant, and it gets pasted a third time. Fix a typo in that description, and every call site needs the same edit.

## Scene 4 — The Cloneable Trap

Java already ships a way to copy an object, so why not use it? Implements Cloneable, override clone, call super dot clone. Effective Java, item thirteen, spends an entire chapter on why this disappoints almost everyone who tries it. Clone is protected, so you have to re-expose it. It throws a checked exception that can never actually fire. And worst of all, super dot clone copies fields shallowly — mutate the quote-unquote copy's image list, and the original's list changes too, silently, because they were always the same list.

## Scene 5 — Why That Hurts

So neither attempt actually works. Typing every variant out by hand means the shared fields get re-typed, and re-typed, and eventually one of them drifts. And reaching for Cloneable trades that problem for a worse one — a protected method you have to re-expose, an exception that means nothing, and a shallow copy that silently links two objects that should be independent. Notice what isn't wrong, though. Product listing itself is fine. It's how you duplicate one that's the problem.

## Scene 6 — The Prototype Pattern

The fix has a name, and it's a genuine Gang of Four pattern. Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype. In plain words? Instead of describing how to build an object from nothing every single time, you keep one fully-assembled example around, and you produce new ones by copying it and changing only what's actually different.

## Scene 7 — A Photocopier, Not a Blueprint

Think about the difference between a blueprint and a photocopier. A blueprint tells you how to build something from raw materials, every single time, from scratch — that's what a constructor is. A photocopier is completely different. It starts from an already-finished page, and hands you an independent copy, instantly. You can scribble all over your copy, and the original sitting on the glass doesn't change. That's a prototype. Not a set of instructions — an actual, already-finished example you clone from.

## Scene 8 — The Shape of It

So here's the shape of it. Product listing implements a one-method interface, Prototype of T, whose only method is copy. Call copy on an existing listing, and you get back a second, fully independent listing with the same state. A listing registry sits alongside it — a named shelf of templates that hands back a fresh copy whenever a caller asks for a key, rather than the caller having to hold a reference to the original at all.

## Scene 9 — One Method, No Baggage

Here's the whole interface. One method, unchecked, public by construction. Compare it against Cloneable from scene four. Nothing to re-expose from a protected superclass method. Nothing to catch that can never actually be thrown. And critically, no default implementation at all — because only the concrete type knows which of its own fields need a real copy, and which can just be shared.

## Scene 10 — copy() Reuses the Constructor

Now look at copy itself. There's no copying logic inside it at all — it just calls the constructor again, passing its own fields straight through. That works because the constructor already builds a brand new array list and a brand new linked hash map, every single time it runs, to protect any caller who hands it a list or a map. Copy gets that protection for free. One piece of defensive copying code, doing double duty.

## Scene 11 — Deep Copy vs. Shared Reference

But not every field gets that deep-copy treatment. Shipping profile is passed straight through, unchanged — the original and the copy end up holding the exact same instance. That's only safe because shipping profile is a record. Immutable, no setters, nothing can change it out from under either listing. This is the real design work in this pattern — not the mechanical 'call the constructor again' part, but deciding, field by field, what deserves a fresh copy and what's safe to share.

## Scene 12 — Cloning and Tweaking

So this is what calling it actually looks like. Five lines, instead of an eleven-argument constructor call repeating eight values that never changed. And master, the original, is completely untouched. White's attributes and white's images are its own independent map and list — never the same objects master is holding.

## Scene 13 — The Registry

The Gang of Four book names one more variant of this, sometimes called a prototype manager — a registry of templates, keyed by name, for when the set of templates is decided at runtime rather than known in the caller's source code. Look closely at create. It never writes new product listing anywhere. It only ever calls copy on whatever was registered under that key. Call it twice with the same key, and you get back two separate, independently-mutable instances.

## Scene 14 — Running It

Let's run it, and see the whole story on one screen. A master listing, and a white variant cloned and tweaked from it. Proof that master's own images are untouched after the clone. Proof that the shipping profile really is the same instance on both. And down at the bottom, the registry handing back two independent instances from one key, and a lookup on a key that was never registered, rejected with a clear message before any listing was ever cloned.

## Scene 15 — Where It Stops

Now the honest part. Every pattern has a ceiling. Deep-copy judgment doesn't come for free. Every mutable field a concrete prototype adds is one more thing its author has to remember to deep-copy in the constructor — miss one, and copy silently produces two listings sharing a list, which is exactly the bug this pattern exists to prevent. Copy also isn't validation. It reproduces whatever state the original had, valid or not. And a registry trades a compile-time constructor name for a runtime string key — convenient when the set of templates truly is decided elsewhere, a needless failure mode otherwise.

## Scene 16 — How It Relates to the Others

So where does prototype sit next to the other creational patterns? Static factory answers 'give me one that does this'. Builder answers 'which pieces, assembled in what order, for one object'. Abstract factory answers 'which whole matching set'. And prototype answers a question none of the others do: 'I already have one of these — how do I get another that's almost the same?' And they compose. A template registered in a listing registry might well have been assembled with a builder before it was ever registered.

## Scene 17 — One Sentence to Keep

If you keep one sentence from all of this, keep this one. When you already have one fully-assembled object and need another that's almost the same, copy it instead of rebuilding it from scratch — and decide, field by field, what copy should mean: a fresh copy for anything mutable, a shared reference for anything that can't change. There's a full set of notes in the project, an animated walkthrough you can step through at your own pace, and a session plan if you fancy teaching this to somebody else. Go add a mutable field of your own to product listing, and watch copy need zero changes to keep working.

## Scene 18 — Thanks for Watching

And that's the prototype pattern. If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. All the source code, the written notes and the diagrams are in the repository. Thanks for watching, and I'll see you in the next one.
