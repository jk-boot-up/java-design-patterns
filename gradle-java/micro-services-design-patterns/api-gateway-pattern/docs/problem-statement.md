# Problem Statement

## The Scenario

The shop has been split into services, and it was the right call. Catalog owns
product names and descriptions. Pricing owns prices and promotions. Inventory owns
stock. Recommendations produces "customers also bought". Four teams, four
deployment schedules, four sets of decisions that no longer collide.

The shop also has a mobile app. When a shopper opens a product page, that page
shows the name, the price, whether it is in stock, and the suggestions. Four
services' worth of information on one screen.

So the app calls all four.

## Attempt One: Let The App Call Everybody

```java
auth.check(token);
Product product = catalog.product(sku);

auth.check(token);
Money price = pricing.price(sku);

auth.check(token);
boolean inStock = inventory.inStock(sku);

auth.check(token);
List<String> recommended = recommendations.alsoBought(sku);

return new ProductPage(sku, product.name(), product.description(),
        price, inStock, recommended);
```

This is not a straw man. It is the obvious first version, most apps start here,
and it returns exactly the right page. There is no bug in it that you could find
by reading it carefully.

`NaiveMobileApp` in this project is that code, and its tests all pass.

## Why That Hurts

**The shopper waits four times too long.** A round trip from a phone to the data
centre is about two hundred milliseconds. Between two services inside the data
centre it is about ten. So four calls from a phone cost eight hundred
milliseconds, and the app has to make all four before it can draw anything.

**The token is checked four times.** Every service insists on knowing who is
asking, which is correct of them. But the client has nowhere to put that logic
except at each call site, so it appears four times — and again in the web client,
slightly differently, and again in the in-store till software.

**The app knows too much.** It knows four addresses, four authentication schemes
and four response shapes. When Pricing renames a field, the app is wrong, and
fixing it means an app-store release and a wait for shoppers to update.

**Every service is treated as essential.** This is the worst of the four, and it
is a design problem rather than a coding one. Run the third act of the demo:

```
      0ms ->   200ms  Catalog          OK        Barista Pro Espresso Machine
    200ms ->   400ms  Pricing          OK        £449.99
    400ms ->   600ms  Inventory        OK        true
    600ms ->   800ms  Recommendations  FAILED    no answer
  no page: Recommendations did not answer
```

The name arrived. The price arrived. The stock level arrived. All three were
discarded, and the shopper — who wanted to know what an espresso machine costs —
was shown an error, because a feature nobody would miss was unavailable.

The client had no way to express "one of my four dependencies does not matter". It
could add a try/catch, of course. And then the web client would need the same
try/catch, and the till software, and each would have to be kept in step with a
judgement about which services are optional that lives nowhere in particular.

## The Question This Project Answers

**Where does the knowledge of how to assemble a product page belong, when no
single service owns all of it?**

Not in four clients, four times over. Somewhere that is written once, deployed
with the services, and reachable in a single call.

## The Goal

Build one service in front of the other four such that:

1. the app makes **one** network crossing per page, not four;
2. the access token is checked **once**, at the edge;
3. the app receives **one** object shaped for its screen, and never learns which
   service owns which field;
4. a failure in an **optional** service still produces a usable page, and the
   degradation is recorded;
5. a failure in an **essential** service produces an honest error rather than a
   page with a hole in it;
6. and the gateway makes **no business decisions** — the price it returns is
   Pricing's answer, unmodified.

Point six is the one that is easiest to lose and hardest to get back.
