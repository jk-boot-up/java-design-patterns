# Value Object Pattern — Video Narration Script

## 1. Value Object

Hello, and welcome. This video explains the Value Object pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a value object is a small object that is defined entirely by what it holds, is never changed after it is made, and cannot be made wrong in the first place. This is the first project in the domain-driven design category, whose subject is writing code that says what the business says. In our online store, the first thing to get right is money. By the end you will see money as a bare number go wrong four ways, then see one small type close every one of them, and hear when I would not use it.

## 2. The Scenario

Here is the scenario. The online store adds up prices, in pounds and in dollars. It shares a bill between people, and it stores each customer's email address. The question: what should a price be? A number? A number and a string? Or something of its own?

## 3. Money As A Double

First, money as a double. Three stamps at one pound ten come to three point three, followed by a long tail of zeros and a three. Point one plus point two is not point three. And ten pounds added to ten dollars comes to twenty, with no complaint at all. The number has no idea what it is a number of.

## 4. The Pattern

The pattern. A money object that holds whole pence and a currency, together, as one thing. It never changes: every operation returns a new one. It refuses to be built wrong. And it refuses to be added to money in another currency. Everything else in this video is a consequence of those four sentences.

## 5. Money As A Value

Second, the same sum with a value. Whole pence, times three, is exactly three pounds thirty. And ten pounds plus ten dollars is refused, with a message that says why. The amount and its currency travel together, so they cannot be separated.

## 6. Equal By Value

Third, equality. Three separate objects, each five pounds, in a set. The set holds one, because a value object is equal to any other with the same contents. A class that compares by identity keeps all three. And five pounds is not equal to five dollars, as it should be.

## 7. Never Changed

Fourth, never changed. Two orders share one price object, and it can be changed. Order B takes five pounds off. Order A now costs fifteen pounds, and nobody touched order A. With values, order B's discount makes a new amount. Order A still pays twenty pounds. Sharing is safe, because nothing can change.

## 8. Valid From The Start

Fifth, valid from the start. Three methods take an email as a string. Two check it. The third, written last, does not, and a bad address is stored. An email address type checks once, when it is made. If you are holding one, it is valid. No method that receives one ever needs to check again. That is the same lesson as the null object.

## 9. Splitting Is A Decision

Last, splitting. Ten pounds three ways, rounded, is three thirty three, three times, which is nine ninety nine. A penny vanished. Allocation gives the odd penny to the first share. Three thirty four, three thirty three, three thirty three, which is exactly ten pounds. Somebody has to decide who gets the odd penny. Now that rule lives in one place.

## 10. How To Recognise It

How do you recognise this in code you did not write? A record, or a final class, with no setters. A constructor that throws on bad input. Methods that return a new instance, such as plus, or with name. And the Java time classes and big decimal, which are value objects the language gave you.

## 11. The Verdict

Here is my verdict, plainly. Use a value object where a raw type hides a meaning: money, an email address, a date range, a quantity with a unit. Make it a record, check it in the constructor, and give it the operations that belong to it. And do not wrap every string.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. The floating point error and the lost penny are real output, not staged. Nothing here uses a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a value that means nothing beyond its raw type, like a loop counter, a wrapper is noise. It earns its place where mistakes are expensive, and where rules exist.

## 14. Thanks for Watching

That's Value Object. If you take one sentence away, take this one: a value object makes the wrong thing impossible to say, instead of something every caller must remember to avoid. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, write a quantity type that refuses a negative number. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
