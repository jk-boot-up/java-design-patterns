# Prototype with Spring Pattern — Video Narration Script

## 1. Prototype with Spring

Hello, and welcome. This video explains the Prototype pattern, in Java, using Spring Boot. This video is presented by Jayasekhar Konduru. First, a simple definition. The Prototype pattern makes new objects by copying an existing example. In Spring, prototype is also the name of a scope. Every time you ask for a prototype-scoped bean, Spring builds a new one from its definition. Think of a cookie cutter. Every press makes a fresh cookie of the same shape. But icing one cookie does not ice the next. This is the framework version of the Prototype video, with the same product listings. We will make the listing a prototype-scoped bean. Then we will hear three surprises. It is not a copy of your edited draft, it is built only once inside a singleton, and Spring never cleans it up.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Prototype video. That one copies a finished product listing into variants. It decides field by field what a copy means, and keeps a registry of templates. If you are new to the pattern, watch that one first. Here, we ask what Spring Boot does with the same idea.

## 3. Before The First Line

One thing is new in this project: Spring Boot. At its heart, Spring is a container that creates your objects. It has a prototype scope, which builds a new bean for every request. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. A New One Each Time

First demo: a new one each time. Ask the container for a listing, twice. You get two different objects. Both are titled untitled, straight from the definition.

## 5. Independent

Second demo: they are independent. Give the first listing a title, blue mug, and an extra picture. The second listing still says untitled, with one picture. So far, this looks exactly like the pattern.

## 6. A Definition, Not A Draft

Third demo: the difference that matters. Edit a draft listing, then ask the container for another. You get an untitled one. The container builds from the definition, not from your draft. Only the draft's own copy method carries your edits across. Spring gives you the scope. Copying is still your job.

## 7. A Prototype Inside A Singleton

Fourth demo: the classic trap. A singleton receives a prototype listing in its constructor. But the constructor only runs once. So the listing is built only once. Every call returns the same listing. One caller sets the title to blue mug. And the next caller sees blue mug too. The bean is a prototype in name only.

## 8. Ask Each Time

Fifth demo: the fix. Instead of the listing itself, the singleton receives an Object Provider. And it asks the provider for a listing each time it needs one. Now every call builds a new listing. And the second caller sees an untitled one.

## 9. Nobody Cleans Up

Last demo: nobody cleans up. Three listings are built. Then the container is closed. None of the three listings is cleaned up. But the singleton's clean-up method does run, once. Spring builds a prototype, and then lets go of it. If yours holds a file, or a connection, closing it is your job.

## 10. The Verdict

So, here is the verdict. Use the prototype scope when you want a fresh object. Inside a singleton, ask for it through a provider. Copy an edited draft with a copy method of your own. And clean up after it yourself.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a scope annotation that says prototype. An Object Provider passed into a constructor. Or get bean, called inside a loop.

## 12. Where You Have Met This

Where have you met this before? In helpers created fresh for each request, builders that hold state, and command objects. Any bean marked prototype.

## 13. What Was Used

For the record, here are the versions. Spring Boot four point one point one. No web server, no database, and no web library.

## 14. What Is Real Here

A quick, honest note about this demo. Spring's container, and its scopes, are real. And nothing here depends on timing.

## 15. When This Is Too Much

So, when is this too much? If the object is cheap, and has nothing to configure, simply creating it with new is easier than a scope.

## 16. Thanks for Watching

That's Prototype with Spring. If you remember one sentence, make it this one. Spring's prototype is a new bean built from its definition, not a copy of your draft. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Inject a listing into a second singleton. And predict what its callers will see, before you run it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
