# Backends for Frontends Pattern — Video Narration Script

## 1. Backends for Frontends

Hello, and welcome. This video explains the Backends for Frontends pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Each kind of client gets its own small backend service. It is owned by the team that owns that client. And its only job is to shape the data for that one screen. Think of a restaurant with one kitchen and two rooms. A dining room, where couples stay two hours, and a counter for commuters with twenty minutes. One waiter with one script cannot serve both well. The fix is not a second kitchen. It is a second waiter, with his own script. In our online store, one coffee maker is shown on a phone screen with six things, and a desktop page with fifteen. By the end, you will know why a smaller response does not solve this. The one question that separates this pattern from an A P I gateway. And three ways it costs more than it saves.

## 2. The Scenario

Here is the scenario. An online shop sells a copper coffee maker. On a phone, the product screen shows six things. The title, the price, one photo, a star rating, the number of ratings, and when it will arrive. On a desktop, the same product shows fifteen things. Including a full description, a specification table, five photos, and three written reviews. Underneath sit five services: catalog, pricing, inventory, reviews, and recommendations. Neither screen is wrong. The two teams simply disagree about what a product is. And everything in this video comes from that disagreement.

## 3. The First Design — The Phone Calls Everybody

First demo: the phone calls every service itself. Each service has its own endpoint, so the phone asks all five. Five requests, over the customer's own mobile connection. And they must happen one after another. Five waits before anything appears on screen. On a train, each one is slow. About seventeen hundred bytes arrive, with twenty-nine fields. And only six are shown. But the real pain here is the five calls, not the bytes.

## 4. The Second Design — One Endpoint For Everybody

Second demo: one endpoint for everybody. The shop puts one endpoint in front of the five services, and every client calls it. One round trip instead of five. That is a real win, and the final pattern keeps it. But one endpoint returns one document for every client. So it grows to hold everything any screen ever needed. About seventeen hundred bytes reach the phone. Only about two hundred are shown. Eighty-seven percent is thrown away. That looks like the problem. It is about to turn out not to be.

## 5. And the Obvious Fix Works

Because there is an obvious fix, and it works. Let the client list the fields it wants, in the request. Seventeen hundred bytes becomes about two hundred. No new services, nothing to deploy. So here is the most useful sentence in this video. If this pattern were about payload size, the story would end here. It would just be a query parameter. People stop here, and think they have applied the pattern. Then the next request arrives.

## 6. The Request That Cannot Be Served

The phone team wants one line under the price. Free delivery, arrives Friday. That sentence exists in no service. It joins three facts: whether it is in stock, the delivery rules, and today's date. Then it writes them as a sentence. That is half an hour of work. But it is a new field on a shared endpoint, which five other clients also receive. So it becomes a contract change, with a review, and a place in someone else's queue. The phone team waits five weeks. That is the real problem. Not a technical failure, but an organisational one. And it is the one this pattern removes.

## 7. The Pattern

Here is the pattern, in one sentence. Give each frontend its own backend, owned by the team that owns the screen, whose only job is to shape the data for that screen. Three words matter. Each. There must be more than one. A single box in front of everything is a gateway, not this. Own. The screen's team changes the backend. If another team owns it, you have rebuilt the five-week queue. Shape. Only the shape: which fields, in what order, and how they are written. Not business rules. Breaking that third word is the first cost, later in this video.

## 8. Who Does What

Let's name the pieces. At the centre is one interface, called client backend. It says which client it is for, and returns the product screen for a product. Two classes implement it: the phone's backend, and the desktop's. And both run at the same time, answering the same question differently, on purpose. Neither is a fallback. The phone always talks to one, and the desktop always talks to the other. Underneath both are the five shop services. Both backends can reach all of them. They only differ in what they choose to send. Then there are two lists of fields: the six the phone shows, and the fifteen the desktop shows. Those lists define what counts as waste.

## 9. A Backend That Knows One Screen

Here is the phone's backend, in words. It receives one request. Then it makes four calls inside the data centre: catalog, pricing, inventory, and reviews. It does not call recommendations at all, because the phone screen has nowhere to show them. Only a backend that knows one screen can make that choice. Then it builds six simple fields. The price arrives from pricing as a whole number of pence. The phone is sent ready-made text: forty-seven pounds ninety-nine. So the phone team can change that formatting this afternoon, not in an app update. And the last field is the delivery sentence. Four lines of code, in the phone team's own project. The field they waited five weeks for.

## 10. Two Backends, Two Documents

Here are the two documents, read aloud. The phone gets six fields. The title: Copper Filter Coffee Maker, one litre. The price: forty-seven pounds ninety-nine. One small image. A rating of four point six, from two hundred and eighteen ratings. And a sentence: free delivery, arrives on the eighteenth. The desktop gets fifteen fields. Everything the phone got, plus the description, the specification, five images, and three reviews. Notice the delivery field. The phone gets a whole sentence. The desktop gets just the date, because its page writes its own sentence. Two backends disagreeing about the shape of a product is not a mistake. It is the pattern working.

## 11. The Same Product, Three Ways

Now the three designs, side by side. Calls made from the phone, over the customer's connection: five, then one, then one. Calls made inside the shop: five, then five, then four. So the work did not disappear. Four slow trips over a mobile network moved into the data centre, where each call takes well under a millisecond. The pattern moves cost. It does not delete it. And the bytes are still good. The phone's own document is under two hundred bytes. About eighty-nine percent smaller than the shared one.

## 12. The Bill, Part One — One Rule, Two Answers

That is the pattern, and it works. Now the bill, with three items. Item one. The pricing team changes the discount rule. A higher price may only be advertised as a saving if it was in force long enough first. This product's price went up eleven days ago, which does not qualify. The desktop uses the current rule, and claims no saving. But the phone's backend has its own old copy of the rule. So it advertises twelve pounds off. Same product, same moment, and one screen makes a claim the shop is not allowed to make. Nothing fails. Both sets of tests pass. So here is the rule to remember. A backend for a frontend may hold the shape. Anything the shop would still believe with every screen switched off belongs behind it. Tax, discounts, stock, and what a price means.

## 13. The Bill, Part Two — Where the Shared Jobs Go

Item two: where do the shared jobs go? Every request needs four things done, whoever sent it. Check the customer's login. Refuse too much traffic. Handle the encryption. And write the access log. Put those inside each backend, and there are eight copies across two backends. Put a gateway in front, and there are four, however many backends you add. So here is the question that settles it. What does this code answer? If it answers: what does this screen need? It belongs in a backend for that frontend. If it answers: is this request allowed in at all? It belongs in a gateway in front of all of them. A gateway is about entry. A backend for a frontend is about shape.

## 14. The Bill, Part Three — How Many Is Too Many

Item three: how many is too many? The shop has six clients. A phone app, a desktop store, a tablet app, a smart television app, an in-store kiosk, and a nightly partner feed. But the tablet shows the phone's six fields in a wider column. So it shares the phone's backend. The kiosk is the desktop page, with the basket hidden. And the partner feed is not a screen at all. Only three of the six really disagree about what a product is. Every extra backend costs something every week. A build pipeline, an on-call rota, upgrades, and one more thing to read during a night-time incident. Two backends is a pattern. Nine is a department.

## 15. What to Take Away

Here are four things to remember. One. Is the endpoint named after a resource, or after a screen? An endpoint for products belongs to everybody, and so to nobody. An endpoint for the phone's product screen belongs to one team. Two. The saving is not bytes. It is whose queue you are standing in. Three. Shape goes inside the backend. Anything the shop believes goes behind it. Four. One backend per real disagreement about what a product is. Not per device, and not per team. And one warning. All four can go wrong without anything failing. Because from inside each backend, each one is right.

## 16. Thanks for Watching

That's the Backends for Frontends pattern. If you remember one sentence, make it this one. Each screen gets its own backend, owned by the team that draws the screen, and it holds the shape, and nothing else. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. All three costs are there as running code, too. Here is one exercise to try. Update the phone backend's copy of the discount rule. Then check that both screens agree again. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
