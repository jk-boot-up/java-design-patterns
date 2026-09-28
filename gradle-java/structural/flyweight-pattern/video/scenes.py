"""Scene definitions for the Flyweight pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "title" | "bullets" | "code" | "console" | "diagram"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="The Flyweight Pattern",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Flyweight pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Flyweight pattern stops '
            'you paying for the same data twice. [[slnc 300]] The parts '
            'of an object that are identical across thousands of copies '
            'are stored once, and shared. [[slnc 300]] And the parts that '
            'differ are passed in, at the moment they are needed. [[slnc '
            '600]] Think of a rubber stamp. [[slnc 300]] One stamp, used '
            'again and again, in a different place each time. [[slnc '
            '700]] In our online store, we look at the small badges shown '
            'on product listings. [[slnc 500]] By the end, you will know '
            'what a flyweight is, what shared and passed-in state mean, '
            'and how to write one yourself.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online store lists one hundred thousand products.",
            "",
            "Every listing shows a small badge:",
            "  NEW   ·   SALE   ·   BESTSELLER   ·   LOW STOCK",
            "",
            "Only four distinct badge designs exist —",
            "but a hundred thousand listings need one each.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] The store lists one '
            'hundred thousand products. [[slnc 300]] Every listing shows '
            'a small badge in the corner. [[slnc 300]] New. [[slnc 200]] '
            'Sale. [[slnc 200]] Bestseller. [[slnc 200]] Or low stock. '
            '[[slnc 600]] Notice this already. [[slnc 300]] There are '
            'only four different badge designs. [[slnc 300]] But a '
            'hundred thousand listings each need one.'
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="What a Badge Design Actually Is",
        body=[
            "icon               — a small glyph, e.g. a star",
            "backgroundColor    — fixed per badge type",
            "textColor          — fixed per badge type",
            "bold               — fixed per badge type",
            "artwork            — a rendered 64 KB icon bitmap",
            "",
            "Every SALE badge in the catalog looks identical.",
        ],
        narration=(
            'Here is what makes up one badge design. [[slnc 500]] An '
            'icon. [[slnc 200]] A background colour. [[slnc 200]] A text '
            'colour. [[slnc 200]] Whether the text is bold. [[slnc 200]] '
            'And a picture, sixty-four kilobytes in size. [[slnc 600]] '
            'And here is the key point. [[slnc 300]] Every sale badge in '
            'the whole catalog looks exactly the same. [[slnc 300]] Same '
            'icon, same colours, same picture. [[slnc 300]] Only the '
            'listing underneath it changes.'
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — One Badge Object Per Listing",
        body="""public NaiveListingBadge(BadgeType type, String listingId) {
    this.listingId = listingId;
    this.type = type;
    this.artwork = new byte[BadgeStyle.ARTWORK_BYTES];   // 64 KB, every time
    switch (type) {
        case SALE -> {
            this.icon = "★";
            this.backgroundColor = "#DC2626";
            this.textColor = "#FFFFFF";
            this.bold = true;
        }
        //  ...NEW, BESTSELLER, LOW_STOCK follow the same shape
    }
}

//  Called once per listing — one hundred thousand times""",
        narration=(
            'Here is the naive approach. [[slnc 400]] Every time a badge '
            'is made for a listing, a brand new sixty-four-kilobyte '
            'picture is created. [[slnc 300]] And the icon and colours '
            'are rebuilt from scratch. [[slnc 600]] That happens once per '
            'listing. [[slnc 300]] One hundred thousand times. [[slnc '
            '300]] So every sale badge holds its own private copy of '
            'exactly the same data.'
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   100,000 listings x 64 KB artwork ≈ 6,250 MB",
            "✗   Only 4 distinct designs actually exist",
            "✗   Every one of those bytes is a duplicate",
            "✗   Garbage collector churns through repeated allocations",
            "✗   No individual badge is wrong — the waste is structural",
        ],
        narration=(
            'That does real damage, to memory. [[slnc 500]] One hundred '
            'thousand listings, each with a sixty-four-kilobyte picture, '
            'adds up to about six gigabytes. [[slnc 300]] For just four '
            'different designs. [[slnc 600]] Almost every one of those '
            "bytes is a duplicate. [[slnc 300]] And Java's memory cleaner "
            'has to work through all those repeated copies. [[slnc 600]] '
            'To be clear, no single badge is wrong. [[slnc 300]] Each one '
            'displays correctly. [[slnc 300]] The waste is in the '
            'structure, not a bug.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Flyweight Pattern",
        body=[
            "“Uses sharing to support large numbers of",
            "fine-grained objects efficiently, by factoring",
            "out state that is shared (intrinsic) from state",
            "supplied by the caller (extrinsic).”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "stop paying for the same data twice.",
        ],
        narration=(
            'The Flyweight pattern fixes exactly this. [[slnc 400]] The '
            'classic book on design patterns, by the authors known as the '
            'Gang of Four, describes it like this. [[slnc 300]] Use '
            'sharing to support large numbers of small objects '
            'efficiently. [[slnc 300]] By separating the state that is '
            'shared, called intrinsic, from the state the caller '
            'supplies, called extrinsic. [[slnc 600]] In plain words: '
            'stop paying for the same data twice.'
        ),
    ),
    dict(
        key="07-stamp",
        kind="bullets",
        title="Remember It With a Rubber Stamp",
        body=[
            "A rubber stamp carries fixed ink and a fixed shape —",
            "that never changes between uses.",
            "",
            "Where you press it on the page is different every time.",
            "",
            "The stamp is the flyweight — shared.",
            "The position on the page is extrinsic — supplied by you.",
        ],
        narration=(
            'Here is how to remember it. [[slnc 300]] Think about a '
            'rubber stamp. [[slnc 500]] The stamp carries its ink and its '
            'shape. [[slnc 300]] That never changes, however many times '
            'you use it. [[slnc 500]] But where you press it on the page '
            'is different every time. [[slnc 600]] The stamp is the '
            'flyweight. [[slnc 300]] It is shared. [[slnc 300]] The '
            'position on the page is extrinsic. [[slnc 300]] You supply '
            'it fresh, each time.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            'Every flyweight has four roles. [[slnc 500]] The flyweight '
            'itself: here, the badge style. [[slnc 300]] The factory: the '
            'only place a badge style is ever built. [[slnc 300]] The '
            'context: a catalog badge, cheap and plentiful, one per '
            'listing. [[slnc 300]] And the client: the demo code, which '
            'asks the factory for styles. [[slnc 600]] Here is the most '
            'important idea in this video. [[slnc 300]] The factory hands '
            'out the same shared style to everyone who asks for the same '
            'type. [[slnc 300]] One badge style object. [[slnc 300]] A '
            'hundred thousand listings pointing at it.'
        ),
    ),
    dict(
        key="09-flyweight",
        kind="code",
        title="The Flyweight — Only Intrinsic State, No Setters",
        body="""public final class BadgeStyle {

    private final BadgeType type;
    private final String icon;
    private final String backgroundColor;
    private final String textColor;
    private final boolean bold;
    private final byte[] artwork;          // built once, shared forever

    public String render(String listingId, String customLabel) {
        String label = customLabel != null ? customLabel : type.name();
        String text  = bold ? label.toUpperCase() : label;
        return "[%s] %s %s on %s (bg=%s, fg=%s)"
                .formatted(type, icon, text, listingId, backgroundColor, textColor);
    }
}""",
        narration=(
            'Here is the flyweight: the badge style. [[slnc 400]] '
            'Everything it holds is shared state. [[slnc 300]] The icon, '
            'the colours, the bold setting, and the picture. [[slnc 300]] '
            'Identical for every sale badge, whichever listing asks. '
            '[[slnc 600]] Now look at how it draws itself. [[slnc 300]] '
            "The listing's I D, and any custom label, are passed in each "
            'time. [[slnc 300]] That is the extrinsic state, and it is '
            'never stored on the shared object. [[slnc 600]] And the '
            'style can never be changed after it is built, on purpose. '
            '[[slnc 300]] Changing a shared object would change every '
            'listing that uses it.'
        ),
    ),
    dict(
        key="10-factory",
        kind="code",
        title="The Factory — computeIfAbsent Does All the Work",
        body="""public final class BadgeStyleFactory {

    private static final Map<BadgeType, BadgeStyle> CACHE = new ConcurrentHashMap<>();

    public static BadgeStyle styleFor(BadgeType type) {
        return CACHE.computeIfAbsent(type, BadgeStyleFactory::build);
    }

    private static BadgeStyle build(BadgeType type) {
        return switch (type) {
            case SALE -> new BadgeStyle(type, "★", "#DC2626", "#FFFFFF", true);
            //  ...NEW, BESTSELLER, LOW_STOCK
        };
    }
}""",
        narration=(
            'Here is the factory. [[slnc 400]] It keeps a small cache, '
            'one entry per badge type. [[slnc 500]] The first time anyone '
            'asks for the sale style, it is built, and stored in the '
            'cache. [[slnc 300]] Every request after that, for any '
            'listing, gets back that exact same object. [[slnc 500]] The '
            'cache is a map built for many threads at once. [[slnc 300]] '
            'So it is safe to use from anywhere, with no extra locking.'
        ),
    ),
    dict(
        key="11-provides",
        kind="bullets",
        title="What the Flyweight Gives You",
        body=[
            "✓   Sharing    —  one BadgeStyle per type, not per listing",
            "✓   Correctness — thread-safe caching with no explicit locks",
            "✓   Separation — intrinsic fields, extrinsic parameters, never mixed",
            "",
            "And notice what is missing: per-listing state on BadgeStyle.",
            "",
            "A flyweight shares. It never remembers who asked.",
        ],
        narration=(
            'So the flyweight gives us three things. [[slnc 500]] '
            'Sharing: one badge style per type, not per listing. [[slnc '
            '300]] Safety: a thread-safe cache, with no locks to write '
            'ourselves. [[slnc 300]] And separation: shared data stored, '
            'and per-listing data passed in, never mixed. [[slnc 600]] '
            'Now notice what the badge style does not contain. [[slnc '
            '300]] Nothing about any particular listing. [[slnc 500]] A '
            'flyweight shares. [[slnc 300]] It never remembers who asked.'
        ),
    ),
    dict(
        key="12-client",
        kind="code",
        title="The Client — This Is the Whole Thing",
        body="""public final class CatalogBadge {

    private final BadgeStyle style;
    private final String listingId;

    public CatalogBadge(BadgeType type, String listingId, String customLabel) {
        this.style = BadgeStyleFactory.styleFor(type);   // shared, not built
        this.listingId = listingId;
    }

    public String render() {
        return style.render(listingId, customLabel);
    }
}

//  100,000 CatalogBadge objects. As few as 4 BadgeStyle objects.""",
        narration=(
            'Here is the context object: the catalog badge. [[slnc 400]] '
            'When it is created, it does not build a style. [[slnc 300]] '
            'It asks the factory for one, and keeps a reference to the '
            'shared style. [[slnc 500]] It only owns two things itself: '
            'the listing I D, and an optional custom label. [[slnc 300]] '
            'Everything else, it borrows. [[slnc 600]] So you can create '
            'a hundred thousand catalog badges. [[slnc 300]] And behind '
            'them, just four badge styles do all the heavy lifting.'
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

== Proving the sharing ==
styleFor(SALE) == styleFor(SALE): true
sample.get(1).style() == sample.get(2).style(): true
BadgeStyle instances actually created: 4

== The naive alternative, for comparison ==
naiveA == naiveB (both SALE): false

== Memory arithmetic for a 100000-listing catalog ==
Naive:      100,000 badges x 64 KB artwork each = 6,250 MB
Flyweight:  4 styles x 64 KB artwork each     = 256 KB
Savings:    6,249 MB avoided by sharing 4 instances instead of 100,000""",
        narration=(
            "Let's run the project. [[slnc 400]] Ask the factory for the "
            'sale style twice, and you get the very same object, both '
            'times. [[slnc 300]] Two different listings share one style. '
            '[[slnc 300]] Only four badge styles were ever created. '
            '[[slnc 600]] Now the naive version. [[slnc 300]] Two '
            'identical sale badges are two separate objects. [[slnc 600]] '
            'And the memory numbers. [[slnc 300]] About six gigabytes '
            'with the naive version. [[slnc 300]] About two hundred and '
            'fifty-six kilobytes with the flyweight. [[slnc 300]] Just by '
            'sharing four objects, instead of a hundred thousand.'
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use a flyweight when object count is huge",
            "and most of each object's state repeats.",
            "",
            "Keep intrinsic state as fields, extrinsic state as parameters.",
            "Never give a flyweight a setter.",
            "Only worth it at scale — five listings don't need this.",
            "",
            "Remember one sentence:",
            "Prototype hands out copies. Flyweight hands out",
            "the same instance, again and again.",
        ],
        narration=(
            'So, to recap. [[slnc 400]] Use a flyweight when you have a '
            "huge number of objects, and most of each one's data repeats. "
            '[[slnc 600]] Store shared data inside the flyweight. [[slnc '
            '300]] Pass per-use data in, each time. [[slnc 300]] And '
            'never let a flyweight be changed. [[slnc 500]] It is only '
            'worth it at scale. [[slnc 300]] Five listings do not need a '
            'cache. [[slnc 600]] And one comparison worth knowing. [[slnc '
            '300]] The Prototype pattern hands out copies. [[slnc 300]] A '
            'flyweight hands out the same object, again and again.'
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "If this helped, a thumbs up and a subscribe go a long way",
            "towards keeping more videos like it coming.",
            "",
            "Full source code, notes and an animation are in the repository.",
        ],
        narration=(
            "That's the Flyweight pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Store the '
            'shared part once, pass the changing part in, and a hundred '
            'thousand objects can share four. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 300]] It runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            'Add a fifth badge type, like free delivery. [[slnc 300]] And '
            'check that still only one style is built for it. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
