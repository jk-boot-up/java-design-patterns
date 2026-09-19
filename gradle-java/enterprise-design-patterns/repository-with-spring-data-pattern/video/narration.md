# Repository with Spring Data Pattern — Video Narration Script

## 1. Repository with Spring Data

Hello, and welcome. This video explains the Repository pattern with Spring Data, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Repository video. That one built two implementations by hand. This one has none. The plain definition, in short: an interface that looks like a collection of your objects, so the code using it asks for objects, not for tables. By the end you will see an interface with no class behind it that still works, a query written from a method's name, and a leak that comes with it: an entity handed to a caller that can change without a save.

## 2. The Partner Project

This video assumes the Repository video. If you have not seen it, start there. It builds one interface, and two implementations by hand: one over a list, one over a database. This one uses the same six customers and the same question: London customers who ordered in the last month. It does not teach the pattern again. It shows what Spring Data does with it.

## 3. Before The First Annotation

Before the first annotation, new things. Spring Boot creates and wires your objects. Spring Data writes your repository for you, from an interface. H two is a database that runs in memory, so nothing needs installing. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. An Interface With No Implementation

Here is the first surprise. The customer repository is an interface. And this project has no class that implements it. Not one. The object Spring injected is a generated proxy. Save works. Find by id works. Find all works. Delete works. None of them were written by anyone.

## 5. A Query From A Name

Now the query from the last video, London customers who ordered in the last month. It was written by hand, twice. Here it is a method name: find distinct by city and orders day greater than. Spring Data reads the name and builds the query. Ada and Grace, in one statement. And the marketing service from the partner video, its body unchanged, gives the same answer. The two implementation classes it needed before are not in this project, and the application runs.

## 6. Cost: A Name Can Be Wrong

Now the bill. Every question still needs a method, and the names grow. Find distinct by city and orders day greater than and orders status in. And the name is now the query. A typo, find by c i i ty, is not caught by the compiler. It is caught only when Spring reads it: no property c i i ty found. The compiler cannot check a name.

## 7. Cost: The Leak On Speed

Second cost. Counting every customer's orders. Six customers, and the orders are lazy. Seven statements: the same seven the hand-built version cost. Add an entity graph annotation to the repository method, and it is one statement. The interface can now say join. But only by carrying a persistence hint, on a type that was meant to hide persistence.

## 8. The Managed Entity That Leaks

Now the failure of this project's own. An entity that a repository hands out is not a plain object. It is managed. A caller, inside a transaction, gets all the customers, and changes one. Moves Ada to Manchester. It never calls save. At commit, Ada's city in the database is Manchester. Written, with no save anywhere. The same change, with no transaction around it: Ada's city in the database is still London. The change is lost, and there is no error. The interface looks like a collection. The objects in it are not plain.

## 9. And The Swap?

One more thing from the hand-built video, still true. A repository is often sold as a way to swap the database. That is claimed far more often than it is used. The real benefit is that callers speak the language of the domain.

## 10. Where You Have Met This

You have met this. Every J P A repository is this pattern. The framework supplies the implementation you wrote by hand, and writes the queries from the names. Now you know what it is doing for you, and where it leaks.

## 11. What Was Used

For the record. Spring Boot four point one point one. Spring Data, Hibernate and H two are whichever versions that release manages. There is no web server and no web starter in this project.

## 12. What Is Real Here

The same honest admission as everywhere in this course, and again short. Everything is real. The proxy is Spring's. The query is built by Spring Data from the name. The counts come from Hibernate's own statistics. The only stand-in is the database, H two in memory.

## 13. When This Is Too Much

So when is it too much? For a handful of queries in one place, Spring Data still saves you two classes. The cost is the leak, and it needs to be known about.

## 14. Thanks for Watching

That's Repository with Spring Data. If you take one sentence away, take this one: the interface hides the database, but the entity it returns does not hide the persistence context. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, add a finder by name prefix, and call it, without writing any other code. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
