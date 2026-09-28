# Registry Pattern — Video Narration Script

## 1. Registry

Hello, and welcome. This video explains the Registry pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A registry is a well-known place where things are kept. So any object can find what it needs, just by asking. Think of a noticeboard in an office. Anyone can walk up and read the phone number they need. But nobody knows who pinned what, or when. This is one of three related patterns that answer one question. How does an object get hold of what it needs? The others are Service Locator, and Dependency Injection, each with its own video. In our online store, the checkout needs a discount policy, a payment gateway, and a notifier. By the end, you will hear, with evidence, why a registry is a global variable with better manners.

## 2. The Scenario

Here is the scenario. The checkout needs three helpers. A discount policy, a payment gateway, and a notifier. And the payment gateway is needed six classes down, from where the checkout starts. So here is the question. How does it get there?

## 3. Pass It Down

First, the plain answer: pass it down. The gateway goes into the storefront. The storefront passes it to the cart service. Then to the order coordinator, the pricing stage, the payment stage, and finally the charger. Six constructors. Only the last one actually uses it. The other five just pass it along. To be fair, that is real friction. But it is also honest. Every dependency is visible, in a constructor.

## 4. The Pattern

Now, the pattern. A well-known object that others can find things in. Registry dot get, payment gateway. From anywhere in the code. The six constructors collapse. The checkout's constructor takes nothing at all. The friction is gone.

## 5. It Works

Second demo: it works. The registry checkout takes nothing in its constructor. It asks the registry for the discount policy, the gateway, and the notifier, whenever it needs them. Six constructors became none. And that is exactly where the trouble starts.

## 6. The Bill: Invisible

Third demo: the first cost, invisible dependencies. Creating a registry checkout compiles, and looks perfectly fine. Its constructor says it needs nothing. Then the first call fails. Nothing is registered for the discount policy. Three things had to be registered first. And nothing in the class says so. The compiler could not tell you, and neither could the constructor.

## 7. The Bill: Order Dependence

Fourth demo: the second cost, and the one teams meet first. Two tests share the registry. One leaves a gateway behind, with a charge already on it. The other expects exactly one charge in total. Run them in one order, and both pass. Run them in the other order, and the second test fails, because it saw two charges. Neither test changed. Only the order they ran in did. This kind of failure can cost a team a whole day. And it comes from shared, global state.

## 8. The Bill: What Is In It?

Fifth demo: the third cost. What is in the registry, right now? At start-up: nothing. After one class has run: the discount policy. After two more: all three. That answer is not written in any one file. It depends on what has run, and in what order. And the registry is shared by every thread, so thread safety becomes a question too.

## 9. Where A Registry Is Right

So, is a registry ever the right answer? Yes. For a very small number of things that are truly application-wide. Set up once, at start-up, and never changed. But not for helpers that vary. And not for anything a test needs to replace.

## 10. The Verdict

So, here is the verdict. Use a registry narrowly. For a very few application-wide things, set up once. Not for the helpers of your business logic. And not for anything a test must replace. The problem it leaves, invisible dependencies, is what the Service Locator pattern tries to fix.

## 11. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a class with static get, lookup, or get instance methods, keyed by type or by name. In Java itself, System get properties, and Locale get default. Look for a context object passed everywhere. And the giveaway: a test setup method that clears something static, because tests were leaking into each other.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. The two test orders are simulated, by running two tests in each order, against one shared registry. But the failure is exactly the real one. And it is in the project's own tests.

## 13. When This Is Too Much

So, when is a registry too much? For nearly everything that is not truly application-wide.

## 14. Thanks for Watching

That's the Registry pattern. If you remember one sentence, make it this one. A registry removes the friction of passing things down, and pays for it by hiding what every class needs. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Run the two tests in both orders yourself. And see which one fails. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
