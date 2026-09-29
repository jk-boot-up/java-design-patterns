# Remote Facade with Spring MVC Pattern — Video Narration Script

## 1. Remote Facade with Spring MVC

Hello, and welcome. This video explains the Remote Facade pattern, with Spring MVC, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A remote facade gives callers across a network a few coarse calls, each doing a lot. Instead of many small calls, each paying for a trip across the network. Spring MVC is the open-source web framework most Java services use. Think of ordering at a restaurant. You give the whole order in one visit, instead of calling the waiter over five times. In this video, the domain is an online shop's phone app, showing and changing an order. By the end, you will hear what five round trips cost. How one call returns a whole screen. How a change becomes all or nothing. And what the facade costs.

## 2. The Scenario

Here is the scenario. The shop's phone app asked the server for each fact of the order screen separately. On a mobile network, each question took about eighty milliseconds. And changing a delivery took two calls, that could fail halfway.

## 3. Act One — A call for every fact

First demo: the phone app asks for each fact separately. The customer. The items. The total. The address. The delivery slot. Five trips across a mobile network. Almost half a second, before the screen can be drawn.

## 4. Act Two — The whole screen as JSON

Second demo: a remote facade. One call returns everything the order screen needs, as one JSON document. One trip across the network. Under a fifth of a second.

## 5. Act Three — All or nothing

Third demo: a change, all or nothing. With small calls, the address changes first. Then the new slot is refused. The order is left half changed. New address, old slot. The facade takes the whole change in one call. Sunday is refused, and nothing changes. Tuesday is accepted, and both change together.

## 6. Act Four — Fine-grained inside

Fourth demo: inside, the order stays fine-grained. The facade calls the order's small methods, inside the server, where calls are cheap. The rule about valid slots lives on the order. And a refusal comes back as a standard problem report.

## 7. Act Five — The bill

Fifth demo: the bill. A small widget shows only the delivery slot. The small call sends eight bytes. The summary sends a hundred and thirty. And every new screen may want its own facade method.

## 8. The Pattern, in Spring MVC

Let's name the pattern, in Spring's words. A thin controller, just for remote callers. One call returns a whole screen, as JSON. One call makes a whole change. And inside, the objects stay fine-grained.

## 9. Who Does What

Here is who does what. The order facade offers the summary, and the delivery change. The order keeps its small methods, and the business rules. The fine-grained controller is the old way. And the mobile network filter adds eighty milliseconds to every request.

## 10. Where You Have Seen It

You have probably met this already. Web endpoints that return a whole screen at once. Backends for frontends, which give each app its own coarse service. And GraphQL, which lets an app ask for a whole screen in one request.

## 11. When To Use It

So, when should you use it? For callers across a network, especially a slow one. Offer screen-sized calls. Make changes all or nothing. And keep the business rules inside, on the objects.

## 12. Thanks for Watching

That's the Remote Facade, with Spring MVC. If you remember one sentence, make it this one. Across a network, ask once for the whole screen, and change it in one step. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add an entity tag to the summary, so an unchanged screen costs almost nothing. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
