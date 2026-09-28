# MVC Pattern — Video Narration Script

## 1. MVC

Hello, and welcome. This video explains the Model View Controller pattern, in Java. It is usually called M V C. This video is presented by Jayasekhar Konduru. First, a simple definition. M V C splits a screen into three roles. The model holds the data, and does the one calculation that matters. The view turns that data into text, and calculates nothing. And the controller takes the user's input, calls the model, and then asks a view to display the result. Think of a newsroom. The reporter writes the facts once. The website and the printed paper both show the same facts. Neither one is allowed to change the numbers. In our online store, a screen and a confirmation email must both show the same order total. In this video, we will see what happens when one of them works out the total for itself. Why that is a structural bug, not a typo. And which kind of M V C you have probably been using all along.

## 2. The Scenario

Here is the job. It is the same order as every project in this series. A customer called Ada Okafor buys an espresso machine, a coffee grinder, and two bags of coffee beans, for three hundred and eighty-two pounds fifty. The order has already been placed. Now Ada must be told about it, twice. Once in a summary on screen. And once in a confirmation email, a moment later. Both must say three hundred and eighty-two pounds fifty. Remember that number, because for a while, one of them will not agree.

## 3. Version One — No Separation At All

We start with no separation at all. One class checks the stock, takes the payment, and writes the screen text, all in one method. It works. And because there is only one calculation, the checkout and the screen text cannot disagree. Its problem is different. You cannot test whether the summary reads correctly, without running a whole checkout at the same time. They are the same fourteen lines. That is the cost of no separation. But as we will hear shortly, the wrong kind of separation costs more.

## 4. Three Roles

So here are the three roles, and what each one is not allowed to know. The model holds the order's lines, and its one total. It does not know how it will be shown: on a screen, in an email, or anywhere else. The view turns the model into text. It calculates nothing. No adding, no rounding, no percentages. If a view does arithmetic on a price, something has already gone wrong. The controller places the order, and builds exactly one model from it. Then it hands that same model to every view that needs it. Here is the key sentence of this video. Two views cannot disagree about a number that neither of them is allowed to calculate.

## 5. The Shortcut

Now for the moment this video is about. The screen already works, reading the model. Then someone is asked to write a confirmation email. They want tidy prices, rounded to the nearest pound. The model has no method for that. So instead of asking for one, the new email view reads the product catalogue directly. And it rounds each price before multiplying. It compiles. A reviewer sees a small, tidy view, and approves it. But it prints a different total. The coffee grinder costs eighty-nine pounds fifty. Rounded, it becomes ninety, and the fifty pence never comes back. So the screen says three hundred and eighty-two pounds fifty. And the email says three hundred and eighty-three pounds. Nothing in the build objected. The customer sees one number at checkout, and a different one in their inbox, thirty seconds later.

## 6. The Whole Mechanism, In One Interface

So how does the pattern prevent this? Not with a warning. With an interface that is simply too narrow to allow the mistake. Every view has exactly one method, called render. It takes one thing: the finished order summary model. There is no way to hand a view a product, a price, or a quantity. So a view has nothing to calculate a total from. That is exactly why the rounding email had to go around this interface, and read the catalogue directly. Going around the model was the only way the bug could ever happen.

## 7. Classic MVC, And The MVC You Have Used

Now, which M V C do we mean? There are two main kinds. The original, classic M V C comes from a language called Smalltalk. There, the view watches the model. When the model changes, every view redraws itself automatically. Web M V C, the kind used by Spring, Rails and Django, works differently. The controller builds a model once, and hands it to a template. The template renders the page once, and it is done. Nothing keeps watching. If you have written a web controller that adds values to a model and returns a view name, you have used this second kind. This project's controller builds the model once, and hands it to its views. So it is closer to the web kind.

## 8. MVP And MVVM, In One Scene

Two related names often come up, so let's separate them. M V P stands for Model, View, Presenter. Here the view is completely passive. It never touches the model. A presenter reads the data, and pushes it into the view. That makes the view easy to fake in a test. M V V M stands for Model, View, View Model. Here the view is bound to the view model's properties. When a property changes, the screen updates by itself, with no explicit push. Many modern user interface frameworks work this way. Teaching either one properly needs a real user interface toolkit, so this video stops here. The short version. In M V C, the view may read the model. In M V P, it may not. And in M V V M, it is bound to it automatically.

## 9. The Rule, Written Where A Build Can Read It

The narrow interface is the main defence. This project also adds a rule, written as a test with a library called ArchUnit. No class in the view package may depend on any class in the infrastructure package. In plain words, a view may not reach into storage or the catalogue. That is exactly how the rounding email got the numbers to do its own sum. The test runs with every other test. And a second test points the rule at the shortcut version, and expects it to fail.

## 10. Watching It Go Red

So what does a failure sound like? The build reports an architecture violation, found once. It names the class, Rounded Email View. And it names what that class reached for, the Product Table. The promise that the email never touches the catalogue is no longer just a promise. It fails the build, by name, in under a second.

## 11. The Forced Change

Now let's do it properly. The change: add a real second view, the email, using the same model. Counted from the real files. One file added: the new email view. One file modified: the setup code, which passes one extra argument. Two lines changed. The model, the controller and all the views make twenty-one classes. Twenty of them were never opened. And here is the part a file count cannot show. The new email's total is not just checked to match the screen. It is guaranteed to, because the email view contains no arithmetic at all. It cannot calculate a wrong answer, because it cannot calculate any answer.

## 12. Both Views, Every Time

Let's run it. The screen says three hundred and eighty-two pounds fifty. The email says three hundred and eighty-two pounds fifty. Not because someone tested both, and they happened to match today. Because there is exactly one place in the program that can produce an order total. And both views read it from there. Run it with a thousand different orders, and they will agree every time. The email view is simply unable to disagree.

## 13. The Bill

Every pattern has a cost, so let's name this one honestly. First, a narrow view interface is a real limit. If a view truly needs something the model does not offer, the honest fix is to widen the model, for every view. Not to reach around it. And no test will stop a model slowly growing methods that only one view ever uses. Second, and most common: controllers grow. Adding just one more check to the controller is always easier than finding the right home for it. This project's controller is only three calls long, on purpose. Keeping it short is a discipline the pattern does not enforce for you.

## 14. When This Is Too Much

So when is this not worth building? M V C earns its keep when more than one output must show the same state. A screen and an email. A screen and a receipt. A desktop app and a command line. It is not worth it when there is exactly one output, and there will never be a second. Then a single method that calculates and prints is not a shortcut. It is all you need.

## 15. Thanks for Watching

That's M V C. If you remember one sentence, make it this one. Two views cannot disagree about a number that neither of them is allowed to calculate. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a method to the model that gives prices rounded to the nearest pound. Then change the shortcut email to use it, instead of reading the catalogue. Both totals will agree, because there is no arithmetic left in the view to get wrong. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
