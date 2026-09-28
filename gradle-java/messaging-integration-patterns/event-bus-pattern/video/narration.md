# Event Bus Pattern — Video Narration Script

## 1. Event Bus

Hello, and welcome. This video explains the Event Bus pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An event bus is one central place inside a program. Parts of the program post events to it. And other parts subscribe to the kinds of event they care about. So none of them needs a reference to any other. Think of the announcement speakers in a railway station. The announcer does not know who is listening. Each traveller only listens for their own train. In our online store, five parts of one program all want to know when an order is placed, or cancelled. In this video, five parts that all know each other are replaced by a bus. We will hear subscribers choosing events by type, a failing subscriber that harms nobody else, an event nobody hears, and then the cost.

## 2. The Scenario

Here is the scenario. Inside the online store's program, five parts react when an order is placed or cancelled. Inventory, email, analytics, loyalty points, and the audit log. So here is the question. Who talks to whom?

## 3. Everyone Knows Everyone

First, the naive way: everyone knows everyone. Five parts that each tell each other about orders need twenty references between them. Add a sixth part, and it needs ten more. The web of connections grows much faster than the number of parts.

## 4. The Pattern

Now, the pattern. There is one bus, inside the program. Parts post events to it. Parts subscribe to the kinds of event they care about. And nobody holds a reference to anybody else.

## 5. Everyone Knows The Bus

Second demo: everyone knows the bus. One post reaches inventory, email, and analytics. Five parts, each holding one reference, to the bus. That is five references, not twenty. And the part that posts the event does not know who hears it.

## 6. By Type

Third demo: subscribing by type. One subscriber listens for order placed, and hears only that. Another listens for every kind of order event. So it hears both: order placed, and order cancelled. Each subscriber asks for exactly the kind of thing it cares about.

## 7. One Failing Subscriber

Fourth demo: one failing subscriber. The email subscriber fails, with a timeout. But analytics still hears the event. The failure is recorded. And the part that posted the event never sees it. It posted, and carried on.

## 8. An Event Nobody Hears

Fifth demo: an event that nobody hears. With no subscriber at all, the bus counts it as a dead event. And nothing complains. With a subscriber that listens for dead events, the unheard event arrives there instead. A typo in an event type, or a forgotten subscription, is a silent loss. Unless something listens for dead events.

## 9. The Bill

Finally, the costs. First: who reacts to an order placed event? Nothing in the code that posts it says. You can ask the bus, but only if you know to ask. Second: a thousand short-lived parts subscribe, and are thrown away without unsubscribing. The bus still holds all of them. That is a memory leak. Unsubscribing each one leaves none. Third: delivery is just a method call, inside one program. So a slow subscriber holds up the part that posted.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for event bus post, and the at Subscribe annotation, in Google's Guava library. Look for Spring's application event publisher, and at Event Listener. Look for the event bus in Vert x. And look for classes named listener or subscriber, that nobody seems to call.

## 11. The Verdict

So, here is the verdict. Use an event bus inside one program, to separate parts that react to what happened. Give events clear types, and subscribe by type. Always unsubscribe when a subscriber goes away. Listen for dead events. And keep a list of who reacts to what, somewhere a person can find it. Do not use one between separate programs, where you need a real message broker. Or where the poster needs an answer.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For two parts that always talk to each other, a direct call is clearer. A bus is for many parts talking to many parts. And its cost is a flow you cannot see by reading one class.

## 14. Thanks for Watching

That's the Event Bus pattern. If you remember one sentence, make it this one. An event bus removes the references between parts of a program, and the price is a flow you cannot see, and subscriptions you must clean up. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a subscriber that unsubscribes itself, after its first event. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
