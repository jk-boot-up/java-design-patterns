# Problem Statement

## The feature

The same feature every project in this category builds: a customer places
an order for three products, stock is checked, payment is taken, a
confirmation is sent. Ada Okafor, `cust-8801`, buys one espresso machine,
one grinder and two bags of beans — **£382.50**.

This project does not re-teach that feature, or the architecture it is
built with. [`clean-architecture-pattern`](../clean-architecture-pattern)
already did both, completely, and this project's `entities`, `usecases` and
`adapters` packages are that project's files, copied unchanged. See
[`../clean-architecture-pattern/docs/problem-statement.md`](../clean-architecture-pattern/docs/problem-statement.md)
for the architecture's own problem statement.

## What this project is actually about

`PlaceAnOrderDemo`, in the hand-wired project, assembles its object graph
in one method: about twenty lines of `new SomeClass(...)`, reaching into
the outermost circle for concrete gateways and handing them to an
interactor that only ever asks for an interface. That method is readable in
one sitting, and it is also, honestly, the version almost nobody writes at
a real job — most teams reach for a container the moment there is more than
one object to wire.

**The question this project answers: what actually changes when a
container does that wiring instead?** Not "is Clean Architecture correct"
— that was settled already. Specifically: does the graph stay the same
shape? Does the forced change still cost nothing extra? And when a
collaborator is missing from the graph — the same mistake, expressed two
ways — where and when does each version's failure actually happen?

## What it must deliver

`AppConfig`, a `@Configuration` class with one `@Bean` method per object
the hand-wired composition root constructed — read the two side by side and
recognise the correspondence. And `BrokenAppConfig`, identical but missing
one `@Bean` method, proving the contrast this project exists for: hand-
wiring fails at compile time; container wiring fails at startup. Both are
real, both are demonstrated running, and neither is asserted in prose
alone.
