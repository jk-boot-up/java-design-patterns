# Layered Architecture with Spring Boot Pattern — Video Narration Script

## 1. Layered Architecture with Spring Boot

Hello, and welcome. This video explains the Layered Architecture pattern, in Java, using Spring Boot. This video is presented by Jayasekhar Konduru. First, a simple definition. A layered architecture splits a program into stacked layers. Each layer may only depend on the layer directly beneath it. In Spring Boot, the usual layers are controllers, services, and repositories. But the rule about who may depend on whom is still yours to enforce. Think of a restaurant again. The waiter takes the order, the chef cooks it, and the store room holds the food. Spring gives everyone a name badge. But the badges do not stop the waiter walking into the store room. This is the framework version of the Layered Architecture video, with the same online store. We will send one real web request through four layers, inside a real transaction. Then we will see a shortcut that Spring accepts without complaint, and the test that catches it.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Layered Architecture video. That one splits placing an order into four layers: presentation, application, domain, and infrastructure. With one rule about who may depend on whom. If you are new to the pattern, watch that one first. Here, we keep the same example, and ask what Spring Boot does with it.

## 3. Before The First Line

Three things are new in this project. One. Spring Boot, a framework that assembles a web application. Its controllers, services and repositories are the presentation, application and infrastructure layers. Two. A real web server, and an in-memory database. Three. ArchUnit, a library that checks the layering rule in a test. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. Four Layers, One Real Request

First demo: one real request. A real web request asks the shop to create an order. The answer is two hundred and one, meaning created, and the stock drops to four. On its way, the request passed through each layer in turn. The controller received it. The service ran the checkout. The repository stored the order. Each of those is one layer, marked by a Spring annotation.

## 5. One Transaction

Second demo: a transaction. This time, the stock is reserved first, and then the card is declined. The customer gets four hundred and two, meaning payment required. And the stock goes back to what it was. Why? Because the service wraps the whole checkout in a transaction. When the payment fails, the transaction undoes the reservation. That is why the transaction belongs in the application layer, the service.

## 6. Failures Become Statuses In One Place

Third demo: turning failures into status codes. A customer asks for ten coffee machines, but only four are left. The answer is four hundred and twenty-two, meaning the request cannot be processed. Notice who decided what. The domain only said: out of stock. One class in the presentation layer decided which number that becomes.

## 7. The Shortcut Runs

Fourth demo: the shortcut. Someone writes a controller that reads the repository directly, skipping the service. The application starts. The shortcut answers requests, with two hundred, meaning OK. Spring connects objects by their type, and it does not mind at all. Ten minutes to write, and nothing objects.

## 8. It Also Leaks

Fifth demo: the shortcut also leaks data. It returns the stored record exactly as it is. And that record includes the cost price, what the shop paid for the item. The proper, layered answer returns a response object instead. And that object leaves the cost price out. So the layer in the middle was doing a job you could not see, until it was skipped.

## 9. A Rule The Container Does Not Have

Last demo: a rule that Spring does not have. A test states which layer may depend on which. We run it over the whole project. It finds three violations. All three are in the shortcut controller. The four real layers have none. Spring connects objects by type. Only a test can say that a dependency is not allowed.

## 10. The Verdict

So, here is the verdict. Keep each layer in its own package. Put the transaction in the service. Return response objects, not stored records. And run a layering test with every build.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for classes marked Rest Controller, Service, and Repository, in separate packages. And look for the at Transactional annotation on a service method.

## 12. Where You Have Met This

Where have you met this before? In most Spring Boot applications you will ever open.

## 13. What Was Used

For the record, here are the versions. Spring Boot four point one point one. The H2 database. And ArchUnit one point five. With a real web server, on a free port.

## 14. What Is Real Here

A quick, honest note about this demo. Everything in it is real. A real web server, real web requests, a real database, and a real transaction.

## 15. When This Is Too Much

So, when is this too much? For a small script with a single table, four layers are more ceremony than help.

## 16. Thanks for Watching

That's Layered Architecture with Spring Boot. If you remember one sentence, make it this one. Spring names the layers, but only a test can say which dependencies are forbidden. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a class that breaks the layering rule. Then run the test, and listen to what it reports. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
