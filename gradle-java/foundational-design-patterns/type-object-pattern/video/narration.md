# Type Object Pattern — Video Narration Script

## 1. Type Object

Hello, and welcome. This video explains the Type Object pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a type object turns the kind of a thing into data. Instead of a subclass for each kind, there is one class, and each object points at a type object that holds what differs. This is another project in the foundational category, whose subject is how an object gets hold of another, and how small idioms shape everyday Java. In our online store, books, laptops and groceries differ only in a few numbers, yet each has its own class. By the end you will see a class for each kind that differs only in numbers, see one class with a type as data, see a new kind added at run time with no new class, see one change in a type reach every product, see a type inherit from another, and see the bill, which is typos found late and behaviour that data cannot hold.

## 2. The Scenario

Here is the scenario. Books have no tax, and cost three pounds to ship. Laptops carry twenty percent tax, and ship free. Groceries have five percent tax. Next month, the shop will sell gift cards. The question: is each kind a class?

## 3. A Class For Each Kind

First, a class for each kind. Three kinds, three classes, and they differ only in three numbers. A novel totals thirteen hundred. A gift card is a fourth kind. That is a fourth class, a new build, and a release.

## 4. The Pattern

The pattern. One class for the thing. A type object for its kind, holding what differs. Each thing points at its type. A new kind is a new type object.

## 5. A Type That Is Data

Second, a type that is data. One product class. A novel totals thirteen hundred, a laptop ninety six thousand, and tea six twenty. Laptops can be returned after ten days, but not after twenty.

## 6. A New Kind At Run Time

Third, a new kind at run time. Types before: three. After: four. Classes added: none. A twenty five pound card totals twenty five hundred, and cannot be returned after one day.

## 7. Change The Type, Change Every Product

Fourth, change the type, change every product. Tax on tea is twenty, on coffee forty. Grocery tax is raised to ten percent, in one place. Tea is now forty, and coffee eighty.

## 8. A Type That Inherits

Fifth, a type that inherits. An ebook states only its shipping: none. Its tax, zero, and its return days, thirty, come from book.

## 9. The Bill

Last, the bill. A typo, b o k, is found when the program runs. With a class for each kind, the typo would not compile. Laptops need a serial number checked, and a type holds data, not steps. A flag says so, but the code that checks it is still somewhere else. And every new difference between kinds is a new field, that the code must remember to read. The type has six fields already.

## 10. How To Recognise It

How do you recognise this in code you did not write? A Type, Kind or Category object referenced by another. Rows in a product_types table, with a foreign key from products. Card, unit or enemy types in games, defined in data files. Currency, Locale and Charset, which describe things as data.

## 11. The Verdict

Here is my verdict, plainly. Use a type object when kinds differ in data, and new kinds should be added without new code. Let types inherit defaults. Where kinds differ in steps, use a strategy or a subclass. Check the name of a type early, and keep the number of fields small.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If the kinds are few, fixed, and differ in behaviour, plain subclasses are clearer. A type object pays off when kinds are many, or added by non-programmers.

## 14. Thanks for Watching

That's Type Object. If you take one sentence away, take this one: a type object makes kinds into data so that a new kind needs no new class, and the price is late errors and behaviour that data cannot hold. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a type for frozen groceries that inherits from grocery but ships for more, and check its total. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
