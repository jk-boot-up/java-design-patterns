#!/usr/bin/env python3
"""The script for the Prototype Pattern video.

One entry per scene. `narration` is spoken aloud and also becomes the
subtitles, so it is written the way someone would actually say it out loud:
contractions, short sentences, the odd aside. Currency and symbols are
spelled out in words, because the synthesiser reads them poorly.

`[[slnc NNN]]` is an embedded speech command that inserts a pause of NNN
milliseconds. It is what stops the delivery sounding like a machine reading
a paragraph, so use it where a person would naturally draw breath — after a
punchline, before a list, at a change of direction. `make_subtitles.py`
strips these before writing captions.

Keep this file the single source of truth: the slides, the audio and the
subtitles are all generated from it.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Prototype Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Prototype pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. [[slnc "
            "300]] Let's start with the simple definition. The prototype pattern "
            "makes a new object by copying one that already exists, rather than "
            "building it from nothing. You keep a fully configured instance to "
            "hand and, whenever you need another, you ask that instance for a "
            "copy of itself and change only the parts that differ. [[slnc 350]] "
            "That's the idea in a sentence, and it answers a question that "
            "neither builder nor a static factory method actually solves. The "
            "rest of the video does it properly, by building a real working Java "
            "project: a marketplace product listing, in Java twenty one. [[slnc "
            "250]] And along the way we'll take a hard look at Java's own built- "
            "in attempt at this, clone, and why Effective Java spends a whole "
            "chapter warning you off it."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Job",
        body=[
            "A seller lists Wireless Earbuds in black. Getting it right",
            "means real work:",
            "",
            "•  a category from the taxonomy, compliant description text",
            "•  a shipping profile, a return window, a warranty length",
            "",
            "Now they want the same earbuds in white. And in blue.",
        ],
        narration=(
            "So here's the job. A seller lists wireless earbuds, in black. "
            "Getting that one listing right is real work — picking a "
            "category from the taxonomy, writing description text that "
            "satisfies the compliance rules, choosing a shipping profile, "
            "setting a return window and a warranty that match the "
            "category's policy. [[slnc 250]] "
            "Now they want the same earbuds in white. And then in blue. "
            "Nothing about the category, the compliance text, the shipping "
            "profile, the return window or the warranty changed. Only the "
            "sku, the title, and one attribute did."
        ),
    ),
    dict(
        key="03-wall",
        kind="code",
        title="The Repeated Eleven-Argument Call",
        body="""ProductListing black = new ProductListing("EARBUD-BLK", "Wireless Earbuds",
        longDescription, "Electronics", "Acme Audio", Money.pounds(59.99),
        List.of("black-1.jpg"), Map.of("color", "Black"), standardShipping, 30, 12);

ProductListing white = new ProductListing("EARBUD-WHT", "Wireless Earbuds (White)",
        longDescription, "Electronics", "Acme Audio", Money.pounds(59.99),
        List.of("white-1.jpg"), Map.of("color", "White"), standardShipping, 30, 12);""",
        narration=(
            "So you write it out, twice. Look at these two calls side by "
            "side. Eleven arguments each, and only two or three of them "
            "actually differ between black and white. [[slnc 300]] "
            "Everything else — the description, the category, the brand, "
            "the price, the shipping profile, the return window, the "
            "warranty — is copied, character for character, between calls. "
            "Add a blue variant, and it gets pasted a third time. Fix a typo "
            "in that description, and every call site needs the same edit."
        ),
    ),
    dict(
        key="04-cloneable",
        kind="code",
        title="The Cloneable Trap",
        body="""public class ProductListing implements Cloneable {
    @Override
    public ProductListing clone() throws CloneNotSupportedException {
        return (ProductListing) super.clone();   // shallow copy
    }
}

// copy.getImages().add("extra.jpg");
// ...now original.getImages() has it too — same List, two names""",
        narration=(
            "Java already ships a way to copy an object, so why not use it? "
            "Implements Cloneable, override clone, call super dot clone. "
            "[[slnc 300]] "
            "Effective Java, item thirteen, spends an entire chapter on why "
            "this disappoints almost everyone who tries it. Clone is "
            "protected, so you have to re-expose it. It throws a checked "
            "exception that can never actually fire. And worst of all, "
            "super dot clone copies fields shallowly — mutate the "
            "quote-unquote copy's image list, and the original's list "
            "changes too, silently, because they were always the same list."
        ),
    ),
    dict(
        key="05-harm",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗  Shared fields are re-typed at every call site",
            "✗  One missed edit and two listings quietly drift apart",
            "✗  Cloneable's clone() is protected, and re-throws for no reason",
            "✗  super.clone() copies mutable fields shallowly, by default",
            "",
            "The object is fine. Both ways of duplicating it are the problem.",
        ],
        narration=(
            "So neither attempt actually works. "
            "[[slnc 300]] "
            "Typing every variant out by hand means the shared fields get "
            "re-typed, and re-typed, and eventually one of them drifts. And "
            "reaching for Cloneable trades that problem for a worse one — a "
            "protected method you have to re-expose, an exception that means "
            "nothing, and a shallow copy that silently links two objects "
            "that should be independent. [[slnc 300]] "
            "Notice what isn't wrong, though. Product listing itself is "
            "fine. It's how you duplicate one that's the problem."
        ),
    ),
    dict(
        key="06-definition",
        kind="quote",
        title="The Prototype Pattern",
        body=[
            "Specify the kinds of objects to create using a prototypical",
            "instance, and create new objects by copying this prototype.",
            "",
            "— Gang of Four, Design Patterns",
            "",
            "In plain words: keep one fully-assembled example around,",
            "and produce new ones by copying it and changing what differs.",
        ],
        narration=(
            "The fix has a name, and it's a genuine Gang of Four pattern. "
            "Specify the kinds of objects to create using a prototypical "
            "instance, and create new objects by copying this prototype. "
            "[[slnc 300]] "
            "In plain words? Instead of describing how to build an object "
            "from nothing every single time, you keep one fully-assembled "
            "example around, and you produce new ones by copying it and "
            "changing only what's actually different."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="A Photocopier, Not a Blueprint",
        body=[
            "A blueprint tells you how to build something from raw materials,",
            "every single time, from scratch.",
            "",
            "•  a photocopier starts from a finished page",
            "•  you get an independent copy, instantly",
            "•  then you annotate the copy — the original stays untouched",
            "",
            "That's a prototype. Not instructions. An actual finished example.",
        ],
        narration=(
            "Think about the difference between a blueprint and a "
            "photocopier. A blueprint tells you how to build something from "
            "raw materials, every single time, from scratch — that's what a "
            "constructor is. [[slnc 300]] "
            "A photocopier is completely different. It starts from an "
            "already-finished page, and hands you an independent copy, "
            "instantly. You can scribble all over your copy, and the "
            "original sitting on the glass doesn't change. [[slnc 250]] "
            "That's a prototype. Not a set of instructions — an actual, "
            "already-finished example you clone from."
        ),
    ),
    dict(
        key="08-shape",
        kind="diagram",
        title="The Shape of It",
        body=None,
        narration=(
            "So here's the shape of it. Product listing implements a "
            "one-method interface, Prototype of T, whose only method is "
            "copy. [[slnc 300]] "
            "Call copy on an existing listing, and you get back a second, "
            "fully independent listing with the same state. A listing "
            "registry sits alongside it — a named shelf of templates that "
            "hands back a fresh copy whenever a caller asks for a key, "
            "rather than the caller having to hold a reference to the "
            "original at all."
        ),
    ),
    dict(
        key="09-interface",
        kind="code",
        title="One Method, No Baggage",
        body="""public interface Prototype<T> {
    T copy();
}

// no protected access to re-expose
// no checked exception that can never fire
// no shallow-copy-by-default surprise""",
        narration=(
            "Here's the whole interface. One method, unchecked, public by "
            "construction. [[slnc 300]] "
            "Compare it against Cloneable from scene four. Nothing to "
            "re-expose from a protected superclass method. Nothing to catch "
            "that can never actually be thrown. And critically, no default "
            "implementation at all — because only the concrete type knows "
            "which of its own fields need a real copy, and which can just "
            "be shared."
        ),
    ),
    dict(
        key="10-copy",
        kind="code",
        title="copy() Reuses the Constructor",
        body="""public ProductListing(String sku, ..., List<String> images, Map<String, String> attributes, ...) {
    this.images = new ArrayList<>(images);          // deep copy, already here
    this.attributes = new LinkedHashMap<>(attributes);
    ...
}

@Override
public ProductListing copy() {
    return new ProductListing(sku, title, description, category, brand, price,
            images, attributes, shippingProfile, returnWindowDays, warrantyMonths);
}""",
        narration=(
            "Now look at copy itself. There's no copying logic inside it at "
            "all — it just calls the constructor again, passing its own "
            "fields straight through. [[slnc 300]] "
            "That works because the constructor already builds a brand new "
            "array list and a brand new linked hash map, every single time "
            "it runs, to protect any caller who hands it a list or a map. "
            "Copy gets that protection for free. One piece of defensive "
            "copying code, doing double duty."
        ),
    ),
    dict(
        key="11-shared",
        kind="code",
        title="Deep Copy vs. Shared Reference",
        body="""public record ShippingProfile(String carrier, int weightGrams, boolean freeShipping) { }

this.shippingProfile = shippingProfile;   // passed straight through, never copied

// master.shippingProfile() == whiteVariant.shippingProfile()  -> true""",
        narration=(
            "But not every field gets that deep-copy treatment. Shipping "
            "profile is passed straight through, unchanged — the original "
            "and the copy end up holding the exact same instance. "
            "[[slnc 300]] "
            "That's only safe because shipping profile is a record. "
            "Immutable, no setters, nothing can change it out from under "
            "either listing. This is the real design work in this pattern — "
            "not the mechanical 'call the constructor again' part, but "
            "deciding, field by field, what deserves a fresh copy and what's "
            "safe to share."
        ),
    ),
    dict(
        key="12-tweak",
        kind="code",
        title="Cloning and Tweaking",
        body="""ProductListing white = master.copy();
white.setSku("EARBUD-WHT");
white.setTitle("Wireless Earbuds (White)");
white.attributes().put("color", "White");
white.images().clear();
white.images().add("earbuds-white-1.jpg");

// master is untouched — its images and attributes were never the same List/Map""",
        narration=(
            "So this is what calling it actually looks like. Five lines, "
            "instead of an eleven-argument constructor call repeating eight "
            "values that never changed. [[slnc 300]] "
            "And master, the original, is completely untouched. White's "
            "attributes and white's images are its own independent map and "
            "list — never the same objects master is holding."
        ),
    ),
    dict(
        key="13-registry",
        kind="code",
        title="The Registry",
        body="""public ProductListing create(String key) {
    ProductListing template = templates.get(key);
    if (template == null) {
        throw new NoSuchElementException("no listing template registered under: " + key);
    }
    return template.copy();
}

// registry.create("earbuds-template") — twice — returns two independent instances""",
        narration=(
            "The Gang of Four book names one more variant of this, "
            "sometimes called a prototype manager — a registry of templates, "
            "keyed by name, for when the set of templates is decided at "
            "runtime rather than known in the caller's source code. "
            "[[slnc 300]] "
            "Look closely at create. It never writes new product listing "
            "anywhere. It only ever calls copy on whatever was registered "
            "under that key. Call it twice with the same key, and you get "
            "back two separate, independently-mutable instances."
        ),
    ),
    dict(
        key="14-run",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

Master:      ProductListing{sku=EARBUD-BLK, title=Wireless Earbuds, ...}
White variant: ProductListing{sku=EARBUD-WHT, title=Wireless Earbuds (White), ...}

master.images() unaffected: [earbuds-black-1.jpg, earbuds-black-2.jpg]
shippingProfile is the same instance: true

registry copies are independent instances: true
Rejected: no listing template registered under: does-not-exist""",
        narration=(
            "Let's run it, and see the whole story on one screen. "
            "[[slnc 250]] "
            "A master listing, and a white variant cloned and tweaked from "
            "it. Proof that master's own images are untouched after the "
            "clone. Proof that the shipping profile really is the same "
            "instance on both. [[slnc 300]] "
            "And down at the bottom, the registry handing back two "
            "independent instances from one key, and a lookup on a key that "
            "was never registered, rejected with a clear message before any "
            "listing was ever cloned."
        ),
    ),
    dict(
        key="15-limits",
        kind="bullets",
        title="Where It Stops",
        body=[
            "✗  Every mutable field you add is one more thing to remember",
            "    to deep-copy — miss one and copy() silently shares state",
            "✗  copy() reproduces invalid state exactly as faithfully as valid",
            "✗  A registry trades a compile-time name for a runtime string key",
            "",
            "✓  Reach for a registry only when the keys genuinely come",
            "    from outside the caller's own code.",
        ],
        narration=(
            "Now the honest part. Every pattern has a ceiling. "
            "[[slnc 300]] "
            "Deep-copy judgment doesn't come for free. Every mutable field a "
            "concrete prototype adds is one more thing its author has to "
            "remember to deep-copy in the constructor — miss one, and copy "
            "silently produces two listings sharing a list, which is exactly "
            "the bug this pattern exists to prevent. [[slnc 250]] "
            "Copy also isn't validation. It reproduces whatever state the "
            "original had, valid or not. And a registry trades a "
            "compile-time constructor name for a runtime string key — "
            "convenient when the set of templates truly is decided "
            "elsewhere, a needless failure mode otherwise."
        ),
    ),
    dict(
        key="16-family",
        kind="bullets",
        title="How It Relates to the Others",
        body=[
            "Static Factory     give me one that…              no factory class",
            "Builder            which pieces, in what order?   one object, assembled gradually",
            "Abstract Factory   which whole set?                one choice, many objects",
            "Prototype          I have one — get me another    copy an existing instance",
            "",
            "A registry's templates might themselves be built with a builder —",
            "the patterns compose rather than compete.",
        ],
        narration=(
            "So where does prototype sit next to the other creational "
            "patterns? [[slnc 250]] "
            "Static factory answers 'give me one that does this'. Builder "
            "answers 'which pieces, assembled in what order, for one "
            "object'. Abstract factory answers 'which whole matching set'. "
            "And prototype answers a question none of the others do: 'I "
            "already have one of these — how do I get another that's almost "
            "the same?' [[slnc 300]] "
            "And they compose. A template registered in a listing registry "
            "might well have been assembled with a builder before it was "
            "ever registered."
        ),
    ),
    dict(
        key="17-wrap",
        kind="title",
        title="One Sentence to Keep",
        body=[
            "When you already have one fully-assembled object and need",
            "another that's almost the same, copy it instead of rebuilding",
            "it — and decide, field by field, what \"copy\" should mean.",
        ],
        narration=(
            "If you keep one sentence from all of this, keep this one. "
            "[[slnc 300]] "
            "When you already have one fully-assembled object and need "
            "another that's almost the same, copy it instead of rebuilding "
            "it from scratch — and decide, field by field, what copy should "
            "mean: a fresh copy for anything mutable, a shared reference for "
            "anything that can't change. [[slnc 350]] "
            "There's a full set of notes in the project, an animated "
            "walkthrough you can step through at your own pace, and a "
            "session plan if you fancy teaching this to somebody else. Go "
            "add a mutable field of your own to product listing, and watch "
            "copy need zero changes to keep working."
        ),
    ),
    dict(
        key="18-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "If this helped, a thumbs up and a subscribe go a long way",
            "towards keeping more videos like it coming.",
            "",
            "Full source code, notes and diagrams are in the repository.",
        ],
        narration=(
            "And that's the prototype pattern. [[slnc 300]] "
            "If you got something out of this, do give it a thumbs up, and "
            "subscribe. It genuinely helps the channel, and it's what makes "
            "more of these possible. [[slnc 250]] "
            "And if there's a pattern you'd like me to cover next, drop it "
            "in the comments. I read every one. [[slnc 250]] "
            "All the source code, the written notes and the diagrams are in "
            "the repository. Thanks for watching, and I'll see you in the "
            "next one."
        ),
    ),
]
