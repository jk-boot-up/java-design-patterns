# Problem Statement

## The feature

The same feature every project in this category builds: a customer places
an order for three products, stock is checked, payment is taken, a
confirmation is sent. Ada Okafor, `cust-8801`, buys one espresso machine,
one grinder and two bags of beans — **£382.50**.

## The naive version

The previous project in this category, Layered Architecture, already built
this feature in four layers, and it was good — presentation calls
application, application calls infrastructure, and a test enforces it.
This project's naive version reproduces its one honest admission: the
application layer's use case names its storage, payment and notification
classes **by importing them directly**, because the interfaces that
describe them are defined down in the bottom layer, not up where the use
case lives.

Reproduced here as `NaivePlaceOrderService`, whose constructor takes
`InMemoryOrderStore`, `InMemoryProductCatalog` and `InMemoryPaymentGateway`
— all three concrete adapter classes, not interfaces the core itself
declared. It works. Every acceptance check passes. And to write a unit test
against it, all three adapters must be constructed first, because nothing
here is narrow enough to fake. Swap the storage strategy, and this class
must be edited — not because its logic changed, but because its constructor
named a type that no longer exists.

## What it costs

Two things, and they are the two halves of the same complaint.

**The core cannot be tested in isolation from what it depends on.** Every
test of the checkout logic must construct real (if in-memory) adapters,
because the use case's own field types are adapter types.

**The core cannot be driven from anywhere new without touching adapters
that have nothing to do with the new caller.** A CLI wanting to call this
use case has no seam to call through except the same constructor that
demands three concrete adapters.

## What the pattern must deliver

A **core** — the domain plus the one use case — that defines its own
**ports**: interfaces, named in the core's own language, for whatever it
needs from the outside world. **Adapters**, on the outside, that implement
those ports (the driven side) or call into the core through them (the
driving side). The core imports nothing from any adapter, in either
direction, and that rule is enforced as a test that fails, naming the class,
the moment it is broken.

The pattern is judged by one forced change, performed twice at once: swap
the storage adapter for a structurally different one, **and** drive the
same core from a simulated command line instead of a simulated HTTP
request — with zero lines changed in the core either time. Hexagonal
architecture is usually taught as being about databases; this project
insists on showing the driving side too, because it is the half most
treatments skip.
