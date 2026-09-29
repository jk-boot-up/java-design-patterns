# Special Case Pattern — Video Narration Script

## 1. Special Case

Hello, and welcome. This video explains the Special Case pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When there is no ordinary object to return, such as no customer logged in, return an object for that special case instead of nothing. It answers every question in the way that fits. Think of the badges at a conference. Delegates get a badge with their name. Walk-in visitors get a visitor badge. Every door reads a badge the same way. Nobody has to stop and ask: do you have a badge at all? In this video, the domain is an online shop. Its checkout serves registered customers, guests without an account, and old orders from deleted accounts. By the end, you will hear how null checks crash a checkout. How special cases remove them. How to ask for behaviour instead of type. And what special cases can hide.

## 2. The Scenario

Here is the scenario. Registered customers get a member discount, loyalty points, and the newsletter. Guests check out without an account. And some old orders belong to accounts that were deleted. For guests and deleted accounts, the customer lookup returned null. Nothing at all.

## 3. Act One — Null checks everywhere

First demo: no customer means null, and null checks everywhere. Null is Java's way of saying: there is no object here. Priya is a registered customer. She pays thirty-eight pounds, after her member discount. Then a guest checks out. There is no account, so the lookup returns null. Checkout checked for null when reading the name, the discount, and the newsletter flag. But the loyalty points line forgot. The page crashes, with a null pointer exception.

## 4. Act Two — A guest special case

Second demo: a guest special case. The lookup never returns null any more. With no account, it returns a guest object. The guest answers every question checkout asks. Its name is Guest. Its discount is zero. It earns no points, and gets no newsletter. Checkout has no if statements at all. Priya pays thirty-eight pounds. The guest pays forty pounds, with no points. Nothing crashes.

## 5. Act Three — An unknown customer

Third demo: a second special case. An old order belongs to account C 99. That account was deleted. The lookup returns an unknown customer. Its name is Former customer. It remembers the old ID. The order history report runs, with no crash, and still says who it was.

## 6. Act Four — Behaviour, not type checks

Fourth demo: ask for behaviour, not for the type. The newsletter step asks each customer one question. Can you receive marketing? Priya: yes. The guest: no. The former customer: no. Nowhere does the code ask: are you a guest? Each case answers for itself.

## 7. Act Five — The bill

Fifth demo: the bill. A special case can hide a mistake. Someone mistypes an ID: C 71 instead of C 17. It quietly becomes a former customer, and checkout carries on. And every new method on customer must now be written three times. Once for registered customers, once for guests, and once for unknown customers.

## 8. The Pattern

Let's name the pattern. Never return null for a situation that is normal. Return an object for that special case instead. A guest. A former customer. Each one implements the same interface as an ordinary customer. And answers every question in the way that fits.

## 9. Who Does What

Here is who does what. Customer is the interface: the questions checkout asks. Registered customer is the ordinary case. Guest and unknown are the special cases. Small records that give the right answers. And the directory's find method never returns null.

## 10. Where You Have Seen It

You have probably met this pattern already. Collections dot empty list is a special case for no items. Web frameworks represent visitors who are not logged in as an anonymous user, not as null. Forums show deleted user in place of a removed account. And the Null Object pattern is the simplest special case of all: one that does nothing.

## 11. When To Use It

So, when should you use it? For situations that are normal, and have a sensible meaning. A guest checking out. An order from a deleted account. Keep real errors as errors. If a missing value is a bug, throw an exception, or return an optional, and let the caller decide.

## 12. Thanks for Watching

That's the Special Case pattern. If you remember one sentence, make it this one. Give the odd but normal case its own object, and stop returning null. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a staff special case, with a twenty percent discount and no points. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
