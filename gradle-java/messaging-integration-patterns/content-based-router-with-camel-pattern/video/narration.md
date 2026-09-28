# Content-Based Router with Camel Pattern — Video Narration Script

## 1. Content-Based Router with Camel

Hello, and welcome. This video explains the Content-Based Router pattern, in Java, using Apache Camel, with a real message broker called RabbitMQ. This video is presented by Jayasekhar Konduru. First, a simple definition. A content-based router is a sorter, sitting between the people who send messages and the people who handle them. It reads what is inside each message, and sends it to the one place that suits it. The sender does not choose. And the receivers never see messages that are not theirs. Now, our online store. Every order lands in one place. A parcel that must go out today goes to express shipping. A gift card, with nothing to box, goes to digital delivery. And an order worth a thousand pounds or more goes to a fraud check first. By the end, you will hear six orders sorted by what they contain. You will hear the order of the questions change the answer. And you will hear what Camel does with an order that no question claims. It keeps no count. It simply lets the order go.

## 2. The Scenario

Here is the scenario. Six orders arrive in one place. Some are parcels that must be posted today. Some are parcels that can wait. Some are gift cards, with nothing to put in a box. One is so valuable that a person should check it before anything ships. And one is a subscription, which is none of those. So here is the question. Who decides where each order goes, and where does that decision live?

## 3. One Queue For Everything

First, with no router at all. All six orders go into the warehouse's own queue of work. The warehouse can pack and post the three physical orders. But it can do nothing with the other three: two gift cards, and a subscription. So the warehouse grows an if statement for every kind of order. And every new kind of order means changing the warehouse. The deciding is in the wrong place.

## 4. The Words, In Plain Language

The two tools bring their own words, so here they are in plain language. The broker is a separate program that holds messages. A named line of messages, waiting to be taken, is called a queue. The post box a sender drops a message into is called an exchange. It keeps nothing. It reads a short label on the message, called the routing key, and puts the message in the matching queue. Camel has its own words too. A written description of where messages come from, what is asked about them, and where they go, is called a route. A yes-or-no question about one message is called a predicate. And the branch taken when every question says no is called otherwise. Remember that last one.

## 5. The Route Reads And Chooses

Second demo: the route reads, and chooses. A Camel route reads the orders queue, and asks four questions, in order. Is the order worth a thousand pounds or more? Is it digital? Was express delivery paid for? Is it a physical thing? The first question answered yes decides. Order one, a parcel with express delivery, goes to express shipping. Orders two and four, both digital, go to digital delivery. Order three is a parcel worth twelve hundred pounds. So the value question claims it first, and it goes to fraud review. Order six, an ordinary parcel, goes to standard shipping. And order five, the subscription, is claimed by no question. It takes the otherwise branch, to manual review, where a person will see it.

## 6. The Route, As Written

Here is the route, described in words. It starts at the orders queue. Then comes one choice, with four questions, in this order. High value, then digital, then express, then physical. Each question names one queue to send to, when the answer is yes. Last comes the otherwise branch, naming manual review. That is the whole router. No sender knows it exists. And no receiver does either. Each receiver just reads its own queue. The deciding lives in one place, written down, in order.

## 7. The First Yes Wins

Third demo: the first yes wins. One digital gift card, worth fifteen hundred pounds, goes through two routes. Both ask the same four questions, but in different orders. With the value question asked first, it goes to fraud review. With the value question asked last, the digital question is reached first, and says yes. So it goes to digital delivery, and nobody checks it. The same card, the same broker, the same questions, and a different answer. The order of the questions is part of the design. And Camel does not warn you when someone changes it.

## 8. A Message No Question Claims

Fourth demo, and the heart of this video: a message no question claims. A subscription order arrives. Every one of the four questions says no. Through the route with an otherwise branch, it arrives in manual review. Now take the otherwise branch away. The route simply ends. It tells the broker the order was handled, and the broker deletes it. The demo counts every message, on all ten queues in the shop. The count is zero. Nothing was logged. Nothing was counted. Nobody was told. Now give the otherwise branch a queue named after the problem: unclaimed. And the order lands there. That one line is the whole difference between an order that is lost, and an order somebody knows about.

## 9. The One Line That Keeps It

In the route itself, the difference is one line. The four questions each say: when this is true, send it to that queue. The last line says: otherwise, send it to the unclaimed queue. Leave that line out, and Camel will not complain. The route installs, starts, and runs. And every order that no question claims disappears, without a sound. So always write the otherwise branch. And send it somewhere named for the problem.

## 10. A New Question

Fifth demo: a new question. Orders from the European Union need their tax worked out before they ship. So a fifth question is added, after the other four. The route goes from four questions to five. No sender was changed. No receiving queue was changed. Only the route. A European subscription used to fall through to manual review. Now it goes to the tax check. But order six, a European parcel, still goes to standard shipping. Because the physical question is asked earlier, and says yes first.

## 11. The Bill

Finally, the costs, and there are three. First, the route depends on the wording inside the message. The sender starts calling parcels goods, instead of physical. The physical question no longer matches. So order nine lands in manual review, and nobody is told why. Second, a branch can fail, which is not the same as not matching. The fraud check is broken, because the service behind it is not answering. Camel tries three times, and then puts the order on an errors queue. Someone had to decide where failures go. Third, there is more to run. One container, one exchange, and ten queues.

## 12. What The Simulation Left Out

The hand-built partner project got the main ideas right. Questions asked in order. The first yes wins. A fallback for anything unclaimed. And new questions, added without touching anyone else. All of that is true of Camel too. But it left out three things. With no fallback, it dropped the order, but counted it. So the loss was a number you could see. Camel counts nothing, and the order is simply gone. Its questions could only say yes or no, and could never fail. And its orders never left the program. Here, they really travel through a broker, from one program to another.

## 13. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a choice step, with a list of when questions, and an otherwise at the end. Worse, a choice with no otherwise at all, which is a place orders can vanish. Look for a queue named manual review, parking lot, or unroutable. That is somebody's otherwise branch. And look for a chain of if statements inside a message handler, deciding which service to call next. That is the same router, without a name.

## 14. The Verdict

So, here is the verdict. Use a content-based router when one stream of messages carries several kinds of work, and the difference is inside the message. Put the questions in order on purpose. And write a test for that order, because nothing warns you when it changes. Always write the otherwise branch, and send it somewhere named for the problem. And always say where a failing message goes. Because a branch that fails is not the same as a branch that did not match.

## 15. What Is Real, And When Not

A quick, honest note about this demo. The RabbitMQ broker is real, version four point three point six. It runs in a container that the demo starts and removes by itself. Apache Camel is real too, version four point twenty. You need Docker running. If it is not, the demo says so, in two plain sentences. Every number you heard comes from the program's own output. And two runs, one after the other, print the same results. So, when is this too much? If the routing is two or three stable rules inside one program, the hand-built version is smaller, and clearer. And it needs no broker at all.

## 16. Thanks for Watching

That's the Content-Based Router, with Camel. If you remember one sentence, make it this one. A message that no question claims is only kept if the route says where to keep it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Remove the error handler from the broken fraud check, and run it again. Then find out where the order went. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
