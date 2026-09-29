# Test Double, Explained

## The pattern in one sentence

A test double takes the place of something your code depends on, so a test can
run fast and offline and ask one precise question: a dummy for "unused", a stub
for "what if", a spy for "what was called", a mock for "never anything else",
and a fake for "the whole journey".

## The 6 acts

### 1. The real provider

Three checkout tests run against the real provider. They pass, but they take
2400 milliseconds of network calls and charge £88.42 to a real test card. Then
the laptop goes offline, on a train, and the fourth test fails with "network
unreachable". Checkout was not broken; the test failed for a reason outside the
code. That is exactly what a unit test must never do.

### 2. A dummy and a stub

Two of the simplest doubles. An empty basket must be refused without touching
the provider, so the test passes a **dummy**, which throws if it is used at all.
The test passes: "refused: the basket is empty". The dummy turns "I think this
never pays" into a checked fact. Then a **stub** that always answers "declined:
insufficient funds" lets the test drive checkout down the decline path, which is
hard to make happen with a real card. Both run in no time and charge nothing.

### 3. A spy

A **spy** answers like a stub, and also writes down every call. The test places
order ORD-7 for £63.44 and then cancels it, and afterwards reads the spy's
notes: `charge(ORD-7, 6344)` and `refund(spy-1)`. So the test can check the
exact amount in pence, that it was charged once, and that the refund used the
right receipt: questions a stub alone cannot answer.

### 4. A mock

A **mock** is told in advance exactly which calls to expect: here, one charge of
6344 pence for ORD-8. That call goes through, and `verify()` confirms every
expected call happened. Then the customer double-clicks and checkout charges
again: the mock fails *at that moment*, "unexpected call ... no more charges
were expected". A spy is checked after the test; a mock checks as the calls
happen, which makes it good at catching things that must never happen twice.

### 5. A fake

A **fake** is a small provider that really works, keeping its ledger in memory.
With a card limit of £100.00, paying £63.44 succeeds, a further £50.00 is
declined as over the limit, cancelling the first order brings the balance back
to £0.00, and £50.00 then succeeds, leaving £50.00. A whole customer journey,
tested in milliseconds, offline, with real behaviour rather than canned answers.

### 6. The bill

A double only checks what you asked it to. A checkout with a planted bug sends
pounds where the provider expects pence, 63 instead of 6344. Tested with a stub
that approves anything, it **passes**. The same bug tested with a spy fails,
because the spy recorded `charge(ORD-12, 63)`. And no double, however careful,
can tell you the real provider still accepts your requests; keep at least one
test against the real thing or its sandbox.

## The verdict

Depend on interfaces for anything slow, costly or out of your control, and
replace them in unit tests. Pick the lightest double that answers your
question: stub before spy, spy before mock, fake for journeys. Check results
(state) rather than calls where you can, because it survives refactoring. And
keep one test against the real provider's sandbox.

## How to recognise this in code you did not write

- Classes named `Fake...`, `Stub...`, `InMemory...` in test folders.
- Mockito: `mock()`, `when().thenReturn()`, `verify()`, `@Mock`, `@Spy`.
- An interface with one real implementation and several in `src/test`.
- `@MockBean` in Spring Boot tests.

## Where you have already met this

- Mockito's `mock()`, `when(...).thenReturn(...)` (a stub) and `verify(...)` (spy-style checks).
- Spring's `@MockBean`, and in-memory databases such as H2 used as fakes.
- Payment sandboxes (Stripe test mode): a fake that the provider runs for you.
- Testcontainers: the other way round, a real database in a container instead of a double.
