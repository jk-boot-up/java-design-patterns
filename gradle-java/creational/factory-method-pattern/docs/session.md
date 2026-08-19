# Session Guide — Factory Method Pattern

A 60-minute guided session for teaching or self-studying the Factory Method
pattern using this project.

- **Audience:** beginners comfortable with core Java, including inheritance
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the ~7.5 minute video
> (`video/factory-method-pattern-explained.mp4`) beforehand. If they do, you
> can compress the problem and pattern segments and spend the extra time on
> the exercises. If you are teaching a group that has *not* watched it, run
> the session exactly as written below.
>
> **Even better pre-work:** run the sibling
> [`../../simple-factory-pattern`](../../simple-factory-pattern) session
> first. Half the value of this session comes from the contrast.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Factory Method pattern solves.
2. Identify the four roles — product, concrete products, creator, concrete
   creators — in real code.
3. Explain what it means for a parent class to call a method it does not
   implement.
4. Add a new variant to a Factory Method hierarchy without editing any
   existing class.
5. State why Factory Method satisfies the Open/Closed Principle where Simple
   Factory does not.
6. Say honestly when Factory Method is *too much* machinery for the job.

## Timetable

| Time | Segment | Mode |
| --- | --- | --- |
| 0:00–0:05 | Setup check | Hands-on |
| 0:05–0:15 | The problem | Discussion |
| 0:15–0:25 | The pattern | Explanation |
| 0:25–0:40 | Code walkthrough | Live coding |
| 0:40–0:50 | Exercises | Hands-on |
| 0:50–0:58 | Pitfalls & comparisons | Discussion |
| 0:58–1:00 | Wrap-up | — |

## 0:00–0:05 — Setup Check

Everyone runs:

```bash
java -version
./gradlew run
```

Anyone whose build fails pairs up with a neighbour. Do not debug installs
during the session — that is what the prerequisites doc is for.

## 0:05–0:15 — The Problem

**Do not show `DeliveryService` yet.** Start with the pain.

Put the naive `ShippingService` from
[`problem-statement.md`](problem-statement.md) on screen and ask:

> *"We are launching drone delivery on Monday. Which file do you open?"*

They will answer "this one". That is the hook. Follow with:

> *"And this class already ships real parcels for four tiers today. How do
> you feel about editing it?"*

Guide the group to name the problems themselves:

- The `if` chain sits *inside* the workflow it varies.
- Adding a tier means editing code that already works.
- A partner module cannot add a tier at all.
- The workflow and the choosing cannot be tested apart.

**Key question to land:** *"The four log lines are the same for every tier.
Why are they inside a method that also does the choosing?"*

If someone proposes "move the `if` into a factory class" — excellent, they
have just re-invented Simple Factory. Acknowledge it, note that it fixes the
duplication but still means editing one central file on Monday, and park it
until 0:50.

## 0:15–0:25 — The Pattern

Introduce the coffee-shop-chain analogy from
[`factory-method-pattern-explained.md`](factory-method-pattern-explained.md):
head office owns the recipe card, the branch owns step 2. Let a participant
retell it back — if they can, they understand it.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the four roles. Trace the `creates` arrows with a finger and say:
*"four arrows, four different classes. In Simple Factory all four left the
same box."* Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and follow the
`createCourier()` call down into the subclass and back up.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice — useful when participants revisit it alone
afterwards.

**The one point that must land:**

> The parent class calls a method it does not implement. The child decides
> what comes back.

Expect this to feel strange. It is worth two full minutes at the whiteboard:
draw `ship()` in the parent box, draw the arrow going *down* to the child,
and the returned `Courier` coming back *up*.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The product interface — `Courier.java`**
Two methods, no implementation. Ask: *"What does a class holding one of
these know about aeroplanes?"* Nothing.

If anyone did the Simple Factory session, ask why this interface is not
`sealed`. Target answer: this pattern exists so new products can arrive from
outside; sealing would slam that door.

**2. A concrete product — `AirCourier.java`**
Point out how small and unaware it is. Ask: *"Does it know what an Express
tier is?"* No.

Skim `PostalCourier`, `BikeCourier`, `GlobalCourier` — same shape. Note that
`GlobalCourier` prints two lines: products are free to differ.

**3. The value objects — `Order.java`, `Shipment.java`**
Cover the `record` primer if needed. One object in, one object out.

**4. The creator — `DeliveryService.java`**
This is the heart of the session. Read `ship(...)` line by line and have the
group label each line as **shared** or **varies**. They will find exactly one
line that varies: `createCourier()`.

Then the three questions worth asking:

- *"Where is `createCourier()` implemented?"* Nowhere in this file.
- *"So what happens when this line runs?"* It lands in the subclass.
- *"Why is `ship` marked `final`?"* So a subclass can change the courier and
  nothing else.

**5. The concrete creators — `ExpressDelivery.java` and friends**
Six lines each. Show all four in quick succession; the repetition is the
point. Then ask the group to search the whole project for `switch`. There is
none. Let that sit for a moment.

**6. The client — `FactoryMethodDemo.java`**
One loop, four tiers, four carriers. Ask what the loop body knows about
carriers. Nothing.

**7. The tests — `DeliveryServiceTest.java`, `CourierTest.java`**
Show `newTierNeedsNoExistingChange` — it invents a whole drone tier as an
anonymous subclass inside the test, and the shared workflow picks it up for
free. Show `guardAppliesToEveryTier` — one guard, written once, enforced on
every tier including ones that do not exist yet.

Run `./gradlew run` live. Point out that the tier lines are structurally
identical across all four blocks and only the courier lines differ. That
visual is worth more than any slide.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add drone delivery (everyone)

Write `DroneCourier` and `DroneDelivery`, then add one line to the demo's
list.

> **The payoff:** ask everyone who finishes *"how many existing files did
> you edit?"* The answer is one — the demo, and only because it is a demo.
> Say this out loud; it is the lesson of the whole session.

### Exercise 2 — Prove the base class is decoupled (everyone)

Search `DeliveryService.java` for any courier class name. There is none.
Now search the whole project for `switch`. Also none. Discuss what replaced
it: the JVM's own method dispatch.

### Exercise 3 — Break it on purpose (everyone)

Delete the `createCourier()` override from `SameDayDelivery`. Compile. Read
the error. The compiler is enforcing the pattern for you.

Then try `new DeliveryService()` and read that error too.

### Exercise 4 — Spot the anti-pattern (discussion)

Present a `DeliveryService` subclass that overrides `createCourier()` *and*
declares its return type as `AirCourier` *and* adds a public
`getAirCourier()`. Ask: *"What have we lost?"* Everything — the creator's
callers can now depend on a concrete courier again.

### Exercise 5 — Stretch (for fast finishers)

Replace the whole hierarchy with a single `DeliveryService` class that takes
a `Supplier<Courier>` in its constructor. It works, it is shorter, and it
needs no subclasses at all. Ask: *when* is that better, and when do you
actually want the subclass? Target answer: the moment a tier needs to differ
in more than one way, or needs a name, or needs its own state.

There is no universally right answer here — that is the discussion.

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- A class per variant — do not build a hierarchy to avoid a two-line
  `switch`.
- Something still has to pick the creator; that decision often becomes a
  Simple Factory, and that is fine as long as you notice.
- Never call the factory method from a constructor.
- Keep the return type abstract.
- Inheritance is a permanent commitment; Strategy is the composition answer.

Then the comparison table. The line worth memorising:

> **Simple Factory chooses with a `switch`. Factory Method chooses with
> inheritance. Abstract Factory chooses a whole family at once.**

If the group did the Simple Factory session, put both class diagrams side by
side on screen. The arrow patterns tell the whole story without words.

Close with real-world sightings: `Collection.iterator()`,
`DocumentBuilderFactory.newDocumentBuilder()`, and any framework class that
says "extend this and override one method".

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one place in your own codebase where a method's shape is identical
> across cases but one step differs, and sketch the Factory Method that
> would replace the branch.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "So the factory method is a class?" | No — it is one method. The class around it is the *creator* |
| "Isn't this the same as Simple Factory?" | Simple Factory chooses with a `switch` in one class; here nothing switches and the choice is a subclass |
| "Why not just pass the courier in?" | You can — that is composition, and it is often right. The subclass earns its place when a tier differs in more than one way |
| "The parent calls a method with no body — is that legal?" | Yes, and it is the entire pattern. Draw it on the board |
| "Four subclasses to avoid four `if` branches?" | A fair objection. The payoff is Monday's fifth tier, and code you do not own |
| "Is this the Template Method pattern?" | Very close cousins — `ship(...)` *is* a template method. Factory Method is the special case where the varying step creates an object |

**If you are running short on time:** cut Exercise 5 and shorten the
pitfalls discussion. Never cut Exercise 1 — it is where the concept actually
lands.

**If you have extra time:** open the sibling Simple Factory project and have
participants convert it to Factory Method, then argue about which version
they would rather maintain. There is a real trade here and the argument is
the learning.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/factory-method-pattern-explained.mp4`) —
      useful as a recap for anyone who joins late, or to send round
      afterwards
- [ ] Naive `ShippingService` snippet ready to show first
- [ ] Simple Factory class diagram ready for the 0:50 comparison
- [ ] IDE font size raised for screen sharing
