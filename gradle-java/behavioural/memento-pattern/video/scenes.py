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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Memento pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A memento is a sealed copy '
            "of an object's state. [[slnc 300]] The object takes the copy "
            'itself, and hands it to someone else to keep. [[slnc 300]] '
            'Later, when you want to go back, the copy is handed back, '
            'and the object restores itself. [[slnc 600]] Think of a save '
            'point in a video game. [[slnc 300]] The game saves '
            'everything about your progress. [[slnc 300]] If things go '
            'wrong, you load the save, and you are back where you were. '
            '[[slnc 700]] In this video, we add an undo button to the '
            'shopping basket of an online shop. [[slnc 500]] By the end, '
            'you will know why one equals sign can make undo empty the '
            'whole basket. [[slnc 300]] How to let something keep your '
            'state without ever seeing inside it. [[slnc 300]] And the '
            'one honest cost of this pattern.'
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
            "Here is the scenario. [[slnc 400]] A shopper's basket holds "
            'three products, and a voucher code worth five pounds off. '
            '[[slnc 300]] The total is sixty-five pounds. [[slnc 500]] '
            "The basket's state is exactly two things. [[slnc 300]] The "
            'lines in it, and the voucher. [[slnc 300]] Remember that, '
            'because it matters soon. [[slnc 500]] The request is simple: '
            'add an undo button. [[slnc 300]] Shoppers keep removing the '
            'wrong item, and then have to find the product again. [[slnc '
            "500]] It sounds like an afternoon's work. [[slnc 300]] But "
            "the obvious afternoon's work is quietly wrong."
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
            "Before any code, let's look closely at one line. [[slnc "
            '400]] Saved lines equals lines. [[slnc 500]] That line does '
            'not copy anything. [[slnc 300]] It records where the list '
            'is, not what is in it. [[slnc 300]] So the saved list and '
            'the live list are the same list, under two names. [[slnc '
            '600]] Then undo clears the live list. [[slnc 300]] Which '
            'also clears the saved list, because they are the same list. '
            '[[slnc 300]] Then it copies the empty saved list back. '
            '[[slnc 600]] So the shopper presses undo, and their whole '
            'basket disappears. [[slnc 300]] Nothing crashes, and nothing '
            'is logged. [[slnc 300]] Nobody wrote a bug on purpose. '
            '[[slnc 300]] Somebody wrote an equals sign.'
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
            'Here is the naive version in full. [[slnc 400]] One method '
            'to save, and one to undo. [[slnc 300]] They look like '
            'opposites, but they are not. [[slnc 500]] The first bug we '
            'just heard. [[slnc 300]] The second is even quieter. [[slnc '
            '300]] Think about what the save method never mentions. '
            '[[slnc 300]] The voucher. [[slnc 300]] It is part of the '
            "basket's state, but it is not saved at all. [[slnc 600]] "
            'Nobody decided to leave it out. [[slnc 300]] It just was not '
            "on anyone's mind the day undo was written. [[slnc 300]] And "
            'there is no line of code to review, because the bug is a '
            'missing line.'
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
            'So what exactly is wrong? [[slnc 300]] Four separate things. '
            '[[slnc 500]] One. [[slnc 200]] The bugs are silent, and they '
            'are missing lines. [[slnc 300]] An empty basket, and a '
            'voucher that never comes back. [[slnc 500]] Two. [[slnc '
            '200]] Every new field is another chance to forget. [[slnc '
            '300]] Add a delivery date next month, and undo becomes '
            'half-right again. [[slnc 500]] Three. [[slnc 200]] The '
            "obvious fix is worse. [[slnc 300]] Make the basket's fields "
            'public, so the undo code can copy them. [[slnc 300]] That '
            'works, but now anything at all can change a basket. [[slnc '
            '500]] And four. [[slnc 200]] Undoing by doing the opposite '
            'sounds tidy, until you try it. [[slnc 300]] Removing a line '
            'undoes an add. [[slnc 300]] But what undoes a remove? [[slnc '
            '300]] You would need to know which line it was, where it '
            'sat, and what the voucher was. [[slnc 300]] In other words, '
            'you would need to have saved it.'
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
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Without breaking encapsulation, '
            "capture an object's internal state and store it outside, so "
            'the object can be restored to that state later. [[slnc 600]] '
            'Anyone can copy some fields. [[slnc 300]] The hard part is '
            'doing it without breaking encapsulation. [[slnc 300]] That '
            'means whoever holds the copy still cannot see inside it. '
            '[[slnc 500]] In this project, the object is the basket. '
            '[[slnc 300]] The copy is a basket snapshot. [[slnc 300]] And '
            'the undo history keeps the snapshots, without ever knowing '
            'what a basket contains.'
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
            'Here is the analogy to hold on to. [[slnc 400]] You are '
            'about to rearrange a room. [[slnc 300]] First, you take a '
            'photograph of it. [[slnc 300]] You seal the photo in an '
            'envelope, and hand it to a friend. [[slnc 500]] Your friend '
            'can keep several envelopes, in order. [[slnc 300]] And hand '
            'back whichever one you ask for. [[slnc 300]] But they cannot '
            'open them. [[slnc 500]] They do not need to, because putting '
            'the room back is your job, not theirs. [[slnc 300]] They '
            'only need to know which envelope is which. [[slnc 300]] So '
            'you write a label on the outside, such as, before I moved '
            'the sofa. [[slnc 600]] In our project, the basket is you. '
            '[[slnc 300]] The snapshot is the sealed envelope. [[slnc '
            '300]] The undo history is your friend. [[slnc 300]] And the '
            'label is the only thing your friend may read.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'So here are the pieces, and there are only three. [[slnc '
            '500]] The Basket is called the originator. [[slnc 300]] It '
            'is the only class that knows what its state is. [[slnc 300]] '
            'So it is the only class that creates a snapshot, and the '
            'only one that reads one back. [[slnc 500]] The Basket '
            'Snapshot is the memento. [[slnc 300]] It holds a complete '
            "copy of the basket's state. [[slnc 500]] And the Basket "
            'History is called the caretaker. [[slnc 300]] It stacks up '
            'snapshots, and hands them back. [[slnc 300]] It is defined '
            'by what it cannot do: it cannot look inside a snapshot. '
            '[[slnc 500]] Only the basket ever opens the envelope.'
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
            'Now the snapshot itself, and two details matter. [[slnc '
            '500]] First, when it is created, it makes a real copy of the '
            "basket's lines. [[slnc 300]] Not a reference to the live "
            'list, but a copy that nothing can change afterwards. [[slnc '
            '300]] A photograph of the basket, not a window onto it. '
            '[[slnc 300]] That single step is the heart of the pattern. '
            '[[slnc 600]] Second, the access rules. [[slnc 300]] The '
            'label can be read by anyone, so an undo menu can show, undo: '
            'removed the laptop stand. [[slnc 300]] But the lines and the '
            'voucher can only be read by classes in the same package. '
            '[[slnc 300]] And the only class there that wants them is the '
            'basket. [[slnc 500]] Even creating a snapshot is restricted. '
            '[[slnc 300]] The only way to get one is to ask a basket for '
            'it.'
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
            'Now the other half, the basket and the history. [[slnc 500]] '
            'The basket has two short methods. [[slnc 300]] Save creates '
            'a snapshot of its lines and voucher. [[slnc 300]] Restore '
            "empties its lines, copies the snapshot's lines back, and "
            'restores the voucher. [[slnc 500]] These are the only lines '
            "in the project that know what a basket's state is. [[slnc "
            '300]] Add a gift message next month, update these two '
            'methods, and undo keeps working. [[slnc 300]] Nothing '
            'outside the basket needs to know. [[slnc 500]] Restore does '
            'not use up the snapshot, so it could be restored twice. '
            '[[slnc 300]] That makes adding redo later a small change. '
            '[[slnc 600]] And the history. [[slnc 300]] To undo, it takes '
            'the latest snapshot, hands it to the basket, and reads the '
            'label. [[slnc 300]] It never opens the snapshot, because it '
            'simply cannot. [[slnc 300]] Undo works, and the history does '
            'not even know a basket has lines.'
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
            'The project has sixteen tests. [[slnc 300]] Two of them '
            'prove the pattern. [[slnc 500]] The first checks the '
            'structure. [[slnc 300]] It looks at every public method on '
            'the snapshot. [[slnc 300]] And it fails if any method '
            "outside a small allowed list could reveal the basket's "
            'contents. [[slnc 300]] A comment saying, the history must '
            'not read a snapshot, lasts until someone is in a hurry. '
            '[[slnc 300]] This test does not. [[slnc 500]] The second '
            'test checks a wrong answer, on purpose. [[slnc 300]] It '
            'confirms that the naive basket still empties itself on undo. '
            "[[slnc 300]] Being broken is that version's job, and the "
            'build says so out loud.'
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
            "Let's run the demo. [[slnc 400]] The same basket, the same "
            'mistake, and the same press of undo. [[slnc 500]] First, the '
            'version without a snapshot. [[slnc 300]] The shopper removes '
            'one item by mistake, and presses undo. [[slnc 300]] The '
            'basket is now empty, and the total is zero. [[slnc 300]] No '
            'error. [[slnc 200]] Nothing in the log. [[slnc 300]] The '
            'basket is just gone. [[slnc 500]] Now the memento version. '
            '[[slnc 300]] The item is back, the voucher is back, and the '
            'total is back to sixty-five pounds. [[slnc 600]] Notice that '
            'nobody wrote code saying, when you undo, remember the '
            'voucher too. [[slnc 300]] The voucher came back because a '
            'snapshot is complete by definition. [[slnc 300]] It is the '
            "basket's whole state, taken by the only object that knows "
            'what that means.'
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
            'So, what should you remember? [[slnc 400]] Undo is not, do '
            'the opposite. [[slnc 300]] Undo is, put back the copy you '
            'took. [[slnc 300]] And only the object that took the copy '
            'ever needs to see inside it. [[slnc 600]] People often '
            'confuse Memento with Command, because both can build undo. '
            '[[slnc 300]] Memento saves the state before a change, and '
            'puts it back. [[slnc 300]] Command saves the operation, and '
            'runs its reverse. [[slnc 400]] Memento is simpler to write, '
            'but uses more memory. [[slnc 300]] Command is the other way '
            'round, and every operation needs a true reverse. [[slnc '
            '500]] And Prototype also copies objects, but for a different '
            'reason. [[slnc 300]] It copies an object to make another '
            'one, not to go back in time. [[slnc 600]] Now the honest '
            'cost. [[slnc 300]] Every snapshot is a full copy. [[slnc '
            '300]] Twenty snapshots of a big basket means twenty baskets '
            'in memory. [[slnc 300]] That is why the history limits how '
            'many it keeps. [[slnc 500]] One more warning. [[slnc 300]] '
            'The copy here is shallow, and that is only safe because each '
            'basket line can never change. [[slnc 300]] Give a line a '
            'setter, and the copy quietly stops being safe.'
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
            "That's the Memento pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Undo means putting '
            'back a sealed copy, taken by the only object that is allowed '
            'to open it. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            "300]] Make the snapshot's lines method public. [[slnc 300]] "
            'Run the tests, and listen as the encapsulation test names '
            'that method. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
