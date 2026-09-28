# Registry with Spring Pattern — Video Narration Script

## 1. Registry with Spring

Hello, and welcome. This video explains the Registry pattern, in Java, using Spring. This video is presented by Jayasekhar Konduru. First, a simple definition. A registry is a well-known place where things are kept, and found by asking. Think of a phone directory. Anyone can look up a number, but everyone shares the same book. This is the framework version of the Registry video. That one built a registry by hand, and showed its costs. Spring's application context is a registry too, but built far better. By the end, you will know what Spring fixes. When asking it for things is a mistake. And the failure that is Spring's own: a cached context that remembers what earlier tests did.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Registry video. That one builds a registry by hand, and shows its costs. Among them, invisible dependencies, and a test that fails depending on the order the tests run in. Here, we use the same checkout. We will not teach the pattern again. Instead, we ask what Spring does with it.

## 3. Before The First Annotation

One thing is new in this project: Spring Boot. Spring's core is a container, called the application context. It creates your objects, and lets you find them by type. That is a registry. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. The Context Is The Registry

First demo: the application context is the registry. Registry dot get, from the hand-built video, becomes context dot get bean here. And it finds the recording gateway. But notice what changed. Nothing is registered by calling a method, from somewhere. Things are registered by declaring them, with an at Component annotation on a class. And a missing object makes Spring fail when it starts, not on the first call.

## 5. Used Well, Or Badly

Second demo: using it well, or badly. The first checkout is given its helpers, through its constructor. It never asks the registry for anything. That is the best way to use a registry: never calling it. The second checkout calls get bean, three times. The result is the same. But its constructor takes nothing, so its needs are invisible again. And creating one with new throws a null pointer exception, because it needs Spring to give it the context. That is the hand-built registry again, inside Spring. A get bean call inside business code is really a service locator.

## 6. The Failure Of Its Own

Third demo: the failure that is Spring's own. Spring's test support caches a context, and reuses it for tests with the same setup. Starting Spring is slow, so this is sensible. But the gateway is a singleton, so it remembers. Test A charges it once, for ninety pounds. Test B, on the same cached context, expects a clean gateway. But it sees that ninety pound charge. That is the hand-built registry's test order problem, now in Spring. This project's tests prove it. The fix is to throw that context away, which is correct, but costs starting a new one.

## 7. A Registry Of Strings

Fourth demo: a registry of text values. Spring has a second registry: the environment, which holds settings as text. Ask it for checkout currency, and you get pounds. Ask with a typo, currency spelled with one r, and you get nothing. No error, and no warning. But a required setting injected with the same typo fails when Spring starts. It says it could not resolve the placeholder. The lookup is silent. The injected one is not.

## 8. Two Of A Type

Fifth demo: two of the same type. There are two notifiers registered. Ask the registry for a notifier, by type. It throws a No Unique Bean Definition exception, because it found two. That is an error while running, at the point of the call. Not a compile error. Asking by type only works, until a second one arrives.

## 9. The Verdict

So, here is the verdict. Spring's context is the registry done well. Declared, checked at start-up, and mostly never called. In business code, have things injected. Keep get bean for the main method, for tests, and for framework plumbing. And keep changing state out of anything that tests share.

## 10. Where You Have Met This

Where have you met this before? Every at Autowired injection goes through it. And every at Spring Boot Test shares one, unless you ask it not to.

## 11. What Was Used

For the record, here are the versions. Spring Boot four point one point one. No web server, no database, and no web library.

## 12. What Is Real Here

A quick, honest note about this demo. Everything here is real. The context, its errors, and the test cache. The project's own tests reproduce the leak, on real Spring.

## 13. When This Is Too Much

So, when is this too much? Never, for the context itself, because you already have one. The cost is in calling it.

## 14. Thanks for Watching

That's the Registry, with Spring. If you remember one sentence, make it this one. The registry done well is one you rarely call, and even then, whatever it holds is shared. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Run only the second leak test, on its own. And watch it fail. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
