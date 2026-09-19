# Singleton with Spring Pattern — Video Narration Script

## 1. Singleton with Spring

Hello, and welcome. This video explains the Singleton pattern with Spring Boot, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Singleton video. That one built an order number sequencer that checkout, the admin console and a retry job all share, and closed the reflection and serialization holes with a single element enum. This one shows the same idea inside Spring Boot. The plain definition, in short: in Spring, a singleton is a scope. The container keeps one instance, and hands it to everyone who asks. By the end you will see the same sequencer as a Spring bean shared by three callers, then see how the guarantee weakens: a plain new, a second container, a changed scope, and a thread-unsafe counter.

## 2. The Partner Project

This video assumes the Singleton video. If you have not seen it, start there. It shares one order number sequencer between checkout, the admin console and a retry job, and closes the reflection and serialization holes with an enum. This one uses the same example. It does not teach the pattern again. It shows what Spring Boot does with it.

## 3. Before The First Line

Before the first line of code, what Spring Boot is. Spring is a framework whose core is a container that creates your objects and hands them out. By default it keeps one instance of each bean, per container. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. One Bean, Shared

First, the good news. Checkout, the admin console and the retry job are each handed a generator by the container, and it is the same object. The numbers run one, two, three across all three callers. Notice what is missing. No private constructor. No static field. Spring did the sharing.

## 5. Nothing Stops new

Second, nothing stops a plain new. The constructor is public, because Spring wants it that way. So anyone can build a second generator, and it starts again at order one. The hand-built singleton made this impossible. Here it is only a convention.

## 6. One Per Container

Third, the word singleton is per container. Start the application twice in one program, and each container has its own generator. Context A issues order one. Context B issues order one. The same order number goes to two customers. An enum could not do that.

## 7. A Scope Change

Fourth, a scope change. Change one word in the bean definition, singleton to prototype, and each caller is handed its own generator. Checkout says order one. Admin says order one. Nothing fails. The compiler is silent. The only sign is duplicate numbers in production.

## 8. When Is It Built?

Fifth, when is it built. By default, at startup, before any caller asks. The count is one. With lazy initialization, the count is zero after startup, and one after the first caller. Eager finds a broken constructor at startup. Lazy finds it in front of a customer.

## 9. Shared Means Shared By Threads

Last, threads. A singleton is shared by every thread, and Spring does not protect its fields. A plain long, held between the read and the write, gives two customers the same number. An atomic long, hit by four threads, gives ten thousand distinct numbers. Spring shares the bean. Keeping its state safe is still your job.

## 10. The Verdict

My verdict, plainly. Let the container own the single instance. Keep the state inside it thread safe. Make sure only one container runs. And use the enum when no container is around.

## 11. How To Recognise It

How do you recognise this in code you did not write? A class with no private constructor and no getInstance method, passed in through a constructor. A component or service with no scope named, because the default is singleton.

## 12. Where You Have Met This

You have met this in every service and repository you have written. The default scope is singleton, so most of them already are.

## 13. What Was Used

For the record. Spring Boot four point one point one. No web server, no database, and no web starter.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: Spring's containers and scopes. The thread collision is forced with a gate, so it happens every time.

## 15. When This Is Too Much

So when is it too much? For a class with no state, the question hardly matters. It bites when the bean holds a counter, a cache or a connection.

## 16. Thanks for Watching

That's Singleton with Spring. If you take one sentence away, take this one: a Spring singleton is one per container, and only as safe as the state inside it. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, make the constructor private, and see what Spring does. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
