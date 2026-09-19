# Prototype with Spring Pattern — Video Narration Script

## 1. Prototype with Spring

Hello, and welcome. This video explains the Prototype pattern with Spring Boot, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Prototype video. That one copied a fully assembled product listing into variants, deciding field by field what a copy means, and kept a registry of templates. This one shows the same idea inside Spring Boot. The plain definition, in short: in Spring, a prototype is a scope. Every request for the bean builds a new one from its definition. By the end you will see the listing as a prototype-scoped bean, then see the three ways it surprises people: it is not a copy of an edited draft, it is built only once inside a singleton, and Spring never destroys it.

## 2. The Partner Project

This video assumes the Prototype video. If you have not seen it, start there. It copies a finished product listing into variants, decides field by field what a copy means, and keeps a registry of templates. This one uses the same example. It does not teach the pattern again. It shows what Spring Boot does with it.

## 3. Before The First Line

Before the first line of code, what Spring Boot is. Spring is a framework whose core is a container that creates your objects. It has a prototype scope, which builds a new bean for every request. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. A New One Each Time

First, the scope. Ask the container for a listing twice, and you get two different objects. Both are untitled, straight from the definition.

## 5. Independent

Second, they are independent. Give one a title and an extra image. The other still says untitled, with one image. So far this looks like the pattern.

## 6. A Definition, Not A Draft

Third, the difference that matters. Edit a draft, then ask the container for another listing. You get an untitled one. The container builds from the definition, not from your draft. Only the draft's own copy method carries the edits. Spring gives you the scope. The copy is still your job.

## 7. A Prototype Inside A Singleton

Fourth, the classic trap. A singleton takes a prototype in its constructor. The constructor runs once, so the listing is built once. Every call returns the same object. One caller sets a title, and the next caller sees it. The bean is a prototype in name only.

## 8. Ask Each Time

Fifth, the fix. Inject an object provider, and ask it each time. Every call builds a new listing. The second caller sees an untitled one.

## 9. Nobody Cleans Up

Last, cleanup. Build three listings, and close the container. None of the three is destroyed. The singleton's destroy method runs once. Spring builds a prototype and lets go of it. If yours holds a file or a connection, closing it is your job.

## 10. The Verdict

My verdict, plainly. Use the prototype scope for a fresh object. Ask for it through a provider inside a singleton. Copy an edited draft with a copy method of your own. And clean up after it yourself.

## 11. How To Recognise It

How do you recognise this in code you did not write? A scope annotation naming prototype. An object provider in a constructor. Or get bean, called in a loop.

## 12. Where You Have Met This

You have met this in per request helpers, stateful builders and command objects. Any bean marked prototype.

## 13. What Was Used

For the record. Spring Boot four point one point one. No web server, no database, and no web starter.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: Spring's container and its scopes. Nothing here depends on timing.

## 15. When This Is Too Much

So when is it too much? If the object is cheap and has no state to configure, new is simpler than a scope.

## 16. Thanks for Watching

That's Prototype with Spring. If you take one sentence away, take this one: Spring's prototype is a new bean from the definition, not a copy of a draft. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, inject a listing into a second singleton, and predict what its callers see. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
