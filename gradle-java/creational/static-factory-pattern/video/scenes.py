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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Static Factory Method pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A static factory '
            'method is a static method that returns an object of its own '
            'type. [[slnc 300]] It is used instead of a public '
            'constructor. [[slnc 400]] Because it has a name, it can say '
            'what it makes. [[slnc 300]] And because it is a method, it '
            'can hand back a shared object, or a different class, instead '
            'of always building something new. [[slnc 600]] If you have '
            'ever written List dot of, you have already used one. [[slnc '
            '700]] In this video, we build the discounts for an online '
            "shop's checkout. [[slnc 500]] By the end, you will know "
            'exactly what this technique gives you, and exactly where it '
            'stops.'
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
            'Here is the job. [[slnc 400]] An online shop prices an '
            'order, and applies a discount to it. [[slnc 500]] The shop '
            'needs several kinds of discount. [[slnc 300]] Ten percent '
            'off. [[slnc 200]] Five pounds off. [[slnc 200]] Free '
            'shipping. [[slnc 200]] No discount at all. [[slnc 200]] And '
            'one clever one, which picks whichever of two others saves '
            'the customer more. [[slnc 500]] The checkout should not care '
            'which one it is given. [[slnc 300]] It should just apply it, '
            'and move on.'
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
            'So you start where everyone starts: constructors. [[slnc '
            '400]] Ten percent off is one number. [[slnc 300]] Five '
            'pounds off is also one number. [[slnc 300]] So you write two '
            'constructors, each taking one decimal number. [[slnc 500]] '
            'And it does not compile. [[slnc 300]] Java says the '
            'constructor is already defined. [[slnc 500]] Why? [[slnc '
            "300]] A constructor's name is fixed. [[slnc 300]] It is "
            'always the name of the class. [[slnc 300]] So the only way '
            'to tell two constructors apart is by their parameter types. '
            '[[slnc 300]] And both take one decimal number. [[slnc 500]] '
            'The difference, percent versus pounds, only exists in your '
            'head. [[slnc 300]] There is nowhere in the code to put it.'
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
            'So what does everyone do instead? [[slnc 400]] They widen '
            'the constructor until every kind of discount fits. [[slnc '
            '300]] One constructor, with three parameters: a percentage, '
            'an amount off, and a free shipping flag. [[slnc 300]] And an '
            'unwritten rule: set the ones you are not using to zero. '
            '[[slnc 500]] Now imagine reading four calls to it, each with '
            'three values. [[slnc 300]] Which one gives five pounds off? '
            '[[slnc 300]] You can work it out, but only by counting '
            'commas. [[slnc 500]] And a call with all zeros? [[slnc 300]] '
            'That is a discount that does nothing. [[slnc 300]] But '
            'nothing in that line says so.'
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
            'And that costs you in five ways. [[slnc 500]] One. [[slnc '
            '200]] The call no longer says what it means. [[slnc 300]] '
            'Two. [[slnc 200]] Nothing stops someone passing a '
            'percentage, an amount, and free shipping, all at once. '
            '[[slnc 300]] That is nonsense, and the compiler accepts it. '
            '[[slnc 300]] Three. [[slnc 200]] Every discount carries '
            'fields that belong to the other kinds. [[slnc 300]] Four. '
            '[[slnc 200]] A new kind of discount means changing the '
            'constructor, and every caller with it. [[slnc 300]] Five. '
            '[[slnc 200]] The new keyword always creates a new object. '
            '[[slnc 300]] Even a discount of nothing is built fresh, '
            'every single time. [[slnc 500]] Notice that the discount '
            'type itself is fine. [[slnc 300]] The problem is the way in.'
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
            'The fix has a name. [[slnc 400]] A static factory method is '
            'a static method that returns an object of its own type, used '
            'instead of a public constructor. [[slnc 300]] It is item '
            'one, the very first item, in the book Effective Java. [[slnc '
            '500]] In plain words: give the constructor a name. [[slnc '
            '300]] That is the whole idea. [[slnc 600]] One warning. '
            '[[slnc 300]] This is not a Gang of Four pattern. [[slnc '
            '300]] And despite the word factory, it is not the Factory '
            'Method pattern. [[slnc 300]] They share a word, and nothing '
            'else.'
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
            'Think about a vending machine. [[slnc 400]] You press a '
            'button with a label on it. [[slnc 300]] You do not open the '
            'front and reach inside. [[slnc 500]] The button has a name, '
            'so you always know what you asked for. [[slnc 300]] The '
            'machine decides which shelf and which slot. [[slnc 300]] '
            'That is its business, not yours. [[slnc 300]] It might hand '
            'you one it already had waiting. [[slnc 300]] And if a button '
            'means nothing, it does not have to make anything at all. '
            '[[slnc 500]] That is the whole idea. [[slnc 300]] You ask '
            'for an outcome, not a manufacturing step.'
        ),
    ),
    dict(
        key="08-shape",
        kind="diagram",
        title="The Shape of It",
        body=None,
        narration=(
            'So here is the shape of it. [[slnc 400]] Your code calls a '
            'named method on the Discount interface itself. [[slnc 300]] '
            'The type is its own factory. [[slnc 300]] There is no '
            'separate factory class anywhere in this project. [[slnc '
            '500]] Behind the interface are five classes that do the real '
            'work. [[slnc 300]] And none of them is public. [[slnc 300]] '
            'So no code outside the package can even name them. [[slnc '
            '500]] That means all five could be renamed, merged, or '
            'deleted tomorrow. [[slnc 300]] And not a single caller would '
            'break.'
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
            'Here is the code. [[slnc 400]] Since Java eight, an '
            'interface can hold static methods. [[slnc 300]] So all six '
            'ways in live on the Discount interface itself. [[slnc 500]] '
            'Just listen to the names. [[slnc 300]] None. [[slnc 200]] '
            'Percentage. [[slnc 200]] Amount off. [[slnc 200]] Free '
            'shipping. [[slnc 200]] Best of. [[slnc 200]] And for coupon. '
            '[[slnc 300]] You know what each one does without reading '
            'inside it. [[slnc 500]] And percentage and amount off could '
            'never have been two constructors. [[slnc 300]] Both take one '
            'number. [[slnc 300]] As named methods, they sit side by '
            'side, and nobody confuses them. [[slnc 500]] That is the '
            'first freedom: a name.'
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
            'Now the second freedom, which a constructor can never have: '
            'not creating anything. [[slnc 500]] A discount of nothing '
            'holds no data. [[slnc 300]] There is no reason for two of '
            'them to exist. [[slnc 300]] So the class keeps one shared '
            'instance, and hides its constructor. [[slnc 300]] The none '
            'method hands back that same object, every single time. '
            '[[slnc 500]] The new keyword always means, make a new one. '
            '[[slnc 300]] It cannot say, here is one I already had. '
            '[[slnc 300]] A named method can. [[slnc 500]] That is '
            'exactly why Integer dot value of exists. [[slnc 300]] And '
            'why calling new Integer is deprecated.'
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
            'The third freedom is the deepest one: choosing the class. '
            '[[slnc 400]] A static factory method does not have to return '
            'the class you expect. [[slnc 500]] Ask for a percentage '
            'discount of zero. [[slnc 300]] You do not get a percentage '
            'discount holding a zero. [[slnc 300]] You get the shared '
            'do-nothing discount instead. [[slnc 500]] Nobody outside can '
            'tell, and nobody can complain. [[slnc 300]] Because the '
            'return type was only ever Discount. [[slnc 500]] Notice the '
            'input check, too. [[slnc 300]] A percentage below zero, or '
            'above one hundred, is refused, before anything is built.'
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
            'And here is the payoff: the whole checkout. [[slnc 500]] '
            'Search it for the new keyword applied to a discount. [[slnc '
            '300]] There is none. [[slnc 300]] Search it for a branch on '
            'the kind of discount. [[slnc 300]] There is none. [[slnc '
            '300]] Search it for any of the five discount class names. '
            '[[slnc 300]] Not one of them appears. [[slnc 500]] It takes '
            'a Discount, asks what it is worth, and subtracts it. [[slnc '
            '300]] That is all. [[slnc 300]] Every decision was made '
            'inside a factory method, long before.'
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
            'The same trick works beautifully on a small value type: '
            'money. [[slnc 500]] Money dot pounds of five, and Money dot '
            'pence of five. [[slnc 300]] Two completely different '
            'amounts. [[slnc 300]] As constructors, they could never '
            'exist side by side, because both take one number. [[slnc '
            '300]] As named methods, they say exactly what they mean. '
            '[[slnc 500]] There is also a parse method, for text coming '
            'from outside. [[slnc 300]] And money zero hands back one '
            'shared instance, for the same reason as the do-nothing '
            'discount.'
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
            'You are not really learning something new. [[slnc 300]] You '
            'are learning the name of something you already use. [[slnc '
            '500]] List dot of. [[slnc 200]] Integer dot value of. [[slnc '
            '200]] Optional dot empty. [[slnc 200]] Local Date dot now. '
            '[[slnc 300]] Every one of those is a static factory method. '
            '[[slnc 500]] And here is something worth remembering. [[slnc '
            '300]] List dot of returns a different class, depending on '
            'how many items you pass it. [[slnc 300]] You have never '
            'noticed, and it has never caused a problem. [[slnc 300]] '
            'That is the third freedom, quietly at work. [[slnc 500]] The '
            'usual names are of, from, value of, get instance, new '
            'instance, parse, and copy of. [[slnc 300]] Use those, and '
            "your code reads like Java's own library."
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
            "Let's run the demo. [[slnc 500]] Every coupon code from the "
            'shop goes through the for coupon method. [[slnc 300]] It '
            'returns whichever discount fits. [[slnc 500]] The code save '
            'ten gives ten percent off, which saves twelve pounds on a '
            'one hundred and twenty pound order. [[slnc 300]] The code '
            'best deal builds a combined discount, holding two others, '
            'and picks the bigger saving. [[slnc 300]] The caller could '
            'never have built that itself, because it cannot name any of '
            'the classes. [[slnc 500]] Then the proofs. [[slnc 300]] '
            'Percentage and amount off, which could never have been '
            'constructors. [[slnc 300]] A none discount that really is '
            'shared. [[slnc 300]] A zero percent discount, quietly '
            'becoming the do-nothing discount. [[slnc 300]] And an '
            'unknown coupon, refused before any object was created.'
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
            'Now the honest part. [[slnc 300]] This technique has limits. '
            '[[slnc 500]] Hiding the constructor means nobody outside can '
            'extend your classes. [[slnc 300]] For value types, that is '
            'usually a good thing. [[slnc 300]] But sometimes, it is a '
            'real problem for someone. [[slnc 500]] Static factory '
            'methods are also harder to find. [[slnc 300]] There is no '
            'new keyword to search for. [[slnc 500]] And the big one. '
            '[[slnc 300]] A static method is fixed when the code '
            'compiles. [[slnc 300]] A subclass cannot change what gets '
            'built, and neither can a configuration file. [[slnc 300]] '
            'The day you need that, you have outgrown this technique. '
            '[[slnc 600]] And do not use it everywhere. [[slnc 300]] In '
            'this project, the order and the receipt are plain records, '
            'with ordinary constructors. [[slnc 300]] They have nothing '
            'to decide.'
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
            'Which brings us to the rest of the factory family. [[slnc '
            '500]] A static factory says: give me one that does this, '
            'with no factory class at all. [[slnc 300]] A simple factory '
            'asks: which one? [[slnc 300]] And answers with a switch, in '
            'a helper class. [[slnc 300]] A factory method asks which '
            'one, and lets a subclass answer. [[slnc 300]] And an '
            'abstract factory asks: which whole matching set? [[slnc '
            '300]] One choice, many related objects. [[slnc 500]] Each '
            'one exists because the one before it reaches a limit. [[slnc '
            '300]] So start with the static factory. [[slnc 300]] And '
            'move up only when something really forces you to.'
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
            'If you keep one sentence from this video, keep this one. '
            '[[slnc 400]] A constructor cannot be named, and cannot '
            'refuse to create a new object. [[slnc 300]] A static factory '
            'method can do both. [[slnc 500]] Everything else in this '
            'video follows from those two facts. [[slnc 500]] The project '
            'has full notes, an animated walkthrough, and a teaching '
            'plan. [[slnc 300]] Try adding a discount of your own. [[slnc '
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
            "That's the Static Factory Method. [[slnc 400]] The full "
            'source code, written notes, and diagrams are all in the '
            'repository. [[slnc 500]] If there is a pattern you would '
            'like to see covered, suggest it in the comments. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
