# Request-Reply with RabbitMQ Pattern — Video Narration Script

## 1. Request-Reply with RabbitMQ

Hello, and welcome. This video explains the Request-Reply pattern, with a real RabbitMQ broker, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Request-reply is asking a question with one message, and getting the answer in another. Each request says where to send the answer. And carries a reference, so the answer can be matched to it. RabbitMQ is an open-source message broker, and it has both of these built into every message. Think of letters to a supplier, each with your address and a reference number. The answers come back in any order, but each names your reference. In this video, the domain is an online shop's checkout, asking an inventory service to reserve items. By the end, you will hear how replies get mixed up. How references and return addresses fix it. And what to do about a reply that never comes.

## 2. The Scenario

Here is the scenario. Checkout asks the inventory service to reserve items, and waits for the answer. The inventory service answers items in its cache first. So replies can come back in a different order. And the web checkout and the phone app both ask.

## 3. Act One — Replies taken in arrival order

First demo: replies taken in the order they come back. Checkout asks for five kettles, then two mugs. The inventory service answers the mugs first, from its cache. Checkout takes the first reply as the kettle's answer. So it believes its kettles were reserved. They were refused.

## 4. Act Two — Correlation IDs

Second demo: correlation identifiers. Each request carries a reference. The inventory service copies it onto the reply. The mug reply still comes first. But its reference says which request it answers. The kettles are refused. The mugs are reserved. Each answer matched to its question.

## 5. Act Three — Return addresses

Third demo: return addresses. Each request names where its reply should go. The phone app uses a RabbitMQ feature called direct reply-to. It needs no reply queue at all. The web checkout uses its own private queue. One inventory service. Each reply goes to the address in its request.

## 6. Act Four — Many in flight

Fourth demo: many requests in flight at once. Twenty requests are sent, before a single reply. The service handles all twenty. Every reply is matched by its reference. None is left waiting.

## 7. Act Five — A reply that never comes

Fifth demo: the bill. The inventory service is busy. Request twenty-four waits half a second. No reply. The requester must time it out, and clean up. But was the mug reserved later? The request was sent with an expiry of half a second. So RabbitMQ dropped it. When the service comes back, there is nothing to handle. Without the expiry, nobody could tell.

## 8. The Pattern, in RabbitMQ

Let's name the pattern, in RabbitMQ's words. Reply to, says where to send the answer. Correlation identifier, says which question it answers. And expiration tells the broker to drop a request, if nobody takes it in time.

## 9. Who Does What

Here is who does what. The requester sends each question, and matches each answer by its reference. The inventory service answers, copying the reference. The broker class runs RabbitMQ in a container. And poll waits for real conditions.

## 10. Where You Have Seen It

You have probably met this already. RabbitMQ's remote procedure call examples. And Spring's send and receive methods. Java messaging has reply-to and correlation fields too. And every email reply carries a reference to the message it answers.

## 11. When To Use It

So, when should you use it? When callers and services are decoupled, and replies may be slow. Always set a reference. Time out in the requester. And give each request an expiry that matches that time-out.

## 12. Thanks for Watching

That's Request-Reply, with RabbitMQ. If you remember one sentence, make it this one. Say where to answer, say which question, and say when to give up. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It needs Docker running, and starts the broker for you. Here is one exercise to try. Remove the expiry in the last demo, and watch the mug get reserved late. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
