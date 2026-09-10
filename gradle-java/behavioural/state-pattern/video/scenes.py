"""Scene definitions for the State pattern teaching video.

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
        title="The State Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the State pattern in Java, "
            "and it is written and presented by Jayasekhar Konduru. [[slnc 300]] "
            "Let's start with the simple definition. The state pattern gives "
            "every state of an object its own class, and has the object delegate "
            "to whichever one it is currently in. What is allowed is then decided "
            "by which class is present, rather than by checks somebody wrote "
            "against a status field — and an operation that makes no sense in a "
            "state is simply absent from it. [[slnc 350]] That's the idea in a "
            "sentence. The rest of the video does it properly, by building a real "
            "working Java project: an online store where an order moves from "
            "placed, to paid, to packed, to shipped, to delivered, with "
            "cancellations and refunds hanging off the side. [[slnc 250]] By the "
            "end you'll know why a refusal should be the absence of code rather "
            "than a check somebody remembered to write, exactly what separates "
            "state from strategy — the pattern it shares a class diagram with — "
            "and when you should not use it at all."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An order moves through a small, well understood lifecycle:",
            "",
            "  PLACED -> PAID -> PACKED -> SHIPPED -> DELIVERED",
            "",
            "and two states end the story: CANCELLED and REFUNDED.",
            "",
            "Six things can be asked of it:",
            "  pay   pack   ship   deliver   cancel   refund",
            "",
            "The answer to every one of them depends on where it is.",
        ],
        narration=(
            "So, imagine an online shop. [[slnc 250]] An order moves through a "
            "small, well understood lifecycle: placed, paid, packed, shipped, "
            "delivered. Two more states end the story — cancelled and refunded — "
            "and once an order reaches either of those, nothing more happens to "
            "it. [[slnc 300]] Six things can be asked of an order: pay, pack, "
            "ship, deliver, cancel and refund. And the answer to every single one "
            "of them depends on where the order currently is. [[slnc 300]] That "
            "sentence is the entire problem, and every design in this video is an "
            "attempt to write it down without repeating yourself."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Look Closely at One Row",
        body=[
            "cancel, in each state:",
            "",
            "  PLACED      allowed — no money has been taken",
            "  PAID        allowed — refund the customer",
            "  PACKED      allowed — refund, AND put the stock back",
            "  SHIPPED     no. it is on a van.",
            "  DELIVERED   no. that is a return, not a cancellation.",
            "",
            "That is not one rule with a guard on it.",
            "It is four different pieces of work, and one refusal.",
        ],
        narration=(
            "Before we write any code, look closely at one row of that table: "
            "cancel. [[slnc 300]] Cancelling a placed order moves no money at "
            "all, because none has been taken. Cancelling a paid order refunds "
            "the customer. Cancelling a packed order refunds the customer and "
            "puts the stock back on the shelf, because somebody has already taped "
            "a box shut. And cancelling a shipped order is not a thing you can "
            "do — the goods are on a van, and the shop has nothing to put back. "
            "[[slnc 350]] So that row is not one rule with a permission check in "
            "front of it. It is four genuinely different pieces of work plus a "
            "refusal, and any design that treats it as one method with a guard is "
            "already losing information."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — One Rule, Three Copies",
        body="""public void cancel(String reason) {
    // Drifted: "anything that has not arrived yet", which
    // reads sensibly and quietly includes SHIPPED.
    if (status == Status.DELIVERED || status == Status.CANCELLED
            || status == Status.REFUNDED) { throw refuse(); }
    ledger.refund(charged.minus(refunded));
    move(Status.CANCELLED, reason);
}

public void refund(String reason) {
    // Drifted: CANCELLED was added so support could "sort it out".
    if (status != Status.DELIVERED && status != Status.CANCELLED) {
        throw refuse();
    }
    ledger.refund(total);          // a cancel already refunded
}""",
        narration=(
            "The obvious first move is a status field and a check at the top of "
            "each method. [[slnc 250]] I want to be fair to this. It is short, it "
            "needs no vocabulary, the whole lifecycle is in one file, and a new "
            "reader can find every rule by scrolling. For a machine this size, an "
            "enum and a map of permitted transitions is often the right answer, "
            "and I'll come back to that at the end. [[slnc 350]] The problem is "
            "not the enum. The problem is that the rules are now written down "
            "once per method, and each copy is phrased in whichever direction its "
            "author found natural. Look at these two. The first is a blocklist. "
            "The second is an allowlist. [[slnc 300]] Cancel was written as: "
            "anything that has not arrived yet can be cancelled. It reads "
            "sensibly. It also quietly includes shipped, because shipped is not "
            "on that list — so a parcel that is on a van gets refunded. [[slnc "
            "300]] And refund originally accepted only delivered, until support "
            "asked for cancelled to be added so they could sort out cancelled "
            "orders. But a cancel has already refunded. So that line pays the "
            "customer a second time."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "There is a third copy, written for the screen:",
            "",
            "  allowedActions()  ->  SHIPPED gives [deliver]",
            "",
            "and that one is right.",
            "",
            "So the cancel button is never drawn,",
            "and the endpoint accepts the call anyway.",
            "",
            "The bug is invisible from the UI,",
            "and reachable from everything that is not the UI.",
        ],
        narration=(
            "And here is what makes it genuinely nasty. [[slnc 250]] There is a "
            "third copy of the same rules, written for the screen — a switch that "
            "returns which buttons to draw. That copy is correct. It says a "
            "shipped order can only be delivered. [[slnc 300]] So the cancel "
            "button is never drawn. Nobody clicking around the application can "
            "reach the bug. Everybody who looks at it believes the rule is "
            "enforced. And the endpoint takes the call anyway, from a script, "
            "from a retry, from an integration, from a support tool. [[slnc 350]] "
            "None of these three is a mistake anybody would make while looking at "
            "the whole lifecycle at once. They happen precisely because nobody "
            "ever is — the lifecycle is not written down anywhere. It only exists "
            "as the intersection of six conditionals."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The State Pattern",
        body=[
            "“Allow an object to alter its behavior when its internal",
            "state changes. The object will appear to change its class.”",
            "",
            "— Gang of Four, 1994",
            "",
            "In plain language:",
            "stop writing one method for all states.",
            "Write one state for all methods.",
        ],
        narration=(
            "The Gang of Four put it like this: allow an object to alter its "
            "behavior when its internal state changes. The object will appear to "
            "change its class. [[slnc 350]] Hold on to that last sentence, "
            "because it is doing all the work. Not — the object has a status "
            "field. The object appears to change its class. A shipped order and a "
            "placed order are the same Java object, but they accept different "
            "messages and do different things with them, which is exactly what "
            "being a different class would mean. [[slnc 300]] In plain language: "
            "stop writing one method for all states, and start writing one state "
            "for all methods. Give the condition a type."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="Everyday Analogy: The Vending Machine",
        body=[
            "A vending machine with no coins in it,",
            "and the same machine holding one pound fifty.",
            "",
            "Same machine. Same buttons.",
            "Pressing one does something different.",
            "",
            "You would not say it has a mode integer.",
            "You would say it is waiting for money, or ready to vend.",
            "",
            "And nobody chose that from outside.",
            "It got there because of what it just did.",
        ],
        narration=(
            "Here's the picture I'd keep in your head. [[slnc 250]] A vending "
            "machine with no coins in it, and the same vending machine holding a "
            "pound fifty. Same machine, same buttons — and pressing the same "
            "button does something completely different. [[slnc 300]] You would "
            "not describe that machine as having a mode integer. You would say it "
            "is waiting for money, or that it is ready to vend. Those are "
            "conditions with names, and the buttons that do nothing in one of "
            "them are the ones that work in the other. [[slnc 350]] And notice "
            "the last bit, because it is the part that separates this from "
            "Strategy: nobody chooses the machine's condition from outside. It "
            "arrives there because of what it just did. A coin went in. A can "
            "came out."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So here are the pieces. [[slnc 250]] Order is the context. It holds "
            "one state, it forwards every request to that state, and it contains "
            "no conditional that mentions a status anywhere. [[slnc 300]] "
            "OrderState is the interface. It declares all six requests. And then "
            "there are seven concrete states — placed, paid, packed, shipped, "
            "delivered, cancelled and refunded — each one holding everything that "
            "is true about that point in the lifecycle. [[slnc 300]] Look at the "
            "shape of that diagram, because I want you to notice something "
            "uncomfortable: it is indistinguishable from a Strategy diagram. A "
            "context, an interface, some implementations. If I removed the names "
            "you could not tell which pattern this is. We'll come back to that."
        ),
    ),
    dict(
        key="09-interface",
        kind="code",
        title="Every Request Refuses By Default",
        body="""public interface OrderState {

    String name();
    List<String> allowedActions();

    default void pay(Order order)     { throw refuse("pay"); }
    default void pack(Order order)    { throw refuse("pack"); }
    default void ship(Order order)    { throw refuse("ship"); }
    default void deliver(Order order) { throw refuse("deliver"); }

    default void cancel(Order order, String reason) { throw refuse("cancel"); }
    default void refund(Order order, String reason) { throw refuse("refund"); }
}""",
        narration=(
            "This is the single most important decision in the project. [[slnc "
            "250]] Every request on the interface has a body, and every one of "
            "those bodies throws. [[slnc 300]] Which means a state does not list "
            "what it forbids. It lists what it allows, by overriding, and "
            "everything else refuses on its own without a line of code being "
            "written. [[slnc 350]] Think about what that does to the failure "
            "mode. In the enum version, forgetting to mention a state in a guard "
            "opens a transition — which is exactly how shipped became "
            "cancellable. Here, forgetting to override closes one. The mistake "
            "you make when you are not paying attention now points the safe way. "
            "[[slnc 300]] And the refusal builds its own message out of the "
            "state's allowed actions, so the explanation can never go stale: "
            "cannot refund a shipped order — the only thing it will accept is "
            "deliver."
        ),
    ),
    dict(
        key="10-context",
        kind="code",
        title="The Context Has No Conditionals At All",
        body="""public void ship() { attempt("ship", state -> state.ship(this)); }

private void attempt(String action, Consumer<OrderState> request) {
    String from = state.name();
    try {
        request.accept(state);
    } catch (IllegalTransitionException e) {
        history.add(OrderEvent.refused(action, from, e.reason()));
        throw e;
    }
}

// package-private: only a state may call this
void transitionTo(OrderState next, String action, String detail) {
    history.add(OrderEvent.moved(action, state.name(), next.name(), detail));
    state = next;
}""",
        narration=(
            "And here is what is left of the order itself. [[slnc 250]] Every "
            "public method is one line: forward the request to whatever state we "
            "are holding. Order does not know there are seven states. It does not "
            "know what order they come in. There is not one if statement in it "
            "that mentions a status. [[slnc 300]] What it does own is the audit "
            "trail. A refusal is caught on the way past, written into the "
            "history, and rethrown — so, somebody tried to cancel this after it "
            "shipped is recorded whether or not it worked, which is exactly the "
            "line you want when you are reading a support ticket. [[slnc 300]] "
            "And notice that transitionTo is package private. From outside, an "
            "order's state changes only as a consequence of asking it to do "
            "something. You cannot set it."
        ),
    ),
    dict(
        key="11-states",
        kind="code",
        title="Same Verb, Genuinely Different Work",
        body="""// PaidState — give the money back
public void cancel(Order order, String reason) {
    order.ledger().refund(back);
    order.transitionTo(CancelledState.INSTANCE, "cancel",
            reason + " — refunded " + back + ", nothing had shipped");
}

// PackedState — give the money back AND undo the packing
public void cancel(Order order, String reason) {
    order.ledger().refund(back);
    order.transitionTo(CancelledState.INSTANCE, "cancel",
            reason + " — refunded " + back + ", box opened and stock returned");
}

// ShippedState — refuse, with a reason worth telling a human
public void cancel(Order order, String reason) {
    throw refuse("cancel", "it is already with the courier — the customer "
            + "must refuse delivery or return it");
}""",
        narration=(
            "Now, this is the slide that decides whether the pattern was worth "
            "it. [[slnc 250]] If the states differed only in which calls they "
            "allowed, this would be an over-engineered enum and you should not do "
            "it. [[slnc 300]] They don't. Cancel in the paid state gives the "
            "money back. Cancel in the packed state gives the money back and puts "
            "the stock back, because a box has been taped shut since then. Three "
            "different bodies for one word — and in the enum version those are "
            "three branches of one method that were, at some point, one branch. "
            "The day somebody merges them because they look nearly the same, the "
            "stock stops going back on the shelf. [[slnc 350]] And the shipped "
            "state overrides cancel too, but only in order to refuse it with a "
            "better reason than the default would have given. The default would "
            "have said, the only thing it will accept is deliver. True, and "
            "useless to a support agent. This says: it is already with the "
            "courier. When a refusal has a reason worth telling a human, write it "
            "down."
        ),
    ),
    dict(
        key="12-proof",
        kind="code",
        title="The Test That Proves It",
        body="""// This test PASSES. What it asserts is the bug.
@Test
void andTheShopPaysTheCustomerTwice() {
    NaiveOrder order = order();
    order.pay();
    order.cancel("out of stock");

    order.refund("support ticket 4471");

    assertEquals(2, order.ledger().refundCount());
    assertEquals(TOTAL.times(2), order.ledger().refunded());
}

@Test
void theSameScenarioIsRefusedByTheStateVersion() {
    order.pay();
    order.cancel("out of stock");

    assertThrows(IllegalTransitionException.class,
            () -> order.refund("support ticket 4471"));
    assertEquals(1, order.ledger().refundCount());
}""",
        narration=(
            "The tests are where the argument stops being rhetoric. [[slnc 250]] "
            "The first one passes. What it asserts is the bug: pay, cancel, "
            "refund, and the shop has paid the customer twice. That test is green "
            "because that is genuinely what the code does. [[slnc 300]] And every "
            "one of those is paired with the identical scenario run through the "
            "state version, where the same three calls end in a refusal and the "
            "ledger still shows exactly one refund. Two tests, same story, "
            "different endings. [[slnc 350]] There is one more I like even "
            "better. It walks all seven states and all six actions — forty two "
            "combinations — and checks that asking the order what buttons to draw "
            "predicts, every single time, whether the call actually throws. In "
            "the naive version that test cannot pass, and the reason it cannot is "
            "the bug."
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== 1. The trap: one rule, written out in three chains ===
  buttons drawn   : [deliver]
  cancel() anyway : accepted — status is now CANCELLED
  refund() anyway : accepted — status is now REFUNDED
  the shop is out : -£97.49 over 2 refunds

=== 3. The refusals, and where they come from ===
  cannot cancel a SHIPPED order: it is already with the courier
  cannot refund a CANCELLED order: it is final, and nothing more can happen

=== 4. Which buttons to draw ===
    PLACED     [pay, cancel]        SHIPPED    [deliver]
    PAID       [pack, cancel]       DELIVERED  [refund]
    PACKED     [ship, cancel]       REFUNDED   []""",
        narration=(
            "Run it, and the two halves sit side by side. [[slnc 250]] Section "
            "one is the status field: the screen offering only deliver, the "
            "endpoint accepting cancel anyway, and a ledger that ends up ninety "
            "seven pounds and forty nine pence short of zero over two refunds. "
            "That is real money, and it left because of one condition in a chain "
            "somebody copied. [[slnc 300]] Section three is the same two requests "
            "through the state version. Both refused, with reasons a human can "
            "read, and both recorded in the history. [[slnc 300]] And section "
            "four prints the buttons for every state. That list comes from the "
            "same class that holds the methods — so unlike the naive version, the "
            "screen and the endpoint cannot disagree, because there is only one "
            "of them now."
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "State and Strategy have the SAME class diagram.",
            "The difference is intent and control:",
            "",
            "  a Strategy is chosen by the caller, and does not change itself",
            "  a State is entered as a consequence of what the object did,",
            "  and states hand control to one another",
            "",
            "The cost, honestly:",
            "  seven classes where there was one enum",
            "  the transition table is gone — it is one arrow per file",
            "",
            "Use it when the BEHAVIOUR varies, not just the permissions.",
        ],
        narration=(
            "So, what to take away. [[slnc 300]] First, the confusion I promised "
            "to clear up. State and strategy have the same class diagram. Not a "
            "similar one — the same one. Any explanation that tries to "
            "distinguish them by structure is wrong, because there is no "
            "structural difference to find. [[slnc 300]] The difference is intent "
            "and control. A strategy is chosen by the caller and does not change "
            "itself: the checkout picks a shipping calculator, and that "
            "calculator does its sum forever unaware that any other calculator "
            "exists. A state is entered as a consequence of what the object did, "
            "and states hand control to one another — paid state's pack method "
            "ends by making the order a packed state. A state names its "
            "successors, and that reference is why the two are not "
            "interchangeable. [[slnc 350]] Now the bill, honestly. Seven classes "
            "where there was one enum. And the transition table no longer exists "
            "anywhere you can read it — it is distributed across seven files, one "
            "arrow at a time. In the enum version you could see the whole "
            "lifecycle in one switch, in ten seconds. That is a real loss. "
            "[[slnc 300]] So do not reach for this every time you see a status "
            "field. If every state's version of a method is the same body behind "
            "a different guard, you wanted the enum and a map of permitted "
            "transitions. Reach for this when the behaviour varies by state and "
            "not merely the permission — when cancelling a paid order and "
            "cancelling a packed one do genuinely different work, as they do here."
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that adds a",
            "RETURN_REQUESTED state to both versions, and counts the edits.",
        ],
        narration=(
            "That's the state pattern. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in "
            "the repository — including the exercise I would most recommend: "
            "add a return requested state between delivered and refunded, first "
            "to the state version and then to the enum, and count what you have "
            "to edit in each. In one of them it is a new file and one existing "
            "class. In the other it is six chains of conditionals and a switch. "
            "[[slnc 300]] If this helped, a like genuinely does help other "
            "people find it, and subscribe if you would like the rest of the "
            "behavioural series. [[slnc 250]] Thanks for watching, and I'll see "
            "you in the next one."
        ),
    ),
]
