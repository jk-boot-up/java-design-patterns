# Singleton with Spring Pattern — Video Narration Script

## 1. Singleton with Spring

Hello, and welcome. This video explains the Singleton pattern, in Java, using Spring Boot. This video is presented by Jayasekhar Konduru. First, a simple definition. The Singleton pattern makes sure there is exactly one instance of a class, shared by everyone. In Spring, singleton is a scope. The container keeps one instance, and hands it to everyone who asks. Think of a shared office printer. Everyone on the floor sends their pages to the same machine. This is the framework version of the Singleton video, with the same order number generator. We will share the generator as a Spring bean, between three callers. Then we will hear how the guarantee weakens. A plain new, a second container, a changed scope, and a counter that is not thread-safe.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Singleton video. That one shares one order number generator between checkout, the admin console, and a retry job. And it closes the reflection and serialization tricks, using an enum. If you are new to the pattern, watch that one first. Here, we ask what Spring Boot does with the same idea.

## 3. Before The First Line

One thing is new in this project: Spring Boot. At its heart, Spring is a container that creates your objects, and hands them out. By default, it keeps one instance of each bean, per container. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. One Bean, Shared

First demo: one bean, shared. Checkout, the admin console, and the retry job are each given a generator by the container. And it is the very same object. The order numbers run one, two, three, across all three callers. Notice what is missing. No private constructor. No static field. Spring did the sharing.

## 5. Nothing Stops new

Second demo: nothing stops a plain new. The generator's constructor is public, because Spring needs it that way. So anyone can create a second generator. And it starts again at order one. The hand-built enum singleton made this impossible. Here, it is only a convention.

## 6. One Per Container

Third demo: singleton means one per container. Start the application twice, inside one program. Each container has its own generator. Container A issues order one. Container B also issues order one. The same order number goes to two customers. An enum could never do that.

## 7. A Scope Change

Fourth demo: a scope change. Change one word in the bean definition, from singleton to prototype. Now each caller gets its own generator. Checkout says order one. The admin console also says order one. Nothing fails, and the compiler says nothing. The only sign is duplicate order numbers, in production.

## 8. When Is It Built?

Fifth demo: when is the singleton created? By default, at startup, before any caller asks. The count of generators built is one. With lazy creation switched on, the count is zero after startup. And one after the first caller arrives. Eager creation finds a broken constructor at startup. Lazy creation finds it in front of a customer.

## 9. Shared Means Shared By Threads

Last demo: shared means shared by threads. A singleton is used by every thread, and Spring does not protect its fields. With a plain number as the counter, two threads both read the same value. So two customers both get order number one. With an Atomic Long, four threads request two thousand five hundred numbers each. And they get ten thousand different numbers. Spring shares the bean. Keeping its data safe is still your job.

## 10. The Verdict

So, here is the verdict. Let the container own the single instance. Keep the data inside it thread-safe. Make sure only one container runs. And use the enum singleton when there is no container around.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a class with no private constructor, and no get instance method, passed in through a constructor. And a component or service with no scope named. Because the default scope is singleton.

## 12. Where You Have Met This

Where have you met this before? In every service and repository class you have written. The default scope is singleton, so most of them already are.

## 13. What Was Used

For the record, here are the versions. Spring Boot four point one point one. No web server, no database, and no web library.

## 14. What Is Real Here

A quick, honest note about this demo. Spring's containers and scopes are real. The thread collision is forced with a gate, so it happens every time.

## 15. When This Is Too Much

So, when does this matter? For a class that holds no data, it hardly matters. It bites when the bean holds a counter, a cache, or a connection.

## 16. Thanks for Watching

That's Singleton with Spring. If you remember one sentence, make it this one. A Spring singleton is one per container, and only as safe as the data inside it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make the generator's constructor private. Then see what Spring does. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
