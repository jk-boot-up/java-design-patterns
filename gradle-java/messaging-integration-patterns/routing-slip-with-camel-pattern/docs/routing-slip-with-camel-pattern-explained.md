# Routing Slip with Apache Camel, Explained

## The pattern in one sentence

With Camel, a routing slip is a header listing each order's steps, and
`routingSlip()` sends the order through them in turn.

## The 5 acts

### 1. One fixed pipeline

First, the old way as a Camel route: every order is sent to all six steps in
turn. Four orders make twenty-four visits, and only fifteen of them do any
work. The rest are steps checking whether they apply, and finding they do not.

### 2. The slip

A slip writer looks at each order once, as it sets off, and lists the steps it
needs. ORD-1 needs validate, charge and pack. ORD-2, a gift, adds gift wrap.
ORD-3, age-restricted, adds an age check. ORD-4, going abroad, adds customs.
The list is stored in a header as endpoint addresses.

### 3. Camel follows the slip

`routingSlip(header("slip"))` sends each order to the steps on its slip, in
turn. The four orders now make fifteen visits, every one doing work. ORD-2
went validate, charge, gift wrap, pack. No step knows which step comes after
it.

### 4. A new step

A fraud check is needed for orders over £500. One rule is added to the slip
writer. ORD-4, worth £640, now goes validate, customs, fraud check, charge,
pack. No route and no other step changed.

### 5. The bill, and a dynamic router

ORD-5's customer is too young. The age check fails, and the slip simply
stops, with charge and pack still on it; a slip cannot choose a new route
from what happened on the way. Camel's `dynamicRouter()` can: it decides each
next step as it goes, and sends ORD-5 from the failed age check to a
notify-customer step.

## The verdict

Use a routing slip when messages need different steps, known at the start. When
the next step depends on what has just happened, use `dynamicRouter()` or a
process manager instead.

## How to recognise this in code you did not write

- `.routingSlip(header("..."))`.
- A header holding comma-separated endpoint addresses.
- `.dynamicRouter(method(...))` returning the next endpoint.

## Where you have already met this

- Camel's `routingSlip()` and `dynamicRouter()`.
- Treatment cards in hospitals, and job travellers in factories.
- Workflow engines where a document carries its approval chain.
