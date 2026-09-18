# MVC Pattern — UML Sequence Diagrams

Four sequences: the pattern working, the shortcut that breaks it, the forced
change, and a refusal.

## 1. One Order, Rendered By Two Views That Cannot Disagree

The model is built once; both views read it and neither computes anything.

![MVC pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Ada as Customer
    participant Ctrl as OrderSummaryController
    participant Svc as PlaceOrderService
    participant Orders as OrderTable
    participant Model as OrderSummaryModel
    participant Screen as ScreenSummaryView
    participant Email as EmailConfirmationView

    Ada->>Ctrl: checkout(request, screen, emailView)
    Ctrl->>Svc: place(request)
    Svc-->>Ctrl: placed, ord-1001, £382.50
    Ctrl->>Orders: find(ord-1001)
    Orders-->>Ctrl: the saved Order
    Ctrl->>Model: of(order)
    Ctrl->>Screen: render(model)
    Screen-->>Ctrl: "Total: £382.50"
    Ctrl->>Email: render(model)
    Email-->>Ctrl: "...for £382.50 is confirmed."
```

</details>

Steps 7 and 9 call the same method on two different classes with the same
argument. Neither `render` implementation contains a `+` or a `*` — the
agreement is not tested for, it is structural.

## 2. The Shortcut — A View That Rounds Its Own Prices

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Ctrl as OrderSummaryController
    participant Model as OrderSummaryModel
    participant Rounded as RoundedEmailView «naive»
    participant Products as ProductTable

    Ctrl->>Rounded: render(model)
    Rounded->>Model: lines()
    Model-->>Rounded: 3 order lines, no prices
    loop each line
        Rounded->>Products: find(sku)
        Products-->>Rounded: the product, at today's catalogue price
        Note over Rounded: rounds the unit price to the<br/>nearest pound before multiplying
    end
    Rounded-->>Ctrl: "...for £383.00 is confirmed."
```

</details>

Compare this with sequence 1. `RoundedEmailView` never asks the model for
`total()` at all — it asks for the raw lines and goes hunting for prices
itself, in a class the model has no relationship with.

## 3. The Forced Change — A Real Second View, Nothing Else Touched

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Root as PlaceAnOrderDemo «composition root»
    participant Ctrl as OrderSummaryController
    participant Screen as ScreenSummaryView
    participant NewEmail as EmailConfirmationView

    Note over Root: the forced change is passing this one<br/>extra argument — new EmailConfirmationView()
    Root->>Ctrl: checkout(request, "ada@example.com",<br/>new ScreenSummaryView(), new EmailConfirmationView())
    Ctrl->>Screen: render(model)
    Ctrl->>NewEmail: render(model)
    Note over Ctrl,NewEmail: OrderSummaryModel, OrderSummaryController<br/>and ScreenSummaryView: byte-for-byte unchanged
```

</details>

## 4. A Refusal — Not Enough Stock

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Ada as Customer
    participant Ctrl as OrderSummaryController
    participant Svc as PlaceOrderService
    participant Products as ProductTable

    Ada->>Ctrl: checkout(3x GRD-014, only 2 in stock)
    Ctrl->>Svc: place(request)
    Svc->>Products: stockOf(GRD-014)
    Products-->>Svc: 2
    Note over Svc: refused before any view is even reached
    Svc-->>Ctrl: refused, "only 2 of GRD-014 left"
    Ctrl-->>Ada: refused, "only 2 of GRD-014 left"
```

</details>

No view or model is constructed at all on this path — a refusal never
reaches the presentation side of the controller.
