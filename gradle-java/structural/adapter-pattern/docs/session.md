# Session Guide — Adapter Pattern

A 60-minute guided session for teaching or self-studying the Adapter
pattern using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/adapter-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Adapter pattern solves.
2. Explain why `AcmeShippingAdapter` holds an `AcmeShippingSdk` field
   instead of subclassing it or modifying it.
3. Identify the four roles — target, adaptee, adapter, client — in real
   code.
4. Predict what happens to client code when a provider is swapped for a
   natively compatible one, versus an adapted one.
5. Distinguish Adapter from Bridge.

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

**Do not show `ShippingRateProvider`/`AcmeShippingAdapter` yet.** Start
with the pain.

Put `NaiveCheckoutService` and `NaiveShippingEstimator` from
[`problem-statement.md`](problem-statement.md) side by side and ask:

> *"These two classes both need a shipping rate from the same third-party
> SDK. What's duplicated between them?"*

Land on: the unit conversion (kg→lb, cents→dollars) is copy-pasted, and
both classes are coupled directly to `AcmeShippingSdk`'s exact method name
and parameter order.

**Key question to land:** *"If Acme changes `fetchCostInCents`'s
signature, or we switch carriers entirely, how many classes need to
change?"* Every single one that calls the SDK directly — and that count
only grows as more callers are added.

## 0:15–0:25 — The Pattern

Introduce the wall-plug analogy from
[`adapter-pattern-explained.md`](adapter-pattern-explained.md). Ask the
group: *"When you travel with a laptop charger, does the charger's
internal circuitry change based on which country's socket you plug into?"*
Land on: no — a small adapter in between translates the physical shape;
the charger and the wall socket never change.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the four roles. Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and trace a single
`quoteRate()` call translating into one `fetchCostInCents()` call.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice.

**The one point that must land:**

> If `CheckoutService` ever needs an `import` of `AcmeShippingSdk`, the
> pattern has not been applied — the whole point is that the client only
> ever knows about `ShippingRateProvider`.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The target — `ShippingRateProvider.java`**
Point out this interface declares exactly the shape checkout wants:
kilograms in, dollars out. Ask: *"Why doesn't this interface know
anything about Acme, pounds, or cents?"*

**2. The adaptee — `AcmeShippingSdk.java`**
Point out this class is intentionally awkward: pounds, cents, a
differently-named method. Ask: *"If we owned this class, would we even
need an adapter?"* No — we'd just change its shape directly. The adapter
exists because we don't own it.

**3. The adapter — `AcmeShippingAdapter.java`**
This is the heart of the session. Point at the `sdk` field and ask: *"Is
this inheritance or composition?"* Composition — and this class is the
only place in the entire codebase that imports `AcmeShippingSdk`. Trace
the two conversions: kg→lb before the call, cents→dollars after.

**4. The client — `CheckoutService.java`**
Ask: *"Which shipping provider does this class work with?"* Trick
question — it doesn't know, and doesn't care. Prove it by running the same
`CheckoutService` with `AcmeShippingAdapter` and then with
`FlatRateShippingProvider` live, showing identical calling code.

**5. The trap — `NaiveCheckoutService.java` / `NaiveShippingEstimator.java`**
Put the conversion block from both naive classes side by side. Ask:
*"These are identical. What happens when the pounds-per-kilogram constant
needs a bug fix?"* Two edits instead of one — and that gap grows with
every caller added.

**6. Run it — `ShippingDemo.java`**
Run `./gradlew run` live. Point at the section quoting the same weight
through both `AcmeShippingAdapter` and the naive classes, and show the
totals matching exactly — the naive code isn't wrong, just duplicated.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a second carrier (everyone)

Add a `SwiftCourierSdk` with its own quirky shape (e.g. grams in, a
`String` price like `"14.20"` out). Write
`SwiftCourierAdapter implements ShippingRateProvider` and confirm
`CheckoutService` works with it immediately, with zero changes to
`CheckoutService`.

> **The payoff:** a whole new carrier integration cost exactly one class.
> Say this out loud when someone finishes.

### Exercise 2 — Prove the client can't tell (everyone)

Write a small test or `main` snippet that constructs `CheckoutService`
with `AcmeShippingAdapter`, then again with `FlatRateShippingProvider`,
and confirms both produce a valid total using identical calling code.

### Exercise 3 — Break the adapter on purpose (discussion)

Add a `getSdk()` getter to `AcmeShippingAdapter` and have
`CheckoutService` call it directly for some special case. Discuss: *"What
did we just throw away?"* The whole point of the client staying ignorant
of the adaptee — now checkout is coupled to Acme again, exactly like the
naive trap.

### Exercise 4 — Stretch (for fast finishers)

Try adapting in the *other* direction: write a class that makes a
`ShippingRateProvider` usable somewhere that expects Acme's exact
`fetchCostInCents(String, double)` shape. Discuss why this feels more
awkward (you have to convert dollars back to cents and kilograms back to
pounds — going against the grain of the units you started with).

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- Adapter is a translator, not a place to add new behavior like retries or
  caching — that belongs in a decorator.
- One adapter per incompatible source — don't grow a single adapter to
  branch on which SDK it's wrapping.
- Don't adapt what you already control — if you own both sides, just
  change one side to match the other.

Then the comparison table. The line worth memorising:

> **Adapter reconciles two interfaces that already exist and disagree.
> Bridge designs two hierarchies from the start so they never have to
> agree on more than one seam.**

Close with real-world sightings: `Arrays.asList`, `InputStreamReader`,
JDBC-ODBC bridges, and every vendor-SDK wrapper class anyone has ever
written.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one place in your own codebase where a third-party library's shape
> leaks directly into more than one caller — a payment gateway SDK or a
> cloud storage client are common ones — and sketch what a single adapter
> class would look like.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "Isn't this the same as Bridge?" | No — Bridge designs two hierarchies together up front so they never disagree; Adapter reconciles an interface someone else already designed, after the fact |
| "Why not just modify `AcmeShippingSdk` to match `ShippingRateProvider`?" | You often can't — it's a third-party dependency you don't own the source of. Even when you can, editing it means every future SDK upgrade risks losing your changes |
| "This feels like overkill for one carrier" | Fair, at this size. The payoff shows up the moment a second caller or a second carrier appears — that's when duplicated conversion logic becomes a real cost |
| "Shouldn't `CheckoutService` cache the rate itself?" | Caching is a separate concern from adapting; it would belong in a decorator wrapping `ShippingRateProvider`, not inside the adapter |

**If you are running short on time:** cut Exercise 4 and shorten the
pitfalls discussion. Never cut Exercise 3 — hitting the "what did we throw
away" moment is where the value of keeping the client ignorant of the
adaptee actually lands.

**If you have extra time:** have participants implement
`SwiftCourierAdapter` from Exercise 1 fully, with its own test class
mirroring `AcmeShippingAdapterTest`.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/adapter-pattern-explained.mp4`) — useful
      as a recap for anyone who joins late, or to send round afterwards
- [ ] The printed shipping quote output from `./gradlew run` ready to put
      on the board
- [ ] IDE font size raised for screen sharing
