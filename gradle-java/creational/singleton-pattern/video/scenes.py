#!/usr/bin/env python3
"""The script for the Singleton Pattern video.

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
        title="Singleton Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Singleton pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. [[slnc "
            "300]] Let's start with the simple definition. The singleton pattern "
            "guarantees that a class has exactly one instance, and gives every "
            "caller one well-known way of reaching it. The class takes control of "
            "its own creation, so however you ask — and we'll see some determined "
            "ways of asking — you cannot get a second one. [[slnc 350]] That's "
            "the idea in a sentence. It's the smallest pattern in the Gang of "
            "Four book, and the one Java developers reach for the most casually. "
            "The rest of the video does it properly, by building a real working "
            "Java project: an order-number sequencer for an online store, in Java "
            "twenty one. [[slnc 250]] And along the way we'll watch a private "
            "constructor get called anyway — twice — by two attacks that "
            "Effective Java's favourite singleton shape is immune to."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Job",
        body=[
            "Every checkout needs an order number: ORD-000001, ORD-000002...",
            "handed out in strict sequence, no gaps, no repeats.",
            "",
            "•  checkout, the admin console, and a background retry job",
            "•  all three must issue numbers from the same counter",
            "",
            "Two different customers must never receive the same number.",
        ],
        narration=(
            "So here's the job. Every checkout on our marketplace needs an "
            "order number — ORD-000001, ORD-000002, and so on — handed out "
            "in strict sequence, no gaps, no repeats. [[slnc 250]] "
            "Checkout issues them. So does the admin console, when support "
            "staff raise a manual order. So does a background job replaying "
            "a failed payment. All three have to draw from the same "
            "counter, or two different customers can end up with the same "
            "order number."
        ),
    ),
    dict(
        key="03-instance-per-caller",
        kind="code",
        title="An Instance Per Caller",
        body="""public class OrderSequenceGenerator {
    private int counter;
    public String nextOrderNumber() {
        counter++;
        return String.format("ORD-%06d", counter);
    }
}

// in CheckoutService:      new OrderSequenceGenerator().nextOrderNumber();  // ORD-000001
// in AdminConsoleService:  new OrderSequenceGenerator().nextOrderNumber();  // ORD-000001 — collision""",
        narration=(
            "Reasonable-looking class. The problem shows up the moment two "
            "different parts of the system each construct their own. "
            "[[slnc 300]] "
            "Checkout builds one, admin console builds another, and each "
            "new OrderSequenceGenerator starts its own counter at zero. "
            "There's nothing wrong with the class itself — the bug is that "
            "the language lets anyone construct as many of it as they "
            "like, when the rule is exactly one, ever."
        ),
    ),
    dict(
        key="04-classic-fix",
        kind="code",
        title="The Classic Fix",
        body="""public final class LegacyOrderSequenceGenerator {
    private static LegacyOrderSequenceGenerator instance;
    private LegacyOrderSequenceGenerator() { }

    public static LegacyOrderSequenceGenerator getInstance() {
        if (instance == null) {
            instance = new LegacyOrderSequenceGenerator();
        }
        return instance;
    }
}""",
        narration=(
            "The textbook fix takes new away from callers and hands back "
            "one shared instance instead. Private constructor, static "
            "field, public getInstance. [[slnc 300]] "
            "Every caller now goes through getInstance, and under normal "
            "use it really does return the same object every time. Private "
            "means private... or does it?"
        ),
    ),
    dict(
        key="05-attack-reflection",
        kind="code",
        title="Breaking It: Reflection",
        body="""Constructor<LegacyOrderSequenceGenerator> ctor =
        LegacyOrderSequenceGenerator.class.getDeclaredConstructor();
ctor.setAccessible(true);
LegacyOrderSequenceGenerator forged = ctor.newInstance();   // succeeds

// forged != LegacyOrderSequenceGenerator.getInstance()  -> true, a second instance exists""",
        narration=(
            "Reflection can call a private constructor directly. Get "
            "declared constructor, set accessible true, new instance — and "
            "it just works. [[slnc 300]] "
            "'Private' is a compile-time convention the compiler checks, "
            "not an absolute the J V M enforces at runtime. Frameworks and "
            "testing tools use exactly this trick for legitimate reasons, "
            "and they never asked this class's permission first."
        ),
    ),
    dict(
        key="06-attack-serialization",
        kind="code",
        title="Breaking It: Serialization",
        body="""ByteArrayOutputStream bytes = new ByteArrayOutputStream();
new ObjectOutputStream(bytes).writeObject(LegacyOrderSequenceGenerator.getInstance());

Object roundTripped = new ObjectInputStream(
        new ByteArrayInputStream(bytes.toByteArray())).readObject();

// roundTripped != LegacyOrderSequenceGenerator.getInstance()  -> true, another second instance""",
        narration=(
            "Second attack, no reflection needed at all. Java's default "
            "serialization never calls a constructor — it rebuilds an "
            "object's fields straight from bytes. [[slnc 300]] "
            "Serialize the shared instance, deserialize it, and what comes "
            "back is a brand-new object, counter reset to zero, silently. "
            "Two separate holes, in a class that was written specifically "
            "to prevent a second instance from ever existing."
        ),
    ),
    dict(
        key="07-definition",
        kind="quote",
        title="The Singleton Pattern",
        body=[
            "Ensure a class only has one instance, and provide a global",
            "point of access to it.",
            "",
            "— Gang of Four, Design Patterns",
            "",
            "In plain words: make it impossible to construct more than one,",
            "and give every caller the same well-known way to reach it.",
        ],
        narration=(
            "The Gang of Four's definition is short. Ensure a class only "
            "has one instance, and provide a global point of access to it. "
            "[[slnc 300]] "
            "In plain words? Make it impossible to construct more than one "
            "of this class, and give every caller in the program the same "
            "well-known way to reach the instance that does exist. The "
            "question this project actually answers is narrower, though: "
            "which Java shape makes that impossible, and which shapes only "
            "look like they do."
        ),
    ),
    dict(
        key="08-shape",
        kind="diagram",
        title="The Shape of It",
        body=None,
        narration=(
            "So here's the shape of it. OrderSequenceGenerator is a "
            "single-element enum — instance is a constant the J V M "
            "creates exactly once, during class loading, before any "
            "caller's code can even reference it. [[slnc 300]] "
            "Three guarantees come with that for free: the J V M's "
            "class-loading is thread-safe by the language specification, "
            "reflection is barred outright from calling an enum's "
            "constructor, and enum deserialization resolves by name "
            "against the existing constant instead of building a new "
            "object."
        ),
    ),
    dict(
        key="09-enum",
        kind="code",
        title="One Constant, Three Guarantees",
        body="""public enum OrderSequenceGenerator {
    INSTANCE;

    private final AtomicLong counter = new AtomicLong();

    public String nextOrderNumber() {
        return String.format("ORD-%06d", counter.incrementAndGet());
    }
}

// no constructor to call, no getInstance(), no null check, no lock""",
        narration=(
            "That is the entire singleton. No private constructor to "
            "remember to write, no getInstance method, no null check, no "
            "lock. [[slnc 300]] "
            "Constructor dot new instance on an enum throws "
            "IllegalArgumentException — the reflection A P I refuses "
            "outright, no defensive code required here. And serializing "
            "instance and reading it back hands you the exact same "
            "instance, because the language defines an enum's serialized "
            "form as its name, not its fields."
        ),
    ),
    dict(
        key="10-atomic",
        kind="code",
        title="Why AtomicLong",
        body="""private final AtomicLong counter = new AtomicLong();

public String nextOrderNumber() {
    return String.format("ORD-%06d", counter.incrementAndGet());
}

// counter++ on a plain int: two threads can read the same value and both increment it
// counter.incrementAndGet(): one atomic operation, no lost updates, ever""",
        narration=(
            "One detail that only matters once you've actually solved the "
            "instance problem. [[slnc 250]] "
            "Now that there truly is exactly one instance, it's reachable "
            "from every thread in the program at once, so the state it "
            "carries has to be safe to mutate concurrently. Counter plus "
            "plus on a plain int is a read, then a write — two threads can "
            "interleave and lose an increment. Increment and get on an "
            "atomic long is a single atomic operation. No two callers can "
            "ever collide on the same number."
        ),
    ),
    dict(
        key="11-run",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

== The fix: an enum singleton ==
first == second: true
ORD-000001
ORD-000002

== Attacking it: reflection ==
Rejected: Cannot reflectively create enum objects

== Attacking it: serialization ==
roundTripped == INSTANCE: true

== The trap: a classic private-constructor singleton ==
legacyFirst == legacySecond: true
ORD-000001

== Breaking it: reflection ==
forged == legacyFirst: false

== Breaking it: serialization ==
legacyRoundTripped == legacyFirst: false""",
        narration=(
            "Let's run it, and see the whole story on one screen. "
            "[[slnc 250]] "
            "The enum issues order numbers, rejects the reflection attack "
            "with a clear exception, and comes back as the exact same "
            "instance after a serialization round trip. [[slnc 300]] "
            "Then the legacy class — identical to callers under normal "
            "use — falls to both of the exact same attacks. Same two lines "
            "of attacking code, run against two classes that look "
            "identical from the outside, with opposite outcomes."
        ),
    ),
    dict(
        key="12-limits",
        kind="bullets",
        title="Where It Stops",
        body=[
            "✗  It's global mutable state — no per-test or per-tenant instance",
            "✗  It hides a dependency the method signature never shows",
            "✗  Wrong tool when the real need is one-per-caller, not one-total",
            "",
            "✓  Reach for it only when the domain genuinely requires exactly one.",
        ],
        narration=(
            "Now the honest part. Every pattern has a ceiling, and this "
            "one's is real. [[slnc 300]] "
            "A singleton is global mutable state dressed up in a pattern "
            "name — any code anywhere can reach INSTANCE, and there's no "
            "clean way to give one test its own counter. It hides a "
            "dependency, too: a method calling INSTANCE inside its body "
            "doesn't show that dependency in its signature the way a "
            "parameter would. [[slnc 250]] "
            "And the moment the system needs a separate sequence per "
            "storefront or per warehouse, 'exactly one for the whole J V "
            "M' is precisely the wrong guarantee — no amount of tuning "
            "fixes that, the pattern itself has to go."
        ),
    ),
    dict(
        key="13-family",
        kind="bullets",
        title="How It Relates to the Others",
        body=[
            "Prototype           I have one — get me another   copy an existing instance",
            "Builder              which pieces, in what order?  one object, assembled gradually",
            "Abstract Factory     which whole set?               one choice, many objects",
            "Singleton            how many should exist?         exactly one, enforced",
            "",
            "The other three control how an object is built. Singleton controls how many.",
        ],
        narration=(
            "So where does singleton sit next to the other creational "
            "patterns? [[slnc 250]] "
            "Prototype answers 'I have one, get me another.' Builder "
            "answers 'which pieces, assembled in what order.' Abstract "
            "factory answers 'which whole matching set.' Singleton is the "
            "odd one out — it says nothing about assembly at all, and "
            "controls how many instances exist, full stop. [[slnc 300]] "
            "It's also the one most often reached for to solve a different "
            "problem — 'I don't want to pass this object around' — which "
            "dependency injection solves without the global-state cost."
        ),
    ),
    dict(
        key="14-wrap",
        kind="title",
        title="One Sentence to Keep",
        body=[
            "A private constructor is a promise the compiler checks, not",
            "one the JVM enforces at runtime. A single-element enum is the",
            "one Java singleton shape that closes both holes, for free.",
        ],
        narration=(
            "If you keep one sentence from all of this, keep this one. "
            "[[slnc 300]] "
            "A private constructor is a promise the compiler checks, not "
            "one the J V M enforces at runtime — reflection and "
            "serialization can both break it. A single-element enum is the "
            "one Java singleton shape that closes both holes, for free, "
            "with no extra code. [[slnc 350]] "
            "There's a full set of notes in the project, an animated "
            "walkthrough you can step through at your own pace, and a "
            "session plan if you fancy teaching this to somebody else. Go "
            "add a readResolve method to the legacy class, and watch "
            "exactly one of the two attacks start failing."
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
            "Full source code, notes and diagrams are in the repository.",
        ],
        narration=(
            "And that's the singleton pattern. [[slnc 300]] "
            "If you got something out of this, do give it a thumbs up, and "
            "subscribe. It genuinely helps the channel, and it's what "
            "makes more of these possible. [[slnc 250]] "
            "And if there's a pattern you'd like me to cover next, drop it "
            "in the comments. I read every one. [[slnc 250]] "
            "All the source code, the written notes and the diagrams are "
            "in the repository. Thanks for watching, and I'll see you in "
            "the next one."
        ),
    ),
]
