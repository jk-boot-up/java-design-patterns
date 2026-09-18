# The Backends for Frontends Pattern, Explained

## In One Sentence

> Give each frontend its own backend, owned by the team that owns the screen, whose
> only job is to turn what the shop knows into the exact shape that one screen draws.

Three words in that sentence are doing all the work.

**Each.** More than one. A single shared endpoint in front of your services is a
perfectly good pattern, but it is a different one — it is an API gateway or an API
composition, and neither of them is this. This pattern only exists in the plural.

**Own.** Not "a backend the platform team provides for the phone". A backend the
*phone team* changes, tests, and ships. If a phone-only field has to be negotiated
with another team, you have the shape of the pattern and none of its benefit.

**Shape.** Not rules. Not prices, not tax, not whether a discount may be
advertised. The backend decides what a product looks like to one screen; the shop
decides what a product *is*. Get that line wrong and the pattern's worst failure —
two screens telling a customer different things — is waiting for you.

## Everyday Analogy: Two Waiters, One Kitchen

A restaurant has one kitchen and two rooms. The dining room takes couples who
settle in for two hours; the counter by the window takes people who have twenty
minutes before a train.

The kitchen cooks the same food for both.

Now give both rooms the same waiter, working from one script. He has to satisfy
both, so his script becomes the union of everything either room might want: he
recites the full wine list, the provenance of the lamb, the specials, the dessert
menu, and the allergen sheet, to everybody. The couple enjoy it. The commuter
misses their train.

The fix is not a second kitchen. The food is the same food, and a second kitchen
would be two places for a recipe to live. The fix is a second waiter, who works the
counter, knows that his customers want the answer to "what can I eat in twenty
minutes", and is allowed to change his own script tomorrow morning without
consulting the dining room.

That is the whole pattern. The kitchen is the shop's services. The waiter is the
backend. Each room gets its own waiter; both waiters walk to the same kitchen; and
neither waiter is allowed to invent a price.

And to keep the analogy honest, the restaurant now pays for two waiters. That is
the bill this project spends its second half on.

## The Problem, In The Shop

One product — a copper coffee maker, SKU-4417. Two screens.

The phone draws six things: title, price, one photograph, the star rating, the
number of ratings, and one sentence saying when the parcel arrives.

The desktop page draws fifteen: all of the above plus the brand, the full
description, the materials, the dimensions, five large photographs, the previous
price, the saving, three written reviews, the stock figure, and a strip of related
products.

The shop has five services that between them hold all of it: catalog, pricing,
inventory, reviews, recommendations.

**Design one — the phone calls all five itself.** Five round trips across a mobile
network, in sequence, before a pixel appears. Twenty-nine fields arrive; six are
drawn.

**Design two — one shared endpoint returns the union.** One round trip, which is a
real improvement. But 87% of the bytes are discarded on arrival, and when the phone
team asks for one new field — a delivery sentence joined from stock, the delivery
rules and the clock — the change has to be agreed with every other client that
receives the same document. They wait five weeks for an afternoon's work.

That second failure is the one that matters, and it is organisational rather than
technical. A `?fields=` query parameter fixes the bytes completely. Nothing fixes
ownership except giving each client something of its own.

## The Pattern

```
  phone app  ──────────►  MobileBff   ─┐
                                       ├──► catalog · pricing · inventory
  desktop    ──────────►  WebBff      ─┘        · reviews · recommendations

  ▲ one call each,                     ▲ four or five calls each,
    over the customer's                  inside the data centre,
    connection                           where they are nearly free
```

Read that in words. Each client makes exactly one call, to a backend that belongs
to it. That backend makes four or five calls to the shop's services, all of them
inside the data centre. It then builds one document containing exactly the fields
its screen draws, in the form the screen draws them, and sends it back.

Two things move, and they are different in kind:

- **Calls move off the expensive network.** Five device calls become one; the four
  that disappeared reappear internally. The work did not go away.
- **Decisions move out of the app.** Formatting `4799` as `"£47.99"`, joining three
  services into an English sentence, choosing a 320-pixel thumbnail over a
  2000-pixel hero image. All of it now happens in a process that can be corrected
  this afternoon, rather than in an app store release that customers may not install
  for two years.

## Participants

| Participant | In this project | Role |
| --- | --- | --- |
| Frontend | the phone app, the desktop store | Draws a screen. Owns a backend. |
| Backend for a frontend | `MobileBff`, `WebBff` | One call in, one screen-shaped document out. |
| The contract | `ClientBackend` | One method. Meaningful only because it has several implementations. |
| Downstream services | `Shop` | The five services that hold the data. Unchanged by the pattern. |
| Shared business rule | `SavingRules` | What the shop believes regardless of client. Must live behind the backends. |
| Entry concerns | `CrossCutting` | Token, rate limit, TLS, access log. Belong in front of all backends. |
| The estate | `ClientEstate` | How many backends the shop's clients actually justify. |
| The measurement | `CallLog`, `Doc`, `Screens` | Counts calls by origin, measures documents, records what each screen draws. |

Two of those deserve a note.

`ClientBackend` is one method and could be deleted without changing any behaviour.
It is here because it names the thing the pattern is about. As its own comment puts
it: what makes this the pattern is not the interface, it is that there is more than
one implementation of it and each is free to answer differently.

`Screens` is the project's ruler. Every claim about waste is measured against a
written-down list of what a human being can actually see on each screen, kept in
one file rather than implied by whichever class happens to be building a response.

## Code Walkthrough

### What each screen draws, written down once

```java
public static final List<String> PHONE = List.of(
        "title", "price", "image", "rating", "ratingCount", "delivery");
```

Six strings. Everything in this project that says "wasteful" means "not on that
list", and that is the only definition of waste it uses.

### Counting calls, in two columns

```java
public enum Origin {
    /** Across the customer's own connection. Slow, metered, and unreliable. */
    DEVICE,
    /** Inside the data centre, between our own processes. Fast and free. */
    INTERNAL
}
```

This enum is the honest bit of the project. The pattern is often sold as "fewer
calls", and that is not true — the same five services get called either way. What
changes is *which network* the calls cross. Counting them in one column would let
the project claim a saving it has not made, so it counts them in two.

### The shop, and why its data never moves

```java
public Doc pricing(String sku) {
    log.record(CallLog.Origin.INTERNAL, "pricing");
    return Doc.doc()
            .put("listPence", 5999)
            .put("nowPence", 4799)
            ...
            .put("listPriceHeldLongEnough", false);
}
```

Fixed values, not random ones, because a byte count that moved between runs could
not be quoted in a document or a narration. And note the last field: the shop
itself knows the higher price is too recent to advertise. It is not hiding
anything. Act 5 is about what each backend *does* with that field.

### The rejected design, and the version of it that works

```java
public Doc product(String sku, List<String> fields) {
    return product(sku).select(fields);
}
```

This is `?fields=`, and the project takes it seriously: it brings the response from
1755 bytes down to 212, which is close to what a tailored backend sends. If this
pattern were about payload size, a query parameter would be the answer and there
would be no new processes to run.

Then the next method:

```java
public static String joinedDelivery() {
    return "not available -- a field like this belongs to one client, and this "
            + "endpoint belongs to all of them";
}
```

A hard-coded string is a blunt way to make a point, and it is the point. There is
no code that could go here. The sentence the phone wants does not exist in any
service, and creating it on a shared endpoint means changing a document that six
clients receive.

### The phone's backend

```java
@Override
public Doc productScreen(String sku) {
    log.record(CallLog.Origin.DEVICE, "mobile-bff");
    Doc catalog = shop.catalog(sku);
    Doc pricing = shop.pricing(sku);
    Doc inventory = shop.inventory(sku);
    Doc reviews = shop.reviews(sku);

    return Doc.doc()
            .put("title", catalog.get("title"))
            .put("price", Money.format((int) pricing.get("nowPence")))
            .put("image", catalog.get("thumbnail"))
            .put("rating", reviews.get("average"))
            .put("ratingCount", reviews.get("count"))
            .put("delivery", deliveryPromise(inventory));
}
```

Read the document it returns before reading how it is built. Six fields, all flat,
all already in the form the screen draws them. The price is a string with a pound
sign in it. The delivery promise is a whole English sentence. Nothing is left for
the phone to work out.

Two details are worth pausing on.

**It calls four services, not five.** There is no `shop.recommendations(sku)` line,
because the phone's product screen does not show a related-products strip. The
backend knows what the screen draws, so it knows what not to ask for. A shared
endpoint cannot make that decision for anybody.

**`image` is the thumbnail.** The catalog holds five 2000-pixel images and one
320-pixel one. Choosing the small one for a four-inch screen is a presentation
decision, and it is being made here rather than in the app.

And the sentence itself:

```java
private static String deliveryPromise(Doc inventory) {
    boolean inStock = (boolean) inventory.get("inStock");
    if (!inStock) {
        return "Out of stock";
    }
    return "Free delivery, arrives " + inventory.get("nextDelivery");
}
```

Four lines. This is the field the phone team waited five weeks for on the shared
endpoint, written in the one place that is allowed to care about it.

### The desktop's backend, disagreeing

```java
return Doc.doc()
        .put("title", catalog.get("title"))
        .put("brand", catalog.get("brand"))
        .put("description", catalog.get("description"))
        ...
        .put("delivery", inventory.get("nextDelivery"))
        .put("stock", inventory.get("quantity"))
        .put("related", recommendations.get("related"));
```

Fifteen fields, and all five services called. Look at `delivery`: where the phone
got a sentence, the desktop gets the bare date. That is not an inconsistency to be
tidied up. The desktop page has a whole delivery panel and wants the parts so it
can lay them out; the phone has one line and wants the sentence.

Two backends over the same data, disagreeing about what a product is. That
disagreement is the pattern working.

## And Now The Bill

Everything above is in every write-up of this pattern. The three things below are
what it costs, and each of them is a real failure that happens in real systems
without announcing itself.

### One: shared logic in two places will diverge

The pricing team reviews the discount rule. The new rule has two conditions: the
higher price must genuinely have been in force long enough to be quoted, and the
saving must be at least five per cent.

```java
static SavingRules current() {
    return (listPence, nowPence, listPriceHeldLongEnough) -> {
        if (!listPriceHeldLongEnough) {
            return "";
        }
        int savedPence = listPence - nowPence;
        int percent = (savedPence * 100) / listPence;
        if (percent < 5) {
            return "";
        }
        return "Save " + Money.format(savedPence) + " (" + percent + "%)";
    };
}
```

The phone's backend, meanwhile, holds a copy taken before the review:

```java
static SavingRules copiedBeforeTheReview() {
    return (listPence, nowPence, listPriceHeldLongEnough) ->
            "Save " + Money.format(listPence - nowPence);
}
```

For SKU-4417 the higher price went up eleven days ago, so
`listPriceHeldLongEnough` is `false`, and the two rules part company:

```
  desktop store says:  (nothing — no saving may be claimed for this price)
  phone app says:      Save £12.00
```

Same product, same price, same second, and one of those screens is making a claim
the shop is not allowed to make. In most countries what a shop may advertise as a
saving is a matter of law, so this is a letter from a regulator rather than a bug
report.

Now the part worth saying out loud, because it is the reason this failure keeps
happening: **nothing about that copy is careless.** It was correct on the day it
was written. It is well named. It has tests, and the tests pass. It is wrong only
in relation to a decision made months later, somewhere else, by people who had no
reason to know a second copy existed. No exception is thrown. Nothing is logged.
The only person who can see the difference is a customer with both screens open.

The rule that prevents it: **a backend for a frontend may hold the shape.
Anything the shop would still believe with every client switched off belongs
behind it.** Discount eligibility, tax, stock allocation, what a price is — those
are the shop's beliefs. Which of the shop's five images to send is shape.

### Two: the shared jobs get done once per backend

Every request needs four things done to it, whoever sent it:

```java
public static final List<String> JOBS = List.of(
        "verify the customer's token",
        "refuse traffic over the rate limit",
        "terminate TLS",
        "write the access log");
```

```java
public static int copiesWhenEachBackendDoesIt(int backends) {
    return JOBS.size() * backends;
}

public static int copiesBehindAGateway() {
    return JOBS.size();
}
```

The second method takes no argument, and that absence is the answer. Behind a
gateway the number of copies does not depend on how many backends there are:

```
  each backend doing it itself: 8 copies across 2 backends
  a gateway in front:           4 copies, whatever the number of backends
```

Eight against four is not a dramatic number at two backends. Try it at six. And
notice how the mistake happens: the nearest place to put token verification is
inside whichever backend you happen to be editing this afternoon, and each
individual decision to do that is reasonable. Do it once per backend and the shop
has as many copies of its authentication code as it has clients, which is the
position it was in before it built a gateway.

The line is a single question, and it is worth memorising because it is also the
answer to "how is this different from an API gateway?":

- Does the code answer **"what does this screen need?"** → a backend for that frontend.
- Does the code answer **"is this request allowed in at all?"** → in front of all of them.

A gateway is about entry. A backend for a frontend is about shape. They are
neighbours and they are frequently deployed together, and they are not the same
pattern.

### Three: one backend per client is not the rule

The shop has six clients:

```
  phone app        own backend        six fields, one sentence, a four-inch screen
  desktop store    own backend        description, specification, five images, reviews
  tablet app       shares one         the phone's fields in a wider column
  smart TV app     own backend        no keyboard, so no search, and pictures do the work
  in-store kiosk   shares one         the desktop page with the basket hidden
  partner feed     shares one         not a screen at all — a nightly file

  one per client:            6 backends
  one per genuine disagreement: 3 backends
```

```java
public int backendsJustified() {
    return (int) clients.stream().filter(Client::disagreesAboutTheProduct).count();
}
```

The filter is the whole design rule expressed as code. It does not count devices
and it does not count teams. It counts clients that **disagree about what a product
is**.

Work through the three that share. The tablet shows the phone's six fields in a
wider column: it disagrees about layout, which is a stylesheet, not a backend. The
kiosk shows the desktop page with the basket hidden: same fields, one hidden. The
partner feed is not a screen at all — it is a nightly file, and it is served by
whichever backend already produces those fields.

And the reason to care, which is not servers:

```java
public static List<String> whatEachBackendCosts() {
    return List.of(
            "a pipeline to build and deploy it",
            "a place in the on-call rota",
            "a dependency upgrade every time a shop service changes",
            "one more process to look at during an incident");
}
```

Every item on that list recurs weekly, for as long as the backend exists, and none
of it appears on an infrastructure bill. Two backends is a pattern. Nine is a
department.

## What This Simulation Does Not Show

This project runs in one JVM with no network and no framework, which buys clarity
and costs realism. Being explicit about what is missing:

**There is no network.** `Shop` returns in microseconds. Every claim this project
makes about round trips is made by *counting* them, not by timing them, which is
why `CallLog` separates device calls from internal ones instead of measuring
latency. A real device call over a poor mobile connection is 100–300ms of pure
waiting; a real internal call is under a millisecond. The counts are honest; the
timings are absent.

**The calls are sequential.** A real backend for a frontend would fetch catalog,
pricing, inventory and reviews concurrently, and the four internal calls would cost
roughly what the slowest one costs. Doing that here would add thread handling to a
project about shape, so it is left out — which means the project understates the
pattern's benefit rather than overstating it.

**Nothing fails.** Every service answers. A real backend has to decide what a
screen does when reviews is down: the phone screen can draw without a star rating,
so a sensible backend returns the other five fields and omits the rating rather
than failing the whole screen. That decision — which fields are essential to *this*
screen — is another thing only a client-specific backend can make, and the
resilience patterns for it live in the microservices category.

**There is no HTTP, no JSON library and no serialisation.** `Doc` is an ordered map
with a `bytes()` method that measures its own compact text form. Real payloads
would compress, and gzip narrows the gap between 1755 bytes and 196 considerably.
The byte comparison in Act 4 is directionally right and should not be quoted as a
production figure.

**There is no gateway.** Act 6 counts copies of four jobs; it does not run them.

**There are no schemas or versioning.** In production each backend publishes a
contract to its client, and shipping a phone app that expects a field the backend
no longer sends is its own category of outage.

## Why The Tests Are The Proof

The tests are where the pattern's claims are made checkable rather than asserted in
prose.

`MobileBffTest` pins the shape exactly:

```java
assertEquals(Screens.PHONE, screen.paths());
```

Not "contains the fields the screen needs" — *equals*. If the backend ever sends a
seventh field, the test fails, because a field that arrives and is not drawn is the
waste this project exists to remove.

```java
assertEquals(1, log.countFrom(CallLog.Origin.DEVICE));
assertEquals(4, log.countFrom(CallLog.Origin.INTERNAL));
```

One and four, stated separately. Both halves of the honest claim in one assertion
pair.

```java
assertTrue(!log.targetsFrom(CallLog.Origin.INTERNAL).contains("recommendations"));
```

A test that something did *not* happen. The phone's screen shows no related
products, so calling recommendations would be work done for nobody.

`WebBffTest` asserts the disagreement:

```java
assertNotEquals(phoneScreen.names(), page.names());
```

If those two ever became equal, the shop would have two processes doing one job and
should delete one. The test protects the pattern from being applied where it is not
needed.

`ClientEstateTest` pins the counting rule, and `CrossCuttingTest` pins the
constant:

```java
assertEquals(CrossCutting.JOBS.size(), CrossCutting.copiesBehindAGateway());
```

And `DemoRunsTest` captures the demo's own output and asserts on the strings the
documents and the narration quote, so a number cannot drift out of a video script
without a build failing first.

## What You Gain

| Gain | Measured here as |
| --- | --- |
| One round trip over the customer's connection | 5 device calls → 1 |
| A document the size of the screen | 1755 bytes → 196 |
| Presentation decisions outside the app | `4799` → `"£47.99"`, in a redeployable process |
| A field for one client, this week | the delivery sentence: four lines, no negotiation |
| Client-shaped composition | three services joined into one sentence |
| Screens free to differ | 6 fields and 15 fields from the same five services |

## What To Watch Out For

| Watch for | Why | What to do |
| --- | --- | --- |
| Business rules inside a backend | Two copies will diverge silently | Keep rules behind the backends; keep shape inside |
| Auth or rate limiting per backend | N copies of the entry code | One gateway in front of all of them |
| One backend per client on principle | A department instead of a pattern | One per genuine disagreement about the data |
| A backend nobody owns | The five-week queue returns | The team that draws the screen changes the backend |
| A backend that grows a database | It is becoming a service, not a view | Backends hold no state of their own |
| Two backends drifting into the same shape | You are paying twice for one job | Merge them; a layout difference is a stylesheet |
| Treating this as an optimisation | You will measure bytes and miss ownership | The win is who may change the shape |

## Backends for Frontends vs. API Gateway vs. API Composition

These three are constantly confused, and the difference is what question each one
answers.

| | Answers | How many | Owned by |
| --- | --- | --- | --- |
| **API Gateway** | "Is this request allowed in?" | One | The platform team |
| **API Composition** | "How do I answer one query from several services?" | A technique, not a process | Whoever writes the endpoint |
| **Backends for Frontends** | "What does *this screen* need?" | One per disagreeing client | The team that owns the screen |

A backend for a frontend almost always *uses* API composition — that is what
`MobileBff.productScreen` is doing when it calls four services. And it almost
always *sits behind* a gateway, which is Act 6's whole argument. The patterns
compose; they do not compete.

## Where You Have Already Seen It

- **Netflix**, which is where the pattern's modern write-up comes from: hundreds of
  device types, from televisions to phones to browsers, each with its own idea of
  what a title looks like, served by device-specific adapters over one shared API.
- **SoundCloud**, whose 2015 write-up gave the pattern its name and its argument —
  a shared public API that could not keep up with the needs of its own mobile apps.
- **GraphQL**, which is a different answer to the same problem: rather than one
  backend per client, one endpoint that lets each client describe its own shape.
  Worth knowing as the alternative, and worth knowing that it moves the ownership
  question rather than removing it — somebody still owns the schema.
- **Any mobile app with a `/v2/home-screen` endpoint.** If an endpoint is named
  after a screen rather than after a resource, you are looking at this pattern.

## Try It Yourself

```bash
./gradlew run
./gradlew test
```

Then:

1. **Add a seventh field to `MobileBff`** — anything, say the warehouse name. Run
   the tests. `sendsOnlyWhatIsDrawn` fails, because the field is not on
   `Screens.PHONE`. That is the guard rail working.
2. **Give the phone the current rule.** In `ProductScreenDemo`, pass
   `SavingRules.current()` to the phone's backend instead of the stale copy. Act 5
   now agrees with the desktop. Notice that the fix is one line and that nothing
   would ever have told you which line.
3. **Delete the delivery sentence** and return the raw date, as the desktop does.
   The phone app now has to build the sentence itself — on the device, in three
   languages, in a release customers may not install.
4. **Add a fourth client** to `ClientEstate` and decide, before you run it, whether
   it disagrees about what a product is. That decision is the design work.
5. **Make the four internal calls concurrent.** How much would the pattern's
   benefit grow? This is the exercise that shows how much the simulation is
   understating.

## See Also

- `docs/problem-statement.md` — the failure, in full, before the pattern
- `docs/class-diagram.md` — the structure, and the argument in the arrows
- `docs/uml-diagram.md` — the three designs as sequence diagrams
- `docs/prerequisites.md` — what you need to know first
- `../../micro-services-design-patterns/api-gateway-pattern/` — the neighbour this
  pattern sits behind
- `../../micro-services-design-patterns/api-composition-pattern/` — the technique
  each backend uses internally
