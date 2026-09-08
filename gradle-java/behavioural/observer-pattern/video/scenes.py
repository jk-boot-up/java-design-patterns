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
            "Hello, and welcome. This video explains the Observer pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. [[slnc "
            "300]] Let's start with the simple definition. The observer pattern "
            "lets one object announce that something has happened, and any number "
            "of others react to it, without the announcer knowing who they are. "
            "Listeners register with the subject; when the event happens the "
            "subject notifies whoever is on the list, and the list can change "
            "without the subject changing. [[slnc 350]] That's the idea in a "
            "sentence, and it's the pattern behind every notification you have "
            "ever received. The rest of the video does it properly, by building a "
            "real working Java project: an online order that changes status, and "
            "the inventory, email, analytics and warehouse systems that care. "
            "[[slnc 250]] By the end you'll know how to add a fifth reaction "
            "without editing a single line of code that already works — and, just "
            "as importantly, what that costs you."
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
            "So, imagine an order in an online store. [[slnc 250]] It moves from "
            "placed, to paid, to shipped, to delivered — and every one of those "
            "transitions matters to somebody. [[slnc 300]] Inventory needs to "
            "release the reservation once the parcel actually ships. The email "
            "system needs to tell the customer it's on its way. Analytics counts "
            "it for the funnel report. And the warehouse feed writes the line "
            "that gets the parcel picked off the shelf. [[slnc 250]] Four "
            "completely unrelated reactions to one small change. And the list "
            "grows: loyalty points, fraud checks, the supplier integration "
            "somebody promised for next quarter."
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
            "The obvious first move is to give the order service the four things "
            "it has to tell, and tell them. [[slnc 300]] Four lines, one after "
            "another. And I want to be fair to it: this is good code. You can "
            "read it top to bottom and see exactly what happens when an order "
            "ships — which, as we'll see later, is more than you can say for the "
            "version we're about to replace it with. [[slnc 250]] For four "
            "reactions that will never change, this is the right answer. So what "
            "follows isn't a bug report yet. It's a design complaint — until the "
            "network gets involved."
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
            "So here's the naive approach, and here's the day it bites. [[slnc "
            "250]] The second line talks to a mail server, over a network, and "
            "one afternoon that mail server times out. [[slnc 350]] Follow what "
            "happens. The order is already marked shipped. Inventory has already "
            "released the stock. Then email throws — and analytics never runs, "
            "and the warehouse feed is never written. [[slnc 300]] So the "
            "customer's order says shipped, the stock is gone, and nobody ever "
            "picks the parcel. The exception that reaches the caller says S M T P "
            "timeout. It says nothing whatsoever about a parcel. [[slnc 250]] "
            "That is not a tangle. That's an incident, and it passed code review, "
            "because those four lines look completely reasonable."
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
            "And that does real damage as the system grows. [[slnc 250]] One "
            "failing reaction takes the rest down with it, because there's "
            "nothing between them. Adding a fifth reaction means opening a method "
            "that four working systems already depend on, and adding a field, and "
            "a constructor parameter — which breaks every test that builds this "
            "class. [[slnc 300]] Analytics wants every transition, so every "
            "status-changing method that ever gets written has to remember to "
            "call it, and the one that forgets is a hole in the funnel report "
            "that nobody notices for a quarter. [[slnc 250]] You can't test the "
            "shipping transition without standing up all four collaborators. And "
            "a plugin, or a regional module, can't add a reaction of its own at "
            "all, because there's nowhere to put it."
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
            "The observer pattern fixes exactly this. [[slnc 250]] In Gang of "
            "Four terms, observer defines a one-to-many dependency between "
            "objects, so that when one object changes state, all its dependents "
            "are notified and updated automatically. [[slnc 300]] In plain "
            "language? Let the thing that changed announce it, and let whoever "
            "cares sign up."
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
            "Here's how to remember it forever. Think about a shop's newsletter. "
            "[[slnc 250]] The shop writes one email and sends it to everyone on "
            "the list. [[slnc 300]] Now — how much does the shop know about what "
            "you do with it? Nothing. You might read it, forward it, or bin it "
            "unopened. It doesn't know, and that's precisely why one subscriber "
            "and a hundred thousand subscribers are the same amount of code. "
            "[[slnc 350]] And here's the half people forget: who owns the "
            "relationship? You do. You subscribed, and you can unsubscribe, "
            "without asking the shop's permission and without the shop being "
            "changed. [[slnc 250]] That's observer. The publisher knows nothing; "
            "the subscribers know the publisher."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "Every observer setup has the same handful of roles. [[slnc 200]] The "
            "subject — here, Order — the thing that changes and keeps the list. "
            "The observer interface, OrderListener, the one type the subject "
            "depends on. The concrete observers: inventory, email, analytics, the "
            "warehouse feed. And the event, OrderEvent, which is what actually "
            "travels. [[slnc 350]] Now look at what's missing from that picture. "
            "There is no arrow between the four listeners — none of them knows "
            "the others exist. And Order has no field called email, or inventory, "
            "or warehouse. [[slnc 300]] Here's the single most important idea in "
            "this whole video. Order cannot behave differently depending on who "
            "is listening, because there is no message it could send to find out "
            "who that is. [[slnc 250]] That's exactly why the thousandth listener "
            "costs nothing."
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
            "This is the observer, OrderListener. [[slnc 250]] Two methods. "
            "onStatusChanged does the work, and name is there because a stack "
            "trace from inside a listener list is otherwise anonymous — and this "
            "is exactly the code where a stack trace is all you're going to get. "
            "[[slnc 350]] But the interesting part is what's deliberately "
            "missing. There's no priority. No ordering hint. No shouldHandle "
            "predicate. [[slnc 250]] Every single one of those would let a "
            "listener make a claim about the other listeners — and the moment a "
            "listener can do that, they're not independent any more, and the "
            "whole thing quietly turns back into the four lines we started with. "
            "[[slnc 300]] And notice the event is a record: an order id, the "
            "status it came from, and the status it's going to. A value. Not the "
            "order itself."
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
            "And this is a concrete observer, InventoryListener. [[slnc 250]] It "
            "reacts to two statuses and ignores the rest — and it ignores them by "
            "simply doing nothing, which is worth noticing. It doesn't ask "
            "permission to skip, and nothing filters events on its behalf. "
            "[[slnc 300]] Compare it with the analytics listener, which wants "
            "every transition there is. Those two have completely different "
            "appetites, they hold completely different state, and the only thing "
            "they have in common is the interface. [[slnc 250]] There's no "
            "mention of email here, no mention of the warehouse, and no mention "
            "of Order. So this class gets its own test, and that test never "
            "constructs an order at all."
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
            "And this is the subject, Order. [[slnc 250]] Search this class for "
            "the word email. Then inventory. Then warehouse. Nothing, all three "
            "times. The list of reactions is not in the class that causes them. "
            "[[slnc 350]] There are three decisions in that method and each one "
            "is deliberate. First, the guard: if nothing changed, there's no "
            "event — otherwise every listener has to defend itself against "
            "duplicates, and the one that forgets sends a second shipping email. "
            "[[slnc 300]] Second, the status is updated before the loop runs, so "
            "a listener that does look at the order sees the world the event "
            "describes, not the one it replaced. [[slnc 350]] And third — this is "
            "the fix for that outage — the try-catch is inside the loop. One "
            "listener throwing is recorded against its name and the loop carries "
            "on to the next one. [[slnc 300]] One more thing: that's a "
            "copy-on-write list, and not because of threads. It's so a listener "
            "can unsubscribe itself while it's being notified — a one-shot "
            "subscription — without blowing up the iteration."
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
            "Here's a subtlety worth pausing on, because it changes how you test "
            "this. [[slnc 250]] A test that says the inventory listener released "
            "one reservation passes against the naive design too. It tells you "
            "the reaction is correct. It proves nothing at all about whether the "
            "pattern was applied. [[slnc 350]] This one does. It defines a "
            "listener entirely inside the test — nothing in the production source "
            "knows it exists — hands it to an order, and it just works. Order was "
            "compiled long before this class existed and didn't need "
            "recompiling. [[slnc 300]] That's the extension point being real, "
            "rather than being a list of four. And if somebody quietly replaced "
            "the listener list with four fields tomorrow, this is the test that "
            "goes red."
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
            "When we run the project, the same broken mail server is used twice. "
            "[[slnc 250]] In section one, through the naive service: inventory "
            "releases the stock, email throws, and the warehouse feed is empty "
            "square brackets. The order shipped and nobody was told to pick it. "
            "[[slnc 350]] In section four, exactly the same failure, this time "
            "behind the pattern. Inventory runs. Analytics runs. The warehouse "
            "feed is written. And the email failure isn't swallowed either — it "
            "comes back as a listener failure, named, so somebody can retry it. "
            "[[slnc 300]] Same exception, two completely different afternoons."
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
            "So, to recap. Use observer when one change has several independent "
            "reactions and the list of them is open-ended — and the list of "
            "people interested in an order genuinely is. [[slnc 300]] Now the "
            "honest cost, because it's a real one. Reading moveTo tells you "
            "nothing about what happens when an order ships. You have to go and "
            "find every addListener call in the codebase, and your development "
            "environment can't help you, because they're all typed as the "
            "interface. That is a genuine loss of legibility, traded for a "
            "genuine gain in independence. [[slnc 250]] Two more warnings. "
            "Notification order is not a contract — it happens to be registration "
            "order, and a listener that depends on that is already broken. Two "
            "reactions that must be sequenced are really one reaction. And a "
            "long-lived subject holding a short-lived listener is the classic "
            "memory leak; removeListener is the whole of the answer, and somebody "
            "has to remember to call it. [[slnc 350]] One last thing. Java "
            "shipped a built-in version of this, java dot util dot Observer, and "
            "deprecated it in Java nine — it wasn't type-safe, Observable was a "
            "class you had to extend, and it promised nothing about ordering. The "
            "pattern was never the problem; that implementation was. Write your "
            "own interface, like we did. [[slnc 300]] And if you remember one "
            "sentence from today, make it this one. Observer decouples; mediator "
            "centralises. In observer the publisher knows nothing and the "
            "subscribers know the publisher. In mediator a hub knows everyone, "
            "deliberately, so it can coordinate them."
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
            "And that's the observer pattern. [[slnc 300]] If you got something "
            "out of this, do give it a thumbs up, and subscribe. It genuinely "
            "helps the channel, and it's what makes more of these possible. "
            "[[slnc 250]] And if there's a pattern you'd like me to cover next, "
            "drop it in the comments. I read every one. [[slnc 250]] All the "
            "source code, the written notes and an interactive animation are in "
            "the repository. Thanks for watching, and I'll see you in the next "
            "one."
        ),
    ),
]
