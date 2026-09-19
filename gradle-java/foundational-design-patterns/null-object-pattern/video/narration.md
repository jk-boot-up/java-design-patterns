# Null Object Pattern — Video Narration Script

## 1. Null Object

Hello, and welcome. This video explains the Null Object pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: instead of returning nothing, return an object that implements the same interface and does nothing, so callers never have to check. This is the first project in the foundational category, whose subject is how an object gets hold of another, and what happens when there is not one. Null Object answers the second half. In our online store, the thing that might not be there is a discount. By the end you will see how null checks spread and one gets forgotten, how this pattern removes them, and, the part most treatments leave out, how it can hide an error. I will also tell you plainly when I would not use it.

## 2. The Scenario

Here is the scenario. In the online store, most customers have no discount. Some have a loyalty discount, and a few, a staff discount. Eight different places in the checkout price an order after whatever discount there is. The question: what should the lookup return, for a customer who has none?

## 3. Return Null

The obvious answer is null. And it works, when everyone remembers to check. Customer one, with a loyalty discount: ninety pounds. Customer two, with none: one hundred pounds. But there are eight places that price an order. Seven remembered to check for null. The eighth, added last, in a hurry, did not. For customer two, it throws a null pointer exception, at checkout, in front of a customer.

## 4. The Check You Stop Seeing

Look at the cost, beyond the crash. The same check, if discount is not null, appears seven times. Seven identical blocks. After the third, a reader stops seeing them. So the eighth method, the one without the check, hides in plain sight. It looks exactly like all the others, minus four lines nobody notices are missing.

## 5. The Pattern

The pattern: a no discount object. It implements the same discount interface as the loyalty and staff discounts. Its apply method just returns the price unchanged. The lookup never returns null. For a customer with no discount, it returns this.

## 6. Every Check Deleted

Now delete every null check, in all eight methods. Run the same four customers. Nine thousand. Ten thousand. Seventy-five hundred. Ten thousand. Identical to before, every one. And the eighth method, that crashed, now returns ten thousand. The forgotten check is no longer possible to forget, because there is nothing to remember.

## 7. The Bill: It Hides Errors

Now the bill, the part most explanations leave out. A null object hides errors. Suppose the discount service is down. A well-meaning directory catches the failure, and returns the no discount object, to keep the checkout going. Customer one, entitled to ten per cent off, is charged ten thousand pence instead of nine thousand. No error. No log. No alert. No discount, and the service was down, now look exactly the same. That is a quieter bug than the exception it replaced, and a worse one.

## 8. Where The Line Is

So where is the line? If absence is a legitimate state of the domain, a null object is right. Having no discount is normal, most customers have none. If absence means something went wrong, the service is down, a null object is wrong. It turns a failure into a normal-looking result.

## 9. The Honest Alternatives

There are two honest alternatives. First, optional. Absence is written into the return type. No discount is an empty optional. A service that is down is still an exception. The two can no longer be confused, and every caller has to decide what absence means to it. In Java, this is often the better answer. Second, an explicit failure. When absence means something went wrong, throw.

## 10. How To Recognise It

How do you recognise this in code you did not write? Collections dot empty list is one: a list that is never null, and does nothing. Input stream null input stream reads nothing. A no-op logger, handed to code that would otherwise check whether logging is configured. And any class called noop or null, implementing an interface with empty method bodies.

## 11. The Verdict

Here is my verdict, plainly. Use a null object when absence is a legitimate state of your domain. Never use one to hide a failure. And where the caller ought to decide what absence means, prefer optional.

## 12. What Is Real Here

The same honest admission as everywhere in this course. It is all plain Java. The discount service is simulated by a switch that makes it fail. But the crash, and the silent full price order, both really happen, in the code you have just seen.

## 13. When This Is Too Much

So when is it too much? For a value with a single call site, a null check is simpler. It earns its place when the same check would be repeated, and when absence is normal.

## 14. Thanks for Watching

That's the Null Object. If you take one sentence away, take this one: absence can be a normal state, but it must never be a place to hide a failure. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, write a test that would catch a directory swallowing an outage. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
