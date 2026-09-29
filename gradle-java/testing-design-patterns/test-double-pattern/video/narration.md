# Test Double Pattern — Video Narration Script

## 1. Test Double

Hello, and welcome. This video explains the Test Double pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A test double is an object that takes the place of something your code depends on, just for a test. So the test can run fast, without the network, without spending real money, and ask exactly the question it needs. The name comes from films. When a scene is dangerous, the actor does not jump off the roof. A stunt double does. Same costume, same shape on camera, but trained for the fall. In this video, the domain is an online shop's checkout. Checkout takes a customer's money through a payment provider: an outside company that charges the card. By the end, you will know the five kinds of test double: dummy, stub, spy, mock and fake. Which question each one answers. And the one thing no double can ever tell you.

## 2. The Scenario

Here is the scenario. Checkout turns a basket total into a paid order. To take the money, it calls a payment gateway. A gateway is the part of the code that talks to the card provider. The real gateway is slow. It needs the network. And every successful call charges a real card. So how do we test checkout?

## 3. Act One — The Real Provider

First demo: testing against the real provider. Three checkout tests. They pass. But they take two point four seconds of network calls. And they charge eighty-eight pounds forty-two to a real test card. Then the laptop goes offline, on a train. The fourth test fails: network unreachable. Checkout was not broken. The test failed for a reason outside the code. A good unit test must never do that.

## 4. The Pattern

Now, the pattern. Checkout depends on an interface, called payment gateway, not on the real provider. An interface is a list of methods, with no code behind them. So a test can put any object behind that interface. Something that looks like a provider to checkout, but is built for the test. There are five kinds of test double. Each one answers a different question.

## 5. Act Two — A Dummy And A Stub

Second demo: the two simplest doubles. First, a dummy. A dummy is passed in only because checkout needs something. It must never be used, and it fails loudly if it is. An empty basket must be refused without touching the provider. With a dummy behind checkout, the test passes. So we know, for certain, the provider was never called. Second, a stub. A stub gives a fixed, canned answer. This one always says: declined, insufficient funds. So the test can check what checkout does when a card is declined. Something hard to arrange with a real card. Both ran instantly, and charged nothing.

## 6. Act Three — A Spy

Third demo: a spy. A spy answers like a stub. But it also writes down every call it receives. The test places order seven, for sixty-three pounds forty-four. Then cancels it. Afterwards, the test reads the spy's notes. Charge order seven, six thousand three hundred and forty-four pence. Then refund receipt spy one. So the test can check the exact amount, that it was charged only once, and that the right receipt was refunded.

## 7. Act Four — A Mock

Fourth demo: a mock. A mock is told in advance exactly which calls to expect. Here: one charge, for order eight, six thousand three hundred and forty-four pence. The charge happens. And a final check, called verify, confirms every expected call arrived. Then the customer double-clicks the pay button. Checkout charges again. And the mock fails the test at that very moment: unexpected call, no more charges were expected. So here is the difference. A spy is checked after the test. A mock checks as the calls happen. That makes it good at catching things that must never happen twice.

## 8. Act Five — A Fake

Fifth demo: a fake. A fake is a small provider that really works, but keeps everything in memory. This one has a card limit of one hundred pounds. Pay sixty-three forty-four: paid. Pay another fifty pounds: declined, over the card limit. Cancel the first order: the balance goes back to zero. Pay fifty pounds again: paid, balance fifty pounds. A whole customer journey, tested in milliseconds, offline. With real behaviour, instead of canned answers.

## 9. Five Doubles, Five Questions

Here are the five doubles, and the question each one answers. A dummy: was the provider left alone? A stub: what does checkout do if the answer is no? A spy: what exactly was called, and with which amount? A mock: nothing else may happen, not even once more. A fake: does the whole journey work, from payment to refund? Pick the lightest double that answers your question.

## 10. Act Six — The Bill

Finally, the bill. A double only checks what you told it to check. Here is a planted bug. Checkout sends the amount in pounds, where the provider expects pence. Sixty-three, instead of six thousand three hundred and forty-four. Tested with a stub that approves anything, the test passes. The bug is invisible. The same bug with a spy fails. Because the spy recorded sixty-three. And no double, however careful, can tell you the real provider still accepts your requests. Keep at least one test against the real provider's test sandbox.

## 11. What Doubles Cost

So, what do doubles cost? They check only what you ask them to. They can quietly drift away from how the real provider behaves. And a mock, which expects exact calls, can break when code is rearranged, even when the customer sees the same result. Where you can, check the result, like the fake's balance, rather than the exact calls. Checks on results survive changes to the code.

## 12. How To Recognise It

How can you spot test doubles in code someone else wrote? Look for Mockito: methods called mock, when, then return, and verify. A mocking library writes these doubles for you. Look for classes named fake, stub, or in memory, in the test folder. Or the mock bean annotation, in Spring tests.

## 13. The Verdict

So, here is the verdict. Depend on an interface for anything slow, costly, or outside your control. Then replace it in your unit tests. Use the lightest double that answers your question. A stub before a spy. A spy before a mock. And a fake for whole journeys. And keep one test against the real provider's sandbox.

## 14. Thanks for Watching

That's the Test Double pattern. If you remember one sentence, make it this one. A test double stands in for a dependency, so a test runs fast and safely, but it only checks what you told it to. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Rewrite the tests using the Mockito library. And for each Mockito call, name which of the five doubles it creates. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
