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
            "Hello, and welcome. This one is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] Today we're doing one of the most useful "
            "patterns in the Gang of Four book. The factory method. [[slnc 250]] "
            "Now it's got a reputation for being confusing, and honestly, I think "
            "that's only because of the way it usually gets explained. So we'll "
            "learn it by building a real working Java project. The delivery step "
            "of an online store. [[slnc 250]] And by the end, you'll know what a "
            "factory method is, why it exists, and how to write one yourself."
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
            "So, imagine you're building an online store. A customer checks out, "
            "and picks a delivery tier. [[slnc 250]] Standard goes by post, takes "
            "five days. Express flies overnight. Same day goes out on a bike. And "
            "international crosses a border. [[slnc 250]] Four different "
            "carriers, four different prices, four different delivery dates. "
            "[[slnc 300]] But here's the detail that matters. Every single one of "
            "them runs the same shipping workflow around that carrier."
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
            "Look at what shipping actually involves. [[slnc 250]] First, we "
            "check the order really has some weight to it. Then we log that we're "
            "preparing the parcel. Then we hand it over to the carrier. And "
            "finally we log the tracking number and the promised date. [[slnc "
            "300]] Steps one, two and four are identical for every tier. Forever. "
            "Only step three, the hand over, is different. [[slnc 300]] Hold on "
            "to that, because it's the whole reason this pattern exists."
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
            "So here's the naive version. And honestly, it's what most of us "
            "would write first. [[slnc 250]] One shipping method, with a chain of "
            "if and else sitting right in the middle of it. [[slnc 250]] The "
            "workflow is in there. The choosing is in there. They're tangled "
            "together in the same method, and you can't read one without reading "
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
            "Now. We're launching drone delivery on Monday. Which file do you "
            "open? [[slnc 300]] This one. The one that already ships real "
            "parcels, for four tiers, today. And every edit to working code is a "
            "chance to break something that was perfectly fine. [[slnc 300]] And "
            "it gets worse. If international also needs a customs check, you now "
            "need a second if chain on the same string, and those two have to "
            "stay in step with each other. [[slnc 250]] A partner team can't add "
            "a tier at all. And you can never test the shared workflow separately "
            "from the choosing, because they're one method."
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
            "The factory method fixes exactly this. [[slnc 250]] The Gang of Four "
            "define it as, define an interface for creating an object, but let "
            "subclasses decide which class to instantiate. [[slnc 250]] Now that "
            "sentence is precise. It's also exactly why the pattern confuses "
            "people. [[slnc 300]] So here it is in plain language. You write the "
            "workflow once, and you leave a hole in the middle of it. Then you "
            "let a subclass fill in that hole. [[slnc 250]] That's it. That's the "
            "entire pattern."
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
            "Here's how to remember it forever. Think about a coffee shop chain. "
            "[[slnc 250]] Head office writes the recipe card for serving a hot "
            "drink. Step one, greet the customer. Step two, make the drink. Step "
            "three, put a lid on it, call out the name, hand it over. [[slnc "
            "300]] Steps one and three are identical in every branch in the "
            "world, and head office owns them. Step two is deliberately left "
            "blank. [[slnc 250]] The Tokyo branch makes matcha. The Rome branch "
            "makes espresso. And head office never learns what matcha even is. It "
            "only knows that whatever comes back can have a lid put on it."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            "Every factory method has four roles. [[slnc 200]] First, the "
            "product, which is our Courier interface. Second, the concrete "
            "products, our four carrier classes. Third, the creator, and that's "
            "Delivery Service, the abstract class that owns the workflow and "
            "declares the factory method. And fourth, the concrete creators, our "
            "four delivery tiers, each one answering a single question. Which "
            "courier. [[slnc 350]] And here's the most important idea in the "
            "whole video. The parent class writes the call. The child class "
            "decides what comes back."
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
            "Let's look at some code. This is the air courier. [[slnc 250]] "
            "Notice how small it is. How ordinary. It knows its own name, its own "
            "tracking prefix, its own speed, and its own pricing. [[slnc 250]] "
            "And it has absolutely no idea that a delivery tier exists, or that "
            "three other carriers exist. Which is deliberate. [[slnc 200]] The "
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
            "And this is the heart of it. [[slnc 250]] Read the ship method, and "
            "label every line as either shared, or varies. The guard is shared. "
            "The two log lines are shared. [[slnc 250]] There's exactly one line "
            "that varies, and it's the call to create courier. [[slnc 300]] Now "
            "look at the top of the class. Create courier is abstract. It has no "
            "body. So the parent class has written a call that it cannot answer "
            "itself. [[slnc 300]] And notice that ship is marked final. A "
            "subclass may change which courier gets used, and nothing else. Not "
            "the guard. Not the logging. Not the order of the steps."
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
            "And here's an entire delivery tier. Six lines. [[slnc 250]] It picks "
            "a courier, it names itself, and that's all it does. All four tiers "
            "look exactly like this. [[slnc 300]] Now go and search the whole "
            "project for the word switch. There isn't one. Search for an if "
            "statement testing a tier name. There isn't one of those either. "
            "[[slnc 300]] The decision that used to be a branch is now a class. "
            "And choosing a class is something Java's own method dispatch does "
            "for us, for free."
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
            "So what did that actually buy us? [[slnc 250]] Monday's drone "
            "delivery is now a new file, and we never touch an existing class. "
            "That's the Open Closed Principle genuinely satisfied, not just "
            "talked about. [[slnc 250]] The weight guard is written once, and it "
            "protects every tier that will ever exist, including ones written "
            "next year, by somebody else. A separate team can ship a tier in "
            "their own jar. And if a subclass forgets to override the factory "
            "method, it won't even compile. [[slnc 350]] Now compare that to its "
            "simpler cousin. A simple factory moves the switch into one file. A "
            "factory method removes the switch entirely."
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
            "When we run the project, you can watch it happen. Here are two of "
            "the four tiers, shipping the very same order. [[slnc 250]] Look at "
            "the first and last line of each block. Same shape, same wording, "
            "same workflow. [[slnc 250]] Only the middle line, the one the "
            "carrier itself printed, is different. And so are the price and the "
            "delivery date. [[slnc 300]] That's the pattern working. One shared "
            "workflow, running completely different carriers."
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
            "So, to recap. Use a factory method when you've got a workflow that's "
            "shared, with one step that varies, and that step creates an object. "
            "[[slnc 300]] Keep the return type abstract. The moment your creator "
            "says it returns an air courier, all that coupling you just removed "
            "comes straight back. [[slnc 250]] Never call the factory method from "
            "a constructor, because the subclass fields aren't ready yet. [[slnc "
            "300]] And be honest with yourself. If the only difference between "
            "your subclasses is one call to new, then a plain supplier passed "
            "into the constructor may be all you need. Don't go building a "
            "hierarchy just to avoid a two line switch. [[slnc 350]] And if you "
            "remember one sentence from today, make it this one. A simple factory "
            "chooses with a switch. A factory method chooses with inheritance."
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
            "And that's the factory method. [[slnc 300]] If you got something out "
            "of this, do give it a thumbs up, and subscribe. It genuinely helps "
            "the channel, and it's what makes more of these possible. [[slnc "
            "250]] And if there's a pattern you'd like me to cover next, drop it "
            "in the comments. I read every one. [[slnc 250]] All the source code, "
            "the written notes and an interactive animation are in the "
            "repository. Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
