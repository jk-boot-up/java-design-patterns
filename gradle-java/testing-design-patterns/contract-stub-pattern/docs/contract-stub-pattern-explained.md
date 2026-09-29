# Contract Stub, Explained

## The pattern in one sentence

A Contract Stub is a test stub made from a shared contract that the real
service is also checked against, so the two cannot drift apart.

## The 5 acts

### 1. A stub that drifted

The checkout team's hand-written stub replies with a "result" of APPROVED,
and the checkout test confirms the order. But the payment team's version 2
renamed "result" to "outcome". In production, checkout finds no result in the
reply and the order is stuck. The stub never knew, so the tests stayed green.

### 2. A stub made from the contract

The two teams write down a contract: three agreed interactions, each a request
and the reply it gets. A normal charge is approved, a card with no funds is
declined, and a zero amount is rejected. The checkout tests run against a
stub made from that contract, and see exactly those three replies.

### 3. The provider is checked too

The other half: the payment team's build replays the same three
interactions against the real service. Version 1 matches all three. Version 2,
with its rename, matches none, so the payment team's own build fails before
the change is released. The stub and the real service cannot quietly drift
apart.

### 4. A strict stub

Checkout starts charging in US dollars. The hand-written stub happily
approves it, although nobody asked the payment team. The contract stub
refuses: there is no interaction in the contract for that request. Checkout
must agree US dollars with the payment team before its tests can rely on it.

### 5. The bill

The contract is shared work: both teams must keep it, version it, and run it
in both builds. And it only covers what is written in it. It says nothing
about how fast the service is, or what happens on the real network.

## The verdict

Use contract stubs when separate teams release services independently. Keep
the contract in a shared, versioned place, run it in both builds, and treat
the stub's refusal of unlisted requests as a prompt to talk to the other team.

## How to recognise this in code you did not write

- Spring Cloud Contract `.groovy` or `.yml` contracts and generated stubs.
- Pact files published to a broker.
- A provider build step named verify or contract test.

## Where you have already met this

- Spring Cloud Contract, which generates WireMock stubs from contracts.
- Pact, whose consumer tests produce the contract the provider verifies.
- OpenAPI-based mock servers checked against the real service.
