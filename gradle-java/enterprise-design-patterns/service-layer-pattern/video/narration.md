# Service Layer Pattern — Video Narration Script

## 1. Service Layer

Hello, and welcome. This video explains the Service Layer pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: put the operations your application offers in one layer, so every way of reaching the application calls the same code. This is the sixth project in the enterprise category. In our online store, the question is where placing an order should live. Put a business logic in a service is advice, not a pattern, so this video shows the problem it solves. By the end you will know what goes wrong with a second entry point, what the service owns and what the domain owns, and where the line is hard to draw.

## 2. The Scenario

Here is the scenario. Placing an order has five steps. Validate the cart. Check the stock. Take the payment. Write the order. Send the confirmation email. The question this video answers is simple: where does that code live?

## 3. The Logic In The Controller

The natural place to start is the web controller. It validates, reserves stock, takes payment, writes the order, and sends the email. A good order is placed. Twenty thousand pence is charged. One email is sent. With one door into the application, this is fine. Nothing in this video says it is wrong.

## 4. A Second Door

Then support asks for a command line, to place orders by phone. The quickest thing is to copy the logic. Later, someone fixes the web door: reserve the stock first, and only then take the payment. Nobody remembers the copy. Now the same request, five mice when three are in stock. Through the web, it is refused, and charged nothing. Through the command line, it is refused too, but the customer was already charged six thousand pence. Charged, or not, depending on which door they came through.

## 5. Put It All In The Domain Object

The other tempting answer is to put it all in the domain object. An order dot place method. It looks tidy. But the order now needs a payment gateway, an email service, a database and the products. Its constructor takes six things. You can see it is no longer a domain object. It is an application, in disguise.

## 6. The Pattern

The pattern is a service layer. One place order operation, and every door calls it. The service owns the order of the steps and the transaction: begin, do the work, commit or roll back. The domain keeps the rules. An order must not be empty. Stock must not go below zero.

## 7. One placeOrder, Two Doors

Same request, five mice when three are in stock. Through the web door: refused, charged nothing. Through the command line: refused, charged nothing. The same answer, and not because anyone was careful. Because both doors call the same place order. They cannot disagree.

## 8. Cost One: The Anemic Domain

Now the bill. First, and it needs a name: the anemic domain model. Push too much into services, and the domain objects become bags of getters and setters, with no behaviour of their own. This anemic order has eight methods, and every one is a getter or a setter. It is the most common shape in enterprise Java, and widely considered an anti-pattern.

## 9. Cost Two: The Line Is Hard To Draw

The honest dividing line is this. Business rules go in the domain. Orchestration goes in the service. But the line is genuinely hard to draw. Free delivery over fifty pounds: is that a rule about the order, or about shipping? Here it is on the order. Another team could put it in a shipping service, and be just as right. Reasonable teams draw it differently.

## 10. Other Ways To Organise It

Two other ways of organising this logic are worth naming. Transaction Script is one procedure per operation, which is roughly what the naive controller was. Table Module is one class for each table. This video names them and teaches neither. Both are real answers, in the right place.

## 11. The Toy Database

A word about what is real here. The database is a toy, with a transaction you can begin and roll back. The payment gateway and the email service are fakes, that remember what they were asked to do. That is how the demo can say a customer was charged six thousand pence.

## 12. Where You Have Met This

You have met this. A class marked as a service, with the transactional annotation on the place order method. The annotation draws the transaction boundary at the service, which is exactly what this project did by hand.

## 13. What Is Real Here

The same honest admission as everywhere in this course. The pattern is real. The gateway and the email are fakes. The drift is real. Copied logic drifting apart is one of the most ordinary things that happens in a team.

## 14. When This Is Too Much

So when is it too much? For one door and one operation, a service layer is just an extra class. It earns its place the moment a second door appears.

## 15. Thanks for Watching

That's the Service Layer. If you take one sentence away, take this one: rules in the domain, orchestration in the service, and every door calls the service. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a third door, a batch import, and count how many files change. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
