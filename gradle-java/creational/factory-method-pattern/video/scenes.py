"""Scene definitions for the Factory Method pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "title" | "bullets" | "quote" | "code" | "console" | "diagram"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="The Factory Method Pattern",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Factory Method pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Factory Method pattern '
            'moves the creation of an object into a method that '
            'subclasses override. [[slnc 400]] A base class writes the '
            'steps that never change. [[slnc 300]] Wherever it needs a '
            'new object, it calls that method. [[slnc 300]] So each '
            'subclass decides which class gets created, and the '
            'surrounding code never changes. [[slnc 600]] Think of a '
            "coffee chain's recipe card. [[slnc 300]] Head office writes "
            'every step, but leaves, make the drink, blank. [[slnc 300]] '
            'Each branch fills in its own drink. [[slnc 700]] In this '
            'video, we build the delivery step of an online store. [[slnc '
            '500]] By the end, you will know what a factory method is, '
            'why it exists, and how to write one yourself.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "A customer checks out and picks a delivery tier.",
            "",
            "Each tier hands the parcel to a different carrier:",
            "  1.  Standard         Royal Post          5 days",
            "  2.  Express          SkyLink Air         2 days",
            "  3.  Same Day         CityRide Bikes      today",
            "  4.  International    TransWorld Freight  9 days",
            "",
            "But every tier runs the same shipping workflow.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] A customer checks out, '
            'and picks a delivery option. [[slnc 500]] Standard delivery '
            'goes by post, and takes five days. [[slnc 300]] Express '
            'flies overnight, and takes two days. [[slnc 300]] Same day '
            'goes out on a bike. [[slnc 300]] And international crosses a '
            'border, and takes nine days. [[slnc 500]] Four different '
            'carriers, with different prices, and different delivery '
            'dates. [[slnc 500]] But here is the important detail. [[slnc '
            '300]] Every one of them runs the same shipping steps around '
            'its carrier.'
        ),
    ),
    dict(
        key="03-workflow",
        kind="bullets",
        title="The Workflow Is Always the Same",
        body=[
            "1.  Check the order actually has weight",
            "2.  Log that we are preparing the parcel",
            "3.  Hand it to the carrier",
            "4.  Log the tracking number and the promised date",
            "",
            "Steps 1, 2 and 4 never change.",
            "Only step 3 differs between tiers.",
        ],
        narration=(
            "Let's list what shipping involves. [[slnc 400]] Step one: "
            'check the order really has some weight. [[slnc 300]] Step '
            'two: log that we are preparing the parcel. [[slnc 300]] Step '
            'three: hand it to the carrier. [[slnc 300]] Step four: log '
            'the tracking number, and the promised date. [[slnc 600]] '
            'Steps one, two, and four are identical for every delivery '
            'option. [[slnc 300]] Only step three, the hand-over, is '
            'different. [[slnc 500]] Remember that, because it is the '
            'whole reason this pattern exists.'
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Problem — One Class Doing Both Jobs",
        body="""public Shipment ship(Order order, String tier) {

    if (order.weightKg() <= 0) { throw ...; }

    Courier courier;
    if (tier.equals("STANDARD")) {
        courier = new PostalCourier();
    } else if (tier.equals("EXPRESS")) {
        courier = new AirCourier();
    } else if (tier.equals("SAME_DAY")) {
        courier = new BikeCourier();
    } else { throw new IllegalArgumentException(...); }

    System.out.println("preparing " + order.orderId());
    return courier.dispatch(order);
}""",
        narration=(
            'Here is the naive version, and it is what most of us would '
            'write first. [[slnc 500]] One shipping method, with a chain '
            'of if statements in the middle, choosing the carrier by '
            'name. [[slnc 500]] The shared steps are in there. [[slnc '
            '300]] The choosing is in there. [[slnc 300]] They are '
            'tangled together, and you cannot read one without the other.'
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   Adding drone delivery means editing working code",
            "✗   Code that already ships real parcels, today",
            "✗   A second difference means a second if chain",
            "✗   A partner module cannot add a tier at all",
            "✗   You cannot test the workflow apart from the choosing",
        ],
        narration=(
            'Now, drone delivery launches on Monday. [[slnc 300]] Which '
            'file do you open? [[slnc 500]] This one. [[slnc 300]] The '
            'one that already ships real parcels, for four delivery '
            'options, today. [[slnc 300]] And every edit to working code '
            'is a chance to break something. [[slnc 500]] It gets worse. '
            '[[slnc 300]] If international also needs a customs check, '
            'you need a second if chain, on the same name. [[slnc 300]] '
            'And the two chains must always stay in step. [[slnc 500]] A '
            'partner team cannot add a delivery option at all. [[slnc '
            '300]] And you cannot test the shared steps without the '
            'choosing, because they are one method.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Factory Method",
        body=[
            "“Define an interface for creating an object,",
            "but let subclasses decide which class",
            "to instantiate.”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "leave a hole in the workflow, and let a subclass fill it.",
        ],
        narration=(
            'The Factory Method fixes exactly this. [[slnc 400]] Here is '
            'its definition, from the famous Gang of Four book. [[slnc '
            '300]] Define an interface for creating an object, but let '
            'subclasses decide which class to create. [[slnc 500]] That '
            'is precise, but it confuses many people. [[slnc 500]] So '
            'here it is in plain words. [[slnc 300]] Write the steps '
            'once, and leave a gap in the middle. [[slnc 300]] Then let a '
            'subclass fill in that gap. [[slnc 300]] That is the whole '
            'pattern.'
        ),
    ),
    dict(
        key="07-coffee",
        kind="bullets",
        title="Remember It With a Coffee Chain",
        body=[
            "Head office writes the recipe card:",
            "",
            "  1.  Greet the customer",
            "  2.  Make the drink          ←  left blank on purpose",
            "  3.  Lid on, call the name, hand it over",
            "",
            "Tokyo makes matcha.  Rome makes espresso.",
            "Head office never learns what matcha is.",
        ],
        narration=(
            'Here is an easy way to remember it: a coffee shop chain. '
            '[[slnc 500]] Head office writes the recipe card for serving '
            'a hot drink. [[slnc 300]] Step one: greet the customer. '
            '[[slnc 300]] Step two: make the drink. [[slnc 300]] Step '
            'three: put a lid on, call out the name, and hand it over. '
            '[[slnc 500]] Steps one and three are the same in every '
            'branch in the world. [[slnc 300]] Step two is left blank, on '
            'purpose. [[slnc 500]] The Tokyo branch makes matcha. [[slnc '
            '300]] The Rome branch makes espresso. [[slnc 300]] And head '
            'office never needs to know what matcha is. [[slnc 300]] It '
            'only knows that whatever comes back can have a lid put on '
            'it.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            'Every factory method has four roles. [[slnc 500]] First, the '
            'product: our Courier interface. [[slnc 300]] Second, the '
            'concrete products: the four carrier classes. [[slnc 300]] '
            'Third, the creator: an abstract class called Delivery '
            'Service. [[slnc 300]] It owns the shared steps, and declares '
            'the factory method. [[slnc 300]] Fourth, the concrete '
            'creators: the four delivery options. [[slnc 300]] Each one '
            'answers a single question: which courier? [[slnc 600]] And '
            'here is the most important idea in the video. [[slnc 300]] '
            'The parent class makes the call. [[slnc 300]] The child '
            'class decides what comes back.'
        ),
    ),
    dict(
        key="09-product",
        kind="code",
        title="A Product — Small, Focused, Unaware",
        body="""public class AirCourier implements Courier {

    public String name() {
        return "SkyLink Air";
    }

    public Shipment dispatch(Order order) {
        System.out.println("SkyLink Air: booking...");
        return new Shipment(TrackingIds.withPrefix("SL"),
                name(), 2, 12.50 + order.weightKg() * 1.20);
    }
}

//  It has no idea a delivery tier exists.""",
        narration=(
            "Let's look at one product: the air courier. [[slnc 400]] "
            'Notice how small, and ordinary, it is. [[slnc 300]] It knows '
            'its own name, SkyLink Air. [[slnc 300]] Its own tracking '
            'prefix, its own speed of two days, and its own pricing. '
            '[[slnc 500]] And it has no idea that delivery options exist, '
            'or that three other carriers exist. [[slnc 300]] That is '
            'deliberate. [[slnc 400]] The other three carriers follow '
            'exactly the same shape.'
        ),
    ),
    dict(
        key="10-creator",
        kind="code",
        title="The Creator — A Workflow With a Hole in It",
        body="""public abstract class DeliveryService {

    protected abstract Courier createCourier();

    public final Shipment ship(Order order) {

        if (order.weightKg() <= 0) { throw ...; }

        Courier courier = createCourier();

        System.out.println(tier() + ": preparing ...");
        Shipment shipment = courier.dispatch(order);
        System.out.println(tier() + ": booked ...");

        return shipment;
    }
}""",
        narration=(
            'And this is the heart of it: the Delivery Service class. '
            '[[slnc 500]] Go through its ship method, step by step, and '
            'label each step shared, or varying. [[slnc 300]] The weight '
            'check is shared. [[slnc 300]] The two log lines are shared. '
            '[[slnc 300]] Exactly one line varies: the call to create '
            'courier. [[slnc 600]] And create courier is abstract. [[slnc '
            '300]] It has no body. [[slnc 300]] So the parent class makes '
            'a call that it cannot answer itself. [[slnc 500]] Notice too '
            'that the ship method is marked final. [[slnc 300]] A '
            'subclass may change which courier is used, and nothing else. '
            '[[slnc 300]] Not the check, not the logging, and not the '
            'order of the steps.'
        ),
    ),
    dict(
        key="11-subclass",
        kind="code",
        title="A Concrete Creator — Six Lines",
        body="""public class ExpressDelivery extends DeliveryService {

    protected Courier createCourier() {
        return new AirCourier();
    }

    public String tier() {
        return "Express";
    }
}

//  That is an entire delivery tier.
//  All four look exactly like this.
//  There is no switch anywhere in this project.""",
        narration=(
            'Here is an entire delivery option: Express Delivery. [[slnc '
            '400]] It is six lines long. [[slnc 300]] Its create courier '
            'method returns a new air courier. [[slnc 300]] And it names '
            'itself, Express. [[slnc 300]] That is all it does. [[slnc '
            '500]] All four delivery options look exactly like this. '
            '[[slnc 500]] Search the whole project for a switch '
            'statement. [[slnc 300]] There is none. [[slnc 300]] Search '
            'for an if statement that tests a delivery name. [[slnc 300]] '
            'There is none of those either. [[slnc 500]] The decision '
            'that used to be a branch is now a class. [[slnc 300]] And '
            'choosing a class is something Java already does for us, for '
            'free.'
        ),
    ),
    dict(
        key="12-openclosed",
        kind="bullets",
        title="What You Gain",
        body=[
            "✓   New tier means a new file — never an edit",
            "✓   Shared behaviour is written once, for every tier",
            "✓   Other teams and other jars can add tiers",
            "✓   The compiler refuses a subclass that forgets the method",
            "",
            "Simple Factory moved the switch into one file.",
            "Factory Method removed the switch entirely.",
        ],
        narration=(
            "So what did that buy us? [[slnc 500]] Monday's drone "
            'delivery is now one new file. [[slnc 300]] No existing class '
            'is touched. [[slnc 300]] That is the Open Closed Principle, '
            'really working. [[slnc 500]] The weight check is written '
            'once, and it protects every delivery option that will ever '
            'exist. [[slnc 300]] Another team can add a delivery option '
            'in their own library. [[slnc 300]] And if a subclass forgets '
            'to provide a courier, it will not even compile. [[slnc 600]] '
            'Compare that with its simpler cousin. [[slnc 300]] A simple '
            'factory moves the switch statement into one file. [[slnc '
            '300]] A factory method removes the switch statement '
            'entirely.'
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

Standard: preparing ORD-2001 for Edinburgh via Royal Post
Royal Post: dropping ORD-2001 into the postal network
Standard: booked RP-FC57FBBE, arriving in 5 day(s)

Express: preparing ORD-2001 for Edinburgh via SkyLink Air
SkyLink Air: booking ORD-2001 onto tonight's flight
Express: booked SL-832C886D, arriving in 2 day(s)""",
        narration=(
            "Let's run the demo. [[slnc 400]] Two of the delivery options "
            'ship the very same order, to Edinburgh. [[slnc 500]] Each '
            'begins with the same line: preparing the order. [[slnc 300]] '
            'And each ends with the same line: booked, with a tracking '
            'number and a delivery date. [[slnc 500]] Only the middle '
            'line is different, printed by the carrier itself. [[slnc '
            '300]] Royal Post drops it into the postal network. [[slnc '
            "300]] SkyLink Air books it onto tonight's flight. [[slnc "
            '500]] One shared set of steps, running completely different '
            'carriers.'
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use a Factory Method when a shared workflow needs",
            "one varying step, and that step creates an object.",
            "",
            "Keep the return type abstract — never the concrete class.",
            "Never call the factory method from a constructor.",
            "One line of difference? A plain Supplier may be enough.",
            "",
            "Remember one sentence:",
            "Simple Factory chooses with a switch.",
            "Factory Method chooses with inheritance.",
        ],
        narration=(
            'So, to recap. [[slnc 400]] Use a factory method when you '
            'have shared steps, with one step that varies, and that step '
            "creates an object. [[slnc 500]] Keep the method's return "
            'type abstract. [[slnc 300]] The moment it promises a '
            'specific carrier class, the coupling comes straight back. '
            '[[slnc 500]] Never call the factory method from a '
            'constructor. [[slnc 300]] The subclass is not fully ready at '
            'that point. [[slnc 500]] And be honest with yourself. [[slnc '
            '300]] If the only difference between subclasses is one new '
            'object, simply passing in a supplier may be enough. [[slnc '
            '300]] Do not build a class hierarchy just to avoid a '
            'two-line switch. [[slnc 600]] And one sentence to remember. '
            '[[slnc 300]] A simple factory chooses with a switch. [[slnc '
            '300]] A factory method chooses with inheritance.'
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
            "That's the Factory Method pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Write '
            'the shared steps once, leave a gap, and let each subclass '
            'fill it. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] If there is a pattern you would '
            'like to see covered, suggest it in the comments. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
