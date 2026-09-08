# The Command Pattern, Explained

The Gang of Four definition:

> *"Encapsulate a request as an object, thereby letting you parameterize
> clients with different requests, queue or log requests, and support
> undoable operations."*

In plain language: **make the action an object, and it can be held, listed,
logged and reversed.**

## The Thing a Method Call Cannot Do

A method call is an event. It happens, it returns, and then it is gone. You
cannot ask it what it did. You cannot put it in a list. You cannot run it
later, or on a different cart, or backwards.

Undo needs every one of those. So the first move is not clever: stop calling
the method, and make an object that *is* the call.

```java
public interface CartCommand {
    String describe();
    void execute(Cart cart);
    void undo(Cart cart);
}
```

That is the entire pattern. Everything below is consequences.

## Everyday Analogy: The Order Slip

A waiter does not carry your words to the kitchen. They write a slip.

The slip can be **stacked** with the others, **read back** to you, **passed**
to a different chef, **found again** an hour later when you query the bill,
and **torn up** if you change your mind before it is cooked. None of that is
possible with a spoken request, which exists only while it is being said.

The slip is the command. The kitchen is the receiver. The waiter — who can
carry any slip without being able to cook anything — is the invoker.

## Participants

| Role | Here | Responsibility |
| --- | --- | --- |
| Command | `CartCommand` | Declares `execute` and `undo` |
| Concrete commands | `AddItemCommand`, `RemoveItemCommand`, `ChangeQuantityCommand`, `ApplyCouponCommand` | One edit each, and its exact inverse |
| Receiver | `Cart` | Knows how to change; knows nothing about commands |
| Invoker | `CartHistory` | Runs commands, keeps the undo and redo stacks |
| Client | `CartCommandsDemo` | Decides which command to build |
| Naive alternative | `NaiveCartEditor` | Direct mutation plus ad-hoc undo notes |

Note which way the ignorance runs. `Cart` has never heard of a command, and
`CartHistory` has never heard of a coupon. Only the concrete commands know
both, and each knows only its own edit.

## Code Walkthrough

### The command that is not trivial to reverse

Read this one twice. It is the reason the project exists.

```java
public void execute(Cart cart) {
    previousQuantity = cart.quantityOf(sku);
    cart.putLine(new CartLine(sku, name, unitPrice, previousQuantity + quantity));
    executed = true;
}

public void undo(Cart cart) {
    if (previousQuantity == 0) {
        cart.removeLine(sku);
    } else {
        cart.putLine(new CartLine(sku, name, unitPrice, previousQuantity));
    }
}
```

Adding 2 to a cart that held 3 leaves 5. Undoing that is **not** "remove the
line" — it is "put it back to 3". Which of the two applies is not known when
the command is constructed, only when it runs. Hence a field the constructor
does not set.

This is the general rule, and it is the one place undo bugs live:

> **Capture the state you will need to reverse yourself inside `execute`,
> from the receiver, at the moment you run.**

Not in the constructor: that is a guess about a cart you have not reached
yet, and an earlier undo may have made it wrong before you get there.

### The command that has to remember *where*

```java
public void execute(Cart cart) {
    position = cart.positionOf(sku);
    removed = cart.removeLine(sku).orElseThrow(...);
}

public void undo(Cart cart) {
    cart.insertLineAt(position, removed);
}
```

Undoing a removal by adding the line back puts it last. To the customer
looking at the screen, that is not undo. Position is part of the state, so
position is part of what gets restored.

### The command whose undo is usually — but not always — nothing

```java
public void execute(Cart cart) {
    previousCoupon = cart.coupon().orElse(null);   // very often null
    cart.setCoupon(coupon);
}

public void undo(Cart cart) {
    cart.setCoupon(previousCoupon);
}
```

A cart holds one coupon, so applying a second replaces the first. Clearing
the coupon on undo is right nine times in ten, and the tenth time it takes a
discount off a customer who never touched it. Restoring `previousCoupon`
handles both cases without a branch.

### The invoker, which knows nothing

```java
public void execute(CartCommand command) {
    command.execute(cart);
    done.push(command);
    undone.clear();
}

public boolean undo() {
    if (done.isEmpty()) { return false; }
    CartCommand command = done.pop();
    command.undo(cart);
    undone.push(command);
    return true;
}
```

Search `CartHistory` for the words *coupon*, *quantity* or *SKU*. They are
not there. It holds `CartCommand`s and does two things with them. That is
precisely why a fifth kind of edit does not touch this file.

Two decisions worth naming:

- **`undone.clear()` on a new command.** Once you take a different branch,
  the old future is unreachable. Every text editor you have used does this.
- **A command that throws is not pushed.** An edit that failed halfway is not
  on the undo stack, because undoing it would apply the reverse of something
  that never fully happened.

## Why the Tests Are the Proof

A test that says "adding two items leaves two items" passes against the
naive editor too. It tests the cart, not the pattern. Three tests here do
not:

- **`undoingAMergedAddRestoresThePreviousQuantity`** — the exact case the
  hand-rolled note gets wrong.
- **`undoRestoresTheReplacedCoupon`** — the other one.
- **`anUnknownCommandWorksUnchanged`** — a gift-wrapping command declared
  inside the test, executed and undone by a `CartHistory` that was compiled
  before it existed. If somebody put a `switch` back in the invoker
  tomorrow, this is the test that goes red.

`NaiveCartEditorTest` asserts the buggy behaviour *as it is*, deliberately.
Those tests are not a claim that the naive version is unfixable — they are
what "fixing it" would have to make fail.

## What You Gain

- **Undo and redo**, exactly, including the cases that depend on prior state.
- **An audit trail for free.** `history.log()` is a list of strings because
  every edit is already an object that can describe itself.
- **A new edit is one class.** No file that already works is opened.
- **Each edit is testable alone**, without an invoker and without a UI.
- **Deferral becomes possible.** A command can be queued, scheduled, sent
  over a wire, or replayed against a different cart — none of which a method
  call can be.

## What to Watch Out For

- **Every operation becomes a class.** For four edits that will never change,
  the naive version is a third of the code and it works. Command pays when
  undo, logging or queuing is a requirement — and undo alone is usually
  enough.
- **The inverse is your problem, and it is where the bugs are.** The pattern
  gives you a place to put `undo`; it does not check that yours is right.
  Every command needs the test that executes it *and then undoes it* against
  a cart that was not empty.
- **Undo must be called in order, on the state the command left behind.**
  `CartHistory` guarantees that. Calling `undo` by hand out of order is
  undefined, which is why each command here refuses to undo before it has
  run.
- **Do not let commands hold live receiver objects.** They hold values — a
  SKU, a quantity, a coupon — never a line the cart may have replaced
  underneath them.
- **Not every operation should be a command.** Reads should not be. If it
  does not change anything, there is nothing to undo and nothing to log.

## Command vs. Memento vs. Strategy vs. Observer

| Pattern | The object is | Undo works by | Tell them apart by |
| --- | --- | --- | --- |
| **Command** | A request | Each command reversing itself | You need a *list of what was done* |
| **Memento** | A snapshot of state | Restoring the whole snapshot | You need to *get back*, and do not care what changed |
| **Strategy** | An algorithm | — | The choice comes from outside and stays put |
| **Observer** | A subscription | — | One change, many independent reactions |

Command and Memento are the two answers to undo, and the trade is clean:
Command stores *the difference* and needs each edit to know its inverse;
Memento stores *the state* and needs no inverses at all, at the cost of a
copy per step and no record of what changed. Real editors often use both.

## Where You Have Already Seen It

- **`Runnable` and `Callable`** — a command with one method and no undo.
  Every `ExecutorService` is an invoker.
- **`javax.swing.Action`** and the undo support in `javax.swing.undo`, which
  is this pattern almost name for name.
- **Database migrations** — `up()` and `down()`.
- **Event sourcing** — the log of commands *is* the system of record; the
  current state is a fold over it.
- **The HTTP request objects** in every web framework: a request reified so
  it can be queued, retried and logged.

## Try It Yourself

1. Write a `ClearCartCommand` that empties the cart, and make its undo put
   every line back in order. Notice that it has to capture a list, and that
   nothing else in the project changes.
2. Give `CartHistory` a `undoAll()` and check it against
   `everyCommandIsSubstitutableForEveryOther`.
3. Add gift wrapping to `NaiveCartEditor` instead, and count the files you
   had to open.
4. Make `AddItemCommand` capture `previousQuantity` in its *constructor*
   rather than in `execute`, then run the whole suite. Exactly one test goes
   red, and it is the one that undoes twice.

## See Also

- [`problem-statement.md`](problem-statement.md) — the outage this fixes
- [`class-diagram.md`](class-diagram.md) — the structure
- [`uml-diagram.md`](uml-diagram.md) — an execute and an undo, side by side
- [`animation.html`](animation.html) — step through the stacks
