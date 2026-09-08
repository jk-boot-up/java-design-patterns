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
            "Hello, and welcome. This video explains the Command pattern in Java, "
            "and it is written and presented by Jayasekhar Konduru. [[slnc 300]] "
            "Let's start with the simple definition. The command pattern turns an "
            "action into an object. Instead of calling a method, you create "
            "something that holds what to do and everything it needs in order to "
            "do it — so the action can be stored, passed around, logged, "
            "replayed, and asked to undo itself afterwards. [[slnc 350]] That's "
            "the idea in a sentence, and it's the pattern behind every undo "
            "button you have ever pressed. The rest of the video does it "
            "properly, by building a real working Java project: a shopping cart "
            "in an online store, and the edits a customer makes to it. [[slnc "
            "250]] By the end you'll know why undo cannot be built out of method "
            "calls, where undo bugs actually live, and what the pattern costs "
            "you."
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
            "So, imagine a shopping cart in an online store. [[slnc 250]] The "
            "customer adds an item, removes one, changes a quantity, tries a "
            "discount code. Then they do what every customer does: they change "
            "their mind, and they look for the undo. [[slnc 300]] Now look at "
            "those four edits again, because each one has a piece of history "
            "attached to it. The cart might already have had some of that item. "
            "The line you removed was in a particular position on the screen. "
            "The coupon you applied may have pushed another one off. [[slnc "
            "300]] Undo is not the opposite of what the customer asked for. It "
            "is the restoration of what was there before they asked."
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
            "The obvious first move is to change the cart, and write a note "
            "beside it saying what you just did. [[slnc 300]] Add two of H one "
            "hundred, push a note saying add, H one hundred, two. Undo pops the "
            "note, looks at what kind of edit it was, and reverses it. [[slnc "
            "250]] I want to be fair to this, because it is good code. Fifteen "
            "lines, readable at a glance, and for a cart that only ever gains "
            "brand new lines it is completely correct. [[slnc 250]] The note is "
            "honest, too: an accurate record of what the customer asked for. "
            "[[slnc 300]] And that is exactly the problem, although you cannot "
            "see it yet."
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
            "So here is the naive approach, and here is the day it bites. [[slnc "
            "250]] A customer has three headphones in their cart and a ten "
            "percent code they applied last week. They add two more headphones, "
            "so the cart says five. They spot a better discount code and apply "
            "that instead. Then they change their mind about both, and press undo "
            "twice. [[slnc 350]] Follow the notes. The first undo pops the coupon "
            "note and clears the coupon — so the ten percent code they never "
            "touched is gone. The second undo pops the add note and removes the "
            "line — so all five headphones disappear, including the three they "
            "chose last week. [[slnc 300]] Nothing threw an exception. Nothing "
            "logged a warning. The note was never wrong; it simply never held "
            "the thing undo actually needed, which is what the cart looked like "
            "beforehand."
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
            "So why does that hurt? [[slnc 250]] Undo reverses the request "
            "rather than the change it caused, and the state it needed — the "
            "three headphones, the old coupon — was never written down by "
            "anybody. A fifth kind of edit means another field on the note, "
            "another case in the switch, and a re-test of the four that already "
            "worked. [[slnc 250]] But the one that matters is the last: this bug "
            "is silent. Nothing crashes. The customer is simply charged the "
            "wrong amount. [[slnc 300]] Most explanations of this pattern stop "
            "at the switch getting long. That is the design complaint. The lost "
            "discount is the actual bug, and it is the reason to change anything."
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
            "The Gang of Four put it like this: encapsulate a request as an "
            "object, thereby letting you parameterize clients with different "
            "requests, queue or log requests, and support undoable operations. "
            "[[slnc 350]] In plain language: make the action an object, and it "
            "can be held, listed, logged and reversed. [[slnc 300]] Here is why "
            "that is not just jargon. A method call is an event. It happens, it "
            "returns, and then it is gone. You cannot put it in a list. You "
            "cannot ask it what it did. You cannot run it again tomorrow, or "
            "against a different cart, or backwards. [[slnc 250]] Undo needs "
            "every one of those. So the first move is not clever at all: stop "
            "calling the method, and make an object that is the call."
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
            "Here is the everyday version. [[slnc 250]] A waiter does not carry "
            "your words to the kitchen. They write a slip. [[slnc 300]] Think "
            "about what that slip can do that your spoken sentence cannot. It "
            "can be stacked with the others. Read back to you. Handed to a "
            "different chef. Found again an hour later when you query the bill. "
            "And torn up if you change your mind before it is cooked. [[slnc "
            "300]] Your spoken words could do none of that, because they only "
            "existed while you were saying them. [[slnc 250]] The slip is the "
            "command. The kitchen — which knows how to cook and has never met "
            "you — is the receiver. And the waiter, who can carry any slip "
            "without being able to cook a thing on it, is the invoker."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So here are the roles. [[slnc 250]] In the middle, the command "
            "interface — Cart Command — with three methods: describe, execute "
            "and undo. On the left, the invoker, Cart History, which holds two "
            "stacks of that interface and does exactly two things with an "
            "element: runs it, or reverses it. On the right, the receiver, the "
            "Cart itself. [[slnc 300]] Along the bottom, the four concrete "
            "commands, and notice what is written under each one: the field it "
            "captures. Previous quantity. The removed line and its position. "
            "Previous coupon. Those fields are the pattern doing its real work. "
            "[[slnc 300]] And notice that the ignorance runs both ways. The Cart "
            "has never heard of a command. And Cart History has never heard of a "
            "coupon — it pops an object and sends it undo. What that means is "
            "the command's business, not the invoker's."
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
            "And here is the entire pattern. Three methods. [[slnc 300]] Describe "
            "gives you one line for the audit trail, in the customer's terms. "
            "Execute does the edit. Undo reverses it. [[slnc 250]] Ask a room "
            "which of those three is hard and everybody says undo, and everybody "
            "is right. [[slnc 300]] Notice that both execute and undo take the "
            "cart as a parameter rather than holding onto one. That is "
            "deliberate. A command holds values — a S K U, a quantity, a coupon — "
            "never a live line that the cart might replace underneath it. The "
            "receiver is passed in at the moment it is needed. [[slnc 250]] "
            "Everything else in this video is a consequence of these twelve lines."
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
            "Read this one twice, because it is the reason the project exists. "
            "[[slnc 300]] The first line of execute asks the cart how many of "
            "this S K U it already has, and keeps the answer. Then it makes the "
            "change. [[slnc 250]] Now look at undo. Adding two to a cart that "
            "held three leaves five. Undoing that is not remove the line — it is "
            "put it back to three. Which branch applies is not known when the "
            "command is constructed. It is only known when it runs. [[slnc 350]] "
            "So here is the rule, and it is the one place undo bugs live. "
            "Capture the state you will need to reverse yourself inside execute, "
            "from the receiver, at the moment you run. Not in the constructor — "
            "that is a guess about a cart you have not reached yet, and an "
            "earlier undo may have made it wrong before you get there. [[slnc "
            "300]] A field the constructor does not set is the visible sign of a "
            "command that captures at run time. [[slnc 250]] The other three are "
            "the same shape. Remove captures the line and its position, because "
            "putting it back at the bottom of the screen is not undo. Apply "
            "coupon captures the coupon it replaced — null nine times out of "
            "ten, and the tenth time it is the discount the naive version threw "
            "away."
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
            "And here is the invoker, in full. [[slnc 250]] Execute runs the "
            "command, pushes it onto the done stack, and clears the undone "
            "stack. Undo pops the top command, sends it undo, and moves it "
            "across. [[slnc 300]] Two decisions are worth naming. [[slnc 200]] "
            "First, undone dot clear: once you take a new action, the old future "
            "is unreachable — every text editor you have used behaves this way. "
            "[[slnc 250]] Second, and this one is quieter: if execute throws, "
            "the push never happens, because undoing a half-applied edit would "
            "apply the reverse of something that never fully happened. [[slnc "
            "300]] Now search this class for the word coupon. Or quantity. Or S "
            "K U. They are not there. That is precisely why a fifth kind of edit "
            "does not open this file."
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
            "This is the test that proves the claim. [[slnc 300]] A test that "
            "says adding two items leaves two items passes against the naive "
            "editor as well — it tests the cart, not the pattern. [[slnc 250]] "
            "This one does not. Gift wrapping is a command declared inside the "
            "test file. Nothing in the main source has ever heard of it. Cart "
            "History was compiled long before it existed, and it runs it, and "
            "undoes it, without a single change. [[slnc 300]] If somebody put a "
            "switch back into the invoker tomorrow, this is the test that goes "
            "red. [[slnc 250]] Beside it sit two more: undoing a merged add "
            "restores the previous quantity, and undo restores the replaced "
            "coupon — the two cases the note-and-switch version got wrong. There "
            "are thirty-seven tests here, and those three carry the argument."
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
            "Run it, and the two halves sit side by side. [[slnc 250]] Section "
            "one is the naive editor: two undos, and the cart is empty and the "
            "coupon is gone. Section four is the identical pair of edits done as "
            "commands: two undos, and the cart has its three headphones and its "
            "ten percent code, exactly as it started. [[slnc 300]] Same "
            "customer, same actions, two different answers — and the difference "
            "is one field per command, captured at the right moment. [[slnc "
            "250]] Then section five, which people do not expect. History dot "
            "log gives you a readable list of everything that was done, in the "
            "customer's language. You did not write that. It came free, because "
            "every edit was already an object that could describe itself."
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
            "So, what to remember. [[slnc 300]] Make the action an object, with "
            "execute, undo and describe. Capture the state undo will need inside "
            "execute, from the receiver — never in the constructor. The invoker "
            "holds a stack of the interface and knows nothing else. And a new "
            "kind of edit is one class, with no working file reopened. [[slnc "
            "350]] Now the honest part, because a pattern video that only lists "
            "benefits is selling you something. [[slnc 250]] Every operation "
            "becomes a class. For four edits that will never change, the naive "
            "version is a third of the code and it works — use it. Command pays "
            "when undo, logging or queuing is a real requirement. [[slnc 250]] "
            "The inverse is yours to get right; the pattern gives you a place to "
            "put undo, it does not check that yours is correct. And reads should "
            "not be commands — nothing to undo, nothing to log. [[slnc 300]] "
            "Finally, know its sibling. Command stores the difference and needs "
            "each edit to know its inverse. Memento stores the state and needs "
            "no inverses at all, at the cost of a copy per step. [[slnc 250]] "
            "And you have used this already: every Runnable handed to an "
            "executor is a command without an undo, and every database migration "
            "with an up and a down is a command with one."
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
            "",
            "Next in the behavioural series: the Template Method pattern.",
        ],
        narration=(
            "That's the command pattern. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in "
            "the repository — including the exercise I would most recommend: "
            "move that capture out of execute and into the constructor, run the "
            "suite, and watch exactly one test go red. Understanding which test, "
            "and why it is that one, is worth more than the rest of this video. "
            "[[slnc 300]] If this helped, a like genuinely does help other people "
            "find it, and subscribe if you would like the rest of the behavioural "
            "series — the template method pattern is next. [[slnc 250]] Thanks "
            "for watching, and I'll see you in the next one."
        ),
    ),
]
