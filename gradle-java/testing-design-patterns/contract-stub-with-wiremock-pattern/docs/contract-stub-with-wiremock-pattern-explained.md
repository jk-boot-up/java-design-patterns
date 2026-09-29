# Contract Stub with WireMock, Explained

## The pattern in one sentence

With WireMock, a contract stub is a real HTTP stub server built from a shared
contract file that the real service is also checked against.

## The 5 acts

### 1. A stub that drifted

The checkout team's hand-written WireMock stub approves any charge with a
"result" field. The checkout test confirms the order. But payment service
version 2 renamed "result" to "outcome", and in production checkout finds no
result in the reply: the order is stuck. The stub never knew.

### 2. A stub from the contract

The two teams keep one contract file with three interactions. A WireMock stub
is built from it, one stub per interaction, matching the request body as JSON.
Checkout's tests get exactly the agreed replies: confirmed, declined for no
funds, rejected for a zero amount.

### 3. The provider is checked too

The payment team's build replays the same three interactions against the real
service over HTTP. Version 1 matches all three. Version 2, with its rename,
matches none, so the payment team's own build fails before the change is
released.

### 4. A strict stub

Checkout starts charging in US dollars. The hand-written stub confirms it,
although nobody asked the payment team. The contract stub answers WireMock's
404, "Request was not matched", and reports the closest stub it had, so the
difference is easy to see.

### 5. The bill

The contract file is shared work: both teams must keep it, version it and run
it in both builds. It covers only the interactions written in it, not speed
or the real network. Spring Cloud Contract automates exactly this flow,
generating the WireMock stubs and the provider tests from contracts.

## The verdict

Use contract stubs when separate teams release separately. Keep the contract
in a shared, versioned place, build stubs from it, verify providers against
it, and let a tool such as Spring Cloud Contract generate both halves.

## How to recognise this in code you did not write

- `WireMock.stubFor(post(...).withRequestBody(equalToJson(...)))`.
- Shared contract files in a repository both teams build.
- `Request was not matched` in a failing test's output.

## Where you have already met this

- Spring Cloud Contract, which generates WireMock stubs and provider tests from contracts.
- Pact, whose consumer tests write the contract the provider verifies.
- WireMock mappings kept in a repository shared by two teams.
