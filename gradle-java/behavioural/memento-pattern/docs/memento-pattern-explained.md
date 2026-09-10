# The Memento Pattern, Explained

> **Without violating encapsulation, capture and externalize an object's
> internal state so that the object can be restored to this state later.**
> — Gang of Four

Two halves, and the first one is the one people skip. Capturing state is easy;
anybody can copy some fields. Capturing it *without violating encapsulation* —
so that the thing holding the copy still cannot see inside the object — is the
part that takes a pattern.

In this project the object is a shopping basket, the copy is a
`BasketSnapshot`, and the thing holding the copies is an undo stack called
`BasketHistory` that manages to do its whole job without knowing that a basket
contains anything at all.

## A Photograph, Not a Window

Here is the mistake this pattern exists to prevent, in one line:

```java
savedLines = lines;      // this saves nothing
```

That records *where* the list is, not *what is in it*. The saved list and the
live list are the same list, so every later edit changes the save too. When
undo eventually runs `lines.clear()`, it clears the very list it was about to
restore from, and the shopper's basket comes back empty.

The snapshot does this instead:

```java
this.lines = List.copyOf(lines);
```

A copy, taken at the moment of saving, that nothing can reach afterwards. A
photograph of the basket rather than a window onto it. Everything else in the
pattern is arrangement; this line is the substance.

## Everyday Analogy: The Sealed Envelope

You are about to rearrange a room. Before you start, you take a photograph, put
it in an envelope, seal it, and hand the envelope to a friend.

Your friend can hold it. They can keep several, in order, and hand you back
whichever one you ask for. What they cannot do is open it — and they do not
need to, because putting the room back is your job, not theirs. They only have
to remember which envelope is which, which is why you write "before I moved the
sofa" on the outside.

That is the whole pattern. The basket is you, the snapshot is the sealed
envelope, the history is the friend, and the label written on the outside is
the one thing the friend is allowed to read.

## Participants

| Role | In this project | Its job |
| --- | --- | --- |
| **Originator** | `Basket` | Knows what its state is. Writes snapshots and reads them back — nobody else does either. |
| **Memento** | `BasketSnapshot` | Holds a complete, immutable copy. Public on the outside, opaque on the inside. |
| **Caretaker** | `BasketHistory` | Holds snapshots and hands them back. Never opens one. |
| **Client** | `BasketUndoDemo` | Presses the buttons. |

## Code Walkthrough

### The memento, and its two interfaces

```java
public final class BasketSnapshot {

    private final List<BasketLine> lines;
    private final String voucher;
    private final String label;

    BasketSnapshot(List<BasketLine> lines, String voucher, String label) {
        this.lines = List.copyOf(lines);
        this.voucher = voucher;
        this.label = label;
    }

    public String label() { return label; }     // the wide interface

    List<BasketLine> lines()  { return lines; }     // the narrow one:
    String voucher()          { return voucher; }   // package-private
}
```

The books describe a memento as having a *wide* interface for the originator
and a *narrow* one for everyone else. In Java you get that for free with the
default access level. `label()` is public, so an undo menu can display "undo:
removed the laptop stand". `lines()` and `voucher()` have no modifier at all,
so only classes in `com.jk.explore.memento` — which means `Basket` — can call
them.

The constructor is package-private too. The only way to get a snapshot is to
ask a basket for one.

### The originator

```java
public BasketSnapshot save(String label) {
    return new BasketSnapshot(lines, voucher, label);
}

public void restore(BasketSnapshot snapshot) {
    lines.clear();
    lines.addAll(snapshot.lines());
    this.voucher = snapshot.voucher();
}
```

Six lines, and they are the only six in the project that know what a basket's
state is. That is the property worth protecting: add a delivery date next
month, and undo keeps working the moment you have added it to these two
methods. Nothing outside the class needs to hear about it.

Note that `restore` reads the snapshot without changing or consuming it. The
same snapshot can be restored twice, which is what makes redo — or a branching
history — possible later without touching any of these classes.

### The caretaker

```java
public class BasketHistory {

    private final Deque<BasketSnapshot> undoStack = new ArrayDeque<>();

    public void record(Basket basket, String label) {
        undoStack.push(basket.save(label));
        if (undoStack.size() > MAX_UNDO_STEPS) {
            undoStack.removeLast();
        }
    }

    public String undo(Basket basket) {
        BasketSnapshot snapshot = undoStack.pop();
        basket.restore(snapshot);
        return snapshot.label();
    }
}
```

Read this class looking for something it cannot do. It never opens a snapshot,
because the methods that would let it are not visible from here. Undo works
without this class knowing that a basket contains lines, or a voucher, or a
price.

That is why it is worth building the feature this way rather than by making the
basket's fields public. Both give you undo. Only one of them leaves the basket
as private as it was before you started.

### Why the copy can be shallow

`List.copyOf` copies the list, not the objects in it. That would be dangerous if
those objects could change — you would be sharing them between the snapshot and
the live basket. They cannot: `BasketLine` is a record, so it is immutable, and
a thing that never changes is safe to share.

That pairing is worth remembering as a general rule. **Immutable parts make a
shallow copy safe. Mutable parts make it a bug waiting to be found.**

## Why the Tests Are the Proof

A test that says "undo restores the basket" passes here and fails on the naive
version, which is a start. Two of the sixteen go further.

`laterChangesCannotReachBackIntoAnOlderSnapshot` empties the basket completely
*after* taking the snapshot, then restores. If the snapshot were an alias
rather than a copy, there would be nothing to come back to. This is the
aliasing bug, written as an assertion.

`SnapshotEncapsulationTest` walks `BasketSnapshot`'s declared methods by
reflection and fails if any public one is outside a small allowed list. A
comment saying "the caretaker must not read a snapshot" survives exactly as
long as the first person in a hurry. Add a public getter and this test names
the method back at you.

And `NaiveBasketTest` asserts the *wrong* answers on purpose — the empty
basket, the voucher that will not come back — so the cost of the alternative is
something the build says out loud rather than something a README claims. Fix
`NaiveBasket` and those tests go red, which is exactly right: being broken is
its entire job.

## What You Gain

- **Undo without opening the object up.** The basket's fields are as private
  after this feature as they were before it.
- **One place that knows the state.** New field, two methods to update, undo
  still correct.
- **Snapshots you can stack.** Multi-level undo is the same three classes and a
  `Deque`.
- **Restore is repeatable.** Nothing is consumed, so redo and branching
  histories are additions rather than rewrites.

## What to Watch Out For

**Memory.** Each snapshot is a full copy. Twenty snapshots of a big basket is
twenty baskets, and `BasketHistory` caps the stack for exactly that reason. If
the state is genuinely large, the alternative is the Command pattern, where you
store the *change* rather than the *state* — smaller, but every operation then
needs a working inverse.

**Deep versus shallow.** The copy here is shallow and safe because the parts are
immutable. Put a mutable object in a basket line and this stops being true, and
it stops being true silently.

**Snapshotting at the wrong moment.** `record` must be called *before* the
change it describes. Call it after and every undo is one step off — a bug that
looks like the pattern failing when it is really the caller.

**Do not reach for it when the state is one field.** If undo means putting one
`int` back, remember the `int`. This earns its keep when "the state" is several
fields that must move together, which is precisely when a hand-rolled undo
starts forgetting one of them.

## Memento vs. Command vs. Prototype

All three copy or replay something, and they get confused constantly.

| | What it stores | Undo works by |
| --- | --- | --- |
| **Memento** | the *state*, before the change | putting the old state back |
| **Command** | the *operation*, and its arguments | running the inverse operation |
| **Prototype** | a copy, to make new objects from | not an undo pattern at all |

Memento is the one to reach for when states are small and operations are
awkward to invert — which is most editing. Command wins when the state is huge
and every operation has a clean inverse. And Prototype shares the machinery of
copying but none of the intent: it copies an object so you can have another
one, not so you can go back.

## Where You Have Already Seen It

- **Every undo button you have ever pressed.** Editors, drawing tools,
  spreadsheets, and the "restore this version" button on a document.
- **Database transactions.** `BEGIN` takes a snapshot in spirit; `ROLLBACK`
  restores it.
- **Java serialization** and its modern replacements, when used to store an
  object's state and read it back later.
- **`git stash`.** The stash is a caretaker holding mementos, and it hands them
  back without interpreting them.

## Try It Yourself

1. **Break the copy.** Change `List.copyOf(lines)` to just `lines` in the
   snapshot's constructor and run the tests. Watch
   `laterChangesCannotReachBackIntoAnOlderSnapshot` fail, and note that nothing
   throws — it just quietly returns the wrong basket.
2. **Break the encapsulation.** Make `lines()` public on `BasketSnapshot` and
   watch `SnapshotEncapsulationTest` name the method back at you. This is the
   exercise most worth doing; it is the moment the structural promise stops
   being a comment.
3. **Add a third field.** Give `Basket` a gift message, and make undo cover it.
   You should be editing two methods and nothing else.
4. **Add redo.** A second `Deque`, and the observation that `restore` never
   consumed the snapshot. It is about ten lines.

## See Also

- [`problem-statement.md`](problem-statement.md) — the version without a
  snapshot, and why it fails twice
- [`class-diagram.md`](class-diagram.md) — the static structure
- [`uml-diagram.md`](uml-diagram.md) — one undo, message by message
- [`animation.html`](animation.html) — the same undo, stepped through
