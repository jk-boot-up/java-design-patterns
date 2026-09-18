# The Problem — One Shape Cannot Serve Two Screens

## The same product, two very different pages

The shop sells a copper filter coffee maker, item SKU-4417. There is one product
in the catalogue and there are two places a customer can look at it.

On a phone, the product screen shows six things: the title, the price, one
photograph, the star rating, how many people left that rating, and one line of
text saying when the parcel arrives. That is all that fits, and it is all the
phone team wants.

On a desktop browser, the same product fills a page: the title, the price, the
price it used to be, the saving, the full description, the materials, the
dimensions, five photographs you can click through, three written reviews, and a
strip of related products along the bottom. Fifteen fields.

Both pages are correct. Neither team is being unreasonable. They simply disagree
about what a product *is*, and that disagreement is the whole of this pattern.

## The first answer: let the phone ask for everything itself

The shop already has five services — catalog, pricing, inventory, reviews and
recommendations. The obvious thing is to let the phone call them.

```
Act 1 — one product screen, five calls from a phone

  calls from the phone:   5
    → catalog
    → pricing
    → inventory
    → reviews
    → recommendations
  downloaded:             1767 bytes
  fields available:       29
  fields drawn on screen: 6
```

Twenty-nine fields arrive; six are drawn. That is wasteful, but waste is not the
serious problem here. The serious problem is the first number.

Five round trips before a single pixel appears. On office wifi nobody notices. On
a train each one is a wait of its own, and they happen one after another rather
than all at once, because the later calls need the earlier answers — you cannot
ask pricing about a product until the catalog has told you which product it is.

Count the network the customer pays for. Five crossings of a mobile network, and
each crossing is the slow, expensive, unreliable kind.

## The second answer: one endpoint that serves everybody

So the shop builds a single endpoint in front of the five services. Every client
calls it, and it returns the union of everything any client might need.

```
Act 2 — one shared endpoint for every client

  calls from the phone:   1
  downloaded:             1755 bytes
  of that, actually drawn: 212 bytes
  thrown away on arrival:  1543 bytes (87%)
```

One round trip instead of five. That is a genuine win and the pattern that follows
keeps it.

Eighty-seven per cent of what arrived is thrown away, and there is an obvious fix
for that too, which is worth taking seriously rather than dismissing:

```
  Now the obvious fix — ask for only the fields you want:
    GET /api/products/4417?fields=… → 212 bytes
```

Two hundred and twelve bytes. The size problem is solved. If this pattern were
about payload size, the story would end here with a query parameter and no new
services.

## What a field selector cannot do

The next request from the phone team is not a field. It is one line of text:
*"Free delivery, arrives 2026-09-18."*

That sentence does not exist in any service. Producing it means asking inventory
whether the item is in stock, asking the delivery rules what that means for
tomorrow's date, looking at the clock, and joining the three into a sentence
written the way the phone app's designer wants it written. It is half an hour of
work.

```
    delivery sentence: not available -- a field like this belongs to one client,
                       and this endpoint belongs to all of them
```

Here is why it does not happen in half an hour. The shared endpoint is a document
that every client receives. Adding a field to it is a change to the contract of
the desktop store, the tablet app, the smart TV app, the in-store kiosk and the
nightly partner feed, none of which asked for a delivery sentence and all of which
must be regression-tested before it ships. So the change joins a queue, behind
work that has nothing to do with the phone.

The phone team could have written it in an afternoon. They wait five weeks.

That is the failure this pattern exists to fix, and notice that it is an
*organisational* failure with a technical cause. One endpoint owned by everybody
is owned by nobody in particular, and every client's small change is every other
client's risk.

## The pattern: one backend per frontend

Give each frontend its own backend, owned by the team that owns the screen, whose
only job is to turn what the shop knows into the exact shape that one screen
draws.

```
Act 3 — one backend per frontend

  phone app asks its own backend, and is sent:
    {
      "title": "Copper Filter Coffee Maker, 1 Litre",
      "price": "£47.99",
      "image": "https://img.shop.example/4417/hero-320.jpg",
      "rating": 4.6,
      "ratingCount": 218,
      "delivery": "Free delivery, arrives 2026-09-18"
    }

  desktop store asks its own backend, and is sent 15 fields including the
  description, the specification, five images and three reviews.
```

Six fields for the phone, fifteen for the desktop, from the same five services.
Neither backend can reach data the other cannot. What differs is the shape, and
the shape is now owned by the team that draws it.

Read the price field once more. It is the string `"£47.99"`. The pricing service
returned the integer `4799`. Somebody has to turn one into the other, and doing it
in the backend means it is done in a process that can be corrected this afternoon
— not inside an app that customers will still be running, unupgraded, in two
years.

```
Act 4 — the same product, three ways

  design                          bytes   device internal
  five calls from the phone        1767        5        5
  one shared endpoint              1755        1        5
  a backend for the phone           196        1        4
```

Read the last two columns together, because they are the point. The device column
falls from five to one. The internal column barely moves: five, five, four. The
work did not go away — it moved off the customer's mobile connection and onto a
data-centre network where a call costs almost nothing.

## The bill — and this is the part people skip

Three costs, all of them real, none of which announces itself.

**Shared logic put in two places will diverge.** The pricing team reviews the
discount rule and adds a condition: a higher price may only be advertised as a
saving if it was genuinely in force for long enough. For SKU-4417 the higher price
went up eleven days ago, which does not qualify. Both backends are told this.

```
Act 5 — the bill: two backends, one rule, two answers

  desktop store says:  (nothing — no saving may be claimed for this price)
  phone app says:      Save £12.00
```

Same product, same price, same second, and one of those screens is making a claim
the shop is not allowed to make. The phone's backend holds a copy of the discount
rule taken before the review, and the review added a condition the copy never
heard about. Nothing throws. Nothing is logged. The only person who can see the
difference is a customer with both screens open.

Nothing about that copy is careless. It was right when it was written, it is well
named, and its tests pass. It is wrong only in relation to a decision made months
later by people with no reason to know a second copy existed.

The rule that prevents it: a backend for a frontend may hold the **shape**, and
anything the shop would still believe with every client switched off belongs
behind it.

**The shared jobs get done once per backend.** Every request, whoever sent it,
needs its token verified, its rate limit checked, its TLS terminated and its
access line logged.

```
Act 6 — the bill: where the shared jobs go

  each backend doing it itself: 8 copies across 2 backends
  a gateway in front:           4 copies, whatever the number of backends
```

The nearest place to put authentication is inside whichever backend you happen to
be editing, and doing that once per backend puts the shop back where it was before
it had a gateway. The line is one question. Does the code answer *"what does this
screen need?"* — it belongs in a backend for that frontend. Does it answer *"is
this request allowed in at all?"* — it belongs in front of all of them. A gateway
is about entry; a backend for a frontend is about shape. They are neighbours and
they are not the same pattern.

**One backend per client is not the rule.** The shop has six clients.

```
Act 7 — the bill: how many backends is too many

  phone app        own backend        six fields, one sentence, a four-inch screen
  desktop store    own backend        description, specification, five images, reviews
  tablet app       shares one         the phone's fields in a wider column
  smart TV app     own backend        no keyboard, so no search, and pictures do the work
  in-store kiosk   shares one         the desktop page with the basket hidden
  partner feed     shares one         not a screen at all — a nightly file

  one per client:            6 backends
  one per genuine disagreement: 3 backends
```

The test is not the device and it is not the team. It is whether the client
disagrees about what a product *is*. A tablet showing the phone's six fields in a
wider column disagrees about nothing, so it is the same backend and a different
stylesheet.

Each extra backend costs, every week, for as long as it exists: a pipeline to
build and deploy it, a place in the on-call rota, a dependency upgrade every time a
shop service changes, and one more process to look at during an incident. Two
backends is a pattern. Nine is a department.

## What the shop actually needs

| What the shared endpoint could not do | What a backend per frontend gives you |
| --- | --- |
| Send one screen exactly its own fields | A **document shaped by one client**, 196 bytes instead of 1755 |
| Add a field for one client this week | **Ownership** — the team that draws the screen owns the endpoint |
| Join stock, delivery and the clock into a sentence | **Composition** placed where one client's needs are legitimate |
| Format money once, outside the app | **Presentation decisions** made in a redeployable process |
| Stop asking the customer's connection five times | **One device round trip**, four cheap internal ones |

And the three things it costs, each of which has to be engineered rather than
assumed:

| The failure | What it takes to avoid it |
| --- | --- |
| Two copies of one business rule silently disagree | Keep **rules behind** the backends; keep only **shape** inside |
| Authentication and rate limiting done per backend | Put the entry concerns in **one gateway in front** |
| A backend per client, then a department | One backend per **genuine disagreement**, not per device |

That is the whole of this project: one shape per screen, owned by the team that
draws it, and an honest account of the three ways it goes wrong.
