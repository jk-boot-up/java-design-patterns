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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Singleton pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Singleton pattern '
            'guarantees that a class has exactly one instance. [[slnc '
            '300]] And it gives every caller one well-known way to reach '
            'it. [[slnc 400]] The class controls its own creation, so no '
            'matter how you ask, you cannot get a second one. [[slnc '
            "600]] Think of a country's official clock. [[slnc 300]] "
            'Everyone sets their watch from the same one. [[slnc 300]] '
            'Two official clocks would cause confusion. [[slnc 700]] In '
            'this video, we build an order number generator for an online '
            'store. [[slnc 500]] And we will watch a private constructor '
            'get called anyway, twice, by two tricks. [[slnc 300]] Then '
            'we will see the one Java shape that stops both.'
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
            'Here is the job. [[slnc 400]] Every checkout in our store '
            'needs an order number. [[slnc 300]] Order one, order two, '
            'order three, and so on. [[slnc 300]] In strict sequence, '
            'with no gaps, and no repeats. [[slnc 500]] Checkout creates '
            'order numbers. [[slnc 300]] So does the admin console, when '
            'support staff raise an order by hand. [[slnc 300]] So does a '
            'background job, retrying a failed payment. [[slnc 500]] All '
            'three must use the same counter. [[slnc 300]] Otherwise, two '
            'different customers could receive the same order number.'
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
            'Here is a reasonable-looking generator class. [[slnc 300]] '
            'It holds a counter, and each call adds one, and returns the '
            'next order number. [[slnc 500]] The problem appears when two '
            'parts of the system each create their own generator. [[slnc '
            '300]] Checkout creates one, and the admin console creates '
            'another. [[slnc 300]] Each one starts its own counter at '
            'zero. [[slnc 300]] So both hand out order number one. [[slnc '
            '500]] The class itself is fine. [[slnc 300]] The bug is that '
            'anyone can create as many as they like, when the rule is '
            'exactly one.'
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
            'The textbook fix takes creation away from callers. [[slnc '
            '400]] Make the constructor private. [[slnc 300]] Keep the '
            'one instance in a static field. [[slnc 300]] And add a '
            'public method, called get instance, that returns it. [[slnc '
            '500]] Now every caller goes through get instance. [[slnc '
            '300]] And in normal use, it really does return the same '
            'object every time. [[slnc 500]] Private means private. '
            '[[slnc 300]] Or does it?'
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
            "First trick: reflection. [[slnc 400]] Java's reflection "
            'features can find a private constructor, switch off its '
            'protection, and call it. [[slnc 300]] And it simply works. '
            '[[slnc 500]] A second generator now exists, separate from '
            'the shared one. [[slnc 500]] Private is a rule the compiler '
            'checks. [[slnc 300]] It is not something Java enforces while '
            'the program runs. [[slnc 300]] Frameworks and testing tools '
            'use this very trick, for good reasons, without asking the '
            'class.'
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
            "Second trick, with no reflection needed. [[slnc 400]] Java's "
            'built-in serialization can save an object as bytes, and '
            'rebuild it later. [[slnc 300]] And when it rebuilds, it '
            'never calls a constructor. [[slnc 500]] So save the shared '
            'generator, and read it back. [[slnc 300]] What comes back is '
            'a brand new object, with its counter reset to zero. [[slnc '
            '300]] Silently. [[slnc 500]] Two separate holes, in a class '
            'written specifically to prevent a second instance.'
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
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Ensure a class has only one '
            'instance, and provide a global point of access to it. [[slnc '
            '500]] In plain words: make it impossible to create more than '
            'one. [[slnc 300]] And give every caller the same, well-known '
            'way to reach it. [[slnc 500]] The real question this project '
            'answers is: which Java shape truly makes a second one '
            'impossible? [[slnc 300]] And which shapes only look like '
            'they do?'
        ),
    ),
    dict(
        key="08-shape",
        kind="diagram",
        title="The Shape of It",
        body=None,
        narration=(
            'Here is the shape of the answer. [[slnc 400]] The order '
            'number generator becomes an enum, with a single value, '
            'called INSTANCE. [[slnc 500]] Java creates that value '
            'exactly once, when the class is loaded, before any caller '
            'can even reach it. [[slnc 500]] That gives three guarantees, '
            'for free. [[slnc 300]] Loading a class is thread-safe, by '
            "Java's own rules. [[slnc 300]] Reflection is forbidden from "
            'creating enum values. [[slnc 300]] And reading an enum back '
            'from bytes returns the existing value, not a new one.'
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
            'That is the entire singleton. [[slnc 300]] An enum with one '
            'value, holding a counter, and a method that returns the next '
            'order number. [[slnc 500]] No private constructor to '
            'remember. [[slnc 300]] No get instance method. [[slnc 300]] '
            'No null check. [[slnc 300]] No lock. [[slnc 500]] Try the '
            'reflection trick, and Java refuses outright: it cannot '
            'reflectively create enum objects. [[slnc 300]] Try the '
            'serialization trick, and you get back the very same '
            'instance. [[slnc 300]] Because Java saves an enum by its '
            'name, not by its fields.'
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
            'One more detail, which only matters once there truly is one '
            'instance. [[slnc 500]] Now every thread in the program can '
            'reach that one generator, at the same time. [[slnc 300]] So '
            'its counter must be safe to change from many threads. [[slnc '
            '500]] Adding one to a plain number is really two steps: read '
            'it, then write it. [[slnc 300]] Two threads can both read '
            'the same value, and one increase is lost. [[slnc 500]] So '
            'the counter is an Atomic Long. [[slnc 300]] Its increment is '
            'one indivisible step. [[slnc 300]] So no two callers can '
            'ever get the same order number.'
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
            "Let's run the demo. [[slnc 500]] The enum hands out order "
            'one, then order two. [[slnc 300]] The reflection trick is '
            'rejected, with a clear error. [[slnc 300]] And after saving '
            'and reading back, it is still the exact same instance. '
            '[[slnc 500]] Then the classic private-constructor version. '
            '[[slnc 300]] In normal use, it looks identical. [[slnc 300]] '
            'But it falls to both tricks. [[slnc 500]] The same two '
            'tricks, used against two classes that look identical from '
            'outside, with opposite results.'
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
            'Now the honest part. [[slnc 300]] This pattern has real '
            'limits. [[slnc 500]] A singleton is global, changeable '
            'state, with a pattern name. [[slnc 300]] Any code anywhere '
            'can reach it. [[slnc 300]] And there is no clean way to give '
            'each test its own counter. [[slnc 500]] It also hides a '
            'dependency. [[slnc 300]] A method that uses the singleton '
            'inside its body does not show that in its parameters. [[slnc '
            '500]] And if the business later needs a separate sequence '
            'for each shop, or each warehouse, exactly one for the whole '
            'program is the wrong promise. [[slnc 300]] Then the pattern '
            'itself has to go. [[slnc 500]] Use it only when the business '
            'truly requires exactly one.'
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
            'So how does the Singleton relate to the other creational '
            'patterns? [[slnc 500]] Prototype answers: I have one, get me '
            'another. [[slnc 300]] Builder answers: which pieces, in what '
            'order. [[slnc 300]] Abstract Factory answers: which whole '
            'matching set. [[slnc 500]] Singleton is the odd one out. '
            '[[slnc 300]] It says nothing about how an object is built. '
            '[[slnc 300]] It only controls how many exist. [[slnc 500]] '
            'It is also often used to solve a different problem: I do not '
            'want to pass this object around. [[slnc 300]] Dependency '
            'injection solves that, without the cost of global state.'
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
            'If you keep one sentence from this video, keep this one. '
            '[[slnc 400]] A private constructor is a promise the compiler '
            'checks, not one Java enforces while the program runs. [[slnc '
            '300]] A single-value enum is the one Java singleton shape '
            'that closes both holes, for free. [[slnc 600]] The project '
            'has full notes, an animated walkthrough, and a teaching '
            'plan. [[slnc 300]] Try adding a read resolve method to the '
            'classic version. [[slnc 300]] And listen for which one of '
            'the two tricks stops working.'
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
            "That's the Singleton pattern. [[slnc 400]] The full source "
            'code, written notes, and diagrams are all in the repository. '
            '[[slnc 500]] If there is a pattern you would like to see '
            'covered, suggest it in the comments. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
