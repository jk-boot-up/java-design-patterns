# Domain Event Pattern — Video Narration Script

## 1. Domain Event

Hello, and welcome. This video explains the Domain Event pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a domain event is a record of something that has already happened in the business, named in the past tense, that never changes, so that other parts of the system can react to it without the thing that raised it knowing who they are. This is the third project in the domain-driven design category, whose subject is writing code that says what the business says. In our online store, the thing that happens is an order being placed. By the end you will see an order that calls three services fall into a half-done state, see the same order say what happened instead, watch a failing reaction leave the order alone and be retried, and see the gap between saving and telling, which is the bill.

## 2. The Scenario

Here is the scenario. When an order is placed in the online store, three things follow. Stock is reserved. A confirmation email is sent. And the sales funnel is counted. The question: who calls whom? Should the order code know all three?

## 3. The Order Calls Everyone

First, the order calls everyone. It saves the order, reserves stock, and then sends the email, and the mail server is down. The caller is told that it failed. But the order is saved, and stock is reserved. And analytics never counted it, because that call was after the failure. A half done state, and the order code knows three other systems.

## 4. The Pattern

The pattern. The order records what happened: order placed, in the past tense. It calls nobody. Whoever cares reacts, later, and separately. And an event is a fact. It is never changed after it is recorded.

## 5. The Order Says What Happened

Second, the order says what happened. Placing it records one event: order placed, with the id, the customer and the total. The order called nobody. Ask for the events again, and there are none, because they have been handed over.

## 6. Delivered After The Save

Third, delivered after the save. Saving the order keeps its event. Nothing has reacted yet. Then a relay delivers the event: stock is reserved, the email is sent, and analytics counts it. Nothing is waiting any more.

## 7. A Failing Reaction

Fourth, a failing reaction. The mail server is down. The email reaction fails, and the other two run. The order is safe, and one event is still waiting, for the email alone. When the server is back, the next relay sends just that one. The email went out once, and stock was not reserved twice.

## 8. Events Are Facts

Fifth, events are facts. Place the order and then cancel it, and two events are recorded, in that order. Each is a record. It carries the data, and it does not carry the order. A handler that receives one cannot reach back and change the order.

## 9. The Gap Between Saving And Telling

Last, the bill. Saving the order and telling everyone are two steps, and the process can stop between them. Here it does. Nothing has reacted, but the event was saved with the order. After a restart, the relay delivers it, and nothing is lost. Publishing straight after the save, with nothing kept, would have lost all three. That is the transactional outbox, and it is the next thing to read.

## 10. How To Recognise It

How do you recognise this in code you did not write? A method that records an event instead of calling a service. Event names in the past tense, like order placed, or payment received. A list of events on an entity, collected when it is saved. And in Spring, the application event publisher, and the domain events annotation.

## 11. The Verdict

Here is my verdict, plainly. Raise a domain event when something happens that other parts of the business care about. Name it in the past tense, and keep it small. Save the events with the aggregate. Deliver them separately, expect a delivery to be repeated, and make each handler safe to run twice. And do not use an event where the caller needs the answer straight away.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. The mail server is a switch that makes the email fail. The relay is called by hand, so the order of events is the same every run.

## 13. When This Is Too Much

So when is it too much? When there is one reaction, and the caller needs its answer, a plain call is clearer. An event is for reactions that may come and go, and may happen later.

## 14. Thanks for Watching

That's Domain Event. If you take one sentence away, take this one: an event lets a thing say what happened, and leaves who cares to someone else, if the saving and the telling are kept together. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add an order shipped event and a handler that reacts to it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
