# The API Gateway Pattern, Explained

## In One Sentence

Put one service in front of all the others, so a client makes a single call
instead of five and only has to know one address.

That is the whole pattern. Everything below is about why that is worth doing,
what it costs, and where the line is that a gateway must not cross.

## Everyday Analogy: The Hotel Reception Desk

Imagine staying in a hotel. You want extra towels, a table for dinner, and a taxi
to the station in the morning.

You could deal with each department yourself. You would need the direct number
for housekeeping, the direct number for the restaurant, and the direct number for
the concierge. You would have to know which department handles what. And when the
hotel reorganises — the restaurant is outsourced, the concierge desk moves — your
list of numbers is wrong and nobody tells you.

So hotels have a reception desk. You ring one number. You say what you want.
Reception knows who handles towels and who handles taxis, and reception deals with
them. You have one number to remember, and it does not change when the hotel
changes.

That is an API gateway. The reception desk is a real, staffed thing that has to
be there and can be closed, which is a cost — but for a guest with three requests
it is unarguably better than three phone numbers.

Notice one more thing about reception, because it is the part people get wrong
when they build gateways. Reception does not decide what dinner costs. It takes
your booking and passes it to the restaurant, and the restaurant decides. A
reception desk that started setting menu prices would be a strange and
troublesome hotel.

## The Problem, In The Shop

Now the online store. A shopper opens a product page in the mobile app, and that
page shows four things:

- the product name and description, which belong to the **Catalog** service;
- the price, which belongs to **Pricing**;
- whether it is in stock, which belongs to **Inventory**;
- "customers also bought", which belongs to **Recommendations**.

Four separate services, because they change on different schedules and are looked
after by different people. That separation is a good thing and nobody wants to
undo it.

But the app is on a phone, possibly on a train. A round trip from a phone to the
data centre takes roughly two hundred milliseconds. A round trip between two
services *inside* the data centre takes roughly ten. Twenty times the cost, per
call — and the app needs four calls.

So the obvious version of the app waits eight hundred milliseconds to draw one
product page. It also checks the shopper's access token four times, because each
service quite reasonably insists on being told who is asking. And it treats all
four services as equally essential, which means the day Recommendations goes
down, a shopper who wanted to know what an espresso machine costs gets an error
page instead.

That last one is the interesting failure, so it is worth being precise about it.
The name arrived. The price arrived. The stock level arrived. All three were
thrown away, because the fourth call — for a feature nobody would miss — failed.

## The Pattern

Add one service, the gateway. It lives in the data centre, next to the others. The
app calls it once and gets back everything the product page needs.

Four things move into the gateway, and one thing deliberately does not.

**One network crossing instead of four.** The app makes one slow trip. The
gateway then makes four fast trips inside the data centre. Two hundred plus four
tens is two hundred and forty milliseconds, against eight hundred.

**One token check instead of four.** The gateway checks the shopper's access
token once, at the edge. The services behind it are inside the trusted network and
do not need to check again. A forged token is rejected before any service is
troubled by it at all.

**One response shape instead of four.** The app receives a single object shaped
the way the screen wants to display it. It never learns four addresses, four
response formats, or which service owns which field. When Pricing changes its
response, the gateway absorbs the change — no app-store release.

**Knowledge of which services matter.** This is the part that is easy to miss and
is the most valuable. The gateway knows Recommendations is optional and that
everything else is not. So a Recommendations failure produces a product page with
no suggestions on it, which is a perfectly good product page, and a Pricing
failure produces an honest error, because a page with no price on it is worse than
no page at all.

And the thing that does not move in: **business decisions**. The gateway does not
apply discounts, does not decide whether a product may be sold, does not compute
totals. It passes Pricing's answer through unaltered. A gateway that starts making
business decisions becomes a service that owns no data but makes rulings about
everybody else's, and it turns into the hardest thing in the system to change.
There is a test in this project whose only job is to hold that line.

## Participants

| Role | Type here | What it does |
| --- | --- | --- |
| Gateway | `ProductPageGateway` | Checks the token once, calls the four services, decides which failures matter, returns one page |
| Client | `MobileApp` | Knows one address and makes one call |
| Naive client | `NaiveMobileApp` | The version without a gateway. Correct, and expensive |
| Downstream services | `CatalogService`, `PricingService`, `InventoryService`, `RecommendationsService` | Each owns one thing and knows nothing about pages |
| Network fabric | `StoreServices` | The four services reachable at a given latency — ten milliseconds internally, two hundred from a phone |
| Composed answer | `ProductPage` | The one object the app receives |
| Edge authentication | `AuthService` | Checks a token and says who is asking. Counts its checks, so the demo can show the difference |
| Harness | `SimulatedClock`, `RemoteCall`, `CallLog` | Simulated time, simulated remote calls with scripted failures, and the timeline |

## Code Walkthrough

The gateway's one method reads as a list of four questions and one judgement:

```java
public ProductPage productPage(String token, String sku) {
    Customer customer = auth.check(token);          // once, at the edge

    Product product = services.catalog().invoke(sku);
    Money price = services.pricing().invoke(sku);
    boolean inStock = services.inventory().invoke(sku);
    List<String> recommended = recommendationsOrNone(sku);

    return new ProductPage(sku, product.name(), product.description(),
            price, inStock, recommended);
}
```

Three of those four calls have no error handling at all. If Catalog fails, the
exception travels straight out to the app, and the app shows an error. That is
intentional: there is no useful product page without a name.

The fourth call is different, and it is the only `catch` in the class:

```java
private List<String> recommendationsOrNone(String sku) {
    try {
        return services.recommendations().invoke(sku);
    } catch (ServiceUnavailableException e) {
        log.note("Gateway", "DEGRADED", "page served without suggestions");
        return List.of();
    }
}
```

An empty list of suggestions and a failed Recommendations service produce the same
page, because a page with no suggestions is normal. Notice that the decision is
written into the log. Nobody tells the shopper anything is wrong — for them
nothing is — but the shop can see it happened.

The version without a gateway does the same work and pays for it four times:

```java
auth.check(token);
Product product = services.catalog().invoke(sku);

auth.check(token);
Money price = services.pricing().invoke(sku);

auth.check(token);
boolean inStock = services.inventory().invoke(sku);

auth.check(token);
List<String> recommended = services.recommendations().invoke(sku);
```

There is nothing stupid about that code. It is the obvious thing to write and it
returns the correct page. Its problems are not bugs you could spot by reading it —
they are counts and timings, which is why they need a timeline to see.

## What The Timeline Shows

Run `./gradlew run`. Two of its four acts are the whole argument.

Without a gateway:

```
      0ms ->   200ms  Catalog          OK        Barista Pro Espresso Machine
    200ms ->   400ms  Pricing          OK        £449.99
    400ms ->   600ms  Inventory        OK        true
    600ms ->   800ms  Recommendations  OK        [SKU-2001, SKU-2002]
  four round trips over the mobile network, 4 token checks, shopper waited 800ms
```

With one:

```
      0ms ->   240ms  Gateway          OK        Barista Pro Espresso Machine  £449.99  in...
    100ms ->   100ms  Gateway          AUTH      one token check for CUST-001
    100ms ->   110ms  Catalog          OK        Barista Pro Espresso Machine
    110ms ->   120ms  Pricing          OK        £449.99
    120ms ->   130ms  Inventory        OK        true
    130ms ->   140ms  Recommendations  OK        [SKU-2001, SKU-2002]
  1 round trip over the mobile network, 1 token check, shopper waited 240ms
```

The gateway's own call opens the timeline and closes it two hundred and forty
milliseconds later. Everything else happens *inside* that trip, which is why the
four internal calls are all stamped between one hundred and one hundred and forty
milliseconds — they are happening while the response is still notionally in
flight.

Then Recommendations goes down. Without a gateway, three answers arrive and are
discarded with an error and the shopper never finds out the price. With a gateway,
the same failure produces a page with no suggestions and a `DEGRADED` line in the
log, and the shopper notices nothing.

## A Note On What This Project Is Not

There is no network here, and that is deliberate.

Everything runs in one JVM. A service is a plain class, a remote call is
`RemoteCall`, and time is a `SimulatedClock` that the tests move by hand. Nothing
starts, nothing listens on a port, and there is no Docker, Spring, broker or
database anywhere in the project.

What that gives you is the pattern's shape, honestly: what objects exist, what
each decides, where the `catch` goes and why it goes there rather than somewhere
else. That shape is identical whether the call underneath is a method call or an
HTTP request, and it is the part that is hard to learn.

What it does not give you is a distributed system. Deployment, service meshes,
partial network partitions, real timeouts, capacity planning and the experience of
being paged at three in the morning are all absent. When you finish this project
you will know what an API gateway is and could write one. You will not have run
one in production. Those are different things, and it would be dishonest to blur
them.

## Why The Tests Are The Proof

Both versions return the same product page. So a test that asserts the page is
correct proves nothing about the pattern — it would pass on the naive version too.

Every test here asserts something only the gateway gives you:

- the app crosses the mobile network exactly **once**;
- the token is checked exactly **once**, not once per service;
- the elapsed time is 240ms against the naive 800ms;
- Recommendations failing still produces a page, and the degradation is logged;
- Pricing failing does **not** produce a page, because a priceless page is worse
  than an error;
- Catalog failing stops the sequence rather than pricing a product whose name
  could not be fetched;
- a forged token costs the services nothing, because it is rejected at the edge;
- the price on the page is Pricing's answer **unmodified** — the test that holds
  the business-logic line;
- `MobileApp` has exactly two public methods, so there is nowhere for a service
  address to leak into the client.

The tests on `NaiveMobileApp` all pass too, and are written to record its costs
rather than to mock it. One of them pins the genuine bug: when Recommendations
fails, three successful answers are thrown away.

## What You Gain

- **One round trip from the client.** On a mobile connection this is the single
  largest thing you can do for a page's speed.
- **A place to put edge concerns.** Authentication, rate limiting, request
  logging, correlation ids: things every request needs and no individual service
  should reimplement.
- **Freedom to change the services.** Split Pricing in two, move Inventory,
  rename a field — the client does not know and does not need a release.
- **A place to make availability decisions.** The judgement that
  Recommendations is optional has to live *somewhere*. In the gateway it is
  written once. In five clients it is written five times, differently.

## What To Watch Out For

- **It is a new single point of failure.** Everything now goes through it. It
  needs to be deployed, monitored and made redundant, and when it is down, the
  shop is down.
- **It attracts business logic.** Every quarter somebody will want to put "just
  one small rule" in the gateway because it is the only place that can see
  everything. Each one is reasonable. The sum of them is a distributed monolith
  with a bottleneck in the middle.
- **It becomes a bottleneck for teams, not just traffic.** If every new field on
  every screen needs a change in the gateway, and one team owns the gateway, that
  team is now in the way of everybody.
- **It is overhead when you are small.** One client and three services do not
  need a gateway. The pattern earns its keep when there are several clients, or
  the client is remote and slow, or the number of services is growing.
- **Fallbacks can lie.** Returning an empty list when Recommendations fails is
  fine because empty suggestions are a normal state. Returning a *cached price*
  when Pricing fails would be a serious bug dressed up as resilience. A fallback
  that hides a real failure is worse than an error.

## API Gateway vs. Facade

They are the same shape one process boundary apart, and the honest answer to "is
a gateway just a facade?" is "almost".

A **facade** — `structural/facade-pattern` in this repository — gives a caller in
the same program one simple method over several complicated subsystems. It is a
class. It cannot be down. It costs nothing to call.

A **gateway** does that *and* three things a facade never does. It crosses a
network, so the number of crossings is the point rather than a detail. It
terminates authentication, because the boundary it sits on is a trust boundary. And
it is a deployable, separately-running thing, which means it can be down, needs
monitoring, and has a version.

The question to ask: **does the thing I am hiding sit on the other side of a
network and a trust boundary?** If not, you want a facade, and you should not pay
for a gateway.

Two other comparisons are worth a sentence. A gateway is not an **adapter** —
adapters translate one interface into another for a single collaborator, while a
gateway aggregates several. And a **Backend for Frontend** is a gateway per client
type: one for the mobile app, one for the web, one for the in-store tills, each
shaped for its own screen. It is the same pattern, applied once per audience,
which is what you reach for when one gateway starts trying to please everybody.

## Where You Have Already Seen It

- **A shop assistant.** You ask one person where the coffee machines are, and
  they know whether that is a stockroom question or a display question.
- **A GP surgery.** You describe a symptom to one doctor, who decides which
  specialist to refer you to. You do not need to know which specialist exists.
- **A travel agent.** One conversation instead of a flight, a hotel and a car,
  and one point of contact when something changes.
- **`nginx` in front of anything.** Every reverse proxy you have configured is
  doing the routing half of this pattern.

## Try It Yourself

1. **Add a fifth field to the page** — say a delivery estimate from `Shipping`.
   Notice you change the gateway and the page record, and `MobileApp` does not
   change at all. Then add the same field to `NaiveMobileApp` and count the
   changes.
2. **Make Pricing optional and see how bad it feels.** Wrap the Pricing call in
   the same try/catch and return a price of zero. The test suite will let you.
   Then look at the page it produces and decide whether you would ship it.
3. **Move the token check inside the loop.** Make the gateway check the token
   before every internal call, then look at `auth.checks()`. This is what
   happens when a gateway does not actually terminate authentication.
4. **Break the business-logic line on purpose.** Apply a ten per cent discount
   inside the gateway. One test fails. Read what it says, and decide whether the
   test is being unhelpful or whether it is right.

## See Also

- [`problem-statement.md`](problem-statement.md) — the scenario in full, and the
  version without a gateway
- [`class-diagram.md`](class-diagram.md) — the types and what depends on what
- [`uml-diagram.md`](uml-diagram.md) — both sequences, including the failure
- [`animation.html`](animation.html) — the timeline, stepped through one call at
  a time
- [`../../structural/facade-pattern`](../../../structural/facade-pattern) — the
  same shape inside one program
- [`../docs/spec.md`](../../docs/spec.md) — the category specification this
  project is built to
