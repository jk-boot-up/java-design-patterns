"""Scene definitions for the Simple Factory pattern teaching video.

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
        title="The Simple Factory Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Simple Factory pattern "
            "in Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. A simple "
            "factory is one place that decides which class to create. Rather than "
            "every caller writing new and choosing a type for itself, callers "
            "hand over a piece of data — a name, a code, a setting — and get back "
            "an object behind an interface they already know. The decision is "
            "made once, in one file, instead of everywhere. [[slnc 350]] That's "
            "the idea in a sentence, and it's the pattern almost every Java "
            "developer writes long before they learn it has a name. The rest of "
            "the video does it properly, by building a real working Java project: "
            "the payment step of an online store. [[slnc 250]] By the end you'll "
            "know what a factory is, why it exists, and how to write one "
            "yourself."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "A customer reaches the payment page and picks how to pay.",
            "",
            "Our code has to run one of four things:",
            "  1.  Credit card",
            "  2.  U P I",
            "  3.  PayPal",
            "  4.  Net banking",
            "",
            "And the choice arrives as data — a string, or an enum.",
        ],
        narration=(
            "So, imagine you are building an online store. A customer gets to the "
            "payment page, and picks how they want to pay. [[slnc 250]] Now your "
            "code has to run one of four things. A credit card payment. A U P I "
            "payment. A pay pal payment. Or net banking. [[slnc 300]] And here's "
            "the detail that matters. That choice arrives as data. It comes from "
            "a dropdown, or a JSON field, or a database column. It's a string, "
            "or an enum. It's not a Java type."
        ),
    ),
    dict(
        key="03-products",
        kind="bullets",
        title="One Interface, Four Implementations",
        body=[
            "interface PaymentMethod",
            "        displayName()   ·   pay(request)",
            "",
            "CreditCardPayment       authorise, then capture",
            "UpiPayment              collect request, then approval",
            "PayPalPayment           redirect, then return",
            "NetBankingPayment       bank login, then transfer",
            "",
            "From the outside they are interchangeable.",
        ],
        narration=(
            "In our project, all four of them do the same job from the outside. "
            "They take a payment request, and they give you back a receipt. So "
            "they share one interface, called Payment Method, with two methods on "
            "it. [[slnc 300]] Inside, though, they're completely different. The "
            "card one authorises, and then captures. The U P I one sends a "
            "collect request, and waits. [[slnc 250]] But from the outside? "
            "Interchangeable. And that's what makes everything else in this "
            "video possible."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Problem — Everyone Chooses for Themselves",
        body="""PaymentMethod method;

if (type.equals("CREDIT_CARD")) {
    method = new CreditCardPayment();
} else if (type.equals("UPI")) {
    method = new UpiPayment();
} else if (type.equals("PAYPAL")) {
    method = new PayPalPayment();
} else if (type.equals("NET_BANKING")) {
    method = new NetBankingPayment();
} else {
    throw new IllegalArgumentException("Unknown type");
}

//  ...repeated in the website, the mobile app, the admin tool""",
        narration=(
            "Right, so here's the problem. Without a factory, whoever needs a "
            "payment method decides for themselves. [[slnc 250]] This chain of if "
            "and else lives inside the checkout code. And our website has a copy "
            "of it. The mobile app has a copy. The admin tool has a copy. [[slnc "
            "300]] The same fragile block, written out three times, by three "
            "people, on three different days."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   The checkout code knows every payment class by name",
            "✗   Add a fifth method — hunt down every caller",
            "✗   Miss one, and it fails in front of a customer",
            "✗   One copy trims the input, another forgets",
            "✗   You cannot test the choosing on its own",
        ],
        narration=(
            "And that does real damage. [[slnc 250]] A class whose only job is to "
            "check out now knows the name of every single payment class in the "
            "system. When we add wallet payments next month, we've to go and "
            "find every caller and edit it. And if we miss one, it fails in front "
            "of a customer. [[slnc 300]] One copy trims the input string. Another "
            "one forgets. And you can't test the choosing on its own, because it "
            "is welded to the checkout code around it."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Simple Factory",
        body=[
            "“Put the decision of which class to instantiate",
            "into one method, so callers can ask for an object",
            "by name instead of building it themselves.”",
            "",
            "—  not a Gang of Four pattern; an idiom everyone writes",
            "",
            "In plain language:",
            "one place that knows how to make things.",
        ],
        narration=(
            "The simple factory fixes exactly this. It takes the decision of "
            "which class to instantiate, and puts it into one method, so callers "
            "can ask for an object by name instead of building it themselves. "
            "[[slnc 300]] One quick note, because this confuses everybody at "
            "first. Simple factory isn't one of the twenty three Gang of Four "
            "patterns. It's an idiom. It's the one everybody actually writes. "
            "And it's the natural first step towards the real creational "
            "patterns. [[slnc 250]] In plain language? It's one place that knows "
            "how to make things."
        ),
    ),
    dict(
        key="07-coffee",
        kind="bullets",
        title="Remember It With a Coffee Shop",
        body=[
            "You don't walk behind the counter, find the machine,",
            "grind the beans and steam the milk.",
            "",
            "You say — “a cappuccino, please” —",
            "and a cappuccino arrives.",
            "",
            "Tomorrow they buy a better machine.",
            "Your order does not change.",
            "",
            "The counter is the factory.",
        ],
        narration=(
            "Here's how to remember it forever. Think about a coffee shop. "
            "[[slnc 250]] You don't walk behind the counter, find the espresso "
            "machine, grind the beans and steam the milk. You say, a cappuccino "
            "please. And a cappuccino arrives. [[slnc 300]] You named what you "
            "wanted. Somebody else knew how to make it. And tomorrow, when the "
            "shop buys a better machine, your order doesn't change one bit. "
            "Because you never knew how it was made in the first place. [[slnc "
            "250]] The counter is the factory."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            "Every factory has four roles. [[slnc 200]] First, the product, which "
            "is our Payment Method interface. Second, the concrete products, "
            "which are our four payment classes. Third, the factory itself, which "
            "here's the Payment Method Factory. And fourth, the client. The code "
            "that just wants to take a payment. [[slnc 350]] Now this next bit's "
            "the single most important idea in the whole video, so stay with me. "
            "The client names the type, as data. The factory names the class. "
            "[[slnc 250]] Go and search the client for the words credit card "
            "payment. You'll not find them anywhere. That's the test of "
            "whether you have actually applied the pattern."
        ),
    ),
    dict(
        key="09-product",
        kind="code",
        title="A Product — Small, Focused, Unaware",
        body="""public final class UpiPayment implements PaymentMethod {

    public String displayName() {
        return "UPI";
    }

    public PaymentReceipt pay(PaymentRequest request) {
        System.out.println("UPI: sending a collect request...");
        return new PaymentReceipt(newTransactionId(),
                displayName(), request.amount());
    }
}

//  It has no idea a factory exists.""",
        narration=(
            "Let's look at some code. This is the U P I payment. [[slnc 250]] "
            "And notice how small it is. How ordinary. It gives its display name, "
            "and it takes the payment. That's it. It has absolutely no idea a "
            "factory exists. [[slnc 300]] Which is deliberate. Because it knows "
            "nothing about who created it, you could lift this class straight "
            "into a completely different application tomorrow. [[slnc 200]] The "
            "other three payment methods follow exactly the same shape."
        ),
    ),
    dict(
        key="10-factory",
        kind="code",
        title="The Factory — One Switch, One Place",
        body="""public class PaymentMethodFactory {

    public static PaymentMethod create(PaymentType type) {

        if (type == null) {
            throw new IllegalArgumentException("Type must not be null");
        }

        return switch (type) {
            case CREDIT_CARD -> new CreditCardPayment();
            case UPI         -> new UpiPayment();
            case PAYPAL      -> new PayPalPayment();
            case NET_BANKING -> new NetBankingPayment();
        };
    }
}

//  No default branch — and that is deliberate.""",
        narration=(
            "And this is the factory itself. One static method, one switch. "
            "[[slnc 250]] This is now the only place in the entire codebase that "
            "calls new on a payment class. [[slnc 300]] Now look carefully at "
            "that switch, because something is missing. There's no default "
            "branch. And that's on purpose. [[slnc 250]] Payment Type is an "
            "enum, and Payment Method is a sealed interface, so the compiler "
            "knows the complete list, and it knows this switch covers every case. "
            "Add a fifth payment type tomorrow, and this file stops compiling "
            "until you handle it. [[slnc 250]] So a forgotten case becomes a "
            "build error, instead of a customer complaint."
        ),
    ),
    dict(
        key="11-provides",
        kind="bullets",
        title="What the Factory Gives You",
        body=[
            "✓   Choosing     —  from data, in exactly one place",
            "✓   Constructing —  so no caller ever writes new",
            "✓   Validating   —  one error message, everywhere",
            "",
            "And be honest about the cost:",
            "",
            "Adding a product means editing the factory.",
            "That breaks the Open/Closed Principle — on purpose.",
        ],
        narration=(
            "So the factory is giving us three things. It chooses the "
            "implementation from data, in exactly one place. It constructs it, so "
            "no caller ever writes new. And it validates the input, so every "
            "caller gets the same error message. [[slnc 350]] Now, let's be "
            "honest about the cost, because a good teacher always should be. "
            "Adding a new payment method means modifying the factory. And that "
            "breaks the Open Closed Principle, which says code should be open to "
            "extension, but closed to modification. [[slnc 250]] The simple "
            "factory doesn't remove that cost. It just centralises it, into one "
            "file you can actually find."
        ),
    ),
    dict(
        key="12-client",
        kind="code",
        title="The Client — This Is the Whole Thing",
        body="""PaymentMethod method = PaymentMethodFactory.create(type);

System.out.println("Checkout: paying with " + method.displayName());

PaymentReceipt receipt = method.pay(request);


//  One line to get the object. Then ordinary polymorphism.
//  No concrete payment class is named anywhere here.
//  Add a fifth method tomorrow and this does not change.""",
        narration=(
            "And now, the payoff. This is the entire client code. [[slnc 250]] "
            "One line to get hold of the object, and then ordinary, everyday "
            "polymorphism. [[slnc 300]] Our checkout doesn't know that pay pal "
            "exists. It doesn't know net banking exists. It's holding something "
            "typed as Payment Method, and it simply calls pay. [[slnc 250]] Add a "
            "fifth payment method tomorrow, and this code doesn't change at all. "
            "That's the whole point of the pattern."
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

Checkout: paying for ORD-1001 with Credit Card
Credit Card: authorising 49.98 for order ORD-1001
Credit Card: capturing the authorised amount
Checkout: done, transaction CC-AB9DC004

Checkout: paying for ORD-1001 with UPI
UPI: sending a collect request to CUST-001
UPI: customer approved 49.98 in the payments app
Checkout: done, transaction UPI-E89BF12E""",
        narration=(
            "When we run the project, you can watch it happen. Here are two of "
            "the four payments. [[slnc 250]] Look at the checkout lines, the "
            "first and the last of each block. They are identical. Only the "
            "middle lines, the ones the payment method itself printed, are "
            "different. [[slnc 300]] And that's the pattern working. The same "
            "client code, running completely different implementations, chosen by "
            "nothing more than a value."
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use a Simple Factory when the class to create",
            "is decided by data, and callers shouldn't care how.",
            "",
            "Keep the factory thin — it chooses and constructs, nothing else.",
            "With one implementation, plain new is clearer.",
            "With forty, reach for a registry instead.",
            "",
            "Remember one sentence:",
            "Simple Factory chooses with a switch.",
            "Factory Method chooses with inheritance.",
        ],
        narration=(
            "So, to recap. Use a simple factory when the class you need is "
            "decided by data, and you want to spare your callers from knowing how "
            "it gets built. [[slnc 300]] Keep the factory thin. Its job is to "
            "choose, and to construct. Nothing else. [[slnc 250]] If you have "
            "only got one implementation, plain new is clearer, so don't go "
            "inventing a factory for its own sake. And if you ever reach forty "
            "cases, reach for a registry instead. [[slnc 350]] And if you "
            "remember one sentence from today, make it this one. A simple factory "
            "chooses with a switch. A factory method chooses with inheritance. "
            "That second one is where you go next."
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
            "And that's the simple factory. [[slnc 300]] If you got something "
            "out of this, do give it a thumbs up, and subscribe. It genuinely "
            "helps the channel, and it's what makes more of these possible. "
            "[[slnc 250]] And if there's a pattern you'd like me to cover "
            "next, drop it in the comments. I read every one. [[slnc 250]] All "
            "the source code, the written notes and an interactive animation are "
            "in the repository. Thanks for watching, and I will see you in the "
            "next one."
        ),
    ),
]
