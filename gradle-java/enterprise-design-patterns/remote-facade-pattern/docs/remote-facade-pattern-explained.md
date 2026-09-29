# Remote Facade, Explained

## The pattern in one sentence

A remote facade gives remote callers coarse-grained calls, a whole screen or
a whole change at once, over fine-grained objects that stay unchanged inside.

## The 5 acts

### 1. Many small remote calls

`FineGrainedApi` publishes each of the order's small methods as its own HTTP
address. To draw the order screen the phone app calls all five: customer,
items, total, address, slot. That is five round trips, 400 milliseconds at 80
each on a mobile network.

### 2. One facade call

`OrderFacade.summary` reads all six facts from the order in-process and packs
them into one reply. The app calls `/order-summary` once: one round trip, 80
milliseconds, and the whole screen can be drawn.

### 3. A change in one call

Changing delivery with small calls: the address call succeeds, then the slot
call fails because "Sun 9-12" is not a slot. The order is left with the new
address and the old slot. The facade call `/order-change-delivery` goes to one
order method that checks the slot first: with a bad slot nothing changes; with
a good one, both change.

### 4. Fine-grained inside

Inside the server, the order keeps its small methods. The facade made six of
those calls in-process, in well under five milliseconds. The rule about valid
slots stays on `Order`; the facade only packs and unpacks.

### 5. The bill

A widget that shows only the delivery slot downloads 8 bytes with the small
call, and 73 with the summary. And the facade is one more layer: each new
screen may want its own method.

## The verdict

Put a remote facade in front of any fine-grained model that is called over a
network. Shape calls around screens and whole changes, keep rules on the
domain objects, and consider a Backend for Frontend or GraphQL when clients
need very different shapes.

## How to recognise this in code you did not write

- `/summary`, `/details` or `/overview` endpoints returning many fields at once.
- Service methods named for a screen or a whole task.
- Session facades and BFF services.

## Where you have already met this

- "Summary" or "details" endpoints in REST APIs that return a whole screen's data.
- Session facades in older Java EE applications.
- Backend for Frontend services, one coarse API per app.
- GraphQL, which lets the client ask for a whole screen in one request.
