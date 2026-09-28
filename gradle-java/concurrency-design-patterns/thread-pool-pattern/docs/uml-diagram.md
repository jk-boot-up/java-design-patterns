# Thread Pool Pattern — UML Sequence Diagrams

Four sequences: the pool's queue at capacity, the pool-starvation
deadlock, the unbounded-queue trap, and the harness's own lost-update
proof, copied unchanged from §46.

## 1. The Pool's Queue Reaches Capacity, And Says No

![Thread Pool pattern sequence diagram](images/uml-diagram.png)

## 2. Pool Starvation — A Task Waiting On A Task In Its Own Pool

![Uml diagram 2](images/uml-diagram-2.png)

## 3. The Unbounded-Queue Trap — A Backlog With No Ceiling

![Uml diagram 3](images/uml-diagram-3.png)

## 4. The Harness's Own Proof — A Lost Update, Every Run

![Uml diagram 4](images/uml-diagram-4.png)

This is the same mechanism §46 built and this project's `HarnessSelfTest`
proves again, copied unchanged, before act two or act three relies on it.
