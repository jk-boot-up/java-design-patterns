# Future/Promise Pattern — UML Sequence Diagrams

Four sequences: three lookups running at once, the Future/Promise
handoff, an exception surfacing wrapped, and the harness's own
lost-update proof, copied unchanged from §46.

## 1. Three Lookups, Submitted At Once, Read In Order

![Future/Promise pattern sequence diagram](images/uml-diagram.png)

## 2. Future And Promise — One Object, Two Threads

![Uml diagram 2](images/uml-diagram-2.png)

## 3. An Exception Surfaces Later, Wrapped

![Uml diagram 3](images/uml-diagram-3.png)

## 4. The Harness's Own Proof — A Lost Update, Every Run

![Uml diagram 4](images/uml-diagram-4.png)

This is the same mechanism §46 built and this project's `HarnessSelfTest`
proves again, copied unchanged, before act two or act three relies on it.
