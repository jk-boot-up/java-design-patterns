# Domain-Driven Design Patterns

The tenth category. The patterns of domain-driven design that a Java developer meets
first: small building blocks for writing code that says what the business says.

**Status: three built.** Each project has code, deterministic tests, a README,
diagrams, an animation, a narrated video pipeline and a YouTube document. Every one
is plain Java with no framework, and each shows the bill as well as the benefit.

1. [Value Object](value-object-pattern) — money and an email address that are equal
   by value, never change, and cannot be built wrong.
2. [Aggregate](aggregate-pattern) — an order and its lines as one unit, with one
   root that enforces every rule, and the cost of drawing the boundary too wide.
3. [Domain Event](domain-event-pattern) — an order that says what happened instead
   of calling everyone, and the gap between saving and telling that leads to the
   transactional outbox.

They are meant to be watched in that order: an aggregate is made of value objects,
and an event is what an aggregate says.

## Still to build

Specification, Anti-Corruption Layer, and Bounded Context with a context map.
