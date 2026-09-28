# The Abstract Factory Pattern Pattern — Video Narration Script

## 1. The Abstract Factory Pattern

Hello, and welcome. This video explains the Abstract Factory pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An abstract factory is one object that creates a whole family of related objects. You choose the factory once. And everything it gives you afterwards is guaranteed to belong together. You can never accidentally mix one family with another. Think of a restaurant's set menu. You choose one menu, and every course that arrives was designed to go together. In this video, an online store's checkout sells into three countries. By the end, you will know what an abstract factory is, why it exists, and, just as importantly, when not to use it.

## 2. The Scenario

Here is the scenario. Your online store used to sell in one country. Now it sells in three. And checkout turns out to be three separate jobs. Working out the tax. Formatting the money. And checking the delivery address. In Britain, that means twenty percent value added tax, prices in pounds, and a postcode. In America, sales tax, dollars, and a zip code. In India, goods and services tax, rupees, and a pin code. Three countries, three sets of rules. And the three parts always change together.

## 3. Nine Classes, Three Legal Combinations

So you write the classes. Three tax calculators, three money formatters, and three address checkers. Nine small classes, each one easy. Picture them in a grid. Three columns: tax, money, and address. And three rows: Britain, America, and India. Each column is just an ordinary interface, with three versions. Nothing new there. But each row is more interesting. A row is a family: three objects designed to be used together. And here is the whole problem, in one sentence. There are nine classes, but only three combinations are legal.

## 4. The Problem

Without a pattern, the checkout picks each piece for itself. One chain of if statements, checking the country name, to choose the tax calculator. Another chain, on the very same name, to choose the money formatter. And a third chain, to choose the address checker. None of this is exactly wrong. It compiles, and it runs. But you have built three separate decisions that must always agree. And nothing checks that they do.

## 5. Why That Hurts

And that costs you. Reorder the cases in one chain, forget the other two, and the checkout charges British tax, but prints it in dollars. A mismatched family is one copy and paste away. When Germany arrives, you must open a class that handles real money, and edit it in three places. Your checkout should be about totals and receipts. Instead, it has become a list of nine class names. And the worst part? None of this fails loudly. It compiles, it runs, and it quietly produces a wrong invoice.

## 6. The Abstract Factory Pattern

This is exactly the problem the Abstract Factory solves. Here is its definition, from the famous Gang of Four book. Provide an interface for creating families of related objects, without naming their concrete classes. The key word is families. In plain words: choose a whole set at once, instead of one piece at a time. And if your objects have no reason to match each other, you do not need this pattern at all.

## 7. The Set Menu

Here is an easy way to remember it: ordering dinner. You can order from the full menu. Pick a starter, pick a main course, pick a wine. Three free choices. And nothing stops you putting a delicate fish next to a heavy red wine. The kitchen will serve it. It will just be wrong. Or, you order the set menu. You make one choice: the tasting menu, please. And three courses arrive that were designed together. You never named a single dish. The set menu takes away your freedom, on purpose. And that is exactly what you are paying for.

## 8. The Roles

Now let's map that onto code. There are five roles. The client is our Checkout Service. It holds one factory, and never mentions a country. The abstract factory is an interface called Market Factory. It has one creation method for each kind of product. The concrete factories are one per country. Each one builds a complete family. The abstract products are three interfaces: tax calculator, money formatter, and address checker. And the concrete products are the nine classes behind them. Here is the key point. Every product is created by exactly one factory. So there is no path that puts a British tax rate next to an American address.

## 9. The Abstract Factory

Here is the abstract factory itself, and it is smaller than you might expect. Four methods, and not one line of real code. One returns the market's name. The other three create a tax calculator, a money formatter, and an address checker. All three return interfaces. And notice what is missing. There is no parameter saying which country. The country is not an argument anywhere. Because it was already decided, the moment someone chose which factory to use.

## 10. A Concrete Factory

Here is one concrete factory: the UK market factory. It creates three things. A UK tax calculator. A pound formatter. And a postcode checker. That is the entire consistency guarantee. And it is remarkably cheap. How many lines check that these three products match? Zero. They match because this is the only place the choice is made. There is nowhere else that could get it wrong. The American and Indian factories have exactly the same shape, with different products.

## 11. The Client

Now the client, and this is the part to really listen to. In its constructor, the checkout asks the factory for four things. The market name, the tax calculator, the money formatter, and the address checker. After that, the factory is never touched again. It was a decision, not a dependency. And the method that quotes an order never mentions a country. Not Britain, not India, not anywhere. No if statements on the country at all. Even the error message is right in every market. Because words like zip code come from the products themselves.

## 12. What You Gain

So what did all that buy us? The headline: a mismatched family is not caught. It is impossible. Nothing is checked, because no code anywhere could produce one. There is now one decision, instead of three. The checkout shrank from nine class names to three interfaces, and no country codes. Adding a new market means adding files, and editing none. In fact, one test invents a German market, inside a single test method. And the unchanged checkout quotes it correctly. And finally, the British market is now a real object. Something you can build, pass around, and test.

## 13. The Honest Cost

But this pattern has a real cost, and you should know it before you use it. Adding a new country is cheap. One factory, three products, and nothing edited. But suppose checkout now needs a receipt template too. That is a new kind of product. So you must add a method to the abstract factory, and then edit every single factory. In the grid, new rows are cheap. New columns are expensive. Also, the number of classes is countries times product kinds, so be sure the families are real. And something, somewhere, still has to choose which factory to use. Here is the honest test for whether you need this. Would a mismatched pair be a bug? If not, just pass the objects in separately.

## 14. Running It

Let's run the demo. The same order, worth one hundred and twenty, is quoted in three countries. Britain adds twenty percent, and shows the total in pounds: one hundred and forty-four. America adds its sales tax, and shows dollars: one hundred and thirty dollars sixty-five. India adds eighteen percent, and shows rupees. All of that came from one method, with no condition on the country at all. Only the factory changed. And finally, the demo sends a British postcode to the American market. It is rejected, because the address checker came from the same family as the money.

## 15. Wrap Up

So, to wrap up. Use the Abstract Factory when several objects must agree with each other. And skip it when they do not, because then you are only adding classes. If you know the other factory patterns, here is how they compare. A simple factory chooses with a switch statement. A factory method chooses through inheritance. And an abstract factory chooses a whole family, all at once. And one sentence to remember. If mixing objects from different groups would be a bug, you want an abstract factory.

## 16. Thanks for Watching

That's the Abstract Factory pattern. If you remember one sentence, make it this one. Choose a whole family of objects at once, and a mismatched family becomes impossible. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. If there is a pattern you would like to see covered, suggest it in the comments. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
