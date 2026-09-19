# Layered Architecture with Spring Boot Pattern — Video Narration Script

## 1. Layered Architecture with Spring Boot

Hello, and welcome. This video explains the Layered Architecture pattern with Spring Boot, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Layered Architecture video. That one arranged placing an order into presentation, application, domain and infrastructure layers, with one rule about who may depend on whom, and counted the bill for a forced change. This one shows the same idea inside Spring Boot. The plain definition, in short: in a Spring Boot application, the layers are controllers, services and repositories, and the layering rule is yours to enforce. By the end you will see one real HTTP request go through four layers with a real transaction, then see the shortcut Spring accepts without complaint, and the test that catches it.

## 2. The Partner Project

This video assumes the Layered Architecture video. If you have not seen it, start there. It arranges placing an order into presentation, application, domain and infrastructure layers, with one rule about who may depend on whom. This one uses the same example. It does not teach the pattern again. It shows what Spring Boot does with it.

## 3. Before The First Line

Before the first line of code, what Spring Boot is. Spring Boot is a framework that assembles a web application. Controllers, services and repositories are its names for the presentation, application and infrastructure layers. ArchUnit is a library that checks the layering rule. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. Four Layers, One Real Request

First, a real request over HTTP. It is created, and the stock drops to four. The controller took it, the service ran it, the repository stored it. Each is one layer, marked by a Spring annotation.

## 5. One Transaction

Second, the transaction. The card is declined after the stock has been reserved. The customer gets a four oh two, and the stock is unchanged. The service's transaction undid the reservation. That is why the transaction belongs in the application layer.

## 6. Failures Become Statuses In One Place

Third, statuses. Ten machines when four are left is refused with four twenty two. The domain only said out of stock. One class in the presentation layer decides what number that becomes.

## 7. The Shortcut Runs

Fourth, the shortcut. A controller reads the repository directly, skipping the service. It starts. It answers. Spring wires by type, and it does not mind. Ten minutes to write, and nothing objects.

## 8. It Also Leaks

Fifth, the shortcut also leaks. It returns the record as it is, and the record includes what the shop paid. The layered answer is a response object, with no cost. The layer in the middle was doing a job you could not see.

## 9. A Rule The Container Does Not Have

Last, the rule. A test states which layer may depend on which. Run over the whole project, it finds three violations, and all of them are in the shortcut. The four real layers have none. Spring wires by type. Only a test can say a layer is not allowed to be there.

## 10. The Verdict

My verdict, plainly. Keep the layers as packages. Put the transaction in the service. Return response objects, not entities. And run a layering test in the build.

## 11. How To Recognise It

How do you recognise this in code you did not write? A rest controller, a service and a repository, in separate packages. And a transactional annotation on a service method.

## 12. Where You Have Met This

You have met this in most Spring Boot applications you will ever open.

## 13. What Was Used

For the record. Spring Boot four point one point one, H2, and ArchUnit one point five. A real web server, on a free port.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: a real web server, real HTTP, a real database and a real transaction.

## 15. When This Is Too Much

So when is it too much? For a small script with one table, four layers are more ceremony than help.

## 16. Thanks for Watching

That's Layered Architecture with Spring Boot. If you take one sentence away, take this one: Spring names the layers, and only a test can say which dependencies are forbidden. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, add a class that breaks the rule, and run the test. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
