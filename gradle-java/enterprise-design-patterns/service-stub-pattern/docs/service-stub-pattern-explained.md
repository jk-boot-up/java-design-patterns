# Service Stub, Explained

## The pattern in one sentence

A service stub is a small in-memory stand-in for an external service, behind
the same gateway interface, used in development and tests and checked against
the real service regularly.

## The 5 acts

### 1. The real service in development

Developers call the real `PostcodeService` for every test checkout. Fifty in a
day cost £2.50 in lookup fees and twenty seconds of waiting. On a train with no
signal, the lookup is unavailable and nothing can be tried.

### 2. A service stub

Checkout already depends only on `AddressGateway`. `PostcodeStub` implements
it with a small in-memory map of postcodes. The same fifty checkouts cost
nothing, need no network, and wait for nothing.

### 3. Awkward cases on demand

A stub can be told what to do. An unknown postcode makes checkout ask the
customer to type their address. A stub switched to "down" makes checkout say
the lookup is unavailable and fall back to typing. Neither can be ordered from
the real service at the moment you want to test it.

### 4. The contract check

`ContractCheck` asks the stub and the real service the same questions, and
lists where they disagree. It runs weekly, not in every test. It finds one
difference: for "ls1 4ap" in small letters, the stub finds the address and the
real service refuses the format. Code tested only against the stub would have
broken in production.

### 5. The bill

A stub is a second, simpler copy of a service you do not own. Every change on
their side must be copied to it, and it only knows the postcodes you put in.
The contract check is what keeps it honest.

## The verdict

Stub services that are slow, paid, unreliable or unavailable offline. Keep
them behind a gateway interface, let them play failures on demand, and run a
contract check against the real service on a schedule.

## How to recognise this in code you did not write

- Classes named `...Stub`, `Fake...` or `InMemory...` implementing a gateway.
- WireMock or MockServer mappings in a test folder.
- A "sandbox" or "test mode" setting for an external provider.

## Where you have already met this

- WireMock and MockServer, which stand in for HTTP services.
- Payment providers' test modes and sandbox accounts.
- LocalStack, which stands in for cloud services on a laptop.
- Pact and other contract-testing tools, which check that stubs still match the real thing.
