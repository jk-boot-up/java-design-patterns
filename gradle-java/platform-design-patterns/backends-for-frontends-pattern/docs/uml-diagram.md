# Backends for Frontends Pattern — UML Sequence Diagrams

Five sequences. The first two are the designs the pattern replaces. The third is the
pattern itself. The last two are the bill — the silent disagreement, and the line
between this pattern and the gateway it sits behind.

## 1. The Chatty Phone — Five Calls Across A Mobile Network

The first design, and the one shops arrive at by accident. Watch where the dashed
boundary is: every single arrow on the customer's side of it is a wait.

![Backends for Frontends pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Phone as phone app
    participant Cat as catalog
    participant Pri as pricing
    participant Inv as inventory
    participant Rev as reviews
    participant Rec as recommendations

    Note over Phone: customer taps SKU-4417

    Phone->>Cat: GET /catalog/SKU-4417
    Cat-->>Phone: 9 fields, 5 image URLs
    Phone->>Pri: GET /pricing/SKU-4417
    Pri-->>Phone: 7 fields
    Phone->>Inv: GET /inventory/SKU-4417
    Inv-->>Phone: 5 fields
    Phone->>Rev: GET /reviews/SKU-4417
    Rev-->>Phone: 3 review bodies
    Phone->>Rec: GET /recommendations/SKU-4417
    Rec-->>Phone: 3 fields

    Note over Phone: 5 device round trips<br/>1767 bytes arrived<br/>29 fields available<br/>6 fields drawn
```

</details>

Five request-and-response pairs, all of them crossing the customer's own connection,
and they happen one after another rather than all at once because the later calls
need the earlier answers.

Then read the closing note. Twenty-nine fields arrived and six were drawn, which
looks like the headline. It is not. The headline is the five. Bytes cost the
customer their data allowance; round trips cost them the two seconds they spend
looking at an empty screen, and on a poor connection each one of those five is a
tenth of a second of pure waiting before any work has begun.

---

## 2. One Shared Endpoint — Better, And Still Wrong

The obvious fix, which genuinely fixes the round trips and genuinely does not fix
the thing that matters.

![Backends for Frontends Pattern — One Shared Endpoint — Better, And Still Wrong](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Phone as phone app
    participant Api as shared /api/products
    participant Shop as catalog · pricing · inventory · reviews · recommendations
    participant Team as the API team
    participant Others as 5 other clients

    Phone->>Api: GET /api/products/4417
    Api->>Shop: 5 internal calls
    Shop-->>Api: everything the shop knows
    Api-->>Phone: the union document, 1755 bytes
    Note over Phone: 212 bytes drawn<br/>1543 thrown away (87%)

    Phone->>Api: GET /api/products/4417?fields=title,price,…
    Api-->>Phone: 212 bytes
    Note over Phone: the size problem is solved

    Phone->>Team: please add one field:<br/>"Free delivery, arrives Friday"
    Team->>Others: that changes the document you receive too
    Others-->>Team: we will need to regression-test it
    Team-->>Phone: it is in the queue
    Note over Phone,Team: an afternoon's work.<br/>five weeks of waiting.
```

</details>

Read the first half and the second half as two separate stories, because they have
different endings.

The first half is a success. One round trip instead of five, and once the field list
is added, two hundred and twelve bytes — close to what a tailored backend would
send. A shop that stopped here would have most of the measurable benefit and none of
the extra processes, and plenty of shops do exactly that.

The second half is why the story continues. The phone team asks for one line of
text, joined from stock, the delivery rules and the clock. It does not exist in any
service, so it is a new field on the shared document, and the shared document is
received by five other clients who did not ask for it and must test it anyway.

Notice who is at fault in that exchange: nobody. The API team is not obstructive,
the other clients are not unreasonable, and the phone team's request is not
exotic. The queue is a property of the *structure* — one endpoint owned by everybody
is owned by nobody in particular.

---

## 3. A Backend Per Frontend

The pattern. Two sequences side by side over the same shop, and the interesting part
is how differently they end.

![Backends for Frontends Pattern — A Backend Per Frontend](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Phone as phone app
    participant MBff as MobileBff
    participant WBff as WebBff
    participant Desk as desktop store
    participant Shop as the five shop services

    Phone->>MBff: GET /phone/product-screen/SKU-4417
    MBff->>Shop: catalog
    MBff->>Shop: pricing
    MBff->>Shop: inventory
    MBff->>Shop: reviews
    Note over MBff: recommendations NOT called —<br/>this screen has no related strip
    Note over MBff: 4799 → "£47.99"<br/>hero-2000.jpg → hero-320.jpg<br/>inStock + date → one sentence
    MBff-->>Phone: 6 flat fields, 196 bytes

    Desk->>WBff: GET /web/product-page/SKU-4417
    WBff->>Shop: all five services
    Note over WBff: 4799 → "£47.99"<br/>5999 → "£59.99"<br/>delivery: the bare date, not a sentence
    WBff-->>Desk: 15 fields, description,<br/>5 images, 3 reviews
```

</details>

For anyone listening rather than looking: the phone makes one call to its own
backend, that backend makes four calls inside the data centre, and it sends back six
flat fields. Then the desktop makes one call to a *different* backend, that backend
makes five calls inside the data centre, and it sends back fifteen fields.

Three things on that diagram are the pattern, and all three are decisions only a
client-specific backend can make.

**The call that is not there.** `MobileBff` never asks recommendations for anything,
because the phone's product screen draws no related-products strip. A shared
endpoint has to call it, because some client somewhere needs it.

**The conversions in the note.** `4799` becomes `"£47.99"`. The 2000-pixel hero
image becomes the 320-pixel thumbnail. Stock plus a date becomes "Free delivery,
arrives 2026-09-18". Every one of those is a presentation decision, and every one of
them now lives in a process that can be corrected this afternoon rather than in an
app release that customers may not install for two years.

**The two backends disagreeing.** Look at `delivery` on both sides. The phone gets a
whole sentence; the desktop gets the bare date, because the desktop page has a
delivery panel and wants the parts. Same field name, same service underneath, two
different answers, and neither is a bug.

---

## 4. The Bill, Part One: Two Backends, One Rule, Two Answers

The pattern's worst failure. There is no error in this sequence — read it looking for
the moment something goes wrong, and notice that there isn't one.

![Backends for Frontends Pattern — The Bill, Part One: Two Backends, One Rule, Two Answers](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Cust as one customer, two screens
    participant MBff as MobileBff
    participant WBff as WebBff
    participant Pri as pricing
    participant Stale as SavingRules (copy, pre-review)
    participant Now as SavingRules (current)

    Note over Pri: the review added a condition:<br/>the higher price must have been<br/>in force long enough to quote

    Cust->>WBff: desktop: what is the saving?
    WBff->>Pri: pricing SKU-4417
    Pri-->>WBff: list 5999, now 4799,<br/>heldLongEnough = false
    WBff->>Now: savingLabel(5999, 4799, false)
    Now-->>WBff: "" — nothing may be claimed
    WBff-->>Cust: no saving shown

    Cust->>MBff: phone: what is the saving?
    MBff->>Pri: pricing SKU-4417
    Pri-->>MBff: list 5999, now 4799,<br/>heldLongEnough = false
    MBff->>Stale: savingLabel(5999, 4799, false)
    Note over Stale: the copy ignores the third argument.<br/>It was written before it existed.
    Stale-->>MBff: "Save £12.00"
    MBff-->>Cust: Save £12.00

    Note over Cust: same product, same price, same second.<br/>No exception. No log line.<br/>Two different claims.
```

</details>

Both backends asked pricing. Both received the same three values, including the flag
that says the higher price is too recent to advertise. The shop is not hiding
anything and nothing has failed.

The difference is in the last argument. The current rule reads
`heldLongEnough = false` and returns an empty string. The stale copy ignores that
argument, because when it was written the argument did not exist. It subtracts, it
formats, and it returns a claim the shop is not permitted to make.

Sit with the shape of that failure for a moment, because it is why this one is worth
a diagram of its own. There is no arrow in that sequence that is wrong. Every
participant behaves correctly according to what it knows. The only place the problem
exists is in the relationship between two files, and the only observer who can see
it is a customer with a phone in one hand and a laptop in front of them.

The rule the diagram argues for: **a backend for a frontend may hold the shape.
Anything the shop would still believe with every client switched off belongs behind
it, with one implementation.**

---

## 5. The Bill, Part Two: Where The Shared Jobs Go

The last sequence is two sequences, and the difference between them is the answer to
"how is this different from an API gateway?"

![Backends for Frontends Pattern — The Bill, Part Two: Where The Shared Jobs Go](images/uml-diagram-5.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Client as any client
    participant Gate as gateway
    participant MBff as MobileBff
    participant WBff as WebBff
    participant Shop as the five shop services

    rect rgb(245, 232, 232)
    Note over MBff,WBff: without a gateway — 4 jobs × 2 backends = 8 copies
    Client->>MBff: request
    Note over MBff: verify token · rate limit<br/>terminate TLS · access log
    MBff->>Shop: compose the phone's screen
    Client->>WBff: request
    Note over WBff: verify token · rate limit<br/>terminate TLS · access log
    WBff->>Shop: compose the desktop's page
    end

    rect rgb(232, 240, 234)
    Note over Gate: with a gateway — 4 jobs, once,<br/>whatever the number of backends
    Client->>Gate: request
    Note over Gate: verify token · rate limit<br/>terminate TLS · access log
    Gate->>MBff: trusted request, customer id attached
    MBff->>Shop: compose the phone's screen
    Gate->>WBff: trusted request, customer id attached
    WBff->>Shop: compose the desktop's page
    end
```

</details>

In the first block each backend does the four shared jobs itself: eight copies of
work that is identical by definition. Add a third client and it is twelve. The way
this happens is not negligence — the nearest place to put token verification is
inside whichever backend you have open, and each individual decision to do it there
is defensible.

In the second block the gateway does them once, and the backends trust what it
passes them. The count is four whether there are two backends or nine, which is why
`CrossCutting.copiesBehindAGateway()` takes no argument.

And the line, stated as one question you can apply to any file:

- *"What does this screen need?"* → it belongs in a backend for that frontend.
- *"Is this request allowed in at all?"* → it belongs in front of all of them.

A gateway is about **entry**. A backend for a frontend is about **shape**. Almost
every real system has both, arranged exactly as the second block above, and that is
the correct relationship between two patterns people spend a lot of time confusing.
