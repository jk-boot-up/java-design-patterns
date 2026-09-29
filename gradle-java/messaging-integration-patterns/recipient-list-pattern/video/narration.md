# Recipient List Pattern — Video Narration Script

## 1. Recipient List

Hello, and welcome. This video explains the Recipient List pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A recipient list works out, for each message, exactly which destinations need it. Then it sends a copy to each of them, and to no one else. Think of an office post room. A letter about a supplier contract arrives. The routing sheet says: contracts to legal, prices to accounts, and big amounts to the finance director too. One copy each, and nobody else is bothered. In this video, the domain is an online shop. It ships from four warehouses, each handling different kinds of product. By the end, you will hear what sending everything everywhere costs. How a recipient list fixes it. How rules and tables change the list. And what happens when one recipient is down.

## 2. The Scenario

Here is the scenario. The shop has four warehouses. North handles kitchen items. Big-items handles furniture. The cold store handles chilled food. And south is a spare. One order can contain items for several of them. So every order was sent to all four.

## 3. Act One — Everything everywhere

First demo: every order sent to every warehouse. Five orders, four warehouses. Twenty deliveries. Only eight were needed. Every warehouse sorts through orders it has nothing to do with.

## 4. Act Two — A recipient list

Second demo: a recipient list. For each order, the list looks at what is in it, and works out who needs it. Order one has kitchen items and furniture. It goes to north, and big-items. Order three is chilled food. It goes to the cold store. Eight deliveries. Exactly the ones needed.

## 5. Act Three — Rules add recipients

Third demo: rules can add recipients. Orders over five hundred pounds also go to fraud review. Gift orders also go to gift wrap. Order four is worth six hundred and fifty pounds. It goes to big-items, the cold store, and fraud review. Order two is a gift. It goes to north, and gift wrap.

## 6. Act Four — A changed table

Fourth demo: the table changes while the shop runs. North closes for a stocktake. Kitchen items now come from south. Order five goes to south, and the cold store. Checkout was not changed at all.

## 7. Act Five — The bill

Fifth demo: the bill. The big-items warehouse is unreachable. Order one reaches south, but not big-items. Half the order is out. The recipient list must retry, or undo. And it must know every destination, and what each one does.

## 8. The Pattern

Let's name the pattern. For each message, build the list of destinations that need it. The list comes from what the message contains, from a table, and from rules. Then send one copy to each destination on the list. And the sender never needs to know who they are.

## 9. Who Does What

Here is who does what. The recipient list holds a table from category to warehouse, and a list of rules. It works out the list, and sends. An order carries its categories, its value, and whether it is a gift. And the inboxes stand in for the warehouses and services that receive the copies.

## 10. Where You Have Seen It

You have probably met this pattern already. Apache Camel has a recipient list step. Large shops split each order across the fulfilment centres that stock its items. And every email you send has a recipient list, chosen for that message.

## 11. When To Use It

So, when should you use it? When each message needs a different set of destinations. If every message has exactly one destination, use a content-based router. If everyone needs everything, use publish-subscribe. And plan for what happens when a message reaches some recipients, but not all.

## 12. Thanks for Watching

That's the Recipient List pattern. If you remember one sentence, make it this one. Work out who needs each message, and send it to exactly them. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Retry a failed recipient once, then send the order to a problem list. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
