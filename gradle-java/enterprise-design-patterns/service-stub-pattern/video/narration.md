# Service Stub Pattern — Video Narration Script

## 1. Service Stub

Hello, and welcome. This video explains the Service Stub pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A service stub is a small, free stand-in for an outside service, such as a paid address lookup. It sits behind the same interface, and answers like the real one. You use it while developing and testing. Think of a flight simulator. Pilots practise in it every day, for free. It can give them an engine failure on demand. But it is only useful while it behaves like the real plane, so it is checked against the real aircraft. In this video, the domain is an online shop. At checkout, it turns a postcode into an address, using a paid outside service. By the end, you will hear what developing against the real service costs. How a stub fixes it. How to test failures on demand. And how to keep a stub honest.

## 2. The Scenario

Here is the scenario. At checkout, the customer types a postcode, and the shop fills in the address. To do that, it asks an outside postcode service. Each lookup costs five pence. It takes four hundred milliseconds. And it needs the network. Developers were calling it for every test checkout.

## 3. Act One — The real service in development

First demo: developing against the real postcode service. Every lookup costs five pence, and takes four hundred milliseconds. A developer tries fifty test checkouts in a day. Two pounds fifty in lookup fees. Twenty seconds of waiting. Then they get on a train with no signal. The lookup is unavailable, and they cannot work at all.

## 4. Act Two — A service stub

Second demo: a service stub. Checkout only knows a small interface: the address gateway. A postcode in, an address out. The stub implements that interface, with a few postcodes kept in memory. Four Mill Lane, Leeds, comes back instantly. Fifty checkouts cost nothing, need no network, and wait for nothing.

## 5. Act Three — Awkward cases on demand

Third demo: the stub plays the awkward cases, on demand. An unknown postcode. Checkout asks the customer to type their address. A service that is down. The stub can pretend. Checkout says the lookup is unavailable, and asks the customer to type it. You cannot ask the real service to go down, just when you want to test it.

## 6. Act Four — The contract check

Fourth demo: a contract check. Once a week, the stub and the real service are asked the same questions. Any difference is reported. One postcode, typed in small letters. The stub finds the address. The real service refuses it: invalid format. Checkout, tested only against the stub, would have broken in production.

## 7. Act Five — The bill

Fifth demo: the bill. A stub is a second, simpler copy of someone else's service. It must be kept in step with the real one. And it only knows the postcodes you gave it. The contract check is what keeps it honest.

## 8. The Pattern

Let's name the pattern. Put the outside service behind a small gateway interface. In development and in tests, plug in a stub. A small class, in memory, that answers like the real service. And regularly, ask the stub and the real service the same questions, to check they still agree.

## 9. Who Does What

Here is who does what. Address gateway is the interface: a postcode in, an address out. Postcode service is the real, paid service. Postcode stub is the stand-in, with a few postcodes, and a switch to pretend it is down. The contract check compares the two. And checkout is the client, which knows only the interface.

## 10. Where You Have Seen It

You have probably met this pattern already. WireMock and MockServer stand in for web services during tests. Payment providers offer sandboxes and test modes. LocalStack stands in for cloud services on a laptop. And Pact, and other contract-testing tools, check that stubs still match the real thing.

## 11. When To Use It

So, when should you use it? Stub outside services that are slow, paid, unreliable, or only available online. Let the stub play failures on demand. And run a contract check against the real service on a schedule. Do not stub your own code just to make tests quicker. Stub what is genuinely outside your control.

## 12. Thanks for Watching

That's the Service Stub pattern. If you remember one sentence, make it this one. Develop against a free stand-in, and check it against the real thing. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Fix the stub so it refuses small letters, and watch the contract check pass. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
