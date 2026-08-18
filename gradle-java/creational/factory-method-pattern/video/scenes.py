"""Scene definitions for the Factory Method pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "title" | "bullets" | "quote" | "code" | "console" | "diagram"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    dict(
        key="01-title",
        kind="title",
        title="The Factory Method Pattern",
        body=["A beginner's guide, in Java 21",
              "Learn it by building an online store's delivery tiers"],
        narration=(
            "Hello, and welcome. In this short video we are going to learn one of the "
            "most useful patterns in the Gang of Four book: the Factory Method. It has a "
            "reputation for being confusing, and I think that is only because of how it "
            "is usually explained. So we will learn it by building a real, working Java "
            "project, the delivery step of an online store. By the end you will know what "
            "a factory method is, why it exists, and how to write one yourself."
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
            "Imagine you are building an online store. A customer checks out and picks a "
            "delivery tier. Standard goes by post and takes five days. Express flies "
            "overnight. Same day goes out on a bike. International crosses a border. Four "
            "different carriers, four different prices, four different delivery dates. "
            "But, and this is the detail that matters, every single one of them runs the "
            "same shipping workflow around the carrier."
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
            "Look at what shipping actually involves. First we check the order really "
            "has some weight. Then we log that we are preparing the parcel. Then we hand "
            "it over to the carrier. And finally we log the tracking number and the "
            "promised date. Steps one, two and four are identical for every tier, "
            "forever. Only step three, the hand over, is different. Hold on to that. It "
            "is the whole reason this pattern exists."
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
            "So here is the naive version, and honestly it is what most of us would "
            "write first. One shipping method, with a chain of if and else sitting right "
            "in the middle of it. The workflow is there. The choosing is there. They are "
            "tangled together in the same method, and you cannot read one without reading "
            "the other."
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
            "Now, we launch drone delivery on Monday. Which file do you open? This one. "
            "The one that already ships real parcels for four tiers today. Every edit to "
            "working code is a chance to break something that was fine. And it gets "
            "worse. If international also needs a customs check, you now need a second if "
            "chain on the same string, and the two have to stay in step. A partner team "
            "cannot add a tier at all. And you can never test the shared workflow "
            "separately from the choosing, because they are one method."
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
            "The Factory Method solves exactly this. The Gang of Four define it as: "
            "define an interface for creating an object, but let subclasses decide which "
            "class to instantiate. That sentence is precise, and it is also why the "
            "pattern confuses people. So here it is in plain language. You write the "
            "workflow once, and you leave a hole in the middle of it. Then you let a "
            "subclass fill in that hole. That is the entire pattern."
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
            "Here is the way to remember it forever. Think about a coffee shop chain. "
            "Head office writes the recipe card for serving a hot drink. Step one, greet "
            "the customer. Step two, make the drink. Step three, put a lid on it, call "
            "out the name, hand it over. Steps one and three are identical in every "
            "branch in the world, and head office owns them. Step two is deliberately "
            "left blank. The Tokyo branch makes matcha. The Rome branch makes espresso. "
            "And head office never learns what matcha is. It only knows that whatever "
            "comes back can have a lid put on it."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            "Every factory method has four roles. First, the product, which is our "
            "Courier interface. Second, the concrete products, our four carrier classes. "
            "Third, the creator. That is Delivery Service, the abstract class that owns "
            "the workflow and declares the factory method. And fourth, the concrete "
            "creators, our four delivery tiers, and each one answers a single question: "
            "which courier. Now here is the most important idea in this whole video. The "
            "parent class writes the call. The child class decides what comes back."
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
            "Let's look at some code. This is the air courier. Notice how small and how "
            "ordinary it is. It knows its own name, its own tracking prefix, its own "
            "speed and its own pricing. And it has absolutely no idea that a delivery "
            "tier exists, or that three other carriers exist. That is deliberate. The "
            "other three carriers follow exactly the same shape."
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
            "And this is the heart of it. Read the ship method and label every line as "
            "either shared, or varies. The guard is shared. The two log lines are shared. "
            "There is exactly one line that varies, and it is the call to create courier. "
            "Now look at the top of the class. Create courier is abstract. It has no "
            "body. The parent class has written a call that it cannot answer itself. Also "
            "notice that ship is marked final. A subclass may change which courier is "
            "used, and nothing else. Not the guard, not the logging, not the order of the "
            "steps."
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
            "And here is an entire delivery tier. Six lines. It picks a courier, it names "
            "itself, and that is all it does. All four tiers look exactly like this. Now "
            "search the whole project for the word switch. There isn't one. Search for an "
            "if statement testing a tier name. There isn't one of those either. The "
            "decision that used to be a branch is now a class, and choosing a class is "
            "something Java's own method dispatch does for us, for free."
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
            "So what did that buy us? Monday's drone delivery is now a new file, and we "
            "never touch an existing class. That is the Open Closed Principle, actually "
            "satisfied, not just talked about. The weight guard is written once and it "
            "protects every tier that will ever exist, including ones written next year "
            "by somebody else. A separate team can ship a tier in their own jar. And if a "
            "subclass forgets to override the factory method, it will not compile. Now "
            "compare this to its simpler cousin. A Simple Factory moves the switch into "
            "one file. A Factory Method removes the switch entirely."
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
            "When we run the project, we can watch it happen. Here are two of the four "
            "tiers, shipping the very same order. Look at the first and last line of each "
            "block. Same shape, same wording, same workflow. Only the middle line, the "
            "one the carrier itself printed, is different, and so are the price and the "
            "delivery date. That is the pattern working. One shared workflow, running "
            "completely different carriers."
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
            "So, to recap. Use a Factory Method when you have a workflow that is shared, "
            "with one step that varies, and that step creates an object. Keep the return "
            "type abstract. The moment your creator says it returns an air courier, all "
            "the coupling you removed comes straight back. Never call the factory method "
            "from a constructor, because the subclass fields are not ready yet. And be "
            "honest with yourself. If the only difference between your subclasses is one "
            "call to new, a plain supplier passed into the constructor may be all you "
            "need. Do not build a hierarchy to avoid a two line switch. If you remember "
            "just one sentence from today, make it this one: a Simple Factory chooses "
            "with a switch, and a Factory Method chooses with inheritance. Thank you for "
            "watching, and enjoy building your own creators."
        ),
    ),
]
