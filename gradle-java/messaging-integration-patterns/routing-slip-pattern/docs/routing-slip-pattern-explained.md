# Routing Slip, Explained

## The pattern in one sentence

A routing slip is a list of processing steps worked out when a message enters
and carried with it, so each step can pass the message on to the next one on
the list.

## The 5 acts

### 1. One fixed pipeline

`FixedPipeline` sends every order through validate, age check, customs,
charge, gift wrap and pack. Four orders make 24 step visits, but only 15 do
any work: a UK order has no customs, a plain order no gift wrap. Every step
starts with its own "does this apply to me?" check.

### 2. Routing slips

`RoutingSlip.slipFor` writes each order's route once, from what the order is.
A plain UK order gets validate, charge, pack. The gift adds gift-wrap. The
age-restricted order adds age-check. The order to France adds customs.

### 3. Steps pass it on

Each order now visits only the steps on its slip. Each step does its job and
passes the order to the next address on the slip. Fifteen visits in all, and
every one does work. ORD-2 went validate, charge, gift-wrap, pack; no step
knows which comes after it.

### 4. A new step

A fraud check is needed for orders over £500. One rule is added where slips
are written. ORD-4, worth £620, now has fraud-check before charge; ORD-1's
slip is unchanged, and none of the steps was touched.

### 5. The bill

ORD-5, a kitchen knife, fails its age check. The slip can stop there, with
charge and pack still on it, but it cannot choose a different route, such as
"ask for ID, then continue". Deciding routes from what happened on the way is
a job for a process manager.

## The verdict

Use routing slips when messages need different, predictable sequences of
steps. Keep the slip-writing rules in one place, keep steps independent, and
switch to a process manager when routes must change along the way.

## How to recognise this in code you did not write

- A list of step names or addresses carried in a message header.
- `routingSlip(...)` in Camel routes.
- Steps that forward to "the next one on the list".

## Where you have already met this

- Apache Camel's `routingSlip`.
- Approval workflows where a document carries its list of approvers.
- Circulation slips on office post and magazines.
