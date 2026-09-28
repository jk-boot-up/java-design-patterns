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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Builder pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Builder pattern creates '
            'an object one piece at a time. [[slnc 300]] Instead of a '
            'constructor with a long list of arguments, you call a named '
            'method for each part you want. [[slnc 300]] In any order. '
            '[[slnc 300]] Then one final method checks everything, and '
            'hands back the finished object. [[slnc 600]] Think of '
            'ordering at a sandwich counter. [[slnc 300]] You name the '
            'bread, then each filling, one at a time. [[slnc 300]] And '
            "they only make it when you say, that's everything. [[slnc "
            '700]] In this video, we build a purchase order for an online '
            'store. [[slnc 500]] By the end, you will know why two famous '
            'books both recommend this pattern. [[slnc 300]] And how it '
            'works together with a static factory method.'
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
            'Here is the job: building a purchase order. [[slnc 500]] Two '
            'things are always required. [[slnc 300]] An order I D and a '
            'customer I D. [[slnc 300]] And at least one item, with a '
            'shipping address. [[slnc 500]] On top of that, there are '
            'five independent, optional extras. [[slnc 300]] Gift '
            'wrapping. [[slnc 200]] A gift message. [[slnc 200]] A coupon '
            'code. [[slnc 200]] Priority shipping. [[slnc 200]] And a '
            'free-text note. [[slnc 500]] Any order might have none of '
            'those, or all of them, in any combination.'
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
            'So you write the constructor everyone starts with. [[slnc '
            '300]] Nine parameters, one for every fact this order might '
            'need. [[slnc 500]] Now imagine reading a call to it. [[slnc '
            '300]] Nine values in a row, separated by commas. [[slnc '
            '300]] Is this a priority order, or a gift order? [[slnc '
            '300]] You have to count commas, and check against the '
            'parameter list, to know. [[slnc 500]] And there are two '
            'true-or-false values in there. [[slnc 300]] Swap them by '
            'accident, and the compiler says nothing at all.'
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
            'The next idea is to add shorter constructors, for the common '
            'cases. [[slnc 400]] But then a gift order without priority '
            'needs one version. [[slnc 300]] A gift order with a coupon '
            'needs another. [[slnc 300]] Every new combination needs a '
            'brand new constructor. [[slnc 300]] Or you fall back to the '
            'nine-parameter one anyway. [[slnc 500]] The book Effective '
            'Java has a name for this: the telescoping constructor. '
            '[[slnc 300]] And it is named as a warning, not as something '
            'to copy.'
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
            'And that costs you in five ways. [[slnc 500]] One. [[slnc '
            '200]] The calling code no longer says what it means. [[slnc '
            '300]] Two. [[slnc 200]] Most calls are full of nulls, and '
            'false values, because most orders use few options. [[slnc '
            '300]] Three. [[slnc 200]] The order of the parameters is '
            'arbitrary, and nothing enforces it. [[slnc 300]] Four. '
            '[[slnc 200]] Every new option widens the constructor, and '
            'touches every caller. [[slnc 300]] Five. [[slnc 200]] There '
            'is nowhere to put a rule like, a gift message means the '
            'order must be gift wrapped. [[slnc 300]] A constructor just '
            'stores values. [[slnc 500]] Notice that the purchase order '
            'itself is fine. [[slnc 300]] The problem is the way in.'
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
            'The fix is a pattern from the famous Gang of Four book. '
            '[[slnc 400]] Separate the construction of a complex object '
            'from its representation, so the same process can create '
            'different results. [[slnc 500]] In plain words: build the '
            'object one piece at a time, in any order. [[slnc 300]] And '
            'check it is complete only when you say you are done. [[slnc '
            '500]] It is also item two in the book Effective Java. [[slnc '
            '300]] Both books describe the same code, from two angles.'
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
            'Here is an analogy: a made-to-order sandwich counter. [[slnc '
            '500]] You do not shout your whole order through the hatch at '
            'once. [[slnc 300]] You name the bread. [[slnc 300]] Then a '
            'filling. [[slnc 200]] Then another. [[slnc 300]] Then any '
            'extras you want. [[slnc 300]] You never list all the '
            'toppings you do not want. [[slnc 500]] And they do not start '
            "making it until you say, that's everything. [[slnc 400]] If "
            'you say that with no fillings at all, they can refuse. '
            '[[slnc 500]] That is exactly the shape of a builder. [[slnc '
            '300]] Build it up piece by piece, and check it only at the '
            'end.'
        ),
    ),
    dict(
        key="08-shape",
        kind="diagram",
        title="The Shape of It",
        body=None,
        narration=(
            'So here is the shape of it. [[slnc 400]] There is exactly '
            'one way in. [[slnc 300]] A static method called builder, on '
            'the purchase order class, which takes the two required I Ds. '
            '[[slnc 300]] It hands back a Builder object. [[slnc 500]] '
            'Every method on the Builder returns that same Builder. '
            '[[slnc 300]] So the calls can be chained, one after another, '
            'in a single statement. [[slnc 500]] Only the final build '
            'method does two things. [[slnc 300]] It checks the order is '
            'complete. [[slnc 300]] And it creates the finished, '
            'unchangeable purchase order. [[slnc 500]] The purchase '
            "order's own constructor is private. [[slnc 300]] The Builder "
            'is the only way to create one.'
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
            'Here is how the code handles required and optional parts. '
            '[[slnc 500]] The two facts that are always required, the '
            "order I D and the customer I D, are the Builder's only "
            'constructor arguments. [[slnc 300]] And you reach that '
            'constructor through the static builder method. [[slnc 500]] '
            'Every optional piece starts with a sensible default. [[slnc '
            '300]] It has no constructor argument at all. [[slnc 300]] So '
            'there is nothing to skip past, because there was never a '
            'position for it.'
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
            'Every Builder method follows the same shape. [[slnc 300]] '
            'Set one piece, then return the Builder itself. [[slnc 500]] '
            'Returning the same Builder is what lets the next call chain '
            'straight on. [[slnc 500]] So creating an order reads like a '
            'sentence. [[slnc 300]] Builder, add a mug, add a book, set '
            'the shipping address, mark it priority, and build. [[slnc '
            '500]] Compare that with the nine-parameter constructor. '
            '[[slnc 300]] Now every piece announces itself by name, in '
            'whatever order you wrote it.'
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
            'Here is something a plain set of setters could never give '
            'you. [[slnc 500]] Setting a gift message also marks the '
            'order as gift wrapped. [[slnc 300]] Because a gift message '
            'on an unwrapped box makes no sense. [[slnc 500]] And that '
            'rule lives in exactly one place. [[slnc 300]] Not repeated '
            'at every call. [[slnc 300]] Not left to a comment that says, '
            'remember to wrap it. [[slnc 300]] It is enforced once, '
            'inside the one method that can enforce it.'
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
            'And this is the moment the order is checked for '
            'completeness. [[slnc 300]] Not when an item is added, and '
            'not when the address is set. [[slnc 300]] Only in build. '
            '[[slnc 500]] If there are no items, build refuses, saying a '
            'purchase order needs at least one item. [[slnc 300]] If '
            'there is no address, it refuses, saying a purchase order '
            "needs a shipping address. [[slnc 500]] Why can't an earlier "
            'method check this? [[slnc 300]] Because adding an item '
            'cannot know whether you are about to add more, or whether '
            'you are finished. [[slnc 300]] Only build marks the moment '
            'you say you are done.'
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
            'One more detail, easy to miss, and important. [[slnc 400]] '
            'When build creates the order, it takes a copy of the '
            "Builder's list of items. [[slnc 300]] A snapshot, not the "
            'same list. [[slnc 500]] So imagine keeping the same Builder, '
            'adding another item, and building a second order. [[slnc '
            '300]] The first order has one item. [[slnc 300]] The second '
            'has two. [[slnc 300]] The first order did not silently gain '
            'the new item. [[slnc 500]] Once build returns, the order no '
            'longer depends on the Builder at all.'
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
            'The Gang of Four book describes one more role, called the '
            'Director. [[slnc 300]] Its job is to know fixed recipes for '
            'common orders. [[slnc 500]] In everyday Java, a director is '
            'usually just a static method. [[slnc 300]] Here, a class '
            'called Purchase Order Presets has a method called express '
            'order. [[slnc 300]] It sets the address, marks it priority, '
            'adds a same-day shipping note, and adds the items. [[slnc '
            "500]] Notice that the preset only ever uses the Builder's "
            "public methods. [[slnc 300]] So the purchase order's private "
            'details can change tomorrow, and not one preset needs to '
            'change.'
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
            "Let's run the demo. [[slnc 500]] First, one order built by "
            'hand, with a gift message and a coupon. [[slnc 300]] It is '
            'gift wrapped automatically, because it has a message. [[slnc '
            '500]] Then three presets: a gift order, a standard order, '
            'and an express order. [[slnc 300]] Each one does exactly '
            'what its name says. [[slnc 500]] Then the reused Builder. '
            '[[slnc 300]] The first order has one item, and the second '
            'has two. [[slnc 300]] Neither affects the other. [[slnc '
            '500]] And finally, two orders are rejected on purpose. '
            '[[slnc 300]] One with no items, and one with no address. '
            '[[slnc 300]] Both are caught before any purchase order is '
            'ever created.'
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
            'Now the honest part. [[slnc 300]] Every pattern has limits. '
            '[[slnc 500]] First, a builder is an extra object. [[slnc '
            '300]] For every order you build, a Builder exists briefly '
            'too. [[slnc 300]] For an order placed a few times a second, '
            'that costs nothing. [[slnc 300]] For something created '
            'millions of times in a tight loop, it is worth thinking '
            'about. [[slnc 500]] Second, it is more code to write, for a '
            'type with few choices to make. [[slnc 500]] That is why this '
            "project's line items and addresses are plain records, with "
            'ordinary constructors. [[slnc 300]] Two or three required '
            'values, and no options. [[slnc 300]] A builder there would '
            'be ceremony for no reason.'
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
            'So how does the Builder relate to the other creational '
            'patterns? [[slnc 500]] A static factory method answers: give '
            'me one that does this. [[slnc 300]] A simple factory '
            'answers: which one? using a helper with a switch. [[slnc '
            '300]] An abstract factory answers: which whole matching set? '
            '[[slnc 300]] And a builder answers a different question. '
            '[[slnc 300]] Not which object, but which pieces, for one '
            'object, built up gradually. [[slnc 500]] And they are not '
            'rivals. [[slnc 300]] The builder method on the purchase '
            'order is itself a static factory method. [[slnc 300]] It '
            'just returns something that collects more information, '
            'before building anything.'
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
            'If you keep one sentence from this video, keep this one. '
            '[[slnc 400]] A constructor makes you decide the whole object '
            'in one call. [[slnc 300]] A builder lets you decide it one '
            'piece at a time, and checks it is complete only when you say '
            'you are done. [[slnc 600]] The project has full notes, an '
            'animated walkthrough, and a teaching plan. [[slnc 300]] Try '
            'adding an option of your own to the purchase order. [[slnc '
            '300]] That is the best way to make it stick.'
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
            "That's the Builder pattern. [[slnc 400]] The full source "
            'code, written notes, and diagrams are all in the repository. '
            '[[slnc 500]] If there is a pattern you would like to see '
            'covered, suggest it in the comments. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
