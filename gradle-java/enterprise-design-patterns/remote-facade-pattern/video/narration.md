# Remote Facade Pattern — Video Narration Script

## 1. Remote Facade

Hello, and welcome. This video explains the Remote Facade pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A remote facade is a front for callers across a network. One call returns everything a screen needs. One call makes a whole change, all or nothing. Inside, the objects stay small and simple. Think of ordering from a shop by post. You would not send five letters, one per question, and wait days for each reply. You send one letter with every question, and get one letter back. In this video, the domain is an online shop's phone app. It shows an order screen: the customer, the items, the total, the address, and the delivery slot. By the end, you will hear why many small calls over a network are slow. How a facade fixes it. How a change can be all or nothing. And what it costs.

## 2. The Scenario

Here is the scenario. The shop's phone app shows an order. The customer, the items, the total, the delivery address, and the delivery slot. The app talks to the server over a mobile network. Every request is a round trip: there and back. About eighty milliseconds each.

## 3. Act One — Many small remote calls

First demo: the phone app asks for each fact separately. The customer's name. The items. The total. The address. The delivery slot. Each question is one trip across the network, and back. On a mobile network, about eighty milliseconds each. Five round trips. Four hundred milliseconds, just to draw one screen.

## 4. Act Two — One facade call

Second demo: a remote facade. The server offers one bigger call: the order summary. It answers with everything the screen needs, in one reply. Order number, customer, items, total, address, and slot. One round trip. Eighty milliseconds.

## 5. Act Three — A change in one call

Third demo: a change in one call, all or nothing. Priya moves, and wants a Sunday delivery. With small calls, the address change works. Then the slot fails: there are no Sunday slots. The order is left half changed: new address, old slot. With the facade, it is one call. The slot is checked first. It fails, and nothing changes. With a Tuesday slot, both change together.

## 6. Act Four — Fine-grained inside

Fourth demo: inside, the order stays fine-grained. The facade calls the order's small methods, six of them. In-process, that takes well under five milliseconds. And the rules stay on the order. Which slots exist is decided by the order, not the facade. The facade only packs and unpacks.

## 7. Act Five — The bill

Fifth demo: the bill. A small widget shows only the delivery slot. With the small call, it downloads eight bytes. With the summary, seventy-three. And the facade is one more layer. Each new screen may want its own facade method.

## 8. The Pattern

Let's name the pattern. Give callers across the network a few big calls. A whole screen at once. A whole change at once. Inside the server, keep the objects small, with their small methods. The facade only gathers and packs. The business rules stay on the objects.

## 9. Who Does What

Here is who does what. The order has small methods, and holds the rules, such as which delivery slots exist. The order facade offers two big calls: the summary, and change delivery. The phone is the remote caller, and counts its round trips. And the fine-grained A P I is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Web A P Is with summary or details endpoints, that return a whole screen at once. Older Java enterprise applications had session facades. Backend for frontend services give each app its own coarse A P I. And GraphQL lets the app ask for a whole screen in one request.

## 11. When To Use It

So, when should you use it? In front of any fine-grained model that is called over a network. Shape the calls around screens, and around whole changes. Keep the rules on the domain objects. Inside one program, you do not need it. Small calls there are almost free.

## 12. Thanks for Watching

That's the Remote Facade pattern. If you remember one sentence, make it this one. Across a network, make fewer, bigger calls, and keep the small ones inside. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a cancel call to the facade, that refuses if the order has shipped. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
