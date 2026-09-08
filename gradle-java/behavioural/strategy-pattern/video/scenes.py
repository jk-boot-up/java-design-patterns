"""Scene definitions for the Strategy pattern teaching video.

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
        title="The Strategy Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Strategy pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. [[slnc "
            "300]] Let's start with the simple definition. The strategy pattern "
            "turns each branch of a decision into a class of its own, behind one "
            "shared interface. The code that needs the work done holds a strategy "
            "and calls it, without knowing or caring which one it is holding — so "
            "a new branch is a new class rather than a new case in a switch. "
            "[[slnc 350]] That's the idea in a sentence, and it is how you get "
            "rid of the big switch statement where every branch does a completely "
            "different calculation. The rest of the video does it properly, by "
            "building a real working Java project: delivery pricing at an online "
            "checkout, with four different shipping rules. [[slnc 250]] By the "
            "end you'll know how to add a fifth rule without editing a single "
            "line of code that already works."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online store has to quote a delivery charge at checkout.",
            "",
            "The rule it charges by is a business decision that changes:",
            "",
            "  flat rate          the same charge on everything",
            "  weight bands       under 1kg, under 5kg, under 20kg, over",
            "  distance           a base fee plus so much per 100 miles",
            "  free over £50      nothing to pay on a large enough order",
        ],
        narration=(
            "So, imagine delivery pricing for an online store. [[slnc 250]] At "
            "checkout, the shop has to quote a delivery charge — and the rule it "
            "charges by is a business decision that keeps changing. [[slnc 300]] "
            "A flat rate, the same on everything. Weight bands: under a kilo, "
            "under five, under twenty, and over that. Distance: a base fee plus "
            "so much per hundred miles. And a campaign rule — free delivery on "
            "orders over fifty pounds. [[slnc 250]] All four are live at some "
            "point. Marketing turns the free delivery campaign on for a fortnight "
            "and off again. None of them is the rule."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="The Obvious First Move",
        body=[
            "An enum for the method, and a switch inside checkout:",
            "",
            "  switch (method) {",
            "      case FLAT_RATE ...",
            "      case WEIGHT_BANDED ...",
            "      case DISTANCE_BASED ...",
            "      case FREE_OVER_THRESHOLD ...",
            "  }",
            "",
            "It works. Every price it produces is correct.",
        ],
        narration=(
            "The obvious first move is an enum for the shipping method and a "
            "switch inside the checkout code. One case per rule. [[slnc 300]] And "
            "I want to be fair to it: this works. Every price it produces is "
            "correct. This is what a competent developer writes first, and for "
            "two rules that never change it is the right answer. [[slnc 250]] So "
            "what we're about to look at isn't a bug report. It's a design "
            "complaint."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Four Rules, One Method",
        body="""public Quote quote(Shipment shipment) {
    switch (method) {
        case FLAT_RATE -> delivery = Money.pounds(4.99);
        case WEIGHT_BANDED -> {
            if (shipment.weightKg() <= 1) delivery = Money.pounds(3.50);
            else if (shipment.weightKg() <= 5) delivery = Money.pounds(6.00);
            else if (shipment.weightKg() <= 20) delivery = Money.pounds(12.00);
            else delivery = Money.pounds(25.00);
        }
        case DISTANCE_BASED -> { ... }
        case FREE_OVER_THRESHOLD -> { ... }
        default -> delivery = Money.zero();
    }
}

//  Look hard at that default. It charges nothing.""",
        narration=(
            "So here's the naive approach. [[slnc 250]] Four unrelated pricing "
            "policies, interleaved in one method. The weight bands, the "
            "per-hundred-miles rounding, the campaign threshold — none of them "
            "have anything to do with each other, and you can't read any one of "
            "them without scrolling past the other three. [[slnc 350]] But look "
            "hard at that default branch at the bottom. It's there because the "
            "compiler demands the method return something, and it does the only "
            "safe-looking thing. It charges nothing. [[slnc 300]] Add a fifth "
            "constant to that enum — locker collection, say — forget this method "
            "exists, and the shop starts shipping for free. No compile error. No "
            "exception. Just a quietly wrong number on the receipt."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   Four unrelated policies share one method",
            "✗   A fifth rule means editing code that already works",
            "✗   Testing one rule means going through checkout",
            "✗   The default branch silently ships for free",
            "✗   Rules cannot be supplied from outside",
        ],
        narration=(
            "And that does real damage as the system grows. [[slnc 250]] Four "
            "unrelated policies share one method. Adding a fifth rule means "
            "opening the one method that four working rules already depend on. "
            "[[slnc 300]] There's no way to ask what the weight-banded rule "
            "charges for six and a half kilos without constructing a whole "
            "shipment and going through checkout — so the arithmetic isn't "
            "separately testable. The default branch quietly ships for free. "
            "[[slnc 250]] And a test, or a regional module, or a partner "
            "integration can't introduce a pricing rule of its own without being "
            "added to the enum first."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Strategy Pattern",
        body=[
            "“Define a family of algorithms, encapsulate each one,",
            "and make them interchangeable.”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "pass in the behaviour, don't branch on a flag.",
        ],
        narration=(
            "The strategy pattern fixes exactly this. [[slnc 250]] In Gang of "
            "Four terms, strategy defines a family of algorithms, encapsulates "
            "each one, and makes them interchangeable — so the algorithm can vary "
            "independently from the clients that use it. [[slnc 300]] In plain "
            "language? Pass in the behaviour. Don't branch on a flag."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="Remember It With Getting Across Town",
        body=[
            "You want to get from the office to the station.",
            "You can walk, take a bus, cycle, or get a taxi.",
            "",
            "You don't change — same person, same start, same destination.",
            "What changes is the method, and each method has its own rules.",
            "",
            "You decide once, in the morning. You don't re-decide",
            "'bus or bike?' at every street corner.",
        ],
        narration=(
            "Here's how to remember it forever. Think about getting across town. "
            "[[slnc 250]] You want to get from the office to the station. You can "
            "walk, take a bus, cycle, or get a taxi. [[slnc 300]] You don't "
            "change — same person, same starting point, same destination. What "
            "changes is the method, and each method has its own rules: a bus has "
            "a timetable, a taxi has a meter, a bike needs somewhere to lock up. "
            "[[slnc 350]] And here's the bit that matters. You decide which one "
            "once, in the morning, based on the weather and how late you are. You "
            "do not re-decide bus or bike at every street corner. [[slnc 250]] "
            "Pick the approach once, then just use it. That's strategy."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Three Roles",
        body=None,
        narration=(
            "Every strategy setup has three roles. [[slnc 200]] The strategy "
            "itself — here, ShippingCostRule — the one interface describing the "
            "job to be done. The concrete strategies: flat rate, weight banded, "
            "distance based, free over threshold. One algorithm each, knowing "
            "nothing about checkout. And the context, CheckoutService, which "
            "holds one rule and calls it. [[slnc 350]] Here's the single most "
            "important idea in this whole video. CheckoutService cannot behave "
            "differently depending on which rule it's holding, because there is "
            "no message it can send to find out which one that is. [[slnc 250]] "
            "The day you need an instance-of check in there, the pattern hasn't "
            "been applied — it's just been decorated."
        ),
    ),
    dict(
        key="09-strategy",
        kind="code",
        title="The Strategy — One Small Interface",
        body="""public interface ShippingCostRule {
    String name();
    Money costFor(Shipment shipment);
}

public record Shipment(String destination, double weightKg,
                       int distanceMiles, Money orderSubtotal) { }

//  FlatRateRule reads none of those fields. That is deliberate:
//  if costFor took just a weight, no distance rule could exist.""",
        narration=(
            "This is the strategy, ShippingCostRule. [[slnc 250]] Two methods. "
            "costFor does the work; name is there so the receipt can say which "
            "policy priced it — without that, the client would need a lookup "
            "table of display names, and that table is the switch we just deleted "
            "growing back somewhere new. [[slnc 350]] And notice what costFor "
            "takes: a whole Shipment. Destination, weight, distance, subtotal. "
            "[[slnc 250]] The flat rate rule reads none of those fields, and "
            "that's fine — it's deliberate. If costFor took just a weight, the "
            "distance rule could not exist, and adding it would change the "
            "interface and therefore every single implementation. Passing the "
            "whole shipment is what makes a new rule cost exactly one class."
        ),
    ),
    dict(
        key="10-concrete",
        kind="code",
        title="A Concrete Strategy — It Knows Only Its Own Arithmetic",
        body="""public final class WeightBandedRule implements ShippingCostRule {

    public record Band(double upToKg, Money cost) { }

    @Override
    public Money costFor(Shipment shipment) {
        for (Band band : bands) {            // lightest band first
            if (shipment.weightKg() <= band.upToKg()) {
                return band.cost();
            }
        }
        return overweightCost;
    }
}""",
        narration=(
            "And this is a concrete strategy, WeightBandedRule. [[slnc 250]] The "
            "band table is data, not code, so a pricing change is a change to a "
            "list rather than to the algorithm. [[slnc 300]] But the thing worth "
            "noticing is what's absent. There's no mention of distance, no "
            "campaign threshold, no flat fee, and no checkout. This class knows "
            "its own arithmetic and nothing else — which means it gets its own "
            "test, and that test never has to construct an order or go anywhere "
            "near a checkout service."
        ),
    ),
    dict(
        key="11-context",
        kind="code",
        title="The Context — Search It for the Word 'Weight'",
        body="""public final class CheckoutService {

    private final ShippingCostRule shippingRule;

    public Quote quote(Shipment shipment) {
        Money delivery = shippingRule.costFor(shipment);
        return new Quote(shippingRule.name(),
                         shipment.orderSubtotal(), delivery);
    }
}

//  No if. No instanceof. No enum. The switch did not move -- it is gone.""",
        narration=(
            "And this is the context, CheckoutService. [[slnc 250]] Search this "
            "class for the words flat, or weight, or distance, and you find "
            "nothing. It holds a rule and it calls it. [[slnc 300]] There's no "
            "if, no instance-of, no enum. And that's the test of whether strategy "
            "has actually been applied: moving a switch out of this class into a "
            "helper would just relocate the decision. Taking the behaviour as a "
            "constructor argument removes it. [[slnc 350]] Now — somebody always "
            "asks at this point, quite rightly: where did the branch actually "
            "go? Something still has to turn a config value into an object. "
            "[[slnc 250]] It goes into a small registry at the edge of the "
            "system. And the difference isn't that it disappeared, it's what it "
            "does and how often. The naive switch ran inside the pricing logic, "
            "on every single quote, tangling the decision up with the arithmetic. "
            "The registry runs once, when the shop is configured, and answers a "
            "completely different question: which rule is in force today. In a "
            "real store that's a database row or a feature flag — the mapping is "
            "data, and the pricing code never sees it."
        ),
    ),
    dict(
        key="12-proof",
        kind="code",
        title="The Test That Actually Proves It",
        body="""@Test
void acceptsARuleDefinedEntirelyInThisTest() {
    ShippingCostRule pricePerKilo = new ShippingCostRule() {
        public String name() { return "Per kilo"; }
        public Money costFor(Shipment s) { return Money.pounds(s.weightKg()); }
    };

    assertEquals(Money.pounds(6.50),
            new CheckoutService(pricePerKilo).quote(PARCEL).delivery());
}

//  Nothing in src/main knows this rule exists.""",
        narration=(
            "Here's a subtlety worth pausing on, because it changes how you test "
            "this. [[slnc 250]] A test that says a six and a half kilo parcel "
            "costs twelve pounds passes against the naive design too. It tells "
            "you the arithmetic is right, but it proves nothing at all about "
            "whether the pattern was applied. [[slnc 350]] This one does. It "
            "defines a pricing rule entirely inside the test — nothing in the "
            "production source knows this rule exists — hands it to "
            "CheckoutService, and it just works. [[slnc 250]] If somebody "
            "quietly put the switch back tomorrow, this is the test that would "
            "go red."
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

Rule "weight" -> Weight banded
  Cardiff, 6.5kg, 180 miles, order £64.00
    Weight banded: subtotal £64.00 + delivery £12.00 = £76.00

Rule "campaign" -> Free over £50.00
  Cardiff, 6.5kg, 180 miles, order £64.00
    Free over £50.00: subtotal £64.00 + delivery FREE = £64.00

An unknown rule name is refused, not defaulted:
  Rejected: no shipping rule called "second-class" """,
        narration=(
            "When we run the project, the same Cardiff parcel gets priced by "
            "every rule in turn. [[slnc 250]] Under weight bands the delivery is "
            "twelve pounds. Under the campaign rule the order is over fifty "
            "pounds, so delivery is free and the total drops to sixty four. "
            "[[slnc 300]] Same client object. Same method call. Not one line of "
            "CheckoutService changed between those two quotes. [[slnc 300]] And "
            "at the bottom, the thing the naive version couldn't do: an "
            "unrecognised rule name is refused outright, rather than falling into "
            "a default branch and shipping for free."
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use strategy when a switch branches on a 'type' or 'mode' field",
            "and each branch does real, unrelated work.",
            "",
            "Keep strategies stateless, and never let the context ask what",
            "it is holding -- instanceof is the branch coming back.",
            "",
            "Remember one sentence:",
            "Strategy's choice comes from outside and stays put.",
            "A State object swaps itself for another as events arrive.",
        ],
        narration=(
            "So, to recap. Use strategy when a switch branches on a type or a "
            "mode field and each branch does real, unrelated work. [[slnc 300]] "
            "Keep the strategies stateless, so one instance can be shared by "
            "every concurrent order. And never let the context ask what it's "
            "holding — the moment you write instance-of, the branch is back and "
            "the pattern is decoration. [[slnc 250]] One honest word of warning: "
            "four classes instead of one method is a real cost. For two rules "
            "that will never change, the switch is genuinely the better answer. "
            "Strategy pays for itself when the family is open-ended — and "
            "delivery pricing really is, because marketing owns it. [[slnc 350]] "
            "And if you remember one sentence from today, make it this one. "
            "Strategy and State have exactly the same shape — an interface, "
            "several implementations, a context holding one. The difference is "
            "who chooses, and how often. Strategy's choice comes from outside and "
            "stays put. A state object swaps itself for another as events arrive."
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
            "And that's the strategy pattern. [[slnc 300]] If you got something "
            "out of this, do give it a thumbs up, and subscribe. It genuinely "
            "helps the channel, and it's what makes more of these possible. "
            "[[slnc 250]] And if there's a pattern you'd like me to cover next, "
            "drop it in the comments. I read every one. [[slnc 250]] All the "
            "source code, the written notes and an interactive animation are in "
            "the repository. Thanks for watching, and I'll see you in the next "
            "one."
        ),
    ),
]
