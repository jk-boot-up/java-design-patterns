# Session Guide — Memento Pattern

A 60-minute session plan for teaching the Memento pattern from this project.
Written for a facilitator working with beginners; every timing is a
suggestion, and the exercises are the part worth protecting if you run late.

**Audience:** developers who can write a class with a few fields, and who have
at some point been surprised to find that two variables were pointing at the
same object.

**Setup:** everyone has the project cloned and `./gradlew test` passing before
the session starts. See [`prerequisites.md`](prerequisites.md).

## Learning Objectives

By the end, participants can:

1. Explain why `saved = live` saves nothing, and what a snapshot has to do
   instead.
2. Name the three roles — originator, memento, caretaker — and say which one is
   allowed to look inside a snapshot.
3. Write an undo feature without making the object's state public.
4. Say what a memento costs (memory) and when the Command pattern is the better
   trade.
5. Say why a shallow copy is safe here, and exactly what would make it unsafe.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check |
| 0:05–0:17 | The problem |
| 0:17–0:27 | The pattern |
| 0:27–0:40 | Code walkthrough |
| 0:40–0:50 | Exercises |
| 0:50–0:58 | Pitfalls and comparisons |
| 0:58–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check

Have everyone run:

```bash
./gradlew test    # 16 tests
./gradlew run
```

Anyone whose tests fail should pair for the session rather than debug.

Then, before showing any code, put this on the board and ask the room what it
prints:

```java
List<String> live  = new ArrayList<>(List.of("a", "b"));
List<String> saved = live;
live.add("c");
System.out.println(saved);
```

Take a show of hands for `[a, b]` against `[a, b, c]`. In a beginner room the
hands will split, and the split *is* the session — the entire naive
implementation is that one misunderstanding, wearing a business feature as a
disguise. Leave the snippet on the board.

## 0:05–0:17 — The Problem

Open [`problem-statement.md`](problem-statement.md) and set the scene: a basket
with lines and a voucher, and a ticket that says "add an undo button".

Show `NaiveBasket.save()` and `NaiveBasket.undo()` side by side and ask whether
they look like opposites. They do. Then run `./gradlew run` and read the first
section out loud together: the shopper removes one line, presses undo, and gets
an empty basket.

Two things to draw out, in this order:

1. **The aliasing.** Walk it slowly with the board snippet: `savedLines` and
   `lines` are one list, so `lines.clear()` clears the save, and `addAll` then
   copies nothing back. Nobody wrote a bug; somebody wrote `=`.
2. **The omission.** The voucher was never saved. Ask "what code review would
   have caught this?" and let the silence do the work — there is no line to
   review, which is what makes this class of bug different.

Then ask what happens when the basket grows a delivery date next month. The
answer — undo goes quietly half-right again — is the argument for the pattern.

## 0:17–0:27 — The Pattern

Give the definition, and split it deliberately:

> Without violating encapsulation, capture and externalize an object's internal
> state so that the object can be restored to this state later.

Everyone can do the second half. The first half is the pattern.

Use the sealed envelope analogy: you photograph the room, seal the photo in an
envelope, and hand it to a friend. They can hold several, in order, and give
you back whichever you ask for. They cannot open one, and do not need to,
because putting the room back is your job.

Then name the three roles against the analogy — you are the originator, the
envelope is the memento, the friend is the caretaker — and ask the room which
one is allowed to look inside. It is worth making them say it.

## 0:27–0:40 — Code Walkthrough

In this order:

1. **`BasketSnapshot`** — start with the access modifiers, not the fields.
   `label()` is public; `lines()` and `voucher()` have no modifier at all. Ask
   what that means, and land on: only classes in this package, which means only
   `Basket`. That is the wide-and-narrow interface, with no framework involved.
2. **The constructor**, and `List.copyOf`. Point back at the board snippet.
   This is the one line that separates a photograph from a window.
3. **`Basket.save` and `Basket.restore`** — six lines, and the only six in the
   project that know what a basket's state is. Ask what changes if a gift
   message is added tomorrow. Answer: these two methods, and nothing else.
4. **`BasketHistory`** — read it looking for something it *cannot* do. It never
   opens a snapshot. Undo works without this class knowing a basket contains
   anything.
5. **`SnapshotEncapsulationTest`** — the structural assertion, and why a comment
   would not have held.

## 0:40–0:50 — Exercises

### Exercise 1 — Break the copy (everyone)

In `BasketSnapshot`'s constructor, change `List.copyOf(lines)` to `lines`. Run
the tests.

`laterChangesCannotReachBackIntoAnOlderSnapshot` fails. The point to draw out
is that nothing *throws* — the snapshot quietly becomes a window, and undo
starts returning a basket that is wrong rather than a basket that is missing.

Put it back afterwards.

### Exercise 2 — Break the encapsulation (everyone)

Make `lines()` public on `BasketSnapshot`. Run the tests, and watch
`SnapshotEncapsulationTest` name the method back at you.

This is the exercise most worth protecting if you are short of time. It takes
a minute, and it is the moment the structural promise stops being a comment.

### Exercise 3 — Add a third field (most people)

Give `Basket` a gift message with a getter and a setter, and make undo cover
it. Participants should find themselves editing `save`, `restore` and the
snapshot's fields — and nothing else. Ask what they would have had to edit in
`NaiveBasket`, and how they would have known to.

### Exercise 4 — Stretch (for fast finishers)

Add redo. A second `Deque`, plus the observation that `restore` never consumed
the snapshot, gets it done in about ten lines. Then ask what should happen to
the redo stack when the shopper makes a *new* change after undoing — there is a
right answer, and finding it is the interesting part.

## 0:50–0:58 — Pitfalls and Comparisons

**Memory.** Every snapshot is a full copy. Show `MAX_UNDO_STEPS` and ask why
it is there. If the state were a 200 MB document, this pattern as written would
be the wrong tool.

**Memento vs. Command.** Memento stores the *state* before the change; Command
stores the *operation* and runs an inverse. Memento is smaller to write and
bigger to hold. Command is the other way round, and needs every operation to
have a genuine inverse — ask the room what the inverse of "clear the basket"
is, given that it has to restore the order of the lines too.

**Deep versus shallow.** Ask why the shallow copy is safe here. The answer is
`BasketLine` being a record. Then ask what breaks if someone gives it a setter.
Nothing, visibly — which is the point.

**Snapshot timing.** `record` must be called *before* the change it describes.
Called after, every undo is one step off, and it looks like the pattern failing
when it is the caller.

## 0:58–1:00 — Wrap-Up

One sentence to leave them with:

> Undo is not "do the opposite". Undo is "put back the copy you took" — and the
> object that made the copy is the only one that ever needs to see it.

Point at [`memento-pattern-explained.md`](memento-pattern-explained.md) for the
written version, and [`animation.html`](animation.html) for the stepped
walkthrough.

## Facilitator Notes

- **The board snippet earns its five minutes.** Almost every question later in
  the session — why copy, why immutable lines, why the naive version empties
  the basket — resolves back to it, and it is much cheaper to resolve there
  than in the middle of the walkthrough.
- **Do not skip running the naive version.** Reading it convinces nobody;
  watching a basket empty itself convinces everybody.
- **Expect the "why not just make the fields public?" question**, and welcome
  it. It is the right question, and the honest answer is that it works, and
  costs the basket's encapsulation permanently to buy one feature once.
- **Expect a room split on Memento vs. Command.** Both are correct answers to
  "how do I do undo"; the choice is about the size of the state versus the
  invertibility of the operations, and saying that plainly settles it.

## Materials Checklist

- [ ] Project cloned, `./gradlew test` green (16 tests)
- [ ] `./gradlew run` output visible to the room
- [ ] Board or slide with the aliasing snippet
- [ ] [`class-diagram.md`](class-diagram.md) and
      [`uml-diagram.md`](uml-diagram.md) open in a tab
- [ ] [`animation.html`](animation.html) open in a browser, for the walkthrough
