# Contract Stub with WireMock Pattern — Video Narration Script

## 1. Contract Stub with WireMock

Hello, and welcome. This video explains the Contract Stub pattern, with WireMock, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A contract stub is a stand-in for another service, built from a written agreement between two teams. The real service is checked against the same agreement. So the two can never quietly drift apart. WireMock is an open-source stub server that answers real web requests. Think of a fire drill run from the building's current floor plan. The builders must update the plan whenever they move a wall. In this video, the domain is an online shop's checkout, calling a payment service run by another team. By the end, you will hear how a hand-written stub let a bug through. How one contract file builds the stub and checks the real service. And where Spring Cloud Contract fits.

## 2. The Scenario

Here is the scenario. The shop's checkout calls a payment service, run by another team. Checkout's tests used a stub its own team had written. The payment team renamed a field. The tests stayed green. Production broke.

## 3. Act One — A stub that drifted

First demo: a hand-written stub. The checkout team's stub approves every charge. The checkout test passes. But the payment team released version two. It renamed the result field. In production, checkout cannot find the result. The order is stuck. The stub never knew.

## 4. Act Two — A stub from the contract

Second demo: a stub built from the contract. The two teams share one file, with three agreed interactions. A stub server is built from it. A normal card is confirmed. A card with no funds is declined. A zero amount is rejected.

## 5. Act Three — The provider is checked too

Third demo: the real payment service is checked against the same file. Every interaction is sent to it, over HTTP. Version one matches, three of three. Version two matches none. The payment team's own build fails, before the change reaches anyone.

## 6. Act Four — A strict stub

Fourth demo: the contract stub is strict. Checkout starts charging in US dollars. The hand-written stub confirms it. Nobody asked the payment team. The contract stub answers, request was not matched. And it shows the closest request it knows.

## 7. Act Five — The bill

Fifth demo: the bill. The contract is shared work. Both teams keep it, version it, and run it in both builds. It covers only what is written in it. And tools such as Spring Cloud Contract automate exactly this. They generate the stubs, and the provider's tests, from the contracts.

## 8. The Pattern, with WireMock

Let's name the pattern, with WireMock. One shared contract file. The consumer tests against a WireMock stub, built from that file. And the provider's build replays the same file against the real service.

## 9. Who Does What

Here is who does what. The contract file lists the agreed interactions. The contract stub builds a WireMock server from it. The provider verifier replays it against the real payment service. And checkout is the consumer.

## 10. Where You Have Seen It

You have probably met this already. Spring Cloud Contract generates WireMock stubs and provider tests from contracts. Pact does the same, starting from the consumer's tests. And teams often share WireMock mapping files in a repository.

## 11. When To Use It

So, when should you use it? When separate teams release their services separately. Share and version the contract. Run it in both builds. And let a tool generate both halves when the contracts grow.

## 12. Thanks for Watching

That's the Contract Stub, with WireMock. If you remember one sentence, make it this one. Build the stub and check the real service from the same contract. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a US dollar interaction to the contract, and make both sides pass. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
