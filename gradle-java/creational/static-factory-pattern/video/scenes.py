#!/usr/bin/env python3
"""The script for the Static Factory Method video.

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
        title="Static Factory Method",
        body=None,
        narration=(
            "Hello, and welcome. This one is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] "
            "Today we're doing the static factory method. It's the simplest way "
            "to create objects well, and honestly, if you've ever written List "
            "dot of, you've already used it. You just didn't know it had a name. "
            "[[slnc 250]] "
            "We'll build it out in a small e-commerce checkout, in Java 21. And "
            "by the end, you'll know exactly what it buys you, and exactly where "
            "it runs out of road."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Job",
        body=[
            "An online shop. One order, and a discount to apply to it.",
            "",
            "The shop needs several kinds of discount:",
            "",
            "•  ten percent off",
            "•  five pounds off",
            "•  free shipping",
            "•  nothing at all",
            "•  whichever of two is worth more",
            "",
            "The checkout should not care which one it was given.",
        ],
        narration=(
            "So here's the job. We've got an online shop. It prices an order, and "
            "it applies a discount to it. [[slnc 250]] "
            "And the shop needs a few different kinds. Ten percent off. Five "
            "pounds off. Free shipping. Nothing at all. And one more that's a bit "
            "clever, it picks whichever of two others saves the customer more. "
            "[[slnc 250]] "
            "Now the checkout, it shouldn't care which one it got handed. It "
            "should just apply the thing and move on."
        ),
    ),
    dict(
        key="03-wall",
        kind="code",
        title="The First Attempt Does Not Compile",
        body="""public class Discount {

    public Discount(double percent) { ... }

    public Discount(double amountOff) { ... }
}

error: constructor Discount(double) is already defined""",
        narration=(
            "Okay, so you start where everyone starts. Constructors. Ten percent "
            "off, that's one number. Five pounds off, also one number. So, two "
            "constructors, each taking a double. [[slnc 300]] "
            "And it doesn't compile. Java tells you the constructor is already "
            "defined. [[slnc 250]] "
            "Now, why? A constructor's name is fixed. It's the name of the class, "
            "you don't get to pick it. So the only thing that can tell two "
            "constructors apart is the list of parameter types. And both of these "
            "take a double. To the compiler, these are the same constructor, "
            "written out twice. [[slnc 250]] "
            "The difference, percent versus pounds, that only exists in your head. "
            "There's literally nowhere in the code to put it."
        ),
    ),
    dict(
        key="04-workaround",
        kind="code",
        title="So Everyone Writes This Instead",
        body="""public Discount(double percent, double amountOff, boolean freeShipping) { ... }

// and then, at the call sites:

Discount tenPercent = new Discount(0.10, 0, false);
Discount fiverOff   = new Discount(0, 5.00, false);
Discount shipping   = new Discount(0, 0, true);
Discount nothing    = new Discount(0, 0, false);""",
        narration=(
            "So what does everybody do instead? You widen the constructor until "
            "every kind fits through it. One constructor, three parameters, and an "
            "unwritten rule that you zero out whatever you're not using. "
            "[[slnc 300]] "
            "Now look at those four call sites, and tell me which one gives five "
            "pounds off. You can work it out. But you're counting commas to do it. "
            "[[slnc 250]] "
            "And that last one, all zeros? That's a discount that does nothing. "
            "Nothing in that line tells you so."
        ),
    ),
    dict(
        key="05-harm",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗  The call site does not say what it means",
            "✗  Nothing stops new Discount(0.10, 5.00, true)",
            "✗  Every kind of discount pays for every field",
            "✗  A new kind means changing the constructor, and every caller",
            "✗  new always allocates — even for the discount that does nothing",
            "",
            "The type is fine. The way in is the problem.",
        ],
        narration=(
            "And that costs you. Five separate ways. [[slnc 300]] "
            "One. The call site doesn't say what it means any more. "
            "Two. Nothing stops somebody passing a percentage, and an amount, and "
            "free shipping, all at once. Which is nonsense, and the compiler will "
            "take it quite happily. "
            "Three. Every kind of discount is carrying fields that belong to the "
            "other kinds. "
            "Four. Adding a new kind means changing the constructor, so every "
            "caller changes with it. "
            "And five. The word new always allocates. So even a discount of "
            "nothing makes you a brand new object, every single time you ask for "
            "one. [[slnc 350]] "
            "But notice what isn't wrong here. The type is fine. It's the way in "
            "that's the problem."
        ),
    ),
    dict(
        key="06-definition",
        kind="quote",
        title="The Static Factory Method",
        body=[
            "A static method that returns an instance of its own class,",
            "used in place of a public constructor.",
            "",
            "— Effective Java, Item 1",
            "",
            "In plain words: give the constructor a name.",
            "",
            "It is not a Gang of Four pattern, and it is not the same",
            "thing as Factory Method. The shared word is a coincidence.",
        ],
        narration=(
            "Right, so the fix has a name. A static factory method is just a "
            "static method that returns an instance of its own class, and you use "
            "it instead of a public constructor. It's item one in Effective Java, "
            "the very first thing in the book. [[slnc 300]] "
            "In plain words? You give the constructor a name. That's it. That's "
            "the whole idea. [[slnc 350]] "
            "One warning before we carry on, and this one matters. This is not a "
            "Gang of Four pattern. And despite the word factory being in there, "
            "it is not the same thing as the Factory Method pattern. They share a "
            "word. That's all they share. Don't let anybody tell you different in "
            "an interview."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="A Vending Machine",
        body=[
            "You press a labelled button. You do not reach inside.",
            "",
            "•  the button has a name  —  so you know what you asked for",
            "•  the machine chooses  —  which shelf, which slot, is its business",
            "•  it may hand you a spare it already had",
            "•  press 'nothing' and it need not make anything at all",
            "",
            "You asked for an outcome. Not for a manufacturing step.",
        ],
        narration=(
            "Think about a vending machine. You press a button with a label on "
            "it. You don't open up the front and reach inside. [[slnc 300]] "
            "The button has a name, so you always know what you asked for. The "
            "machine works out which shelf and which slot, and honestly, that's "
            "its business, not yours. It might hand you one it already had "
            "sitting there. And if you press a button that means nothing, well, "
            "it doesn't have to manufacture anything at all. [[slnc 300]] "
            "And that's the whole idea, really. You're asking for an outcome. "
            "You're not asking for a manufacturing step."
        ),
    ),
    dict(
        key="08-shape",
        kind="diagram",
        title="The Shape of It",
        body=None,
        narration=(
            "So here's the shape of it. Your code sits up at the top, and it "
            "calls a named method on the Discount interface itself. The type is "
            "its own factory. There's no separate factory class anywhere in this "
            "project. None. [[slnc 300]] "
            "Below the line are the five classes doing the actual work. And not "
            "one of them is public. So no code outside the package can even write "
            "their names down. [[slnc 300]] "
            "Which means, and this is the good bit, all five of them could be "
            "renamed tomorrow. Or merged. Or deleted. And not a single caller "
            "would break. They never knew they were there."
        ),
    ),
    dict(
        key="09-interface",
        kind="code",
        title="The Type Is Its Own Factory",
        body="""public interface Discount {

    Money appliedTo(Order order);
    String describe();

    static Discount none()                  { return NoDiscount.INSTANCE; }

    static Discount percentage(int percent) { ... }

    static Discount amountOff(Money amount) { ... }

    static Discount freeShipping()          { return FreeShippingDiscount.INSTANCE; }

    static Discount bestOf(Discount a, Discount b) { ... }

    static Discount forCoupon(String code)  { ... }
}""",
        narration=(
            "And here's the code. Since Java 8, an interface can hold static "
            "methods, so all six ways in live on Discount itself. [[slnc 250]] "
            "Just read the names. None. Percentage. Amount off. Free shipping. "
            "Best of. For coupon. You know what every one of those does without "
            "reading a single line inside them. [[slnc 300]] "
            "And percentage and amount off? Those two could never have been "
            "constructors. One takes a number, and so does the other. As named "
            "methods, they sit right next to each other, and nobody is ever going "
            "to confuse them. [[slnc 250]] "
            "That's the first freedom. And honestly, on its own, it'd already be "
            "worth doing."
        ),
    ),
    dict(
        key="10-not-allocate",
        kind="code",
        title="Freedom Two: Not to Allocate",
        body="""final class NoDiscount implements Discount {

    static final NoDiscount INSTANCE = new NoDiscount();

    private NoDiscount() { }

    public Money appliedTo(Order order) { return Money.zero(); }
}

// Discount.none() is shared: true""",
        narration=(
            "Now, the freedom a constructor can never have. [[slnc 250]] "
            "A discount of nothing has no state. There's no reason for two of "
            "them to exist. Ever. So the class keeps one shared instance, hides "
            "its constructor away, and the none method hands you back that same "
            "object every single time. [[slnc 300]] "
            "And think about what new actually means. It's defined as making "
            "something new. It has no way of saying, actually, here's one I "
            "already had. A named method does. [[slnc 300]] "
            "This is exactly why Integer dot value of exists. And exactly why "
            "calling new Integer is deprecated."
        ),
    ),
    dict(
        key="11-choose-class",
        kind="code",
        title="Freedom Three: to Choose the Class",
        body="""static Discount percentage(int percent) {
    if (percent < 0 || percent > 100) {
        throw new IllegalArgumentException("percentage must be 0-100");
    }
    return percent == 0 ? none() : new PercentageDiscount(percent);
}

// percentage(0) -> No discount""",
        narration=(
            "The third freedom, this is the deep one. A static factory method "
            "doesn't have to return the class you'd expect. [[slnc 300]] "
            "Ask for a percentage discount of zero. You don't get a percentage "
            "discount holding a zero. You get the shared do nothing one instead. "
            "[[slnc 300]] "
            "And nobody outside can tell. Nobody outside can complain either, "
            "because the return type was only ever Discount. You asked for an "
            "outcome, so the method is free to serve it however it likes. "
            "[[slnc 250]] "
            "Have a look at the validation as well. It runs before anything gets "
            "built. A constructor can throw too, sure, but only after you've "
            "already committed to the word new."
        ),
    ),
    dict(
        key="12-client",
        kind="code",
        title="What the Client Looks Like",
        body="""public Receipt checkout(Order order, Discount discount) {

    Money off   = discount.appliedTo(order);
    Money total = order.subtotal().plus(order.shipping()).minus(off);

    return new Receipt(order.orderId(), order.subtotal(), order.shipping(),
            discount.describe(), off, total);
}""",
        narration=(
            "And this. This is the payoff. The whole checkout. [[slnc 300]] "
            "Go looking for the word new applied to a discount. There isn't one. "
            "Look for a branch on the kind of discount. There isn't one. Look for "
            "any of those five class names. Not one of them is in here. "
            "[[slnc 300]] "
            "It takes a Discount, asks it what it's worth, and subtracts it. "
            "That's all it does. Every decision got made inside a factory method, "
            "long before this line ever ran."
        ),
    ),
    dict(
        key="13-money",
        kind="code",
        title="The Same Trick on a Value Type",
        body="""Money.pounds(5)   ->  £5.00
Money.pence(5)    ->  £0.05

Money.parse("£5.00")

// two named doors to the same type
// no pair of constructors could have been these""",
        narration=(
            "The same trick works beautifully on a small value type. [[slnc 250]] "
            "Money dot pounds of five, and Money dot pence of five. Two completely "
            "different amounts of money. As constructors, they could never have "
            "lived side by side, because both of them take a number. As named "
            "methods, they read themselves out loud, and nobody has to guess the "
            "unit. [[slnc 300]] "
            "There's a parse method as well, for text coming in from the outside "
            "world. And money zero hands back one shared instance, for exactly "
            "the same reason the no discount one does."
        ),
    ),
    dict(
        key="14-jdk",
        kind="bullets",
        title="You Already Use This Every Day",
        body=[
            "List.of(\"a\", \"b\")          Integer.valueOf(5)",
            "Optional.empty()           LocalDate.now()",
            "String.valueOf(42)         Map.entry(k, v)",
            "",
            "List.of() returns a different class depending on the size.",
            "You have never noticed, and it has never mattered.",
            "",
            "of · from · valueOf · getInstance · newInstance · parse · copyOf",
        ],
        narration=(
            "Here's the thing, though. You're not learning something new. You're "
            "learning the name of something you already do. [[slnc 300]] "
            "List of. Integer value of. Optional empty. Local date now. String "
            "value of. Every single one of those is a static factory method. "
            "[[slnc 300]] "
            "And this next bit is worth hanging on to. List dot of gives you back "
            "a different class depending on how many elements you pass it. There "
            "are special implementations for zero, for one, and for two. You've "
            "never noticed. It's never once caused you a problem. That's the third "
            "freedom, working away quietly, in code you use every day. "
            "[[slnc 300]] "
            "And those names along the bottom, they're the conventions the whole "
            "ecosystem follows. Of. From. Value of. Get instance. New instance. "
            "Parse. Copy of. Use those, and your code reads like the standard "
            "library."
        ),
    ),
    dict(
        key="15-run",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

Coupon: SAVE10
Checkout: order ORD-4001 subtotal £120.00 + shipping £4.99
Checkout: 10% off saves £12.00
Checkout: total £112.99

Coupon: BESTDEAL
Checkout: best of (10% off, £5.00 off) saves £12.00

percentage(10) -> 10% off
amountOff(£10) -> £10.00 off
none() is shared: true
percentage(0) -> No discount
Rejected: unknown coupon code: SAVE99""",
        narration=(
            "Let's run it, and you can see the whole lot on one screen. "
            "[[slnc 250]] "
            "Every coupon code coming in from the storefront goes through the for "
            "coupon method, and that returns whichever implementation fits. That "
            "best deal code builds a composite, holding two other discounts, and "
            "that's a class the caller couldn't possibly have assembled itself, "
            "because it can't name any of the three. [[slnc 300]] "
            "Then look at the proof down at the bottom. Two methods that could "
            "never have been two constructors. A none that genuinely is shared. A "
            "percentage of zero, quietly turning into the do nothing discount. And "
            "an unknown coupon, turned away before a single object was created."
        ),
    ),
    dict(
        key="16-limits",
        kind="bullets",
        title="Where It Stops",
        body=[
            "✗  No public constructor means no subclassing from outside",
            "✗  Harder to find — no new to search for, just a method in a list",
            "✗  Resolved at compile time, so a subclass cannot change the answer",
            "✗  A config file cannot change it either",
            "",
            "✓  Don't bother when there is nothing to decide.",
            "    Order and Receipt here are plain records, on purpose.",
        ],
        narration=(
            "Right. Now the honest part, because everything has a ceiling. "
            "[[slnc 300]] "
            "Hiding the constructor means nobody outside can subclass your "
            "implementations. For value types, that's usually a feature rather "
            "than a bug. But every now and then, it's a real problem for somebody. "
            "[[slnc 250]] "
            "Static factories are also harder to find. There's no new to search "
            "for. It's just a method, sitting there among all the others. "
            "[[slnc 250]] "
            "And then the big one. A static method is resolved at compile time. It "
            "can't be overridden. So a subclass can't change what gets built, and "
            "neither can a config file. The day you need that, you've outgrown "
            "this technique. [[slnc 350]] "
            "Oh, and one more thing. Don't go applying this everywhere. Order and "
            "Receipt in this project are plain records, with ordinary public "
            "constructors, because they've got nothing to decide. That contrast is "
            "completely deliberate."
        ),
    ),
    dict(
        key="17-family",
        kind="bullets",
        title="The Rest of the Family",
        body=[
            "Static Factory     give me one that…             no factory class",
            "Simple Factory     which one?                    a helper with a switch",
            "Factory Method     which one — my subclass says   the type system decides",
            "Abstract Factory   which whole set?              one choice, many objects",
            "",
            "Each one exists because the one above it has a ceiling.",
        ],
        narration=(
            "Which brings us neatly on to the rest of the family. [[slnc 250]] "
            "The static factory says, give me one that does this. No factory class "
            "at all. "
            "The simple factory asks, which one? and moves that question out into "
            "a helper class with a switch in it. "
            "Factory method asks which one, and lets a subclass answer, so the "
            "decision moves into the type system. "
            "And the abstract factory asks, which whole matching set? One choice, "
            "and you get many related objects out of it. [[slnc 350]] "
            "Every one of those exists because the one before it hits a ceiling. "
            "So start here. And move up only when something genuinely forces you "
            "to."
        ),
    ),
    dict(
        key="18-wrap",
        kind="title",
        title="One Sentence to Keep",
        body=[
            "A constructor cannot be named,",
            "and cannot refuse to allocate.",
            "A static factory method can do both.",
        ],
        narration=(
            "If you keep one sentence from all of this, keep this one. "
            "[[slnc 300]] "
            "A constructor can't be named, and it can't refuse to allocate. A "
            "static factory method does both. [[slnc 350]] "
            "And everything else we've talked about follows from those two things. "
            "[[slnc 300]] "
            "There's a full set of notes in the project, an animated walkthrough "
            "you can step through at your own pace, and a session plan if you "
            "fancy teaching this to somebody else. Go and add a discount of your "
            "own. That's the best way to make it stick."
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
            "And that's the static factory method. [[slnc 300]] "
            "If you got something out of this, do give it a thumbs up, and "
            "subscribe. It genuinely helps the channel, and it's what makes more "
            "of these possible. [[slnc 250]] "
            "And if there's a pattern you'd like me to cover next, drop it in the "
            "comments. I read every one. [[slnc 250]] "
            "All the source code, the written notes and the diagrams are in the "
            "repository. Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
