# Simple Factory Pattern — Narration Script

The full spoken script for `simple-factory-pattern-explained.mp4`, scene by
scene. This is the human-readable copy used for review; the authoritative
text lives next to each slide in [`scenes.py`](scenes.py). If you change the
wording there, update this file too.

- **Voice:** macOS `Samantha` (female, US English) at 170 words per minute
- **Runtime:** approximately 6 minutes
- **Audience:** beginners with no prior design-pattern knowledge

A note on spelling: a few words are written the way they should be *spoken*
rather than the way they are written in code — "U P I" instead of "UPI",
"pay pal" instead of "PayPal" — because the speech synthesiser mangles them
otherwise. Keep that habit if you edit the script.

## 1. The Simple Factory Pattern

Hello, and welcome. In this short video we are going to learn the pattern that almost every Java developer writes before they know it has a name: the Simple Factory. We will learn it by building a real, working Java project, the payment step of an online store. By the end you will know what a factory is, why it exists, and how to write one yourself.

## 2. The Scenario

Imagine you are building an online store. A customer reaches the payment page and chooses how they want to pay. Your code now has to run one of four things: a credit card payment, a U P I payment, a pay pal payment, or net banking. And here is the important detail. That choice arrives as data. It comes from a dropdown, or a JSON field, or a database column. It is a string or an enum. It is not a Java type.

## 3. One Interface, Four Implementations

In our project all four do the same job from the outside. They take a payment request and give back a payment receipt. So they share one interface, called Payment Method, with two methods on it. Inside, they are completely different. The card one authorises and then captures. The U P I one sends a collect request and waits. But from the outside they are interchangeable, and that is what makes everything else possible.

## 4. The Problem — Everyone Chooses for Themselves

So here is the problem. Without a factory, whoever needs a payment method decides for themselves. This chain of if and else lives inside the checkout code. Our website has a copy. Our mobile app has a copy. Our admin tool has a copy. The same fragile block, written three times, by three people, on three different days.

## 5. Why That Hurts

This causes real damage. A class whose only job is to check out now knows the name of every payment class in the system. When we add wallet payments next month, we have to find every caller and edit it, and if we miss one it fails in front of a customer. One copy trims the input string, another forgets. And you cannot test the choosing logic on its own, because it is welded to the checkout code around it.

## 6. The Simple Factory

The Simple Factory solves exactly this. It puts the decision of which class to instantiate into one method, so callers can ask for an object by name instead of building it themselves. One quick note, because it confuses everybody at first. Simple Factory is not one of the twenty three Gang of Four patterns. It is an idiom, the one everybody actually writes, and it is the natural first step towards the real creational patterns. In plain language, it is one place that knows how to make things.

## 7. Remember It With a Coffee Shop

Here is the way to remember it forever. Think about a coffee shop. You do not walk behind the counter, find the espresso machine, grind the beans and steam the milk. You say, a cappuccino please, and a cappuccino arrives. You named what you wanted. Somebody else knew how to make it. And tomorrow, when the shop buys a better machine, your order does not change at all, because you never knew how it was made. The counter is the factory.

## 8. The Four Roles

Every factory has four roles. First, the product, which is our Payment Method interface. Second, the concrete products, our four payment classes. Third, the factory itself, which in our project is the Payment Method Factory. And fourth, the client, the code that just wants to take a payment. Now here is the single most important idea in this whole video. The client names the type as data. The factory names the class. Search the client for the words credit card payment and you will not find them anywhere. That is the test of whether you have applied the pattern correctly.

## 9. A Product — Small, Focused, Unaware

Let's look at some code. This is the U P I payment. Notice how small and how ordinary it is. It gives its display name, and it takes the payment. It has absolutely no idea that a factory exists. That is deliberate. Because it knows nothing about who created it, you could lift this class into a completely different application tomorrow. The other three payment methods follow exactly the same shape.

## 10. The Factory — One Switch, One Place

And this is the factory itself. One static method, one switch. This is now the only place in the entire codebase that calls new on a payment class. Look carefully at that switch, because there is something missing. There is no default branch. That is deliberate. Payment Type is an enum and Payment Method is a sealed interface, so the compiler knows the complete list, and it knows this switch covers every case. Add a fifth payment type tomorrow, and this file stops compiling until you handle it. A forgotten case becomes a build error instead of a customer complaint.

## 11. What the Factory Gives You

So the factory is giving us three things. It chooses the implementation from data, in exactly one place. It constructs it, so no caller ever writes new. And it validates the input, so every caller gets the same error message. Now let's be honest about the cost, because every good teacher should be. Adding a new payment method means modifying the factory. That breaks the Open Closed Principle, which says code should be open to extension but closed to modification. The Simple Factory does not remove that cost. It centralises it, into one file you can find.

## 12. The Client — This Is the Whole Thing

And now the payoff. This is the entire client code. One line to obtain the object, and then ordinary, everyday polymorphism. Our checkout does not know that pay pal exists. It does not know that net banking exists. It holds something typed as Payment Method and it simply calls pay. If we add a fifth payment method tomorrow, this code does not change at all. That is the whole point of the pattern.

## 13. Running It

When we run the project, we can watch it happen. Here are two of the four payments. Look at the checkout lines, the first and the last of each block. They are identical. Only the middle lines, the ones the payment method itself printed, are different. That is the pattern working. The same client code, running completely different implementations, chosen by nothing more than a value.

## 14. Wrap Up

So, to recap. Use a Simple Factory when the class you need is decided by data, and you want to spare your callers from knowing how it is built. Keep the factory thin. Its job is to choose and construct, nothing else. If you only have one implementation, plain new is clearer, so do not invent a factory for its own sake. And if you ever reach forty cases, reach for a registry instead. If you remember just one sentence from today, make it this one: a Simple Factory chooses with a switch, and a Factory Method chooses with inheritance. That second one is where you go next. Thank you for watching, and enjoy building your own factories.

