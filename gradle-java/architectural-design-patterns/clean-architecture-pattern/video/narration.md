# Clean Architecture Pattern — Video Narration Script

## 1. Clean Architecture

Hello, and welcome. This video explains Clean Architecture in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the plain definition. Concentric circles -- entities at the centre, use cases around them, interface adapters around those, frameworks and drivers on the outside -- with one rule, stated once. Source code dependencies point only inward. This is the fourth project in a series building the same online shop five different ways, and I want to be upfront about something before we start. This is a close relative of the previous project, Hexagonal Architecture, and pretending otherwise would be dishonest. What is genuinely new here, and what this video actually spends its time on: a use case's own boundary, not folded into one undifferentiated outside. The moment control and dependency point in opposite directions, shown in code rather than described. And the largest forced change in this whole category -- adding two new things at once, not swapping one. By the end you will have seen the single trick this entire pattern rests on, stated as one sentence you can hold in your head with the screen off.

## 2. The Scenario

Same order as every project in this category. Check stock, take payment, store the order, notify the customer. Ada Okafor's three hundred and eighty-two pounds fifty. What is different in this video is how many named rings sit between the entity at the centre and the class that actually calls out to the network. Four needs -- a catalogue, a payment gateway, somewhere to store an order, a way to notify -- stated as four interfaces, all four declared by the use case itself, exactly as the project before this one taught you to expect.

## 3. The Naive Version

Here is where this project starts. A class that calls itself a use case, with a constructor typed as three concrete gateway classes -- not the interfaces the real use case declares. It works. It places the order correctly. And it reaches straight through the interface-adapters ring it is supposed to sit inside of, to name classes that live two rings further out. Testing it means constructing all three gateways first, and swapping any one of them means opening and editing this file.

## 4. Four Circles, One Rule

Four rings. Entities at the centre -- an order, a price, a product, true whether or not anything outside is even running. Use cases around them -- the interactor, and the boundary interfaces it declares for whatever it needs. Interface adapters around those -- controllers translating a request into the use case's own input shape, gateways translating the use case's boundary calls into real storage. And frameworks and drivers on the outside -- in this project, just the composition root. And one rule, which is the entire architecture stated as a sentence: source code dependencies point only inward. Not mostly inward. Never outward, at any boundary, for any reason you will have thought of at eleven o'clock on a Friday.

## 5. This Is Not Hexagonal Again

I promised to be honest about the overlap, so let me name it precisely rather than wave at it. Same centre, same rule about which way a dependency may point. What is actually different: one boundary becomes three named rings, because the translation work between a use case's own shapes and the outside world is a distinct job, worth its own ring. The dependency-inversion moment is shown as two directions disagreeing, in real code, on screen, rather than left as a diagram. The forced change adds two new things at once instead of swapping one -- proving the architecture scales by addition, not only by substitution. And the fourth difference is this project's own honesty about being the most over-applied pattern in the category, which gets its own section later, with real numbers rather than a warning label.

## 6. The Real Graph, Wired By Hand

A simulated HTTP request arrives at a controller, which calls one method on the use case's own boundary interface. Open the interactor and count its imports. Two: entities, and its own package, use cases. Not one adapter. And the composition root -- main -- reached into the outermost ring for four concrete gateways and handed them to this interactor by hand, in about twenty lines. No annotation, no container, nothing invisible.

## 7. The Dependency-Inversion Moment

This is the single most valuable thing in this video, so I am going to say it slowly. The interactor calls orders dot save. Orders is typed as OrderRepository -- an interface, declared right here, in the use case's own package. The class that really keeps a map of orders lives two rings further out, and reaches up to implement that interface. Now watch the two directions separately. Control -- what actually runs when this line executes -- flows outward, landing in that outer class's code. The dependency -- what type must exist on this file's classpath for it to compile at all -- points inward, at an interface the inner ring owns. Control flows out. The dependency points in. Those are two different questions, with two different answers, and letting them disagree is the entire trick this architecture is built on.

## 8. Wired By Hand, On Purpose

One deliberate choice this project makes, worth defending directly. There is no dependency injection container anywhere in this project. The whole object graph is assembled in main, by hand, in about twenty lines -- reach into the outermost ring for a concrete gateway class, hand it to an interactor that only ever asks for an interface. Watching those twenty lines is where dependency inversion stops being a diagram and becomes something you can point at. An annotation that did the same wiring invisibly could not teach that moment -- it would simply make it disappear. If you want to see this same graph assembled by a container instead, there is a companion project that does exactly that, and nothing else.

## 9. Add Two Things At Once

So here is the largest forced change in the category, and notice the word: added, not swapped. A batch controller, reading CSV rows the way a nightly import would. A file-backed order store, a structurally different way of keeping an order than a map ever was. Both added at the same time, both new files. And the original path -- the HTTP controller, the in-memory store -- is still sitting there, still working, completely untouched. This is not a replacement. It is proof that the architecture scales by addition, which is the harder and more useful claim.

## 10. Both Paths, Proven Rather Than Narrated

Counted from the real files on disk: two files added, one file modified -- the composition root, five lines. Fifteen classes make up entities and use cases together. Every one of them: never opened, for either addition. There is a test in this project called Both Added At Once, and it does not narrate this claim -- it runs both paths, the original and the new one, in the same test run, and asserts both succeed.

## 11. The Rule, As ArchUnit's Own API

The previous two projects in this category wrote their rule as noClasses dot that dot should. This one uses ArchUnit's own purpose-built API for exactly this shape -- named layers, and one sentence for who may reach whom. Three layers, declared by package. Entities may be reached by use cases and adapters, but reach neither. Use cases may be reached by adapters, but reach only entities. One test, three layers, the entire concentric rule -- and a second test widens an equivalent rule to the naive package and asserts it fails, naming the class that broke it.

## 12. Watching It Go Red

Here is what the build prints. It names the naive interactor, and it names the gateway it reached for. That message is the entire product of this category. Not a diagram on a wiki page that nobody has opened since onboarding -- a sentence a build produces, unprompted, the moment the rule stops being true.

## 13. The Bill

Every project in this category has to pay a bill honestly, and this one's is the largest. Count the files for one feature. Two data-transfer objects, four boundary interfaces, one interactor, two controllers, four gateways. Fourteen files, for placing an order. A simple CRUD screen built this way ends up with more interfaces than behaviour, and this is, honestly, the most over-applied pattern in the entire category. It costs real files, real indirection, and a whole team that has to understand the rule together, or it quietly decays into folders with impressive names and nothing enforcing any of them.

## 14. When This Is Too Much

So when does fourteen files for one feature pay for itself? Long-lived systems. More than one delivery mechanism, or more than one data source, genuinely -- not hypothetically. A domain worth protecting from whichever framework is fashionable this year. And when does it not? Almost everything smaller than that. If you cannot name a second delivery mechanism or a second data source that is actually going to exist, you are building the seam for a change that is never coming, and paying fourteen files for the privilege.

## 15. Thanks for Watching

That's Clean Architecture. If you take one sentence away, take this one: control flows outward; the dependency points inward; letting those two disagree is the whole of the pattern. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, try this. Add a third delivery mechanism of your own, and confirm that the use case layer needs zero lines changed to accept it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching, and I'll see you in the next one.
