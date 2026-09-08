"""Scene definitions for the Adapter pattern teaching video.

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
        title="The Adapter Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Adapter pattern in Java, "
            "and it is written and presented by Jayasekhar Konduru. [[slnc 300]] "
            "Let's start with the simple definition. The adapter pattern wraps a "
            "class whose interface you cannot change inside one that has the "
            "interface you want. Your code goes on calling the interface it "
            "expects, the adapter does the translating, and the awkward original "
            "is touched by exactly one class in your codebase. [[slnc 350]] "
            "That's the idea in a sentence — making two interfaces that were "
            "never designed for each other work together anyway. The rest of the "
            "video does it properly, by building a real working Java project: a "
            "checkout flow that needs shipping rates from a third-party S D K "
            "with completely different units. [[slnc 250]] By the end you'll know "
            "how to isolate an incompatible interface behind one class, and how "
            "to write that class yourself."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "Checkout needs a shipping rate for an order:",
            "",
            "  destination ZIP code, weight in kilograms, price in dollars",
            "",
            "The only carrier available is a third-party SDK:",
            "",
            "  Acme Shipping — weight in pounds, price in integer cents",
        ],
        narration=(
            "So, imagine checkout for an online store. [[slnc 250]] Checkout "
            "needs a shipping rate for an order, given a destination ZIP code and "
            "a weight in kilograms, and it wants a price back in dollars. That's "
            "the shape the rest of the codebase already uses everywhere. "
            "[[slnc 300]] And the only carrier available is a third-party S D K, "
            "Acme Shipping. It works in pounds, not kilograms, and it returns a "
            "price in integer cents, not dollars."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Two Shapes That Don't Match",
        body=[
            "What checkout wants   — quoteRate(zip, kilograms) -> dollars",
            "What Acme provides    — fetchCostInCents(zip, pounds) -> cents",
            "",
            "Naively, every caller converts units itself, every time.",
        ],
        narration=(
            "Look closely and the two shapes just don't line up. [[slnc 250]] "
            "Checkout wants to call something like quoteRate, pass a ZIP code and "
            "a weight in kilograms, and get dollars back. Acme's S D K gives you "
            "fetchCostInCents, taking pounds, returning cents. [[slnc 300]] "
            "Naively, every place in the codebase that needs a rate ends up doing "
            "its own unit conversion, by hand, every single time."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Convert at Every Call Site",
        body="""public final class NaiveCheckoutService {
    private final AcmeShippingSdk sdk = new AcmeShippingSdk();

    public BigDecimal shippingCost(String destinationZip, double weightKg) {
        double weightLb = weightKg * 2.20462;
        long cents = sdk.fetchCostInCents(destinationZip, weightLb);
        return BigDecimal.valueOf(cents)
                .divide(new BigDecimal("100"), 2, RoundingMode.HALF_UP);
    }
}

//  NaiveShippingEstimator repeats this exact conversion independently.""",
        narration=(
            "So here's the naive approach. [[slnc 250]] NaiveCheckoutService "
            "multiplies kilograms by two point two oh four six two to get "
            "pounds, calls Acme's S D K directly, then divides the returned "
            "cents by a hundred to get dollars. [[slnc 300]] And here's the "
            "problem. NaiveShippingEstimator, an entirely separate class "
            "elsewhere in the codebase, repeats this exact same conversion "
            "independently — copy-pasted, not shared."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   The unit conversion is duplicated at every call site",
            "✗   Every caller is coupled to Acme's exact method shape",
            "✗   Switching carriers means touching every caller, one by one",
            "✗   Nothing here is a bug — the waste is structural",
        ],
        narration=(
            "And that does real damage as the system grows. [[slnc 250]] The "
            "pounds-per-kilogram constant and the cents-to-dollars division get "
            "copy-pasted into every class that needs a rate. Every one of those "
            "callers is coupled to Acme's exact method name and parameter order. "
            "[[slnc 300]] Switch carriers, or Acme changes their S D K, and every "
            "caller needs to change, one at a time. [[slnc 250]] None of this is "
            "a bug — both naive classes compute a correct rate. The waste is "
            "structural: one mechanical conversion, scattered everywhere."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Adapter Pattern",
        body=[
            "“Convert the interface of a class into another interface",
            "clients expect.”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "one class translates, so nothing else has to.",
        ],
        narration=(
            "The adapter pattern fixes exactly this. [[slnc 250]] In Gang of "
            "Four terms, adapter converts the interface of a class into another "
            "interface clients expect, letting classes work together that "
            "couldn't otherwise, because of incompatible interfaces. [[slnc 300]] "
            "In plain language? One class translates, so nothing else in the "
            "codebase ever has to."
        ),
    ),
    dict(
        key="07-plug",
        kind="bullets",
        title="Remember It With a Wall Plug",
        body=[
            "A UK charger has UK prongs. A US wall socket has US slots.",
            "You don't rewire the charger, and you don't rewire the wall.",
            "",
            "A small adapter sits between them, translating one shape into",
            "the other. Neither side ever changes.",
            "",
            "One small translator. Two things that were never designed together.",
        ],
        narration=(
            "Here's how to remember it forever. Think about traveling with a "
            "laptop charger. [[slnc 250]] Your charger has UK prongs, the wall "
            "socket has US slots. You don't rewire the charger, and you "
            "certainly don't rewire the wall. [[slnc 300]] You plug a small "
            "adapter in between, and its entire job is translating one physical "
            "shape into the other. Neither the charger nor the socket ever "
            "changes. [[slnc 250]] One small translator, sitting between two "
            "things that were never designed together."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            "Every adapter setup has four roles. [[slnc 200]] The target, "
            "ShippingRateProvider, the interface clients already expect. The "
            "adaptee, AcmeShippingSdk, the existing incompatible class we don't "
            "control. The adapter, AcmeShippingAdapter, which implements the "
            "target and holds the adaptee. And the client, CheckoutService, "
            "which only ever depends on the target interface. [[slnc 350]] "
            "Here's the single most important idea in this whole video. "
            "AcmeShippingAdapter is the only class in the entire codebase that "
            "imports AcmeShippingSdk. Every other class only ever sees "
            "ShippingRateProvider."
        ),
    ),
    dict(
        key="09-target",
        kind="code",
        title="The Target — The Shape Checkout Already Expects",
        body="""public interface ShippingRateProvider {
    BigDecimal quoteRate(String destinationZip, double weightKg);
}

public final class AcmeShippingSdk {
    public long fetchCostInCents(String zip, double poundsMass) {
        // pounds in, integer cents out -- a shape checkout never asked for
    }
}""",
        narration=(
            "This is the target, ShippingRateProvider. [[slnc 250]] It's "
            "declared entirely in checkout's own terms — kilograms in, dollars "
            "out. [[slnc 300]] And this is the adaptee, AcmeShippingSdk. Pounds "
            "in, integer cents out, a method called fetchCostInCents. It's a "
            "shape checkout never asked for, and one we don't control."
        ),
    ),
    dict(
        key="10-adapter",
        kind="code",
        title="The Adapter — One Class Translates, Once",
        body="""public final class AcmeShippingAdapter implements ShippingRateProvider {

    private static final BigDecimal KG_TO_LB = new BigDecimal("2.20462");
    private final AcmeShippingSdk sdk;

    @Override
    public BigDecimal quoteRate(String destinationZip, double weightKg) {
        double weightLb = BigDecimal.valueOf(weightKg)
                .multiply(KG_TO_LB).doubleValue();
        long cents = sdk.fetchCostInCents(destinationZip, weightLb);
        return BigDecimal.valueOf(cents)
                .divide(new BigDecimal("100"), 2, RoundingMode.HALF_UP);
    }
}""",
        narration=(
            "And this is the adapter, AcmeShippingAdapter. [[slnc 250]] It "
            "implements ShippingRateProvider and holds an AcmeShippingSdk by "
            "composition. [[slnc 300]] quoteRate converts kilograms to pounds, "
            "calls the S D K, then converts the returned cents back to dollars. "
            "Every unit conversion in this entire project happens right here, "
            "exactly once."
        ),
    ),
    dict(
        key="11-client",
        kind="code",
        title="The Client — Can't Tell Adapted From Native",
        body="""ShippingRateProvider acme = new AcmeShippingAdapter(new AcmeShippingSdk());
ShippingRateProvider flat = new FlatRateShippingProvider();

CheckoutService checkoutA = new CheckoutService(acme);
CheckoutService checkoutB = new CheckoutService(flat);

checkoutA.totalWithShipping(subtotal, "94107", 3.5);   // adapted
checkoutB.totalWithShipping(subtotal, "94107", 3.5);   // native, no adapting at all""",
        narration=(
            "And here's the client, CheckoutService. [[slnc 250]] It's "
            "constructed with a ShippingRateProvider — sometimes that's an "
            "adapted AcmeShippingAdapter, sometimes it's a FlatRateShippingProvider "
            "written natively, with no adapting involved at all. [[slnc 300]] "
            "CheckoutService's own code never changes between the two. It "
            "genuinely cannot tell an adapted implementation from a native one — "
            "that's the whole payoff."
        ),
    ),
    dict(
        key="12-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

== Checkout works with any ShippingRateProvider, adapted or native ==
Acme (adapted):  $63.46
Flat rate (native):  $57.48

== The adapter converts units at exactly one seam ==
3.5 kg checkout weight -> AcmeShippingSdk sees pounds, returns cents
Quoted rate: $13.48

== The naive alternative, for comparison ==
NaiveCheckoutService:    $13.48
NaiveShippingEstimator:  $13.48""",
        narration=(
            "When we run the project, checkout produces a total with either "
            "provider, no branching in sight. [[slnc 250]] The isolated "
            "quoteRate call shows exactly what's happening under the hood: "
            "three point five kilograms goes in, Acme sees pounds, and thirteen "
            "dollars forty eight comes back out. [[slnc 300]] And down at the "
            "bottom, the naive classes produce the exact same number — they "
            "aren't wrong, they're just duplicated, and coupled directly to a "
            "shape that belongs behind one seam."
        ),
    ),
    dict(
        key="13-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use adapter when an existing interface doesn't match what",
            "your code already expects, and you can't change either side.",
            "",
            "Keep the adapter a pure translator — no new behavior, no caching,",
            "no retries. That belongs in a decorator, not here.",
            "",
            "Remember one sentence:",
            "Adapter reconciles two interfaces that already disagree.",
            "Bridge designs two hierarchies so they never have to.",
        ],
        narration=(
            "So, to recap. Use adapter when an existing interface doesn't "
            "match what your code already expects, and you can't or shouldn't "
            "change either side. [[slnc 300]] Keep the adapter a pure "
            "translator — no new behavior, no caching, no retry logic. Anything "
            "beyond translation belongs in a decorator, not here. [[slnc 350]] "
            "And if you remember one sentence from today, make it this one. "
            "Adapter reconciles two interfaces that already exist and disagree. "
            "Bridge designs two hierarchies from the start so they never have "
            "to agree on more than one seam."
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
            "And that's the adapter pattern. [[slnc 300]] If you got "
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
