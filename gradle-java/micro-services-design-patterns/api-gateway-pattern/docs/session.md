# Session Guide — API Gateway Pattern

A one-hour session. It is the first of the microservices category, so a few
minutes go on setting up what the whole category is and, more importantly, what it
is not.

**Audience:** developers who know Java and have met a few Gang of Four patterns.
No infrastructure experience assumed or required.

**Format:** laptops open. Everything runs offline with a JDK.

## Learning Objectives

By the end, a participant can:

1. Say in one sentence what an API gateway is, without using the word "gateway".
2. Explain why four calls from a phone is much worse than four calls inside a data
   centre, with a number.
3. Point at the one `catch` in `ProductPageGateway` and say why it is around that
   call and not the other three.
4. Name the difference between a gateway and a facade in a form you can act on.
5. Name three things a gateway must not do.
6. Say honestly what this project does not teach.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check, and what this category is not |
| 0:05–0:17 | The problem: four calls from a train |
| 0:17–0:27 | The pattern, from a hotel reception desk |
| 0:27–0:42 | Code walkthrough |
| 0:42–0:52 | Exercises |
| 0:52–0:58 | Gateway vs facade, and what to watch out for |
| 0:58–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check, And An Honest Warning

```bash
cd micro-services-design-patterns/api-gateway-pattern
./gradlew test
```

25 tests, green, in about a second.

Then say the honest thing up front, because it changes how people listen:

> There is no network in this project. No Docker, no Spring, no Kafka, no
> database. A service is a class, a remote call is a method call that costs
> simulated time and can be told to fail. What you will learn is the shape of the
> pattern — what objects exist, what each decides, where the error handling goes.
> What you will not learn is how to run a distributed system. Both of those are
> real, and they are different.

Getting this out of the way early stops the question that otherwise derails minute
forty.

## 0:05–0:17 — The Problem

Don't show the gateway. Show the obvious code:

```java
auth.check(token);  Product product = catalog.product(sku);
auth.check(token);  Money price = pricing.price(sku);
auth.check(token);  boolean inStock = inventory.inStock(sku);
auth.check(token);  List<String> recs = recommendations.alsoBought(sku);
```

Ask the room what is wrong with it. Most groups will say "the repeated auth
check" — which is real, but it is the third-worst problem. Let them work.

Then run act one:

```
      0ms ->   200ms  Catalog          OK        Barista Pro Espresso Machine
    200ms ->   400ms  Pricing          OK        £449.99
    400ms ->   600ms  Inventory        OK        true
    600ms ->   800ms  Recommendations  OK        [SKU-2001, SKU-2002]
```

Two hundred milliseconds a trip from a phone. Ten milliseconds a trip inside the
data centre. Twenty times, and the app needs four.

Then run act three, where Recommendations is down. Read the timeline out loud. The
name arrived. The price arrived. The stock arrived. All discarded, and the shopper
does not find out the price, because "customers also bought" was unavailable.

That is the moment the room usually goes quiet. Let it.

## 0:17–0:27 — The Pattern

Do the hotel reception desk out loud, before any code:

> You want towels, a dinner table and a taxi. Three departments. You could keep
> three phone numbers, work out which department does what, and be wrong when the
> hotel reorganises. Or you ring reception once.

Then the two extra points that matter:

- Reception is a real, staffed thing. It has to be there, and it can be closed.
  That is a cost, and it is why a gateway is overhead when you have one client and
  three services.
- Reception does not set the menu prices. It takes the booking to the restaurant,
  and the restaurant decides. This is the discipline that keeps a gateway
  maintainable, and it is the one every team loses first.

Now run act two. 240ms against 800ms, one token check against four.

## 0:27–0:42 — Code Walkthrough

Read `ProductPageGateway.productPage` first, and ask the room to spot the
asymmetry: three calls with no error handling, one with a `catch`.

Then ask **why**. The answer is not technical. Suggestions are optional and prices
are not. That is a fact about a shop, and the whole reason a gateway is valuable is
that this fact now lives in one place instead of in every client.

Then `recommendationsOrNone`, and the `log.note("DEGRADED", ...)` inside it. Ask:
who is that log line for? Not the shopper — for them nothing is wrong. It is for
the shop, so that "we served forty thousand pages without suggestions yesterday" is
a thing somebody can find out.

Then the tests, and make the point about them explicitly:

> Both versions return the same page. So no test here asserts that the page is
> correct — that would pass on the naive version. Every test asserts something only
> the gateway gives you.

Walk three:

- `theAppCrossesTheMobileNetworkExactlyOnce`
- `aServiceThePageCannotDoWithoutIsAllowedToFailTheWholeCall`
- `theGatewayMakesNoPricingDecisionsOfItsOwn`

The third one is worth dwelling on. A test whose job is to stop a future developer
adding a feature.

## 0:42–0:52 — Exercises

### Exercise 1 — Add a fifth field (everyone)

Add a delivery estimate from a new `ShippingService`. Change the gateway and
`ProductPage`. Count how many lines of `MobileApp` you changed. Then do the same to
`NaiveMobileApp` and count again.

### Exercise 2 — Make Pricing optional (everyone)

Wrap the Pricing call in the same try/catch, returning `Money.pence(0)`. The
compiler will let you. One test will fail. Look at the page it produces and decide
whether you would ship it.

### Exercise 3 — Break the line on purpose (discussion)

Apply a ten per cent discount inside the gateway.
`theGatewayMakesNoPricingDecisionsOfItsOwn` fails. Is the test being unhelpful?

Expected discussion: the discount has to be *somewhere*, and Pricing already owns
prices and promotions. Putting it in the gateway means two services now decide
prices and only one of them is called Pricing.

### Exercise 4 — Stretch

Split the gateway in two: a `MobileProductPageGateway` returning a compact page and
a `WebProductPageGateway` returning a fuller one. That is Backend for Frontend, and
it is what you reach for when one gateway is trying to please two audiences.

## 0:52–0:58 — Gateway vs Facade, And The Pitfalls

The distinguishing question, on a slide by itself:

> **Does the thing I am hiding sit on the other side of a network and a trust
> boundary?**

If no, you want a facade. A facade is a class; it cannot be down; calling it is
free. A gateway crosses a network, terminates authentication, and is a deployable
thing with a version and a pager.

Then the four pitfalls, quickly:

- a new single point of failure;
- a magnet for business logic;
- a team bottleneck, if one team owns it and every screen change needs it;
- fallbacks that lie. Empty suggestions when Recommendations fails is honest. A
  cached price when Pricing fails is a bug wearing a resilience costume.

## 0:58–1:00 — Wrap-Up

One sentence: **one front door, one token check, one response shape, and the
knowledge of which services actually matter — written once.**

Then the honest closer, again: you now know what a gateway is and could write one.
You have not run one. Point at
[`api-gateway-pattern-explained.md`](api-gateway-pattern-explained.md) for the
long form and at the category spec for what the other eleven projects cover.

## Facilitator Notes

- **The "no network" warning is not optional.** Skip it and somebody spends
  twenty minutes trying to work out where the HTTP client is.
- **Do not rush act three.** The lost product page is the emotional core of the
  session. Everything after it is easier to motivate.
- **Somebody will say "this is just a facade".** They are nearly right, and
  saying so is a good sign. Use the distinguishing question rather than arguing.
- **Somebody will propose putting the discount in the gateway.** Also a good
  sign. Exercise 3 exists for them.
- **Watch the clock in the walkthrough.** Fifteen minutes goes fast, and the
  three tests matter more than reading every class.

## Materials Checklist

- [ ] JDK 21 on every laptop, verified before the session
- [ ] `./gradlew test` and `./gradlew run` both run once on the presenting machine
- [ ] Act one and act three output ready to show side by side
- [ ] `docs/animation.html` open in a browser tab
- [ ] The distinguishing question on a slide of its own
