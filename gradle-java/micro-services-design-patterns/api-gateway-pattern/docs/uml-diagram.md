# API Gateway Pattern — UML Sequence Diagram

## The Happy Path, With A Gateway

One slow crossing, four fast ones inside it.

![API Gateway pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App as MobileApp
    participant GW as ProductPageGateway
    participant Auth as AuthService
    participant Cat as Catalog
    participant Pri as Pricing
    participant Inv as Inventory
    participant Rec as Recommendations

    App->>GW: productPage("tok-abc123", "SKU-1234")
    Note over App,GW: 200ms — the only mobile crossing

    GW->>Auth: check(token)
    Auth-->>GW: CUST-001
    Note over GW,Auth: one token check, at the edge

    GW->>Cat: product(sku)
    Cat-->>GW: Barista Pro Espresso Machine
    GW->>Pri: price(sku)
    Pri-->>GW: £449.99
    GW->>Inv: inStock(sku)
    Inv-->>GW: true
    GW->>Rec: alsoBought(sku)
    Rec-->>GW: [SKU-2001, SKU-2002]
    Note over GW,Rec: four internal calls, 10ms each

    GW-->>App: ProductPage
    Note over App: shopper waited 240ms
```

</details>

## The Failure Path: An Optional Service Is Down

The same sequence, with Recommendations refusing to answer. The gateway makes a
decision and the shopper never finds out.

![The failure path: an optional service is down](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App as MobileApp
    participant GW as ProductPageGateway
    participant Cat as Catalog
    participant Pri as Pricing
    participant Inv as Inventory
    participant Rec as Recommendations
    participant Log as CallLog

    App->>GW: productPage(token, "SKU-1234")
    GW->>Cat: product(sku)
    Cat-->>GW: Barista Pro Espresso Machine
    GW->>Pri: price(sku)
    Pri-->>GW: £449.99
    GW->>Inv: inStock(sku)
    Inv-->>GW: true

    GW->>Rec: alsoBought(sku)
    Rec--xGW: ServiceUnavailableException
    GW->>Log: note(DEGRADED, "page served without suggestions")
    Note over GW: empty list, because a page with<br/>no suggestions is a normal page

    GW-->>App: ProductPage, 0 suggestions
    Note over App: 240ms, and nothing to report to the shopper
```

</details>

## The Failure Path: An Essential Service Is Down

Pricing fails, and the gateway deliberately does *not* rescue it.

![The failure path: an essential service is down](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App as MobileApp
    participant GW as ProductPageGateway
    participant Cat as Catalog
    participant Pri as Pricing
    participant Inv as Inventory

    App->>GW: productPage(token, "SKU-1234")
    GW->>Cat: product(sku)
    Cat-->>GW: Barista Pro Espresso Machine
    GW->>Pri: price(sku)
    Pri--xGW: ServiceUnavailableException
    GW--xApp: ServiceUnavailableException
    Note over GW,Inv: Inventory is never called —<br/>no point stocking a product<br/>whose price is unknown
    Note over App: an honest error, because a page<br/>with no price is worse than no page
```

</details>

## The Comparison: No Gateway At All

![The comparison: no gateway at all](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant App as NaiveMobileApp
    participant Auth as AuthService
    participant Cat as Catalog
    participant Pri as Pricing
    participant Inv as Inventory
    participant Rec as Recommendations

    App->>Auth: check(token)
    App->>Cat: product(sku)
    Cat-->>App: name
    Note over App,Cat: 200ms

    App->>Auth: check(token)
    App->>Pri: price(sku)
    Pri-->>App: £449.99
    Note over App,Pri: 200ms

    App->>Auth: check(token)
    App->>Inv: inStock(sku)
    Inv-->>App: true
    Note over App,Inv: 200ms

    App->>Auth: check(token)
    App->>Rec: alsoBought(sku)
    Rec--xApp: ServiceUnavailableException
    Note over App,Rec: 200ms, and the name, price<br/>and stock are all discarded
```

</details>

## Notes

**Compare the first diagram with the last.** Same services, same answers, same
number of service calls. The difference is entirely where the slow link sits: once
at the front, or four times through the middle.

**The failure diagrams are the point of this pattern, not a footnote.** Two
failures, two different correct responses, and the reason they differ is a
business fact rather than a technical one: nobody misses suggestions, and everybody
needs the price. That judgement has to be written down *somewhere*, and the whole
argument for a gateway is that the somewhere should be one place.

**Notice what is missing from the third diagram.** Inventory is never called. The
gateway does not soldier on gathering the rest of a page it already knows it cannot
produce. There is a test for that, because the alternative — collecting three more
answers and then throwing them away — is a genuinely easy mistake to make.

**Nothing in the second diagram reaches the shopper.** The `DEGRADED` note goes to
the shop's own log. The shopper gets a product page. Telling them "recommendations
are currently unavailable" would be worse than silence, because for them nothing is
wrong.
