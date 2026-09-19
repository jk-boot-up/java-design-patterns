# Registry Pattern — Video Narration Script

## 1. Registry

Hello, and welcome. This video explains the Registry pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a registry is a well-known place where things are kept, so any object can find what it needs by asking. This is the third project in the foundational category, and the first of three that answer one question: how does an object get hold of what it needs? Registry is a well-known place. The next video, on Service Locator, adds a middleman. The one after, on Dependency Injection, stops the asking altogether. All three use the same three collaborators in our online store, a discount policy, a payment gateway and a notifier, so you can compare them. By the end you will see why a registry is a global variable with better manners, with evidence.

## 2. The Scenario

Here is the scenario. The checkout needs three things: a discount policy, a payment gateway, and a notifier. And the payment gateway is needed six classes down from where the checkout starts. How does it get there?

## 3. Pass It Down

The plain answer: pass it down. The gateway goes into the storefront, which passes it to the cart service, which passes it to the order coordinator, the pricing stage, the payment stage, and finally the charger. Six constructors. Only the last one uses it. The other five forward it. I want to be fair to this. It is real friction, and anyone who says otherwise has not had to add a parameter to six constructors. But it is also honest. Every dependency is visible, in a signature.

## 4. The Pattern

The pattern: a well-known object that others find things in. Registry dot get, payment gateway. From anywhere. The six constructors collapse. The checkout's constructor takes nothing at all. The friction is gone.

## 5. It Works

And it works. The registry checkout takes nothing in its constructor. It asks the registry for the discount policy, the gateway and the notifier, when it needs them. Six constructors became none. And that is exactly where the trouble starts.

## 6. The Bill: Invisible

First cost. The dependencies become invisible. New registry checkout compiles, and constructs, and looks perfectly fine. Its signature says it needs nothing. Then the first call fails: nothing is registered for discount policy. Three things had to be registered first, and nothing in the class says so. The compiler could not tell you. Neither could the constructor.

## 7. The Bill: Order Dependence

Second cost, and the one teams meet first. Two tests share the registry. One leaves a gateway behind, with a charge already on it. The other expects exactly one charge in total. In one order, both pass. In the other order, the second test fails: it saw two charges. Neither test changed. The order they ran in did. This is the kind of failure that costs a team a day, and it comes from global state.

## 8. The Bill: What Is In It?

Third cost. What is in the registry, right now? At start-up, nothing. After one class ran, the discount policy. After two more, all three. That answer is not in any one file. It depends on what has run, and in what order. And it is a static map, shared by every thread, so thread safety is now a question too.

## 9. Where A Registry Is Right

Is there a place where a registry is the right answer? Yes. A very small number of things that are truly application-wide, set up once at start-up, and never changed. Not collaborators that vary. Not anything a test needs to replace.

## 10. The Verdict

My verdict, plainly. Use a registry narrowly. For a very few application-wide things, set up once. Not for the collaborators of your business logic, and not for anything a test must replace. And the problem it leaves, invisible dependencies, is what the next video tries to fix, with a middleman that can find and create things.

## 11. How To Recognise It

How do you recognise this in code you did not write? A class with static get, lookup, or get instance methods, keyed by type or by name. System dot get properties. Locale dot get default. A context object passed everywhere. And the giveaway: a before each method that clears something static, because tests were leaking into each other.

## 12. What Is Real Here

The same honest admission as everywhere in this course. It is all plain Java. The two orders are simulated by running two test bodies, in each order, against one shared registry. But the failure is exactly the real one, and it is in the project's own tests.

## 13. When This Is Too Much

So when is a registry too much? For nearly everything that is not truly application-wide.

## 14. Thanks for Watching

That's the Registry. If you take one sentence away, take this one: a registry removes the friction of passing things down, and pays for it by hiding what every class needs. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, run the two tests in both orders yourself, and see which one fails. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
