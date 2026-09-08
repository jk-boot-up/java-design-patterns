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
            "Hello, and welcome. This video explains the Flyweight pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. [[slnc "
            "300]] Let's start with the simple definition. The flyweight pattern "
            "stops you paying for the same data twice. The parts of an object "
            "that are identical across thousands of instances are stored once and "
            "shared between all of them, and everything that actually differs is "
            "passed in from outside at the moment it is needed. [[slnc 350]] "
            "That's the idea in a sentence, and it's a pattern that only shows up "
            "once your object count gets large. The rest of the video does it "
            "properly, by building a real working Java project: badge rendering "
            "across an e-commerce catalog. [[slnc 250]] By the end you'll know "
            "what a flyweight is, what intrinsic and extrinsic state actually "
            "mean, and how to write one yourself."
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
            "So, imagine an online store with one hundred thousand product "
            "listings. [[slnc 250]] Every single listing shows a small badge in "
            "the corner. New. Sale. Bestseller. Low stock. [[slnc 300]] Here's "
            "the thing to notice already. There are only four distinct badge "
            "designs in the whole catalog. But a hundred thousand listings each "
            "need one drawn."
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
            "Look at what actually makes up one badge design. An icon. A "
            "background colour. A text colour. Whether it's bold. And a "
            "rendered artwork bitmap, sixty four kilobytes. [[slnc 300]] And "
            "here's the key observation. Every single SALE badge in the entire "
            "catalog looks completely identical. Same icon, same colours, same "
            "artwork. Only the listing underneath it changes."
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
            "So here's the naive approach. [[slnc 250]] Every time we build a "
            "badge for a listing, we allocate a brand new sixty four kilobyte "
            "artwork array, and we rebuild the icon and the colours from "
            "scratch, based on a switch over the type. [[slnc 300]] That "
            "constructor runs once per listing. One hundred thousand times. And "
            "every single SALE badge ends up holding its own private, identical "
            "copy of the exact same data."
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
            "And that does real damage, purely on memory. [[slnc 250]] One "
            "hundred thousand listings, each with a sixty four kilobyte "
            "artwork, comes to roughly six point two five gigabytes. For four "
            "distinct designs. [[slnc 300]] Every one of those bytes past the "
            "first four copies is a pure duplicate. And the garbage collector "
            "has to work through all those repeated allocations. [[slnc 250]] "
            "To be clear, no individual badge object is wrong. It renders "
            "correctly. The waste is structural, not a bug."
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
            "The flyweight pattern fixes exactly this. [[slnc 250]] And the "
            "definition, in Gang of Four terms, is that a flyweight uses "
            "sharing to support large numbers of fine grained objects "
            "efficiently, by factoring out state that is shared, called "
            "intrinsic, from state supplied by the caller, called extrinsic. "
            "[[slnc 300]] In plain language? Stop paying for the same data "
            "twice."
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
            "Here's how to remember it forever. Think about a rubber stamp. "
            "[[slnc 250]] The stamp itself carries fixed ink, and a fixed "
            "shape. That never changes, no matter how many times you use it. "
            "[[slnc 300]] But where you press it down on the page? That's "
            "different every single time. [[slnc 250]] The stamp is the "
            "flyweight. It gets shared. The position on the page is extrinsic. "
            "You supply it fresh, every time you stamp."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            "Every flyweight setup has four roles. [[slnc 200]] The flyweight "
            "itself, which here is BadgeStyle. The flyweight factory, "
            "BadgeStyleFactory, which is the only place a BadgeStyle ever gets "
            "built. The context, CatalogBadge, which is cheap and plentiful, "
            "one per listing. And the client, BadgeDemo, which asks the "
            "factory for styles. [[slnc 350]] Here's the single most important "
            "idea in this whole video. The factory hands out the same shared "
            "instance to every caller asking for the same type. One BadgeStyle "
            "object. A hundred thousand listings pointing at it."
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
            "This is the flyweight itself, BadgeStyle. [[slnc 250]] Every "
            "field on it — the icon, the colours, the bold flag, the artwork "
            "— is intrinsic. Identical for every SALE badge, no matter which "
            "listing is asking. [[slnc 300]] And look closely at render. "
            "listingId and customLabel arrive as parameters, not fields. "
            "That's extrinsic state, supplied fresh by the caller every time, "
            "and never stored on the shared object. [[slnc 250]] There are no "
            "setters here, on purpose. Mutating a shared instance would "
            "corrupt every listing sharing it."
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
            "And this is the factory. [[slnc 250]] One line does the entire "
            "pattern's work. Cache dot computeIfAbsent, keyed by badge type. "
            "[[slnc 300]] The very first time anyone asks for SALE, the "
            "lambda runs, build constructs a brand new BadgeStyle, and it goes "
            "into the cache. Every single call after that — for any listing, "
            "from any thread — finds SALE already there, and gets back that "
            "exact same instance. [[slnc 250]] Using a ConcurrentHashMap means "
            "this is safe under concurrent access with no extra locking at "
            "all."
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
            "So the flyweight is giving us three things. [[slnc 200]] "
            "Sharing — one BadgeStyle per badge type, not per listing. "
            "Correctness — thread-safe caching, with no locks we had to write "
            "ourselves. And separation — intrinsic fields and extrinsic "
            "parameters, cleanly kept apart. [[slnc 350]] Now notice what it "
            "doesn't contain. There is no per-listing state anywhere on "
            "BadgeStyle. [[slnc 250]] A flyweight shares. It never remembers "
            "who asked."
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
            "And here's the context object that ties it together, "
            "CatalogBadge. [[slnc 250]] Its constructor doesn't build a "
            "style. It asks the factory for one, and holds a shared "
            "reference. It owns exactly two things itself: the listing id and "
            "an optional custom label. Everything else, it borrows. [[slnc "
            "300]] So you can create a hundred thousand of these CatalogBadge "
            "objects, and behind them, as few as four actual BadgeStyle "
            "instances doing all the heavy lifting."
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
            "When we run the project, the proof is right there in the "
            "output. [[slnc 250]] styleFor SALE, called twice, returns true "
            "for equals equals — the exact same object, both times. Two "
            "different listings share one style instance. [[slnc 300]] Now "
            "compare that to the naive alternative. naive A equals naive B, "
            "for two identical SALE badges, is false. Same input, opposite "
            "identity. [[slnc 300]] And at the bottom, the arithmetic that "
            "makes it matter. Six thousand two hundred fifty megabytes, down "
            "to two hundred fifty six kilobytes, just by sharing four "
            "instances instead of a hundred thousand."
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
            "So, to recap. Use a flyweight when your object count is huge, "
            "and most of each object's state repeats across instances. [[slnc "
            "300]] Keep intrinsic state as fields, extrinsic state as "
            "parameters, and never give a flyweight a setter. And remember, "
            "this pattern is only worth it at scale — five listings do not "
            "need a cache. [[slnc 350]] And if you remember one sentence from "
            "today, make it this one. Prototype hands out copies. Flyweight "
            "hands out the same instance, again and again."
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
            "And that's the flyweight pattern. [[slnc 300]] If you got "
            "something out of this, do give it a thumbs up, and subscribe. It "
            "genuinely helps the channel, and it's what makes more of these "
            "possible. [[slnc 250]] And if there's a pattern you'd like me to "
            "cover next, drop it in the comments. I read every one. [[slnc "
            "250]] All the source code, the written notes and an interactive "
            "animation are in the repository. Thanks for watching, and I'll "
            "see you in the next one."
        ),
    ),
]
