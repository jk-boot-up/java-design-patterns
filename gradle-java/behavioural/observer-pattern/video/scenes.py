"""Scene definitions for the Observer pattern teaching video.

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
        title="The Observer Pattern",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Observer pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Observer pattern lets '
            'one object announce that something happened. [[slnc 300]] '
            'Any number of other objects can react to it. [[slnc 300]] '
            'And the announcer does not need to know who they are. [[slnc '
            '500]] Listeners sign up with the announcer, which is called '
            'the subject. [[slnc 300]] When the event happens, the '
            'subject notifies everyone on its list. [[slnc 300]] And the '
            'list can change, without the subject changing. [[slnc 600]] '
            'This is the pattern behind every notification you have ever '
            'received. [[slnc 700]] In this video, an online order '
            'changes status, and four separate systems care: inventory, '
            'email, analytics, and the warehouse. [[slnc 500]] By the '
            'end, you will know how to add a fifth reaction without '
            'editing any code that already works. [[slnc 300]] And what '
            'that costs you.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online order moves from Placed to Paid to Shipped.",
            "",
            "Every one of those transitions matters to somebody:",
            "",
            "  inventory        release the reservation once it ships",
            "  email            tell the customer it's on its way",
            "  analytics        count it for the funnel report",
            "  warehouse feed   write the line that gets the parcel picked",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] An order in an online '
            'store moves from placed, to paid, to shipped, to delivered. '
            '[[slnc 300]] And every change matters to someone. [[slnc '
            '500]] Inventory must release the reserved stock once the '
            'parcel ships. [[slnc 300]] The email system must tell the '
            'customer it is on its way. [[slnc 300]] Analytics counts it '
            'for the sales report. [[slnc 300]] And the warehouse feed '
            'writes the line that gets the parcel picked from the shelf. '
            '[[slnc 500]] Four unrelated reactions to one small change. '
            '[[slnc 300]] And the list keeps growing: loyalty points, '
            'fraud checks, and more.'
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="The Obvious First Move",
        body=[
            "Give the order service the four things it has to tell:",
            "",
            "  inventory.onStatusChanged(event);",
            "  email.onStatusChanged(event);",
            "  analytics.onStatusChanged(event);",
            "  warehouseFeed.onStatusChanged(event);",
            "",
            "Four lines. You can see everything it does.",
        ],
        narration=(
            'The obvious first approach is simple. [[slnc 300]] Give the '
            'order service the four systems it must tell, and call each '
            'one in turn. [[slnc 500]] Four lines, one after another. '
            '[[slnc 300]] To be fair, this is good code. [[slnc 300]] You '
            'can read it top to bottom, and see exactly what happens when '
            'an order ships. [[slnc 400]] For four reactions that never '
            'change, it is the right answer. [[slnc 500]] So far, this is '
            'only a design complaint. [[slnc 300]] Until the network gets '
            'involved.'
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Four Calls, No Net",
        body="""public void markShipped(String orderId, OrderStatus from) {
    OrderEvent event = new OrderEvent(orderId, from, OrderStatus.SHIPPED);

    inventory.onStatusChanged(event);
    email.onStatusChanged(event);        // talks to a mail server
    analytics.onStatusChanged(event);    // never runs if email throws
    warehouseFeed.onStatusChanged(event);
}

//  The order shipped. The warehouse was never told.""",
        narration=(
            'Here is the day it goes wrong. [[slnc 400]] The second call, '
            'to email, talks to a mail server over the network. [[slnc '
            '300]] One afternoon, that mail server times out. [[slnc '
            "600]] Let's follow what happens. [[slnc 300]] The order is "
            'already marked shipped. [[slnc 300]] Inventory has already '
            'released the stock. [[slnc 300]] Then the email call throws '
            'an error. [[slnc 300]] So analytics never runs, and the '
            "warehouse feed is never written. [[slnc 600]] The customer's "
            'order says shipped, the stock is gone, and nobody ever picks '
            'the parcel. [[slnc 300]] The error message talks about a '
            'mail server timeout. [[slnc 300]] It says nothing at all '
            'about a parcel. [[slnc 500]] That is a real incident, and it '
            'passed code review, because those four lines look perfectly '
            'reasonable.'
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   One failing reaction takes the rest down with it",
            "✗   A fifth reaction means editing a working method",
            "✗   Every status-changing method must remember analytics",
            "✗   You cannot test shipping without stubbing all four",
            "✗   A new reaction cannot be added from outside at all",
        ],
        narration=(
            'And it gets worse as the system grows. [[slnc 500]] One '
            'failing reaction stops all the ones after it. [[slnc 400]] '
            'Adding a fifth reaction means editing a method that four '
            'working systems depend on. [[slnc 300]] Plus a new field, '
            'and a new constructor parameter, which breaks every test '
            'that builds this class. [[slnc 400]] Analytics wants every '
            'status change. [[slnc 300]] So every new status method must '
            'remember to call it. [[slnc 300]] The one that forgets '
            'leaves a quiet hole in the report. [[slnc 400]] You cannot '
            'test shipping without faking all four systems. [[slnc 400]] '
            'And a plugin cannot add a reaction of its own, because there '
            'is nowhere to put one.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Observer Pattern",
        body=[
            "“Define a one-to-many dependency between objects so that",
            "when one object changes state, all its dependents are",
            "notified and updated automatically.”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "let the thing that changed announce it,",
            "and let whoever cares sign up.",
        ],
        narration=(
            'The Observer pattern fixes exactly this. [[slnc 400]] Here '
            'is its definition, from the famous Gang of Four book. [[slnc '
            '300]] Define a one-to-many dependency between objects, so '
            'that when one object changes state, all its dependents are '
            'notified automatically. [[slnc 500]] In plain words: let the '
            'thing that changed announce it. [[slnc 300]] And let whoever '
            'cares sign up.'
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="Remember It With a Newsletter",
        body=[
            "A shop sends its newsletter to everyone on the list.",
            "",
            "It does not know who you are, or what you do with it.",
            "One subscriber or a hundred thousand — same code, same send.",
            "",
            "And you own the relationship, not the shop:",
            "you subscribed, and you can unsubscribe, without asking.",
        ],
        narration=(
            "Here is an easy way to remember it: a shop's newsletter. "
            '[[slnc 500]] The shop writes one email, and sends it to '
            'everyone on the list. [[slnc 400]] How much does the shop '
            'know about what you do with it? [[slnc 300]] Nothing. [[slnc '
            '300]] You might read it, forward it, or delete it unopened. '
            '[[slnc 300]] That is exactly why one subscriber and a '
            'hundred thousand subscribers take the same amount of code. '
            '[[slnc 500]] And who owns the relationship? [[slnc 300]] You '
            'do. [[slnc 300]] You subscribed, and you can unsubscribe, '
            'without the shop changing at all. [[slnc 500]] That is the '
            'Observer pattern. [[slnc 300]] The publisher knows nothing '
            'about its subscribers. [[slnc 300]] The subscribers know the '
            'publisher.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'Every Observer design has the same few roles. [[slnc 500]] '
            'The subject is the Order. [[slnc 300]] It changes, and it '
            'keeps the list of listeners. [[slnc 400]] The observer '
            'interface is called Order Listener. [[slnc 300]] It is the '
            'only type the order depends on. [[slnc 400]] The concrete '
            'observers are the four listeners: inventory, email, '
            'analytics, and the warehouse feed. [[slnc 400]] And the '
            'event, called Order Event, is what actually travels from the '
            'order to the listeners. [[slnc 600]] Now notice what is '
            'missing. [[slnc 300]] No listener knows that any other '
            'listener exists. [[slnc 300]] And the order has no field for '
            'email, inventory, or the warehouse. [[slnc 500]] Here is the '
            'key idea. [[slnc 300]] The order cannot behave differently '
            'depending on who is listening, because it has no way to find '
            'out who is listening. [[slnc 300]] That is why the '
            'thousandth listener costs nothing extra.'
        ),
    ),
    dict(
        key="09-strategy",
        kind="code",
        title="The Observer — One Small Interface",
        body="""public interface OrderListener {
    String name();
    void onStatusChanged(OrderEvent event);
}

public record OrderEvent(String orderId, OrderStatus from, OrderStatus to) { }

//  No priority. No ordering hint. No shouldHandle predicate.
//  Every one of those would let a listener make claims about the others.""",
        narration=(
            'The observer interface, Order Listener, has just two '
            'methods. [[slnc 400]] On Status Changed does the work. '
            '[[slnc 300]] And name gives each listener a name, so that '
            'when one fails, the error says which one. [[slnc 600]] The '
            'interesting part is what is deliberately left out. [[slnc '
            '300]] No priority. [[slnc 200]] No ordering. [[slnc 200]] No '
            'filter that decides whether to handle an event. [[slnc 400]] '
            'Each of those would let one listener make claims about the '
            'others. [[slnc 300]] And then they would no longer be '
            'independent. [[slnc 500]] The event itself is a simple '
            'value. [[slnc 300]] It holds the order I D, the old status, '
            'and the new status. [[slnc 300]] Not the order itself.'
        ),
    ),
    dict(
        key="10-concrete",
        kind="code",
        title="A Concrete Observer — It Knows Only Its Own Job",
        body="""public final class InventoryListener implements OrderListener {

    @Override
    public void onStatusChanged(OrderEvent event) {
        switch (event.to()) {
            case SHIPPED   -> { released++;  sink.accept("released " + ...); }
            case CANCELLED -> { restocked++; sink.accept("restocked " + ...); }
            default -> { }        // the other statuses are not our business
        }
    }
}""",
        narration=(
            'Now one real listener: the inventory listener. [[slnc 400]] '
            'It reacts to two statuses. [[slnc 300]] When an order ships, '
            'it releases the reserved stock. [[slnc 300]] When an order '
            'is cancelled, it puts the stock back. [[slnc 300]] For every '
            'other status, it simply does nothing. [[slnc 500]] Compare '
            'it with the analytics listener, which wants every single '
            'status change. [[slnc 300]] The two have completely '
            'different needs. [[slnc 300]] The only thing they share is '
            'the interface. [[slnc 500]] The inventory listener never '
            'mentions email, the warehouse, or even the order class. '
            '[[slnc 300]] So it can be tested on its own, without ever '
            'creating an order.'
        ),
    ),
    dict(
        key="11-context",
        kind="code",
        title="The Subject — Search It for the Word 'Email'",
        body="""private final List<OrderListener> listeners = new CopyOnWriteArrayList<>();

public List<ListenerFailure> moveTo(OrderStatus next) {
    if (next == status) { return List.of(); }        // no event, no notify
    OrderEvent event = new OrderEvent(id, status, next);
    status = next;                                   // before the loop

    List<ListenerFailure> failures = new ArrayList<>();
    for (OrderListener listener : listeners) {
        try { listener.onStatusChanged(event); }
        catch (RuntimeException e) { failures.add(ListenerFailure.of(listener, e)); }
    }
    return List.copyOf(failures);
}""",
        narration=(
            'Now the subject, the Order class. [[slnc 400]] Search it for '
            'the word email. [[slnc 300]] Then inventory. [[slnc 300]] '
            'Then warehouse. [[slnc 300]] None of them appear. [[slnc '
            '300]] The list of reactions is not in the class that causes '
            'them. [[slnc 600]] The method that changes the status makes '
            'three deliberate decisions. [[slnc 500]] First, if the '
            'status did not really change, no event is sent. [[slnc 300]] '
            'Otherwise every listener must guard against duplicates, and '
            'one that forgets sends a second shipping email. [[slnc 500]] '
            'Second, the status is updated before any listener is told. '
            '[[slnc 300]] So a listener always sees the world the event '
            'describes. [[slnc 500]] Third, and this is the fix for our '
            'incident. [[slnc 300]] Each listener is called inside its '
            'own try and catch. [[slnc 300]] If one fails, the failure is '
            'recorded under its name, and the next listener still runs. '
            '[[slnc 500]] And the list is a special copy-on-write list. '
            '[[slnc 300]] That lets a listener unsubscribe itself while '
            'it is being notified, without breaking the loop.'
        ),
    ),
    dict(
        key="12-proof",
        kind="code",
        title="The Test That Actually Proves It",
        body="""@Test
void anUnknownListenerWorksUnchanged() {
    Order order = new Order("A-9");
    order.addListener(new OrderListener() {
        public String name() { return "loyalty"; }
        public void onStatusChanged(OrderEvent e) { ... }
    });

    assertTrue(order.moveTo(OrderStatus.DELIVERED).isEmpty());
}

//  Nothing in src/main knows this listener exists.""",
        narration=(
            'Here is a subtle point about testing. [[slnc 400]] A test '
            'that says the inventory listener released the stock would '
            'pass for the naive design too. [[slnc 300]] It shows the '
            'reaction is correct. [[slnc 300]] It proves nothing about '
            'the pattern. [[slnc 500]] This test does. [[slnc 300]] It '
            'creates a brand new loyalty listener, entirely inside the '
            'test file. [[slnc 300]] Nothing in the main code knows it '
            'exists. [[slnc 300]] It is added to an order, and it simply '
            'works. [[slnc 400]] The order class was written long before, '
            'and did not need changing. [[slnc 500]] If someone replaced '
            'the listener list with four fixed fields, this is the test '
            'that would fail.'
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== 1. The trap: an order service that calls each system by name ===
  [inventory] released the reservation for A-1001
  !! SMTP timeout after 30s
  warehouse feed     : []
  The order shipped. The warehouse was never told.

=== 4. One listener throws; the others still run ===
  [inventory] released the reservation for A-1004
  [analytics] recorded A-1004: Placed -> Shipped
  [warehouse-feed] wrote "A-1004,SHIPPED"
  failures reported  : [email failed: SMTP timeout after 30s]
  The warehouse was told anyway.""",
        narration=(
            "Let's run the demo. [[slnc 300]] The same broken mail server "
            'is used twice. [[slnc 500]] First, with the naive service. '
            '[[slnc 300]] Inventory releases the stock, the email call '
            'throws, and the warehouse feed stays empty. [[slnc 300]] The '
            'order shipped, and nobody was told to pick it. [[slnc 500]] '
            'Then, the same failure with the Observer pattern. [[slnc '
            '300]] Inventory runs. [[slnc 200]] Analytics runs. [[slnc '
            '200]] The warehouse feed is written. [[slnc 400]] And the '
            'email failure is not hidden either. [[slnc 300]] It comes '
            'back as a named listener failure, so someone can retry it. '
            '[[slnc 500]] The same error, and two very different '
            'afternoons.'
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use observer when one change has several independent reactions",
            "and the list of them is open-ended.",
            "",
            "The honest cost: reading moveTo no longer tells you what happens.",
            "Your IDE can't help -- every call site is typed as the interface.",
            "",
            "Remember one sentence:",
            "Observer decouples; Mediator centralises.",
            "The publisher knows nothing; the subscribers know the publisher.",
        ],
        narration=(
            'So, to recap. [[slnc 400]] Use Observer when one change has '
            'several independent reactions, and the list of them keeps '
            'growing. [[slnc 600]] Now the honest cost. [[slnc 300]] '
            'Reading the order class no longer tells you what happens '
            'when an order ships. [[slnc 300]] You must find every place '
            'a listener is added, across the codebase. [[slnc 300]] That '
            'is a real loss of clarity, traded for real independence. '
            '[[slnc 500]] Two more warnings. [[slnc 300]] The order in '
            'which listeners are called is not a promise. [[slnc 300]] If '
            'two reactions must happen in sequence, they are really one '
            'reaction. [[slnc 400]] And a long-lived subject holding a '
            'short-lived listener is a classic memory leak. [[slnc 300]] '
            'Someone must remember to remove the listener. [[slnc 500]] '
            'Java once had a built-in version of this pattern, but it was '
            'deprecated in Java nine. [[slnc 300]] The pattern was never '
            'the problem, that implementation was. [[slnc 300]] So write '
            'your own small interface, as this project does. [[slnc 600]] '
            'And one sentence to remember. [[slnc 300]] Observer '
            'separates, Mediator centralises. [[slnc 300]] In Observer, '
            'the publisher knows nobody. [[slnc 300]] In Mediator, a hub '
            'knows everyone, on purpose, so it can coordinate them.'
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
            "That's the Observer pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Let the thing '
            'that changed announce it, let whoever cares sign up, and one '
            'failing listener no longer stops the rest. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] If there '
            'is a pattern you would like to see covered, suggest it in '
            'the comments. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
