# Sequence Diagram

The interaction, which for a behavioural pattern matters more than the class
diagram. Three blocks: the naive method answering the wrong question, the same
order through a chain, and an order nobody claims.

![Sequence diagram](images/uml-diagram.png)

```mermaid
sequenceDiagram
    autonumber
    actor Checkout
    participant Naive as NaiveScreening
    participant Chain as ScreeningChain
    participant Address as AddressCheck
    participant Stock as StockCheck
    participant Fraud as FraudScoreCheck
    participant Payment as PaymentLimitCheck

    rect rgb(255, 232, 232)
    note over Checkout, Payment: R2001 — a monitor, £250 card, fraud score 92
    Checkout->>Naive: validate(request)
    Naive->>Naive: address ok
    Naive->>Naive: stock ok
    Naive->>Naive: card limit exceeded
    Naive-->>Checkout: REJECTED "try another card"
    note right of Naive: the fraud check is the next line<br/>and is never reached
    end

    rect rgb(232, 245, 233)
    note over Checkout, Payment: the same order, through the standard chain
    Checkout->>Chain: screen(request)
    Chain->>Address: screen(request, consulted)
    Address->>Stock: screen(request, consulted)
    Stock->>Fraud: screen(request, consulted)
    Fraud-->>Chain: Decision(REJECTED, "fraud-score")
    note over Payment: never called
    Chain-->>Checkout: report — decided by fraud-score,<br/>never ran: payment-limit
    end

    rect rgb(232, 240, 254)
    note over Checkout, Payment: a clean order — nobody has an opinion
    Checkout->>Chain: screen(request)
    Chain->>Address: screen(request, consulted)
    Address->>Stock: screen(request, consulted)
    Stock->>Fraud: screen(request, consulted)
    Fraud->>Payment: screen(request, consulted)
    Payment-->>Chain: Optional.empty()
    Chain->>Chain: fall back to the wiring's answer
    Chain-->>Checkout: APPROVED by "end of chain"
    end
```

## Reading It

**The red block** is the bug from
[`problem-statement.md`](problem-statement.md). Nothing goes wrong in it. Every
step is correct, the method returns a true statement about the card, and the
customer is told something actionable. The failure is the step that is missing,
and it is missing because of where it was typed.

**The green block** is the same four checks in the same program, and the
interesting arrow is the one that is not drawn. `PaymentLimitCheck` appears in
the diagram and is never called. That absence is the pattern: work behind a
decision is not merely irrelevant, it does not happen, and the report says so.

Note also that `Chain` appears twice and only twice — at the start and at the
end. It hands the order to the first link and does not see it again until
somebody answers. There is no loop in `ScreeningChain.screen`, no index, and no
knowledge of how many links exist.

**The blue block** is the liability. Four links, all consulted, none of them
willing to decide. Something still has to answer the customer, and what that
something says was chosen at wiring time — it is the `fallback` argument, and
there is no constructor without one.

## The Same Interaction, As A Flow

Where the order can go, once, per screening:

```mermaid
flowchart TD
    R[CheckoutRequest] --> A{address}
    A -- decides --> D[Decision, chain stops]
    A -- no opinion --> S{stock}
    S -- decides --> D
    S -- no opinion --> F{fraud-score}
    F -- decides --> D
    F -- no opinion --> P{payment-limit}
    P -- decides --> D
    P -- no opinion --> E[end of chain]
    E --> FB[the fallback given to the constructor]
    FB --> D
```

Every diamond has the same two exits, which is why the links can be reordered
without any of them being edited: no link knows which diamond it is.

![Screening flow](images/screening-flow.png)
