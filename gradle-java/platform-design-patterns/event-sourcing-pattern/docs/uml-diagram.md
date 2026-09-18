# Event Sourcing Pattern — UML Sequence Diagrams

Four sequences. The first is the whole pattern in one picture; the other three are
the three things it makes possible that the current-state design cannot do at all.

## 1. A Write, Then A Read

Nothing is stored when the balance is asked for. It is worked out.

![Event Sourcing pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Checkout
    participant Accounts as EventSourcedLoyaltyAccounts
    participant Store as LoyaltyEventStore
    participant Support

    Checkout->>Accounts: award("C-4417", 60, "ORD-8801", 1 Mar)
    Accounts->>Store: append(PointsAwarded)
    Note over Accounts,Store: no balance is updated, because there is no balance

    Support->>Accounts: balanceFor("C-4417")
    Accounts->>Store: eventsFor("C-4417")
    Store-->>Accounts: [awarded 60, redeemed 25, awarded 120, expired 15]
    Note over Accounts: running = 0 + 60 - 25 + 120 - 15
    Accounts-->>Support: 140
```

</details>

The write side has one job: turn a decision into a fact and put the fact at the end
of the log. The read side has one job: walk the facts and add them up. There is no
field anywhere holding 140, and asking a second time does the same walk again.

## 2. Why Is It 140?

The same walk, printing itself.

![Event Sourcing Pattern — Why Is It 140?](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Support
    participant Accounts as EventSourcedLoyaltyAccounts
    participant Store as LoyaltyEventStore
    participant Event as LoyaltyEvent

    Support->>Accounts: explain("C-4417")
    Accounts->>Store: eventsFor("C-4417")
    Store-->>Accounts: four events, oldest first

    loop for each event
        Accounts->>Event: effectOnBalance()
        Event-->>Accounts: +60 / -25 / +120 / -15
        Accounts->>Event: because()
        Event-->>Accounts: "earned 60 points on order ORD-8801"
        Note over Accounts: append one line with the running total
    end

    Accounts-->>Support: 2025-03-01 earned 60 ... balance 60<br/>2025-03-03 spent 25 ... balance 35<br/>2025-03-08 earned 120 ... balance 155<br/>2025-03-14 lost 15 to expiry ... balance 140
```

</details>

Each event explains itself through `because()`, so the accounts class never has to
know how to describe an expiry. Add a fourth kind of event and the explanation comes
with it.

## 3. The Bug Investigation, Weeks Later

The query does not exist while the bug is live. It is written afterwards, against
data that was already lying there.

![Event Sourcing Pattern — The Bug Investigation, Weeks Later](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Checkout
    participant Accounts as EventSourcedLoyaltyAccounts
    participant Store as LoyaltyEventStore
    participant Dev as Developer, three weeks later

    Note over Checkout: the double-awarding release is live
    Checkout->>Accounts: award("C-5120", 45, "ORD-9001", 8 Mar)
    Accounts->>Store: append(PointsAwarded ORD-9001)
    Checkout->>Accounts: award("C-5120", 45, "ORD-9001", 8 Mar)
    Accounts->>Store: append(PointsAwarded ORD-9001)
    Note over Checkout: the fix ships. Two events remain, and both are true.

    Dev->>Accounts: duplicateAwards("C-5120")
    Accounts->>Store: eventsFor("C-5120")
    Accounts-->>Dev: "ORD-9001 awarded 2 times"

    Dev->>Accounts: balanceWithDuplicateAwardsIgnored("C-5120")
    Accounts->>Store: eventsFor("C-5120")
    Note over Accounts: skip an award whose order id was already counted
    Accounts-->>Dev: 55

    Note over Store: nothing was appended, edited or deleted.<br/>store.size() is the same number it was before.
```

</details>

The log was never wrong — the shop really did award twice. The *interpretation* was
wrong, so the repair is a change to the reading code. That is the sentence worth
carrying out of this project.

## 4. The Snapshot, And What It Costs

The fix for a slow fold, and the second place a balance comes to live.

![Event Sourcing Pattern — The Snapshot, And What It Costs](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant Accounts as EventSourcedLoyaltyAccounts
    participant Snaps as SnapshotStore
    participant Store as LoyaltyEventStore

    Note over Store: 5,000 events in the log

    Caller->>Accounts: balanceFor("C-6000") with no snapshot
    Accounts->>Store: eventsFor("C-6000", from 0)
    Store-->>Accounts: 5,000 events examined
    Accounts-->>Caller: 500

    Caller->>Accounts: snapshotFor("C-6000", "fold v1")
    Accounts-->>Caller: C-6000 = 500, as at event 5000, by fold v1
    Caller->>Snaps: save(snapshot)

    Note over Store: one more order arrives

    Caller->>Accounts: balanceFor("C-6000") with the snapshot
    Accounts->>Snaps: forCustomer("C-6000")
    Snaps-->>Accounts: 500, as at event 5000
    Accounts->>Store: eventsFor("C-6000", from 5000)
    Store-->>Accounts: 1 event examined
    Accounts-->>Caller: 502

    Note over Snaps: and if "fold v1" had a bug,<br/>this snapshot is wrong forever and nothing throws
```

</details>

Five thousand reads become one, and the answer is identical. The price is that a
balance is now stored somewhere again, which is the thing the pattern set out to
avoid — so the snapshot records which event it covers and which code computed it,
and the cure when that code was wrong is to throw every snapshot away and refold.
That cure is cheap only because the log kept everything.
