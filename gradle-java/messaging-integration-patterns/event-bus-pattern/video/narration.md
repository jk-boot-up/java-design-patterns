# Event Bus Pattern — Video Narration Script

## 1. Event Bus

Hello, and welcome. This video explains the Event Bus pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: an event bus is a single place where components post events and subscribe to the kinds they care about, so that none of them holds a reference to any other. This is the fifth project in the messaging and integration category, whose subject is how separate systems exchange messages safely. In our online store, five parts of the same program all want to know when an order is placed or cancelled. By the end you will see five components that all know each other, see each know only the bus, see subscribers pick events by type, see one failing subscriber leave the others alone, see an event nobody hears, and see the bill, which is that the flow becomes hard to see.

## 2. The Scenario

Here is the scenario. Inside the online store's program, five components react when an order is placed or cancelled: inventory, email, analytics, loyalty points and the audit log. The question: who talks to whom?

## 3. Everyone Knows Everyone

First, everyone knows everyone. Five components that each tell each other about orders need twenty references between them. Add a sixth, and it needs ten more. The web grows faster than the components.

## 4. The Pattern

The pattern. One bus, inside the program. Components post events to it. Components subscribe to the kinds of event they care about. And nobody holds a reference to anybody else.

## 5. Everyone Knows The Bus

Second, everyone knows the bus. One post reaches inventory, email and analytics. Five components each hold one reference, to the bus: five references, not twenty. And the poster holds no reference to any subscriber.

## 6. By Type

Third, by type. A subscriber for order placed hears only that. A subscriber for every order event, the parent type, hears both the placed and the cancelled. Each subscriber asks for the kind of thing it cares about.

## 7. One Failing Subscriber

Fourth, one failing subscriber. Email fails, on a timeout. Analytics still hears the event. The failure is recorded. The poster does not see it. It posted, and carried on.

## 8. An Event Nobody Hears

Fifth, an event nobody hears. With no subscriber, the bus counts it as a dead event, and nothing complains. With a subscriber for dead events, the unheard event arrives there. A typo in an event type, or a forgotten subscription, is a silent loss, unless something listens for dead events.

## 9. The Bill

Last, the bill. Who reacts to an order placed event? Nothing in the code that posts it says. The bus can be asked, but you have to know to ask. A thousand short lived components that subscribe and are thrown away without cancelling are all still held: a memory leak. Cancelling each leaves none. And delivery is a method call in one process, so a slow subscriber holds up the poster.

## 10. How To Recognise It

How do you recognise this in code you did not write? eventBus.post(...) and @Subscribe in Guava. Spring's ApplicationEventPublisher and @EventListener. Android's LocalBroadcastManager, and Vert.x's EventBus. Classes with names ending in Listener or Subscriber and no visible caller.

## 11. The Verdict

Here is my verdict, plainly. Use an event bus inside a program to decouple components that react to what happened. Type the events, subscribe by type, always cancel a subscription when the subscriber goes away, listen for dead events, and keep a list of who reacts to what somewhere a person can find. Do not use one across processes, where you need a real broker, or where the poster needs an answer.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For two components that always talk, a direct call is clearer. A bus is for many-to-many, and its cost is a flow you cannot see by reading one class.

## 14. Thanks for Watching

That's Event Bus. If you take one sentence away, take this one: an event bus removes the references between components, and the price is a flow you cannot see, and subscriptions you must clean up. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a subscriber that unsubscribes itself after its first event. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
