"""Scene definitions for the Facade pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "title" | "bullets" | "code" | "console" | "diagram"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    dict(
        key="01-title",
        kind="title",
        title="The Facade Pattern",
        body=["A beginner's guide, in Java 21",
              "Learn it by building an online store checkout"],
        narration=(
            "Hello, and welcome. In this short video we are going to learn one of the "
            "most useful and most approachable design patterns in software: the Facade "
            "pattern. We will learn it by building a real, working Java project, an "
            "online store checkout. By the end you will know what a facade is, why it "
            "exists, and how to write one yourself."
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
            "Imagine you are building an online store. A customer fills their basket "
            "and clicks the Place Order button. That one click looks simple from the "
            "outside, but behind the scenes four different things have to happen. We "
            "reserve the stock, so nobody else buys the last item. We charge the "
            "customer's card. We schedule the shipment with the warehouse. And finally "
            "we email the customer a confirmation."
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
            "In our project, each of those four jobs lives in its own class. The "
            "Inventory Service reserves stock. The Payment Service charges the card and "
            "gives us back a payment identifier. The Shipping Service books the delivery "
            "and gives us a tracking number. And the Notification Service sends the "
            "confirmation email. Each one is small, focused, and does its job well."
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
            "So here is the problem. Without a facade, every single part of our "
            "application that wants to place an order has to know about all four of "
            "these services. It has to create them, call them in exactly the right "
            "order, and carry results from one to the next. Our website does this. Our "
            "mobile app does this. Our admin tool does this. The same fragile code, "
            "copied in three places."
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
            "This causes real damage. New developers have to learn four classes just to "
            "place one order. The ordering is easy to get wrong, and getting it wrong "
            "means charging a customer for something we cannot ship. When we add a fifth "
            "step tomorrow, we have to edit every caller. And testing becomes painful, "
            "because a simple order needs four collaborators standing up every time."
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
            "The Facade pattern solves exactly this. The definition is short: a facade "
            "provides a simplified, unified interface to a set of interfaces in a "
            "subsystem, making that subsystem easier to use. In plain language, it gives "
            "you one simple front door to a complicated building."
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
            "Here is the way to remember it forever. Think about a restaurant. You do "
            "not walk into the kitchen and talk to the grill chef, then the sauce chef, "
            "then the pastry chef. You talk to one person, the waiter, and you say, I "
            "will have the steak. The waiter knows which chefs to speak to, in what "
            "order, and what to bring back to you. The chefs still exist. They still do "
            "skilled, specialised work. You are simply protected from that complexity. "
            "The waiter is a facade."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Three Roles",
        body=None,
        narration=(
            "Every facade has three roles. First, the facade itself, which in our "
            "project is the Order Facade class. Second, the subsystems, which are our "
            "four services. And third, the client, the code that just wants to place an "
            "order. Now here is the single most important idea in this whole video. The "
            "facade knows about the subsystems. But the subsystems never know about the "
            "facade. That arrow points one way only, and that is what keeps each service "
            "independently reusable."
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
            "Let's look at some code. This is the Inventory Service. Notice how small "
            "and how ordinary it is. It reserves stock, and it returns whether that "
            "succeeded. It has absolutely no idea that a facade exists. That is "
            "deliberate. Because it knows nothing about the bigger workflow, you could "
            "lift this class into a completely different application tomorrow. The other "
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
            "And this is the facade itself. It holds the four services as private "
            "fields, and it exposes just one method: place order. Look at what that "
            "method is really doing. It reserves stock first. If that fails, it stops "
            "immediately, so the customer is never charged for something we cannot ship. "
            "Only then does it take the payment. Then it schedules the shipment. Then it "
            "sends the email. And finally it packages the three results into one "
            "confirmation object and hands it back."
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
            "So the facade is giving us three things. It gives us sequencing: the right "
            "calls in the right order, defined in exactly one place. It gives us a "
            "guard rail: no payment unless stock was secured. And it gives us assembly: "
            "three separate results gathered into one clean object. Notice what it does "
            "not contain: there is almost no business logic in here. A facade delegates. "
            "It does not decide. Keep it thin, and it stays a facade rather than turning "
            "into a giant, tangled class."
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
            "And now the payoff. This is the entire client code. Three lines. We create "
            "the facade, we build a request, and we place the order. Our client does not "
            "know that payments exist. It does not know that shipping exists. If we add "
            "a fraud check to the facade tomorrow, this code does not change at all. "
            "That is the whole point of the pattern."
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
            "When we run the project, we can watch it happen. Each line of output comes "
            "from a different service, in the exact order the facade arranged: stock "
            "reserved, card charged, shipment scheduled, email sent. And at the end, one "
            "single confirmation returned to the client. One call in. One result out. "
            "Four subsystems quietly coordinated in between."
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
            "So, to recap. Use a facade when a group of classes has to be used together "
            "in a particular way, and you want to spare your callers that complexity. "
            "Keep the facade thin, keep the subsystems public and independent, and "
            "remember that a facade is a convenience, not a wall. If you remember just "
            "one sentence from today, make it this one: an adapter changes an interface, "
            "but a facade simplifies many of them. Thank you for watching, and enjoy "
            "building your own facades."
        ),
    ),
]
