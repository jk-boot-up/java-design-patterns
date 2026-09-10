# The Interpreter Pattern, Explained

> **Given a language, define a representation for its grammar along with an
> interpreter that uses the representation to interpret sentences in the
> language.**
> — Gang of Four

That sentence puts people off, and it should not. Strip the vocabulary and it
says: *write one small class per kind of phrase, and let a big phrase hold
small ones.* The tree of objects you end up with **is** the sentence, and
running the sentence is calling one method on the top of the tree.

In this project the language is promotion rules, a sentence is
`country is UK and basket over 50`, and interpreting one is asking a tree of
`Rule` objects whether an order matches.

## One Interface, Two Kinds of Class

```java
public interface Rule {
    boolean matches(Order order);
    String describe();
}
```

Everything in the language implements that, and there are only two kinds of
implementation.

A **terminal** is a leaf. It holds no other rule, and answering it is one
comparison:

```java
public record BasketOver(int pounds) implements Rule {
    public boolean matches(Order order) { return order.basketPounds() > pounds; }
    public String describe()            { return "basket over " + pounds; }
}
```

A **non-terminal** holds other rules and answers by asking them:

```java
public record AndRule(List<Rule> parts) implements Rule {
    public boolean matches(Order order) {
        for (Rule part : parts) {
            if (!part.matches(order)) { return false; }
        }
        return true;
    }
}
```

Read `AndRule` again and notice what is *not* in it. It does not know what its
parts are. It does not know whether they are leaves or more `AndRule`s. It does
not know how many levels are below it, and it never finds out, because it only
ever asks. That is the whole trick, and it is why a rule of any shape and any
depth is used exactly like a rule with one comparison in it.

## Everyday Analogy: A Sentence Diagram

Think of how a sentence is put together. "The tall man in the blue coat" is a
noun phrase, and so is "the man" — one is more elaborate, but both fit in the
same slot. You can drop either into "…bought a laptop" without rewriting the
sentence around it.

A rule tree is the same idea. `basket over 50` and
`country is UK and basket over 50 or first order` are both a `Rule`, and both
fit wherever a `Rule` fits. The grammar composes, so the objects compose.

## Participants

| Role | In this project | Its job |
| --- | --- | --- |
| **Abstract expression** | `Rule` | Two methods, and everything is one of these |
| **Terminal expression** | `BasketOver`, `CountryIs`, `ItemsAtLeast`, `FirstOrder` | A leaf: one comparison, no children |
| **Non-terminal expression** | `AndRule`, `OrRule`, `NotRule` | Holds rules, answers by asking them |
| **Context** | `Order` | What a sentence is interpreted *against* |
| **Client** | `PromotionBook`, `VoucherRuleDemo` | Builds a tree, then calls `matches` once |

`RuleParser` is deliberately absent from that table. Building the tree is not
part of the pattern — the Gang of Four say so plainly, and hand-built trees are
a perfectly good use of it. The parser is here because a rule language nobody
can write in is not much of a language.

## The Grammar

The whole language is five phrases and two connectives:

```
rule       :=  group ( "or" group )*
group      :=  condition ( "and" condition )*
condition  :=  [ "not" ] terminal
terminal   :=  "basket over" N | "country is" X | "items at least" N
               | "first order"
```

Splitting on `or` first and `and` second is what gives *and* the tighter grip,
so `A and B or C` reads as `(A and B) or C` — the way a person says it. There
are no brackets, so that is the only precedence there is. It is a real limit,
and it is written down as one rather than discovered later.

## The Tree Can Explain Itself

`describe()` looks like a nicety and is not. Each node says its own piece and
asks its parts for theirs, so the sentence comes back out of the tree:

```java
"SAVE15 (15% off) applies when country is UK and basket over 100"
```

That string is rebuilt from the objects the checkout actually obeys — not
remembered from the line that was read in. If the two ever disagreed, this is
the one telling the truth. It is what makes "why did this order get 15% off?" a
question the code can answer, in the words the offer was written in, for the
audit log and for the shopper alike.

A round-trip test asserts that parsing a rule and describing it returns the
line unchanged, so that guarantee is checked rather than hoped for.

## A Typo Is Refused on Wednesday

```java
throw new IllegalArgumentException("I do not understand \"" + text + "\"");
```

A rule language that guesses is worse than no rule language. Every phrase the
parser cannot read is refused, naming the phrase, and `PromotionBook.fromLines`
therefore fails while the promotion is being *saved* rather than while an order
is being *priced*. Compare that with a mistyped Java condition, which is valid
Java and behaves wrongly at checkout with nothing to object to it.

## What You Gain

- **Rules are data.** A promotion is a line of text that can live in a
  database, a spreadsheet or a config file, and be edited by the people who own
  the offers.
- **New rules need no new code.** `BIGBASKET | 20 | basket over 200 or items at
  least 10` is a shape that appears nowhere in the code, and adding it is one
  line — no class, no compile, no deploy.
- **Composition is free.** Four terminals and three connectives already express
  more rules than anybody will write.
- **Each piece is testable alone.** `BasketOver` is one comparison; `AndRule`
  is a loop. Both fit in a test that reads like a sentence.
- **The rules can be printed.** For an audit log, a support screen, or a "why
  am I not getting this discount?" page.

## What to Watch Out For

**It does not scale to a big language.** One class per phrase is fine for seven
phrases and unbearable for seventy. A grammar with real syntax wants a parser
generator, not this pattern — the Gang of Four say the same thing, and it is
the most commonly ignored sentence in the chapter.

**The parser is the part that grows.** Adding a terminal is a small class and
one `if`. Adding *bracketed* expressions is a real parser, and that is a much
bigger day's work than it looks.

**It is slower than an `if`.** Every node is an object and every evaluation is
a virtual call. For three promotions on one order this is irrelevant. For a
rule evaluated a million times a second it is not, and the answer then is to
compile the tree once rather than to abandon the pattern.

**Do not reach for it when the rules never change.** If the shop has run the
same two promotions for four years, the two `if` statements are better code
than a language is. This pattern earns its keep when rules change often enough
that *shipping code* is the bottleneck.

**Keep the context small.** `Order` has four accessors, and every one of them
is a word marketing can use. Passing the whole application state in as the
context turns a language into a back door.

## Interpreter vs. Composite vs. Strategy

| | What it is | What it is for |
| --- | --- | --- |
| **Interpreter** | a tree of expressions with `matches` | evaluating a sentence in a small language |
| **Composite** | a tree of parts with the same interface | treating one thing and many things alike |
| **Strategy** | one interchangeable behaviour | swapping *how* something is done |

Interpreter *is* a Composite — the tree, the uniform interface and the "leaves
and containers look alike" property are exactly Composite's. The difference is
intent: Composite is about structure, Interpreter is about meaning. And a whole
rule tree is often used as a Strategy: the checkout holds a `Rule` and does not
care which one, which is Strategy's shape wrapped around Interpreter's insides.

## Where You Have Already Seen It

- **Regular expressions.** A compiled `Pattern` is a tree of expression
  objects, and `matches` walks it.
- **Search filters** — `price:<50 AND brand:acme` on any shop or issue tracker.
- **Spreadsheet formulas**, which are parsed into a tree and evaluated against
  the cells as context.
- **`java.util.function.Predicate`** with `and`, `or` and `negate`. Those three
  methods are non-terminal expressions, and the JDK ships them.

## Try It Yourself

1. **Add a terminal.** `country is not UK` already works via `not`; try adding
   `basket under N` instead. One record, one `if` in the parser, and no
   existing class changes — that is the property worth feeling.
2. **Break the precedence.** Swap the order of `parseOr` and `parseAnd` so
   `and` splits first, and watch `andBindsTighterThanOr` fail. Then work out
   which promotions would have quietly changed meaning.
3. **Break the round trip.** Make `OrRule.describe()` join with `" OR "` and
   watch the round-trip test catch it. The audit log and the tree are not
   allowed to drift.
4. **Add brackets.** This is the hard one, and it is meant to be: it is the
   moment the parser stops being a convenience and becomes a parser.

## See Also

- [`problem-statement.md`](problem-statement.md) — promotions as Java
  branches, and the two bugs that follow
- [`class-diagram.md`](class-diagram.md) — the static structure
- [`uml-diagram.md`](uml-diagram.md) — one order evaluated, message by message
- [`animation.html`](animation.html) — the same evaluation, stepped through
