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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Prototype pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Prototype pattern makes '
            'a new object by copying one that already exists, instead of '
            'building it from nothing. [[slnc 400]] You keep one fully '
            'set-up example to hand. [[slnc 300]] When you need another, '
            'you ask it for a copy of itself. [[slnc 300]] Then you '
            'change only the parts that differ. [[slnc 600]] Think of a '
            'photocopier. [[slnc 300]] You start from a finished page, '
            'and get an independent copy instantly. [[slnc 700]] In this '
            'video, we copy product listings in an online marketplace. '
            "[[slnc 500]] Along the way, we look closely at Java's "
            'built-in copy method, called clone. [[slnc 300]] And why the '
            'book Effective Java warns you away from it.'
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
            'Here is the job. [[slnc 400]] A seller lists wireless '
            'earbuds, in black. [[slnc 500]] Getting that one listing '
            'right is real work. [[slnc 300]] Choosing a category. [[slnc '
            '200]] Writing a description that meets the rules. [[slnc '
            '200]] Choosing a shipping profile. [[slnc 200]] And setting '
            'a return window and a warranty. [[slnc 500]] Now the seller '
            'wants the same earbuds in white. [[slnc 300]] And then in '
            'blue. [[slnc 500]] The category, description, shipping, '
            'returns, and warranty are all unchanged. [[slnc 300]] Only '
            'the product code, the title, and the colour are different.'
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
            'So you write it out twice, using the constructor. [[slnc '
            '400]] Each call has eleven arguments. [[slnc 300]] And only '
            'two or three of them differ between black and white. [[slnc '
            '500]] Everything else is copied, word for word, between the '
            'calls. [[slnc 300]] The description, category, brand, price, '
            'shipping, returns, and warranty. [[slnc 500]] Add a blue '
            'version, and it is pasted a third time. [[slnc 300]] Fix a '
            'typo in the description, and every copy needs the same fix.'
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
            'Java already has a way to copy objects, so why not use it? '
            '[[slnc 400]] You implement the Cloneable interface, and '
            'override the clone method. [[slnc 500]] The book Effective '
            'Java spends a whole chapter explaining why this disappoints '
            'almost everyone. [[slnc 500]] The clone method is protected, '
            'so you must make it public yourself. [[slnc 300]] It '
            'declares an error that can never actually happen. [[slnc '
            '300]] And worst of all, it copies fields shallowly. [[slnc '
            "500]] So if you add a picture to the copy's image list, the "
            "original's list changes too. [[slnc 300]] Silently. [[slnc "
            '300]] Because they were always the same list.'
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
            'So neither approach works. [[slnc 500]] Typing every version '
            'out by hand means the shared details get retyped again and '
            'again. [[slnc 300]] And eventually, one of them drifts. '
            '[[slnc 500]] Using Cloneable swaps that problem for a worse '
            'one. [[slnc 300]] A method you must expose yourself, an '
            'error that means nothing, and a shallow copy that silently '
            'links two objects. [[slnc 500]] Notice that the product '
            'listing itself is fine. [[slnc 300]] The problem is how you '
            'duplicate one.'
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
            'The fix is a pattern from the famous Gang of Four book. '
            '[[slnc 400]] Specify the kinds of objects to create using an '
            'example instance, and create new objects by copying that '
            'example. [[slnc 500]] In plain words: keep one fully '
            'assembled example around. [[slnc 300]] And make new ones by '
            'copying it, and changing only what is different.'
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
            'Think about the difference between a blueprint and a '
            'photocopier. [[slnc 500]] A blueprint tells you how to build '
            'something from raw materials, every single time. [[slnc '
            '300]] That is what a constructor is. [[slnc 500]] A '
            'photocopier is different. [[slnc 300]] It starts from a '
            'finished page, and hands you an independent copy, instantly. '
            '[[slnc 300]] You can scribble all over your copy, and the '
            'original on the glass does not change. [[slnc 500]] That is '
            'a prototype. [[slnc 300]] Not instructions, but a finished '
            'example you copy from.'
        ),
    ),
    dict(
        key="08-shape",
        kind="diagram",
        title="The Shape of It",
        body=None,
        narration=(
            'So here is the shape of it. [[slnc 400]] The product listing '
            'class implements a small interface called Prototype. [[slnc '
            '300]] It has just one method, called copy. [[slnc 500]] Call '
            'copy on an existing listing, and you get back a second, '
            'fully independent listing, with the same details. [[slnc '
            '500]] Alongside it sits a listing registry. [[slnc 300]] It '
            'is a named shelf of templates. [[slnc 300]] Ask it for a '
            'template by name, and it hands back a fresh copy.'
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
            'Here is the whole Prototype interface: one method, called '
            'copy. [[slnc 500]] Compare it with Cloneable. [[slnc 300]] '
            'Nothing protected to expose. [[slnc 300]] No error to catch '
            'that can never happen. [[slnc 500]] And no automatic copying '
            'at all. [[slnc 300]] Because only the real class knows which '
            'of its fields need a true copy, and which can simply be '
            'shared.'
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
            'Now look at the copy method itself. [[slnc 400]] There is no '
            'special copying logic inside it. [[slnc 300]] It simply '
            'calls the constructor again, passing in its own details. '
            '[[slnc 500]] That works because the constructor already '
            'creates a brand new image list, and a brand new attribute '
            'map, every time it runs. [[slnc 300]] It does that to '
            'protect any caller who hands it a list. [[slnc 500]] So copy '
            'gets that protection for free. [[slnc 300]] One piece of '
            'protective code, doing two jobs.'
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
            'But not every field gets a fresh copy. [[slnc 400]] The '
            'shipping profile is passed straight through. [[slnc 300]] '
            'The original and the copy share the very same shipping '
            'profile object. [[slnc 500]] That is only safe because the '
            'shipping profile can never change. [[slnc 300]] It is a '
            'record, with no setters. [[slnc 600]] This is the real '
            'design work in this pattern. [[slnc 300]] Not calling the '
            'constructor again. [[slnc 300]] But deciding, field by '
            'field, what needs a fresh copy, and what is safe to share.'
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
            'Here is what copying and adjusting looks like. [[slnc 400]] '
            'Copy the black master listing. [[slnc 300]] Set the new '
            'product code. [[slnc 300]] Set the new title, wireless '
            'earbuds, white. [[slnc 300]] Change the colour to white. '
            '[[slnc 300]] And replace the pictures. [[slnc 500]] Five '
            'short steps, instead of an eleven-argument call, repeating '
            'eight values that never changed. [[slnc 500]] And the master '
            'listing is completely untouched. [[slnc 300]] The white '
            'listing has its own independent colour details, and its own '
            'list of pictures.'
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
            'The Gang of Four book also describes a registry of '
            'templates, sometimes called a prototype manager. [[slnc '
            '300]] It is useful when the set of templates is decided '
            'while the program runs. [[slnc 500]] Its create method looks '
            'up a template by name. [[slnc 300]] If there is none, it '
            'refuses, and names the missing key. [[slnc 300]] Otherwise, '
            'it returns a copy of the template. [[slnc 500]] Notice it '
            'never builds a listing from scratch. [[slnc 300]] It only '
            'ever copies. [[slnc 300]] Ask for the same name twice, and '
            'you get two separate, independent listings.'
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
            "Let's run the demo. [[slnc 500]] First, a master listing, "
            'and a white version copied and adjusted from it. [[slnc '
            "500]] The master's own pictures are unchanged after the "
            'copy. [[slnc 300]] And the shipping profile really is the '
            'same shared object in both. [[slnc 500]] Then the registry '
            'hands back two independent listings, from one name. [[slnc '
            '500]] And finally, a request for a name that was never '
            'registered. [[slnc 300]] It is refused with a clear message, '
            'before any listing is copied.'
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
            'Now the honest part. [[slnc 300]] Every pattern has limits. '
            '[[slnc 500]] First, deciding what to copy takes care. [[slnc '
            '300]] Every changeable field a class adds is one more thing '
            'its author must remember to copy properly. [[slnc 300]] Miss '
            'one, and copies silently share a list. [[slnc 300]] Exactly '
            'the bug this pattern exists to prevent. [[slnc 500]] Second, '
            'copying is not checking. [[slnc 300]] A copy reproduces the '
            "original's state, whether it was valid or not. [[slnc 500]] "
            'Third, a registry swaps a class name the compiler can check, '
            'for a text key that is only checked at run time. [[slnc '
            '300]] Use a registry only when the templates really are '
            'decided elsewhere.'
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
            'So how does Prototype relate to the other creational '
            'patterns? [[slnc 500]] A static factory answers: give me one '
            'that does this. [[slnc 300]] A builder answers: which '
            'pieces, in what order, for one object. [[slnc 300]] An '
            'abstract factory answers: which whole matching set. [[slnc '
            '300]] And Prototype answers a question none of the others '
            'do. [[slnc 300]] I already have one, so how do I get another '
            'that is almost the same? [[slnc 500]] And they work '
            'together. [[slnc 300]] A template stored in a registry might '
            'well have been built with a builder in the first place.'
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
            'If you keep one sentence from this video, keep this one. '
            '[[slnc 400]] When you already have one fully assembled '
            'object, and need another that is almost the same, copy it '
            'instead of rebuilding it. [[slnc 300]] And decide, field by '
            'field, what copy should mean. [[slnc 300]] A fresh copy for '
            'anything that can change. [[slnc 300]] A shared reference '
            'for anything that cannot. [[slnc 600]] The project has full '
            'notes, an animated walkthrough, and a teaching plan. [[slnc '
            '300]] Try adding a new changeable field to the product '
            'listing. [[slnc 300]] And notice that the copy method needs '
            'no changes at all.'
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
            "That's the Prototype pattern. [[slnc 400]] The full source "
            'code, written notes, and diagrams are all in the repository. '
            '[[slnc 500]] If there is a pattern you would like to see '
            'covered, suggest it in the comments. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
