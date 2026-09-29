# Recipient List with Apache Camel Pattern — Video Narration Script

## 1. Recipient List with Apache Camel

Hello, and welcome. This video explains the Recipient List pattern, built with Apache Camel, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A recipient list works out, for each message, who should get it. Then sends a copy to each of them, and to nobody else. Apache Camel is an open-source library for moving messages, and it has this step built in. Think of an office clerk who writes on each letter the names of the people it concerns. The post room makes one copy per name. In this video, the domain is an online shop, sending orders to its warehouses. By the end, you will hear how Camel sends each order only where it is needed. How rules add recipients. And what happens when one recipient fails.

## 2. The Scenario

Here is the scenario. The shop sent every order to every warehouse. Five orders, four warehouses. Twenty deliveries. Most of them for items that warehouse did not even stock.

## 3. Act One — Every order to every warehouse

First demo: every order to every warehouse. Camel's multicast sends a copy of each order to all four warehouses. Five orders, four warehouses. Twenty deliveries. Most of them for items that warehouse does not even stock.

## 4. Act Two — A recipient list

Second demo: a recipient list. For each order, Camel asks the routing table who should get it. O R D one holds kitchen items and furniture. It goes to the north warehouse, and the big-items warehouse. O R D three holds chilled food. It goes to the cold store only. Ten deliveries in all, instead of twenty.

## 5. Act Three — Rules add recipients

Third demo: rules add recipients. O R D four is worth six hundred and fifty pounds. Over five hundred. So fraud review gets a copy too. O R D two is a gift. So gift wrap gets a copy. Camel did not change. The table just returned more names.

## 6. Act Four — The table changes while running

Fourth demo: the table changes while the shop runs. The north warehouse closes for stocktake. Kitchen items now come from south. O R D five now reaches south, and the cold store. No route was changed. Nothing was restarted.

## 7. Act Five — One recipient fails

Fifth demo: the bill. The big-items warehouse cannot be reached. O R D one is sent. The south warehouse gets its copy. Big items fails. Camel reports the failure. But half the order is already out. Retrying, or undoing the half that went out, is still the shop's job.

## 8. The Pattern, in Camel

Let's name the pattern, in Camel's words. The recipient list step asks a routing table, for each message. The table returns a list of addresses. And Camel sends one copy to each address.

## 9. Who Does What

Here is who does what. Shop routes holds the routes. The routing table decides who gets each order. That part is plain Java, because it is the shop's business. The warehouses are the destinations. And the order is the message.

## 10. Where You Have Seen It

You have probably met this already. Camel's recipient list, and Spring Integration's recipient list router. The To and Cc lines of an email, chosen for each message. And order systems that split each order across warehouses.

## 11. When To Use It

So, when should you use it? When who needs a message depends on what is in it. Keep the routing table in plain code. And decide in advance what happens when one recipient fails.

## 12. Thanks for Watching

That's the Recipient List, with Apache Camel. If you remember one sentence, make it this one. Work out who needs each message, and send it only to them. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Send failed copies to a retry route, instead of failing the whole order. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
