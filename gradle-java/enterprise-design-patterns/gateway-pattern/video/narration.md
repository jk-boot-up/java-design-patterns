# Gateway Pattern — Video Narration Script

## 1. Gateway

Hello, and welcome. This video explains the Gateway pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a gateway is one class that wraps access to an outside system. The rest of the program speaks its own language, and can be tested without the real thing. This is another project in the enterprise category, whose subject is how a business application organises its logic, its data and its requests. In our online store, the outside thing is a payment provider. By the end you will see three places call a payment provider's client directly, see one door put in front of it, test the shop with no network, keep the network's habits in one class, swap provider without touching the shop, and see the bill, which is what the door cannot say.

## 2. The Scenario

Here is the scenario. The online store takes payments through an outside provider. Checkout, subscription renewals, and gift card top ups all need to charge a card. The provider's client uses maps of strings, and two digit result codes. The question: who talks to it?

## 3. The Provider's Client, Everywhere

First, the provider's client, everywhere. Checkout, subscription renewal and the gift card top up each build the provider's request and read its result codes. All three work. And one of them, the gift card, forgot the currency field. Nobody has noticed yet.

## 4. The Pattern

The pattern. One class wraps the outside system. It speaks the shop's language: approved, declined, unavailable. Only that class knows the provider's fields and codes. And the rest of the shop depends on the door, not on what is behind it.

## 5. One Door

Second, one door. The shop asks twice. The first is approved, and comes back with a receipt. The second is declined. Checkout has no field name and no result code in it. It speaks approved, declined and unavailable.

## 6. Tests That Never Leave The Process

Third, tests that never leave the process. A fake gateway, told what to answer, gives approved, then declined, then unavailable. Three questions, and zero network calls. A real provider cannot be told to be down on demand. The fake can.

## 7. One Place For The Network's Habits

Fourth, one place for the network's habits. The provider times out once, then answers. The gateway retries, and the shop is told: paid. Two network calls were made, and one line was logged. Two timeouts in a row, and the shop is told unavailable. The retry rule lives in one class.

## 8. Another Provider, The Same Shop

Fifth, another provider, the same shop. The same checkout runs on Acme, and on a second provider whose client has a completely different shape. Checkout was not changed. It was given a different gateway.

## 9. The Bill: What The Door Cannot Say

Last, the bill. Acme can hold a payment and capture part of it later. The gateway interface has one method: charge. To use partial capture, a method must be added to the interface and to all three gateways. And BetaPay cannot do it at all, so the interface must say what happens then. A door in the shop's words can only say what every provider can say.

## 10. How To Recognise It

How do you recognise this in code you did not write? An interface named for what the program needs, with an implementation named for the vendor. A Fake or InMemory implementation used in tests. A class that imports the vendor's SDK, which nothing else does. A wrapper around RestTemplate, WebClient, or a mail sender.

## 11. The Verdict

Here is my verdict, plainly. Put a gateway in front of any outside system your program depends on: a payment provider, a mail server, a remote API. Keep it small and in the program's own words. Put the system's habits in it: codes, retries, timeouts. Give tests a fake. Expect the interface to be the common ground, and decide on purpose what to do about features that only one provider has.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a call made in one place to a system that will never change, a wrapper is one more class to read. It earns its place with several callers, or a need for a fake.

## 14. Thanks for Watching

That's Gateway. If you take one sentence away, take this one: a gateway lets the shop speak its own language to the outside, at the price of only saying what every provider can say. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a refund method to the gateway, and see how many classes must change. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
