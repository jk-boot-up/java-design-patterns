#!/usr/bin/env python3
"""The script for the Static Factory Method video.

One entry per scene. `narration` is spoken aloud and also becomes the
subtitles, so it is written the way someone would say it — currency and
symbols spelled out in words, because the synthesiser reads them poorly.

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
            "Hello, and welcome. This video is written and presented by "
            "Jayasekhar Konduru. "
            "Today we are learning the static factory method, using a small "
            "e-commerce checkout written in Java 21. "
            "It is the simplest way to create objects well, and if you have ever "
            "written List dot of, you have already used it. "
            "By the end of this video you will know exactly what it buys you, "
            "and exactly where it stops."
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
            "Here is the job. An online shop prices one order, and applies a "
            "discount to it. "
            "The shop needs several kinds of discount. Ten percent off. Five "
            "pounds off. Free shipping. Nothing at all. And one that quietly "
            "picks whichever of two others is worth more to the customer. "
            "The checkout should not care which kind it was handed. It should "
            "just apply it."
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
            "So you start with constructors. Ten percent off is one number. "
            "Five pounds off is one number. Two constructors, each taking one "
            "double. "
            "And it does not compile. Java says the constructor is already "
            "defined. "
            "Look at why. A constructor's name is fixed, it is the name of the "
            "class, so the only thing that can tell two of them apart is the "
            "list of parameter types. Both of these take a double. To the "
            "compiler, they are the same constructor written twice. "
            "The meaning, percent versus pounds, exists only in your head. "
            "There is nowhere in the code to put it."
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
            "The usual escape is to widen the constructor until every kind fits "
            "through it. One constructor, three parameters, and a convention "
            "that you zero out the ones you are not using. "
            "Now read those four call sites. Which one gives five pounds off? "
            "You can work it out, but you have to count commas to do it. "
            "And the last one, all zeros, is a discount that does nothing. "
            "Nothing in that line says so."
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
            "That costs you five separate things. "
            "The call site no longer says what it means. "
            "Nothing stops somebody passing a percentage and an amount and free "
            "shipping all at once, which is nonsense the compiler will happily "
            "accept. "
            "Every kind of discount carries fields belonging to the other kinds. "
            "Adding a new kind means changing the constructor, and therefore "
            "every single caller. "
            "And the word new always allocates, so even a discount of nothing "
            "creates a fresh object every time you ask for one. "
            "Notice what is not wrong here. The type is fine. It is the way in "
            "that is the problem."
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
            "The fix has a name. A static factory method is simply a static "
            "method that returns an instance of its own class, used in place of "
            "a public constructor. It is the very first item in the book "
            "Effective Java. "
            "In plain words, you give the constructor a name. "
            "One honest warning before we go on. This is not a Gang of Four "
            "pattern, and despite the word factory, it is not the same thing as "
            "the Factory Method pattern. The two share a word and nothing else. "
            "Do not let anyone tell you otherwise in an interview."
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
            "Think of a vending machine. You press a labelled button. You do not "
            "open the front and reach inside. "
            "The button has a name, so you always know what you asked for. "
            "The machine decides which shelf and which slot to take it from, and "
            "that is entirely its business, not yours. "
            "It might hand you one it already had sitting ready. "
            "And if you press a button that means nothing, it does not have to "
            "manufacture anything at all. "
            "That is the whole idea. You ask for an outcome, not for a "
            "manufacturing step."
        ),
    ),
    dict(
        key="08-shape",
        kind="diagram",
        title="The Shape of It",
        body=None,
        narration=(
            "Here is the shape of the solution. "
            "Your code sits at the top. It calls a named method on the Discount "
            "interface itself. The type is its own factory. There is no separate "
            "factory class anywhere in this project. "
            "Below the line are the five classes that actually do the work. Not "
            "one of them is public, so no code outside the package can even "
            "write their names. "
            "Which means all five could be renamed, merged, or deleted tomorrow, "
            "and not a single caller would break. Callers never knew they "
            "existed."
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
            "And here is the code. Since Java 8, an interface can hold static "
            "methods, so the six ways in live on Discount itself. "
            "Read the names. None. Percentage. Amount off. Free shipping. Best "
            "of. For coupon. "
            "Percentage and amount off would have been impossible as "
            "constructors, because one takes a number and so does the other. As "
            "named methods, they sit side by side and nobody could confuse them. "
            "That is the first freedom, and on its own it would already be worth "
            "doing."
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
            "Now the freedom a constructor can never have. "
            "A discount of nothing has no state. There is no reason for two of "
            "them to exist, ever. So the class keeps one shared instance, hides "
            "its constructor, and the none method hands that same object back "
            "every single time. "
            "The word new is defined as making something new. It has no option "
            "to say, actually, here is one I already had. A named method does. "
            "This is exactly why Integer dot value of exists, and why calling new "
            "Integer is deprecated."
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
            "The third freedom is the deepest one. A static factory method is "
            "not obliged to return the class you might expect. "
            "Ask for a percentage discount of zero, and you do not get a "
            "percentage discount holding a zero. You get the shared do nothing "
            "one instead. "
            "Nobody outside can tell, and nobody outside can complain, because "
            "the return type was only ever Discount. You asked for an outcome, "
            "so the method was free to serve it however it liked. "
            "Notice the validation too. It runs before anything is built. A "
            "constructor can throw, but only after you have already committed to "
            "the word new."
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
            "And this is the payoff. The whole checkout. "
            "Search it for the word new applied to a discount, and there is none. "
            "Search it for a branch on the kind of discount, and there is none. "
            "Search it for any of those five class names, and it does not contain "
            "one of them. "
            "It takes a Discount, asks it what it is worth, and subtracts. Every "
            "decision was made inside a factory method, long before this line ran."
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
            "The same technique works just as well on a small value type. "
            "Money dot pounds of five, and Money dot pence of five, are two "
            "completely different amounts. As constructors they could never have "
            "coexisted, because both take a number. As named methods they read "
            "themselves aloud, and nobody has to guess the unit. "
            "There is a parse method too, for text coming in from the outside "
            "world. And money zero returns a single shared instance, for the same "
            "reason the no discount one does."
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
            "You are not learning something new here. You are learning the name "
            "of something you already do. "
            "List of. Integer value of. Optional empty. Local date now. String "
            "value of. Every one of those is a static factory method. "
            "And here is the detail worth keeping. List dot of returns a "
            "different class depending on how many elements you pass. There are "
            "specialised implementations for zero, one and two. You have never "
            "noticed, and it has never once caused you a problem. That is the "
            "third freedom, working quietly, in code you use daily. "
            "The names on the bottom line are the conventions the whole ecosystem "
            "follows. Of, from, value of, get instance, new instance, parse, and "
            "copy of. Use them, and your code will read like the standard library."
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
            "Running it puts all of that on one screen. "
            "Each coupon code from the storefront goes through the for coupon "
            "method, which returns whichever implementation fits. The best deal "
            "code builds a composite holding two other discounts, a class the "
            "caller could not possibly have assembled itself, because it cannot "
            "name any of the three. "
            "Then the proof at the bottom. Two methods that could never have been "
            "two constructors. A none that is genuinely shared. A percentage of "
            "zero quietly turning into the do nothing discount. And an unknown "
            "coupon rejected before any object was created."
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
            "Now the honest part, because every technique has a ceiling. "
            "Hiding the constructor means nobody outside can subclass your "
            "implementations. For value types that is usually a feature. "
            "Occasionally it is a genuine problem for somebody. "
            "Static factories are also harder to discover. There is no new to "
            "search for, just a method sitting among all the others. "
            "And the big one. A static method is resolved at compile time. It "
            "cannot be overridden, so a subclass cannot change what gets built, "
            "and neither can a configuration file. When you need that, you have "
            "outgrown this technique. "
            "One more thing. Do not apply this everywhere. Order and Receipt in "
            "this project are plain records with ordinary public constructors, "
            "because they have nothing to decide. That contrast is deliberate."
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
            "Which leads neatly to the rest of the family. "
            "The static factory asks, give me one that does this. There is no "
            "factory class at all. "
            "The simple factory asks, which one? and moves that question out into "
            "a helper class with a switch. "
            "Factory method asks, which one, and lets a subclass answer, moving "
            "the decision into the type system. "
            "And the abstract factory asks, which whole matching set? One choice "
            "producing many related objects. "
            "Each of those exists because the one above it has a ceiling. Start "
            "here, and move up only when something actually forces you to."
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
            "If you keep one sentence from this video, keep this one. "
            "A constructor cannot be named, and cannot refuse to allocate. A "
            "static factory method can do both. "
            "Everything else follows from those two sentences. "
            "The project has a full set of notes, an animated walkthrough you can "
            "step through at your own pace, and a session plan if you want to "
            "teach it to somebody else. Go and add a discount of your own."
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
            "That is the static factory method. "
            "If you found this useful, please do give the video a thumbs up and "
            "subscribe to the channel. It genuinely helps the channel grow, and "
            "it is what makes more content like this possible. "
            "If there is a pattern you would like covered next, leave it in the "
            "comments and I will read every one. "
            "The full source code, the written notes and the diagrams are all in "
            "the repository. Thank you for watching, and I will see you in the "
            "next one."
        ),
    ),
]
