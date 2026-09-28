# Bounded Context Pattern — Video Narration Script

## 1. Bounded Context

Hello, and welcome. This video explains the Bounded Context pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A bounded context is a boundary, inside which every word has exactly one meaning, and one model. The contexts around it have their own meanings. And they are connected on purpose. Think of the word, bank. To a banker, it holds money. To a fisherman, it is the edge of a river. Both are right, in their own world. In our online store, the word that means three different things is customer. In this video, one customer class tries to serve three departments. Then three small models each mean what their own department means. We will hear them talk through events, and then the cost.

## 2. The Scenario

Here is the scenario. Sales, Shipping, and Support all talk about the customer. To Sales, a customer is a buyer, with a credit limit. To Shipping, a customer is an address to deliver to. To Support, a customer is a person, with support tickets. So here is the question. Is that really one class?

## 3. One Customer For Everyone

First, the usual way: one customer class, for everyone. It has twelve fields, because every department added what it needed. Each department only uses a handful of them. But every department depends on all twelve. So a change for one department is a change for every department.

## 4. The Pattern

Now, the pattern. Draw a boundary. Inside it, every word has one meaning, and one model. Each department gets its own model of the customer. They share only an I D. And they talk to each other through events.

## 5. The Same Word, Three Meanings

Second demo: one word, three meanings. Is Ada an active customer? Sales says yes, because she bought something in the last ninety days. Shipping says yes, because a parcel is on its way to her. Support says no, because she has no open ticket. One class cannot give all three answers. And each answer is right, in its own context.

## 6. A Model For Each Context

Third demo: a model for each context. Sales has a Buyer. Shipping has a Recipient. Support has a Contact. Each has four fields, and each means what its own department means. None of them knows the others' types. They share just one thing: the customer I D.

## 7. The Contexts Talk By Events

Fourth demo: the contexts talk through events. Sales renames Ada, from Ada Lovelace to Ada King. And it publishes that fact as an event. For a moment, Sales says Ada King, and Shipping still says Ada Lovelace. One event is waiting. Then the event is delivered. Shipping updates its own recipient to Ada King. It never saw the Sales buyer at all.

## 8. The Boundary Can Be Checked

Fifth demo: the boundary can be checked. A test scans the source code. It finds no place where one context uses another context's types. So Shipping can add a field to its recipient. And nothing in Sales or Support needs to change.

## 9. The Bill

Finally, the cost. Ada's name is now stored three times. Between a rename and its delivery, two contexts disagree about her name. That gap has a name: eventual consistency. And each context needs its own translator, for every event it cares about. That is the price of a clean boundary.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for the same word, such as customer or product, defined by separate classes, in separate packages. Look for services or modules that each have their own database, and their own idea of a customer. Look for events that carry an I D and a few plain values, not whole objects. And look for a context map, a diagram showing which context depends on which.

## 11. The Verdict

So, here is the verdict. Draw a bounded context wherever the same word starts to mean different things. Or wherever different teams own the model. Give each context its own model. Share only I Ds and events. Translate at the border. And accept that the copies will lag behind a little. Do not split a small system that one team understands.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every result you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? In a small system that one team understands, one model is simpler, and translation is pure cost. A boundary earns its place where the meanings really do differ.

## 14. Thanks for Watching

That's the Bounded Context pattern. If you remember one sentence, make it this one. A bounded context lets every word mean one thing, at the price of translating between contexts. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make the support context react to the rename event. And write its translator. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
