"""Scene definitions for the Facade pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "title" | "bullets" | "code" | "console" | "diagram"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="The Facade Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Facade pattern in Java, "
            "and it is written and presented by Jayasekhar Konduru. [[slnc 300]] "
            "Let's start with the simple definition. The facade pattern puts one "
            "simple interface in front of a complicated set of classes. The "
            "subsystem keeps every one of its parts, and the specialist can still "
            "reach them, but the ordinary caller talks to a single object with a "
            "single method instead of orchestrating six. [[slnc 350]] That's the "
            "idea in a sentence, and it's one of the most useful and most "
            "approachable patterns in software. The rest of the video does it "
            "properly, by building a real working Java project: the checkout of "
            "an online store. [[slnc 250]] By the end you'll know what a facade "
            "is, why it exists, and how to write one yourself."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "A customer clicks “Place Order”.",
            "",
            "Behind that one click, four things must happen:",
            "  1.  Reserve the stock",
            "  2.  Charge the customer's card",
            "  3.  Schedule the shipment",
            "  4.  Email a confirmation",
        ],
        narration=(
            "So, imagine you're building an online store. A customer fills up "
            "their basket, and clicks the place order button. [[slnc 250]] Now "
            "that one click looks simple from the outside. But behind the scenes, "
            "four different things have to happen. [[slnc 250]] We reserve the "
            "stock, so nobody else buys the last item. We charge the customer's "
            "card. We schedule the shipment with the warehouse. And finally, we "
            "email the customer a confirmation."
        ),
    ),
    dict(
        key="03-services",
        kind="bullets",
        title="Four Separate Services",
        body=[
            "InventoryService        reserves the stock",
            "PaymentService          charges the card, returns a payment id",
            "ShippingService         books delivery, returns a tracking id",
            "NotificationService     sends the confirmation email",
            "",
            "Each one is small, focused, and does its job well.",
        ],
        narration=(
            "In our project, each of those four jobs lives in its own class. "
            "[[slnc 250]] The Inventory Service reserves the stock. The Payment "
            "Service charges the card, and gives us back a payment identifier. "
            "The Shipping Service books the delivery, and gives us a tracking "
            "number. And the Notification Service sends the confirmation email. "
            "[[slnc 250]] Each one is small, focused, and does its own job well."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Problem — Everyone Wires It Up Themselves",
        body="""InventoryService inventory = new InventoryService();
PaymentService payment = new PaymentService();
ShippingService shipping = new ShippingService();
NotificationService notification = new NotificationService();

if (!inventory.reserveStock(productId, quantity)) {
    throw new IllegalStateException("Out of stock");
}
String paymentId = payment.charge(customerId, amount);
String trackingId = shipping.scheduleShipment(orderId, address);
notification.sendOrderConfirmation(customerId, orderId, trackingId);

//  ...repeated in the website, the mobile app, the admin tool""",
        narration=(
            "So here's the problem. [[slnc 250]] Without a facade, every single "
            "part of our application that wants to place an order has to know "
            "about all four of these services. It has to create them, call them "
            "in exactly the right order, and carry the results from one across to "
            "the next. [[slnc 300]] Our website does this. The mobile app does "
            "this. The admin tool does this. The same fragile code, copied into "
            "three places."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   Callers must learn four classes to place one order",
            "✗   The order is easy to get wrong — charge before stock check",
            "✗   Add a fifth step, and every caller must change",
            "✗   The same code is duplicated and drifts out of sync",
            "✗   Testing one order needs four collaborators",
        ],
        narration=(
            "And that does real damage. [[slnc 250]] New developers have to learn "
            "four classes just to place one order. The ordering is easy to get "
            "wrong, and getting it wrong means charging a customer for something "
            "we can't actually ship. [[slnc 300]] When we add a fifth step "
            "tomorrow, we're editing every caller. And testing gets painful, "
            "because a simple order needs four collaborators standing up, every "
            "single time."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Facade Pattern",
        body=[
            "“Provides a simplified, unified interface to a set",
            "of interfaces in a subsystem, making the subsystem",
            "easier to use.”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "one simple front door to a complicated building.",
        ],
        narration=(
            "The facade fixes exactly this. [[slnc 250]] And the definition is "
            "short. A facade provides a simplified, unified interface to a set of "
            "interfaces in a subsystem, making that subsystem easier to use. "
            "[[slnc 300]] In plain language? It gives you one simple front door, "
            "to a complicated building."
        ),
    ),
    dict(
        key="07-waiter",
        kind="bullets",
        title="Remember It With a Waiter",
        body=[
            "You don't walk into the kitchen and brief",
            "the grill chef, the sauce chef and the pastry chef.",
            "",
            "You tell one person — the waiter —",
            "“I'll have the steak.”",
            "",
            "The chefs still exist. You are simply",
            "protected from the complexity.",
            "",
            "The waiter is a facade.",
        ],
        narration=(
            "Here's how to remember it forever. Think about a restaurant. [[slnc "
            "250]] You don't walk into the kitchen and talk to the grill chef, "
            "and then the sauce chef, and then the pastry chef. You talk to one "
            "person. The waiter. And you say, I'll have the steak. [[slnc 300]] "
            "The waiter knows which chefs to speak to, in what order, and what to "
            "bring back to you. [[slnc 250]] The chefs still exist. They're still "
            "doing skilled, specialised work. You're simply protected from all "
            "that complexity. [[slnc 200]] The waiter is a facade."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Three Roles",
        body=None,
        narration=(
            "Every facade has three roles. [[slnc 200]] First, the facade itself, "
            "which here is the Order Facade class. Second, the subsystems, which "
            "are our four services. And third, the client. The code that just "
            "wants to place an order. [[slnc 350]] Now here's the single most "
            "important idea in this whole video. The facade knows about the "
            "subsystems. But the subsystems never know about the facade. [[slnc "
            "250]] That arrow points one way only. And that's what keeps each "
            "service independently reusable."
        ),
    ),
    dict(
        key="09-subsystem",
        kind="code",
        title="A Subsystem — Small, Focused, Unaware",
        body="""public class InventoryService {

    public boolean reserveStock(String productId, int quantity) {
        System.out.println("Inventory: reserving "
                + quantity + " unit(s) of " + productId);
        return true;
    }
}

//  It has no idea a facade exists.
//  You could reuse it in a different application tomorrow.""",
        narration=(
            "Let's look at some code. This is the Inventory Service. [[slnc 250]] "
            "Notice how small it is. How ordinary. It reserves stock, and it "
            "returns whether that worked. That's all. It has absolutely no idea a "
            "facade exists. [[slnc 300]] Which is deliberate. Because it knows "
            "nothing about the bigger workflow, you could lift this class into a "
            "completely different application tomorrow. [[slnc 200]] The other "
            "three services follow exactly the same shape."
        ),
    ),
    dict(
        key="10-facade",
        kind="code",
        title="The Facade — One Method, Four Subsystems",
        body="""public class OrderFacade {

    private final InventoryService inventoryService;
    private final PaymentService paymentService;
    private final ShippingService shippingService;
    private final NotificationService notificationService;

    public OrderConfirmation placeOrder(OrderRequest request) {

        if (!inventoryService.reserveStock(productId, quantity)) {
            throw new IllegalStateException("Out of stock");
        }

        String paymentId  = paymentService.charge(customerId, amount);
        String trackingId = shippingService.scheduleShipment(orderId, address);
        notificationService.sendOrderConfirmation(customerId, orderId, trackingId);

        return new OrderConfirmation(orderId, paymentId, trackingId);
    }
}""",
        narration=(
            "And this is the facade itself. [[slnc 250]] It holds the four "
            "services as private fields, and it exposes just one method. Place "
            "order. [[slnc 300]] Now look at what that method is really doing. It "
            "reserves the stock first. And if that fails, it stops immediately, "
            "so the customer is never charged for something we can't ship. [[slnc "
            "250]] Only then does it take the payment. Then it schedules the "
            "shipment. Then it sends the email. And finally it packages those "
            "three results into one confirmation object, and hands it back."
        ),
    ),
    dict(
        key="11-provides",
        kind="bullets",
        title="What the Facade Gives You",
        body=[
            "✓   Sequencing    —  the right calls, in the right order, in one place",
            "✓   A guard rail  —  no payment unless stock was secured",
            "✓   Assembly      —  three results gathered into one clean object",
            "",
            "And notice what is missing: business logic.",
            "",
            "A facade delegates. It does not decide.",
            "Keep it thin.",
        ],
        narration=(
            "So the facade is giving us three things. [[slnc 200]] It gives us "
            "sequencing. The right calls, in the right order, defined in exactly "
            "one place. It gives us a guard rail. No payment, unless the stock "
            "was secured. And it gives us assembly. Three separate results, "
            "gathered into one clean object. [[slnc 350]] Now notice what it "
            "doesn't contain. There's almost no business logic in here at all. A "
            "facade delegates. It doesn't decide. [[slnc 250]] Keep it thin, and "
            "it stays a facade, rather than turning into one of those giant "
            "tangled classes we've all met."
        ),
    ),
    dict(
        key="12-client",
        kind="code",
        title="The Client — This Is the Whole Thing",
        body="""OrderFacade orderFacade = new OrderFacade();

OrderRequest request = new OrderRequest(
        "CUST-001", "SKU-1234", 2, 49.98, "221B Baker Street, London");

OrderConfirmation confirmation = orderFacade.placeOrder(request);


//  No knowledge of inventory, payment, shipping or email.
//  Add a fraud check to the facade tomorrow
//  and this code does not change at all.""",
        narration=(
            "And now, the payoff. This is the entire client code. Three lines. "
            "[[slnc 250]] We create the facade, we build a request, and we place "
            "the order. [[slnc 300]] Our client doesn't know that payments exist. "
            "It doesn't know shipping exists. And if we add a fraud check to the "
            "facade tomorrow, this code doesn't change at all. [[slnc 250]] "
            "That's the whole point of the pattern."
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

Inventory: reserving 2 unit(s) of SKU-1234
Payment: charged $49.98 to customer CUST-001 (paymentId=PMT-C68994F4)
Shipping: scheduled shipment for order ORD-0D1ADD0C
          to 221B Baker Street, London (trackingId=TRK-A844891E)
Notification: emailed customer CUST-001 confirmation for
          order ORD-0D1ADD0C (trackingId=TRK-A844891E)

Order placed: OrderConfirmation[orderId=ORD-0D1ADD0C,
          paymentId=PMT-C68994F4, trackingId=TRK-A844891E]""",
        narration=(
            "When we run the project, you can watch it happen. [[slnc 250]] Each "
            "line of output comes from a different service, in the exact order "
            "the facade arranged. Stock reserved. Card charged. Shipment "
            "scheduled. Email sent. [[slnc 300]] And at the end, one single "
            "confirmation returned to the client. [[slnc 250]] One call in. One "
            "result out. And four subsystems quietly coordinated in between."
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use a facade when classes must be used together",
            "in a particular way, and callers shouldn't care.",
            "",
            "Keep the facade thin.",
            "Keep the subsystems public and independent.",
            "A facade is a convenience, not a wall.",
            "",
            "Remember one sentence:",
            "An Adapter changes an interface.",
            "A Facade simplifies many of them.",
        ],
        narration=(
            "So, to recap. Use a facade when a group of classes has to be used "
            "together in a particular way, and you want to spare your callers all "
            "that complexity. [[slnc 300]] Keep the facade thin. Keep the "
            "subsystems public and independent. And remember that a facade is a "
            "convenience, not a wall. [[slnc 350]] And if you remember one "
            "sentence from today, make it this one. An adapter changes an "
            "interface. A facade simplifies many of them."
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
            "And that's the facade pattern. [[slnc 300]] If you got something out "
            "of this, do give it a thumbs up, and subscribe. It genuinely helps "
            "the channel, and it's what makes more of these possible. [[slnc "
            "250]] And if there's a pattern you'd like me to cover next, drop it "
            "in the comments. I read every one. [[slnc 250]] All the source code, "
            "the written notes and an interactive animation are in the "
            "repository. Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
