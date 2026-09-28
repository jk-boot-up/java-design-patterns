# Transaction Script Pattern — Video Narration Script

## 1. Transaction Script

Hello, and welcome. This video explains the Transaction Script pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A transaction script organises business logic as one procedure for each request. The procedure runs as one transaction. And there are no business objects behind it. The steps themselves are the design. Think of a recipe card. Step one, step two, step three, from top to bottom. No theory, just the steps. In our online store, the action is placing an order. In this video, one procedure places an order, and undoes it as one transaction. Two scripts drift apart when they copy a rule. And we hear how a script grows in the middle. We will also hear where a script is exactly right.

## 2. The Scenario

Here is the scenario. When a customer places an order, the store checks the quantity, and the stock. It takes the items from stock. It prices the order, with a bulk discount. It charges the card. And it saves the order. So here is the question. One method, or a set of objects?

## 3. One Request, One Procedure

First demo: one request, one procedure. Two mugs are ordered. The order costs sixteen pounds, and the stock falls to eight. The whole business action is one method. You read it from top to bottom. No order object, and no rules class.

## 4. The Pattern

Now, the pattern. One procedure for each request. It runs as one transaction. There are no business objects behind it. The steps are the design. And anything shared goes into helper functions.

## 5. One Transaction

Second demo: one transaction. The card is declined, after the stock was already taken. The transaction undoes everything the script did. The stock is back to ten. And no order was saved. That is why a script is one transaction. Either all of it happened, or none of it did.

## 6. A Second Script Copies The Rule

Third demo: a second script copies the rule. The script that changes an existing order needed to price a quantity. So it copied the pricing code. Later, the bulk discount changed, from ten items to five. And only one script was updated. Now seven mugs cost fifty pounds forty when first ordered. But fifty-six pounds when the same order is changed.

## 7. Share A Procedure

Fourth demo: share a procedure. The pricing moves into one helper function, which both scripts call. Now both agree: fifty pounds forty. It is still procedural. There is no order object. Just one function that both scripts share.

## 8. The Bill: Growth

Fifth demo, and the cost: growth. The first script makes three decisions. So there are eight different paths through it, to test. A year later, after loyalty, region, and coupon rules are added, it makes seven decisions. That means one hundred and twenty-eight paths. Every new rule went into the middle of one method. That is what a script costs as the rules pile up.

## 9. Where A Script Is Right

Last demo: where a script is exactly right. A month-end job adds up the orders. Two orders, three hundred and sixteen pounds. A dozen lines, read once, and rarely changed. A job with one purpose, and a few rules, is clearer as a script than as a set of objects.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a method named after a use case, such as place order, that does everything from checking to saving. Look for service classes with long methods, and no business objects, only data holders. Look for two methods containing the same price calculation. And the at Transactional annotation, on a method holding most of the business logic.

## 11. The Verdict

So, here is the verdict. Use a transaction script when the logic is simple, runs step by step, and is unlikely to grow. And when a team wants the shortest path from request to result. Keep shared rules in helper functions. Move to business objects when the same rules start appearing in several scripts. Or when one script has more decisions than anyone can test.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? A script is the opposite of too much. Its risk is too little structure, as the rules grow. So watch the decisions piling up in the middle of the method.

## 14. Thanks for Watching

That's the Transaction Script pattern. If you remember one sentence, make it this one. A transaction script is the simplest design that works, and its cost is measured in how it grows. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add one more rule to the grown script. And count how many new paths now need a test. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
