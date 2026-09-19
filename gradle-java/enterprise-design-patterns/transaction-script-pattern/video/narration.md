# Transaction Script Pattern — Video Narration Script

## 1. Transaction Script

Hello, and welcome. This video explains the Transaction Script pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a transaction script organises business logic as one procedure for each request. The procedure runs as one transaction, and there are no domain objects behind it. The steps are the design. This is another project in the enterprise category, whose subject is how a business application organises its logic, its data and its requests. In our online store, the action is placing an order. By the end you will see an order placed by one procedure, see it undone as one transaction, see two scripts drift when they copy a rule, and see the bill, which is that a script grows in the middle. I will also say plainly where a script is exactly right.

## 2. The Scenario

Here is the scenario. When a customer places an order, the store checks the quantity and the stock. It takes the stock. It prices the order, with a bulk discount. It charges the card, and saves the order. The question: one method, or a set of objects?

## 3. One Request, One Procedure

First, one request, one procedure. Two mugs are ordered. The order is sixteen pounds, and the stock falls to eight. The whole business action is one method, and you read it from the top to the bottom. No order object, no rules class.

## 4. The Pattern

The pattern. One procedure for each request. It runs as one transaction. There are no domain objects behind it: the steps are the design. Anything shared goes in helper functions.

## 5. One Transaction

Second, one transaction. The card is declined after the stock was taken. The transaction undoes everything the script did. The stock is back to ten, and no order was saved. That is the reason a script is one transaction: it either all happened, or none of it did.

## 6. A Second Script Copies The Rule

Third, a second script copies the rule. The amend script needed to price a quantity, so it copied the pricing. Later the bulk discount moved from ten items to five, and one script was told. Seven mugs cost fifty pounds forty when placed, and fifty six pounds when the same order is amended.

## 7. Share A Procedure

Fourth, share a procedure. The pricing moves into one helper function that both scripts call. Now they agree. It is still procedural. There is no order object. There is a function that both scripts call.

## 8. The Bill: Growth

Fifth, the bill. The first script has three decisions, so eight paths to test. A year later, after loyalty, region and coupon rules, it has seven decisions, and a hundred and twenty eight paths. Every new rule went in the middle of one method. That is what a script costs as the rules pile up.

## 9. Where A Script Is Right

Last, where a script is exactly right. A month end job that adds up the orders: two orders, three hundred and sixteen pounds. A dozen lines, read once, changed rarely. A job with one purpose and a few rules is clearer as a script than as a set of objects.

## 10. How To Recognise It

How do you recognise this in code you did not write? A method named for a use case, such as placeOrder, that does everything from validation to saving. Service classes with long methods and no domain objects, only data holders. Two methods that each contain the same price calculation. @Transactional on a method that contains most of the business logic.

## 11. The Verdict

Here is my verdict, plainly. Use a transaction script when the logic is simple, mostly sequential and unlikely to grow, and when a team wants the shortest path from request to result. Keep shared rules in helper functions. Move to a domain model when the same rules start to appear in several scripts, or when a script's decisions outgrow what anyone can test.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? A script is the opposite of too much. Its risk is too little structure as the rules grow, so watch the decisions in the middle of the method.

## 14. Thanks for Watching

That's Transaction Script. If you take one sentence away, take this one: a transaction script is the simplest design that works, and its cost is measured in how it grows. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a fourth rule to the grown script, and count how many new paths it needs a test for. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
