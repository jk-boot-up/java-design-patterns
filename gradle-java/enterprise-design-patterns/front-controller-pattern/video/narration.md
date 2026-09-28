# Front Controller Pattern — Video Narration Script

## 1. Front Controller

Hello, and welcome. This video explains the Front Controller pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A front controller is a single entry point that every request passes through. The shared work is done once, right there. Logging, checking who is asking, finding the right handler, and dealing with failures. Think of the reception desk in an office building. Every visitor signs in there, and is checked, before being sent to the right floor. In our online store, every visitor's web request arrives here first. In this video, handlers that look after themselves forget a security check. Then one front door does that work once. We will hear routing from a single table, logging of refused requests, and a failure hidden safely from the customer. And then the cost.

## 2. The Scenario

Here is the scenario. The online store's web application has pages for products, orders, and the customer's account. Every request must be logged. And every private page needs the visitor to be signed in. So here is the question. Who does that work?

## 3. Every Handler Looks After Itself

First, the naive way: every handler looks after itself. The orders handler was written in a hurry, and has no sign-in check. So a visitor who is not signed in receives Ada's orders. The account handler does check, and refuses with four hundred and one, meaning not signed in. But it only logs requests it accepts. So neither request left a log line.

## 4. The Pattern

Now, the pattern. One entry point for every request. Filters run first. One logs the request. Another checks who is asking. Then a routing table finds the right handler. And any failure is answered once, in one place. The handlers only do their own work.

## 5. One Entry Point

Second demo: one entry point. Through the front controller, the orders page without signing in is refused, with four hundred and one. The orders page, when signed in, is served, with two hundred, meaning OK. The products page is marked as public, so it needs neither. The sign-in check is written once. No handler can forget it, because no handler has it.

## 6. Routes In One Table

Third demo: routes in one table. A page that does not exist gets four hundred and four, meaning not found. A request with the wrong method gets four hundred and five, meaning not allowed. Both come from the routing table, in one place. So every unknown request is answered the same way.

## 7. Everything Is Logged

Fourth demo: everything is logged. Three requests, and three log lines. A refused request to orders. An accepted request to orders. And a request to a page that does not exist. Logging is a filter that runs first. So it sees everything, including requests that never reach a handler.

## 8. Failures Are Handled Once

Fifth demo: failures are handled once. A handler throws an error, and its message happens to include a password. The customer sees a plain five hundred: something went wrong. The full detail goes to the log, and only the log. The password never reaches the customer.

## 9. The Bill: One Door

Finally, the cost: one door. One filter has a bug in it. Now the products page, the orders page, and the account page all fail at once, with five hundred. The front controller is the one place everything depends on. Every request passes through it. So a mistake in it is a mistake everywhere.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a single servlet, or dispatcher, that receives every path. Look for a chain of filters, or middleware, in front of the handlers. Look for a routing table, or annotations that map paths to methods. In Spring, this is the Dispatcher Servlet. In Node's Express, it is app dot use.

## 11. The Verdict

So, here is the verdict. Use a front controller for any application with several pages, and shared work. Such as signing in, logging, error handling, and routing. Keep the filters small, in a clear order, and well tested, because everything depends on them. Keep the handlers free of the shared work. Most web frameworks already give you one. So learn the one you have.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every result you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a program with just one endpoint, a front controller is a door in front of a door. And its main risk is being a single point of failure. So keep it simple, and tested.

## 14. Thanks for Watching

That's the Front Controller pattern. If you remember one sentence, make it this one. A front controller does the shared work of every request once, and becomes the one thing everything depends on. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a filter that limits how many requests a visitor can make. And decide where in the order it should run. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
