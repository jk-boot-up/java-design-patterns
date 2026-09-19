# Bounded Context Pattern — Video Narration Script

## 1. Bounded Context

Hello, and welcome. This video explains the Bounded Context pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a bounded context is a boundary inside which every word has exactly one meaning, and one model. The contexts around it have their own, and they are linked on purpose. This is the sixth project in the domain-driven design category, whose subject is writing code that says what the business says. In our online store, the word that means three different things is customer. By the end you will see one customer class try to serve three departments, see three small models that each mean what their department means, see the contexts talk by events, and see the bill, which is that everything is now stored and translated more than once.

## 2. The Scenario

Here is the scenario. Sales, Shipping and Support all talk about the customer. To Sales, a customer is a buyer with a credit limit. To Shipping, it is an address to deliver to. To Support, it is a person with tickets. The question: is that one class?

## 3. One Customer For Everyone

First, one customer class for everyone. It has twelve fields, because every department added what it needed. Each department uses only a handful, but every one depends on all twelve. So any department's change is every department's change.

## 4. The Pattern

The pattern. Draw a boundary. Inside it, every word has one meaning and one model. Each department gets its own model of the customer. They share only an identity, and they talk to one another by events.

## 5. The Same Word, Three Meanings

Second, one word, three meanings. Is Ada an active customer? Sales says yes: she bought in the last ninety days. Shipping says yes: a parcel is on its way. Support says no: she has no open ticket. One class cannot answer all three. Each answer is right, in its own context.

## 6. A Model For Each Context

Third, a model for each context. Sales has a buyer. Shipping has a recipient. Support has a contact. Four fields each, and each means what its department means. None of them knows the others' types. They share one thing: the customer id.

## 7. The Contexts Talk By Events

Fourth, the contexts talk by events. Sales renames Ada, and publishes a fact. For a moment, Sales says Ada King, and Shipping still says Ada Lovelace, with one event waiting. Then the event is delivered, and Shipping updates its own recipient. It never saw a buyer.

## 8. The Boundary Can Be Checked

Fifth, the boundary can be checked. A test scans the source, and finds no import of one context's types by another. So Shipping can add a field to its recipient, and nothing in Sales or Support needs to change.

## 9. The Bill

Last, the bill. Ada's name is now stored three times. Between a rename and its delivery, two contexts disagree about it, and that gap has a name: eventual consistency. And every context needs its own translator for every event it cares about. That is the price of a clean boundary.

## 10. How To Recognise It

How do you recognise this in code you did not write? The same word, such as Customer or Product, defined by separate classes in separate packages. Services or modules that each have their own database and their own idea of a customer. Events carrying an id and a few plain values, not whole objects. A context map, or a diagram of who is upstream of whom.

## 11. The Verdict

Here is my verdict, plainly. Draw a bounded context wherever the same word starts to mean different things, or where different teams own the model. Give each its own model, share only ids and events, translate at the border, and accept that copies lag. Do not split a small system that one team understands.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? In a small system that one team understands, one model is simpler, and translation is pure cost. A boundary earns its place where meanings really diverge.

## 14. Thanks for Watching

That's Bounded Context. If you take one sentence away, take this one: a bounded context lets every word mean one thing, at the price of translating between the things it means. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a support context that reacts to the rename event, and write its translator. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
