# Delegation Pattern — Video Narration Script

## 1. Delegation

Hello, and welcome. This video explains the Delegation pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: delegation is when an object does not do a job itself. It hands the job to a helper object that it holds, and that it can swap. This is another project in the foundational category, whose subject is how an object gets hold of another, and how small idioms shape everyday Java. In our online store, an order can be priced in several ways, and each new way seems to need a new kind of order. By the end you will see classes multiply for each way of pricing, see an order hand its pricing on, see the helper swapped while the order lives, see two helpers used at once, see why the helper is given the order, and see the bill, which is an extra call and forwarding methods.

## 2. The Scenario

Here is the scenario. An order can be priced with a premium discount, with gift wrap, with both, or with neither. A customer may become premium in the middle of shopping. The question: do we need a class for each?

## 3. A Subclass For Each Way

First, a subclass for each way. Premium, gift wrap, and both: four classes for two features. A third feature would need eight. A premium gift order is ninety six hundred. And an order cannot change its class once it exists.

## 4. The Pattern

The pattern. The object holds a helper. When asked to do the job, it hands the job to the helper. The helper can be swapped, and used with others.

## 5. The Order Hands The Pricing On

Second, the order hands the pricing on. One order class. With no rule, ten thousand. With premium, nine thousand. With gift wrap, ten thousand six hundred.

## 6. Change The Helper While It Lives

Third, change the helper while it lives. The customer joins the premium plan while shopping. The same order object: ten thousand, then nine thousand.

## 7. Two Helpers At Once

Fourth, two helpers at once. Premium then gift wrap: ninety six hundred, the same as the class made for both. Classes added: none.

## 8. The Helper Needs To See The Order

Fifth, the helper needs to see the order. Gift wrap is three hundred for each item, so it must look at the order it was called for. Two items: ten thousand six hundred. Three items: ten thousand nine hundred. That is why the order passes itself in: the helper is a different object, and does not know which order it is helping.

## 9. The Bill

Last, the bill. One total made three calls to helpers, where inheritance made none: one more hop for every helper. To look like a helper with four methods, the order had to write four forwarding methods that only pass the call on. And a helper knows nothing of its owner unless it is told.

## 10. How To Recognise It

How do you recognise this in code you did not write? A field of an interface type, and a method that just calls it. Strategy, State, Decorator and Proxy, which are all delegation with a purpose. Kotlin's by keyword, and Lombok's @Delegate. Collections.unmodifiableList, which hands each call to a list it holds.

## 11. The Verdict

Here is my verdict, plainly. Prefer holding a helper to inheriting from a parent, when what varies is one job. Pass the owner in if the helper needs it. Let the helper be swapped, and combined. Accept the extra hop, and the forwarding code, or use a language feature that writes it for you.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If there is one fixed way of doing a job, do it directly. Delegation pays off when a job varies, or must change at run time.

## 14. Thanks for Watching

That's Delegation. If you take one sentence away, take this one: delegation hands a job to a helper you can swap and combine, and the price is an extra call, and the forwarding code you must write. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a fourth rule that adds a shipping fee, and combine it with premium without adding a class. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
