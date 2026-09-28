# Chain of Responsibility Pattern — Video Narration Script

## 1. Chain of Responsibility

Hello, and welcome. This video explains the Chain of Responsibility pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. You hand a request to a line of objects, one after another. Each object either answers, and the request stops there. Or it stays quiet, and passes the request to the next one. Think of calling a support line. The first person tries to help. If they can't, they pass you on to someone more senior. You make one call, and you never need to know who will finally answer. In our online store, every order is checked before it is accepted. Is the address one we deliver to? Is the stock available? Is the order risky? And will the card cover the total? By the end, you will know why the order of those checks should be easy to change. And how this pattern differs from the Decorator pattern, which looks exactly the same on paper.

## 2. The Scenario

Here is the scenario. Before an online shop accepts an order, it checks it in four ways. One. Is the address somewhere a courier actually delivers? Two. Can the warehouse supply every item in the basket? Three. What does the fraud model think of this customer? Four. Does the card cover the total? Any one of those checks can reject the order. If none objects, the order is accepted. And here is the important part. Which checks run, and in what order, must be easy to change. For example, trade customers are invoiced at the end of the month. So they skip the card check.

## 3. Look Closely at One Order

Before any code, let's look closely at one order. Someone buys a monitor for three hundred and twenty-nine pounds. Their card has a limit of two hundred and fifty pounds. And the fraud model scores the account ninety-two out of a hundred, which is very risky. Two of our four checks would reject this order. But only one gets to speak, because the first rejection ends the checking. So which one speaks? Whichever is written first. Nobody decided that on purpose. Yet it matters a lot. It is the difference between telling the customer to try another card, and alerting the fraud team.

## 4. The Naive Approach — Four Checks, One Method

The obvious first approach is one method, with four checks, one after another. Each check can return early with a rejection. To be fair, this has real strengths. It is short, and the whole policy is in one file. For a shop with simple rules that never change, it is the right answer. But in this method, the card check comes before the fraud check. So our risky order is rejected as a card problem. The customer tries another card, and it works. There was never anything wrong with the cards. Then there is a second method, for trade customers. Someone copied the first method, and deleted the card check. But in the same edit, the address check was deleted too. So an order of two desks is now on its way to an island that no courier serves.

## 5. Why That Hurts

So what exactly is wrong? Four separate things. One. The order of the checks is fixed inside the method. Changing it means editing the file where the rules live. Two. Each check can only say yes or no. But a fraud model gives a score, and the useful part is the middle band. Those are the orders a person should review. An order scoring sixty-four is simply accepted, because there is no third answer. Three. Variations are copies, and copies drift apart. We just heard that happen. And four. To test the fraud rule, a test must first build an address, a basket and a card, that the fraud rule does not even care about.

## 6. The Chain of Responsibility Pattern

Here is the pattern's definition, from the famous Gang of Four book. Avoid coupling the sender of a request to its receiver, by giving more than one object a chance to handle the request. The key idea is not just running several checks in a row. A simple loop can do that. The key idea is that the caller does not know which check will answer. So here is the move. Instead of one method that knows all four checks, write four objects. Each one knows one check, and nothing about the others.

## 7. An Analogy

Here is an analogy to hold on to: an expenses claim at work. A forty pound lunch? Your team lead approves it. Four thousand pounds of laptops? Your team lead cannot, so it goes up to their director. Four hundred thousand pounds? That goes to the board. Three things about that office are the pattern. You submit once, without knowing who can approve what. Whoever can answer, answers, and it stops there. The board never sees your lunch receipt. And the chain of managers is not written on the claim form. The pattern's risk is there too. A claim that nobody is allowed to approve can sit in a queue forever.

## 8. The Roles

So here are the pieces, and there are only a few. The client is the checkout. It holds one screening chain, calls it once, and gets back a report. The screening chain links the checks together. It hands the order to the first check, and then waits until someone answers. The screening handler is the shared base class for every check. It holds a link to the next check, and one method for each check to fill in. Below it sit the four real checks. And what comes back is a report. It says the decision, which check made it, and which checks never ran.

## 9. The Handler — And the Line That Is Written Once

The whole pattern fits in about twenty lines, in the base class. It has one field, a link to the next check. One method that each check writes, called check. And one method that walks along the chain, called screen. Listen to what check returns. It returns an optional decision. Empty means: I have no opinion, pass it on. A decision means: I am answering, and the chain stops here. Returning nothing does not mean no. It means, not my call. The screen method is marked final, so no check can change it. In textbook versions, every check writes its own pass-along code. And a common bug is a check that forgets to pass the request on, so it silently vanishes. Here, that logic is written exactly once, and no check ever touches the next link.

## 10. The Chain — And What Silence Means

Now the chain itself, and two things are worth noticing. First, what is missing. There is no loop over the checks, and no counting. The chain hands the order to the first check, and waits for an answer. That is why reordering the checks is only a wiring change. Second, the fallback. An order really can pass every check, with nobody deciding anything. Like the expenses claim nobody can approve. So the chain must be given a fallback decision when it is built. There is no way to build one without it. Approve by default, and the chain fails open. Refer to a person by default, and it fails closed. The same checks, with opposite attitudes to risk, decided by one setting.

## 11. Two Links — And the One With Three Answers

Let's look at two of the checks, which work differently on purpose. The address check is the ordinary kind. If the country is not one we deliver to, it rejects the order, and names itself as the one who decided. If the address is fine, it returns empty, meaning no opinion. The fraud score check has three possible answers. A score of eighty or more, and it rejects. Between fifty-five and seventy-nine, it refers the order to a person. Below that, it says nothing. That third answer costs the chain nothing, because the chain never looks inside a decision. A check stops the chain whenever it is willing to own the answer. And that answer does not have to be no.

## 12. The Tests — Asserting What Did NOT Happen

The project has twenty-one tests. Two of them show the pattern best. Note that a simple test like, an order to an island is rejected, passes for the naive method too. So it proves nothing about the pattern. The first special test checks that a check behind the decision never ran. Not that its answer was ignored, but that it never ran at all. In real life, that means the payment service was never called, and never charged for. The second test uses the same four checks, but wires the card check before the fraud check. And the answer becomes the card problem again, exactly like the naive method. So the naive behaviour was not a bug in the checks. It was a setting that nobody could change without editing code.

## 13. Running It

Let's run the demo, and compare the two approaches. First, the naive method. The risky order, with a fraud score of ninety-two, is rejected as a card problem. And a trade order is accepted, for delivery to an island that no courier serves. Second, the same checks as a chain. For the monitor order, the fraud check answers, and the report says the card check never ran. For the island order, the address check answers, and three checks never ran. No warehouse lookup, no fraud model call, and nothing to pay for. That never-ran list is the real difference between a chain and a validator that collects every problem. A chain gives one answer, from one check, and stops. Finally, the trade customers. They use the standard chain, with the card check simply left out of the wiring. Nothing was copied, so nothing could go missing. And the island order is caught.

## 14. What to Remember

So, what should you remember? First, the confusion promised at the start. Chain of Responsibility and Decorator have exactly the same class structure. So you cannot tell them apart by their diagram. Instead, ask one question. Does every layer have to run? If yes, you want a Decorator. There, a layer that fails to pass the work on is a bug. If no, because one layer might settle the matter alone, you want a chain. In code, the difference is tiny. In a decorator, the call to the next object always happens. In a chain, that call sits inside an if. Now, the honest cost. A policy that once read top to bottom in one method is now spread over four check classes, a base class, and some wiring. You need a report to see who decided. And an order can reach the end with nobody answering. So if the checks and their order never change, just write the four ifs. Use a chain when you need to change the order, without editing any check.

## 15. Thanks for Watching

That's the Chain of Responsibility pattern. If you remember one sentence, make it this one. A chain passes a request along until one object is willing to answer, so the order of the checks becomes something you can change. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Take the standard chain, and move the card check above the fraud check. Run the demo, and listen to how the customer is told something different about the very same order. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
