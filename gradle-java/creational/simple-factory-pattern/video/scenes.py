"""Scene definitions for the Simple Factory pattern teaching video.

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
        title="The Simple Factory Pattern",
        body=["A beginner's guide, in Java 21",
              "Learn it by building an online store checkout"],
        narration=(
            "Hello, and welcome. In this short video we are going to learn the pattern "
            "that almost every Java developer writes before they know it has a name: "
            "the Simple Factory. We will learn it by building a real, working Java "
            "project, the payment step of an online store. By the end you will know what "
            "a factory is, why it exists, and how to write one yourself."
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
            "Imagine you are building an online store. A customer reaches the payment "
            "page and chooses how they want to pay. Your code now has to run one of four "
            "things: a credit card payment, a U P I payment, a pay pal payment, or net "
            "banking. And here is the important detail. That choice arrives as data. It "
            "comes from a dropdown, or a JSON field, or a database column. It is a string "
            "or an enum. It is not a Java type."
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
            "In our project all four do the same job from the outside. They take a "
            "payment request and give back a payment receipt. So they share one "
            "interface, called Payment Method, with two methods on it. Inside, they are "
            "completely different. The card one authorises and then captures. The U P I "
            "one sends a collect request and waits. But from the outside they are "
            "interchangeable, and that is what makes everything else possible."
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
            "So here is the problem. Without a factory, whoever needs a payment method "
            "decides for themselves. This chain of if and else lives inside the checkout "
            "code. Our website has a copy. Our mobile app has a copy. Our admin tool has "
            "a copy. The same fragile block, written three times, by three people, on "
            "three different days."
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
            "This causes real damage. A class whose only job is to check out now knows "
            "the name of every payment class in the system. When we add wallet payments "
            "next month, we have to find every caller and edit it, and if we miss one it "
            "fails in front of a customer. One copy trims the input string, another "
            "forgets. And you cannot test the choosing logic on its own, because it is "
            "welded to the checkout code around it."
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
            "The Simple Factory solves exactly this. It puts the decision of which class "
            "to instantiate into one method, so callers can ask for an object by name "
            "instead of building it themselves. One quick note, because it confuses "
            "everybody at first. Simple Factory is not one of the twenty three Gang of "
            "Four patterns. It is an idiom, the one everybody actually writes, and it is "
            "the natural first step towards the real creational patterns. In plain "
            "language, it is one place that knows how to make things."
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
            "Here is the way to remember it forever. Think about a coffee shop. You do "
            "not walk behind the counter, find the espresso machine, grind the beans and "
            "steam the milk. You say, a cappuccino please, and a cappuccino arrives. You "
            "named what you wanted. Somebody else knew how to make it. And tomorrow, when "
            "the shop buys a better machine, your order does not change at all, because "
            "you never knew how it was made. The counter is the factory."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            "Every factory has four roles. First, the product, which is our Payment "
            "Method interface. Second, the concrete products, our four payment classes. "
            "Third, the factory itself, which in our project is the Payment Method "
            "Factory. And fourth, the client, the code that just wants to take a payment. "
            "Now here is the single most important idea in this whole video. The client "
            "names the type as data. The factory names the class. Search the client for "
            "the words credit card payment and you will not find them anywhere. That is "
            "the test of whether you have applied the pattern correctly."
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
            "Let's look at some code. This is the U P I payment. Notice how small and "
            "how ordinary it is. It gives its display name, and it takes the payment. It "
            "has absolutely no idea that a factory exists. That is deliberate. Because it "
            "knows nothing about who created it, you could lift this class into a "
            "completely different application tomorrow. The other three payment methods "
            "follow exactly the same shape."
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
            "And this is the factory itself. One static method, one switch. This is now "
            "the only place in the entire codebase that calls new on a payment class. "
            "Look carefully at that switch, because there is something missing. There is "
            "no default branch. That is deliberate. Payment Type is an enum and Payment "
            "Method is a sealed interface, so the compiler knows the complete list, and "
            "it knows this switch covers every case. Add a fifth payment type tomorrow, "
            "and this file stops compiling until you handle it. A forgotten case becomes "
            "a build error instead of a customer complaint."
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
            "So the factory is giving us three things. It chooses the implementation "
            "from data, in exactly one place. It constructs it, so no caller ever writes "
            "new. And it validates the input, so every caller gets the same error "
            "message. Now let's be honest about the cost, because every good teacher "
            "should be. Adding a new payment method means modifying the factory. That "
            "breaks the Open Closed Principle, which says code should be open to "
            "extension but closed to modification. The Simple Factory does not remove "
            "that cost. It centralises it, into one file you can find."
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
            "And now the payoff. This is the entire client code. One line to obtain the "
            "object, and then ordinary, everyday polymorphism. Our checkout does not know "
            "that pay pal exists. It does not know that net banking exists. It holds "
            "something typed as Payment Method and it simply calls pay. If we add a fifth "
            "payment method tomorrow, this code does not change at all. That is the whole "
            "point of the pattern."
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
            "When we run the project, we can watch it happen. Here are two of the four "
            "payments. Look at the checkout lines, the first and the last of each block. "
            "They are identical. Only the middle lines, the ones the payment method "
            "itself printed, are different. That is the pattern working. The same client "
            "code, running completely different implementations, chosen by nothing more "
            "than a value."
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
            "So, to recap. Use a Simple Factory when the class you need is decided by "
            "data, and you want to spare your callers from knowing how it is built. Keep "
            "the factory thin. Its job is to choose and construct, nothing else. If you "
            "only have one implementation, plain new is clearer, so do not invent a "
            "factory for its own sake. And if you ever reach forty cases, reach for a "
            "registry instead. If you remember just one sentence from today, make it "
            "this one: a Simple Factory chooses with a switch, and a Factory Method "
            "chooses with inheritance. That second one is where you go next. Thank you "
            "for watching, and enjoy building your own factories."
        ),
    ),
]
