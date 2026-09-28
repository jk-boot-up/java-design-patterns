# Value Object Pattern — Video Narration Script

## 1. Value Object

Hello, and welcome. This video explains the Value Object pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A value object is a small object defined entirely by what it holds. It never changes after it is made. And it cannot be made wrong in the first place. Think of a banknote. One ten pound note is as good as any other ten pound note. You do not care which one you hold, only what it is worth. In our online store, the first thing to get right is money. In this video, money as a bare number goes wrong in four ways. Then one small type fixes every one of them. And we will hear when not to use it.

## 2. The Scenario

Here is the scenario. The online store adds up prices, in pounds, and in dollars. It splits a bill between several people. And it stores each customer's email address. So here is the question. What should a price be? A number? A number and some text? Or something of its own?

## 3. Money As A Double

First, money as a plain decimal number, a double. Three stamps at one pound ten each should cost three pounds thirty. But the result is three point three, followed by a long tail of zeros and a three. Point one plus point two is not exactly point three. And ten pounds plus ten dollars comes to twenty, with no complaint at all. The number has no idea what it is a number of.

## 4. The Pattern

Now, the pattern. A Money object that holds whole pence, and a currency, together, as one thing. It never changes. Every operation returns a new Money. It refuses to be created with bad data. And it refuses to be added to money in another currency. Everything else in this video follows from those four rules.

## 5. Money As A Value

Second demo: the same sums, with a value object. One hundred and ten pence, times three, is exactly three pounds thirty. And ten pounds plus ten dollars is refused. The message says: cannot combine pounds with dollars. The amount and its currency travel together, so they can never be separated.

## 6. Equal By Value

Third demo: equal by value. Three separate Money objects, each worth five pounds, are put into a set. The set holds just one. Because a value object is equal to any other with the same contents. A class that compares objects by identity would keep all three. And five pounds is not equal to five dollars, exactly as it should be.

## 7. Never Changed

Fourth demo: never changed. Two orders share one price object, and that object can be changed. Order B takes five pounds off. Now order A costs fifteen pounds too, and nobody touched order A. With value objects, order B's discount creates a new amount. Order A still costs twenty pounds. Sharing is safe, because nothing can change.

## 8. Valid From The Start

Fifth demo: valid from the start. Three methods receive an email address as plain text. Two of them check it. The third, written last, does not. So a bad address gets stored. An Email Address type checks the address once, when it is created. If you are holding one, it is valid. No method that receives one ever needs to check it again.

## 9. Splitting Is A Decision

Last demo: splitting is a decision. Split ten pounds three ways, rounding each share. You get three pounds thirty-three, three times. That adds up to nine ninety-nine. A penny has vanished. Money's allocate method gives the odd penny to the first share. Three thirty-four, three thirty-three, and three thirty-three. Exactly ten pounds. Someone has to decide who gets the odd penny. Now that rule lives in one place.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a record, or a final class, with no setters. A constructor that throws an error on bad input. Methods that return a new object, such as plus, or with name. And Java's own date and time classes, and Big Decimal, which are value objects built into the language.

## 11. The Verdict

So, here is the verdict. Use a value object wherever a plain type hides a meaning. Money, an email address, a date range, or a quantity with a unit. Make it a record. Check its data in the constructor. And give it the operations that belong to it. But do not wrap every string.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. The decimal error, and the lost penny, are real output, not staged. And nothing here uses the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a value that means nothing beyond its plain type, like a loop counter, a wrapper is just noise. A value object earns its place where mistakes are expensive, and where rules exist.

## 14. Thanks for Watching

That's the Value Object pattern. If you remember one sentence, make it this one. A value object makes the wrong thing impossible to say, instead of something every caller must remember to avoid. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Write a Quantity type. And make it refuse a negative number. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
