# Process Manager Pattern — Video Narration Script

## 1. Process Manager

Hello, and welcome. This video explains the Process Manager pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A process manager takes charge of a process with several steps. It keeps track of where each case is, sends it to the next step, and decides what happens after every reply. Including when something goes wrong. Think of a wedding planner. The caterer, the florist, and the venue only talk to the planner. When the florist cannot deliver, the planner calls a backup. When the venue cancels, the planner cancels the caterer too. In this video, the domain is an online shop. Each order must be reserved, paid for, and shipped. By the end, you will hear how a simple chain of steps loses track. How a process manager runs each order. How it handles branches and failures. And what a central brain costs.

## 2. The Scenario

Here is the scenario. Each order is fulfilled in three steps. Reserve the stock. Take payment. Ship. Each service simply passed the order on to the next. But cards get declined, and warehouses run out.

## 3. Act One — Steps chained together

First demo: each step hands on to the next. The warehouse reserves a kettle, and hands on to payments. Payments charges, and hands on to shipping. Order one ships. Order three's card is declined. The chain stops at payments. But the warehouse never hears, so its kettle stays reserved. Only one kettle shipped, yet two are gone from stock. And where is order three now? Nobody knows.

## 4. Act Two — A process manager

Second demo: a process manager runs each order's journey. The services no longer call each other. They only answer the manager. For order one, the manager asks the main warehouse to reserve. Reserved. It asks payments to charge. Paid. It asks shipping to ship. Shipped. Order one is done.

## 5. Act Three — A branch

Third demo: the manager decides the next step. Order two is a sofa. The main warehouse replies: out of stock. The manager decides: try the partner warehouse. Reserved. The order is paid, shipped, and done.

## 6. Act Four — The unhappy path

Fourth demo: the unhappy path is part of the process. Order three's card is declined. The manager knows this order reserved a kettle. So it tells the warehouse to release it. And it emails the customer. The order is cancelled, cleanly. The kettle is back in stock.

## 7. Act Five — The bill

Fifth demo: the bill. The manager can say where every order is, in one line. But every route, and every branch, lives in one class. It grows with each new step. And its state is in memory. A restart would forget every order in progress. Real process managers store their state.

## 8. The Pattern

Let's name the pattern. One component owns the process. It keeps each order's state. It sends the order to the next step. And after every reply, it decides what happens next. The services never call each other. They only answer the process manager.

## 9. Who Does What

Here is who does what. The process manager holds each order's state, and decides every next step. The main warehouse, the partner warehouse, payments, shipping, and emails each do one job, and answer. And chained is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Workflow engines such as Camunda, Temporal, and Step Functions are process managers you configure. Orchestrated sagas in microservices are the same idea. And every order management system that tracks each order's status is one.

## 11. When To Use It

So, when should you use it? When routes branch, and failures must be undone. Store the manager's state, so a restart forgets nothing. And when processes are long, or many, use a workflow engine rather than writing your own.

## 12. Thanks for Watching

That's the Process Manager pattern. If you remember one sentence, make it this one. Let one place own the whole journey, including the unhappy paths. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Save the manager's state to a file, and restart it in the middle of an order. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
