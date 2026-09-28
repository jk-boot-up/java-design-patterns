"""Scene definitions for the Command pattern teaching video.

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
        title="The Command Pattern",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Command pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Command pattern turns an '
            'action into an object. [[slnc 300]] Instead of just calling '
            'a method, you create an object that holds what to do, and '
            'everything needed to do it. [[slnc 400]] Then the action can '
            'be stored, passed around, logged, replayed, and even asked '
            'to undo itself. [[slnc 600]] This is the pattern behind '
            'every undo button you have ever pressed. [[slnc 700]] In '
            'this video, we build a shopping cart for an online store, '
            'and the edits a customer makes to it. [[slnc 400]] By the '
            'end, you will know why undo cannot be built from plain '
            'method calls. [[slnc 300]] Where undo bugs really come from. '
            '[[slnc 300]] And what the pattern costs.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "A customer edits their cart, and expects to be able to take it back.",
            "",
            "Four kinds of edit, and each one needs an exact inverse:",
            "",
            "  add an item          the cart may already have some",
            "  remove an item       it was in a position on the screen",
            "  change a quantity    it had an old quantity",
            "  apply a coupon       there may already be one on the cart",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] A customer edits their '
            'shopping cart. [[slnc 300]] They add an item, remove one, '
            'change a quantity, and try a discount code. [[slnc 300]] '
            'Then, like every customer, they change their mind, and press '
            'undo. [[slnc 600]] Each of those edits has some history '
            'attached. [[slnc 300]] The cart may already have held some '
            'of that item. [[slnc 300]] A removed line had a particular '
            'position in the list. [[slnc 300]] And a new coupon may have '
            'replaced an older one. [[slnc 600]] So here is the key idea. '
            '[[slnc 300]] Undo is not the opposite of what the customer '
            'asked for. [[slnc 300]] It is putting back whatever was '
            'there before they asked.'
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="The Obvious First Move",
        body=[
            "Change the cart, and write a note of what you changed:",
            "",
            "  cart.putLine(H-100 x 5);",
            "  changes.push(new Change(\"add\", \"H-100\", 2));",
            "",
            "Then undo pops the note and switches on it.",
            "",
            "Fifteen lines. It works. It is a third of the code.",
        ],
        narration=(
            'The obvious first approach is simple. [[slnc 300]] Change '
            'the cart, and write a note of what you changed. [[slnc 400]] '
            'For example: add two headphones, and push a note that says, '
            'add, headphones, two. [[slnc 300]] To undo, pop the note, '
            'see what kind of edit it was, and reverse it. [[slnc 500]] '
            'To be fair, this is good code. [[slnc 300]] About fifteen '
            'lines, easy to read. [[slnc 300]] And for a cart that only '
            'ever gains brand new items, it is completely correct. [[slnc '
            '400]] The note is honest, too. [[slnc 300]] It records '
            'exactly what the customer asked for. [[slnc 500]] And that '
            'turns out to be the problem.'
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — The Note Records the Request",
        body="""public void addItem(String sku, String name, Money unitPrice, int quantity) {
    cart.putLine(new CartLine(sku, name, unitPrice, cart.quantityOf(sku) + quantity));
    changes.push(new Change("add", sku, quantity));
}

public boolean undo() {
    Change change = changes.pop();
    switch (change.kind()) {
        case "add" -> cart.removeLine(change.sku());   // wrong if the line already existed
        case "coupon" -> cart.setCoupon(null);         // wrong if a coupon was replaced
    }
    return true;
}""",
        narration=(
            'Here is the day it goes wrong. [[slnc 400]] A customer '
            'already has three headphones in their cart. [[slnc 300]] And '
            'a ten percent discount code, applied last week. [[slnc 500]] '
            'They add two more headphones, so the cart now holds five. '
            '[[slnc 300]] Then they apply a better discount code, which '
            'replaces the old one. [[slnc 300]] Then they change their '
            "mind about both, and press undo twice. [[slnc 600]] Let's "
            'follow the notes. [[slnc 300]] The first undo finds the '
            'coupon note, and clears the coupon. [[slnc 300]] So the ten '
            'percent code, which they never touched, is gone. [[slnc '
            '400]] The second undo finds the add note, and removes the '
            'headphones line. [[slnc 300]] So all five headphones '
            'disappear, including the three from last week. [[slnc 600]] '
            'Nothing crashed, and nothing warned anyone. [[slnc 300]] The '
            'notes were not wrong. [[slnc 300]] They just never recorded '
            'what undo really needed: how the cart looked before.'
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   Undo reverses the request, not the change it caused",
            "✗   The state undo needs was never written down",
            "✗   A fifth kind of edit means a new field and a new case",
            "✗   And a re-test of the four that already worked",
            "✗   The bug is silent — the customer is simply charged wrongly",
            "",
            "The switch growing is the complaint. The lost discount is the bug.",
        ],
        narration=(
            'So why does this hurt? [[slnc 400]] Undo reverses the '
            'request, not the change the request caused. [[slnc 300]] The '
            'information undo needed, the three headphones and the old '
            'coupon, was never saved. [[slnc 500]] Every new kind of edit '
            'adds another field to the note, another case to the undo '
            'code, and another round of testing for the old cases. [[slnc '
            '500]] But the worst part is that this bug is silent. [[slnc '
            '300]] Nothing crashes. [[slnc 300]] The customer is simply '
            'charged the wrong amount.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Command Pattern",
        body=[
            "“Encapsulate a request as an object, thereby letting you",
            "parameterize clients with different requests, queue or log",
            "requests, and support undoable operations.”",
            "",
            "— Gang of Four, 1994",
            "",
            "In plain language:",
            "make the action an object,",
            "and it can be held, listed, logged and reversed.",
        ],
        narration=(
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Encapsulate a request as an object, '
            'so that you can queue it, log it, and support undo. [[slnc '
            '500]] In plain words: make the action an object. [[slnc '
            '300]] Then it can be kept, listed, logged, and reversed. '
            '[[slnc 600]] Why does that matter? [[slnc 300]] A method '
            'call is an event. [[slnc 300]] It happens, it returns, and '
            'then it is gone. [[slnc 300]] You cannot put it in a list, '
            'ask it what it did, or run it backwards. [[slnc 500]] Undo '
            'needs all of those things. [[slnc 300]] So the first step is '
            'simple. [[slnc 300]] Instead of calling the method, create '
            'an object that represents the call.'
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="Everyday Analogy: The Order Slip",
        body=[
            "A waiter does not carry your words to the kitchen. They write a slip.",
            "",
            "  the slip can be stacked with the others",
            "  read back to you",
            "  passed to a different chef",
            "  found again an hour later when you query the bill",
            "  torn up if you change your mind",
            "",
            "The slip is the command. The kitchen is the receiver.",
            "The waiter — who cannot cook — is the invoker.",
        ],
        narration=(
            'Here is an everyday example: a restaurant order slip. [[slnc '
            '500]] A waiter does not carry your spoken words to the '
            'kitchen. [[slnc 300]] They write a slip. [[slnc 500]] Think '
            'about what that slip can do. [[slnc 300]] It can wait in a '
            'stack with the others. [[slnc 300]] It can be read back to '
            'you. [[slnc 300]] It can be handed to a different chef. '
            '[[slnc 300]] It can be found an hour later, when you '
            'question the bill. [[slnc 300]] And it can be torn up, if '
            'you change your mind. [[slnc 600]] In the pattern, the slip '
            'is the command. [[slnc 300]] The kitchen, which knows how to '
            'cook but has never met you, is called the receiver. [[slnc '
            '300]] And the waiter, who carries any slip without cooking '
            'anything, is called the invoker.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'So here are the roles in our project. [[slnc 500]] The '
            'command interface is called Cart Command. [[slnc 300]] It '
            'has three methods: describe, execute, and undo. [[slnc 500]] '
            'The invoker is called Cart History. [[slnc 300]] It keeps '
            'two stacks of commands, one for done and one for undone. '
            '[[slnc 300]] It only ever runs a command, or reverses one. '
            '[[slnc 500]] The receiver is the Cart itself. [[slnc 500]] '
            'Then there are four concrete commands: add item, remove '
            'item, change quantity, and apply coupon. [[slnc 300]] Each '
            'one saves exactly the information it needs to undo itself. '
            '[[slnc 300]] The old quantity. [[slnc 200]] The removed line '
            'and its position. [[slnc 200]] Or the old coupon. [[slnc '
            '500]] And notice that neither side knows the other. [[slnc '
            '300]] The cart has never heard of a command. [[slnc 300]] '
            'And the history has never heard of a coupon.'
        ),
    ),
    dict(
        key="09-interface",
        kind="code",
        title="The Command — Three Methods",
        body="""public interface CartCommand {

    /** One line for the audit trail, in the customer's terms. */
    String describe();

    /** Do it, capturing whatever undo will need. */
    void execute(Cart cart);

    /** Put the cart back the way this command found it. */
    void undo(Cart cart);
}""",
        narration=(
            'The whole interface is just three methods. [[slnc 500]] '
            'Describe returns one line for the history log, in the '
            "customer's own terms. [[slnc 300]] Execute makes the change. "
            '[[slnc 300]] And undo reverses it. [[slnc 500]] Which one is '
            'hard? [[slnc 300]] Undo, of course. [[slnc 500]] Notice one '
            'detail. [[slnc 300]] Both execute and undo receive the cart '
            'as a parameter. [[slnc 300]] A command does not hold on to a '
            'cart. [[slnc 300]] It only holds plain values, like a '
            'product code, a quantity, or a coupon. [[slnc 300]] The cart '
            'is handed in at the moment it is needed.'
        ),
    ),
    dict(
        key="10-concrete",
        kind="code",
        title="The One That Is Not Trivial to Reverse",
        body="""public void execute(Cart cart) {
    previousQuantity = cart.quantityOf(sku);      // <-- the whole pattern
    cart.putLine(new CartLine(sku, name, unitPrice, previousQuantity + quantity));
    executed = true;
}

public void undo(Cart cart) {
    if (previousQuantity == 0) {
        cart.removeLine(sku);
    } else {
        cart.putLine(new CartLine(sku, name, unitPrice, previousQuantity));
    }
}""",
        narration=(
            "This part is the reason the project exists, so let's go "
            'slowly. [[slnc 500]] Take the add item command. [[slnc 300]] '
            'The very first thing execute does is ask the cart: how many '
            'of this item do you already have? [[slnc 300]] It saves that '
            'answer. [[slnc 300]] Then it adds the new items. [[slnc '
            '600]] Now think about undo. [[slnc 300]] Adding two '
            'headphones to a cart that held three leaves five. [[slnc '
            '300]] Undoing that does not mean removing the line. [[slnc '
            '300]] It means setting the quantity back to three. [[slnc '
            '500]] And we can only know that when the command runs, not '
            'when it is created. [[slnc 600]] So here is the rule, and it '
            'is where undo bugs live. [[slnc 300]] Save the information '
            'you need for undo inside execute, from the receiver, at the '
            'moment the command runs. [[slnc 300]] Not in the '
            'constructor. [[slnc 300]] At construction time, the cart may '
            'not yet look the way it will when the command runs. [[slnc '
            '600]] The other commands follow the same rule. [[slnc 300]] '
            'Remove item saves the line and its position, so undo puts it '
            'back in the same place. [[slnc 300]] And apply coupon saves '
            'the coupon it replaced. [[slnc 300]] Usually there is none. '
            '[[slnc 300]] But sometimes, it is exactly the discount the '
            'naive version threw away.'
        ),
    ),
    dict(
        key="11-invoker",
        kind="code",
        title="The Invoker, Which Knows Nothing",
        body="""public void execute(CartCommand command) {
    command.execute(cart);
    done.push(command);      // only if execute returned normally
    undone.clear();          // a new action makes the old future unreachable
}

public boolean undo() {
    if (done.isEmpty()) { return false; }
    CartCommand command = done.pop();
    command.undo(cart);
    undone.push(command);
    return true;
}""",
        narration=(
            'Now the invoker, Cart History. [[slnc 400]] To execute, it '
            'runs the command, pushes it onto the done stack, and clears '
            'the undone stack. [[slnc 300]] To undo, it pops the top '
            'command, tells it to undo, and moves it to the undone stack. '
            '[[slnc 600]] Two decisions are worth noticing. [[slnc 400]] '
            'First, clearing the undone stack. [[slnc 300]] Once you take '
            'a new action, the old redo path is gone. [[slnc 300]] Every '
            'text editor you have used behaves this way. [[slnc 500]] '
            'Second, if execute fails with an error, the command is never '
            'pushed. [[slnc 300]] Undoing a half-finished edit would '
            'reverse something that never fully happened. [[slnc 600]] '
            'And notice what this class never mentions. [[slnc 300]] No '
            'coupons, no quantities, no products. [[slnc 300]] That is '
            'why a new kind of edit never needs to change this file.'
        ),
    ),
    dict(
        key="12-proof",
        kind="code",
        title="The Test That Proves It",
        body="""@Test
void anUnknownCommandWorksUnchanged() {
    history.execute(add("A-1", 1));

    // Gift wrapping. Nothing in src/main has ever heard of it.
    CartCommand giftWrap = new CartCommand() {
        public String describe() { return "add gift wrapping"; }
        public void execute(Cart cart) { cart.putLine(GIFT_WRAP); }
        public void undo(Cart cart)    { cart.removeLine("GIFT"); }
    };

    history.execute(giftWrap);
    history.undo();
}""",
        narration=(
            'Here is the test that proves the pattern works. [[slnc 400]] '
            'A simple test like, adding two items leaves two items, would '
            'also pass for the naive version. [[slnc 300]] It tests the '
            'cart, not the pattern. [[slnc 600]] This test is different. '
            '[[slnc 300]] It creates a gift wrapping command, inside the '
            'test file itself. [[slnc 300]] Nothing in the main code has '
            'ever heard of gift wrapping. [[slnc 400]] Yet Cart History '
            'runs it, and undoes it, without a single change. [[slnc '
            '500]] If someone ever added special cases back into the '
            'history class, this is the test that would fail. [[slnc '
            '500]] Two more tests check the exact cases the naive version '
            'got wrong. [[slnc 300]] Undoing an add restores the old '
            'quantity. [[slnc 300]] And undoing a coupon restores the '
            'coupon it replaced. [[slnc 300]] The project has '
            'thirty-seven tests, and those three carry the argument.'
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== 1. The trap: undo notes that record the request, not the cart ===
  Two undos later, they expected to be back where they started:
    (empty)
  The 3 headphones are gone, and so is WELCOME10.

=== 4. The two edits the naive version got wrong ===
  Two undos later:
    H-100    Wireless headphones     3 x   £89.99 =   £269.97
    WELCOME10 (-10%)                                 -£27.00
  3 headphones, and WELCOME10 is back.

=== 5. What you get for free once an edit is an object ===
  history.log():
    add 1 x H-100
    set H-100 to 4
    apply coupon WELCOME10""",
        narration=(
            "Let's run the demo, and compare. [[slnc 500]] First, the "
            'naive version. [[slnc 300]] After two undos, the cart is '
            'empty, and the discount code is gone. [[slnc 500]] Then the '
            'same two edits, done with commands. [[slnc 300]] After two '
            'undos, the cart has its three headphones, and its ten '
            'percent code, exactly as it started. [[slnc 500]] The same '
            'customer, the same actions, and two different results. '
            '[[slnc 300]] The difference is one saved field per command, '
            'captured at the right moment. [[slnc 600]] And there is a '
            'bonus. [[slnc 300]] The history can print a readable list of '
            'everything the customer did, in plain words. [[slnc 300]] '
            'Nobody wrote extra code for that. [[slnc 300]] It comes '
            'free, because every edit is an object that can describe '
            'itself.'
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "✓   Make the action an object: execute, undo, describe",
            "✓   Capture undo state inside execute — never in the constructor",
            "✓   The invoker holds a stack of the interface and knows nothing else",
            "✓   A new kind of edit is one class, and no file gets reopened",
            "",
            "✗   Every operation becomes a class — for four fixed edits, don't",
            "✗   The inverse is yours to get right; nothing checks it for you",
            "✗   Reads should not be commands: nothing to undo, nothing to log",
            "",
            "Command stores the difference.  Memento stores the state.",
        ],
        narration=(
            'So, what should you remember? [[slnc 500]] Make each action '
            'an object, with execute, undo, and describe. [[slnc 300]] '
            'Save the information undo needs inside execute, never in the '
            'constructor. [[slnc 300]] Keep the invoker simple: it holds '
            'commands, and knows nothing else. [[slnc 300]] And a new '
            'kind of edit is one new class, with no old file reopened. '
            '[[slnc 600]] Now the honest costs. [[slnc 400]] Every '
            'operation becomes a class. [[slnc 300]] For four edits that '
            'never change, the naive version is a third of the code, and '
            'it works. [[slnc 300]] Use Command when undo, logging, or '
            'queuing is a real need. [[slnc 500]] The pattern gives undo '
            'a home, but it does not check that your undo is correct. '
            '[[slnc 300]] And simple reads should not be commands, '
            'because there is nothing to undo. [[slnc 600]] Finally, know '
            'its close relative, the Memento pattern. [[slnc 300]] '
            'Command saves the difference, and each edit must know how to '
            'reverse itself. [[slnc 300]] Memento saves a full snapshot '
            'instead, and needs no reversing, but costs a copy at every '
            'step. [[slnc 500]] And you have used Command already. [[slnc '
            '300]] A task handed to a thread pool is a command without '
            'undo. [[slnc 300]] And a database migration with an up step '
            'and a down step is a command with undo.'
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that breaks",
            "undo on purpose by moving one line into the constructor.",
        ],
        narration=(
            "That's the Command pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Turn each action '
            'into an object that saves what it needs to undo itself, at '
            'the moment it runs. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Move that saving step out of execute, and into '
            'the constructor. [[slnc 300]] Run the tests, and exactly one '
            'will fail. [[slnc 300]] Working out which one, and why, is '
            'worth more than the rest of this video. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
