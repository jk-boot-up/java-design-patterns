# Service Locator Pattern — Video Narration Script

## 1. Service Locator

Hello, and welcome. This video explains the Service Locator pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a service locator is a middleman. You ask it for what you need, and it finds it, or creates it. This is the fourth project in the foundational category, and the second of three that answer one question: how does an object get hold of what it needs? The last video showed a registry, a bag of things someone remembered to put in. This one adds a middleman. The next one stops the asking. All three use the same three collaborators in our online store. Service Locator is widely called an anti-pattern. I will show you why, with evidence. But I will also be fair, because it was a reasonable answer to a real problem, and there are places it is still right.

## 2. The Scenario

Here is the scenario. The same checkout, with the same three collaborators. And the registry's problems are now felt: dependencies you cannot see, and state shared between tests. Can a smarter middleman fix them?

## 3. The Advance: Recipes

Here is what a locator does better than a registry. A registry holds things. A locator holds recipes for making them. Before anything is asked for, nothing has been made. Ask three times for the gateway, configured as a singleton: it is made once. Ask three times for the notifier, configured as a prototype: it is made three times. It creates lazily, and it decides how long each thing lives. A registry can do neither.

## 4. The Other Advance: Swap For A Test

The second advance. Configure a fake gateway, and the same checkout charges the fake. No change to the checkout at all. That is a genuine step forward, and I want to say so. Service Locator was a real answer to a real problem.

## 5. The Bill: The Compiler Says Nothing

Now the bill, as evidence. Production is configured, and somebody forgets the notifier. New locator checkout compiles. It constructs. The build is green. Nothing anywhere complains. Then a real order arrives. The checkout asks for the discount policy, and gets it. It asks for the gateway, and charges the customer. Then it asks for the notifier, and there is no recipe. It fails. The customer has already been charged. The failure arrived in production, after the money moved, not in the build.

## 6. The Bill: Every Class Depends On It

Second cost. Every class that needs a collaborator now depends on the locator. Here, three of them: the auditor, the checkout, and the receipt printer. Each is otherwise pure domain logic, now coupled to infrastructure. And a unit test of any of them must configure the locator first, or it fails. A unit test that needs global set-up is never quite a unit test.

## 7. Where It Is Still Right

Now to be fair. There is a place this pattern is still right. A plug-in system, where what is available is genuinely not known until run time. Java has one built in: service loader. It found two payment plug-ins, card, and bank transfer, listed in a file. The application could not have known about them in advance. Asking is the whole point. Service loader is this pattern, in the standard library, and it is nobody's mistake.

## 8. The Verdict

My verdict, plainly. For business logic, prefer the alternative: do not ask, be given. Keep a locator for plug-in systems, and for the composition root of a small application, the one place that wires things together.

## 9. The Word Is Ask

The whole difficulty is one word. Ask. The class asks, so nobody outside it knows what it needs. Not the compiler, not the constructor, not the person writing a test. The next video removes the asking.

## 10. How To Recognise It

How do you recognise this in code you did not write? The words find, lookup, get bean, or resolve, called from inside business classes. Service loader, or a J N D I lookup. Get bean, inside a class that is itself a bean: a locator, inside a container. And the giveaway: a class with a no-argument constructor, that plainly needs several things to work.

## 11. What Is Real Here

The same honest admission as everywhere in this course. It is all plain Java. Service loader is the real one from the standard library. The forgotten notifier is simulated, but it happens exactly this way in real projects.

## 12. When This Is Too Much

So when is it too much? For business logic. It is right for plug-ins, and for the composition root.

## 13. Thanks for Watching

That's the Service Locator. If you take one sentence away, take this one: the word that matters is ask, because a class that asks hides what it needs from everyone who is not inside it. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a third plug-in to the services file, and run act five. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
