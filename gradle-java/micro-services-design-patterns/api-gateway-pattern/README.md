# API Gateway Pattern

**Put one service in front of all the others, so a client makes a single call
instead of five and only has to know one address.**

Think of a hotel reception desk. You do not keep separate phone numbers for
housekeeping, the restaurant and the concierge; you ring reception, and reception
deals with whoever needs dealing with. One number to remember, and it does not
change when the hotel reorganises its departments.

The shop's mobile app needs a product page, and that page is made of four
services' worth of information: the name from **Catalog**, the price from
**Pricing**, availability from **Inventory**, and "customers also bought" from
**Recommendations**. The obvious app calls all four itself. It works. It is also
four slow trips instead of one, four token checks instead of one, and — the
expensive part — it loses the whole product page on the day a feature nobody would
miss goes down.

## Run

```bash
./gradlew run
```

Four acts. The first two are the same page built two ways:

```
==================================================================
1. No gateway: the app calls all four services itself
==================================================================
      0ms ->   200ms  Catalog          OK        Barista Pro Espresso Machine
    200ms ->   400ms  Pricing          OK        £449.99
    400ms ->   600ms  Inventory        OK        true
    600ms ->   800ms  Recommendations  OK        [SKU-2001, SKU-2002]
  page: Barista Pro Espresso Machine  £449.99  in stock  2 suggestions
  four round trips over the mobile network, 4 token checks, shopper waited 800ms

==================================================================
2. With a gateway: the app makes one call
==================================================================
      0ms ->   240ms  Gateway          OK        Barista Pro Espresso Machine  £449.99  in...
    100ms ->   100ms  Gateway          AUTH      one token check for CUST-001
    100ms ->   110ms  Catalog          OK        Barista Pro Espresso Machine
    110ms ->   120ms  Pricing          OK        £449.99
    120ms ->   130ms  Inventory        OK        true
    130ms ->   140ms  Recommendations  OK        [SKU-2001, SKU-2002]
  page: Barista Pro Espresso Machine  £449.99  in stock  2 suggestions
  1 round trip over the mobile network, 1 token check, shopper waited 240ms
```

Identical page. 240 milliseconds against 800, and one token check against four. A
phone reaching the data centre takes about 200ms per trip; two services inside it
take about 10. The gateway's own call opens the timeline and closes it 240ms later,
and the four internal calls all happen *inside* that trip.

The other two acts are the same failure, twice:

```
==================================================================
3. Recommendations is down, and there is no gateway
==================================================================
      0ms ->   200ms  Catalog          OK        Barista Pro Espresso Machine
    200ms ->   400ms  Pricing          OK        £449.99
    400ms ->   600ms  Inventory        OK        true
    600ms ->   800ms  Recommendations  FAILED    no answer
  no page: Recommendations did not answer
  the name, the price and the stock all arrived, and were thrown away with the error.
  the shopper wanted to know what an espresso machine costs. They cannot find out,
  because a feature nobody would miss is unavailable.

==================================================================
4. Recommendations is down, and there is a gateway
==================================================================
      0ms ->   240ms  Gateway          OK        Barista Pro Espresso Machine  £449.99  in...
    100ms ->   100ms  Gateway          AUTH      one token check for CUST-001
    100ms ->   110ms  Catalog          OK        Barista Pro Espresso Machine
    110ms ->   120ms  Pricing          OK        £449.99
    120ms ->   130ms  Inventory        OK        true
    130ms ->   140ms  Recommendations  FAILED    no answer
    140ms ->   140ms  Gateway          DEGRADED  page served without suggestions
  page: Barista Pro Espresso Machine  £449.99  in stock  0 suggestions
  degraded: true. The shopper sees the price, the stock and no suggestions,
  which is a product page. Nobody is told anything is wrong, because for them
  nothing is.
```

The gateway knows Recommendations is optional and Pricing is not. That is a fact
about a shop rather than about software, and the reason the pattern is worth a whole
service is that the fact now lives in one place instead of in every client.

## Test

```bash
./gradlew test
```

25 tests, in about a second, with no `Thread.sleep` anywhere. Time is a
`SimulatedClock` the tests move by hand, and failures are scripted — `failNext(2)`
means "fail the next two calls, then behave" — so every assertion is about what the
pattern did rather than what chance did.

Both versions of the app return the same product page, so no test asserts that the
page is correct; that would pass on the naive version too. Every test asserts
something only the gateway gives you: one network crossing, one token check, 240ms
against 800ms, a degraded page when an optional service fails, an honest error when
an essential one does, and — the test whose job is to stop a future feature — that
the price on the page is Pricing's answer unmodified.

## One JVM, no infrastructure

This project starts nothing. No Docker, no Spring, no Kafka, no database, no HTTP
port. It runs offline with only a JDK installed. A service is a plain class, and a
remote call is `RemoteCall`: it advances a simulated clock by however long its link
takes, writes a line into the timeline, and either answers or throws.

That is a deliberate trade and it is worth being straight about. What you get is
the pattern's shape — what objects exist, what each decides, where the error
handling goes and why it goes there rather than somewhere else — and that shape is
the same whether the call underneath is a method call or an HTTP request. What you
do not get is a distributed system: no deployment, no service mesh, no partial
network partitions, no capacity planning. Finish this project and you will know
what an API gateway is and could write one. You will not have run one in
production.

## Learning Material

| Document | What it covers |
| --- | --- |
| [`docs/problem-statement.md`](docs/problem-statement.md) | Four calls from a train, with the numbers, and the product page that gets lost |
| [`docs/api-gateway-pattern-explained.md`](docs/api-gateway-pattern-explained.md) | The pattern from a hotel reception desk, the code, the costs, and gateway vs facade |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types, and why `MobileApp` depends on exactly one thing |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Four sequences: the happy path, both failure paths, and no gateway at all |
| [`docs/animation.html`](docs/animation.html) | The timeline, one call at a time, in a browser |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What you need to know, what you explicitly do not, and how to get a JDK |
| [`docs/session.md`](docs/session.md) | A one-hour taught session with exercises |
| [`docs/spec.md`](docs/spec.md) | The generated specification, with measured test counts and timings |
| [`docs/youtube.md`](docs/youtube.md) | Title, description and chapters for the video |

### The pattern in one picture

![Class diagram](docs/images/class-diagram.png)

### Video

The narrated walkthrough is built from [`video/scenes.py`](video/scenes.py) by
[`video/build_video.sh`](video/build_video.sh). The rendered file is not committed —
see the repository README for why — and takes about ten minutes to produce on macOS.

## Where this sits

First of twelve in
[`micro-services-design-patterns`](..), and the gentlest. It is placed first
because it invites the comparison with
[Facade](../../structural/facade-pattern) — the same shape one process boundary
apart — which makes it the easiest bridge from the Gang of Four patterns into
this category.

The distinguishing question, if you only remember one thing: **does the thing I am
hiding sit on the other side of a network and a trust boundary?** If not, you want
a facade, and you should not pay for a gateway.
