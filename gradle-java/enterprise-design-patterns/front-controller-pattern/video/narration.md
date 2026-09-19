# Front Controller Pattern — Video Narration Script

## 1. Front Controller

Hello, and welcome. This video explains the Front Controller pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a front controller is a single entry point that every request passes through. The shared work, logging, checking who is asking, finding the right handler and handling failure, is done once, there. This is another project in the enterprise category, whose subject is how a business application organises its logic, its data and its requests. In our online store, the thing every visitor reaches first is a web request. By the end you will see handlers that each look after themselves and one that forgets to check who is asking, then see one door do that work once, route every request from a single table, log even refused requests, and hide a failure's detail from the customer, and then see the bill, which is that everything now depends on that door.

## 2. The Scenario

Here is the scenario. The online store's web application has pages for products, for orders, and for the customer's account. Every request needs to be logged. Every private page needs the visitor to be signed in. The question: who does that work?

## 3. Every Handler Looks After Itself

First, every handler looks after itself. The orders handler was written on a Friday, and has no sign in check. A visitor who is not signed in receives Ada's orders. The account handler does check, but it logs only what it accepts, so neither request left a log line.

## 4. The Pattern

The pattern. One entry point for every request. Filters run first: log the request, check who is asking. A routing table then finds the handler. And a failure is answered once, in one place. The handlers do only their own work.

## 5. One Entry Point

Second, one entry point. Through the front controller, orders without a sign in is refused with a four oh one. Orders with a sign in is served. Products, which is listed as public, needs neither. The check is written once, and no handler can forget it, because no handler has it.

## 6. Routes In One Table

Third, routes in one table. An unknown page gets a four oh four. A wrong method gets a four oh five. Both come from the routing table, in one place, so every unknown request is answered the same way.

## 7. Everything Is Logged

Fourth, everything is logged. Three requests, and three log lines. The refused request is in the log, and so is the missing page. Logging is a filter that runs first, so it sees everything, including what never reaches a handler.

## 8. Failures Are Handled Once

Fifth, failures handled once. A handler throws an error, and its message includes a password. The customer sees a plain five hundred: something went wrong. The detail goes to the log, and only the log. The password never reached the customer.

## 9. The Bill: One Door

Last, the bill. One filter has a bug in it. Now the products page, the orders page and the account page all return a five hundred at once. The front controller is the one place everything depends on. Every request passes through it, so a mistake in it is a mistake in everything.

## 10. How To Recognise It

How do you recognise this in code you did not write? A single servlet or dispatcher mapped to every path. A filter chain, or middleware, in front of the handlers. A routing table or annotations that map paths to methods. DispatcherServlet in Spring, app.use(...) in Express, Rack middleware in Ruby.

## 11. The Verdict

Here is my verdict, plainly. Use a front controller for any application with several pages or endpoints and shared concerns: sign in, logging, error handling, routing. Keep filters small, ordered, and well tested, because everything depends on them. Keep handlers free of the shared work. Most web frameworks give you one already, so learn the one you have.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a program with one endpoint, a front controller is a door in front of a door. Its risk is being a single point of failure, so keep it simple and tested.

## 14. Thanks for Watching

That's Front Controller. If you take one sentence away, take this one: a front controller does the shared work of a request once, and becomes the one thing everything depends on. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a rate limit filter, and decide where in the order it should run. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
