# Null Object Pattern — Video Narration Script

## 1. Null Object

Hello, and welcome. This video explains the Null Object pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Instead of returning nothing, return an object that does nothing. It implements the same interface as the real objects. So callers never have to check whether they got anything. Think of a blank voucher that is worth nothing. The till can accept it like any other voucher. It simply takes nothing off the price. In our online store, the thing that might not be there is a discount. In this video, null checks spread, and one gets forgotten. Then this pattern removes them. And we will hear the part most explanations leave out: how it can hide a real error. And when not to use it.

## 2. The Scenario

Here is the scenario. In our online store, most customers have no discount. Some have a loyalty discount. And a few have a staff discount. Eight different places in the checkout work out an order's price, after any discount. So here is the question. What should the discount lookup return, for a customer who has none?

## 3. Return Null

The obvious answer is null, meaning nothing. And it works, as long as everyone remembers to check. Customer one has a loyalty discount, and pays ninety pounds. Customer two has none, and pays one hundred pounds. But eight places work out the price. Seven remembered to check for null. The eighth, added last, in a hurry, did not. For customer two, it crashes with a null pointer exception. At checkout, in front of a customer.

## 4. The Check You Stop Seeing

There is another cost, beyond the crash. The same check, if the discount is not null, appears seven times. Seven identical blocks. After the third one, a reader stops noticing them. So the eighth method, the one without the check, hides in plain sight. It looks just like the others, minus four lines nobody notices are missing.

## 5. The Pattern

Now, the pattern: a No Discount object. It implements the same Discount interface as the loyalty and staff discounts. Its apply method simply returns the price, unchanged. And the lookup never returns null. For a customer with no discount, it returns this object.

## 6. Every Check Deleted

Third demo: every null check deleted. All eight methods lose their null checks. Then the same four customers run again. Ninety pounds. One hundred pounds. Seventy-five pounds. One hundred pounds. Exactly the same as before. And the eighth method, which crashed, now returns one hundred pounds. The forgotten check can no longer be forgotten, because there is nothing to remember.

## 7. The Bill: It Hides Errors

Now the cost, the part most explanations leave out. A null object can hide errors. Suppose the discount service is down. A well-meaning lookup catches the failure, and returns No Discount, to keep checkout running. Customer one is entitled to ten percent off. But is charged one hundred pounds, instead of ninety. No error. No log. No alert. Having no discount, and the service being down, now look exactly the same. That is a quieter bug than the crash it replaced, and a worse one.

## 8. Where The Line Is

So where is the line? If absence is a normal state in your business, a null object is right. Having no discount is normal. Most customers have none. But if absence means something went wrong, like the service being down, a null object is wrong. It turns a failure into a normal-looking result.

## 9. The Honest Alternatives

Fourth demo: the honest alternatives. First, Java's Optional type. Absence is written into the return type itself. Customer one has a discount, and customer two has an empty optional. And a service that is down still throws an error. It never becomes an empty optional. So the two cases can no longer be confused. And every caller must decide what absence means. The second alternative: when absence means something went wrong, throw an error, clearly.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Java's empty list is one: a list that is never null, and holds nothing. The null input stream reads nothing. A logger that does nothing, handed to code that would otherwise check whether logging is set up. And any class named no-op, or null something, with empty method bodies.

## 11. The Verdict

So, here is the verdict. Use a null object when absence is a normal state in your business. Never use one to hide a failure. And where the caller should decide what absence means, prefer Optional.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. The discount service is simulated by a switch that makes it fail. But the crash, and the silent full-price order, both really happen, in the code you just heard about.

## 13. When This Is Too Much

So, when is this too much? For a value used in only one place, a single null check is simpler. A null object earns its place when the same check would be repeated. And when absence is normal.

## 14. Thanks for Watching

That's the Null Object pattern. If you remember one sentence, make it this one. Absence can be a normal state, but it must never be a place to hide a failure. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Write a test that would catch a lookup quietly hiding a service outage. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
