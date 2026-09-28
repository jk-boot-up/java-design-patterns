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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Adapter pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An adapter wraps a class you '
            'cannot change, inside a class with the shape you want. '
            '[[slnc 300]] Your code keeps calling the shape it expects. '
            '[[slnc 300]] The adapter does the translating. [[slnc 300]] '
            'And the awkward original is touched by just one class in '
            'your code. [[slnc 600]] Think of a travel plug adapter. '
            '[[slnc 300]] Your charger and the wall socket never change. '
            '[[slnc 300]] A small adapter in between makes them fit. '
            '[[slnc 700]] In our online store, checkout needs shipping '
            "prices from another company's toolkit, which uses completely "
            'different units. [[slnc 500]] By the end, you will know how '
            'to hide a mismatched interface behind one class, and how to '
            'write that class yourself.'
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
            'Here is the scenario. [[slnc 400]] Checkout needs a shipping '
            'price for an order. [[slnc 300]] It gives a delivery zip '
            'code, and a weight in kilograms. [[slnc 300]] And it wants '
            'the price back in dollars. [[slnc 300]] That is the shape '
            'the rest of the code already uses. [[slnc 600]] But the only '
            'carrier available is a toolkit from another company, called '
            'Acme Shipping. [[slnc 300]] It works in pounds of weight, '
            'not kilograms. [[slnc 300]] And it returns the price in '
            'whole cents, not dollars.'
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
            'The two shapes just do not match. [[slnc 500]] Checkout '
            'wants to ask for a quote, with a zip code and kilograms, and '
            "get dollars back. [[slnc 300]] Acme's toolkit takes pounds, "
            'and returns cents. [[slnc 600]] So, done naively, every part '
            'of the code that needs a price does its own unit conversion, '
            'by hand, every time.'
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
            'Here is the naive approach. [[slnc 400]] The naive checkout '
            'multiplies kilograms by two point two oh four six two, to '
            "get pounds. [[slnc 300]] It calls Acme's toolkit directly. "
            '[[slnc 300]] Then it divides the cents by a hundred, to get '
            'dollars. [[slnc 600]] And here is the problem. [[slnc 300]] '
            'A completely separate class, a shipping estimator, repeats '
            'exactly the same conversion. [[slnc 300]] Copied and pasted, '
            'not shared.'
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
            'That does real damage as the system grows. [[slnc 500]] The '
            'conversion numbers get copied into every class that needs a '
            'price. [[slnc 300]] Every one of those classes depends on '
            "Acme's exact method name, and the order of its inputs. "
            '[[slnc 500]] Switch to another carrier, or let Acme change '
            'its toolkit, and every one of those classes must change, one '
            'by one. [[slnc 600]] And none of this is a bug. [[slnc 300]] '
            'Both naive classes calculate the correct price. [[slnc 300]] '
            'The waste is in the structure: one simple conversion, '
            'scattered everywhere.'
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
            'The Adapter pattern fixes exactly this. [[slnc 400]] The '
            'classic book on design patterns, by the authors known as the '
            'Gang of Four, describes it like this. [[slnc 300]] Convert '
            'the interface of a class into another interface that clients '
            'expect. [[slnc 600]] In plain words: one class translates, '
            'so nothing else has to.'
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
            'Here is how to remember it. [[slnc 300]] Think about '
            'travelling with a laptop charger. [[slnc 500]] Your charger '
            'has a British plug. [[slnc 300]] The wall socket is '
            'American. [[slnc 300]] You do not rewire the charger. [[slnc '
            '300]] And you certainly do not rewire the wall. [[slnc 500]] '
            'You plug a small adapter in between. [[slnc 300]] Its whole '
            'job is to turn one shape into the other. [[slnc 300]] '
            'Neither the charger nor the socket ever changes. [[slnc '
            '600]] One small translator, between two things that were '
            'never designed to fit.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            'Every adapter has four roles. [[slnc 500]] The target: the '
            'interface checkout already expects, called the shipping rate '
            "provider. [[slnc 300]] The adaptee: Acme's toolkit, the "
            'mismatched class we cannot change. [[slnc 300]] The adapter: '
            "the Acme shipping adapter, which offers the target's shape, "
            "and holds Acme's toolkit inside. [[slnc 300]] And the "
            'client: the checkout service, which only ever talks to the '
            'target. [[slnc 600]] Here is the most important idea in this '
            'video. [[slnc 300]] The adapter is the only class in the '
            "whole code that knows Acme's toolkit exists. [[slnc 300]] "
            'Every other class only sees the shipping rate provider.'
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
            'Here is the target, the shipping rate provider. [[slnc 400]] '
            "It is written entirely in checkout's own terms. [[slnc 300]] "
            'Kilograms in, dollars out. [[slnc 600]] And here is the '
            "adaptee, Acme's toolkit. [[slnc 300]] Pounds in, whole cents "
            'out. [[slnc 300]] A shape checkout never asked for, and one '
            'we cannot change.'
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
            'And here is the adapter. [[slnc 400]] It offers the shipping '
            "rate provider's shape, and keeps Acme's toolkit inside it. "
            '[[slnc 600]] When asked for a quote, it converts kilograms '
            "to pounds. [[slnc 300]] It calls Acme's toolkit. [[slnc "
            '300]] Then it converts the cents back to dollars. [[slnc '
            '500]] Every unit conversion in this whole project happens '
            'right here, exactly once.'
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
            'And here is the client, the checkout service. [[slnc 400]] '
            'It is given a shipping rate provider. [[slnc 300]] Sometimes '
            'that is the Acme adapter. [[slnc 300]] Sometimes it is a '
            'flat-rate provider, written in the right shape from the '
            'start, with no adapting at all. [[slnc 600]] The checkout '
            'code never changes between the two. [[slnc 300]] It cannot '
            'tell an adapted provider from a native one. [[slnc 300]] And '
            'that is the whole payoff.'
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
            "Let's run the project. [[slnc 400]] Checkout calculates a "
            'total with either provider, with no special cases. [[slnc '
            '300]] With Acme, through the adapter: sixty-three dollars '
            'forty-six. [[slnc 300]] With the flat rate: fifty-seven '
            'dollars forty-eight. [[slnc 600]] Looking inside one quote: '
            'three and a half kilograms goes in. [[slnc 300]] Acme sees '
            'pounds. [[slnc 300]] And thirteen dollars forty-eight comes '
            'back out. [[slnc 600]] And the naive classes give exactly '
            'the same number. [[slnc 300]] They are not wrong. [[slnc '
            '300]] They are just duplicated, and tied to a shape that '
            'belongs behind one class.'
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
            'So, to recap. [[slnc 400]] Use an adapter when an existing '
            'interface does not match what your code expects. [[slnc '
            '300]] And you cannot, or should not, change either side. '
            '[[slnc 600]] Keep the adapter a pure translator. [[slnc '
            '300]] No new behaviour, no caching, and no retries. [[slnc '
            '300]] Anything beyond translating belongs in a different '
            'pattern, the Decorator. [[slnc 600]] And one comparison '
            'worth knowing. [[slnc 300]] An adapter fixes two interfaces '
            'that already exist, and disagree. [[slnc 300]] The Bridge '
            'pattern designs two sides from the start, so they never need '
            'fixing.'
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
            "That's the Adapter pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] An adapter is one '
            'small translator, so the rest of your code never has to know '
            'about a mismatched interface. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 300]] It runs offline, '
            'with nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Add a second '
            'carrier, with yet another set of units. [[slnc 300]] And '
            'notice that checkout does not change at all. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
