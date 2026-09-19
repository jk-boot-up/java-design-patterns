# Interpreter with SpEL Pattern — Video Narration Script

## 1. Interpreter with SpEL

Hello, and welcome. This video explains the Interpreter pattern with Spring Expression Language, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Interpreter video. That one turned promotion rules written as text into a tree of small rule objects, and applied them to orders, with a parser written by hand. This one shows the same idea inside Spring Expression Language. The plain definition, in short: SpEL is a ready made interpreter. A rule written as text becomes a tree, and the tree is evaluated against an object. By the end you will see the same promotion rules run by a library instead of a hand-built parser, then see the costs: a bigger language than you wanted, errors that arrive late, and a safety choice you must make.

## 2. The Partner Project

This video assumes the Interpreter video. If you have not seen it, start there. It turns a promotion written as text into a tree of small rule objects, with a parser written by hand, and applies it to orders. This one uses the same example. It does not teach the pattern again. It shows what Spring Expression Language does with it.

## 3. Before The First Line

Before the first line of code, what Spring Expression Language is. Spring includes an expression language, called SpEL. It parses a line of text into a tree, and evaluates the tree against any object. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. The Rules Are Text

First, the rules are text. Welcome ten: first order. UK big: country is UK, and the basket is over fifty pounds. Bulk: five items or a basket over two hundred pounds. Not UK: everyone else. Asha gets UK big. Ben gets welcome and not UK. Carol gets UK big and bulk. There is no parser in this project, and no rule class.

## 5. The Language Came Free

Second, the language came free. A conditional, a pattern match against a voucher code, and a remainder all work, and we wrote none of them. In the hand built version, each one was a new class. That is the gain. The cost is next.

## 6. Two Kinds Of Typo

Third, two kinds of typo. A syntax error, two ands in a row, is refused when the book is built. Good. A misspelled property name is accepted, because nothing checks names until there is an order. It fails when the first order arrives. The defence is a test that loads every rule against a sample order.

## 7. The Language Can Reach The Program

Fourth, the danger. In the full context, a rule can call any static method in the program. Here it only reads a system property, but it could call anything. The read only context refuses it. It also refuses method calls. Rules written by marketing are input, and input is not trusted. Use the read only context.

## 8. Missing Values

Fifth, missing values. Asha has no voucher, so reading a property of it fails. Put a question mark before the dot, and the failure becomes no match. Asha gets nothing, and Ben, who has a voucher, gets his promotion.

## 9. Parsed Once

Last, the cost of parsing. The four rules are parsed once, when the book is built. A thousand orders then go through the same four trees, and fifteen hundred promotions apply. Parsing is the expensive part, so do it at startup, not per order.

## 10. The Verdict

My verdict, plainly. Use it when rules change without a release. Parse once, at startup. Use the read only context for rules that come from people. And test every rule against real orders.

## 11. How To Recognise It

How do you recognise this in code you did not write? A spel expression parser. A value annotation with a hash and braces. Or a pre authorize annotation with a string in it.

## 12. Where You Have Met This

You have met this in every value annotation with a hash sign, and every pre authorize. Each is a SpEL expression.

## 13. What Was Used

For the record. The expression library from Spring Framework seven. No container, and no Boot runtime.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: the real parser and the real evaluation contexts. Nothing depends on timing.

## 15. When This Is Too Much

So when is it too much? For a fixed handful of rules, plain Java is simpler, and the compiler checks it.

## 16. Thanks for Watching

That's Interpreter with SpEL. If you take one sentence away, take this one: SpEL is a ready-made interpreter, and the evaluation context is the safety choice. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, try the T operator in the read only context, and read the message. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
