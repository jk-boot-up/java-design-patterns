# Session Guide — Facade Pattern

A 60-minute guided session for teaching or self-studying the Facade
pattern using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the ~6.5 minute video
> (`video/facade-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on
> the exercises. If you are teaching a group that has *not* watched it,
> run the session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Facade pattern solves.
2. Identify the three roles — facade, subsystems, client — in real code.
3. Explain why the dependency arrow points only one way.
4. Write a small facade over two or more existing services.
5. Say when a facade is the *wrong* choice.
6. Distinguish Facade from Adapter, Mediator and Proxy.

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

**Do not show the facade yet.** Start with the pain.

Put the naive checkout code from
[`problem-statement.md`](problem-statement.md) on screen and ask:

> *"A new team member has to add checkout to the mobile API. What do they
> have to know?"*

Guide the group to name the problems themselves:

- They must know all four services exist.
- They must know the correct order.
- Nobody stops them charging the card before checking stock.
- The same eight lines now live in three places.

**Key question to land:** *"What happens when we add a fraud check?"*
Answer: every caller changes.

## 0:15–0:25 — The Pattern

Introduce the waiter analogy from
[`facade-pattern-explained.md`](facade-pattern-explained.md). Let a
participant retell it back — if they can, they understand it.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the three roles. Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and trace one call with
a finger.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice — useful when participants revisit it alone
afterwards.

**The one point that must land:**

> The facade knows about the subsystems. The subsystems do **not** know
> about the facade.

Ask why that matters. Target answer: the services stay reusable on their
own.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. A subsystem — `InventoryService.java`**
Point out how small and unaware it is. Ask: *"Could I use this class in a
totally different app?"* Yes. That is the point.

Skim `PaymentService`, `ShippingService`, `NotificationService` — same
shape, no surprises.

**2. The value objects — `OrderRequest.java`, `OrderConfirmation.java`**
Cover the `record` primer if anyone is new to it. Emphasise: one object in,
one object out.

**3. The facade — `OrderFacade.java`**
This is the heart of the session. Walk through `placeOrder` and ask the
group to spot what it is actually doing. Draw out three answers:

- **sequencing** the four calls,
- **guarding** — no charge if stock fails,
- **assembling** three results into one confirmation.

Ask: *"How many lines of business logic are in here?"* Almost none — it
delegates. That is what keeps it a facade and not a god object.

**4. The client — `FacadeDemo.java`**
Three lines. Ask what it knows about payments. Nothing.

**5. The tests — `OrderFacadeTest.java` and `SubsystemsTest.java`**
`OrderFacadeTest` hands the facade four recording subsystems and asserts the
*order* it called them in, that it passed the request through untouched, and
that an order refused for stock is never charged, shipped or emailed.
`SubsystemsTest` defends the opposite requirement: every service is still
public and still usable on its own. Ask the room which of those two would
break first if somebody "tidied up" by making the services package-private.

Run `./gradlew run` live and map each printed line back to a class.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a step (everyone)

Create `FraudCheckService` with
`boolean isSuspicious(String customerId, double amount)`.
Call it from the facade **before** payment and throw if suspicious.

> **The payoff:** `FacadeDemo` does not change at all. Say this out loud
> when someone finishes — it is the lesson of the whole session.

### Exercise 2 — Prove the guard rail (everyone)

Make `reserveStock` return `false`. Run the demo. Confirm the customer is
never charged, then add a test asserting no payment line is printed.

### Exercise 3 — Spot the anti-pattern (discussion)

Present a facade that validates addresses, calculates tax, applies
discounts and writes an audit log. Ask: *"Is this still a facade?"*
No — it has absorbed business logic. A facade delegates; it does not decide.

### Exercise 4 — Stretch (for fast finishers)

Extract an interface for each subsystem and inject them through the
constructor. Discuss what this buys (mocking in tests, swapping providers)
and what it costs (more files, more indirection).

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- A facade is not a god object.
- Do not forbid direct subsystem access — a facade is a convenience, not a
  wall.
- One facade per workflow, not one per application.

Then the comparison table. The line worth memorising:

> **Adapter changes an interface. Facade simplifies many of them.**

Close with real-world sightings: `JdbcTemplate`, `LoggerFactory`, and the
observation that most REST controllers are already facades.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one place in your own codebase where a caller wires together three
> or more services, and sketch the facade that would replace it.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "It's just a wrapper class" | A wrapper wraps *one* thing; a facade unifies *many* |
| "So subsystems become private?" | No — they stay public and independently usable |
| "Isn't this the same as Adapter?" | Adapter matches an *expected* interface; facade invents a *simpler* one |
| "Facades make things slower" | It is one extra method call — irrelevant next to a network hop |

**If you are running short on time:** cut Exercise 4 and shorten the
pitfalls discussion. Never cut Exercise 1 — it is where the concept
actually lands.

**If you have extra time:** have participants write a second facade over a
returns/refund workflow using the same four services.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/facade-pattern-explained.mp4`) — useful as a
      recap for anyone who joins late, or to send round afterwards
- [ ] Naive checkout snippet ready to show first
- [ ] IDE font size raised for screen sharing
