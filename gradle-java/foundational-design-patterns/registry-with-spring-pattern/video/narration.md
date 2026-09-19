# Registry with Spring Pattern — Video Narration Script

## 1. Registry with Spring

Hello, and welcome. This video explains the Registry pattern with Spring, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Registry video. That one built a registry by hand, and showed its costs. Spring's application context is a registry too, built far better. The plain definition, in short: a well-known place where things are kept, found by asking. By the end you will see what Spring fixes about the hand-built registry, when asking it is a mistake, and the failure that is Spring's own: a cached context that remembers what earlier tests did.

## 2. The Partner Project

This video assumes the Registry video. If you have not seen it, start there. It builds a registry by hand, and shows four costs, among them invisible dependencies, and a test that fails because of the order the tests ran in. This one uses the same checkout. It does not teach the pattern again. It shows what Spring does with it.

## 3. Before The First Annotation

Before the first annotation, one new thing. Spring's core is a container, called the application context. It creates your objects, and lets you find them by type. That is a registry. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. The Context Is The Registry

Here is the first thing to see. Registry dot get, from the hand-built video, is context dot get bean here. It found the recording gateway. But look at what changed. Nothing is registered by calling a method, from somewhere. Things are registered by declaration: a component annotation on a class. And a missing bean fails when the context starts, not on the first call.

## 5. Used Well, Or Badly

Now two ways to use it. The injected checkout is given its collaborators, and never calls the registry at all. That is the best use of a registry: never calling it. The other checkout calls get bean, three times. Same result. But its constructor takes nothing, its dependencies are invisible again, and constructing one with new throws a null pointer exception, because it needs Spring to hand it the context. That is the hand-built registry, inside Spring. A get bean inside a business class is a service locator.

## 6. The Failure Of Its Own

Now the failure of Spring's own. Spring's test support caches a context, and reuses it across tests with the same configuration. Starting Spring is slow, so it is a sensible thing to do. But the gateway is a singleton, so it remembers. Test A charges it once. Test B, on the same cached context, starts by expecting a clean gateway. It sees nine thousand. That is the hand-built registry's order-dependent test failure, in Spring. This project's own tests prove it: the second test passes only because the first ran before it. Run alone, it would fail. The fix is to throw the context away, which is correct, and costs a new context.

## 7. A Registry Of Strings

Spring has a second registry, and this one is of strings: the environment. Ask it for checkout currency, and you get pounds. Ask with a typo, checkout curency, and you get null. No error. No warning. A required value with the same typo, injected, fails when the context starts: could not resolve placeholder. The untyped lookup is silent. The injected one is not.

## 8. Two Of A Type

One more. Ask the registry for the notifier, by type, when there are two. No unique bean definition exception. Two beans found. It is a run-time error, at the call site, not a compile error. Asking by type is only unambiguous until the second one arrives.

## 9. The Verdict

My verdict, plainly. Spring's context is the registry, done well: declared, checked at start-up, and mostly never called. In business code, inject. Keep get bean to main, to tests, and to framework glue. And keep singleton state out of anything that tests share.

## 10. Where You Have Met This

You have met this. Every autowired lookup goes through it. And every Spring boot test shares one, unless you ask it not to.

## 11. What Was Used

For the record. Spring Boot four point one point one. No web server, no database, and no web starter.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: the context, its errors, and the test cache. The tests in the project run the leak on real Spring.

## 13. When This Is Too Much

So when is it too much? Never, for the context itself: you already have one. The cost is in calling it.

## 14. Thanks for Watching

That's the Registry with Spring. If you take one sentence away, take this one: the registry done well is one you rarely call, and even then, whatever it holds is shared. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, run only the second leak test, on its own, and watch it fail. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
