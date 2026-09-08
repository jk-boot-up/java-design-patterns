#!/usr/bin/env python3
"""The script for the Builder Pattern video.

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
        title="Builder Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Builder pattern in Java, "
            "and it is written and presented by Jayasekhar Konduru. [[slnc 300]] "
            "Let's start with the simple definition. The builder pattern "
            "constructs an object one piece at a time. Instead of a constructor "
            "taking a long list of arguments, you call a named method for each "
            "part you want to set, in whatever order suits you, and then one "
            "final method that validates the lot and hands back the finished "
            "object. [[slnc 350]] That's the idea in a sentence. It's in the "
            "original Gang of Four book, and it's also item two in Effective "
            "Java, and by the end you'll know exactly why both books claim it. "
            "The rest of the video does it properly, by building a real working "
            "Java project: a purchase order in an online store, in Java 21, "
            "picking up right where the static factory method left off. [[slnc "
            "250]] And you'll see the two of them compose, because one of them "
            "returns the other."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Job",
        body=[
            "A purchase order. Two facts are always required:",
            "",
            "•  an order id and a customer id",
            "•  at least one item, and a shipping address",
            "",
            "And five independent optional pieces:",
            "",
            "•  gift wrap, with an optional message",
            "•  a coupon code, priority shipping, and a free-text note",
        ],
        narration=(
            "So here's the job. We're building a purchase order. Two things "
            "about it are always true. It needs an order id and a customer id, "
            "and it needs at least one item and a shipping address. "
            "[[slnc 250]] "
            "But on top of that, there are five completely independent optional "
            "pieces. Gift wrap, which can carry a message. A coupon code. "
            "Priority shipping. And a free-text note. Any order might have none "
            "of those, or all of them, in any combination."
        ),
    ),
    dict(
        key="03-wall",
        kind="code",
        title="The Constructor With Nine Parameters",
        body="""public PurchaseOrder(String orderId, String customerId, List<LineItem> items,
                      Address shippingAddress, boolean giftWrapped, String giftMessage,
                      String couponCode, boolean priority, String notes) { ... }

new PurchaseOrder("ORD-9001", "CUST-100", items, home,
        true, "Happy birthday!", "WELCOME10", false, null);""",
        narration=(
            "So you write the constructor everyone starts with. Nine "
            "parameters, one for every fact this order might need. "
            "[[slnc 300]] "
            "Now look at the call underneath it, and tell me, quickly, is this "
            "the priority order, or the gift order? You have to count commas "
            "and cross-check against the parameter list to know. And there are "
            "two booleans in there. Swap them by accident, and the compiler "
            "says absolutely nothing."
        ),
    ),
    dict(
        key="04-telescoping",
        kind="code",
        title="Telescoping Constructors",
        body="""public PurchaseOrder(String orderId, String customerId, List<LineItem> items, Address a) { ... }
public PurchaseOrder(..., boolean giftWrapped) { ... }
public PurchaseOrder(..., boolean giftWrapped, String giftMessage) { ... }
public PurchaseOrder(..., String couponCode) { ... }
// every new option needs one more overload, or the nine-parameter constructor

Effective Java calls this the telescoping constructor pattern —
and it names it as the problem, not the solution.""",
        narration=(
            "The next instinct is to add smaller constructors on top, one for "
            "the common cases. But look what happens. A gift order without "
            "priority needs one overload. A gift order with a coupon needs "
            "another. Every new combination either needs a brand new overload, "
            "or you fall back to the nine-parameter one anyway. "
            "[[slnc 300]] "
            "Effective Java actually has a name for this. The telescoping "
            "constructor pattern. And it's named as the chapter's cautionary "
            "tale, not as something to reach for."
        ),
    ),
    dict(
        key="05-harm",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗  The call site does not say what it means",
            "✗  Most calls are mostly null, or mostly false",
            "✗  Parameter order is arbitrary — and unenforced",
            "✗  Every new option widens the constructor, and every caller",
            "✗  There is nowhere to put a rule that spans two fields",
            "",
            "The type is fine. The way in is the problem.",
        ],
        narration=(
            "And that costs you, in five specific ways. "
            "[[slnc 300]] "
            "One. The call site stops saying what it means. "
            "Two. Most calls are mostly null, or mostly false, because most "
            "orders don't use most of the options. "
            "Three. The parameter order is completely arbitrary, and nothing "
            "in the language enforces it. "
            "Four. Every new option widens the constructor, and every existing "
            "caller has to be touched, even the ones that never wanted the new "
            "option. "
            "And five, the one people miss: there is nowhere to put a rule like "
            "'a gift message implies gift wrap'. A constructor just assigns "
            "fields. [[slnc 300]] "
            "But notice, again, what isn't wrong. The type itself is fine. "
            "It's the way in that's the problem."
        ),
    ),
    dict(
        key="06-definition",
        kind="quote",
        title="The Builder Pattern",
        body=[
            "Separate the construction of a complex object from its",
            "representation so that the same construction process",
            "can create different representations.",
            "",
            "— Gang of Four, Design Patterns",
            "",
            "In plain words: decide the object a piece at a time,",
            "and check it is complete only when you say you are done.",
            "",
            "It is also Effective Java, Item 2 — one honest technique,",
            "described from two directions.",
        ],
        narration=(
            "The fix has a name, and this time it really is a Gang of Four "
            "pattern. Separate the construction of a complex object from its "
            "representation, so the same construction process can create "
            "different representations. [[slnc 300]] "
            "In plain words? You decide the object a piece at a time, in "
            "whatever order suits you, and it only gets checked for "
            "completeness the moment you say you're done. [[slnc 300]] "
            "And it's also item two in Effective Java. Same technique, "
            "described from two angles — one as a design pattern for building "
            "complex objects, the other as the fix for the telescoping "
            "constructor we just saw. Both books are talking about the same "
            "code."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="A Made-to-Order Sandwich Counter",
        body=[
            "You do not shout the whole order through the hatch at once.",
            "",
            "•  bread, then fillings, one at a time, in any order",
            "•  extras are optional — you only mention the ones you want",
            "•  they don't start making it until you say \"that's everything\"",
            "•  say it with no fillings at all, and they can refuse",
            "",
            "You build it up. They check it's complete when you're done.",
        ],
        narration=(
            "Think about ordering at a made-to-order sandwich counter. You "
            "don't shout the entire order through the hatch in one go. "
            "[[slnc 300]] "
            "You say the bread. Then a filling. Then another. Then maybe some "
            "extras, and you only mention the ones you actually want — nobody "
            "says 'no pickles, no mustard, no onions' for every topping that "
            "isn't there. And crucially, they don't start making the sandwich "
            "until you say 'that's everything'. [[slnc 300]] "
            "If you say that with no fillings at all, they can quite "
            "reasonably say no. That's the whole shape of a builder. You "
            "build it up, a piece at a time, and completeness only gets "
            "checked at the very end."
        ),
    ),
    dict(
        key="08-shape",
        kind="diagram",
        title="The Shape of It",
        body=None,
        narration=(
            "So here's the shape of it. There's exactly one door in: "
            "PurchaseOrder dot builder, taking the two facts every order "
            "truly needs. That hands back a Builder. [[slnc 300]] "
            "Every chainable method on that Builder returns the very same "
            "Builder, so the calls read as one flowing statement. And only "
            "the final build call does two things at once: it checks the "
            "order is actually complete, and it constructs the immutable "
            "PurchaseOrder. [[slnc 300]] "
            "PurchaseOrder's own constructor is private. The Builder is the "
            "only path in, from anywhere outside this class."
        ),
    ),
    dict(
        key="09-required",
        kind="code",
        title="Required Facts, Optional Pieces",
        body="""public static Builder builder(String orderId, String customerId) {
    return new Builder(orderId, customerId);
}

public static final class Builder {
    private final String orderId;
    private final String customerId;
    private final List<LineItem> items = new ArrayList<>();
    private Address shippingAddress;
    // ...five more optional fields, no constructor arguments at all
}""",
        narration=(
            "Here's the code. The two facts that are always required — order "
            "id, and customer id — are the only two arguments the Builder's "
            "constructor takes, and that constructor is private, reached only "
            "through the static builder method. [[slnc 300]] "
            "Every optional piece, by contrast, starts at a sensible default "
            "and has no constructor argument at all. There's nothing to skip "
            "past, because there was never a positional slot for it in the "
            "first place."
        ),
    ),
    dict(
        key="10-chain",
        kind="code",
        title="One Method, One Piece",
        body="""public Builder addItem(LineItem item) {
    items.add(Objects.requireNonNull(item, "item"));
    return this;
}

public Builder priority() {
    this.priority = true;
    return this;
}

// PurchaseOrder.builder("ORD-9001", "CUST-100")
//         .addItem(mug).addItem(book)
//         .shippingAddress(home)
//         .priority()""",
        narration=(
            "Every method follows the same shape: set one piece, then return "
            "this. Returning the same builder is what lets the next call "
            "chain straight off the end of it, with no temporary variable "
            "anywhere. [[slnc 300]] "
            "And look at that call underneath. Compare it to the "
            "nine-parameter constructor from scene three. You don't have to "
            "ask which argument is which any more — every piece announces "
            "itself by name, in whatever order you happened to write it."
        ),
    ),
    dict(
        key="11-rule",
        kind="code",
        title="A Rule That Lives in One Place",
        body="""public Builder giftMessage(String message) {
    this.giftMessage = Objects.requireNonNull(message, "giftMessage");
    this.giftWrapped = true;   // a message implies wrapping
    return this;
}""",
        narration=(
            "Here's the part a plain bag of setters could never give you. "
            "Setting a gift message also sets gift wrapped to true, because a "
            "gift message on a box that isn't wrapped makes no sense in this "
            "domain. [[slnc 300]] "
            "And that rule lives in exactly one place. Not repeated at every "
            "call site, not left to a comment saying 'remember to also wrap "
            "it' — it's enforced, once, inside the one method that can enforce "
            "it."
        ),
    ),
    dict(
        key="12-build",
        kind="code",
        title="Checked Only When You Say You're Done",
        body="""public PurchaseOrder build() {
    if (items.isEmpty()) {
        throw new IllegalStateException("a purchase order needs at least one item");
    }
    if (shippingAddress == null) {
        throw new IllegalStateException("a purchase order needs a shipping address");
    }
    return new PurchaseOrder(this);
}""",
        narration=(
            "And this is the moment completeness gets checked. Not "
            "addItem, not shippingAddress — build. [[slnc 300]] "
            "Why can't an earlier method check this instead? Because "
            "addItem has no way of knowing whether you're about to call "
            "shippingAddress next, or whether you're finished. Only build "
            "marks the moment you've declared yourself done, so it's the only "
            "method that can honestly ask 'is this actually complete?'"
        ),
    ),
    dict(
        key="13-immutable",
        kind="code",
        title="The Product Stops Watching the Builder",
        body="""private PurchaseOrder(Builder builder) {
    this.items = List.copyOf(builder.items);
    this.orderId = builder.orderId;
    // ...
}

PurchaseOrder first = builder.addItem(mug).build();
PurchaseOrder second = builder.addItem(book).build();

// first items: 1, second items: 2""",
        narration=(
            "One more detail, easy to miss and important. The constructor "
            "takes List dot copyOf of the builder's items — a snapshot, not "
            "the same list. [[slnc 300]] "
            "So keep the same builder around, add another item, and build a "
            "second order from it. The first order you built does not "
            "silently gain the new item. It already took its own copy. The "
            "product stops watching the builder the instant build returns."
        ),
    ),
    dict(
        key="14-director",
        kind="code",
        title="The Director, the Java Way",
        body="""public static PurchaseOrder expressOrder(String orderId, String customerId,
        List<LineItem> items, Address address) {
    PurchaseOrder.Builder builder = PurchaseOrder.builder(orderId, customerId)
            .shippingAddress(address)
            .priority()
            .notes("Ship same-day if received before 2pm.");
    items.forEach(builder::addItem);
    return builder.build();
}

// touches only Builder's public methods — never PurchaseOrder's fields""",
        narration=(
            "The Gang of Four book gives builder a fourth role, a Director, "
            "usually its own interface and class, whose whole job is to know "
            "fixed recipes for common configurations. [[slnc 300]] "
            "In idiomatic Java, that's usually just a static method, and "
            "that's exactly what PurchaseOrderPresets is here. Look closely: "
            "expressOrder never touches a PurchaseOrder field, or the "
            "constructor. It only ever calls Builder's public methods. Which "
            "means PurchaseOrder can change its private representation "
            "tomorrow, and not one preset has to change with it."
        ),
    ),
    dict(
        key="15-run",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

Hand-built: PurchaseOrder{orderId=ORD-9001, items=2, giftWrapped=true, ...}

gift order      -> giftWrapped=true message=Happy birthday!
standard order  -> giftWrapped=false priority=false
express order   -> priority=true notes=Ship same-day if received before 2pm.

first items: 1, second items: 2

Rejected: a purchase order needs at least one item
Rejected: a purchase order needs a shipping address""",
        narration=(
            "Let's run it, and see the whole story on one screen. "
            "[[slnc 250]] "
            "One order built by hand, with a gift message and a coupon "
            "chained straight on. Three presets, each reading exactly like "
            "what it configures. The reused-builder proof, one order with one "
            "item, the next with two, neither reaching into the other. "
            "[[slnc 300]] "
            "And at the bottom, two orders rejected on purpose — one with no "
            "items, one with no address — both caught as IllegalStateException "
            "before a single PurchaseOrder object was ever created."
        ),
    ),
    dict(
        key="16-limits",
        kind="bullets",
        title="Where It Stops",
        body=[
            "✗  A second object exists — briefly — for every one you build",
            "✗  More typing for a type with nothing to decide",
            "✗  Required fields still need somewhere to live — the constructor",
            "",
            "✓  Don't bother when there is nothing to decide.",
            "    LineItem and Address here are plain records, on purpose.",
        ],
        narration=(
            "Now the honest part. Every pattern has a ceiling. "
            "[[slnc 300]] "
            "A builder is a second object. Briefly, for every PurchaseOrder "
            "you build, a Builder exists too. For an order placed a few times "
            "a second, that's nothing. For something constructed millions of "
            "times in a hot loop, it's a real allocation to weigh. "
            "[[slnc 250]] "
            "It's also more typing, for a type that has nothing to decide. "
            "And the required fields don't disappear — the Builder's own "
            "constructor still takes them positionally, it's just a much "
            "shorter list. [[slnc 300]] "
            "Which is exactly why LineItem and Address in this project are "
            "plain records, with ordinary public constructors. Two or three "
            "required fields, no options, no rules between them — a builder "
            "there would be ceremony around a non-problem."
        ),
    ),
    dict(
        key="17-family",
        kind="bullets",
        title="How It Relates to the Others",
        body=[
            "Static Factory     give me one that…             no factory class",
            "Simple Factory     which one?                    a helper with a switch",
            "Abstract Factory   which whole set?               one choice, many objects",
            "Builder            which pieces, in what order?  one object, assembled gradually",
            "",
            "Builder and static factory are not rivals — they compose.",
            "PurchaseOrder.builder(...) is itself a static factory method.",
        ],
        narration=(
            "So where does builder sit next to the other creational patterns? "
            "[[slnc 250]] "
            "Static factory answers 'give me one that does this', with no "
            "factory class at all. Simple factory moves 'which one?' into a "
            "helper with a switch. Abstract factory answers 'which whole "
            "matching set?', one choice producing several related objects. "
            "And builder answers a different question entirely: not which "
            "object, but which pieces, assembled in what order, for one "
            "object. [[slnc 300]] "
            "And here's the nice part. They're not rivals. PurchaseOrder dot "
            "builder is itself a static factory method — it just happens to "
            "return something whose whole job is collecting more information "
            "before it builds anything."
        ),
    ),
    dict(
        key="18-wrap",
        kind="title",
        title="One Sentence to Keep",
        body=[
            "A constructor makes you decide the whole object",
            "in one call. A builder lets you decide it a piece",
            "at a time, and checks it is complete only when",
            "you say you are done.",
        ],
        narration=(
            "If you keep one sentence from all of this, keep this one. "
            "[[slnc 300]] "
            "A constructor makes you decide the whole object in one call. A "
            "builder lets you decide it a piece at a time, and checks it is "
            "complete only when you say you are done. [[slnc 350]] "
            "There's a full set of notes in the project, an animated "
            "walkthrough you can step through at your own pace, and a "
            "session plan if you fancy teaching this to somebody else. Go add "
            "an option of your own to PurchaseOrder. That's the best way to "
            "make it stick."
        ),
    ),
    dict(
        key="19-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "If this helped, a thumbs up and a subscribe go a long way",
            "towards keeping more videos like it coming.",
            "",
            "Full source code, notes and diagrams are in the repository.",
        ],
        narration=(
            "And that's the builder pattern. [[slnc 300]] "
            "If you got something out of this, do give it a thumbs up, and "
            "subscribe. It genuinely helps the channel, and it's what makes "
            "more of these possible. [[slnc 250]] "
            "And if there's a pattern you'd like me to cover next, drop it in "
            "the comments. I read every one. [[slnc 250]] "
            "All the source code, the written notes and the diagrams are in "
            "the repository. Thanks for watching, and I'll see you in the "
            "next one."
        ),
    ),
]
