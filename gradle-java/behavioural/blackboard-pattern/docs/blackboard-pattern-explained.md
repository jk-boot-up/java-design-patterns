# Blackboard, Explained

## The pattern in one sentence

A blackboard lets independent experts read and add to one shared set of facts,
while a controller chooses which ready expert goes next and stops when the
answer is known.

## The 5 acts

### 1. Every check, every time

`FraudCheckAll` runs every check, in an order written by hand: both country
lookups must come before comparing them. For the risky order, the answer is
clear after the five cheap checks, but the 800 millisecond device check runs
anyway, for 902 milliseconds in total. Adding a check means editing this
method and finding the right place for it.

### 2. The blackboard

Each check is now a knowledge source that only says what it needs and what it
adds. The good order goes on the board. The controller lets the cheapest ready
check go first: order value, then card country and IP country. Once both
countries are on the board, the country comparison becomes ready. Velocity and
the device check follow. Six checks, risk zero: approved.

### 3. Stopping early

The risky order uses a British card from a Russian address, and the account
placed five orders in the last hour. The country match adds 40 risk and the
velocity check adds 30. At 70, above the rejection line of 60, the controller
stops. Five checks, 102 milliseconds; the 800 millisecond device check never
runs.

### 4. A new expert

Fraudsters start buying gift cards. A new knowledge source is written: over
£200 of gift cards adds 60 risk. It is added to the list; no other check, and
not the controller, changes. An order for six gift cards worth £300 is now
rejected. Without the new expert, it would have been approved.

### 5. The bill

Nobody wrote down the order of events: it depends on which facts arrived and
what each check costs, so the log is the only story of a decision. And the
board is shared: every check can read every fact on it, including the card
number, which is exactly what a privacy review will ask about.

## The verdict

Use it when many independent pieces of knowledge combine into one decision,
their order depends on what is known, and new pieces arrive often: fraud,
diagnosis, recommendations. Keep each expert small, log every contribution,
and decide carefully what the board may expose.

## How to recognise this in code you did not write

- A shared context or facts map that many small classes read and write.
- Classes with a `canHandle` or `ready` method and an `apply` or `contribute` method.
- A loop that picks the next rule or agent until a score or a goal is reached.
- Rule engines and risk scoring services.

## Where you have already met this

- Fraud and risk engines that combine many independent signals into one score.
- Speech recognition and early AI systems such as Hearsay-II, where the pattern was born.
- Rule engines such as Drools, whose rules fire when the facts they need are present.
- Multi-agent AI setups where agents post findings to a shared memory.
