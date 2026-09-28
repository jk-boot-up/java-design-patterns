# Specification Pattern — Video Narration Script

## 1. Specification

Hello, and welcome. This video explains the Specification pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A specification is a business rule, written as an object. It can say whether something meets the rule. It can explain itself. And it can combine with other rules to make new ones. Think of a job advert's requirements. Speaks English, and has a driving licence, and lives nearby. Each part is simple, and together they describe exactly who fits. In our online store, the rule is: which products are cheap, and available? In this video, one rule is copied into three places, and drifts apart. Then it is named once, and combined. We will hear it explain why a product fails, and then the cost.

## 2. The Scenario

Here is the scenario. In our online store, three features need the same idea: cheap, and available. The search page shows those products. A promotion is offered on them. And they get free shipping. So here is the question. Where should the rule live?

## 3. The Same Rule, Written Three Times

First, the naive way: the same rule, written three times. The search page and free shipping agree. The blue mug, and the tea. But the promotion, written later, offers four products. It includes a mug at exactly ten pounds, because its copy says ten pounds or less. And it includes a discontinued mug, because it forgot to check. Nobody meant that. Three copies simply drift apart.

## 4. The Pattern

Now, the pattern. A rule becomes an object. It says whether something meets it. It can describe itself, in words. And it combines with other rules, using and, or, and not. Written once, and used everywhere.

## 5. The Rule, Named Once

Second demo: the rule, named once. It reads: in stock, and under ten pounds, and not discontinued. The search page, the promotion, and free shipping all use it. And now they all agree: the blue mug, and the tea. Change the rule in one place, and all three features change together.

## 6. Rules Combine

Third demo: rules combine. Here is a gift idea rule. A mug under ten pounds, or a tea that is on sale. It is built from small rules, joined with and, and or. It describes itself in those words. And it finds three products that are in stock. No new class was written.

## 7. A Rule Can Say Why Not

Fourth demo: a rule can explain why not. The red mug fails on price. The old mug fails because it is discontinued. The green mug fails because it is out of stock. And the blue mug qualifies. Each explanation comes from the rule itself. Nobody wrote an error message by hand. So the message can never drift away from the rule.

## 8. The Same Rule, Two Jobs

Fifth demo: one rule, two jobs. First, it selects from a list, and finds two products. Second, it checks a single product a customer picked. The old mug is refused, with the reason: it is discontinued. One definition of cheap and available, used both to filter, and to check.

## 9. The Bill

Finally, the cost. Ten thousand products, and sixty-six matches. But to find them, all ten thousand were checked. A specification runs in memory. To let a database do the searching instead, the rule must be turned into a database query. And one more thing. For a rule used in only one place, a simple lambda is easier than a specification.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for an interface with a method like, is satisfied by, together with and, or, and not. Look for classes named after a business condition, like In Stock. Look for Java's Predicate interface, with its and, and or methods. And look for Spring Data's Specification.

## 11. The Verdict

So, here is the verdict. Use a specification when a rule is needed in several places. Or when rules must be combined, or explained. Or when a rule is chosen while the program runs. Keep the small rules small, and name them in the business's own words. Turn it into a database query when the data is large. And for a rule used only once, a lambda is enough.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. The drift between the three copies is real output. The catalogue of ten thousand products is built in memory. And the count of products checked is exact.

## 13. When This Is Too Much

So, when is this too much? For a condition used only once, a lambda is clearer. A specification earns its place when a rule is shared, combined, or must explain itself.

## 14. Thanks for Watching

That's the Specification pattern. If you remember one sentence, make it this one. A specification gives a business rule one home, so every feature that needs it agrees. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a rule for products in a given category, that are also on sale. And build it only from the existing small rules. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
