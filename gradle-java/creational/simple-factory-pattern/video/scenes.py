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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Simple Factory pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A simple factory is one '
            'place that decides which class to create. [[slnc 400]] '
            'Instead of every caller choosing a class for itself, callers '
            'hand over a piece of data, like a name or a code. [[slnc '
            '300]] And they get back an object, behind an interface they '
            'already know. [[slnc 300]] The decision is made once, in one '
            'file, instead of everywhere. [[slnc 600]] Think of a coffee '
            'shop counter. [[slnc 300]] You say, a cappuccino, please, '
            'and one arrives. [[slnc 300]] You never go behind the '
            'counter to make it yourself. [[slnc 700]] In this video, we '
            'build the payment step of an online store. [[slnc 500]] By '
            'the end, you will know what a factory is, why it exists, and '
            'how to write one yourself.'
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
            'Here is the scenario. [[slnc 400]] A customer reaches the '
            'payment page, and chooses how to pay. [[slnc 500]] Our code '
            'must then run one of four things. [[slnc 300]] A credit card '
            "payment. [[slnc 200]] A U P I payment, which is India's "
            'instant bank transfer. [[slnc 200]] A PayPal payment. [[slnc '
            '200]] Or net banking. [[slnc 600]] And here is the key '
            'detail. [[slnc 300]] That choice arrives as data. [[slnc '
            '300]] From a drop-down list, a web request, or a database. '
            '[[slnc 300]] It is a piece of text, or an enum value. [[slnc '
            '300]] Not a Java class.'
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
            'All four payment methods do the same job, from the outside. '
            '[[slnc 300]] They take a payment request, and return a '
            'receipt. [[slnc 500]] So they share one interface, called '
            'Payment Method, with two methods. [[slnc 300]] One gives its '
            'display name. [[slnc 300]] The other takes the payment. '
            '[[slnc 500]] Inside, they are completely different. [[slnc '
            '300]] The card payment authorises, and then captures the '
            'money. [[slnc 300]] The U P I payment sends a collect '
            'request, and waits for approval. [[slnc 500]] But from the '
            'outside, they are interchangeable. [[slnc 300]] And that '
            'makes everything else in this video possible.'
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
            'Here is the problem. [[slnc 400]] Without a factory, every '
            'piece of code that needs a payment method chooses one for '
            'itself. [[slnc 500]] A chain of if statements checks the '
            'payment type, and creates the matching class. [[slnc 300]] '
            'That chain lives inside the checkout code. [[slnc 300]] The '
            'website has a copy. [[slnc 200]] The mobile app has a copy. '
            '[[slnc 200]] The admin tool has a copy. [[slnc 500]] The '
            'same fragile block, written three times, by three people, on '
            'three different days.'
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
            'And that does real damage. [[slnc 500]] The checkout code '
            'now knows the name of every payment class in the system. '
            '[[slnc 400]] When wallet payments arrive next month, every '
            'copy must be found and edited. [[slnc 300]] Miss one, and it '
            'fails in front of a customer. [[slnc 500]] One copy trims '
            'extra spaces from the input. [[slnc 300]] Another forgets. '
            '[[slnc 500]] And you cannot test the choosing on its own, '
            'because it is welded to the checkout code around it.'
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
            'The simple factory fixes exactly this. [[slnc 400]] It puts '
            'the decision about which class to create into one method. '
            '[[slnc 300]] So callers can ask for an object by name, '
            'instead of building it themselves. [[slnc 500]] One quick '
            'note, because this confuses everybody at first. [[slnc 300]] '
            'The simple factory is not one of the twenty-three Gang of '
            'Four patterns. [[slnc 300]] It is an everyday idiom, the one '
            'everybody actually writes. [[slnc 300]] And it is the '
            'natural first step towards the other creational patterns. '
            '[[slnc 500]] In plain words: one place that knows how to '
            'make things.'
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
            'Here is an easy way to remember it: a coffee shop. [[slnc '
            '500]] You do not walk behind the counter, find the espresso '
            'machine, grind the beans, and steam the milk. [[slnc 300]] '
            'You say, a cappuccino, please. [[slnc 300]] And a cappuccino '
            'arrives. [[slnc 500]] You named what you wanted. [[slnc '
            '300]] Someone else knew how to make it. [[slnc 500]] And '
            'tomorrow, when the shop buys a better machine, your order '
            'does not change at all. [[slnc 300]] Because you never knew '
            'how it was made. [[slnc 500]] The counter is the factory.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            'Every factory has four roles. [[slnc 500]] First, the '
            'product: the Payment Method interface. [[slnc 300]] Second, '
            'the concrete products: the four payment classes. [[slnc '
            '300]] Third, the factory itself: the Payment Method Factory. '
            '[[slnc 300]] And fourth, the client: the code that simply '
            'wants to take a payment. [[slnc 600]] Now the most important '
            'idea in the whole video. [[slnc 300]] The client names the '
            'payment type, as data. [[slnc 300]] The factory names the '
            'class. [[slnc 500]] Search the client code for the words '
            'credit card payment. [[slnc 300]] You will not find them '
            'anywhere. [[slnc 300]] That is how you know the pattern has '
            'really been applied.'
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
            "Let's look at one product: the U P I payment. [[slnc 400]] "
            'Notice how small, and ordinary, it is. [[slnc 300]] It gives '
            'its display name, and it takes the payment. [[slnc 300]] '
            'That is all. [[slnc 500]] It has no idea a factory exists. '
            '[[slnc 300]] That is deliberate. [[slnc 300]] Because it '
            'knows nothing about who created it, you could move this '
            'class into a completely different application tomorrow. '
            '[[slnc 500]] The other three payment methods follow exactly '
            'the same shape.'
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
            'And here is the factory itself. [[slnc 300]] One static '
            'method, called create, with one switch statement. [[slnc '
            '500]] It is now the only place in the whole codebase that '
            'creates a payment class. [[slnc 600]] Notice something '
            'missing from that switch. [[slnc 300]] There is no default '
            'branch. [[slnc 300]] And that is on purpose. [[slnc 500]] '
            'The payment type is an enum, and the Payment Method '
            'interface is sealed. [[slnc 300]] So the compiler knows the '
            'complete list of cases. [[slnc 300]] Add a fifth payment '
            'type tomorrow, and this file will not compile until you '
            'handle it. [[slnc 500]] A forgotten case becomes a build '
            'error, instead of a customer complaint.'
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
            'So the factory gives us three things. [[slnc 500]] It '
            'chooses the class from data, in exactly one place. [[slnc '
            '300]] It creates the object, so no caller ever writes new. '
            '[[slnc 300]] And it checks the input, so every caller gets '
            "the same error message. [[slnc 600]] Now, let's be honest "
            'about the cost. [[slnc 300]] Adding a new payment method '
            'means editing the factory. [[slnc 300]] That breaks the Open '
            'Closed Principle, which says code should be open to '
            'extension, but closed to modification. [[slnc 500]] The '
            'simple factory does not remove that cost. [[slnc 300]] It '
            'just moves it into one file you can actually find.'
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
            'And now, the payoff: the client code. [[slnc 500]] One line '
            'asks the factory for a payment method. [[slnc 300]] After '
            'that, it is ordinary, everyday polymorphism. [[slnc 500]] '
            'The checkout does not know that PayPal exists. [[slnc 300]] '
            'It does not know net banking exists. [[slnc 300]] It holds a '
            'Payment Method, and simply calls pay. [[slnc 500]] Add a '
            'fifth payment method tomorrow, and this code does not change '
            'at all. [[slnc 300]] That is the whole point of the pattern.'
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
            "Let's run the demo. [[slnc 400]] Two of the four payments "
            'run, for the same order. [[slnc 500]] Listen to the '
            "checkout's lines, the first and the last of each payment. "
            '[[slnc 300]] They are identical. [[slnc 300]] Paying with, '
            'and then, done. [[slnc 500]] Only the lines in between are '
            'different. [[slnc 300]] The card authorises and captures. '
            '[[slnc 300]] The U P I payment sends a collect request, and '
            'the customer approves it. [[slnc 500]] The same client code, '
            'running completely different payment methods, chosen by '
            'nothing more than a value.'
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
            'So, to recap. [[slnc 400]] Use a simple factory when the '
            'class you need is decided by data. [[slnc 300]] And when '
            'callers should not care how it is built. [[slnc 500]] Keep '
            'the factory thin. [[slnc 300]] Its job is to choose, and to '
            'create. [[slnc 300]] Nothing else. [[slnc 500]] If there is '
            'only one implementation, just use new. [[slnc 300]] It is '
            'clearer. [[slnc 300]] And if you ever reach forty cases, use '
            'a registry instead. [[slnc 600]] And one sentence to '
            'remember. [[slnc 300]] A simple factory chooses with a '
            'switch. [[slnc 300]] A factory method chooses with '
            'inheritance.'
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
            "That's the Simple Factory pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Put '
            'the choice of which class to create in one place, and let '
            'callers ask for it by name. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] If there is a '
            'pattern you would like to see covered, suggest it in the '
            'comments. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
