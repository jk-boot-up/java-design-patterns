# Singleton Pattern Pattern — Video Narration Script

## 1. Singleton Pattern

Hello, and welcome. This video explains the Singleton pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Singleton pattern guarantees that a class has exactly one instance. And it gives every caller one well-known way to reach it. The class controls its own creation, so no matter how you ask, you cannot get a second one. Think of a country's official clock. Everyone sets their watch from the same one. Two official clocks would cause confusion. In this video, we build an order number generator for an online store. And we will watch a private constructor get called anyway, twice, by two tricks. Then we will see the one Java shape that stops both.

## 2. The Job

Here is the job. Every checkout in our store needs an order number. Order one, order two, order three, and so on. In strict sequence, with no gaps, and no repeats. Checkout creates order numbers. So does the admin console, when support staff raise an order by hand. So does a background job, retrying a failed payment. All three must use the same counter. Otherwise, two different customers could receive the same order number.

## 3. An Instance Per Caller

Here is a reasonable-looking generator class. It holds a counter, and each call adds one, and returns the next order number. The problem appears when two parts of the system each create their own generator. Checkout creates one, and the admin console creates another. Each one starts its own counter at zero. So both hand out order number one. The class itself is fine. The bug is that anyone can create as many as they like, when the rule is exactly one.

## 4. The Classic Fix

The textbook fix takes creation away from callers. Make the constructor private. Keep the one instance in a static field. And add a public method, called get instance, that returns it. Now every caller goes through get instance. And in normal use, it really does return the same object every time. Private means private. Or does it?

## 5. Breaking It: Reflection

First trick: reflection. Java's reflection features can find a private constructor, switch off its protection, and call it. And it simply works. A second generator now exists, separate from the shared one. Private is a rule the compiler checks. It is not something Java enforces while the program runs. Frameworks and testing tools use this very trick, for good reasons, without asking the class.

## 6. Breaking It: Serialization

Second trick, with no reflection needed. Java's built-in serialization can save an object as bytes, and rebuild it later. And when it rebuilds, it never calls a constructor. So save the shared generator, and read it back. What comes back is a brand new object, with its counter reset to zero. Silently. Two separate holes, in a class written specifically to prevent a second instance.

## 7. The Singleton Pattern

Here is the pattern's definition, from the famous Gang of Four book. Ensure a class has only one instance, and provide a global point of access to it. In plain words: make it impossible to create more than one. And give every caller the same, well-known way to reach it. The real question this project answers is: which Java shape truly makes a second one impossible? And which shapes only look like they do?

## 8. The Shape of It

Here is the shape of the answer. The order number generator becomes an enum, with a single value, called INSTANCE. Java creates that value exactly once, when the class is loaded, before any caller can even reach it. That gives three guarantees, for free. Loading a class is thread-safe, by Java's own rules. Reflection is forbidden from creating enum values. And reading an enum back from bytes returns the existing value, not a new one.

## 9. One Constant, Three Guarantees

That is the entire singleton. An enum with one value, holding a counter, and a method that returns the next order number. No private constructor to remember. No get instance method. No null check. No lock. Try the reflection trick, and Java refuses outright: it cannot reflectively create enum objects. Try the serialization trick, and you get back the very same instance. Because Java saves an enum by its name, not by its fields.

## 10. Why AtomicLong

One more detail, which only matters once there truly is one instance. Now every thread in the program can reach that one generator, at the same time. So its counter must be safe to change from many threads. Adding one to a plain number is really two steps: read it, then write it. Two threads can both read the same value, and one increase is lost. So the counter is an Atomic Long. Its increment is one indivisible step. So no two callers can ever get the same order number.

## 11. Running It

Let's run the demo. The enum hands out order one, then order two. The reflection trick is rejected, with a clear error. And after saving and reading back, it is still the exact same instance. Then the classic private-constructor version. In normal use, it looks identical. But it falls to both tricks. The same two tricks, used against two classes that look identical from outside, with opposite results.

## 12. Where It Stops

Now the honest part. This pattern has real limits. A singleton is global, changeable state, with a pattern name. Any code anywhere can reach it. And there is no clean way to give each test its own counter. It also hides a dependency. A method that uses the singleton inside its body does not show that in its parameters. And if the business later needs a separate sequence for each shop, or each warehouse, exactly one for the whole program is the wrong promise. Then the pattern itself has to go. Use it only when the business truly requires exactly one.

## 13. How It Relates to the Others

So how does the Singleton relate to the other creational patterns? Prototype answers: I have one, get me another. Builder answers: which pieces, in what order. Abstract Factory answers: which whole matching set. Singleton is the odd one out. It says nothing about how an object is built. It only controls how many exist. It is also often used to solve a different problem: I do not want to pass this object around. Dependency injection solves that, without the cost of global state.

## 14. One Sentence to Keep

If you keep one sentence from this video, keep this one. A private constructor is a promise the compiler checks, not one Java enforces while the program runs. A single-value enum is the one Java singleton shape that closes both holes, for free. The project has full notes, an animated walkthrough, and a teaching plan. Try adding a read resolve method to the classic version. And listen for which one of the two tricks stops working.

## 15. Thanks for Watching

That's the Singleton pattern. The full source code, written notes, and diagrams are all in the repository. If there is a pattern you would like to see covered, suggest it in the comments. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
