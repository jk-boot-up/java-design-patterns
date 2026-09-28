# Clean Architecture Pattern — Video Narration Script

## 1. Clean Architecture

Hello, and welcome. This video explains Clean Architecture, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Clean Architecture arranges a program in rings, like the layers of an onion. The most important rules sit in the middle. The technical details sit on the outside. And there is one rule. Code may only depend on things further in. Never on things further out. Think of a castle. The treasure is in the keep, at the centre. The walls and the gates are outside it. You can rebuild a gate without touching the treasure. In this video, we apply that to an online shop that places an order. It is a close relative of Hexagonal Architecture, and we will say plainly what is new. By the end, you will know the one trick the whole pattern rests on, in a single sentence.

## 2. The Scenario

Here is the job. It is the same order as every project in this series. A customer called Ada Okafor buys an espresso machine, a coffee grinder, and two bags of coffee beans. The total is three hundred and eighty-two pounds fifty. To place that order, the program needs four things. A catalogue, to check stock. A payment gateway, to take the money. Somewhere to store the order. And a way to notify the customer. Each of those four needs is written as an interface. And the use case itself, the code that places the order, owns all four.

## 3. The Naive Version

Let's start with the naive version. It is a class that calls itself a use case. But its constructor asks for three concrete classes: an in-memory order store, an in-memory product list, and an in-memory payment gateway. Not interfaces. Real, specific classes. Does it work? Yes. It places the order correctly. The problem is where it reaches. It sits near the centre, but it names classes from the outer rings. So to test it, you must build all three of those classes first. And to swap any one of them, you must open and edit this file.

## 4. Four Circles, One Rule

Now, the four rings, from the inside out. Ring one, at the centre: entities. These are the business nouns, like an order, a price, and a product. They are true even if nothing else is running. Ring two: use cases. This is the code that does the job, like placing an order. It declares interfaces for everything it needs. Ring three: interface adapters. Controllers bring requests in. Gateways take calls out, to real storage. Ring four, on the outside: frameworks and drivers. In this project, that is just the main method that wires everything together. And the one rule. Code may only depend on things further in. Not mostly. Always. Even late on a Friday, when a shortcut looks tempting.

## 5. This Is Not Hexagonal Again

Is this just Hexagonal Architecture again? Partly, yes. The centre is the same, and so is the rule about which way dependencies point. But there are four real differences. One. The single outside world of Hexagonal is split into named rings. Translating between the use case and the outside world is treated as its own job, with its own ring. Two. We will see the key idea, called dependency inversion, happen in real code, not just in a picture. Three. The big change later in this video adds two new things at once, instead of swapping one. And four. This pattern is used far more often than it should be. So later on, we will count its real cost.

## 6. The Real Graph, Wired By Hand

Now the proper version, running. A pretend web request arrives at a controller. The controller calls one method on the use case's own interface. The order is created, with status two hundred and one, and a total of three hundred and eighty-two pounds fifty. Now think about the use case class itself. It imports from only two places: the entities, and its own use-case package. Not a single adapter. So who connects it to the real gateways? The main method does. It creates four real gateways, and hands them to the use case, by hand. About twenty lines of code. No framework, and nothing hidden.

## 7. The Dependency-Inversion Moment

This is the most important idea in the video, so let's go slowly. The use case calls orders dot save. Here, orders is an interface called Order Repository. That interface is declared in the use case's own package, in the inner ring. The class that really stores orders lives two rings further out. It implements that interface. Now, ask two separate questions. First question. When this line runs, where does the program go? Outward, into the outer class. That is the direction of control. Second question. What must exist for this file to compile? Only the interface, which lives in the inner ring. So the dependency points inward. Control flows out. The dependency points in. Letting those two directions disagree is the whole trick of this architecture.

## 8. Wired By Hand, On Purpose

One choice in this project deserves an explanation. There is no dependency injection framework here at all. Instead, the main method builds everything by hand, in about twenty lines. It takes a real gateway from the outer ring. And it hands it to a use case that only knows the interface. Why do it by hand? Because you can read those twenty lines, and see the inversion happen. A framework annotation would do the same wiring invisibly, and the lesson would disappear with it. If you want to see the same program wired by a framework instead, there is a companion project that does exactly that.

## 9. Add Two Things At Once

Now, the biggest change in this series. And listen for the word: we add, we do not swap. First new thing: a batch controller. It reads orders from rows of a file, the way a nightly import would. Second new thing: a store that keeps orders in a flat file, instead of in memory. Both are added at the same time, as new files. And the original path, the web controller and the in-memory store, is still there, and still works. The imported order comes through, for two hundred and forty-nine pounds. And the use case file? Zero lines changed. The web controller? Zero lines changed. The architecture grew by adding, which is the harder and more useful promise.

## 10. Both Paths, Proven Rather Than Narrated

Let's count exactly what changed. Two files were added: the batch controller, and the file-based store. One file was modified: the main method, and only five lines of it. Together, the entities and the use cases are fifteen classes. Not one of those fifteen was opened for either change. And this is not just a claim. A test in the project runs both paths, the old one and the new one, in the same run. And it checks that both succeed.

## 11. The Rule, As ArchUnit's Own API

How do we stop someone breaking the rule by accident? We turn the rule into a test, using a library called ArchUnit. The test names three layers, by package. Entities, use cases, and adapters. Then it says who may use whom. Entities may be used by use cases and by adapters, but they use neither. Use cases may be used by adapters, but they only use entities. One test holds the whole ring rule. And a second test points the same rule at the naive version from the start. That test is expected to fail, and to name the class that broke the rule.

## 12. Watching It Go Red

So what does a failure sound like? The build reports an architecture violation. It names the naive use case class. And it names the in-memory order store that the class reached out for. That message is the real product of this whole series. Not a diagram on a wiki page that nobody reads. A clear sentence from the build, the moment the rule stops being true.

## 13. The Bill

Every pattern has a cost, and this one has the biggest bill in the series. Let's count the files for this one feature, placing an order. Two data transfer objects. Four boundary interfaces. One use case. Two controllers. And four gateways. Fourteen files, to place an order. A simple screen that just reads and writes records would end up with more interfaces than actual behaviour. Honestly, this is the most over-used pattern in the series. And without a team that understands the rule, it slowly decays into folders with impressive names, and nothing enforcing them.

## 14. When This Is Too Much

So when are fourteen files worth it? For systems that will live for many years. For systems with more than one way in, or more than one place to store data, for real, not just in theory. And for business rules worth protecting from whatever framework is popular this year. And when is it not worth it? Almost everything smaller than that. If you cannot name a second way in, or a second data store, that will actually exist, you are paying fourteen files for a change that will never come.

## 15. Thanks for Watching

That's Clean Architecture. If you remember one sentence, make it this one. Control flows outward, the dependency points inward, and letting those two disagree is the whole pattern. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a third way into the program, of your own. Then check that the use case layer needs zero lines changed to accept it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
