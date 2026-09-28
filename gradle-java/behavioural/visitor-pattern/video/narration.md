# Visitor Pattern — Video Narration Script

## 1. Visitor

Hello, and welcome. This video explains the Visitor pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Visitor pattern lets you add a new operation to a set of objects, without changing those objects. You write the operation as its own class, called a visitor. You hand it to each object in turn. And each object calls back the one method on the visitor that fits its own type. Think of inspectors visiting a building. A fire officer, a valuer, and a census taker each walk the same rooms. But each one does a completely different job. In this video, an online shop's catalog is a tree of categories, products, and bundles. The business keeps asking new questions about it. Each question becomes a visitor. By the end, you will know what double dispatch means. And, more usefully, when this pattern is the wrong answer.

## 2. The Scenario

Here is the scenario: the shop's catalog. It is a tree. Categories hold products, and other categories. And it has looked like that since the shop opened. What changes is not the tree. It is the questions the business asks about it. Finance wants the value of the stock, and a spreadsheet every Monday. Merchandising wants a count of items in each category. Shipping wants to know which items cannot simply be boxed and posted. Four questions, one structure. And next month there will be a fifth. That shape is the only situation where this pattern is worth its cost.

## 3. Two Kinds of Node, and They Are Not Alike

Before the design, let's compare two kinds of item, because everything depends on their difference. A product is one item on the shelf. It has a price, a stock level, and maybe a restriction. For example, a lithium battery needs a dangerous goods declaration if it flies. A bundle is a kit sold as one thing. The starter kit is a phone, a case, and a spare battery, for six hundred and thirty-nine pounds. Now ask both of them two questions. First: what are you worth? A product is its price times its stock. A bundle is its kit price times its stock, not the sum of its parts. Second: are you restricted? A product either is, or is not. A bundle has no restriction of its own. It is restricted by what is inside the box.

## 4. The Naive Approach — A Method Per Report

The obvious approach is to add each report as a method on the catalog items. After four reports, the shared interface has methods for value, counting, spreadsheet export, and the compliance audit. Is spreadsheet export really about a product? No. It is a rule from a file format. A field containing a comma must be wrapped in quotes. Yet that rule now lives inside a class that describes a thing on a shelf. To be fair, this design is not foolish. Each method is the shortest correct answer to its question. And the naive stock value matches the visitor version, to the penny. The trouble arrives with the fourth report, in the third year.

## 5. Why That Hurts

Here is what goes wrong, in order. One. Every new report changes the catalog classes themselves. The quoting rule now lives in two item classes. Two. Knowing something twice is how it comes to be known differently. The bundle class was written later, by copying the product class, and the copy dropped the quoting. Then marketing renamed the kit to, Starter Kit, comma, three items. And one row of the finance spreadsheet quietly gained an extra column. Three, and this one really matters. The compliance check was copied too. The bundle version reads the bundle's own restriction, which is never set. So the starter kit, with a lithium battery inside, is missing from the dangerous goods report. And a shipment goes out marked as safe for air freight. Nobody wrote that bug on purpose. And every new report means another method, in every item class.

## 6. The Visitor Pattern

Here is the pattern's definition, from the famous Gang of Four book. Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new operation, without changing the classes of the elements it works on. That second sentence is a promise about change. This is not a way of walking a tree. It is a way of choosing which kind of change will be cheap. And notice what the definition does not say. It says nothing about adding new kinds of element. That silence is the whole cost of the pattern.

## 7. An Analogy

Here is an analogy: a building, and the people who inspect it. The fire officer checks the exits. The valuer estimates what it is worth. The census taker counts the people. Three completely different jobs. The caretaker walks each inspector along the same route, through the same doors, in the same order. The caretaker does not care what they are looking for. And the inspectors do not need to know the layout. Now a new kind of inspector arrives, an accessibility auditor. They join the walk, and nothing in the building changes. That is the benefit. But add a new kind of room, like a server room. Now every single inspector must be told what to do in it. That is the cost, and it arrives every time the building changes shape.

## 8. The Roles

Here are the pieces, and the shape to remember is two families side by side. On one side, the catalog, with three item types: product, bundle, and category. That family is finished, and has been for years. On the other side, the reports. A Catalog Visitor interface, and six visitors below it. Stock value, category count, spreadsheet export, compliance audit, a trace, and a low stock report. That family grows every month. The catalog only depends on the visitor interface. No item knows that any particular report exists. Count them: three item types, six visitors. Adding a visitor is free. Adding an item type means editing all six visitors. Those two numbers are the whole argument, for and against this pattern.

## 9. The Element and the Visitor

Here is the whole pattern, and it is smaller than its reputation. Every catalog item has a method called accept, which receives a visitor. That is the last method the item interface will ever need. The visitor interface has one visit method for each item type. Visit a product, visit a bundle, and visit a category. They share the same name, and differ only by the type they receive. There is also a leave method, called on the way back out of a category. So a report can keep track of which category it is in. And inside each item class, accept is just one line. It calls the visitor's visit method, passing itself. The same line, in all three classes. So why not write it once, in one place? That is the next question, and the only truly hard idea here.

## 10. Why accept Has To Exist

Imagine you have a catalog item, but your variable only says it is a catalog component. Try calling the visitor's visit method with it directly. It will not compile. Java chooses between same-named methods using the type the compiler can see, at that line. All it can see is a catalog component. And there is no visit method for that. It does not matter that the object really is a product. Now move the same call inside the product class. There, the compiler knows it is a product. So it picks visit product. So there are two hops. The first hop, calling accept, finds which item we are on, at run time. The second hop, calling visit, picks which report method runs. Together, they choose a method based on two types at once. That is called double dispatch. Is it awkward to read? Yes. That is a fact about Java's rules, not about catalogs.

## 11. The Walk, and Two Reports

Now three pieces of real code. First, the walk, inside the category class. The category visits itself, then passes the visitor to each child, and then says it is leaving. Always in the same order, so today's spreadsheet can be compared with yesterday's. That walk is written once, and every report gets it for free. Second, the stock value report. A product is worth its price times its stock. A bundle is worth its kit price times its stock. Two plain rules, with no if statements, and no type checks. Third, the compliance rule the naive version lost. A bundle is restricted by what is inside it. So the visitor loops over the bundle's contents. And that loop lives in the one report that needs it.

## 12. The Tests — Asserting What Only Visitor Gives You

Two tests are worth describing. A test that checks the stock total proves nothing about the pattern, because the naive version passes it too. The first test proves the pattern's promise. A brand new report is written inside the test file. It walks a catalog whose classes were written long before it existed. No catalog file was opened, and it works. The second test deliberately shows a cost. A report that only cares about accessories is offered seven items, and only wants five. It cannot skip the rest. The walk belongs to the catalog, so the report must filter, and still do the whole tour.

## 13. Running It

Let's run the demo. First, the naive design. The bundle's spreadsheet row has eight fields, where every other row has seven. And the compliance report has two findings, but the starter kit is not one of them. Now the same catalog and the same four questions, as visitors. The bundle's name is quoted correctly, because one quoting rule, in one class, handles every item. And the audit now has three findings. The starter kit is on the list, because of the spare battery in the box. It is no longer marked safe for air freight. Finally, the part not to skip. Add one new item type, such as a gift card. Every one of the six visitors stops compiling, until a method is written for it. The naive design would have needed only one new class.

## 14. What to Remember

So, what should you remember? Accept exists because Java chooses methods by the type the compiler can see. Two hops to reach one method, and it is never obvious to a new reader. The trade is this. A new operation costs one new file, and zero edits. A new item type costs one method, in every visitor you have ever written. So before you choose, count two numbers in your own code. How many item types, and how many operations on them. Which one grew last year? Whichever is growing must be the cheap one. For a shop catalog, operations grow, so Visitor fits. For something still gaining new kinds of item, it is the other way round. And with only two operations, on a tree that never changes? Just write the two methods, on the items.

## 15. Thanks for Watching

That's the Visitor pattern. If you remember one sentence, make it this one. Visitor makes new operations cheap, and new item types expensive, so use it only when operations are what keep growing. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try, and it is the uncomfortable one. Add a gift card item type. Then fix every visitor the compiler complains about. And count how many needed a real rule, and how many just got an empty method. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
