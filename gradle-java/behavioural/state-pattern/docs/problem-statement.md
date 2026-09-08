# Problem Statement — An Order That Behaves Differently Depending On Where It Is

## The Scenario

An order in an online shop moves through a small, well understood lifecycle.

```
PLACED --pay--> PAID --pack--> PACKED --ship--> SHIPPED --deliver--> DELIVERED
```

Two of those are the end of the story: `CANCELLED` and `REFUNDED`. Nothing
happens to an order after it reaches either.

Six things can be asked of an order — `pay`, `pack`, `ship`, `deliver`,
`cancel` and `refund` — and the answer to every one of them depends on where
the order currently is:

| Asked to… | PLACED | PAID | PACKED | SHIPPED | DELIVERED |
| --- | --- | --- | --- | --- | --- |
| pay | takes the money | no | no | no | no |
| pack | no | boxes it | no | no | no |
| ship | no | no | books a courier | no | no |
| deliver | no | no | no | signs it for | no |
| cancel | yes, nothing to refund | yes, refund | yes, refund **and put the stock back** | **no** | no, that is a return |
| refund | no | no | no | no | yes, once |

Read the `cancel` row twice. It is not a permission check with a yes and a no
in it. It is four genuinely different pieces of work: cancelling a `PLACED`
order moves no money at all, cancelling a `PAID` one refunds, cancelling a
`PACKED` one refunds *and* unpacks a box that somebody has already taped shut,
and cancelling a `SHIPPED` one is not a thing you can do — the goods are on a
van and the shop has nothing to put back on a shelf.

## The Obvious First Move

A status field and a check at the top of each method.

```java
public enum Status { PLACED, PAID, PACKED, SHIPPED, DELIVERED, CANCELLED, REFUNDED }

public void cancel(String reason) {
    if (status == Status.DELIVERED || status == Status.CANCELLED
            || status == Status.REFUNDED) {
        throw new IllegalTransitionException(status.name(), "cancel",
                "it is not cancellable");
    }
    Money back = ledger.charged().minus(ledger.refunded());
    if (!back.isZero()) {
        ledger.refund(back);
    }
    move(Status.CANCELLED, reason + " — refunded " + back);
}
```

Be fair to this. It is short, it needs no vocabulary, one file holds the whole
lifecycle, and a new reader can see every rule by scrolling. For a machine
this size, an enum and a map of permitted transitions is often the *right*
answer, and this project says so out loud at the end. The problem is not the
enum. The problem is what happens to the conditionals around it.

## Where It Breaks

The rules are not written down once. They are written down once **per
method**, and each copy is phrased slightly differently.

### Drift one: the guard that was phrased as a sentence

`cancel` above was written as "anything that has not arrived yet can be
cancelled", and so it lists the three states where it must refuse. It reads
sensibly. It is also wrong, because `SHIPPED` is not on that list — the parcel
is on a van, and the method takes the money out of the till and gives it back.

```
A SHIPPED order, and the screen the agent is looking at:
  status          : SHIPPED
  buttons drawn   : [deliver]
  cancel() anyway : accepted — status is now CANCELLED
```

### Drift two: the guard somebody widened on purpose

`refund` originally accepted only `DELIVERED`. Support asked for `CANCELLED`
to be added so they could "sort out" cancelled orders. A cancel has already
refunded, so the second refund pays the customer a second time.

```
A CANCELLED order, already refunded once:
  ledger          : charge £97.49; refund £97.49
  refund() anyway : accepted — status is now REFUNDED
  the shop is out : -£97.49 over 2 refunds
```

### Drift three: the copy that is right, and disagrees

There is a third copy of the same rules, written for the screen:

```java
public List<String> allowedActions() {
    return switch (status) {
        case SHIPPED -> List.of("deliver");
        ...
    };
}
```

That one is correct. It says a shipped order can only be delivered. So the
cancel button is never drawn — and the endpoint accepts the call anyway. The
bug is invisible from the UI, and reachable from anything that is not the UI.

Every one of these is a single condition inside a chain that was copied and
then edited. None of them is a mistake anybody would make while looking at the
whole lifecycle at once. They happen precisely because nobody ever is.

## What We Actually Want

* One place per state, holding **everything** true about that state.
* Refusals that exist by default, so a rule that was never written is a
  refusal rather than an accident.
* Behaviour that varies by state, not just permissions — cancelling a `PAID`
  order and a `PACKED` one do different work, and the code should show that.
* A screen and an endpoint that cannot disagree, because they ask the same
  object.
* A new state that does not mean editing six chains of conditionals.

## What This Costs

Seven classes where there was one enum, and a transition table that no longer
exists anywhere you can read it — it is distributed across the states, one
arrow at a time. Adding a state means editing whichever state hands over to it.
That trade is only worth making when the *behaviour* varies by state and not
merely the permissions. Here it does.

The [pattern write-up](state-pattern-explained.md) shows the design, and the
[class diagram](class-diagram.md) shows the shape it ends up as.
