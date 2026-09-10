# Session Guide — Mediator Pattern

A 60-minute session plan for teaching the Mediator pattern from this project.
Written for a facilitator working with beginners; every timing is a
suggestion, and the exercises are the part worth protecting if you run late.

**Audience:** developers who can write a class that holds a reference to
another class, and who have at some point wired two things together directly
and regretted it.

**Setup:** everyone has the project cloned and `./gradlew test` passing before
the session starts. See [`prerequisites.md`](prerequisites.md).

## Learning Objectives

By the end, participants can:

1. Explain why *n* objects that talk to each other cost *n*² and why a hub
   costs *n*.
2. Name the two roles — mediator and colleague — and say which one is allowed
   to know things.
3. Write a mediator for a set of interacting objects, and keep the colleagues
   ignorant of each other.
4. Say what a mediator's failure mode is (the god object) and what to do about
   it.
5. Tell Mediator apart from Observer, and say why the difference is knowledge
   and direction rather than mechanism.

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
./gradlew test    # 14 tests
./gradlew run
```

Anyone whose tests fail should pair for the session rather than debug.

Then, before showing any code, draw five boxes on the board labelled Country,
Shipping, Gift wrap, Total, Place Order, and ask: **"Which of these affect
which?"** Let the room call out arrows and draw every one of them. You will
end up with a picture nobody can read, in about ninety seconds, and that
picture is the entire motivation for the session. Leave it on the board.

## 0:05–0:17 — The Problem

Open [`problem-statement.md`](problem-statement.md) and set the scene: five
controls, four rules, and the difficulty is where the rules live.

Then open `NaiveCheckoutForm` and read the constructor out loud:

```java
country.wire(shipping, giftWrap, total, placeOrder);
shipping.wire(giftWrap, total, placeOrder);
giftWrap.wire(shipping, total);
```

Nine references, five controls. Point back at the board.

Now run the demo and read the first section together:

```
gift wrap : offered=false, ticked=true   <-- still ticked
Total: £42   <-- £2 for wrapping that will not happen
place order : enabled   <-- no courier chosen, and it will let them through
```

Ask the room to find where each bug is. The valuable realisation is that
**neither bug is a line of code**. Both are a line that was never written.
Ask: how would you catch that in review? (You would have to hold the whole
form in your head and notice an absence. Nobody does this reliably at 5pm.)

## 0:17–0:27 — The Pattern

Redraw the five boxes, this time with a sixth in the middle, and one arrow
from each box to it. Count the arrows: five. Then do the arithmetic out loud —
3 controls, 5 controls, 10 controls; 6, 20, 90 versus 3, 5, 10.

Then the control tower analogy, which does most of the work with beginners.
Aircraft near an airport do not negotiate with each other; they all talk to
the tower. Not because pilots are untrustworthy, but because the rules of the
airspace need to be in one head.

Ask: **"What is the smallest thing a widget could say to the tower?"** Steer
towards "something about me changed" and then show:

```java
public interface CheckoutMediator {
    void changed(FormWidget source);
}
```

One method. Sit with how small that is for a moment; people expect a mediator
interface to be large, and the smallness is the point — colleagues report,
they do not ask.

## 0:27–0:40 — Code Walkthrough

Read the code in this order. Resist jumping to `CheckoutForm` first.

1. **`FormWidget`** — two fields. Ask what is *missing* before discussing what
   is there. There is no field that can hold another widget, so the tangle is
   not merely discouraged, it is unrepresentable.

2. **`CountrySelector`** — the whole class fits on the screen. `select` stores
   a country and announces. Put `NaiveCountry.select` next to it; that one is
   four statements about four other widgets and is still missing two.

3. **`CheckoutForm.changed`** — six lines. Read them, then say: you have now
   read the behaviour of the checkout page. There is nowhere else for a rule
   to be.

4. **`refreshTotal()` and `refreshButton()` run every time.** This is the
   moment worth slowing down for. Ask why the mediator does not check whether
   they *need* to run. Answer: because deciding that is exactly the judgement
   the naive form got wrong, and re-asking a cheap question is always right.

5. **`GiftWrapCheckbox.setAvailable`** — withdrawing the offer clears the tick
   in the same method. Ask whether that is "remembering to also untick it".
   It is not; there is no method that does only half.

6. **The package-private setters.** `showOptions`, `setAvailable`, `show`,
   `setEnabled`. The mediator pushes down; nothing outside the package can.
   Ask what would happen if `showOptions` called `announceChange()`. (A
   change storm. This is Exercise 3.)

7. **`WidgetIsolationTest`** — the structural promise, asserted by reflection.
   Run it. Then say: a comment saying "widgets must not reference each other"
   lasts until the first person in a hurry.

## 0:40–0:50 — Exercises

### Exercise 1 — Break the isolation (everyone)

Add a `private TotalLabel total;` field to `CountrySelector` and run the
tests.

`WidgetIsolationTest` fails and names the field. The discussion: this is the
first step of the tangle, and it is a step somebody takes for a *good* reason
every time.

### Exercise 2 — Add a sixth control (everyone)

Add a voucher-code field that takes £5 off the total. Do it in the mediated
form, and count the files touched. Then plan — do not write — the same change
in `NaiveCheckoutForm`, and count what it would touch.

The number people usually reach is two files versus five, and the naive
version needs new wiring in both directions.

### Exercise 3 — Cause a change storm (most people)

Make `ShippingSelector.showOptions` call `announceChange()` and run the
tests.

Watch what happens, then discuss why the mediator's push methods are silent.
This is a real failure mode of the pattern and it is worth seeing once, in a
safe place.

### Exercise 4 — Stretch (for fast finishers)

`CheckoutForm` is doing five jobs. Split it into a `DeliveryMediator` and a
`PaymentMediator` and decide how the two should talk. Should one of them be a
colleague of the other? Is there a mediator of mediators, and if so, when does
that stop helping?

## 0:50–0:58 — Pitfalls and Comparisons

Cover briefly, from
[`mediator-pattern-explained.md`](mediator-pattern-explained.md):

- **The god object.** The honest cost. Everything you take out of the widgets
  goes into the mediator. Split before it becomes unopenable.
- **Colleagues that ask instead of report.** A getter on the mediator brings
  the coupling back with an extra hop.
- **Change storms.** Exercise 3.
- **Using it on two controls.** Two things that affect each other and never
  will be three are clearer wired directly.

Then the comparison, which is the question that always comes up:

| | What it does | Who knows whom |
| --- | --- | --- |
| **Mediator** | Centralises the interaction between peers | Colleagues know the mediator; it knows all of them |
| **Observer** | Broadcasts an event to whoever is listening | Publisher knows nothing about subscribers |
| **Facade** | Simplifies a subsystem for outside callers | Facade knows the subsystem; it knows nothing of the facade |

The line worth saying explicitly: an Observer publisher deliberately knows
*nothing* about its subscribers; a mediator knows all its colleagues on
purpose, and that knowledge is what lets it enforce a rule spanning several of
them. A publisher could not disable a button because a drop-down was cleared.

## 0:58–1:00 — Wrap-Up

One sentence to leave in the room:

> **When everything talks to everything, nobody can see the whole thing. Give
> them one place to talk to, and the rules have somewhere to live.**

Point at [`animation.html`](animation.html) for anyone who wants to walk the
click again, and at the video for anyone who wants it narrated.

## Facilitator Notes

- **Draw the arrows on the board yourself, live.** The unreadable picture is
  worth far more than a slide of the same picture, because the room built it.
- **Do not skip running the naive demo.** "Charges £2 for gift wrapping it
  will never do" lands much harder as output than as a claim.
- **Expect "isn't this just an event bus?"** Good question. An event bus is
  closer to Observer: it does not know who is listening and cannot enforce a
  rule across listeners. A mediator knows its colleagues by name, and that is
  the whole point.
- **Expect "isn't the mediator now doing too much?"** Yes, and say so plainly.
  This is the one pattern whose main criticism is completely fair. The answer
  is not to deny it but to split mediators, and the exercise is there.
- **Watch the clock at 0:27.** The walkthrough overruns, and Exercises 1 and 3
  are where the learning happens.

## Materials Checklist

- [ ] Project cloned, `./gradlew test` green for everyone
- [ ] `docs/animation.html` open in a browser tab
- [ ] `docs/images/class-diagram.png` on screen for 0:17–0:27
- [ ] A whiteboard, kept clear for the five boxes at 0:00 and again at 0:17
- [ ] The video queued as optional follow-up
