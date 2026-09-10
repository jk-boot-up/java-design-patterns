"""Scene definitions for the Memento teaching video.

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
        title="Memento",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Memento pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. A memento is "
            "a sealed copy of an object's state, taken by that object, handed "
            "to somebody else to hold, and handed back later when you want to "
            "go back. It is how every undo button you have ever pressed works. "
            "[[slnc 350]] That's the idea in a sentence. The rest of the video "
            "does it properly, by building a real working Java project: the "
            "shopping basket of an online shop, with an undo button on it. "
            "[[slnc 250]] By the end you'll know why one equals sign is the "
            "difference between undo working and undo emptying the basket, how "
            "to let something save your state without ever being able to see "
            "it, and the one honest cost of this pattern."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The shopping basket of an online shop.",
            "",
            "Its state is two things:",
            "",
            "    the lines        2 x USB-C cable,  Laptop stand,  Desk mat",
            "    the voucher      SAVE5  —  £5 off the whole basket",
            "",
            "    total: £65",
            "",
            "And the ticket says:  add an undo button.",
            "",
            "Shoppers keep removing the wrong line, and then have to",
            "go and find the product again.",
        ],
        narration=(
            "So, imagine an online shop. [[slnc 250]] This is a shopper's "
            "basket. Three products, and a voucher code that takes five pounds "
            "off the whole thing. Sixty five pounds. [[slnc 300]] The basket's "
            "state is exactly two things: the lines in it, and the voucher. "
            "Remember that, because it matters in a minute. [[slnc 300]] And "
            "the ticket says, add an undo button. Shoppers keep removing the "
            "wrong line and then have to go and find the product again, so one "
            "step back would save them a lot of irritation. [[slnc 350]] That "
            "is the whole feature. It sounds like an afternoon's work, and this "
            "is one of those cases where the obvious afternoon's work is subtly "
            "wrong."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Look Closely at One Line",
        body=[
            "    savedLines = lines;",
            "",
            "That does not copy anything.",
            "",
            "It writes down WHERE the list is, not WHAT IS IN IT.",
            "The save and the live basket are now the same list.",
            "",
            "    lines.clear();            <- clears the save as well",
            "    lines.addAll(savedLines); <- copies nothing back",
            "",
            "The shopper presses undo, and their basket is empty.",
            "Nothing throws. Nothing logs.",
        ],
        narration=(
            "Before any code, look closely at one line. [[slnc 300]] Saved "
            "lines equals lines. [[slnc 300]] That does not copy anything. It "
            "writes down where the list is, not what is in it, so the saved "
            "list and the live list are the same list under two names. [[slnc "
            "350]] And then undo clears the live list, which is also the saved "
            "list, and copies the now-empty saved list back over it. [[slnc "
            "300]] Sit with that for a second, because it is the reason this "
            "pattern exists. The shopper presses undo and their basket is gone. "
            "Nothing throws. Nothing gets logged. Nobody wrote a bug — somebody "
            "wrote an equals sign."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Undo Without a Snapshot",
        body="""private final List<BasketLine> lines = new ArrayList<>();
private List<BasketLine> savedLines;
private String voucher = "";

public void save() {
    savedLines = lines;      // an alias, not a copy
                             // ...and nothing about the voucher
}

public void undo() {
    lines.clear();           // this clears savedLines too
    lines.addAll(savedLines);
}""",
        narration=(
            "Here's the whole thing. [[slnc 250]] Read those two methods side "
            "by side and they look like opposites. They are not. [[slnc 300]] "
            "The first bug we've just seen. The second one is quieter still. "
            "Look at what save doesn't mention. [[slnc 300]] The voucher. It is "
            "part of the basket's state, and it is not in the save at all. "
            "[[slnc 350]] And I want to be precise about the lesson, because it "
            "isn't that somebody was careless. Nobody decided not to save the "
            "voucher. It simply wasn't on anyone's mind on the day undo was "
            "written. There is no line of code you could review to find that "
            "out, because the bug is the absence of a line."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "1.  The bugs are silent and shaped like omissions.",
            "    An empty basket. A voucher that does not come back.",
            "",
            "2.  Every new field is a fresh chance to forget.",
            "    Add a delivery date and undo goes quietly half-right",
            "    again — once per field, forever.",
            "",
            "3.  The obvious fix is worse: make the fields public,",
            "    and buy one feature with the basket's encapsulation.",
            "",
            "4.  'Undo by doing the opposite' needs an inverse for",
            "    every operation — and a remove has no inverse",
            "    unless you already saved what it removed.",
        ],
        narration=(
            "Let's be precise, because it's four separate costs. [[slnc 300]] "
            "One. The bugs are silent, and they're shaped like omissions. An "
            "empty basket, and a voucher that doesn't come back. You cannot "
            "review a line that was never written. [[slnc 300]] Two. Every new "
            "field is a fresh chance to forget. Add a delivery date next month "
            "and undo goes quietly half right again, and it will keep doing "
            "that once per field, forever, because nothing connects the "
            "basket's state to what undo saves. [[slnc 300]] Three. The obvious "
            "fix is worse than the bug. Make the fields public so the undo code "
            "can reach in and copy them. That works, and it means anything at "
            "all can now edit a basket. You've bought one feature with the "
            "basket's encapsulation, permanently. [[slnc 350]] And four. Undo "
            "by doing the opposite sounds tidy until you try it. Removing a "
            "line undoes an add — but what undoes a remove? You'd have to know "
            "which line, and where it was in the list, and what the voucher was "
            "doing at the time. Which is to say: you'd have to have saved it."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Memento Pattern",
        # One line per rendered line: kind_quote lays these out as-is.
        body=[
            "Without violating encapsulation, capture and",
            "externalize an object's internal state so that the",
            "object can be restored to this state later.",
            "",
            "— Gang of Four",
            "",
            "Everyone can do the second half.",
            "'Without violating encapsulation' is the pattern.",
        ],
        narration=(
            "Here's the definition from the Gang of Four book. [[slnc 250]] "
            "Without violating encapsulation, capture and externalize an "
            "object's internal state, so that the object can be restored to "
            "this state later. [[slnc 350]] Two halves, and the first one is "
            "the one people skip. Capturing state is easy — anybody can copy "
            "some fields. Capturing it without violating encapsulation, so that "
            "the thing holding the copy still cannot see inside the object, is "
            "the part that takes a pattern. [[slnc 300]] In this project the "
            "object is a basket, the copy is a basket snapshot, and the thing "
            "holding the copies is an undo stack that manages to do its entire "
            "job without knowing that a basket contains anything at all."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "You are about to rearrange a room.",
            "",
            "  You photograph it.",
            "  You seal the photo in an envelope.",
            "  You hand the envelope to a friend.",
            "",
            "They can hold several, keep them in order, and give you",
            "back whichever one you ask for.",
            "",
            "They cannot open one — and they do not need to,",
            "because putting the room back is YOUR job.",
            "",
            "That is why you write on the outside: 'before I moved the sofa'.",
        ],
        narration=(
            "Here's the analogy to hold on to, and with this one, if you take "
            "nothing else away, take this. [[slnc 250]] You're about to "
            "rearrange a room. Before you start, you take a photograph, put it "
            "in an envelope, seal it, and hand the envelope to a friend. [[slnc "
            "350]] Your friend can hold it. They can keep several of them, in "
            "order, and hand you back whichever one you ask for. What they "
            "cannot do is open it. [[slnc 300]] And they don't need to, because "
            "putting the room back is your job, not theirs. They only have to "
            "remember which envelope is which — which is exactly why you write "
            "on the outside, before I moved the sofa. [[slnc 300]] That's the "
            "whole pattern. The basket is you, the snapshot is the sealed "
            "envelope, the undo stack is the friend, and the label on the "
            "outside is the one thing the friend is allowed to read."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So here are the pieces, and there are only three. [[slnc 250]] "
            "Basket is the originator. It's the only class that knows what the "
            "basket's state actually is, which is why it's the only class that "
            "writes a snapshot and the only class that reads one back. [[slnc "
            "300]] Basket snapshot is the memento. It holds a complete copy, "
            "and the interesting thing about it is the access modifiers rather "
            "than the fields — we'll come to that. [[slnc 300]] And basket "
            "history is the caretaker. It stacks snapshots up and hands them "
            "back, and it is defined by what it cannot do. [[slnc 250]] Notice "
            "that the history never touches the snapshot's contents. Every "
            "arrow that opens an envelope comes from the basket. That's the "
            "shape worth remembering."
        ),
    ),
    dict(
        key="09-memento",
        kind="code",
        title="The Memento — Two Interfaces, No Framework",
        body="""public final class BasketSnapshot {

    private final List<BasketLine> lines;
    private final String voucher;

    BasketSnapshot(List<BasketLine> lines, String voucher, String label) {
        this.lines = List.copyOf(lines);     // a COPY. this is the pattern.
        ...
    }

    public String label() { return label; }        // the wide interface

    List<BasketLine> lines() { return lines; }     // the narrow one:
    String voucher()         { return voucher; }   // package-private""",
        narration=(
            "Here's the memento, and there are two things in it. [[slnc 300]] "
            "The first is list dot copy of. A copy, taken at the moment of "
            "saving, that nothing can reach afterwards. A photograph of the "
            "basket rather than a window onto it. Everything else in this "
            "pattern is arrangement; that line is the substance. [[slnc 350]] "
            "The second is the access modifiers, and I'd read them before the "
            "fields. The books describe a memento as having a wide interface "
            "for the originator and a narrow one for everybody else. In Java "
            "you get that for free. [[slnc 300]] Label is public, so an undo "
            "menu can display, undo: removed the laptop stand. Lines and "
            "voucher have no modifier at all, which means only classes in this "
            "package can call them — and the only class in this package that "
            "wants to is the basket. [[slnc 300]] The constructor is "
            "package-private too. The only way to get a snapshot is to ask a "
            "basket for one."
        ),
    ),
    dict(
        key="10-originator",
        kind="code",
        title="The Originator and the Caretaker",
        body="""public BasketSnapshot save(String label) {         // on Basket
    return new BasketSnapshot(lines, voucher, label);
}

public void restore(BasketSnapshot snapshot) {
    lines.clear();
    lines.addAll(snapshot.lines());
    this.voucher = snapshot.voucher();
}

public String undo(Basket basket) {               // on BasketHistory
    BasketSnapshot snapshot = undoStack.pop();
    basket.restore(snapshot);                     // hand it back.
    return snapshot.label();                      // never open it.
}""",
        narration=(
            "And here's the other half. [[slnc 300]] Six lines on the basket, "
            "and they are the only six in the project that know what a basket's "
            "state is. That's the property worth protecting. Add a gift message "
            "next month and undo keeps working the moment you've added it to "
            "these two methods — nothing outside the class needs to hear about "
            "it. [[slnc 350]] Notice also that restore reads the snapshot "
            "without consuming it, so the same one could be restored twice. "
            "That's what makes redo a ten-line addition later rather than a "
            "rewrite. [[slnc 300]] And then the caretaker. Read it looking for "
            "something it cannot do. It pops a snapshot, hands it to the "
            "basket, and reads the label. It never opens one, because the "
            "methods that would let it aren't visible from there. [[slnc 300]] "
            "Undo works, and the undo stack does not know that a basket "
            "contains lines."
        ),
    ),
    dict(
        key="11-proof",
        kind="code",
        title="The Tests — Asserting the Structure, Not Just the Behaviour",
        body="""@Test void nothingPublicOnASnapshotGivesUpTheBasket() {
    for (Method m : BasketSnapshot.class.getDeclaredMethods())
        if (isPublic(m) && !ALLOWED.contains(m.getName()))
            offenders.add(m.getName());

    assertEquals(List.of(), offenders);
}

@Test void undoEmptiesTheBasketInstead() {        // the NAIVE basket
    basket.save();
    basket.remove("Laptop stand");
    basket.undo();
    assertEquals(0, basket.itemCount());          // the wrong answer,
}                                                 // pinned on purpose""",
        narration=(
            "Sixteen tests, and these two are the ones that prove the pattern. "
            "[[slnc 300]] A test saying undo restores the basket is a fine "
            "test, but it doesn't say anything about the design. [[slnc 300]] "
            "The first one here asserts the structure. It walks the snapshot's "
            "declared methods by reflection and fails if any public one is "
            "outside a small allowed list. [[slnc 300]] Because a comment "
            "saying, the caretaker must not read a snapshot, survives exactly "
            "as long as the first person who is in a hurry. This doesn't. Add a "
            "public getter and it names the method back at you. [[slnc 350]] "
            "And the second one is the interesting one, because it asserts the "
            "wrong answer. It pins the naive version's empty basket in place, "
            "with a message explaining why. [[slnc 300]] Fix the naive version "
            "and its own tests go red. That's deliberate. Being broken is its "
            "entire job, and the cost of that design should be something the "
            "build says out loud rather than something a README claims."
        ),
    ),
    dict(
        key="12-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== undo without a snapshot ===
  the basket the shopper built:   4 items,  SAVE5,  £65
  after removing the laptop stand by mistake:   3 items,  £31
  after pressing undo:
    (the basket is empty)
    total: £0            <- no exception, no log, just an empty basket

=== undo with a snapshot ===
  the basket the shopper built:   4 items,  SAVE5,  £65
  after removing the laptop stand by mistake:   3 items,  £31
  after pressing undo (removed the laptop stand):
    2 x USB-C cable  £18     1 x Laptop stand  £34     1 x Desk mat  £18
    voucher: SAVE5           total: £65""",
        narration=(
            "Run it, and the two halves sit side by side. [[slnc 250]] Same "
            "basket. Same mistake. Same click on undo. [[slnc 300]] The top "
            "half is the version without a snapshot. The shopper removes one "
            "line, presses undo, and gets an empty basket and a zero pound "
            "total. No exception. Nothing in the log. Just a basket that is "
            "gone. [[slnc 350]] The bottom half is the mementoed one. The line "
            "is back, the voucher is back, the total is back. [[slnc 300]] And "
            "here's the part I'd frame. Nobody wrote any code that says, when "
            "you undo, remember the voucher as well. The voucher came back "
            "because a snapshot is complete by definition — it is the basket's "
            "state, all of it, taken by the only object that knows what that "
            "means."
        ),
    ),
    dict(
        key="13-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "Undo is not 'do the opposite'.",
            "Undo is 'put back the copy you took' — and the object that",
            "took the copy is the only one that ever needs to see it.",
            "",
            "  Memento    stores the STATE, and puts it back",
            "  Command    stores the OPERATION, and inverts it",
            "  Prototype  copies an object to make another one —",
            "             same machinery, nothing to do with undo",
            "",
            "The honest cost: every snapshot is a full copy.",
            "Twenty snapshots is twenty baskets, which is why the",
            "history caps the stack.",
            "",
            "And a shallow copy is only safe because BasketLine",
            "is immutable. Give it a setter and this stops being true —",
            "silently.",
        ],
        narration=(
            "So, what to take away. [[slnc 300]] Undo is not, do the opposite. "
            "Undo is, put back the copy you took — and the object that took the "
            "copy is the only one that ever needs to see it. [[slnc 350]] On "
            "the comparison, because this is the question I'd expect. Memento "
            "and command are both correct answers to how do I do undo, and they "
            "get confused constantly. Memento stores the state before the "
            "change and puts it back. Command stores the operation and runs an "
            "inverse. [[slnc 300]] Memento is smaller to write and bigger to "
            "hold. Command is the other way round, and it needs every operation "
            "to have a genuine inverse — so ask yourself what the inverse of "
            "clear the basket is, given that it has to restore the order of the "
            "lines too. And prototype shares the machinery of copying but none "
            "of the intent: it copies an object so you can have another one, not "
            "so you can go back. [[slnc 350]] Now the honest bill. Every "
            "snapshot is a full copy, so twenty snapshots of a big basket is "
            "twenty baskets. That's why the history caps the stack, and if your "
            "state is genuinely large, command is the better trade. [[slnc "
            "300]] And one thing to watch that catches people out. The copy "
            "here is shallow, and it's safe because basket line is a record — a "
            "thing that never changes is safe to share. Give it a setter and "
            "that stops being true, and it stops being true silently. Immutable "
            "parts make a shallow copy safe. Mutable parts make it a bug waiting "
            "to be found."
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that makes",
            "one method public, and watches a test name it.",
        ],
        narration=(
            "That's the memento pattern. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in "
            "the repository — including the exercise I'd most recommend. Make "
            "the snapshot's lines method public, run the tests, and watch the "
            "encapsulation test name the offending method back at you. It takes "
            "a minute, and it's the moment the structural promise stops being a "
            "comment. [[slnc 300]] If this helped, a like genuinely does help "
            "other people find it, and subscribe if you'd like the rest of the "
            "behavioural series. [[slnc 250]] Thanks for watching, and I'll see "
            "you in the next one."
        ),
    ),
]
