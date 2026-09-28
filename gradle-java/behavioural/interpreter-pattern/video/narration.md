# Interpreter Pattern — Video Narration Script

## 1. Interpreter

Hello, and welcome. This video explains the Interpreter pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Interpreter pattern is for small languages. You write one small class for each kind of phrase in the language. And bigger phrases are built by holding smaller ones. The result is a tree of objects that represents a sentence. To run the sentence, you call one method on the top of the tree. Think of a recipe card. Mix the flour and the eggs, then bake. The cook does not need a new cookbook for every cake, just a few words that combine. In this video, we write an online shop's promotion rules as simple text, instead of as code. By the end, you will know why a rule that can explain itself is worth more than a rule that merely works. And you will know this pattern's honest limit.

## 2. The Scenario

Here is the scenario. An online shop runs promotions. Each promotion has a code, a percentage off, and a rule about who qualifies. Save ten gives ten percent off for UK orders over fifty pounds. Save fifteen gives fifteen percent off for UK orders over one hundred pounds. Free ship gives five percent off for UK orders of three items or more. In Java, the first promotion is four lines of code, and there is nothing wrong with that. The trouble starts later. Each new offer gets written by copying the one above it, and changing the numbers. That is quick, and it looks correct.

## 3. Two Copies, Two Bugs, No Exceptions

Here are two copies that went wrong, in opposite directions. Save fifteen gives money away. The request said fifteen percent off baskets over one hundred pounds. The fact that it was for UK customers only was mentioned in an earlier paragraph. So nobody wrote the country check. Now every large overseas order gets fifteen percent off. On a one hundred and twenty pound order, that is eighteen pounds lost, every time. Free ship does the opposite. It was copied from an old welcome offer, and it kept that offer's first-order check. So a returning UK customer with three items gets nothing. And nobody complains, because a missing discount looks like a customer who simply did not qualify. Neither bug causes an error. Both are correct-looking code that compiled, passed review, and shipped.

## 4. The Naive Approach — Every Rule Is a Branch

Here is the shape of the naive code. One method per promotion, each with one if statement. And one method at the top that picks the best discount. Honestly, for three offers, this is fine. But think about what happens when marketing wants a new offer live by Friday. It becomes a code change, a review, a merge, and a release. And the person writing the code is not the person who understands the offer. Both bugs came from that gap. Every offer must be translated into Java by hand. And nothing ever checks the translation.

## 5. Why That Hurts

So what exactly is wrong? Five separate things. One. Every rule change is a code change. Seventy-five pounds instead of fifty means a whole release. Two. The people who own the offers cannot read the rules. So nobody can check that the code matches the request. Three. Nothing can explain itself. When a customer asks why they got fifteen percent off, the only answer is, read the source code. Four. There is no place to catch a typo. A mistyped condition is still valid Java. It compiles, deploys, and quietly does the wrong thing at checkout. And five. It gets worse over time. Each new promotion is another chance to copy the wrong condition.

## 6. The Interpreter Pattern

Here is the pattern's definition, from the famous Gang of Four book. Given a language, define a representation for its grammar, along with an interpreter that uses it to interpret sentences in the language. That sounds hard, but it is not. In plain words: write one small class for each kind of phrase. And let big phrases hold small ones. In this project, the language is promotion rules. A sentence is something like: country is UK, and basket over fifty. And interpreting it means asking a tree of rule objects whether an order matches.

## 7. An Analogy

Here is an analogy from everyday English. The phrase, the man, is a noun phrase. The phrase, the tall man in the blue coat, is also a noun phrase. One is longer, but both fit in the same place in a sentence. Either can be followed by, bought a laptop. Rules work exactly the same way. Basket over fifty is a rule. Country is UK, and basket over fifty, or first order, is also a rule. Both fit anywhere a rule fits. The grammar combines, so the objects combine.

## 8. The Roles

So here are the pieces. At the top is Rule, the shared interface. It has two methods: matches, and describe. Every rule class in the project is a Rule. Below it are just two kinds of class. The first kind are simple rules, called terminal expressions. Basket over, country is, items at least, and first order. Each makes one comparison, and holds no other rule. The second kind combine other rules, called non-terminal expressions. And, or, and not. They hold other rules, and answer by asking them. And one more piece: the order itself. That is what a rule is checked against. Only the simple rules ever look at it.

## 9. Two Kinds of Class, and That Is All

Here is the whole pattern in code. The Rule interface has two methods, and no fields. Basket over is a simple rule. It compares the basket total with a number, and describes itself as, basket over, and the number. That is the whole class. The And rule holds two other rules. It matches only when both parts match. Notice what the And rule does not know. It does not know what its parts are. Simple rules, or more And rules? How deep does the tree go? It never finds out, because it only ever asks. That is the whole trick. A rule of any size and shape is used exactly like the simplest rule.

## 10. The Tree Can Explain Itself — and Refuse a Typo

This buys two things that are easy to undervalue. The first is describe. Each rule describes its own part, and asks its parts to describe theirs. So the whole sentence can be rebuilt from the tree. And that sentence comes from the very objects the checkout obeys. Not from a copy of the text. So when a customer asks why they got fifteen percent off, the code can answer in the words the offer was written in. A test checks that reading a rule and describing it gives back the same line. The second thing is refusing typos. A rule language that guesses is worse than none. So any phrase the reader cannot understand is refused, and the phrase is named. The typo is caught when the promotion is saved, on a quiet Wednesday. Not at a busy checkout on Friday.

## 11. The Tests — Asserting the Grammar, Not Just the Answer

The project has twenty-one tests. Three are worth describing. The first checks precedence, which means which word binds tighter. A and B or C must mean: A and B together, or else C. That is how a person would say it. Swap two lines in the rule reader, and this test fails. The second is the round trip. Read a line, describe the tree, and you must get the same line back. That keeps the explanation and the decision in step. The third test checks a wrong answer, on purpose. It confirms that the naive version gives fifteen percent to an American order. Being broken is that version's whole job in this project, and the build says so out loud.

## 12. Running It

Let's run the demo. Three orders, checked both ways. The Java version gives fifteen percent to an American order. And nothing at all to a UK customer who qualifies. No error for either. The rule language gets all three right. And every discount comes with a reason, in the words the offer was written in. Then it is Friday, and marketing wants one more offer. Basket over two hundred, or items at least ten. No promotion in the shop has ever used or before. Yet adding it is one line of text. No new class, nothing recompiled, nothing deployed. And finally, a rule with a typo in it: basket ovr fifty. It is refused, by name, the moment the promotion is saved.

## 13. What to Remember

So, what should you remember? A rule written in code can only be run. A rule written in a language can be run, read, printed, checked, and changed by the person who owns it. Now, two patterns people confuse with this one. Composite is a tree of parts, where one thing and many things are treated alike. Interpreter uses exactly that tree. The difference is purpose. Composite is about structure. Interpreter is about meaning. And Strategy. The checkout holds a rule, and does not care which one. That is Strategy on the outside, with Interpreter on the inside. Now the honest costs. One class per phrase is fine for seven phrases, and painful for seventy. A language with real syntax, like brackets, needs a proper parser tool, not this pattern. The Gang of Four say exactly that. And if the rules never change, two if statements beat a language. This pattern pays off when releasing code is the bottleneck.

## 14. Thanks for Watching

That's the Interpreter pattern. If you remember one sentence, make it this one. Write one small class per kind of phrase, and your rules can be run, read, checked, and explained. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Swap the two splitting steps in the rule reader, so that and binds more loosely than or. Run the tests. Then work out which of the shop's promotions would quietly change their meaning. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
