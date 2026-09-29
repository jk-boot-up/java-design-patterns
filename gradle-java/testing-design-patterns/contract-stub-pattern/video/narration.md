# Contract Stub Pattern — Video Narration Script

## 1. Contract Stub

Hello, and welcome. This video explains the Contract Stub pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A stub is a stand-in for another service, used in tests. A contract stub is made from a written agreement between the two teams. And the real service is checked against that same agreement. So the stub and the real service can never quietly drift apart. Think of a fire drill. If it used an old floor plan, everyone would practise walking to an exit that has since been bricked up. A contract stub is a drill always run from the current plan. In this video, the domain is an online shop's checkout, which calls a payment service run by another team. By the end, you will hear how a hand-written stub let a bug reach production. How a contract feeds both the stub and a check of the real service. Why a strict stub helps. And what the contract costs.

## 2. The Scenario

Here is the scenario. The shop's checkout calls a payment service, run by another team. Checkout's tests used a stub the checkout team had written by hand. The payment team renamed a field in its reply. The tests stayed green. And production broke.

## 3. Act One — A stub that drifted

First demo: a hand-written stub. A stub is a stand-in for another service, used in tests. The checkout team wrote their own stub of the payment service. It replies with a field called result, set to approved. The checkout test passes. But the payment team released version two. They renamed result, to outcome. In production, checkout finds no result in the reply. The order is stuck. And the tests stayed green, because the stub never changed.

## 4. Act Two — A stub made from the contract

Second demo: a stub made from a contract. The two teams write down what they have agreed. Three interactions. Each one is a request, and the reply it gets. A normal charge is approved. A card with no funds is declined. A zero amount is rejected. Checkout's tests use a stub built from that contract. And they get exactly those three replies.

## 5. Act Three — The provider is checked too

Third demo: the real payment service is checked against the same contract. The payment team's build replays all three interactions. Version one matches, three of three. Version two, with the rename, matches zero of three. So the payment team's own build fails. Before the change reaches anyone. The stub and the real service can never quietly drift apart.

## 6. Act Four — A strict stub

Fourth demo: the contract stub is strict. Checkout starts charging in US dollars. The hand-written stub approves it. Nobody asked the payment team. The contract stub refuses. There is no interaction in the contract for that request. So checkout must agree it with the payment team first.

## 7. Act Five — The bill

Fifth demo: the bill. The contract is shared work. Both teams must keep it, version it, and run it in both builds. And it only covers what is written in it. It says nothing about speed. Or about the real network.

## 8. The Pattern

Let's name the pattern. Write the contract down, as requests and the replies they get. The consumer tests against a stub made from that contract. The provider's build checks the real service against the same contract.

## 9. Who Does What

Here is who does what. The contract holds the agreed interactions. The contract stub answers checkout's tests from it, and refuses anything else. The provider verifier replays it against the real payment service. And checkout is the consumer being tested.

## 10. Where You Have Seen It

You have probably met this pattern already. Spring Cloud Contract turns contracts into stubs, and tests for the provider. Pact does the same, starting from the consumer's tests. And mock servers built from an interface description work the same way.

## 11. When To Use It

So, when should you use it? When separate teams release their services separately. Share and version the contract. Run it in both builds. And when the stub refuses a request, treat it as a prompt to talk to the other team.

## 12. Thanks for Watching

That's the Contract Stub pattern. If you remember one sentence, make it this one. Build the stub and check the real service from the same contract. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a US dollar interaction to the contract, and make both sides pass. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
