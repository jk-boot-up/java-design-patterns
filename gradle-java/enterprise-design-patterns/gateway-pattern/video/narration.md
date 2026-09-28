# Gateway Pattern — Video Narration Script

## 1. Gateway

Hello, and welcome. This video explains the Gateway pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A gateway is one class that wraps access to an outside system. The rest of the program speaks its own language. And it can be tested without the real outside system. Think of a travel adapter plug. Your charger stays the same in every country. Only the adapter knows the shape of the foreign socket. In our online store, the outside system is a payment provider. In this video, three places call the provider directly. Then one door is put in front of it. We will test the shop with no network, keep the network's quirks in one class, and swap provider without touching the shop. And then the cost.

## 2. The Scenario

Here is the scenario. The online store takes payments through an outside provider. Checkout, subscription renewals, and gift card top-ups all need to charge a card. The provider's own client code uses maps of text values, and two-digit result codes. So here is the question. Who should talk to it?

## 3. The Provider's Client, Everywhere

First, the naive way: the provider's client, everywhere. Checkout, subscription renewal, and gift card top-up each build the provider's request themselves. And each reads the provider's result codes. All three work. But one of them, the gift card, forgot the currency field. And nobody has noticed yet.

## 4. The Pattern

Now, the pattern. One class wraps the outside system. It speaks the shop's language: approved, declined, or unavailable. Only that class knows the provider's fields and codes. And the rest of the shop depends on the door, not on what is behind it.

## 5. One Door

Second demo: one door. The shop asks for two payments. The first is approved, and comes back with a receipt. The second is declined. The checkout code contains no provider field names, and no result codes. It only speaks of approved, declined, and unavailable.

## 6. Tests That Never Leave The Process

Third demo: tests that never leave the program. A fake gateway is told what to answer. It gives approved, then declined, then unavailable. Three questions, and zero network calls. A real provider cannot be told to go down on demand. The fake can.

## 7. One Place For The Network's Habits

Fourth demo: one place for the network's quirks. The provider times out once, and then answers. The gateway tries again, and the shop is simply told: paid. Two network calls were made. If it times out twice in a row, the shop is told: unavailable. The retry rule lives in one class.

## 8. Another Provider, The Same Shop

Fifth demo: another provider, the same shop. The same checkout runs on the Acme provider. And then on a second provider, called BetaPay, whose client has a completely different shape. The checkout was not changed at all. It was simply given a different gateway.

## 9. The Bill: What The Door Cannot Say

Finally, the cost: what the door cannot say. Acme can hold a payment, and collect only part of it later. But the gateway interface has just one method: charge. To use that feature, a method must be added to the interface, and to all three gateways. And BetaPay cannot do it at all. So the interface must say what happens then. A door that speaks the shop's language can only say what every provider can say.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for an interface named after what the program needs, with an implementation named after the vendor. Look for a fake, or in-memory, version used in tests. Look for one class that imports the vendor's library, which nothing else imports. And look for wrappers around web clients, or mail senders.

## 11. The Verdict

So, here is the verdict. Put a gateway in front of any outside system your program depends on. A payment provider, a mail server, or a remote service. Keep it small, and in your program's own words. Put the outside system's quirks inside it: codes, retries, and timeouts. Give your tests a fake. And expect the interface to cover only what all providers share. Decide on purpose what to do about features only one provider has.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every result you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a call made in one place, to a system that will never change, a wrapper is just one more class to read. A gateway earns its place when there are several callers, or when you need a fake for testing.

## 14. Thanks for Watching

That's the Gateway pattern. If you remember one sentence, make it this one. A gateway lets your program speak its own language to the outside world, at the price of only saying what every provider can say. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a refund method to the gateway. Then count how many classes had to change. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
