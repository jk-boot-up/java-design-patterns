# Delegation Pattern — Video Narration Script

## 1. Delegation

Hello, and welcome. This video explains the Delegation pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Delegation is when an object does not do a job itself. Instead, it hands the job to a helper object that it holds. And that helper can be swapped. Think of a busy manager with an assistant. The manager passes the diary to the assistant. And if the assistant changes, the manager's job does not. In our online store, an order can be priced in several ways. And each new way seems to need a new kind of order. In this video, classes multiply for every way of pricing. Then an order hands its pricing to a helper. We will swap the helper, combine two helpers, and then hear the cost.

## 2. The Scenario

Here is the scenario. An order can be priced with a premium discount. Or with gift wrap. Or with both, or neither. And a customer might become premium in the middle of shopping. So here is the question. Do we need a separate class for each combination?

## 3. A Subclass For Each Way

First, the naive way: a subclass for each combination. Premium, gift wrap, and both. That is four classes, for just two features. A third feature would need eight. A premium gift order costs ninety-six pounds. But once an order exists, it can never change its class.

## 4. The Pattern

Now, the pattern. The object holds a helper. When asked to do the job, it hands the job to the helper. The helper can be swapped. And it can be combined with other helpers.

## 5. The Order Hands The Pricing On

Second demo: the order hands its pricing on. There is just one order class. With no pricing rule, the order costs one hundred pounds. With the premium rule, ninety pounds. With the gift wrap rule, one hundred and six pounds.

## 6. Change The Helper While It Lives

Third demo: change the helper while the order exists. The customer joins the premium plan, while shopping. The very same order object costs one hundred pounds, and then ninety.

## 7. Two Helpers At Once

Fourth demo: two helpers at once. Premium, and then gift wrap. The total is ninety-six pounds. Exactly the same as the special class made for both. And the number of classes added: none.

## 8. The Helper Needs To See The Order

Fifth demo: the helper needs to see the order. Gift wrap costs three pounds for each item. So the helper must look at the order it is pricing. Two items: one hundred and six pounds. Three items: one hundred and nine pounds. That is why the order passes itself in, when it calls the helper. The helper is a separate object. It does not know which order it is helping, unless it is told.

## 9. The Bill

Finally, the cost. Working out one total made three calls to helpers. Inheritance would have made none. So there is one extra hop, for every helper. To offer a helper's four methods, the order had to write four forwarding methods. They do nothing but pass the call along. And a helper knows nothing about its owner, unless it is told.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a field whose type is an interface, and a method that simply calls it. Many famous patterns are delegation with a purpose. Strategy, State, Decorator, and Proxy. Kotlin has a keyword for it, called by. And Java's unmodifiable list simply hands each call to a list it holds.

## 11. The Verdict

So, here is the verdict. When what varies is one job, prefer holding a helper, over inheriting from a parent. Pass the owner in, if the helper needs to see it. Let the helper be swapped, and combined. And accept the extra hop, and the forwarding code. Or use a language feature that writes the forwarding for you.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If there is only one fixed way to do a job, just do it directly. Delegation pays off when a job varies, or must change while the program runs.

## 14. Thanks for Watching

That's the Delegation pattern. If you remember one sentence, make it this one. Delegation hands a job to a helper you can swap and combine, and the price is an extra call, and forwarding code you must write. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a fourth rule that adds a shipping fee. And combine it with premium, without adding a class. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
