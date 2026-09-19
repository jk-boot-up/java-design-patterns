# Specification, Explained

## The pattern in one sentence

A specification is a business rule written as an object, that can say whether something satisfies it, and that combines with other rules into new ones.

## The six acts

### The Same Rule, Written Three Times

The search page and shipping agree. The promotion, written later, offers a mug at exactly ten pounds and a discontinued mug, because its copy of the rule says ten pounds or less and forgets discontinued.

```
  search page:   [MUG-BLUE, TEA-050]
  promotion:     [MUG-BLUE, MUG-RED, MUG-OLD, TEA-050]
  free shipping: [MUG-BLUE, TEA-050]
  the promotion includes MUG-RED at exactly 10.00 and MUG-OLD, which is discontinued. nobody meant that.
```

### The Rule, Named Once

The rule is built once from three small rules, and the search page, the promotion and shipping all use it. They agree.

```
  ((in stock and under £10) and not discontinued)
  search, promotion and shipping all ask for: [MUG-BLUE, TEA-050].
  change the rule in one place and all three change.
```

### Rules Combine

Small rules combine into a new one with and and or, and the new rule describes itself.

```
  ((a mug and under £10) or (on sale and a tea))
  [MUG-BLUE, MUG-OLD, TEA-050], in stock.
  three small rules, combined into a fourth, and no new class was written.
```

### A Rule Can Say Why Not

For each product that fails, the rule names the exact part it fails, so the explanation comes from the rule itself.

```
  MUG-RED: does not qualify, [under £10]
  MUG-OLD: does not qualify, [not discontinued]
  MUG-GREEN: does not qualify, [in stock]
  MUG-BLUE: qualifies
  the same object that decides can explain, so an error message is not written by hand.
```

### The Same Rule, Two Jobs

The same rule selects a list, and validates one product a customer picked, with the reason.

```
  to select: [MUG-BLUE, TEA-050].
  to validate one product a customer picked, MUG-OLD: refused, [not discontinued].
  one definition of cheap and available, used to filter a list and to check a single choice.
```

### The Bill

Finding sixty six products among ten thousand looks at all ten thousand, because a specification runs in memory. To let a database do it, the rule must be turned into a query. And a rule used once does not need a specification.

```
  10000 products. matches: 66. products looked at to find them: 10000.
  an in-memory specification looks at everything. to ask the database instead, the rule must be turned into a query.
  and for a rule used in one place, a plain lambda in the filter is simpler than a specification.
```

## The verdict

Use a specification when the same business rule is needed in several places, when rules must be combined or explained, or when a rule is chosen at run time. Keep the leaves small and name them in the business's words. Turn it into a query when the data is large. For a rule used once, a lambda is enough.

## How to recognise this in code you did not write

- An interface with `isSatisfiedBy` and `and`, `or`, `not`.
- Classes named for business conditions: `InStock`, `EligibleForDiscount`.
- Spring Data's `Specification` and JPA's `Predicate` composition.
- `Predicate.and` and `Predicate.or` in the JDK, which are the same idea.

## Where you have already met this

`java.util.function.Predicate` composes with `and`, `or` and `negate`. Spring Data JPA's `Specification` is the pattern, turned into a database query.

## When this is too much

For a condition used once, a lambda is clearer. A specification earns its place when a rule is shared, combined, or must explain itself.
