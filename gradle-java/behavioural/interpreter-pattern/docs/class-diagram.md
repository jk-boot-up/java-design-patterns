# Interpreter Pattern — Class Diagram

Shows the static structure: one interface, four leaves, three connectives, and
the order they are all asked about. The version that writes the same promotions
as Java branches is drawn alongside, and the difference between one growing
method and a family of tiny classes is the whole argument.

![Interpreter pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Rule {
        <<interface, abstract expression>>
        +matches(Order) boolean
        +describe() String
    }

    class BasketOver {
        <<terminal, record>>
        +int pounds
    }

    class CountryIs {
        <<terminal, record>>
        +String country
    }

    class ItemsAtLeast {
        <<terminal, record>>
        +int count
    }

    class FirstOrder {
        <<terminal, record>>
    }

    class AndRule {
        <<non-terminal, record>>
        +List~Rule~ parts
    }

    class OrRule {
        <<non-terminal, record>>
        +List~Rule~ parts
    }

    class NotRule {
        <<non-terminal, record>>
        +Rule part
    }

    class Order {
        <<context, record>>
        +int basketPounds
        +String country
        +int itemCount
        +boolean firstOrder
    }

    class RuleParser {
        <<not part of the pattern>>
        +parse(String) Rule
    }

    class Promotion {
        <<record>>
        +String code
        +int percentOff
        +Rule rule
        +fromLine(String) Promotion
        +appliesTo(Order) boolean
        +explain() String
    }

    class PromotionBook {
        <<client>>
        +fromLines(List~String~) PromotionBook
        +bestPercentFor(Order) int
        +reasonsFor(Order) List~String~
    }

    class NaiveVoucherRules {
        <<the trap>>
        +bestPercentFor(Order) int
    }

    class VoucherRuleDemo {
        <<client>>
        +main(String[])
    }

    Rule <|.. BasketOver
    Rule <|.. CountryIs
    Rule <|.. ItemsAtLeast
    Rule <|.. FirstOrder
    Rule <|.. AndRule
    Rule <|.. OrRule
    Rule <|.. NotRule

    AndRule o-- Rule : holds many
    OrRule o-- Rule : holds many
    NotRule o-- Rule : holds one

    Rule ..> Order : matches(order) reads it
    RuleParser ..> Rule : builds the tree
    Promotion o-- Rule
    Promotion ..> RuleParser : fromLine()
    PromotionBook o-- Promotion
    VoucherRuleDemo ..> PromotionBook
    VoucherRuleDemo ..> NaiveVoucherRules : the same offers, as branches
```

</details>

## Notes

- `Rule` is the **abstract expression**, and it is the reason the picture works.
  Two methods, no fields, and every other rule class in the project is one of
  these. That is what lets a rule of any shape sit wherever a rule is expected.
- The four **terminal expressions** are the leaves. Each holds a value and one
  comparison, and none of them holds another `Rule` — look at the diagram and
  they have no line going back into `Rule` at all. `FirstOrder` is a record with
  no components, which costs nothing and gives it a free `equals`, so a test can
  compare two parsed trees for equality.
- The three **non-terminal expressions** are the only classes with an aggregation
  line back into `Rule`, and that single loop in the diagram is the recursion.
  `AndRule` holding `Rule` means it can hold another `AndRule`, or an `OrRule`,
  or a leaf — and it never learns which, because it only ever calls `matches`.
- **The tree is the sentence.** `country is UK and basket over 50` is not stored
  as a string anywhere; it is an `AndRule` holding a `CountryIs` and a
  `BasketOver`. `describe()` walks back down and rebuilds the words, which is why
  the audit log and the code the checkout obeys cannot drift apart.
- `Order` is the **context** — the thing a sentence is interpreted against. Every
  arrow into it comes from a terminal, because only leaves ask questions. Keeping
  it to four accessors keeps the language to four nouns.
- `RuleParser` is marked as not part of the pattern on purpose. Trees can be
  built by hand, and `RuleTest` does exactly that. The parser turns the pattern
  into a feature marketing can use, but the pattern is the tree.
- `PromotionBook` is a client and contains no mention of countries, baskets or
  item counts. It asks each promotion whether it applies. Every fact about *when*
  an offer applies lives in a line of text.
- `NaiveVoucherRules` is the same three promotions as hand-written branches, and
  it holds two copy-paste mistakes: SAVE15 never got the UK check written, so
  overseas orders take 15%, and FREESHIP inherited a `firstOrder()` test from a
  retired offer, so returning shoppers are offered nothing. Both are pinned by
  passing tests rather than fixed.
