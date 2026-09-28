"""Scene definitions for the Decorator pattern teaching video.

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
        title="The Decorator Pattern",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Decorator pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Decorator pattern adds '
            'behaviour to an object by wrapping it in another object with '
            'the same shape. [[slnc 300]] Each wrapper does its own small '
            'job, and then passes the call along. [[slnc 300]] So '
            'features can be combined while the program runs, in any '
            'order, without a class for every combination. [[slnc 600]] '
            'Think of dressing for the weather, one layer at a time. '
            '[[slnc 700]] In our online store, checkout pricing has '
            'optional extras, like gift wrapping and insurance. [[slnc '
            '500]] By the end, you will know how to make any combination '
            'of optional features work together, with one small class per '
            'feature.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "Checkout pricing for a product with optional extras:",
            "",
            "  gift wrapping, shipment insurance, express handling",
            "",
            "Any combination should be selectable, in any order:",
            "",
            "  gift wrap alone, insurance alone, all three together, or none",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] A product has a base '
            'price. [[slnc 300]] But customers can add optional extras. '
            '[[slnc 300]] Gift wrapping, shipping insurance, and express '
            'handling. [[slnc 500]] Any combination should be possible. '
            '[[slnc 300]] Gift wrap alone, insurance alone, all three '
            'together, or none.'
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="One Class Per Combination",
        body=[
            "Two features need up to three classes:",
            "  gift-wrapped, insured, gift-wrapped-and-insured",
            "",
            "Add a third feature — express handling — and covering every",
            "combination needs four more classes.",
        ],
        narration=(
            'The obvious first move is a class for each combination. '
            '[[slnc 500]] Two optional features already need three '
            'classes. [[slnc 300]] One for gift wrap, one for insurance, '
            'and one for both. [[slnc 500]] Add a third feature, express '
            'handling, and you need four more classes to cover every '
            'combination.'
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — One Class Per Combination",
        body="""public final class NaiveGiftWrappedInsuredProduct {
    private static final BigDecimal GIFT_WRAP_FEE = new BigDecimal("3.50");
    private static final BigDecimal RATE = new BigDecimal("0.02");

    public BigDecimal cost() {
        BigDecimal wrapped = price.add(GIFT_WRAP_FEE);
        BigDecimal premium = wrapped.multiply(RATE).setScale(2, HALF_UP);
        return wrapped.add(premium);
    }
}

//  Both fee calculations are already duplicated from the single-feature classes.""",
        narration=(
            'Here is the naive approach. [[slnc 400]] One class handles a '
            'gift-wrapped, insured product. [[slnc 300]] It adds a fixed '
            'gift-wrap fee. [[slnc 300]] Then it works out an insurance '
            'charge on top. [[slnc 600]] And here is the problem. [[slnc '
            '300]] The gift-wrap fee, and the insurance calculation, are '
            'both copied from the single-feature classes. [[slnc 300]] '
            'Copied and pasted, not shared.'
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   The number of classes grows combinatorially",
            "✗   Every fee calculation is duplicated across classes",
            "✗   A pricing bug fix means hunting down every copy",
            "✗   Nothing here is a bug — the waste is structural",
        ],
        narration=(
            'That does real damage as the system grows. [[slnc 500]] The '
            'number of classes explodes. [[slnc 300]] Four optional '
            'features would need fifteen classes, just to cover every '
            'mix. [[slnc 300]] And every fee calculation is copied into '
            'every class that needs it. [[slnc 500]] Fix a pricing bug, '
            'like changing the insurance rate, and you must find every '
            'copy. [[slnc 600]] None of this is a bug. [[slnc 300]] Each '
            'naive class gives the correct price. [[slnc 300]] The waste '
            'is in the structure.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Decorator Pattern",
        body=[
            "“Attach additional responsibilities to an object dynamically.”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "wrap it, don't subclass it.",
        ],
        narration=(
            'The Decorator pattern fixes exactly this. [[slnc 400]] The '
            'classic book on design patterns, by the authors known as the '
            'Gang of Four, describes it like this. [[slnc 300]] Attach '
            'extra responsibilities to an object while the program runs. '
            '[[slnc 300]] A flexible alternative to creating subclasses. '
            '[[slnc 600]] In plain words: wrap it, do not subclass it.'
        ),
    ),
    dict(
        key="07-layers",
        kind="bullets",
        title="Remember It With Dressing for Weather",
        body=[
            "A shirt can have a sweater put on over it, and a raincoat",
            "put on over the sweater.",
            "",
            "Each layer adds its own effect, without the shirt needing to",
            "know a raincoat exists, or the raincoat knowing what's underneath.",
            "",
            "Wear any subset of layers, in any order, with no distinct",
            "garment for every combination.",
        ],
        narration=(
            'Here is how to remember it. [[slnc 300]] Think about '
            'dressing for the weather. [[slnc 500]] Put a jumper over '
            'your shirt. [[slnc 300]] Then a raincoat over the jumper. '
            '[[slnc 300]] Each layer adds its own effect: first warmth, '
            'then keeping dry. [[slnc 500]] The shirt does not need to '
            'know the raincoat exists. [[slnc 300]] And the raincoat does '
            'not care what is underneath. [[slnc 600]] You can wear any '
            'mix of layers, in any order. [[slnc 300]] Without owning a '
            'separate garment for every combination.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            'Every decorator has four roles. [[slnc 500]] The component: '
            'the shared interface that plain and decorated products both '
            'follow. [[slnc 300]] Here, it is called priced item. [[slnc '
            '400]] The concrete component: a plain product, with no '
            'extras. [[slnc 400]] The abstract decorator: it follows the '
            'same interface, and holds another priced item inside it. '
            '[[slnc 400]] And the concrete decorators: gift wrap, '
            'insurance, and express handling. [[slnc 300]] Each adds '
            'exactly one charge. [[slnc 600]] Here is the most important '
            'idea in this video. [[slnc 300]] Every decorator has exactly '
            'the same shape as the thing it wraps. [[slnc 300]] So '
            'decorators can be nested as deep as you like. [[slnc 300]] '
            'And the caller never needs to know how many layers there '
            'are.'
        ),
    ),
    dict(
        key="09-component",
        kind="code",
        title="The Component — The Shared Shape",
        body="""public interface PricedItem {
    BigDecimal cost();
    String description();
}

public final class Product implements PricedItem {
    // plain item, no extras -- name and price only
    @Override public BigDecimal cost() { return price; }
    @Override public String description() { return name; }
}""",
        narration=(
            'Here is the component, the priced item interface. [[slnc '
            '400]] It is shared by plain products and decorated ones. '
            '[[slnc 300]] It has just two questions: what is your cost, '
            'and what is your description? [[slnc 600]] And here is the '
            'concrete component: a plain product. [[slnc 300]] A name and '
            'a price, with no extras at all.'
        ),
    ),
    dict(
        key="10-decorator",
        kind="code",
        title="A Concrete Decorator — Delegate, Then Add",
        body="""public abstract class ProductDecorator implements PricedItem {
    protected final PricedItem wrapped;
}

public final class InsuranceDecorator extends ProductDecorator {
    private static final BigDecimal RATE = new BigDecimal("0.02");

    @Override
    public BigDecimal cost() {
        BigDecimal base = wrapped.cost();
        BigDecimal premium = base.multiply(RATE).setScale(2, HALF_UP);
        return base.add(premium);
    }
}""",
        narration=(
            'Here is one concrete decorator: insurance. [[slnc 400]] It '
            'holds a wrapped priced item inside it. [[slnc 600]] When '
            'asked for its cost, it first asks the wrapped item for its '
            'cost. [[slnc 300]] Then it adds a two percent insurance '
            'charge on top. [[slnc 500]] It has no idea whether the '
            'wrapped item is a plain product, or another decorator.'
        ),
    ),
    dict(
        key="11-stacking",
        kind="code",
        title="Stacking Order Changes the Result",
        body="""PricedItem giftWrappedThenInsured =
        new InsuranceDecorator(new GiftWrapDecorator(product));
PricedItem insuredThenGiftWrapped =
        new GiftWrapDecorator(new InsuranceDecorator(product));

giftWrappedThenInsured.cost();   // $85.16 -- insures the gift-wrap fee too
insuredThenGiftWrapped.cost();   // $85.09 -- gift wrap is flat, added after""",
        narration=(
            'Here is a detail worth pausing on. [[slnc 400]] Insurance '
            'charges a percentage of whatever it wraps. [[slnc 300]] So '
            'the order of wrapping changes the total. [[slnc 600]] Gift '
            'wrap first, then insure: eighty-five dollars sixteen. [[slnc '
            '300]] Because the insurance also covers the gift-wrap fee. '
            '[[slnc 500]] Insure first, then gift wrap: eighty-five '
            'dollars nine. [[slnc 300]] Because the fixed fee is added '
            'after the insurance is worked out. [[slnc 600]] Both are '
            'fair prices, for two different policies. [[slnc 300]] The '
            'Decorator pattern makes that choice clear and visible. '
            '[[slnc 300]] Instead of burying it inside one combination '
            'class.'
        ),
    ),
    dict(
        key="12-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

== Stacking decorators, one feature at a time ==
Wireless Headphones: $79.99
Wireless Headphones, gift-wrapped: $83.49
Wireless Headphones, gift-wrapped, insured: $85.16
Wireless Headphones, gift-wrapped, insured, express handling: $95.15

== Stacking order changes the result -- insurance prices whatever it wraps ==
Wireless Headphones, insured, gift-wrapped: $85.09

== The naive alternative, for comparison ==
Wireless Headphones, gift-wrapped, insured: $85.16""",
        narration=(
            "Let's run the project. [[slnc 400]] Wireless headphones cost "
            'seventy-nine dollars ninety-nine. [[slnc 300]] With gift '
            'wrap, eighty-three forty-nine. [[slnc 300]] Then insured, '
            'eighty-five sixteen. [[slnc 300]] Then with express '
            'handling, ninety-five fifteen. [[slnc 600]] Swap the '
            'gift-wrap and insurance order, and the total becomes '
            'eighty-five dollars nine. [[slnc 300]] Exactly the '
            'difference we just described. [[slnc 600]] And the naive '
            'combination class gives the same number as the matching '
            'stack of decorators. [[slnc 300]] It is not wrong. [[slnc '
            '300]] It is just one more class than the pattern needs.'
        ),
    ),
    dict(
        key="13-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use decorator when optional, combinable behavior would",
            "otherwise mean one class per combination.",
            "",
            "Keep every decorator's interface identical to the component --",
            "no new methods, or callers can no longer treat it as one.",
            "",
            "Remember one sentence:",
            "Decorator keeps the same interface so wrapped and unwrapped",
            "objects stay interchangeable. Adapter deliberately changes it.",
        ],
        narration=(
            'So, to recap. [[slnc 400]] Use a decorator when optional, '
            'combinable features would otherwise need a class for every '
            "combination. [[slnc 600]] Keep every decorator's shape "
            'identical to the thing it wraps. [[slnc 300]] The moment a '
            'decorator adds a new method, callers can no longer treat it '
            'like the plain item. [[slnc 600]] And one comparison worth '
            'knowing. [[slnc 300]] A decorator keeps the same shape, so '
            'wrapped and unwrapped items can be swapped. [[slnc 300]] The '
            'Adapter pattern deliberately changes the shape, to fit two '
            'things that disagree.'
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
            "That's the Decorator pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Wrap an object '
            'in layers with the same shape, one feature per layer, '
            'instead of writing a class for every combination. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 300]] '
            'It runs offline, with nothing installed except a Java '
            'development kit. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Add a fourth extra, like a gift message. [[slnc '
            '300]] And notice you only need one new class. [[slnc 500]] '
            'If this helped, a like really does help other people find '
            "it. [[slnc 300]] And subscribe, if you'd like the rest of "
            'the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
