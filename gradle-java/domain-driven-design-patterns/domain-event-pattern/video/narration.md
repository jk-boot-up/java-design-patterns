# Domain Event Pattern — Video Narration Script

## 1. Domain Event

Hello, and welcome. This video explains the Domain Event pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A domain event is a record of something that has already happened in the business. It is named in the past tense, and it never changes. Other parts of the system can react to it, without the thing that raised it knowing who they are. Think of a birth announcement in a newspaper. It states a fact that has already happened. Whoever reads it decides what to do: send a card, visit, or nothing. In our online store, the thing that happens is an order being placed. In this video, an order that calls three services falls into a half-done state. Then the same order simply says what happened. We will hear a failing reaction retried safely, and the gap between saving and telling, which is the cost.

## 2. The Scenario

Here is the scenario. When an order is placed in our online store, three things must follow. Stock is reserved. A confirmation email is sent. And the sale is counted for the sales report. So here is the question. Who calls whom? Should the order code know about all three?

## 3. The Order Calls Everyone

First, the naive way: the order calls everyone. It saves the order, reserves the stock, and then sends the email. But the mail server is down. The caller is told that placing the order failed. Yet the order is saved, and the stock is reserved. And the sales report never counted it, because that step came after the failure. A half-done state. And the order code knows three other systems.

## 4. The Pattern

Now, the pattern. The order records what happened: order placed, in the past tense. It calls nobody. Whoever cares reacts, later, and separately. And an event is a fact. Once recorded, it never changes.

## 5. The Order Says What Happened

Second demo: the order says what happened. Placing order two records one event: order placed. It holds the order I D, the customer, Ada, and the total, forty-nine pounds ninety-nine. The order called nobody. Ask for its events again, and there are none. Because they have already been handed over.

## 6. Delivered After The Save

Third demo: delivered after the save. Saving the order also keeps its event. At this point, nothing has reacted yet. Then a relay delivers the event. Stock is reserved. The email is sent. And the sales report counts it. Nothing is waiting any more.

## 7. A Failing Reaction

Fourth demo: a failing reaction. The mail server is down. The email reaction fails. The other two reactions still run. The order is safe. And one event is still waiting, for the email alone. When the mail server is back, the next relay sends just that email. The email goes out once, and the stock is not reserved twice.

## 8. Events Are Facts

Fifth demo: events are facts. Place an order, and then cancel it. Two events are recorded, in that order: order placed, then order cancelled. Each event is a simple record. It carries data, not the order itself. So a handler that receives one cannot reach back and change the order.

## 9. The Gap Between Saving And Telling

Finally, the cost: the gap between saving and telling. Saving the order, and telling everyone about it, are two separate steps. And the program can stop between them. Here it does. Nothing has reacted yet. But the event was saved together with the order. After a restart, the relay delivers it, and nothing is lost. If the event had been sent straight after the save, and not kept, all three reactions would have been lost. Keeping events with the data like this is called the transactional outbox, and it has its own video.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a method that records an event, instead of calling a service. Look for event names in the past tense, like order placed, or payment received. Look for a list of events on an entity, collected when it is saved. And in Spring, look for the application event publisher, and the at Domain Events annotation.

## 11. The Verdict

So, here is the verdict. Raise a domain event when something happens that other parts of the business care about. Name it in the past tense, and keep it small. Save the events together with the data. Deliver them separately. Expect a delivery to be repeated, so make every handler safe to run twice. And do not use an event where the caller needs an answer straight away.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. The mail server is a simple switch, which makes the email fail. And the relay is run by hand, so events happen in the same order on every run.

## 13. When This Is Too Much

So, when is this too much? When there is only one reaction, and the caller needs its answer, a plain method call is clearer. An event is for reactions that may come and go, and may happen later.

## 14. Thanks for Watching

That's the Domain Event pattern. If you remember one sentence, make it this one. An event lets something say what happened, and leaves who cares to someone else, as long as saving and telling are kept together. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add an order shipped event. And a handler that reacts to it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
