# Interpreter Pattern — UML Sequence Diagram

Shows the runtime interaction behind one evaluated rule. The order is £120 from
the UK with four items, and the promotion being checked is
`country is UK and basket over 100`. Follow how little each participant knows:
the book asks the promotion, the promotion asks the top of the tree, and the top
of the tree asks its parts.

![Interpreter pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Shopper
    participant Book as PromotionBook
    participant Promo as Promotion SAVE15
    participant Conj as AndRule
    participant Country as CountryIs UK
    participant Basket as BasketOver 100
    participant Order

    Note over Shopper,Order: context: £120, UK, 4 items, returning shopper

    Shopper->>Book: bestPercentFor(order)
    activate Book
    Book->>Promo: appliesTo(order)
    activate Promo
    Note over Promo: it holds a Rule.<br/>It does not know which one.
    Promo->>Conj: matches(order)
    activate Conj

    Conj->>Country: matches(order)
    activate Country
    Country->>Order: country()
    Order-->>Country: "UK"
    Country-->>Conj: true
    deactivate Country

    Conj->>Basket: matches(order)
    activate Basket
    Basket->>Order: basketPounds()
    Order-->>Basket: 120
    Basket-->>Conj: true
    deactivate Basket

    Note over Conj: every part said yes
    Conj-->>Promo: true
    deactivate Conj
    Promo-->>Book: true
    deactivate Promo
    Note over Book: 15% is the best so far
    Book-->>Shopper: 15
    deactivate Book

    Shopper->>Book: reasonsFor(order)
    activate Book
    Book->>Promo: explain()
    Promo->>Conj: describe()
    Conj->>Country: describe()
    Country-->>Conj: "country is UK"
    Conj->>Basket: describe()
    Basket-->>Conj: "basket over 100"
    Conj-->>Promo: "country is UK and basket over 100"
    Promo-->>Book: "SAVE15 (15% off) applies when …"
    Book-->>Shopper: the reason, in the words of the offer
    deactivate Book
```

</details>

## Notes

- **Every arrow points downwards, and none points sideways.** The book talks to
  promotions, a promotion talks to its one rule, and a connective talks to its
  parts. No participant reaches past its own children, which is why a rule three
  levels deep needs no new code anywhere above it.
- **`AndRule` does not know who it asked.** The two `matches` calls out of it are
  the same call; that one of them landed on a country check and the other on a
  basket check is invisible to it. Replace either part with a whole nested
  `OrRule` and this diagram grows a branch without a single line changing.
- **Only leaves touch the context.** Every arrow into `Order` comes from a
  terminal. The connectives never read the order at all, which is what keeps them
  reusable across a language they know nothing about.
- **`matches` short-circuits.** `AndRule` returns `false` on the first part that
  says no, so on the US order the `CountryIs` check ends the evaluation and
  `BasketOver` is never asked. The diagram for that order is shorter, and that is
  the loop in `AndRule` doing it, not any cleverness in the parser.
- **The second half is the same walk, for words instead of a verdict.**
  `describe()` visits exactly the nodes `matches()` did and returns the sentence
  the offer was written in. Because it is rebuilt from the objects the checkout
  obeyed — not remembered from the line that was read in — the audit log cannot
  disagree with the decision.
- **The tree was built earlier, and once.** `RuleParser` appears nowhere in this
  diagram: parsing happened when the promotion was saved. A typo would have been
  refused then, on a Wednesday, rather than mispricing an order on Friday.
- Compare with `NaiveVoucherRules`: there is no diagram to draw. One method, a
  run of `if` statements, no participants and no messages — and no place for
  anything to explain itself, which is precisely why its two wrong answers came
  out silently.
