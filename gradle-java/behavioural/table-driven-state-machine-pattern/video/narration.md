# Table-Driven State Machine Pattern — Video Narration Script

## 1. Table-Driven State Machine

Hello, and welcome. This video explains the Table-Driven State Machine pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A state machine is anything that is always in one of a few statuses, and moves between them when something happens. In a table-driven state machine, every allowed move is one row in a table. From this status, on this action, go to that status. Anything not in the table is refused. Think of an airport. Check-in, then security, then the gate, then the plane. There is one chart of allowed steps, and every desk checks it. A step that is not on the chart does not happen. In this video, the domain is an online shop. Its orders move from placed, to paid, to shipped, to delivered. And they can be cancelled, or refunded. By the end, you will hear how scattered if statements hide missing rules. How one table fixes it. How to add a rule with two lines. And what the table does not do for you.

## 2. The Scenario

Here is the scenario. An order is placed. Then paid. Then shipped. Then delivered. Along the way, it might be cancelled, or refunded. Each of those is a status. At any moment, an order has exactly one. The shop had one method per action: pay, ship, cancel, refund. And each method checked the status in its own way.

## 3. Act One — Rules in if statements

First demo: the rules, scattered across if statements. Each method checks the status in its own way. An order is paid, shipped, and delivered. So far, so good. Now someone cancels it. The cancel method only refuses shipped orders. Nobody thought of delivered. So a delivered order is now cancelled. Another order is refunded. Then refunded again. The refund method only checks that it was paid. Two refunds, of sixty-three pounds forty-four, are paid out.

## 4. Act Two — The table

Second demo: the rules, in one table. Each row says: from this status, on this action, go to that status. From placed: pay goes to paid, and cancel goes to cancelled. From paid: ship goes to shipped, and refund goes to refunded. From shipped: deliver goes to delivered. That is all of them. Anything not written here is not allowed. Order one is paid, shipped and delivered, by looking each move up in the table.

## 5. Act Three — Wrong moves refused

Third demo: a move that is not in the table is refused. Try to cancel the delivered order. Refused: cannot cancel a delivered order. Try to refund an order a second time. Refused: cannot refund a refunded order. The table can also answer a useful question. Which buttons should the page show? For a paid order: ship, and refund. Nothing else.

## 6. Act Four — A new rule

Fourth demo: a new rule. The shop starts accepting returns. Two rows are added to the table. From delivered, return goes to returned. From returned, refund goes to refunded. No method changes. A delivered order now shows one button: return. And order one is returned, and refunded.

## 7. Act Five — The bill

Fifth demo: the bill. Seven statuses times six actions is forty-two cells. Only seven of them are allowed moves. As the table grows, it gets hard to read, so draw it as a diagram. And the table only says where an order may go. Paying the refund, and emailing the customer, are still code. You attach them to each move.

## 8. The Pattern

Let's name the pattern. Write every allowed move as one row, in one table. From this status, on this action, go to that status. To change an order's status, look the move up. If it is not in the table, refuse it, and say why. And when the rules change, change the table. A new rule is a new row.

## 9. Who Does What

Here is who does what. Status and Action are two enums, fixed lists of names. The transition table is the whole rule book. It can say what comes next, and which actions are allowed from any status. The order holds its status, and asks the table before every move. And the if else order is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Spring State Machine is configured as a table of transitions. Ticket systems such as Jira let an admin edit the allowed moves between statuses. Almost every shop has order and payment statuses. And parsers and network protocols are built on state tables, too.

## 11. When To Use It

So, when should you use it? Whenever something has a handful of statuses, and rules about which can follow which. Orders, payments, tickets, bookings. Keep the table in one place. Draw it as a diagram. Attach side effects, such as emails, to the moves. And when each status needs a lot of its own behaviour, look at the State pattern instead.

## 12. Thanks for Watching

That's the Table-Driven State Machine pattern. If you remember one sentence, make it this one. Write every allowed move in one table, and refuse everything else. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a lost status, for parcels that never arrive. Which actions lead into it, and out of it? If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
