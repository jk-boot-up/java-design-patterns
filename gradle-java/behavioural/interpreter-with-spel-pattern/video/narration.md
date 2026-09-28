# Interpreter with SpEL Pattern — Video Narration Script

## 1. Interpreter with SpEL

Hello, and welcome. This video explains the Interpreter pattern, in Java, using the Spring Expression Language. This video is presented by Jayasekhar Konduru. First, a simple definition. The Interpreter pattern turns sentences in a small language into a tree of objects, and then runs that tree. The Spring Expression Language, called SpEL, is a ready-made interpreter. You give it a rule written as text. It turns the text into a tree, and checks the tree against an object. Think of a calculator. You type a sum as text, and it works out the answer. You never have to build the calculator yourself. This is the framework version of the Interpreter video, with the same promotion rules for an online shop. This time, a library runs the rules, instead of a hand-built reader. Then we look at the costs: a bigger language than you wanted, errors that show up late, and a safety choice you must make.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Interpreter video. That one turns a promotion written as text into a tree of small rule objects. And it writes its own reader for the text. If you are new to the pattern, watch that one first. Here, we keep the same example, and ask what SpEL does with it.

## 3. Before The First Line

One thing is new in this project: Spring's expression language library. It reads a line of text, turns it into a tree, and evaluates that tree against any object. It replaces both the hand-written reader and all the rule classes. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. The Rules Are Text

First demo: the rules are plain text. Welcome ten: the customer's first order. UK big: the country is UK, and the basket is over fifty pounds. Bulk: five items or more, or a basket over two hundred pounds. Not UK: everyone outside the UK. Asha gets UK big. Ben gets welcome ten, and not UK. Carol gets UK big, and bulk. There is no reader in this project, and no rule classes. The library does it all.

## 5. The Language Came Free

Second demo: the language comes free. A rule can use an if-then-else, a pattern match on a voucher code, and a remainder calculation. All of them just work, and we wrote none of them. In the hand-built version, each one would have been a new class. That is the gain. Now for the costs.

## 6. Two Kinds Of Typo

Third demo: two kinds of typo. First, a grammar mistake, like two ands in a row. That is refused as soon as the rule book is built. Good. Second, a misspelled property name. That is accepted, because nothing checks names until an order arrives. So it fails later, when the first real order comes in. The defence is a test that loads every rule, and checks it against a sample order.

## 7. The Language Can Reach The Program

Fourth demo: the danger. With the full evaluation context, a rule can call any static method in the whole program. Here, it only reads a system setting. But it could call anything. The read-only context refuses that. It refuses method calls too. A rule can only read properties. Rules written by the marketing team are input. And input must never be trusted. So use the read-only context.

## 8. Missing Values

Fifth demo: missing values. Asha has no voucher. So a rule that reads a property of her voucher fails with an error. Add a question mark before the dot, and a missing voucher simply means no match. Now Asha gets nothing, without an error. And Ben, who does have a voucher, gets his promotion.

## 9. Parsed Once

Last demo: the cost of reading rules. The four rules are read and turned into trees once, when the rule book is built. Then a thousand orders go through those same four trees. Fifteen hundred promotions apply. The trees were built four times, not four thousand. Reading the text is the expensive part, so do it at startup, not for every order.

## 10. The Verdict

So, here is the verdict. Use it when rules must change without a release. Read the rules once, at startup. Use the read-only context for any rule written by people. And test every rule against real orders.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for the SpEL Expression Parser class. Look for an at Value annotation with a hash sign and curly braces. Or an at Pre Authorize annotation with a text rule inside it.

## 12. Where You Have Met This

Where have you met this before? In every at Value annotation that uses a hash sign. And in every at Pre Authorize annotation. Each of those holds a SpEL expression.

## 13. What Was Used

For the record, here are the versions. Just the expression library, from Spring Framework seven. No container, and no Spring Boot.

## 14. What Is Real Here

A quick, honest note about this demo. Everything in it is real. The real expression reader, and the real evaluation contexts. And nothing depends on timing.

## 15. When This Is Too Much

So, when is this too much? For a small, fixed set of rules, plain Java is simpler. And the compiler checks it for you.

## 16. Thanks for Watching

That's Interpreter with SpEL. If you remember one sentence, make it this one. SpEL is a ready-made interpreter, and choosing the evaluation context is your safety decision. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. In the read-only context, try a rule that calls a static method. Then read the message it gives you. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
