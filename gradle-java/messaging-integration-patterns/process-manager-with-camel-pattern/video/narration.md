# Process Manager with Apache Camel Pattern — Video Narration Script

## 1. Process Manager with Apache Camel

Hello, and welcome. This video explains the Process Manager pattern, built with Apache Camel's saga step, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A process manager runs a journey of several steps, from one place. It decides each next step, and makes sure every journey ends in a known state. Apache Camel is an open-source library for moving messages. Its saga step runs such journeys, and undoes earlier steps when a later one fails. Think of a travel agent booking a flight, a hotel, and a car. The agent notes how to cancel each booking. If the car fails, the agent cancels the hotel and the flight, and rings the customer. In this video, the domain is an online shop's orders, which reserve stock, take payment, and ship. By the end, you will hear how a declined card stranded stock. How a saga owns each journey. How Camel runs the undo steps. And what a saga costs.

## 2. The Scenario

Here is the scenario. Each order reserves stock, takes payment, and ships. Each step simply handed on to the next. When a card was declined, the kettle reserved for it was never given back.

## 3. Act One — Steps hand on to each other

First demo: each step hands on to the next. Reserve stock, then take payment, then ship. Order one is shipped. Order three's card is declined. The chain stops at payments. But its kettle is never given back. One kettle left, of three. Though only one was shipped. And nothing knows where order three is.

## 4. Act Two — A saga

Second demo: a saga runs each order's journey. One route owns the whole journey. Order one is reserved at the main warehouse. Paid. Shipped. When the journey ends well, Camel calls the completion route. Order one is marked done.

## 5. Act Three — A branch

Third demo: the journey branches. Order two is for a teapot. The main warehouse has none. So the reserve step asks the partner warehouse. It has two. Payment and shipping go ahead. Done.

## 6. Act Four — Camel runs the undo steps

Fourth demo: the card is declined, and Camel runs the undo steps. When the reserve step joined the saga, it named how to undo itself. The card is declined. So Camel calls the undo step. The kettle goes back to the warehouse. Then Camel calls the cancellation route. The order is marked cancelled. The customer gets an email. Two kettles of three remain, as they should.

## 7. Act Five — The bill

Fifth demo: the bill. The shop can now say where every order is. But every step that changes something needs an undo step, written by someone. And undoing is not the same as never having happened. And this saga service keeps its notes in memory. A restart forgets every journey. Production needs a coordinator that keeps them safe.

## 8. The Pattern, in Camel

Let's name the pattern, in Camel's words. The saga step makes one route own the whole journey. Each step that changes something names its undo step. When a step fails, Camel calls the undo steps, then the cancellation route. When all goes well, the completion route.

## 9. Who Does What

Here is who does what. Shop routes declares the saga, and its completion and undo routes. The services do the work. Reserve, pay, ship, and release. The saga service keeps track of each journey while the program runs. And the order is the message.

## 10. Where You Have Seen It

You have probably met this already. Camel's saga, often with a separate coordinator service. Workflow engines, such as Temporal and Axon. And every travel booking, where a failed step cancels the earlier ones.

## 11. When To Use It

So, when should you use it? When a journey crosses several services, and each one changes something. Write an undo for every step. Remember that undo is not rewind. And use a durable coordinator in production.

## 12. Thanks for Watching

That's the Process Manager, with Apache Camel's saga. If you remember one sentence, make it this one. One place owns the journey, and every step knows how to undo itself. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add an undo step for shipping, that books a return label. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
