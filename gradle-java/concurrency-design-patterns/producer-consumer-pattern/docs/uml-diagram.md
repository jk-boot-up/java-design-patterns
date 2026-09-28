# Producer–Consumer Pattern — UML Sequence Diagrams

Four sequences: the queue at capacity, a clean shutdown, an abrupt one, and
the lost-update race the shared harness is proven against.

## 1. The Queue Reaches Capacity, And Says No

![Producer-Consumer pattern sequence diagram](images/uml-diagram.png)

## 2. Clean Shutdown — The Pill Travels Through The Queue

![Uml diagram 2](images/uml-diagram-2.png)

## 3. Abrupt Shutdown — Whatever Is Queued Is Lost

![Uml diagram 3](images/uml-diagram-3.png)

## 4. The Harness's Own Proof — A Lost Update, Every Run

![Uml diagram 4](images/uml-diagram-4.png)

This is the mechanism reused, with different shared state, in
Read–Write Lock and Monitor Object later in this category.
