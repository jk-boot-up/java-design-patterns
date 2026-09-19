# Interpreter with SpEL, Explained

## The pattern in one sentence

SpEL is a ready-made interpreter: a text rule becomes a tree, and the tree is evaluated against an object.

## What is new here

The pattern is [Interpreter](../interpreter-pattern). This page is only what Spring Expression Language adds.

### The Rules Are Text

Four promotions, written as text. Three orders. Each order gets the promotions whose rule matches.

```
  WELCOME10 | 10 | firstOrder
  UKBIG | 15 | country == 'UK' and basketPence > 5000
  BULK | 20 | items >= 5 or basketPence > 20000
  NOTUK | 5 | !(country == 'UK')
  asha  (UK, 60.00, 2 items):            [UKBIG (15% off)]
  ben   (DE, 30.00, 1 item, first):      [WELCOME10 (10% off), NOTUK (5% off)]
  carol (UK, 250.00, 6 items):           [UKBIG (15% off), BULK (20% off)]
```

### The Language Came Free

A conditional, a regular-expression match and a remainder all work at once, because the library's language is much bigger than the four words the shop needed.

```
  a conditional, a pattern match and a remainder, and nothing new was written:
  ben:   [VOUCHER (8% off)]
  asha:  [MODULO (1% off)]
```

### Two Kinds Of Typo

A syntax error is caught when the book is built. A misspelled property name is accepted, and fails when the first order arrives.

```
  a rule that is not a valid expression is refused when the book is built: SpelParseException.
  a misspelled property is accepted when the book is built.
  it fails when the first order arrives: SpelEvaluationException.
```

### The Language Can Reach The Program

In the full context, a rule can call any static method in the program. The read-only context refuses that, and method calls too.

```
  with the full context, a rule can call any static method: [HOSTILE (99% off)].
  with the read-only context it is refused: SpelEvaluationException.
  it also refuses a method call, voucher.length(): SpelEvaluationException. a rule can only read properties.
  rules written by marketing are input. Use the read-only context.
```

### Missing Values

Asha has no voucher, so reading a property of it fails. The question-mark-dot operator turns that into no match.

```
  asha has no voucher, and voucher.empty fails: SpelEvaluationException.
  with the safe-navigation operator, asha: [], ben: [LONGVOUCHER (8% off)].
```

### Parsed Once

The four rules are parsed when the book is built. A thousand orders are then evaluated against the same trees.

```
  1000 orders through the same four parsed rules: 1500 promotions applied.
  the tree was built four times, at startup, not four thousand.
```

## The verdict

Use SpEL when the rules change without a release. Parse once, at startup. Use the read-only context for rules that come from people. Test every rule against real orders.

## How to recognise this in code you did not write

- `SpelExpressionParser` and `parseExpression`.
- `@Value("#{...}")` and `@ConditionalOnExpression`.
- `@PreAuthorize("hasRole('ADMIN')")`.

## Where you have already met this

Every `@Value("#{...}")` and every `@PreAuthorize`. Each is a SpEL expression.

## When this is too much

For a fixed handful of rules, plain Java is simpler and checked by the compiler.
