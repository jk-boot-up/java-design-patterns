# Clean Architecture with Spring — UML Sequence Diagrams

Two sequences: the container succeeding, and the container failing on the
identical mistake that would not compile in the hand-wired project.

## 1. The Container Wires The Whole Graph

![Clean Architecture with Spring sequence diagram](images/uml-diagram.png)

## 2. The Container Fails — At Startup, Not At Compile Time

![The container failing at startup](images/uml-diagram-2.png)

Compare sequence two with deleting the equivalent argument from
`clean-architecture-pattern`'s hand-wired `new PlaceOrderInteractor(...)`
call: that failure happens in your editor, at the moment you try to save
the file, and never reaches a running process at all.
