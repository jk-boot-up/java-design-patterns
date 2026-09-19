# Specification Pattern — Video Narration Script

## 1. Specification

Hello, and welcome. This video explains the Specification pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a specification is a business rule written as an object. It can say whether something satisfies it, it can explain itself, and it combines with other rules into new ones. This is the fourth project in the domain-driven design category, whose subject is writing code that says what the business says. In our online store, the rule is what counts as a cheap product that is available. By the end you will see one rule copied into three places and drift, see it named once and combined, see it explain why a product fails, and see the bill, which is that it looks at everything.

## 2. The Scenario

Here is the scenario. In the online store, three features need the same idea: cheap and available. The search page shows such products. A promotion is offered on them. And they ship free. The question: where does the rule live?

## 3. The Same Rule, Written Three Times

First, the same rule written three times. The search page and the shipping offer agree: the blue mug and the tea. The promotion, written later, offers four. It includes a mug at exactly ten pounds, because its copy says ten pounds or less. And it includes a discontinued mug, because it forgot to check. Nobody meant that. Three copies drift.

## 4. The Pattern

The pattern. A rule is an object. It says whether a candidate satisfies it. It can say what it means, in words. And it combines with other rules, using and, or, and not, to make new ones. Written once, and used everywhere.

## 5. The Rule, Named Once

Second, the rule, named once. It reads: in stock, and under ten pounds, and not discontinued. The search page, the promotion and shipping all use it, and they all agree: the blue mug and the tea. Change the rule in one place, and all three change.

## 6. Rules Combine

Third, rules combine. A gift idea: a mug under ten pounds, or a tea that is on sale. Built from small rules with and, and or. It describes itself, and it picks out three products that are in stock. No new class was written.

## 7. A Rule Can Say Why Not

Fourth, a rule can say why not. The red mug fails on price. The old mug fails on being discontinued. The green mug fails on stock. Each explanation comes from the rule itself. Nobody wrote an error message by hand, so it cannot drift from the rule.

## 8. The Same Rule, Two Jobs

Fifth, the same rule does two jobs. It selects from a list. And it checks a single product that a customer picked, and if it fails, says why. One definition of cheap and available, used to filter, and to validate.

## 9. The Bill

Last, the bill. Ten thousand products, and sixty six matches. To find them, every one of the ten thousand was looked at. A specification runs in memory. To let a database do the work, the rule has to be turned into a query. And one more thing. For a rule used in a single place, a plain lambda is simpler than a specification.

## 10. How To Recognise It

How do you recognise this in code you did not write? An interface with a method like is satisfied by, and with and, or, and not. Classes named for a business condition, like in stock. The predicate class in the JDK, with its and, and or. And Spring Data's Specification.

## 11. The Verdict

Here is my verdict, plainly. Use a specification when a rule is needed in several places, when rules must be combined or explained, or when a rule is chosen at run time. Keep the small rules small, and name them in the business's words. Turn it into a query when the data is large. And for a rule used once, a lambda is enough.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. The drift between the three copies is real output. The catalogue of ten thousand products is built in memory, and the count of products looked at is exact.

## 13. When This Is Too Much

So when is it too much? For a condition used once, a lambda is clearer. A specification earns its place when a rule is shared, combined, or must explain itself.

## 14. Thanks for Watching

That's Specification. If you take one sentence away, take this one: a specification gives a business rule one home, so every feature that needs it agrees. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a rule for products in a given category that are also on sale, built only from the existing small rules. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
