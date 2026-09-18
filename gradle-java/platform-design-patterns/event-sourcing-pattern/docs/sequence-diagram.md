# Event Sourcing Pattern — Sequence Diagram

Four things happening to one customer's loyalty points, and then two questions asked about
them — in the order the calls happen. The architecture diagram puts the two designs side by
side and the data flow diagram shows writes going down and reads coming up; this one shows
**when each side does its work**, and the surprise is that the write side does almost
none.

Follow the writes first. The customer earns sixty points on an order in March, spends
twenty-five on the next one, earns a hundred and twenty on a third, and loses fifteen to
the twelve-month expiry. Each time, the checkout hands a fact to the store and the store
puts it at the end of the log. Nothing is added up. Nothing is overwritten. **There is no
balance to update, because there is no balance.**

Then the reads. Support asks what the balance is, and the accounts object fetches the four
events, oldest first, and adds them: zero plus sixty, minus twenty-five, plus a hundred
and twenty, minus fifteen — a hundred and forty. Ask again and the same walk happens
again. Then support asks the harder question, the one the shop could not answer before:
*why* is it a hundred and forty. The same walk runs, and this time each event is asked to
describe itself, so the answer comes back as four dated lines with a running total beside
each one.

![Event Sourcing pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Checkout
    participant Accounts as EventSourcedLoyaltyAccounts
    participant Store as LoyaltyEventStore
    participant Support

    Checkout->>Accounts: award C-4417, 60 points, ORD-8801, 1 Mar
    Accounts->>Store: append PointsAwarded
    Checkout->>Accounts: redeem 25 points, ORD-8814, 3 Mar
    Accounts->>Store: append PointsRedeemed
    Checkout->>Accounts: award 120 points, ORD-8907, 8 Mar
    Accounts->>Store: append PointsAwarded
    Checkout->>Accounts: expire 15 points, 14 Mar
    Accounts->>Store: append PointsExpired
    Note over Accounts,Store: nothing was added up,<br/>because nothing stores a balance

    Support->>Accounts: balance for C-4417?
    Accounts->>Store: events for C-4417
    Store-->>Accounts: the four events, oldest first
    Note over Accounts: 0 + 60 - 25 + 120 - 15
    Accounts-->>Support: 140 points

    Support->>Accounts: and why is it 140?
    Accounts->>Store: the same four events again
    Note over Accounts: each event describes itself,<br/>with the running total beside it
    Accounts-->>Support: earned 60 on ORD-8801 ... 60<br/>spent 25 on ORD-8814 ... 35<br/>earned 120 on ORD-8907 ... 155<br/>lost 15 to expiry ... 140
```

</details>

## What the order proves

**The write side is one arrow long.** Turn a decision into a fact, put the fact at the end
of the log, stop. Every interesting thing in this pattern happens on the read side, which
is the opposite of the design it replaces — there, the write did the arithmetic and the
read was a single lookup of a number that could not explain itself.

**The same walk answers both questions.** The balance and the explanation are the same
traversal with a different amount of printing, which is why the second question costs
nothing extra to support. A stored balance can answer the first and has no way at all to
answer the second.

**Each event explains itself.** The accounts object never learns how to describe an
expiry; it asks the expiry. Add a fifth kind of event next year and its explanation
arrives with it, rather than being bolted onto a growing switch statement somewhere else.

**Reading is the expensive direction, and that is the bill.** Four events add up
instantly; five thousand do not, and the fix — a snapshot — is a stored balance,
reintroducing the very thing the pattern removed. A snapshot written by buggy code stays
wrong for ever and nothing throws. The log is the truth; a snapshot is only a cache of it.

The investigation weeks after a bug shipped, and what a snapshot costs, are sequences 3
and 4 in [`uml-diagram.md`](uml-diagram.md).
