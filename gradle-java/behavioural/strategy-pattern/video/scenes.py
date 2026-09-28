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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Strategy pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Strategy pattern turns '
            'each branch of a decision into its own class, behind one '
            'shared interface. [[slnc 400]] The code that needs the work '
            'done holds a strategy, and calls it. [[slnc 300]] It does '
            'not know, or care, which strategy it holds. [[slnc 300]] So '
            'a new option is a new class, not a new case in a switch '
            'statement. [[slnc 600]] Think of getting across town. [[slnc '
            '300]] You can walk, take the bus, or call a taxi. [[slnc '
            '300]] You choose once, and then just go. [[slnc 700]] In '
            'this video, we price delivery at an online checkout, using '
            'four different shipping rules. [[slnc 500]] By the end, you '
            'will know how to add a fifth rule without editing a single '
            'line of code that already works.'
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
            'Here is the scenario. [[slnc 400]] At checkout, an online '
            'shop must quote a delivery charge. [[slnc 300]] And the rule '
            'it uses keeps changing, because it is a business decision. '
            '[[slnc 500]] There are four rules. [[slnc 300]] A flat rate, '
            'the same on everything. [[slnc 300]] Weight bands: under one '
            'kilo, under five, under twenty, and above. [[slnc 300]] '
            'Distance: a base fee, plus a charge per hundred miles. '
            '[[slnc 300]] And a campaign rule: free delivery on orders '
            'over fifty pounds. [[slnc 500]] Marketing switches the '
            'campaign on for two weeks, and off again. [[slnc 300]] No '
            'single rule is permanent.'
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
            'The obvious first approach is simple. [[slnc 300]] A list of '
            'shipping methods, and a switch statement inside the checkout '
            'code, with one case per rule. [[slnc 500]] To be fair, this '
            'works. [[slnc 300]] Every price it produces is correct. '
            '[[slnc 300]] For two rules that never change, it is the '
            'right answer. [[slnc 500]] So what follows is not a bug '
            'report. [[slnc 300]] It is a design complaint.'
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
            'Here is the naive version. [[slnc 400]] Four unrelated '
            'pricing rules, mixed together in one method. [[slnc 300]] '
            'Weight bands, distance rounding, and the campaign threshold '
            'have nothing to do with each other. [[slnc 300]] Yet you '
            'cannot read one without reading past the other three. [[slnc '
            '600]] Now think about the default branch at the bottom of '
            'the switch. [[slnc 300]] It exists because the method must '
            'return something. [[slnc 300]] And it does the only '
            'safe-looking thing: it charges nothing. [[slnc 500]] Add a '
            'fifth shipping method, such as locker collection, and forget '
            'this switch. [[slnc 300]] The shop starts delivering for '
            'free. [[slnc 300]] No compile error, no crash, just a '
            'quietly wrong number on the receipt.'
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
            'And the damage grows with the system. [[slnc 500]] Four '
            'unrelated rules share one method. [[slnc 300]] A fifth rule '
            'means editing the method that four working rules depend on. '
            '[[slnc 400]] To test one rule, like the price for six and a '
            'half kilos, you must build a whole shipment, and go through '
            'checkout. [[slnc 400]] The default branch quietly delivers '
            'for free. [[slnc 400]] And no test, regional module, or '
            'partner can add a rule of its own, without changing the '
            'central list first.'
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
            'The Strategy pattern fixes exactly this. [[slnc 400]] Here '
            'is its definition, from the famous Gang of Four book. [[slnc '
            '300]] Define a family of algorithms, put each one in its own '
            'class, and make them interchangeable. [[slnc 500]] In plain '
            'words: pass in the behaviour. [[slnc 300]] Do not branch on '
            'a flag.'
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
            'Here is an easy way to remember it: getting across town. '
            '[[slnc 500]] You want to get from the office to the station. '
            '[[slnc 300]] You could walk, take a bus, cycle, or get a '
            'taxi. [[slnc 500]] You do not change. [[slnc 300]] Same '
            'person, same start, same destination. [[slnc 300]] What '
            'changes is the method, and each method has its own rules. '
            '[[slnc 300]] A bus has a timetable, a taxi has a meter, and '
            'a bike needs somewhere to lock up. [[slnc 500]] And here is '
            'the key point. [[slnc 300]] You decide once, in the morning, '
            'based on the weather and how late you are. [[slnc 300]] You '
            'do not decide again at every street corner. [[slnc 500]] '
            'Choose the approach once, then just use it. [[slnc 300]] '
            'That is Strategy.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Three Roles",
        body=None,
        narration=(
            'Every Strategy design has three roles. [[slnc 500]] The '
            'strategy is the interface for the job. [[slnc 300]] Here, it '
            'is called Shipping Cost Rule. [[slnc 500]] The concrete '
            'strategies are the four rules: flat rate, weight banded, '
            'distance based, and free over a threshold. [[slnc 300]] Each '
            'one is one algorithm, and knows nothing about checkout. '
            '[[slnc 500]] And the context is the Checkout Service. [[slnc '
            '300]] It holds one rule, and calls it. [[slnc 600]] Here is '
            'the most important idea in the video. [[slnc 300]] The '
            'checkout cannot behave differently depending on which rule '
            'it holds. [[slnc 300]] It has no way to find out which rule '
            "that is. [[slnc 400]] If you ever need to check the rule's "
            'type inside the checkout, the pattern has not really been '
            'applied.'
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
            'The strategy interface has just two methods. [[slnc 400]] '
            'Cost For works out the delivery price. [[slnc 300]] And name '
            "gives the rule's display name, so the receipt can say which "
            'rule priced it. [[slnc 300]] Without name, you would need a '
            'separate table of display names, and that table is the old '
            'switch, growing back. [[slnc 600]] Notice what Cost For '
            'receives: the whole shipment. [[slnc 300]] Destination, '
            'weight, distance, and order total. [[slnc 500]] The flat '
            'rate rule uses none of those, and that is fine. [[slnc 300]] '
            'If Cost For only received a weight, the distance rule could '
            'not exist. [[slnc 300]] Passing the whole shipment means a '
            'new rule costs exactly one new class.'
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
            'Now one real strategy: the weight banded rule. [[slnc 400]] '
            'Its price bands are data, a simple list, not code. [[slnc '
            '300]] So changing a price means editing a list, not the '
            'algorithm. [[slnc 500]] It goes through the bands from '
            'lightest to heaviest, and returns the first price that fits. '
            '[[slnc 600]] And notice what is missing. [[slnc 300]] No '
            'distance, no campaign threshold, no flat fee, and no '
            'checkout. [[slnc 300]] This class knows its own arithmetic, '
            'and nothing else. [[slnc 300]] So it can be tested on its '
            'own, without ever creating an order.'
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
            'Now the context, the Checkout Service. [[slnc 400]] Search '
            'it for the words flat, weight, or distance. [[slnc 300]] You '
            'find nothing. [[slnc 300]] It holds a rule, and calls it. '
            '[[slnc 500]] No if statements. [[slnc 200]] No type checks. '
            '[[slnc 200]] No list of methods. [[slnc 500]] Moving the '
            'switch into a helper would only relocate the decision. '
            '[[slnc 300]] Receiving the rule as a constructor argument '
            'removes it. [[slnc 600]] People often ask: where did the '
            'decision go? [[slnc 300]] Something still has to turn a '
            'setting into a rule object. [[slnc 400]] It moves into a '
            'small registry, at the edge of the system. [[slnc 300]] The '
            'naive switch ran inside the pricing logic, on every quote. '
            '[[slnc 300]] The registry runs once, when the shop is '
            'configured. [[slnc 300]] It only answers one question: which '
            'rule is in force today? [[slnc 300]] In a real shop, that '
            'answer is a database row, or a feature flag.'
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
            'Here is a subtle point about testing. [[slnc 400]] A test '
            'saying a six and a half kilo parcel costs twelve pounds '
            'would pass for the naive design too. [[slnc 300]] It proves '
            'the arithmetic, but nothing about the pattern. [[slnc 500]] '
            'This test does. [[slnc 300]] It creates a brand new pricing '
            'rule, entirely inside the test file. [[slnc 300]] Nothing in '
            'the main code knows it exists. [[slnc 300]] It hands the '
            'rule to the Checkout Service, and it simply works. [[slnc '
            '500]] If someone ever put the switch back, this is the test '
            'that would fail.'
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
            "Let's run the demo. [[slnc 400]] The same parcel, going to "
            'Cardiff, is priced by every rule in turn. [[slnc 500]] With '
            'weight bands, delivery costs twelve pounds. [[slnc 300]] '
            'With the campaign rule, the order is over fifty pounds, so '
            'delivery is free, and the total drops to sixty-four pounds. '
            '[[slnc 500]] The same checkout object. [[slnc 200]] The same '
            'method call. [[slnc 300]] Not one line of the checkout '
            'changed between those two quotes. [[slnc 500]] And finally, '
            'something the naive version could not do. [[slnc 300]] An '
            'unknown rule name is refused outright. [[slnc 300]] It does '
            'not fall into a default branch, and deliver for free.'
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
            'So, to recap. [[slnc 400]] Use Strategy when a switch '
            'branches on a type or mode, and each branch does real, '
            'unrelated work. [[slnc 500]] Keep strategies stateless, so '
            'one instance can be shared by every order at once. [[slnc '
            '300]] And never let the context ask what it is holding. '
            '[[slnc 300]] The moment it checks the type, the branch is '
            'back. [[slnc 600]] One honest warning. [[slnc 300]] Four '
            'classes instead of one method is a real cost. [[slnc 300]] '
            'For two rules that never change, the switch is the better '
            'answer. [[slnc 300]] Strategy pays off when the family of '
            'rules keeps growing, as delivery pricing does. [[slnc 600]] '
            'And one sentence to remember. [[slnc 300]] Strategy and '
            'State have exactly the same shape. [[slnc 300]] The '
            'difference is who chooses, and how often. [[slnc 300]] A '
            'strategy is chosen from outside, and stays put. [[slnc 300]] '
            'A state swaps itself for another, as events happen.'
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
            "That's the Strategy pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Pass in the '
            'behaviour, instead of branching on a flag. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] If there '
            'is a pattern you would like to see covered, suggest it in '
            'the comments. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
