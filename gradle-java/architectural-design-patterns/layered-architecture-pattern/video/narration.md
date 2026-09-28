# Layered Architecture Pattern — Video Narration Script

## 1. Layered Architecture

Hello, and welcome. This video explains the Layered Architecture pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A layered architecture splits a program into stacked groups of classes, called layers. Each layer may only depend on the layer directly beneath it. The promise is that changing one layer should not force changes in the layers above it. Think of a restaurant. The customer talks to the waiter. The waiter talks to the chef. The chef takes food from the store room. The customer never walks into the store room. But here is what people rarely say. Drawing four boxes on a whiteboard costs nothing. And nothing stops a busy developer adding one import that skips a box. So in this video, we build a real online shop with four layers. We watch someone take a shortcut, and see that nothing complains. Then we write the rule as a test, and watch it catch the shortcut. And finally, we make a real change, and count exactly what it touched.

## 2. The Scenario

Here is the job, and it stays the same for the whole video. A customer called Ada Okafor orders three things from an online shop. One espresso machine, for two hundred and forty-nine pounds. One coffee grinder, for eighty-nine pounds fifty. And two bags of coffee beans, at twenty-two pounds each. The total is three hundred and eighty-two pounds fifty. Placing that order takes four steps, in order. Check the stock, so nobody buys the last grinder twice. Take the payment. Reduce the stock and save the order. And send a confirmation email. Every version of the code in this video places exactly this order. So you can compare them fairly.

## 3. Version One — No Layers At All

We start with no layers at all. Just one class. It keeps the prices, the stock levels, the orders, and the sent emails, all as fields. And one method does the whole checkout. It works out the total, checks stock, takes the money, reduces stock, saves the order, and sends the email. Seventy-four lines, and each line is easy to read. But here is the problem. Try to test just the arithmetic, that the three items really add up to three hundred and eighty-two pounds fifty. You can't do it on its own. To create this class, you must also create its stock, its orders, and its email list. Pricing and storage are welded together, with no seam to pull them apart.

## 4. Four Layers, Stacked

So we split it into four layers. The names matter less than what each layer is not allowed to know. Layer one, at the top: presentation. It turns what the customer typed into one call. And it turns the answer back into words. Layer two: application. It runs the checkout as a fixed list of steps. Check stock, charge the card, reduce stock, save the order, send the confirmation. Layer three: domain. These are the business nouns, like an order, a price, and a product. They know nothing about the layers above or below them. Layer four, at the bottom: infrastructure. This is where orders, products, card payments and emails really live. And the rule that makes this an architecture. Each layer depends only on the layer directly beneath it. Nothing reaches back up. And nothing skips past its neighbour.

## 5. The One Call That Ruins Them

Now for the moment this whole video is about. Someone needs a new screen that lists a customer's past orders. The application layer has no method for that yet. Adding one properly means three new files. So the new screen talks to the order storage directly. Ten minutes, instead of an afternoon. It compiles. It looks tidy. The reviewer approves it. The tests pass. It ships. And here is the lesson. Nothing in the build objected. The four layers still exist, and the folder names are still right. But one screen has quietly skipped a layer, and no tool told anyone. A rule that nothing checks does not break all at once. It decays, one reasonable shortcut at a time.

## 6. Why This Keeps Happening

Why does this keep happening? Not because people are careless. Architecture is usually taught with diagrams, and with words like decoupled, maintainable, and clean. They sound like facts about the code. But a build cannot check any of them. A dependency rule is different. Presentation may not touch infrastructure. That is a sentence about imports. And a program can check imports, every single time it builds. A diagram cannot fail. A test can.

## 7. The Rule, Written Where A Build Can Read It

So here is the architecture, written as a test. It uses a small open-source library called ArchUnit. And it reads almost like English. No classes in the presentation package should depend on classes in the infrastructure package. That is one test method. It runs every time the other tests run. And it costs about thirty lines. The rule also carries a reason, written in plain words. It says that a screen reading storage directly must be changed every time storage changes, and nothing warns you. Whoever sees the failure later reads that reason too.

## 8. Watching It Go Red

Let's watch the rule catch the shortcut. A second test points the same rule at the shortcut screen from earlier. And it expects the rule to fail. Here is what the build reports. An architecture violation, found once. It names the class, Order History Screen. It names what that class reached for, the In Memory Order Table. And it even gives the line number. So a promise made at a whiteboard has become a check that fails the build, by name, in under a second. And because we have seen it fail, we can trust it when it passes.

## 9. The Forced Change

An architecture claims that some future change will be cheap. So let's make that change, and count the cost. The change: orders stop living in a simple map, looked up by order I D. Instead, they live in an append-only log, read backwards to find the latest version of each order. That is a very different way to store data. Here is the bill, counted from the real files. One file added. One file modified: the setup code, which is the only place allowed to create the storage class. And one line changed. The four layers contain seventeen classes. Sixteen of them were never opened. Not the word decoupled. A number.

## 10. And The One That Took The Shortcut

And what about the shortcut screen? Remember, it used the in-memory storage class directly. The concrete class, not the interface. So when the storage is replaced, that screen no longer compiles. It cannot accept the new storage, because it never asked for the interface. Every screen that went through the application layer was untouched. The one that took the shortcut is broken, by a change it had nothing to do with. That is the real bill for those ten minutes. And it arrives much later, on some unrelated day, when nobody remembers the shortcut was ever taken.

## 11. What This Project Does Not Fix

Now, one honest admission. This project does not solve everything. Think about what the application layer imports. The storage interface, the card payment interface, and the email interface. All three are defined down in the infrastructure layer. The rule allows that, because application sits directly above infrastructure. But it means the application layer still reaches down into infrastructure, just to know those names. The interface for storing orders lives down there, next to its implementation. Not up here, next to the code that uses it. Hexagonal Architecture, which has its own video, changes exactly this. It moves that interface up into the core, so the dependency points the other way. This project is one deliberate step before that.

## 12. An Order That Is Not Obvious

One more detail inside the application layer, because it is easy to miss. The card is charged first. Before the stock is reduced, and before the order is saved. Why? Imagine the other way round. Save the order, reduce the stock, and then charge the card. If the card is declined, you are left with a saved order, and missing stock, that should never have happened. Charging first means a declined card stops everything, before anything has changed. This is exactly the kind of decision the application layer exists to own. Once, in one place, instead of repeated on every screen that needs a checkout.

## 13. The Bill

Every pattern has a cost, so let's be honest about this one. First, indirection. Add one field to the checkout form, and it may touch three or four places. One small idea for the customer becomes several edits for you. Second, pass-through layers. Some methods in the application layer only pass a call along. That is real, and it is tedious. Third, the problem we just heard about. The application layer still has to name the storage package to compile. Layers organise the code. On their own, they do not reverse which way a dependency points.

## 14. When This Is Too Much

So when is this too much? Four layers and an architecture test are worth it when more than one caller uses the same business logic. Or when the code will outlive its first choice of storage. They are not worth it for a small script that reads a file, does one calculation, and prints the result. Four packages around fifteen lines of logic is not layering. It is just packaging. Here is a simple test. If adding the extra layer files for a new screen takes longer than the screen is worth, the layers have stopped paying for themselves.

## 15. Thanks for Watching

That's Layered Architecture. If you remember one sentence, make it this one. A layered architecture is not the four folders, it is the test that fails when someone skips one. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Widen the architecture test, so it also checks the shortcut package. Run it, and read every violation the build finds. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
