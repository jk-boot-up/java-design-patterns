# Service Locator Pattern — Video Narration Script

## 1. Service Locator

Hello, and welcome. This video explains the Service Locator pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A service locator is a middleman. You ask it for what you need, and it finds it, or creates it. Think of a hotel concierge. You ask for a taxi, and the concierge arranges one. But nobody can tell, by looking at you, that you needed a taxi. This is one of three related patterns about how an object gets hold of what it needs. The others are Registry, and Dependency Injection, each with its own video. Service Locator is often called an anti-pattern. This video shows why, with evidence. But it is also fair, because it solved a real problem, and there are places where it is still right.

## 2. The Scenario

Here is the scenario. The same online checkout, with the same three helpers. A discount policy, a payment gateway, and a notifier. And the problems of a simple registry are now being felt. Dependencies you cannot see, and state shared between tests. So here is the question. Can a smarter middleman fix them?

## 3. The Advance: Recipes

First demo: the locator's first advance, recipes. A registry holds things. A locator holds recipes for making them. Before anything is asked for, nothing has been made. Ask three times for the gateway, set up as one shared instance. It is made once. Ask three times for the notifier, set up to be fresh each time. It is made three times. So it creates things only when needed, and decides how long each one lives. A registry can do neither.

## 4. The Other Advance: Swap For A Test

Second demo: the other advance, swapping for a test. Set up the locator with a fake gateway. And the very same checkout charges the fake one. With no change to the checkout at all. That is a genuine step forward. Service Locator was a real answer to a real problem.

## 5. The Bill: The Compiler Says Nothing

Third demo: now the cost, with evidence. Production is set up, but someone forgets the notifier. Creating a locator checkout compiles. It constructs. The build is green. Nothing anywhere complains. Then a real order arrives. The checkout asks for the discount policy, and gets it. It asks for the gateway, and charges the customer. Then it asks for the notifier, and there is no recipe. It fails. The customer has already been charged. The failure arrived in production, after the money moved, not in the build.

## 6. The Bill: Every Class Depends On It

Fourth demo: the second cost, every class depends on the locator. Here, three classes call the locator: the auditor, the checkout, and the receipt printer. Each one would otherwise be pure business logic. Now each is tied to infrastructure. And a unit test of any of them must set up the locator first, or it fails. A unit test that needs global setup is never quite a unit test.

## 7. Where It Is Still Right

Fifth demo: where this pattern is still right. A plug-in system, where what is available is genuinely not known until the program runs. Java has one built in, called Service Loader. It found two payment plug-ins: card, and bank transfer. Both listed in a small file. The application could not have known about them in advance. Here, asking is the whole point. Service Loader is this pattern, in Java's own library, and it is nobody's mistake.

## 8. The Verdict

So, here is the verdict. For business logic, prefer the alternative: do not ask, be given. Keep a locator for plug-in systems. And for the one place in a small application that wires everything together.

## 9. The Word Is Ask

The whole difficulty comes down to one word: ask. The class asks for what it needs. So nobody outside it knows what it needs. Not the compiler, not the constructor, and not the person writing a test. Dependency Injection, in its own video, removes the asking.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for words like find, lookup, get bean, or resolve, called from inside business classes. Look for Service Loader, or a J N D I lookup. Look for get bean, inside a class that Spring itself created. And the giveaway: a class with an empty constructor, that plainly needs several things to work.

## 11. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Service Loader is the real one, from Java's own library. The forgotten notifier is simulated, but it happens exactly this way in real projects.

## 12. When This Is Too Much

So, when is this too much? For business logic. It is right for plug-ins, and for the one place that wires the application together.

## 13. Thanks for Watching

That's the Service Locator pattern. If you remember one sentence, make it this one. The word that matters is ask, because a class that asks hides what it needs from everyone outside it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a third payment plug-in to the services file. Then run the plug-in demo again. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
