"""Scene definitions for the Proxy pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="The Proxy Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Proxy pattern in Java, "
            "and it is written and presented by Jayasekhar Konduru. [[slnc 300]] "
            "Let's start with the simple definition. The proxy pattern puts a "
            "stand-in in front of a real object, with the same interface as the "
            "real thing. The caller cannot tell the difference, but the stand-in "
            "is free to delay the expensive work, check who is asking, or count "
            "the calls, before it passes anything along. [[slnc 350]] That's the "
            "idea in a sentence — controlling when an object gets built, and who "
            "is allowed to touch it. The rest of the video does it properly, by "
            "building a real working Java project: an online store's category "
            "page, where loading a product's full-resolution image is expensive "
            "and not every asset is one a shopper may see. [[slnc 250]] By the "
            "end you'll know how to delay expensive work until it is actually "
            "needed, and how to put an access check in one place that no caller "
            "can forget."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "A product listing backed by full-resolution images:",
            "",
            "  loading one image is expensive -- decoding, memory, disk",
            "",
            "Two things the listing needs, that the image itself shouldn't know about:",
            "",
            "  don't load an image until it is actually rendered",
            "  don't let a non-admin render a restricted image at all",
        ],
        narration=(
            "So, imagine a product listing backed by full-resolution images. "
            "[[slnc 250]] Loading a single one of those is expensive — decoding "
            "the file, allocating the memory, reading from disk. [[slnc 300]] "
            "And there are two things the listing needs that the image itself "
            "really shouldn't have to know anything about. First, don't load an "
            "image until it is actually rendered. And second, don't let a "
            "non-admin render a restricted image at all."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Where Those Checks End Up",
        body=[
            "Without a stand-in, both concerns land in the caller:",
            "",
            "  the listing builds every image up front, in its constructor",
            "  every screen re-implements the same role check inline",
            "",
            "Add a thumbnail grid, a slideshow, a search result page --",
            "and each one has to remember to do both, correctly.",
        ],
        narration=(
            "Without a stand-in, both of those concerns land in the caller. "
            "[[slnc 250]] The listing builds every image up front in its "
            "constructor, because that's the simplest thing that works. And "
            "every screen that shows an image re-implements the same role check "
            "inline. [[slnc 300]] Now add a thumbnail grid, a slideshow, a "
            "search results page — and each one of those has to remember to do "
            "both of those things, and to do them correctly."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Eager Loading and Inline Checks",
        body="""public final class NaiveProductListing {
    private final List<HighResolutionProductImage> images = new ArrayList<>();

    public NaiveProductListing(List<String> skus) {
        for (String sku : skus) {
            images.add(new HighResolutionProductImage(sku));   // every one, up front
        }
    }
}

public final class NaiveAdminImageViewer {
    public String view(Role role) {
        if (role != Role.CATALOG_ADMIN) {              // copy-pasted per screen
            throw new SecurityException("Only catalog admins may view " + image.sku());
        }
        return image.render();
    }
}""",
        narration=(
            "So here's the naive approach. [[slnc 250]] NaiveProductListing takes "
            "a list of SKUs and, in its constructor, builds a "
            "HighResolutionProductImage for every single one — before anything has been "
            "rendered at all. [[slnc 300]] And NaiveAdminImageViewer has the "
            "role check written directly inside its view method. That check is "
            "correct. The problem is that it's correct in exactly one place, and "
            "the next screen has to copy it."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   Work is paid for images that are never shown",
            "✗   The access rule is duplicated in every screen that shows an image",
            "✗   A screen that forgets the check is a silent security hole",
            "✗   Nothing here is a bug — the waste is structural",
        ],
        narration=(
            "And that does real damage as the system grows. [[slnc 250]] You pay "
            "the full loading cost for images that are never shown — build a "
            "listing of ten and render one, and nine loads were wasted. The "
            "access rule is duplicated in every screen that renders an image. "
            "[[slnc 300]] And worse than duplication: a screen that simply "
            "forgets the check isn't a compile error, it's a silent security "
            "hole. [[slnc 250]] None of this is a bug. Each naive class does "
            "exactly what it says. The waste is structural — access control and "
            "lifetime management pushed out into every caller."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Proxy Pattern",
        body=[
            "“Provide a surrogate or placeholder for another object",
            "to control access to it.”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "same interface, but it decides whether and when the call gets through.",
        ],
        narration=(
            "The proxy pattern fixes exactly this. [[slnc 250]] In Gang of Four "
            "terms, proxy provides a surrogate or placeholder for another object "
            "in order to control access to it. [[slnc 300]] In plain language? "
            "Same interface, but it decides whether, and when, the call actually "
            "gets through."
        ),
    ),
    dict(
        key="07-bouncer",
        kind="bullets",
        title="Remember It With the Bouncer on the Door",
        body=[
            "A bouncer stands in front of the club, not inside it.",
            "",
            "You talk to the bouncer exactly the way you'd talk to the club --",
            "you ask to come in. The bouncer decides if the request gets through.",
            "",
            "The club is the same club either way. Nothing was added to it.",
            "Somebody just controls the door.",
        ],
        narration=(
            "Here's how to remember it forever. Think about the bouncer on the "
            "door of a club. [[slnc 250]] The bouncer stands in front of the "
            "club, not inside it. You talk to the bouncer exactly the way you'd "
            "talk to the club itself — you ask to come in. [[slnc 300]] And the "
            "bouncer decides whether that request gets through. [[slnc 250]] "
            "Here's the part that matters. The club is the same club either way. "
            "Nothing was added to it, nothing was changed about it. Somebody just "
            "controls the door."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            "Every proxy setup has four roles. [[slnc 200]] The subject, ProductImage, "
            "the interface the real thing and every stand-in share. The real "
            "subject, HighResolutionProductImage, the expensive object we're protecting. "
            "The proxies — LazyProductImage, which delays construction until the first "
            "render call, and RestrictedProductImage, which checks the "
            "caller's role first. And the client, ProductImageDemo, which holds "
            "only a ProductImage and never learns which of those it actually has. "
            "[[slnc 350]] Here's the single most important idea in this whole "
            "video. The proxy exposes exactly the same interface as the real "
            "subject, and returns exactly the same result. Nothing new is added. "
            "That is what makes it a proxy and not a decorator."
        ),
    ),
    dict(
        key="09-subject",
        kind="code",
        title="The Subject — The Shared Shape",
        body="""public interface ProductImage {
    String render();
    String sku();
}

public final class HighResolutionProductImage implements ProductImage {
    public HighResolutionProductImage(String sku) {
        this.sku = sku;
        LOAD_COUNT.incrementAndGet();      // stands in for "this is expensive"
    }

    @Override public String render() { return "Rendering " + sku + " hero image (1920x1080)"; }
    @Override public String sku()    { return sku; }
}""",
        narration=(
            "This is the subject, ProductImage. [[slnc 250]] It's the shared interface "
            "the real image and every proxy implement — just render, and "
            "S K U. [[slnc 300]] And this is the real subject, "
            "HighResolutionProductImage. Its constructor bumps a static load count, "
            "which is our stand-in for expensive work. Notice it knows nothing "
            "about proxies, or roles, or laziness. It just is an image."
        ),
    ),
    dict(
        key="10-virtual",
        kind="code",
        title="The Virtual Proxy — Build It Late, Build It Once",
        body="""public final class LazyProductImage implements ProductImage {
    private final String sku;
    private HighResolutionProductImage realImage;   // null until the first render()

    @Override
    public String render() {
        if (realImage == null) {
            realImage = new HighResolutionProductImage(sku);
        }
        return realImage.render();
    }

    @Override
    public String sku() { return sku; }   // cheap: never triggers a load
}""",
        narration=(
            "And this is the virtual proxy, LazyProductImage. [[slnc 250]] It holds a "
            "S K U, and a realImage field that stays null until somebody "
            "actually calls render. First call, it builds the real image and "
            "caches it. Every call after that reuses the cached one. [[slnc "
            "300]] And look at the S K U method. It answers straight from the "
            "proxy's own "
            "field, without loading anything. That detail matters — a proxy that "
            "has to build the real subject just to answer a cheap question has "
            "defeated its own purpose."
        ),
    ),
    dict(
        key="11-protection",
        kind="code",
        title="The Protection Proxy — And Why It Takes a ProductImage",
        body="""public final class RestrictedProductImage implements ProductImage {
    private final ProductImage image;   // a ProductImage, not a HighResolutionProductImage
    private final Role role;

    @Override
    public String render() {
        if (role != Role.CATALOG_ADMIN) {
            throw new SecurityException("Only catalog admins may view " + image.sku());
        }
        return image.render();
    }
}

ProductImage guarded =
        new RestrictedProductImage(new LazyProductImage("SKU-9001"), Role.CATALOG_ADMIN);""",
        narration=(
            "Here's the subtlety worth pausing on. [[slnc 250]] "
            "RestrictedProductImage takes a ProductImage in its constructor. Not a "
            "HighResolutionProductImage — a ProductImage. [[slnc 300]] That one detail is what "
            "lets it wrap a LazyProductImage, so you get the role check and the lazy "
            "loading together, from two small classes that were never written "
            "with each other in mind. [[slnc 250]] And notice the order. If the "
            "role check fails, it throws before it ever calls render on the "
            "image it wraps — so a denied shopper never causes a load at all. The "
            "expensive work is skipped because the access decision came first."
        ),
    ),
    dict(
        key="12-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

== Naive listing -- eagerly loads every image, even ones never scrolled to ==
Images loaded eagerly, before rendering anything: 3

== Virtual proxy -- loads an image only when it's actually rendered ==
Images loaded so far (real subject not yet touched): 0
Images loaded after first render: 1
Images loaded after second render (unchanged -- cached): 1

== Protection proxy -- controls access to render() based on role ==
Catalog admin can render: Rendering SKU-2087 hero image (1920x1080)
Shopper denied: Only catalog admins may view SKU-2087

== Composing proxies -- protection proxy wrapping a virtual proxy ==
Total images loaded so far: 2 -- SKU-9001 is not among them yet, still lazy
Total images loaded after admin render: 3""",
        narration=(
            "When we run the project, the numbers tell the whole story. [[slnc "
            "250]] The naive listing has loaded three images before rendering "
            "anything. The virtual proxy has loaded zero — the real subject "
            "hasn't been touched. [[slnc 300]] After the first render it's one. "
            "After the second render it's still one, because the instance was "
            "cached. [[slnc 250]] Then the protection proxy lets an admin "
            "through and refuses a shopper. And in the composed section, S K U "
            "nine thousand one stays unloaded right up until an admin passes "
            "the role "
            "check — one proxy wrapped in the other, doing both jobs at once."
        ),
    ),
    dict(
        key="13-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use proxy when a client shouldn't have to manage when an object",
            "is created, or whether it's allowed to be used at all.",
            "",
            "Keep the proxy's interface identical to the subject, and keep cheap",
            "questions cheap -- never load the real thing just to answer one.",
            "",
            "Remember one sentence:",
            "Proxy keeps the same interface and controls access.",
            "Decorator keeps the same interface and adds new behaviour.",
        ],
        narration=(
            "So, to recap. Use proxy when a client shouldn't have to manage when "
            "an object gets created, or whether it's allowed to be used at all. "
            "[[slnc 300]] Keep the proxy's interface identical to the subject, "
            "and keep the cheap questions cheap — never load the real thing just "
            "to answer one. [[slnc 350]] And if you remember one sentence from "
            "today, make it this one. Proxy keeps the same interface and "
            "delegates in order to control access — when to create, whether to "
            "allow, where the real thing lives. Decorator keeps the same "
            "interface and delegates in order to add new behaviour on top. Same "
            "shape, different intent."
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "If this helped, a thumbs up and a subscribe go a long way",
            "towards keeping more videos like it coming.",
            "",
            "Full source code, notes and an animation are in the repository.",
        ],
        narration=(
            "And that's the proxy pattern. [[slnc 300]] If you got something out "
            "of this, do give it a thumbs up, and subscribe. It genuinely helps "
            "the channel, and it's what makes more of these possible. [[slnc "
            "250]] And if there's a pattern you'd like me to cover next, drop it "
            "in the comments. I read every one. [[slnc 250]] All the source code, "
            "the written notes and an interactive animation are in the "
            "repository. Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
