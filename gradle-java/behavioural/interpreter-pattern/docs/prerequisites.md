# Prerequisites

Everything you need before starting the Interpreter pattern project. The
pattern has a reputation for being the hard one in the book. It is not; it is
the one with the worst-worded definition. If you can write a class with one
method in it, you can write an interpreter.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, interfaces, `implements`, `new`.
- **Interfaces and polymorphism** — that a variable of type `Rule` can hold any
  class that implements `Rule`, and that calling `matches` on it runs whichever
  one is actually in there. Everything in this project rests on that one fact.
- **Collections** — `List`, `List.of(...)`, and a `for` loop over a list.
- **Records** — `record BasketOver(int pounds) implements Rule`. Read it as "a
  small immutable class with the constructor, accessors and `equals` written for
  you". Records can implement interfaces, and here every rule is one.

### Helpful, but explained as we go

- **Recursion, gently** — a class that holds a list of its own interface type,
  and a method that calls the same method on each item. There is no arithmetic
  and no base-case puzzle; if you can follow a folder containing folders, you
  can follow this.
- **`String.split` with a regular expression** — the parser uses two, and both
  are shown and explained where they appear. You do not need to know regex.
- **Any experience of a search filter** — `price:<50 AND brand:acme` in a shop
  or an issue tracker. You have used an interpreter; this project builds one.

### Explicitly NOT required

- Compilers, parser generators, ANTLR, grammars or formal language theory. The
  grammar here is five phrases long and is printed in full in the explainer.
- Any expression-evaluation library, scripting engine or rules engine.
- Threads, reflection, or serialization.
- Any other design pattern — though [Composite](../../structural/composite-pattern)
  is the same shape with a different purpose, and worth comparing afterwards if
  you have met it.

## A 60-Second "One Interface, Two Kinds of Class" Primer

Everything in the language implements this:

```java
public interface Rule {
    boolean matches(Order order);
    String describe();
}
```

A **terminal** is a leaf. It holds no other rule, and answering is one
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

That is the entire pattern. Everything else in the project is those two shapes
repeated, or a convenience built on top of them.

## A 60-Second "The Tree Is the Sentence" Primer

The rule `country is UK and basket over 50` is never stored as text. It is
stored as objects:

```java
new AndRule(List.of(new CountryIs("UK"), new BasketOver(50)))
```

Draw that and you get a tree: an `AndRule` at the top with two leaves under it.
Asking the top whether an order matches sets off one call per node, downwards,
and the answers come back up. Ask the top to `describe()` itself and you get the
sentence back — rebuilt from the objects rather than remembered.

Because `AndRule` holds `Rule` and not "a leaf", either of those two children
could be replaced by another whole tree, and nothing above would change. That is
what "composes" means, and it is worth spending the sixty seconds on.

## A 60-Second "Context" Primer

A sentence has to be interpreted *against* something. Here it is one order:

```java
public record Order(int basketPounds, String country, int itemCount,
                    boolean firstOrder) { }
```

Four accessors, and they are also the entire vocabulary of the language — you
can only write rules about things the context can be asked. Keeping the context
small is therefore a design decision, not an oversight: it is what stops a rule
language turning into a back door into the application.

## Software Prerequisites

| Tool | Version | Why |
| --- | --- | --- |
| JDK | 21 | The project is built against Java 21 |
| Gradle | none needed | The wrapper (`./gradlew`) downloads it |
| An IDE | any | IntelliJ IDEA, VS Code, Eclipse — all fine |

### Installing JDK 21

**macOS** (Homebrew):

```bash
brew install openjdk@21
```

**Linux** (Debian/Ubuntu):

```bash
sudo apt install openjdk-21-jdk
```

**Windows** — download a build from
[Adoptium](https://adoptium.net/temurin/releases/?version=21) and run the
installer.

Verify:

```bash
java -version
```

You want to see `21` at the start of the version string.

### Gradle

Do not install it. Every command in this project uses the wrapper script
checked in alongside the source:

```bash
./gradlew build      # macOS / Linux
gradlew.bat build    # Windows
```

The first run downloads the right Gradle version and takes a minute. Later
runs are quick.

## Verify Your Setup

From the project directory:

```bash
./gradlew test
```

You should see the build succeed with **21 tests**. Then:

```bash
./gradlew run
```

You should see five sections. In the second, an overseas order takes 15% off
that it should never have had, and a qualifying UK shopper is offered nothing —
with no exception thrown for either. That is wrong, and it is meant to be. The
third section runs the same three orders through rules written as text and gets
them all right, with a "because" line for each. The fourth adds a promotion
nobody anticipated in one line, and the fifth refuses a rule with a typo in it.

If all five print, you are ready.

## Troubleshooting

**`./gradlew: Permission denied`** — mark it executable:

```bash
chmod +x gradlew
```

**`Unsupported class file major version`** — Gradle picked up an older JDK.
Check `java -version`, and point Gradle at 21 explicitly if you have several
installed:

```bash
./gradlew test -Dorg.gradle.java.home=/path/to/jdk-21
```

**The tests fail in `NaiveVoucherRulesTest`** — somebody has fixed one of the
deliberate bugs in `NaiveVoucherRules`. Those two bugs are the lesson; put them
back.

**`parsingAndDescribingRoundTrip` fails** — a `describe()` has been changed so
that a rule no longer reads back the way it was written. That is the test doing
its job: the audit log and the tree the checkout obeys are not allowed to drift
apart.

**`I do not understand "…"`** — the parser refusing a phrase it does not know.
The vocabulary is `basket over N`, `country is X`, `items at least N`,
`first order`, and the connectives `and`, `or` and `not`. There are no brackets.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — promotions as Java
   branches, and the two bugs that follow
2. `NaiveVoucherRules` in the source — three branches, two of them wrong, no
   exceptions
3. [`interpreter-pattern-explained.md`](interpreter-pattern-explained.md) — the
   pattern and the code
4. [`class-diagram.md`](class-diagram.md) and
   [`uml-diagram.md`](uml-diagram.md) — the family of classes, then one rule
   evaluated through them
5. [`animation.html`](animation.html) — the same evaluation, step by step, in a
   browser
6. `./gradlew run`, then read `VoucherRuleDemo` alongside its output
