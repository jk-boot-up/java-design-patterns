# Content-Based Router with Camel Pattern — Video Narration Script

## 1. Content-Based Router with Camel

Hello, and welcome. This video explains the Content-Based Router pattern in Java, using a real routing framework, Apache Camel, over a real message broker, RabbitMQ. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. A content-based router is a sorter that sits between the people who send messages and the people who handle them. It reads what is inside each message, and sends it on to the one place that suits it. The sender does not choose, and the receivers never see the messages that are not theirs. Now the same thing in our online store. Every order lands in one place. A parcel that must go out today goes to express shipping. A gift card, with nothing to put in a box, goes to digital delivery. An order worth a thousand pounds or more goes to a fraud check first. By the end you will have seen six orders sorted by what they contain, seen the order of the questions change the answer, and seen what Camel does with an order that no question claims. It keeps no count. It simply lets the order go.

## 2. The Scenario

Here is the scenario. Six orders arrive in one place. Some are parcels that must be posted today. Some are parcels that can wait. Some are gift cards, with nothing to put in a box. One is so valuable that a person should check it before anything ships. And one is a subscription, which is none of those. The question is who decides where each order goes, and where that decision lives.

## 3. One Queue For Everything

First, with no router at all. All six orders are put in the warehouse's own line of waiting work. The warehouse can pack and post the three physical ones. It can do nothing with the other three: two gift cards and a subscription. So the warehouse grows an if for every kind of order, and every new kind of order means changing the warehouse. The deciding is in the wrong place.

## 4. The Words, In Plain Language

Two tools bring their own words, so here they are in plain language first. The broker is a separate program that holds messages. A named line of messages, waiting until somebody takes them, is called a queue. The post box a sender drops a message into is called an exchange. It keeps nothing. It reads the short label on the message, which is called the routing key, and puts the message in the matching line. Camel has its own words. A written description of where messages come from, what is asked about them, and where they go, is called a route. A yes-or-no question asked about one message is called a predicate. And the branch taken when every question says no is called otherwise. Hold on to that last one.

## 5. The Route Reads And Chooses

Second, a Camel route reads the orders line and asks four questions, in order. Is the order worth a thousand pounds or more? Is it digital? Was express delivery paid for? Is it a physical thing? The first question answered yes decides. Order one, a parcel paid for express, goes to express shipping. Orders two and four, both digital, go to digital delivery. Order three is a parcel worth twelve hundred pounds, so the value question claims it first, and it goes to fraud review. Order six, an ordinary parcel, goes to standard shipping. And order five, the subscription, is claimed by no question at all. It takes the otherwise branch, to manual review, where a person will see it.

## 6. The Route, As Written

Here is the route, said in words. It starts at the orders line. Then comes one choice with four questions under it, in this order: high value, then digital, then express, then physical. Each question names one line to post to when the answer is yes. Last comes the otherwise branch, naming manual review. That is the whole router. No sender knows it exists, and no receiver does either. Each receiver just reads its own line. The deciding lives in one place, written down, in order.

## 7. The First Yes Wins

Third, the order of the questions. One digital gift card, worth fifteen hundred pounds, goes through two routes that ask the same four questions in two different orders. With the value question asked first, it goes to fraud review. With the value question asked last, the digital question is reached first and says yes, so it goes to digital delivery, and nobody checks it. Same card, same broker, same questions, a different answer. The order of the questions is part of the design, and Camel does not warn you when somebody changes it.

## 8. A Message No Question Claims

Fourth, and this is the heart of the video. A subscription order. Every one of the four questions says no. Through the route with an otherwise branch, it arrives in manual review. Now take the otherwise branch away. The route simply ends. It tells the broker the order was handled, and the broker deletes it. The demo then counts every message on all ten lines in the shop, and the count is zero. Nothing was logged. Nothing was counted. Nobody was told. Give the otherwise branch a line named for the problem, called unclaimed, and the order lands there. That one line is the whole difference between an order that is lost and an order somebody knows about.

## 9. The One Line That Keeps It

In the route itself, the difference is one line. The four questions each say, when this is true, post it to that line. The last line says, otherwise, post it to the unclaimed line. Leave that line out, and Camel will not complain. The route installs, it starts, it runs, and every order that no question claims disappears without a sound. So always write the otherwise branch, and send it somewhere named for the problem.

## 10. A New Question

Fifth, a new question. Orders from inside the European Union need their tax worked out before they ship, so a fifth question is added, asked after the other four. The route goes from four questions to five. No sender was changed, and no receiving line was changed. Only the route was. A subscription from the European Union used to fall through to manual review. It now goes to the tax check. But order six, a parcel from the European Union, still goes to standard shipping, because the physical question is asked earlier and says yes first.

## 11. The Bill

Last, the bill. Three costs. First, the route is tied to the wording inside the message. The sender starts calling parcels goods instead of physical. The physical question no longer matches, so order nine lands in manual review, and nobody is told why. Second, a branch can fail, which is not the same as not matching. The fraud check is broken, because the service behind it is not answering. Camel tried it three times, the first attempt and two retries, and then put the order on an errors line, which ended up holding one order. Somebody had to say where failures go. Third, there is something to run: one container, one exchange and ten queues.

## 12. What The Simulation Left Out

The hand-built partner project got the idea right. Questions asked in order. The first yes wins. A fallback for anything unclaimed. A new question added without touching anybody else. Every one of those lessons is true of Camel. It left out three things. When it had no fallback, it dropped the order and counted it, so the loss was a number you could see. Camel counts nothing, and the order is simply gone. Its questions could only say yes or no, and could never fail. And the order never left the program. Here it really travels, through a broker, from one program to another.

## 13. How To Recognise It

How do you recognise this in code you did not write? A choice step with a list of when questions and an otherwise at the end. Worse, a choice with no otherwise at all, which is a place orders can vanish. A line of waiting messages with a name like manual review, parking lot or unroutable, which is somebody's otherwise branch. And an if chain inside a message handler, deciding which service to call next, which is the same router with no name.

## 14. The Verdict

Here is my verdict, plainly. Use a content-based router when one stream of messages carries several kinds of work, and the difference is inside the message. Put the questions in order on purpose, and write a test for that order, because nothing warns you when it changes. Always write the otherwise branch, and send it somewhere named for the problem. And always say where a failing message goes, because a branch that fails is not a branch that did not match.

## 15. What Is Real, And When Not

What is real here? A RabbitMQ broker, version four point three point six, running in a container that the demo starts and removes by itself. Apache Camel, version four point twenty. You need a container runtime such as Docker running, and if it is not, the demo tells you so in two plain sentences. Every number in this video comes from the program's own output, and two runs one after the other print the same thing. And when is this too much? If the routing is two or three stable rules inside one program, the hand-built version is smaller and clearer, and needs no broker at all.

## 16. Thanks for Watching

That's Content-Based Router with Camel. If you take one sentence away, take this one: a message that no question claims is kept only if the route says where to keep it. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, take the error handler out of the broken fraud check, run it again, and find out where the order went. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
