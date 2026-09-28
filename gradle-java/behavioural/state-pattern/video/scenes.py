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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'State pattern, in Java. [[slnc 300]] This video is presented '
            'by Jayasekhar Konduru. [[slnc 600]] First, a simple '
            'definition. [[slnc 300]] The State pattern gives every state '
            'of an object its own class. [[slnc 300]] The object then '
            'hands each request to whichever state it is currently in. '
            '[[slnc 400]] So what is allowed depends on which state class '
            'is present, not on checks someone wrote against a status '
            'field. [[slnc 300]] And an action that makes no sense in a '
            'state is simply missing from it. [[slnc 600]] Think of a '
            'vending machine. [[slnc 300]] With no coins in it, pressing '
            'a button does nothing. [[slnc 300]] With a pound fifty in '
            'it, the same button gives you a drink. [[slnc 700]] In this '
            'video, an online order moves from placed, to paid, to '
            'packed, to shipped, to delivered, with cancellations and '
            'refunds along the way. [[slnc 500]] By the end, you will '
            'know why a refusal should be missing code, not a remembered '
            'check. [[slnc 300]] How State differs from Strategy. [[slnc '
            '300]] And when not to use it.'
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
            'Here is the scenario. [[slnc 400]] An order moves through a '
            'simple lifecycle. [[slnc 300]] Placed, then paid, then '
            'packed, then shipped, then delivered. [[slnc 400]] Two more '
            'states end the story: cancelled, and refunded. [[slnc 300]] '
            'Once an order reaches either of those, nothing more happens '
            'to it. [[slnc 500]] Six things can be asked of an order. '
            '[[slnc 300]] Pay, pack, ship, deliver, cancel, and refund. '
            '[[slnc 400]] And the answer to every one depends on where '
            'the order is right now. [[slnc 500]] That sentence is the '
            'whole problem.'
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
            "Before any code, let's look closely at one action: cancel. "
            '[[slnc 500]] Cancelling a placed order moves no money, '
            'because none was taken. [[slnc 300]] Cancelling a paid order '
            'refunds the customer. [[slnc 300]] Cancelling a packed order '
            'refunds the customer and puts the stock back on the shelf, '
            'because a box has already been packed. [[slnc 300]] And a '
            'shipped order cannot be cancelled at all. [[slnc 300]] The '
            'goods are already on a van. [[slnc 600]] So cancel is not '
            'one rule with a permission check in front of it. [[slnc '
            '300]] It is several different jobs, plus a refusal.'
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
            'The obvious first approach is a status field, and a check at '
            'the top of each method. [[slnc 500]] To be fair, this is '
            'short, simple, and the whole lifecycle is in one file. '
            '[[slnc 300]] For small machines, a status list and a table '
            'of allowed moves is often the right answer. [[slnc 600]] The '
            'problem is that the rules get written once per method. '
            '[[slnc 300]] And each copy is phrased however its author '
            'found natural. [[slnc 500]] The cancel check was written as: '
            'anything that has not arrived yet can be cancelled. [[slnc '
            '300]] That sounds sensible. [[slnc 300]] But it quietly '
            'includes shipped orders. [[slnc 300]] So a parcel that is '
            'already on a van gets refunded. [[slnc 500]] The refund '
            'check had a different history. [[slnc 300]] Support asked '
            'for cancelled orders to be refundable too. [[slnc 300]] But '
            'cancelling had already refunded the customer. [[slnc 300]] '
            'So that change pays the customer a second time.'
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
            'And here is what makes it truly nasty. [[slnc 400]] There is '
            'a third copy of the same rules, used to decide which buttons '
            'to show on screen. [[slnc 300]] That copy is correct. [[slnc '
            '300]] It says a shipped order can only be delivered. [[slnc '
            '500]] So the cancel button never appears. [[slnc 300]] '
            'Nobody clicking around the app can reach the bug. [[slnc '
            '300]] Everyone believes the rule is enforced. [[slnc 400]] '
            'But the server still accepts a cancel request, from a '
            'script, a retry, or a support tool. [[slnc 500]] Nobody made '
            'these mistakes while looking at the whole lifecycle. [[slnc '
            '300]] They happened because the lifecycle is never written '
            'down in one place.'
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
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Allow an object to change its '
            'behaviour when its internal state changes. [[slnc 300]] The '
            'object will appear to change its class. [[slnc 600]] That '
            'last sentence does all the work. [[slnc 300]] A shipped '
            'order and a placed order are the same Java object. [[slnc '
            '300]] But they accept different requests, and do different '
            'things with them. [[slnc 300]] Exactly as if they were '
            'different classes. [[slnc 500]] In plain words: stop writing '
            'one method that handles every state. [[slnc 300]] Instead, '
            'write one class per state, that handles every method.'
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
            'Here is the picture to keep in your head: a vending machine. '
            '[[slnc 500]] One machine has no coins in it. [[slnc 300]] '
            'The same machine, a moment later, holds a pound fifty. '
            '[[slnc 300]] Same machine, same buttons. [[slnc 300]] But '
            'pressing a button does something completely different. '
            '[[slnc 500]] You would not say the machine has a mode '
            'number. [[slnc 300]] You would say it is waiting for money, '
            'or ready to sell. [[slnc 300]] Those are named conditions. '
            '[[slnc 500]] And notice this, because it separates State '
            "from Strategy. [[slnc 300]] Nobody chooses the machine's "
            'condition from outside. [[slnc 300]] It gets there because '
            'of what just happened. [[slnc 300]] A coin went in. [[slnc '
            '200]] A drink came out.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'So here are the pieces. [[slnc 500]] The Order is called the '
            'context. [[slnc 300]] It holds one current state, and passes '
            'every request to it. [[slnc 300]] It contains no if '
            'statements about status at all. [[slnc 500]] Order State is '
            'the interface. [[slnc 300]] It declares all six requests. '
            '[[slnc 500]] Then there are seven real states: placed, paid, '
            'packed, shipped, delivered, cancelled, and refunded. [[slnc '
            '300]] Each one holds everything that is true at that point '
            'in the lifecycle. [[slnc 600]] And here is something '
            'uncomfortable. [[slnc 300]] This design looks exactly like '
            'the Strategy pattern. [[slnc 300]] A context, an interface, '
            'and some implementations. [[slnc 300]] We will come back to '
            'how they differ.'
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
            'This is the most important decision in the project. [[slnc '
            '500]] Every request on the interface has a default body. '
            '[[slnc 300]] And every default body refuses the request. '
            '[[slnc 500]] So a state does not list what it forbids. '
            '[[slnc 300]] It only lists what it allows, by overriding '
            'those methods. [[slnc 300]] Everything else refuses by '
            'itself. [[slnc 600]] Think about what that does to mistakes. '
            '[[slnc 300]] In the status field version, forgetting a check '
            'opens a door. [[slnc 300]] That is exactly how shipped '
            'orders became cancellable. [[slnc 400]] Here, forgetting to '
            'override closes a door. [[slnc 300]] The careless mistake '
            'now points the safe way. [[slnc 500]] And the refusal '
            "message is built from the state's allowed actions. [[slnc "
            '300]] For example: cannot refund a shipped order, the only '
            'thing it will accept is deliver.'
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
            'Now, what is left of the Order itself? [[slnc 400]] Every '
            'public method is one line. [[slnc 300]] It passes the '
            'request to the current state. [[slnc 400]] The order does '
            'not know there are seven states. [[slnc 300]] It does not '
            'know their sequence. [[slnc 300]] And there is not one if '
            'statement about status in it. [[slnc 600]] What the order '
            'does own is the history. [[slnc 300]] When a request is '
            'refused, the refusal is recorded, and then passed on. [[slnc '
            '300]] So a line like, someone tried to cancel this after it '
            'shipped, is always recorded. [[slnc 300]] That is exactly '
            'what you want when reading a support ticket. [[slnc 500]] '
            "And from outside, nobody can simply set an order's state. "
            '[[slnc 300]] It only changes as a result of asking the order '
            'to do something.'
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
            'This part decides whether the pattern is worth it. [[slnc '
            '500]] If the states only differed in which requests they '
            'allowed, this would be over-engineering. [[slnc 300]] But '
            'they differ in real work. [[slnc 500]] Cancel, in the paid '
            'state, gives the money back. [[slnc 300]] Cancel, in the '
            'packed state, gives the money back, and also puts the stock '
            'back on the shelf. [[slnc 400]] In the status field version, '
            'those were branches of one method. [[slnc 300]] The day '
            'someone merges them, because they look nearly the same, the '
            'stock stops going back. [[slnc 600]] The shipped state also '
            'overrides cancel, but only to refuse it with a better '
            'reason. [[slnc 300]] It says: this order is already with the '
            'courier. [[slnc 300]] When a refusal has a reason worth '
            'telling a person, write it down.'
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
            'The tests are where the argument becomes proof. [[slnc 500]] '
            'The first test passes, and what it checks is the bug. [[slnc '
            '300]] Pay, cancel, then refund, and the shop has paid the '
            'customer twice. [[slnc 300]] It passes, because that is '
            'really what the naive code does. [[slnc 500]] Next to it, '
            'the same steps run through the State version. [[slnc 300]] '
            "The refund is refused, and the shop's ledger shows exactly "
            'one refund. [[slnc 600]] And one more test is even better. '
            '[[slnc 300]] It tries all seven states with all six actions, '
            'forty-two combinations. [[slnc 300]] For each one, it checks '
            'that the buttons shown on screen exactly predict whether the '
            'action is accepted. [[slnc 300]] The naive version can never '
            'pass that test, and the reason is its bug.'
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
            "Let's run the demo. [[slnc 500]] First, the status field "
            'version. [[slnc 300]] The screen shows only a deliver '
            'button. [[slnc 300]] But the server accepts a cancel anyway, '
            'and then a refund. [[slnc 300]] The shop ends up '
            'ninety-seven pounds and forty-nine pence out of pocket, over '
            'two refunds. [[slnc 300]] That is real money, lost to one '
            'copied condition. [[slnc 500]] Now the same two requests '
            'through the State version. [[slnc 300]] Both are refused, '
            'with reasons a person can read. [[slnc 300]] And both are '
            'recorded in the history. [[slnc 500]] Finally, the demo '
            'lists the buttons for every state. [[slnc 300]] That list '
            'comes from the same classes that hold the behaviour. [[slnc '
            '300]] So the screen and the server can never disagree again.'
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
            'So, what should you remember? [[slnc 500]] First, State and '
            'Strategy have exactly the same class structure. [[slnc 300]] '
            'You cannot tell them apart by their diagram. [[slnc 500]] '
            'The difference is who is in control. [[slnc 300]] A strategy '
            'is chosen by the caller, and never changes itself. [[slnc '
            '300]] For example, the checkout picks a shipping calculator, '
            'and it just does its sum. [[slnc 400]] A state is entered '
            'because of what the object just did. [[slnc 300]] And states '
            'hand control to each other. [[slnc 300]] When the paid state '
            'packs an order, it moves the order into the packed state. '
            '[[slnc 600]] Now the honest cost. [[slnc 300]] Seven '
            'classes, where there used to be one list of statuses. [[slnc '
            '300]] And the full table of moves is no longer in one place. '
            '[[slnc 300]] It is spread across seven files. [[slnc 300]] '
            'That is a real loss. [[slnc 500]] So do not use this for '
            'every status field. [[slnc 300]] If each state only differs '
            'in permission, use a status list and a table of allowed '
            'moves. [[slnc 300]] Use the State pattern when the actual '
            'work differs by state, as it does here.'
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
            "That's the State pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Give each state its '
            'own class, so that a forbidden action is simply code that '
            'does not exist. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a return requested state, between delivered and '
            'refunded. [[slnc 300]] Add it to the State version, and then '
            'to the status field version. [[slnc 300]] And count how many '
            'places you had to edit in each. [[slnc 500]] If this helped, '
            'a like really does help other people find it. [[slnc 300]] '
            "And subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
