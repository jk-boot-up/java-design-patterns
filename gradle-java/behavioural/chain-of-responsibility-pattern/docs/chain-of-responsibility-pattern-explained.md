# The Chain of Responsibility Pattern

## In One Sentence

Hand a request to a series of objects, one after another, until one of them
takes it.

Each link either answers — and the run stops there — or says nothing and passes
the request along. The caller does not know which link will answer, or even
whether any of them will.

## Intent

> Avoid coupling the sender of a request to its receiver by giving more than
> one object a chance to handle the request. Chain the receiving objects and
> pass the request along the chain until an object handles it.
>
> — *Design Patterns*, Gamma, Helm, Johnson, Vlissides

Read the first clause carefully. The pattern is not primarily about running
several checks in a row — you can do that with a `for` loop. It is about the
caller not knowing **which** of them will answer.

## The Thing A Sequence Of `if`s Cannot Do

Four checks in one method are four checks in one method. They can be reordered
by editing the method, extracted into private helpers, and tested by
constructing enough state to reach them. All of that is achievable and none of
it is the problem.

The problem is that the *sequence* is not a value. You cannot pass it, store it,
print it in a support tool, configure it per market, or have two of them. When
the trade flow needs the same checks minus one, the only tool the language gives
you is a second method — and a second method is a copy, and copies drift.
`NaiveScreening.validateTradeAccount` lost the address check in exactly this
way, and nothing noticed, because nothing in the code says the two methods are
related.

Turning each check into an object makes the sequence a value:

```java
Decision approveIfNobodyObjects = Decision.approved("end of chain", "no link objected");

ScreeningChain standard = new ScreeningChain("standard", approveIfNobodyObjects,
        new AddressCheck(),
        new StockCheck(onShelf),
        new FraudScoreCheck(),
        new PaymentLimitCheck());

ScreeningChain trade = new ScreeningChain("trade-account", approveIfNobodyObjects,
        new AddressCheck(),
        new StockCheck(onShelf),
        new FraudScoreCheck());
```

The trade flow is the standard flow with one line deleted from the wiring. No
check was copied, so no check could be lost.

## The Analogy: An Expenses Approval

Submit a £40 lunch receipt and your team lead approves it. Submit £4,000 of
laptops and your team lead cannot — the claim goes up to their director.
£400,000 goes to the board.

Three things about that office are the pattern:

1. **You submit once.** You do not address the claim to whoever is empowered to
   approve that amount; you do not know the thresholds and you should not have
   to.
2. **Whoever can answer, answers, and it stops there.** The board does not see
   your lunch receipt. Not because they would object — because nobody asked
   them.
3. **The hierarchy is not printed on the claim form.** It is set up elsewhere,
   it differs between departments, and it changes without the form changing.

And the failure mode is the pattern's too: a claim that nobody in the hierarchy
is authorised to approve sits in a queue forever, and nobody is told. That is
the unhandled request, and it is why `ScreeningChain` will not let you build a
chain without saying what "nobody decided" means.

## Participants

| Role | In this project | What it does |
| --- | --- | --- |
| Handler | `ScreeningHandler` | holds the successor; declares `check`; walks the chain in a `final` method |
| Concrete Handlers | `AddressCheck`, `StockCheck`, `FraudScoreCheck`, `PaymentLimitCheck` | one check each, and nothing else |
| Client / builder | `ScreeningChain` | assembles the links, names the fallback, starts the request off |
| Request | `CheckoutRequest` | immutable; no link can change what the next one sees |
| Answer | `Decision`, `Outcome` | approved, rejected or referred, plus who said so |
| Evidence | `ScreeningReport` | which links ran, and which never did |

Nine classes in total. `ScreeningHandler` is the pattern; the other eight give
it something to do.

## The Design in Three Decisions

### 1. The walk is written once, and it is `final`

```java
final Optional<Decision> screen(CheckoutRequest request, List<String> consulted) {
    consulted.add(name());
    Optional<Decision> mine = check(request);
    if (mine.isPresent()) {
        return mine;
    }
    return next == null ? Optional.empty() : next.screen(request, consulted);
}
```

In the textbook version each handler writes its own
`if (canHandle) ... else next.handle(request)`. That version has a bug waiting
in it: a handler that declines to handle something and forgets the `else`. The
request vanishes, no exception is thrown, and the symptom appears somewhere else
entirely.

Here there is one copy of that logic, a subclass cannot override it, and a link
author writes only:

```java
protected Optional<Decision> check(CheckoutRequest request);
```

Empty means *no opinion, pass it on*. A present `Decision` means *I am
answering, and the chain stops here*. Those are two different things, and half
the confusion about this pattern is people reading "returns nothing" as "says
no".

### 2. A link is not obliged to reject

Most explanations imply handlers only ever say no. A handler stops the chain
whenever it is willing to take responsibility for the answer, and the answer can
be anything. `FraudScoreCheck` is the clearest case, because it can produce all
three outcomes:

```java
if (score >= REJECT_AT) return Optional.of(Decision.rejected(name(), ...));
if (score >= REFER_AT)  return Optional.of(Decision.referred(name(), ...));
return Optional.empty();
```

A score of 64 is neither a yes nor a no — it is "a person should look at this",
and that third answer is the one the naive version cannot express, so it guesses
and guesses cheaply. The chain does not care which of the three came back; it
only cares that a decision came back at all.

### 3. What is *not* consulted is part of the answer

```
R2002   £45     GB   JE3 8QX  card limit £2000   fraud 10
   -> REJECTED  by address        no courier covers JE3 8QX
              never ran: stock, fraud-score, payment-limit
```

The risk model was not called and not billed for. This is the observable
difference between this pattern and a validator that collects every problem with
a request: **a chain gives you one answer, from one link, and stops.** If your
requirement is "tell the customer everything wrong with their order at once", do
not build this — build a collector.

### 4. Falling off the end is a named policy, not a `null`

`ScreeningChain`'s constructor takes the fallback, and there is no constructor
that omits it:

```java
new ScreeningChain(name, Decision.approved("end of chain", ...), links...);  // fails open
new ScreeningChain(name, Decision.referred("end of chain", ...), links...);  // fails closed
```

Same links, opposite risk appetites, one argument apart. The GoF book lists
"receipt isn't guaranteed" as a liability of this pattern and leaves it there.
It is a real liability, and this is what dealing with it deliberately looks
like.

## Chain of Responsibility vs Decorator

Both are objects holding the next object. Both build a run-time structure out of
small pieces. On a class diagram they are indistinguishable, which is why the
comparison belongs here rather than in a footnote.

**The question a developer can actually ask at the point of choosing:** *does
every layer have to run?*

- If the answer is yes — every layer contributes something to a result that is
  assembled on the way through — you want **Decorator**, and a layer that
  declined to delegate would be a bug.
- If the answer is no — a layer may be able to settle the matter by itself, and
  the layers behind it should then not run — you want **Chain of
  Responsibility**, and a layer that always delegated would be pointless.

In code the tell is one character deep: in a decorator, the call to the next
object is unconditional; in a handler, it is inside an `if`.

## Why the Tests Are the Proof

An outcome test — "a Jersey order is rejected" — passes against
`NaiveScreening` just as happily as against the chain. It proves nothing about
the pattern.

`ScreeningChainTest` asserts the things only a chain gives you:

- a link behind a decision **never runs**, and the report names it,
- the same links wired in two orders give two different answers,
- an unclaimed request gets the fallback that the wiring named,
- a link declared inside the test file joins a chain that was compiled without
  it ever having existed.

`ChecksTest` makes the isolation argument by omission: every test builds one
check and asks it one question, with none of the state the other checks need.

`NaiveScreeningTest` pins the bugs with *passing* tests — including the one
where the standard method catches the Jersey order and the copied trade method
does not.

## What You Gain

- **Each check is one class**, testable with nothing else set up.
- **The order is a value** — printable, configurable, and different per flow.
- **Variants are subsets**, not copies, so a check cannot be lost in a copy.
- **Work is skipped**, and the skipping is visible.
- **New checks need no change to any existing class**, including the chain.

## What You Give Up

- **The policy is no longer readable in one place.** `validate` could be read
  top to bottom. The wiring lists the links, but what each does is elsewhere.
- **You need the report.** "Which link rejected this?" is not answerable from
  the verdict alone. Four `if`s never needed that.
- **A request can go unanswered**, and dealing with that is work the naive
  version did not have.
- **Link instances are single-use.** A handler holds its successor, so build a
  second chain from fresh instances.
- **More classes.** Four checks, a handler base, a chain, a report.

## When Not To Use It

- **The checks and their order never change.** Write the four `if` statements.
  The demo says this in the program's own output.
- **Every problem must be reported, not just the first.** That is a collector,
  not a chain.
- **The order between checks is a genuine dependency** — check B is only
  meaningful after check A has passed and produced something. That is a
  pipeline, not a chain of independent links.
- **There are two checks.** Two objects, a base class and a wiring line is more
  machinery than `if (a) ... if (b) ...` however elegant it is.

## Related Patterns

| Pattern | Relationship |
| --- | --- |
| [Decorator](../../../structural/decorator-pattern) | same structure; every layer runs, and a layer cannot end the run |
| [Composite](../../../structural/composite-pattern) | often the structure a chain is walked over in GUI event handling — the parent is the successor |
| [Command](../../command-pattern) | a chain answers *who handles this request*; a command turns *the request itself* into an object, and the two combine well |
| [Strategy](../../strategy-pattern) | one object chosen to do the work, chosen by the caller; a chain chooses itself, at run time, out of several candidates |
