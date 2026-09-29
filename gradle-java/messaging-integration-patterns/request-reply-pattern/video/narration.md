# Request-Reply with Correlation Identifier Pattern — Video Narration Script

## 1. Request-Reply with Correlation Identifier

Hello, and welcome. This video explains Request-Reply with a Correlation Identifier, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When services talk through queues, each request gets a unique ID, and says where the reply should go. Each reply names the ID of the request it answers. So replies can come back in any order, and still be matched. Think of a theatre cloakroom. You hand in your coat, and get a numbered ticket. Coats come back in any order. You take the one whose number matches your ticket. In this video, the domain is an online shop. Checkout reserves stock by sending requests over a queue to an inventory service, which works on several at once. By the end, you will hear how matching replies by order goes wrong. How IDs and return addresses fix it. How many requests can be in flight. And what a lost reply costs.

## 2. The Scenario

Here is the scenario. Checkout asks the inventory service to reserve stock. It sends each request over a queue. The inventory service works on several at once. Kettles are checked in a slow warehouse system. Mugs, in a fast one. So the replies come back in whatever order they finish.

## 3. Act One — Replies matched by order

First demo: two requests, with replies assumed to come back in the same order. Checkout asks to reserve five kettles. Then two mugs. The mug check is fast, so its reply comes back first. Checkout takes it as the kettle's answer: reserved. Then the kettle's real answer arrives: refused, because only four exist. Checkout takes that as the mug's answer. Both are wrong.

## 4. Act Two — Correlation IDs

Second demo: correlation IDs. Each request now carries a unique ID. The kettle request is web one. The mug request is web two. The inventory service copies that ID into its reply. The mug reply still arrives first. But it says: I answer web two. So the kettle is refused, and the mugs are reserved. Both correct.

## 5. Act Three — Return addresses

Third demo: return addresses. The phone app uses the same inventory service as the web checkout. Each request says where its reply should go. The app's own queue, or the web's own queue. The app's teapot reservation comes back to the app. The web's comes back to the web.

## 6. Act Four — Many in flight

Fourth demo: many requests in flight at once. Checkout sends twenty requests, before a single reply has come back. The replies arrive in whatever order the inventory service finishes them. All twenty are answered, and matched. None is left waiting.

## 7. Act Five — The bill

Fifth demo: the bill. A reply is lost on the way back. Checkout waits half a second, and gives up. But the request is still in its waiting table. Someone must time it out, and clean up. And was the mug reserved, or not? Checkout cannot tell.

## 8. The Pattern

Let's name the pattern. Give each request a unique ID, and a return address: the queue its reply should go to. Each reply carries the ID of the request it answers. That is the correlation identifier. The requester keeps a table of questions waiting for answers, and matches each reply by its ID.

## 9. Who Does What

Here is who does what. The requester gives out IDs, owns a reply queue, and keeps the waiting table. The inventory service reads the requests, and sends each reply to the queue the request named. A message carries its ID, the ID it answers, its return address, and a body. And the in-order requester is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. J M S messages have a correlation ID and a reply-to header. RabbitMQ has the same two properties. And every email that quotes your order number is a reply with a correlation identifier.

## 11. When To Use It

So, when should you use it? Whenever services talk through queues, and one needs an answer from another. Always set an ID, a return address, and a timeout. Clean up the waiting table. And design for the case where a reply is lost, and you do not know what happened.

## 12. Thanks for Watching

That's Request-Reply with a Correlation Identifier. If you remember one sentence, make it this one. Number every question, and make every answer quote the number. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Remove timed-out requests from the waiting table automatically. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
