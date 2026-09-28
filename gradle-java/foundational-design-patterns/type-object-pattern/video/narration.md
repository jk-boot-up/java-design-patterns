# Type Object Pattern — Video Narration Script

## 1. Type Object

Hello, and welcome. This video explains the Type Object pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A type object turns the kind of a thing into data. Instead of a subclass for each kind, there is one class. And each object points to a type object, which holds whatever differs. Think of a library's shelf labels. The labels say how long each kind of book can be borrowed. Change a label, and every book on that shelf follows the new rule. In our online store, books, laptops, and groceries differ in only a few numbers. Yet each one has its own class. In this video, we replace those classes with one class and some data. We will add a new kind while the program runs, change a rule in one place, and let one type inherit from another. And then the cost.

## 2. The Scenario

Here is the scenario. Books have no tax, and cost three pounds to ship. Laptops have twenty percent tax, and ship free. Groceries have five percent tax. And next month, the shop will start selling gift cards. So here is the question. Should each kind of product be its own class?

## 3. A Class For Each Kind

First, the naive way: a class for each kind. Three kinds, three classes. And they differ only in three numbers. A novel costs thirteen pounds in total. And a gift card is a fourth kind. That means a fourth class, a new build, and a new release.

## 4. The Pattern

Now, the pattern. One class for the product. A type object for its kind, which holds whatever differs. Each product points to its type. And a new kind is just a new type object.

## 5. A Type That Is Data

Second demo: a type that is data. Now there is just one product class. A novel costs thirteen pounds. A laptop costs nine hundred and sixty pounds. And a pack of tea costs six pounds twenty. A laptop can be returned after ten days. But not after twenty.

## 6. A New Kind At Run Time

Third demo: a new kind, while the program runs. Before, there are three product types. After adding gift cards, there are four. Classes added: none. A twenty-five pound gift card costs exactly twenty-five pounds. And it cannot be returned, even after one day.

## 7. Change The Type, Change Every Product

Fourth demo: change the type, and every product follows. The tax on a pack of tea is twenty pence. On a bag of coffee, forty pence. Now grocery tax is raised to ten percent, in one place. The tea's tax becomes forty pence. The coffee's becomes eighty pence.

## 8. A Type That Inherits

Fifth demo: a type that inherits. An ebook type states only its shipping cost: nothing. Its tax, which is zero, and its return period, thirty days, both come from the book type. So the ebook only states what is different.

## 9. The Bill

Finally, the costs. First, a typo in a type's name, like book spelled b o k, is only found when the program runs. With a class for each kind, that typo would not even compile. Second, laptops need their serial number checked. But a type holds data, not steps. A flag can say a check is needed, but the code that does the check lives somewhere else. Third, every new difference between kinds becomes a new field. And the code must remember to read it. This type already has six fields.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a Type, Kind, or Category object, pointed to by another object. Look for a product types table in a database, with products linked to it. Look for card types, unit types, or enemy types in games, defined in data files. And Java's own Currency, Locale, and Charset classes, which describe things as data.

## 11. The Verdict

So, here is the verdict. Use a type object when kinds differ in data, and new kinds should be added without new code. Let types inherit defaults from each other. Where kinds differ in steps, use a strategy, or a subclass. Check type names early. And keep the number of fields small.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If the kinds are few, fixed, and differ in behaviour, plain subclasses are clearer. A type object pays off when there are many kinds. Or when new kinds are added by people who are not programmers.

## 14. Thanks for Watching

That's the Type Object pattern. If you remember one sentence, make it this one. A type object turns kinds into data, so a new kind needs no new class, and the price is late errors, and behaviour that data cannot hold. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a type for frozen groceries. Make it inherit from groceries, but cost more to ship. Then check its total. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
