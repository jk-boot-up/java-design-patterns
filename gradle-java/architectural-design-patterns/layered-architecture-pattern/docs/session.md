# Session Guide — Layered Architecture Pattern

A 60-minute guided session. The shape to protect is that the four-layer
diagram takes five minutes and the rest of the hour is spent on the one line
that breaks it and the test that catches that line — the diagram is the part
everyone already has; the enforcement is the part this session is actually
for.

## Learning Objectives

By the end of the session a participant can:

1. Name the four layers, what each one is allowed to know, and draw the one
   direction dependencies are allowed to point.
2. Show, from the source, a shortcut that skips a layer and explain why it
   compiles and passes review.
3. Read an ArchUnit rule and say in plain English what it forbids.
4. State the forced change performed in this project and the exact count of
   files it touched.
5. Say, without hedging, one application size at which this architecture is
   not worth building.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup, and the class nobody would reject in review |
| 0:05–0:15 | No layers at all |
| 0:15–0:25 | Four layers, and the one call that ruins them |
| 0:25–0:35 | The rule, as a test |
| 0:35–0:48 | The forced change, counted |
| 0:48–0:55 | Exercises |
| 0:55–1:00 | When this is too much, and wrap-up |

## 0:00–0:05 — Setup, And The Class Nobody Would Reject

Everyone runs:

```bash
cd architectural-design-patterns/layered-architecture-pattern
./gradlew -q run
```

Put `naive/presentation/OrderHistoryScreen.java` on the screen. Ask the room:
would this pass code review? Most hands go up. It is short, it reads clearly,
it compiles, and the tests pass. Land the point: **that is exactly the
problem.** Nothing about this class looks wrong until you know what it costs
later, which is the rest of the session.

## 0:05–0:15 — No Layers At All

Read act one of the output together, then open `EverythingOrderService`.
Seventy-four lines, one class, doing validation, pricing, storage and email
together.

Ask: how would you write a test for "three lines price to £382.50" without
touching storage? Let the room try. There is no seam — the pricing
arithmetic and the storage map are fields of the same object.

## 0:15–0:25 — Four Layers, And The One Call That Ruins Them

Read acts two and three together. Act two is the real four layers, working.
Act three is `OrderHistoryScreen` taking the shortcut.

```
  that screen skipped the application layer and read storage directly.
  it compiles, it is tidy, the tests pass, and it shipped.
  NOTHING IN THE BUILD OBJECTED.
```

Ask the room to find the one import that causes this. It is
`InMemoryOrderTable`, the concrete class, in a file under `presentation`.
Point out: a reviewer reading this diff in isolation, without the other
three layers open beside it, has almost no way to catch it.

## 0:25–0:35 — The Rule, As A Test

Open `ArchitectureTest.java`. Read the first rule aloud, in English, before
looking at the code:

> No class in the presentation package may depend on a class in the
> infrastructure package.

Then show the ArchUnit statement and map each word onto the sentence. Run:

```bash
./gradlew test --tests ArchitectureRuleCatchesTheShortcutTest
```

Read the printed failure message together. Ask the room to find
`OrderHistoryScreen` and `InMemoryOrderTable` in it by name. That message is
the product — it is the thing a developer sees at the moment they would
otherwise have shipped the shortcut.

## 0:35–0:48 — The Forced Change, Counted

Read act five. Put the numbers on the board:

```
  files added     : 1
  files modified  : 1
  lines changed   : 1
  classes in the four layers : 17
  of those, never opened     : 16
```

Ask: which sixteen classes never had to be opened? Walk the room through
`AppendOnlyOrderTable` — a different storage strategy entirely — and the one
line in `PlaceAnOrderDemo` that switches to it. Then reread the shortcut
report: `OrderHistoryScreen` does not compile after this change, because it
imported the concrete class rather than the interface. The sixteen
untouched classes and the one broken naive class are the same argument, told
twice.

## 0:48–0:55 — Exercises

1. **Add a fifth layer scene.** Write a class in `presentation` that calls
   `ProductTable` directly, run `./gradlew test`, and read the failure
   message it produces. Revert it afterwards.
2. **Trace an import.** Starting from `PlaceOrderService`, list every class
   it imports, and say which layer each one is in. Which layer does it never
   import from?
3. **Price a hypothetical.** If a new field were added to the checkout form,
   list every file that would need to change to carry it from the screen to
   storage. Is four files reasonable for this application's size?

## 0:55–1:00 — When This Is Too Much, And Wrap-Up

Ask the room directly: at what size of application does building four
layers and an architecture test cost more than it returns? Push for a
concrete answer — "a script with one calculation and one caller" is the
right shape of answer, not "it depends".

Close with the one sentence worth remembering: a layered architecture is not
the four folders. It is the test that fails when somebody reaches past one.
