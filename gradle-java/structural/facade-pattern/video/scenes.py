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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Facade pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A facade puts one simple '
            'front door in front of a complicated group of classes. '
            '[[slnc 300]] The classes behind it all still exist, and '
            'specialists can still use them. [[slnc 300]] But ordinary '
            'callers talk to one object, with one method, instead of '
            'juggling many. [[slnc 600]] Think of a waiter in a '
            'restaurant. [[slnc 300]] You tell the waiter what you want, '
            'and the waiter deals with the kitchen. [[slnc 700]] In our '
            'online store, we look at checkout. [[slnc 500]] By the end, '
            'you will know what a facade is, why it exists, and how to '
            'write one yourself.'
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
            'Here is the scenario. [[slnc 400]] A customer fills their '
            'basket, and clicks place order. [[slnc 500]] That one click '
            'looks simple. [[slnc 300]] But behind it, four different '
            'things must happen. [[slnc 500]] Reserve the stock, so '
            'nobody else buys the last item. [[slnc 300]] Charge the '
            "customer's card. [[slnc 300]] Book the delivery with the "
            'warehouse. [[slnc 300]] And email the customer a '
            'confirmation.'
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
            'In this project, each of those four jobs lives in its own '
            'class. [[slnc 500]] The inventory service reserves the '
            'stock. [[slnc 300]] The payment service charges the card, '
            'and returns a payment I D. [[slnc 300]] The shipping service '
            'books the delivery, and returns a tracking number. [[slnc '
            '300]] And the notification service sends the email. [[slnc '
            '500]] Each one is small, focused, and does its job well.'
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
            'Here is the problem. [[slnc 400]] Without a facade, every '
            'part of the application that places an order must know all '
            'four services. [[slnc 300]] It must create them. [[slnc '
            '300]] Call them in exactly the right order. [[slnc 300]] And '
            'pass the results from one to the next. [[slnc 600]] The '
            'website does this. [[slnc 300]] The mobile app does this. '
            '[[slnc 300]] The admin tool does this. [[slnc 300]] The same '
            'fragile code, copied into three places.'
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
            'That does real damage. [[slnc 500]] New developers must '
            'learn four classes, just to place one order. [[slnc 300]] '
            'The order of steps is easy to get wrong. [[slnc 300]] And '
            'getting it wrong means charging a customer for something we '
            'cannot ship. [[slnc 500]] Add a fifth step tomorrow, and '
            'every caller must change. [[slnc 300]] The copies slowly '
            'drift apart. [[slnc 300]] And testing one order needs all '
            'four services set up, every time.'
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
            'The Facade pattern fixes exactly this. [[slnc 400]] The '
            'classic book on design patterns, by the authors known as the '
            'Gang of Four, describes it like this. [[slnc 300]] Provide '
            'one simple, unified interface to a set of interfaces in a '
            'subsystem, making it easier to use. [[slnc 600]] In plain '
            'words: one simple front door, to a complicated building.'
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
            'Here is how to remember it. [[slnc 300]] Think about a '
            'restaurant. [[slnc 500]] You do not walk into the kitchen '
            'and talk to the grill chef, then the sauce chef, then the '
            'pastry chef. [[slnc 300]] You talk to one person, the '
            'waiter. [[slnc 300]] And you say: I will have the steak. '
            '[[slnc 500]] The waiter knows which chefs to speak to, in '
            'what order, and what to bring back. [[slnc 500]] The chefs '
            'still exist, doing skilled work. [[slnc 300]] You are just '
            'protected from the complexity. [[slnc 300]] The waiter is a '
            'facade.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Three Roles",
        body=None,
        narration=(
            'Every facade has three roles. [[slnc 500]] The facade '
            'itself: here, the order facade class. [[slnc 300]] The '
            'subsystems: our four services. [[slnc 300]] And the client: '
            'the code that just wants to place an order. [[slnc 600]] '
            'Here is the most important idea in this video. [[slnc 300]] '
            'The facade knows about the services. [[slnc 300]] But the '
            'services never know about the facade. [[slnc 500]] The '
            'connection only goes one way. [[slnc 300]] And that keeps '
            'each service reusable on its own.'
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
            'Here is one of the services: the inventory service. [[slnc '
            '400]] Notice how small and ordinary it is. [[slnc 300]] It '
            'reserves stock, and says whether that worked. [[slnc 300]] '
            'That is all. [[slnc 300]] It has no idea a facade exists. '
            '[[slnc 600]] That is on purpose. [[slnc 300]] Because it '
            'knows nothing about the bigger process, you could reuse it '
            'in a different application tomorrow. [[slnc 300]] The other '
            'three services follow the same shape.'
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
            'Here is the facade itself. [[slnc 400]] It holds the four '
            'services inside it. [[slnc 300]] And it offers just one '
            'method: place order. [[slnc 600]] Here is what that method '
            'does. [[slnc 300]] First, it reserves the stock. [[slnc '
            '300]] If that fails, it stops at once, so the customer is '
            'never charged for something we cannot ship. [[slnc 500]] '
            'Only then does it take the payment. [[slnc 300]] Then it '
            'books the delivery. [[slnc 300]] Then it sends the email. '
            '[[slnc 300]] Finally, it gathers the three results into one '
            'confirmation, and hands it back.'
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
            'So the facade gives us three things. [[slnc 500]] '
            'Sequencing: the right calls, in the right order, written in '
            'one place. [[slnc 300]] A safety rule: no payment, unless '
            'the stock was secured. [[slnc 300]] And assembly: three '
            'separate results, gathered into one clean answer. [[slnc '
            '600]] Now notice what it does not contain. [[slnc 300]] '
            'Almost no business logic. [[slnc 300]] A facade passes work '
            'on. [[slnc 300]] It does not make decisions. [[slnc 500]] '
            'Keep it thin, and it stays a facade. [[slnc 300]] Instead of '
            'growing into one of those giant, tangled classes.'
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
            'And now the payoff. [[slnc 300]] Here is the whole client '
            'code, in three steps. [[slnc 500]] Create the facade. [[slnc '
            '300]] Build an order request. [[slnc 300]] And place the '
            'order. [[slnc 600]] The client does not know that payments '
            'exist. [[slnc 300]] Or shipping. [[slnc 300]] And if a fraud '
            'check is added to the facade tomorrow, this code does not '
            'change at all. [[slnc 300]] That is the whole point.'
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

Inventory: reserving 2 unit(s) of SKU-1234
Payment: charged £49.98 to customer CUST-001 (paymentId=PMT-C68994F4)
Shipping: scheduled shipment for order ORD-0D1ADD0C
          to 221B Baker Street, London (trackingId=TRK-A844891E)
Notification: emailed customer CUST-001 confirmation for
          order ORD-0D1ADD0C (trackingId=TRK-A844891E)

Order placed: OrderConfirmation[orderId=ORD-0D1ADD0C,
          paymentId=PMT-C68994F4, trackingId=TRK-A844891E]""",
        narration=(
            "Let's run the project. [[slnc 400]] Each line of output "
            'comes from a different service, in the order the facade '
            'arranged. [[slnc 500]] Two units of the product are '
            'reserved. [[slnc 300]] The card is charged forty-nine pounds '
            'ninety-eight. [[slnc 300]] The delivery is booked, with a '
            'tracking number. [[slnc 300]] And the confirmation email is '
            'sent. [[slnc 600]] At the end, one confirmation goes back to '
            'the client. [[slnc 300]] One call in. [[slnc 300]] One '
            'result out. [[slnc 300]] And four services quietly '
            'coordinated in between.'
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
            'So, to recap. [[slnc 400]] Use a facade when a group of '
            'classes must be used together in a particular way. [[slnc '
            '300]] And you want to spare callers that complexity. [[slnc '
            '600]] Keep the facade thin. [[slnc 300]] Keep the services '
            'public, and independent. [[slnc 300]] A facade is a '
            'convenience, not a wall. [[slnc 600]] And one comparison '
            'worth knowing. [[slnc 300]] An adapter changes one '
            'interface. [[slnc 300]] A facade simplifies many of them.'
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
            "That's the Facade pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] A facade is one '
            'simple front door that coordinates many classes, so callers '
            'never have to. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Add a fraud check to '
            'the facade, before payment. [[slnc 300]] And notice that the '
            'client code does not change. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
