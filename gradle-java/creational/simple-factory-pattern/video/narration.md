# The Simple Factory Pattern Pattern — Video Narration Script

## 1. The Simple Factory Pattern

Hello, and welcome. This video explains the Simple Factory pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A simple factory is one place that decides which class to create. Instead of every caller choosing a class for itself, callers hand over a piece of data, like a name or a code. And they get back an object, behind an interface they already know. The decision is made once, in one file, instead of everywhere. Think of a coffee shop counter. You say, a cappuccino, please, and one arrives. You never go behind the counter to make it yourself. In this video, we build the payment step of an online store. By the end, you will know what a factory is, why it exists, and how to write one yourself.

## 2. The Scenario

Here is the scenario. A customer reaches the payment page, and chooses how to pay. Our code must then run one of four things. A credit card payment. A U P I payment, which is India's instant bank transfer. A PayPal payment. Or net banking. And here is the key detail. That choice arrives as data. From a drop-down list, a web request, or a database. It is a piece of text, or an enum value. Not a Java class.

## 3. One Interface, Four Implementations

All four payment methods do the same job, from the outside. They take a payment request, and return a receipt. So they share one interface, called Payment Method, with two methods. One gives its display name. The other takes the payment. Inside, they are completely different. The card payment authorises, and then captures the money. The U P I payment sends a collect request, and waits for approval. But from the outside, they are interchangeable. And that makes everything else in this video possible.

## 4. The Problem — Everyone Chooses for Themselves

Here is the problem. Without a factory, every piece of code that needs a payment method chooses one for itself. A chain of if statements checks the payment type, and creates the matching class. That chain lives inside the checkout code. The website has a copy. The mobile app has a copy. The admin tool has a copy. The same fragile block, written three times, by three people, on three different days.

## 5. Why That Hurts

And that does real damage. The checkout code now knows the name of every payment class in the system. When wallet payments arrive next month, every copy must be found and edited. Miss one, and it fails in front of a customer. One copy trims extra spaces from the input. Another forgets. And you cannot test the choosing on its own, because it is welded to the checkout code around it.

## 6. The Simple Factory

The simple factory fixes exactly this. It puts the decision about which class to create into one method. So callers can ask for an object by name, instead of building it themselves. One quick note, because this confuses everybody at first. The simple factory is not one of the twenty-three Gang of Four patterns. It is an everyday idiom, the one everybody actually writes. And it is the natural first step towards the other creational patterns. In plain words: one place that knows how to make things.

## 7. Remember It With a Coffee Shop

Here is an easy way to remember it: a coffee shop. You do not walk behind the counter, find the espresso machine, grind the beans, and steam the milk. You say, a cappuccino, please. And a cappuccino arrives. You named what you wanted. Someone else knew how to make it. And tomorrow, when the shop buys a better machine, your order does not change at all. Because you never knew how it was made. The counter is the factory.

## 8. The Four Roles

Every factory has four roles. First, the product: the Payment Method interface. Second, the concrete products: the four payment classes. Third, the factory itself: the Payment Method Factory. And fourth, the client: the code that simply wants to take a payment. Now the most important idea in the whole video. The client names the payment type, as data. The factory names the class. Search the client code for the words credit card payment. You will not find them anywhere. That is how you know the pattern has really been applied.

## 9. A Product — Small, Focused, Unaware

Let's look at one product: the U P I payment. Notice how small, and ordinary, it is. It gives its display name, and it takes the payment. That is all. It has no idea a factory exists. That is deliberate. Because it knows nothing about who created it, you could move this class into a completely different application tomorrow. The other three payment methods follow exactly the same shape.

## 10. The Factory — One Switch, One Place

And here is the factory itself. One static method, called create, with one switch statement. It is now the only place in the whole codebase that creates a payment class. Notice something missing from that switch. There is no default branch. And that is on purpose. The payment type is an enum, and the Payment Method interface is sealed. So the compiler knows the complete list of cases. Add a fifth payment type tomorrow, and this file will not compile until you handle it. A forgotten case becomes a build error, instead of a customer complaint.

## 11. What the Factory Gives You

So the factory gives us three things. It chooses the class from data, in exactly one place. It creates the object, so no caller ever writes new. And it checks the input, so every caller gets the same error message. Now, let's be honest about the cost. Adding a new payment method means editing the factory. That breaks the Open Closed Principle, which says code should be open to extension, but closed to modification. The simple factory does not remove that cost. It just moves it into one file you can actually find.

## 12. The Client — This Is the Whole Thing

And now, the payoff: the client code. One line asks the factory for a payment method. After that, it is ordinary, everyday polymorphism. The checkout does not know that PayPal exists. It does not know net banking exists. It holds a Payment Method, and simply calls pay. Add a fifth payment method tomorrow, and this code does not change at all. That is the whole point of the pattern.

## 13. Running It

Let's run the demo. Two of the four payments run, for the same order. Listen to the checkout's lines, the first and the last of each payment. They are identical. Paying with, and then, done. Only the lines in between are different. The card authorises and captures. The U P I payment sends a collect request, and the customer approves it. The same client code, running completely different payment methods, chosen by nothing more than a value.

## 14. Wrap Up

So, to recap. Use a simple factory when the class you need is decided by data. And when callers should not care how it is built. Keep the factory thin. Its job is to choose, and to create. Nothing else. If there is only one implementation, just use new. It is clearer. And if you ever reach forty cases, use a registry instead. And one sentence to remember. A simple factory chooses with a switch. A factory method chooses with inheritance.

## 15. Thanks for Watching

That's the Simple Factory pattern. If you remember one sentence, make it this one. Put the choice of which class to create in one place, and let callers ask for it by name. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. If there is a pattern you would like to see covered, suggest it in the comments. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
