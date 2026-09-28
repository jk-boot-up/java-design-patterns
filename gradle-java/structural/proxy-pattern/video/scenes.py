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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Proxy pattern, in Java. [[slnc 300]] This video is presented '
            'by Jayasekhar Konduru. [[slnc 600]] First, a simple '
            'definition. [[slnc 300]] A proxy is a stand-in, placed in '
            'front of a real object, with exactly the same shape. [[slnc '
            '300]] The caller cannot tell the difference. [[slnc 300]] '
            'But the stand-in can delay expensive work, check who is '
            'asking, or count calls, before passing anything along. '
            '[[slnc 600]] Think of a bouncer at the door of a club. '
            '[[slnc 300]] You ask the bouncer to come in, and the bouncer '
            'decides. [[slnc 700]] In our online store, a category page '
            'shows product images. [[slnc 300]] Loading a full-size image '
            'is expensive. [[slnc 300]] And some images only certain '
            'staff may see. [[slnc 500]] By the end, you will know how to '
            'delay expensive work until it is needed. [[slnc 300]] And '
            'how to put an access check in one place that no caller can '
            'forget.'
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
            'Here is the scenario. [[slnc 400]] A product listing uses '
            'full-size images. [[slnc 300]] Loading just one is '
            'expensive: reading the file, decoding it, and holding it in '
            'memory. [[slnc 600]] And the listing needs two things that '
            'the image itself should not have to care about. [[slnc 500]] '
            'First: do not load an image until it is actually shown. '
            '[[slnc 300]] Second: do not let an ordinary shopper see a '
            'restricted image at all.'
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
            'Without a stand-in, both jobs land on the caller. [[slnc '
            '500]] The listing loads every image up front, when it is '
            'created, because that is simplest. [[slnc 300]] And every '
            'screen that shows an image repeats the same access check. '
            '[[slnc 600]] Now add a thumbnail grid, a slideshow, and a '
            'search results page. [[slnc 300]] Each one must remember to '
            'do both jobs, and do them correctly.'
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
            'Here is the naive approach. [[slnc 400]] The naive listing '
            'receives a list of product codes. [[slnc 300]] And straight '
            'away, it loads a full-size image for every one, before '
            'anything is shown. [[slnc 600]] And a separate admin viewer '
            'has the access check written directly inside it. [[slnc '
            '300]] That check is correct. [[slnc 300]] But it is correct '
            'in only one place. [[slnc 300]] The next screen has to copy '
            'it.'
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
            'That does real damage as the system grows. [[slnc 500]] You '
            'pay the full loading cost for images that are never shown. '
            '[[slnc 300]] Load a listing of ten, show one, and nine loads '
            'were wasted. [[slnc 500]] The access rule is copied into '
            'every screen that shows an image. [[slnc 300]] And worse, a '
            'screen that forgets the check does not fail to build. [[slnc '
            '300]] It becomes a silent security hole. [[slnc 600]] None '
            'of this is a bug. [[slnc 300]] The waste is in the '
            'structure: access and timing pushed out into every caller.'
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
            'The Proxy pattern fixes exactly this. [[slnc 400]] The '
            'classic book on design patterns, by the authors known as the '
            'Gang of Four, describes it like this. [[slnc 300]] Provide a '
            'stand-in, or placeholder, for another object, to control '
            'access to it. [[slnc 600]] In plain words: the same shape, '
            'but it decides whether, and when, the call gets through.'
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
            'Here is how to remember it. [[slnc 300]] Think about the '
            'bouncer at the door of a club. [[slnc 500]] The bouncer '
            'stands in front of the club, not inside it. [[slnc 300]] You '
            'talk to the bouncer just as you would to the club. [[slnc '
            '300]] You ask to come in. [[slnc 300]] And the bouncer '
            'decides whether you get through. [[slnc 600]] Here is the '
            'part that matters. [[slnc 300]] The club is the same club '
            'either way. [[slnc 300]] Nothing was added to it. [[slnc '
            '300]] Someone just controls the door.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            'Every proxy has four roles. [[slnc 500]] The subject: the '
            'shared interface, here called product image. [[slnc 300]] '
            'The real subject: the full-size image, the expensive object '
            'being protected. [[slnc 300]] The proxies: a lazy image, '
            'which waits until the first time it is shown. [[slnc 300]] '
            "And a restricted image, which checks the caller's role "
            'first. [[slnc 300]] And the client: the demo code, which '
            'only ever holds a product image, and never learns which kind '
            'it has. [[slnc 600]] Here is the most important idea in this '
            'video. [[slnc 300]] A proxy has exactly the same shape as '
            'the real object, and gives exactly the same result. [[slnc '
            '300]] Nothing new is added. [[slnc 300]] That is what makes '
            'it a proxy, and not a decorator.'
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
            'Here is the subject: the product image interface. [[slnc '
            '400]] It has just two questions. [[slnc 300]] Show yourself. '
            '[[slnc 300]] And what is your product code? [[slnc 600]] And '
            'here is the real subject: the full-size image. [[slnc 300]] '
            'Every time one is created, it adds one to a load counter. '
            '[[slnc 300]] That counter stands for expensive work. [[slnc '
            '500]] It knows nothing about proxies, roles, or waiting. '
            '[[slnc 300]] It just is an image.'
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
            'Here is the lazy proxy. [[slnc 400]] It holds a product '
            'code, and an empty space for the real image. [[slnc 500]] '
            'The first time it is asked to show itself, it loads the real '
            'image, and keeps it. [[slnc 300]] Every time after that, it '
            'reuses the one it kept. [[slnc 600]] And when asked for its '
            'product code, it answers from its own record. [[slnc 300]] '
            'Without loading anything. [[slnc 500]] That matters. [[slnc '
            '300]] A proxy that loads the real thing just to answer a '
            'cheap question has defeated its own purpose.'
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
            'Here is a detail worth pausing on: the restricted proxy. '
            '[[slnc 400]] It wraps any product image, not just a '
            'full-size one. [[slnc 500]] That is what lets it wrap a lazy '
            'image. [[slnc 300]] So you get the role check and the lazy '
            'loading together. [[slnc 300]] From two small classes that '
            'were never written with each other in mind. [[slnc 600]] And '
            'notice the order. [[slnc 300]] If the role check fails, it '
            'refuses before touching the image it wraps. [[slnc 300]] So '
            'a refused shopper never causes a load at all. [[slnc 300]] '
            'The expensive work is skipped, because the access decision '
            'came first.'
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
            "Let's run the project. [[slnc 400]] The naive listing has "
            'loaded three images before showing anything. [[slnc 500]] '
            'The lazy proxy has loaded none. [[slnc 300]] The real image '
            'has not been touched. [[slnc 300]] After the first time it '
            'is shown, one image is loaded. [[slnc 300]] After the second '
            'time, still only one, because it was kept. [[slnc 600]] Then '
            'the restricted proxy lets an admin through, and refuses a '
            'shopper. [[slnc 500]] And in the combined example, the '
            'restricted image stays unloaded, right up until an admin '
            'passes the check. [[slnc 300]] One proxy wrapped in the '
            'other, doing both jobs at once.'
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
            'So, to recap. [[slnc 400]] Use a proxy when the caller '
            'should not have to manage when an object is created. [[slnc '
            '300]] Or whether it may be used at all. [[slnc 600]] Keep '
            "the proxy's shape identical to the real object. [[slnc 300]] "
            'And keep cheap questions cheap. [[slnc 300]] Never load the '
            'real thing just to answer one. [[slnc 600]] And one '
            'comparison worth knowing. [[slnc 300]] A proxy and a '
            'decorator look the same: same shape, passing calls along. '
            '[[slnc 300]] But a proxy controls access: when to create, '
            'and whether to allow. [[slnc 300]] A decorator adds new '
            'behaviour on top. [[slnc 300]] Same shape, different '
            'purpose.'
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
            "That's the Proxy pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] A proxy is a '
            'stand-in with the same shape as the real thing, deciding '
            'when it is built, and who may use it. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 300]] It runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            'Add a third proxy that counts how often each image is shown. '
            '[[slnc 300]] And notice the caller does not change. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
