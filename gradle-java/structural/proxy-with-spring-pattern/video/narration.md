# Proxy with Spring Pattern — Video Narration Script

## 1. Proxy with Spring

Hello, and welcome. This video explains the Proxy pattern in Java, using Spring Boot. This video is presented by Jayasekhar Konduru. First, a simple definition. A proxy is a stand-in, placed in front of a real object, with exactly the same shape. It can delay expensive work, or check who is asking, before passing the call on. In Spring, the proxy is generated for you, while the program runs. And a separate piece of code, called an aspect, says what the proxy does on each call. In our online store, the example is product images again. By the end, you will hear the same two proxies come from Spring, instead of being written by hand. And the two ways a call can slip past the generated proxy.

## 2. The Partner Project

This video builds on the plain Java Proxy video. If you have not seen it, start there. That video puts two hand-written proxies in front of a product image. One that loads lazily, and one that checks access. And it combines the two. This video uses the same example. It does not teach the pattern again. It shows what Spring Boot does with it.

## 3. Before The First Line

Before any code, what is Spring Boot? Spring is a framework, built around a container that creates your objects for you. Those objects are called beans. With its aspect support switched on, Spring wraps a bean in a generated proxy. And it runs your extra code around each call. And a promise. Skipping this video loses none of the pattern. The plain Java video teaches all of it.

## 4. The Bean Is Not Your Class

First demo: the bean is not your class. Ask the container for the image catalogue. What you receive is a generated subclass of it. It is a proxy, wrapped around the real object. And nobody wrote it.

## 5. Protection, Written Once

Second demo: protection, written once. An admin asks for an image, and gets it. A shopper asks, and is refused, before the real method even runs. The rule is not inside the catalogue. It lives in an aspect.

## 6. Lazy Loading

Third demo: lazy loading. At startup, no images are loaded. A cheap question, like who owns the catalogue, loads none. The first time an image is shown, one is loaded. It took two annotations. Marking the class as lazy on its own is not enough.

## 7. One Aspect, Three Screens

Fourth demo: one aspect, three screens. The same aspect protects the catalogue, the order export, and the refund desk. A shopper is refused by all three. The rule exists in one place. In the plain Java version, each screen needed its own proxy class.

## 8. A Call On this

Fifth demo: a call from inside. A method inside the catalogue calls its own protected method directly. That call never passes through the proxy. From outside, the shopper is refused. But through that inside call, the shopper gets the image. Nothing fails. Nothing is logged. The rule is silently switched off.

## 9. A Final Method

Last demo: a final method. A method marked final cannot be replaced by the generated subclass. So the proxy runs it on itself. And the proxy holds none of the real object's data. The rule is skipped, and the method crashes with a null pointer error. Here, the failure is loud. But if the method used no data, it would simply run unprotected, and nobody would notice.

## 10. The Verdict

So, here is the verdict. Write each rule once, in an aspect. Call protected methods from outside the bean, never from inside it. Avoid final methods on beans that Spring wraps. And test that refusals happen, not just that successes work.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for an aspect with around advice. Look for transactional or cacheable annotations on methods. Or a class name in an error trace containing Spring C G LIB, the tool that generates the proxies.

## 12. Where You Have Met This

Where have you met this before? In every method marked transactional. That is a proxy, opening and closing a database transaction around your call.

## 13. What Was Used

For the record, here is what was used. Spring Boot, version four point one point one, with its aspect support. There is no web server, and no database.

## 14. What Is Real Here

A quick, honest note about this demo. Everything is real: Spring's generated proxies, and the aspect code. And nothing depends on timing, so every run gives the same result.

## 15. When This Is Too Much

So, when is this too much? For one class with one rule, a hand-written wrapper is easier to read than an aspect.

## 16. Thanks for Watching

That's Proxy, with Spring. If you remember one sentence, make it this one. Spring writes the proxy for you, but it only protects the calls that actually pass through it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Remove the final keyword from that method. Then run the last demo again, and hear the rule work. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
