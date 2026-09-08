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
            "Hello, and welcome. This video explains the Decorator pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. [[slnc "
            "300]] Let's start with the simple definition. The decorator pattern "
            "adds behaviour to an object by wrapping it in another object with "
            "the same interface. Each wrapper does its own small piece of work "
            "and then passes the call along, so features can be combined at "
            "runtime, in any order, without writing a class for every "
            "combination. [[slnc 350]] That's the idea in a sentence. The rest of "
            "the video does it properly, by building a real working Java project: "
            "checkout pricing in an online store, with stackable extras like gift "
            "wrapping and insurance. [[slnc 250]] By the end you'll know how to "
            "make any combination of optional features work together, in any "
            "order, with one small class per feature."
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
            "So, imagine checkout pricing for an online store. [[slnc 250]] A "
            "product has a base price, but customers can add optional extras: "
            "gift wrapping, shipment insurance, and express handling. [[slnc "
            "300]] And any combination of these should be selectable — gift "
            "wrap alone, insurance alone, all three together, or none at all."
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
            "The obvious first move is a class for each combination you need "
            "today. [[slnc 250]] Two optional features already need up to "
            "three classes — one for gift wrap, one for insurance, one for "
            "both together. [[slnc 300]] Add a third feature, express "
            "handling, and covering every combination needs four more classes "
            "on top of that."
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
            "So here's the naive approach. [[slnc 250]] "
            "NaiveGiftWrappedInsuredProduct adds a flat gift-wrap fee, then "
            "computes an insurance premium on top of that. [[slnc 300]] And "
            "here's the problem. Both the gift-wrap fee and the insurance "
            "premium calculation are already duplicated from the "
            "single-feature classes elsewhere in the codebase — copy-pasted, "
            "not shared."
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
            "And that does real damage as the system grows. [[slnc 250]] The "
            "number of classes grows combinatorially — four optional features "
            "would need fifteen classes just to cover every subset. Every fee "
            "calculation is copy-pasted into every class that needs that "
            "feature. [[slnc 300]] Fix a pricing bug, like changing the "
            "insurance rate, and you have to hunt down every copy "
            "individually. [[slnc 250]] None of this is a bug — each naive "
            "class computes a correct price. The waste is structural: "
            "combinable behavior modeled as a fixed set of subclasses."
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
            "The decorator pattern fixes exactly this. [[slnc 250]] In Gang "
            "of Four terms, decorator attaches additional responsibilities to "
            "an object dynamically, providing a flexible alternative to "
            "subclassing for extending functionality. [[slnc 300]] In plain "
            "language? Wrap it, don't subclass it."
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
            "Here's how to remember it forever. Think about dressing for "
            "weather. [[slnc 250]] A base shirt can have a sweater put on "
            "over it, and a raincoat put on over the sweater. Each layer adds "
            "its own effect — warmth, then water resistance. [[slnc 300]] The "
            "shirt never needs to know a raincoat exists, and the raincoat "
            "never needs to know what's underneath it. [[slnc 250]] You can "
            "wear any subset of layers, in any order, without owning a "
            "distinct garment for every combination."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            "Every decorator setup has four roles. [[slnc 200]] The "
            "component, PricedItem, the interface both plain and decorated "
            "products share. The concrete component, Product, a plain item "
            "with no extras. The abstract decorator, ProductDecorator, which "
            "implements the component and holds another component by "
            "composition. And the concrete decorators — GiftWrapDecorator, "
            "InsuranceDecorator, ExpressHandlingDecorator — each adding "
            "exactly one fee. [[slnc 350]] Here's the single most important "
            "idea in this whole video. Every decorator exposes exactly the "
            "same interface as the thing it wraps, so decorators nest "
            "arbitrarily deep, and the client never has to know how many "
            "layers it's calling into."
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
            "This is the component, PricedItem. [[slnc 250]] It's the shared "
            "interface both plain products and decorated products implement "
            "— just cost, and description. [[slnc 300]] And this is the "
            "concrete component, Product. A plain item with a name and a "
            "price, no extras, no decorators involved at all."
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
            "And this is a concrete decorator, InsuranceDecorator. [[slnc "
            "250]] It extends ProductDecorator, which holds a wrapped "
            "PricedItem by composition. [[slnc 300]] cost calls "
            "wrapped-dot-cost first, then adds a two percent premium on top "
            "of whatever comes back. It has no idea whether wrapped is a "
            "plain Product or another decorator underneath it."
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
            "Here's the subtlety worth pausing on. [[slnc 250]] Because "
            "InsuranceDecorator prices a percentage of whatever it wraps, "
            "wrapping order changes the total. [[slnc 300]] Gift-wrap then "
            "insure comes to eighty five dollars and sixteen cents, because "
            "the premium includes the gift-wrap fee. Insure then gift-wrap "
            "comes to eighty five dollars and nine cents, because the flat "
            "fee is added after insurance is already computed. [[slnc 250]] "
            "Both are legitimate prices for different policies — decorator "
            "makes that an explicit, visible choice, not a decision buried "
            "in one combination class."
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
            "When we run the project, each decorator stacks cleanly on top "
            "of the last, one feature at a time, up to ninety five dollars "
            "and fifteen cents with all three extras. [[slnc 250]] Reverse "
            "the gift-wrap and insurance order and the total shifts to "
            "eighty five dollars and nine cents — exactly the difference we "
            "just walked through. [[slnc 300]] And down at the bottom, the "
            "naive combination class produces the exact same number as the "
            "matching decorator stack — it isn't wrong, it's just one more "
            "class than the pattern ever needed."
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
            "So, to recap. Use decorator when optional, combinable behavior "
            "would otherwise mean one class per combination. [[slnc 300]] "
            "Keep every decorator's interface identical to the component it "
            "wraps — the moment a decorator adds a new method, callers can no "
            "longer treat it interchangeably with the plain component. "
            "[[slnc 350]] And if you remember one sentence from today, make "
            "it this one. Decorator keeps the same interface in and out so "
            "wrapped and unwrapped objects stay interchangeable. Adapter "
            "deliberately changes the interface to reconcile two shapes that "
            "disagree."
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
            "And that's the decorator pattern. [[slnc 300]] If you got "
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
