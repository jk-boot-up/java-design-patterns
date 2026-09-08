# Chain of Responsibility Pattern — Video Narration Script

## 1. Chain of Responsibility

Hello, and welcome. This video explains the Chain of Responsibility pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. You hand a request to a line of objects, one after another, until one of them takes it. Each one either answers, and everything stops there, or says nothing and passes the request along. That's the idea in a sentence. The rest of the video does it properly, by building a real working Java project: the checks an online store runs before it accepts an order. Is the address deliverable, can the warehouse pick it, what does the fraud model think, will the card cover the total. By the end you'll know why the order of those checks should be something you can change, and what separates a chain from a decorator — the pattern it is most often mistaken for.

## 2. The Scenario

So, imagine an online shop. Before an order is accepted we check it four ways. Is the address somewhere a courier actually goes. Can the warehouse pick every line in the basket. What does the risk model think of this customer. And does the card cover the total. Any one of those can reject the order. If none of them objects, we accept it. And here is the part that matters. Which checks run, and in what order, is something we need to change. Trade accounts don't get a card check, because they're invoiced at the end of the month. That one sentence is the whole problem.

## 3. Look Closely at One Order

Before any code, look closely at one order. A three hundred and twenty nine pound monitor, on a card with a two hundred and fifty pound limit, from an account the risk model scores ninety two out of a hundred. Two of our four checks would reject this. Only one of them gets the chance, because the first rejection ends the screening. So which one? Whichever is written first. Nobody decided that. And the difference between the two answers is the difference between telling a customer to try another card, and telling the fraud team an account exists.

## 4. The Naive Approach — Four Checks, One Method

The obvious first move is one method with four checks in it and an early return on each. I want to be fair to this, because the whole argument depends on it. It is short, the entire policy is in one file, and a new joiner can tell you what it does in thirty seconds. For a shop with one market and rules that never change, this is the right answer. But look at the third line and the fourth. The card is checked above fraud. Our order is rejected as a card problem, the customer tries another card, and it works — because there was never anything wrong with the cards. And then the second method. Trade accounts are invoiced, so somebody copied the first one and deleted the card check. In the same edit, the address check went too. Two desks are now on their way to Jersey.

## 5. Why That Hurts

Let's be precise, because it is four separate things. One. The order of the checks is welded into the method, so changing it means editing the file the rules live in. Two. The answer is a yes or a no, so there is no third answer. A risk model gives you a score, and the reason anybody pays for one is the band in the middle — the orders a human should look at. Sixty four gets accepted, because there is nowhere else to put it. Three. Variants are copies, and copies drift. We just watched that happen. And four. The fraud rule is the fourth statement, so to reach it a test has to build an address, a basket and a card that the fraud rule does not care about.

## 6. The Chain of Responsibility Pattern

Here is the definition from the Gang of Four book, and the first half is the half everybody skips. Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. The pattern is not really about running several checks in a row. You can do that with a loop. It is about the caller not knowing which of them will answer. So the move is this. Stop writing one method that knows all four checks. Write four objects that each know one check, and none of the others.

## 7. An Analogy

Here's the analogy to hold on to. An expenses claim. A forty pound lunch receipt, and your team lead approves it. Four thousand pounds of laptops, and your team lead cannot — that goes up to their director. Four hundred thousand goes to the board. Three things about that office are the pattern. You submit once, and you don't have to know the thresholds. Whoever can answer, answers, and it stops there — the board never sees your lunch receipt. And the hierarchy is not printed on the claim form. The failure mode is the pattern's too. A claim nobody is allowed to approve sits in a queue forever.

## 8. The Roles

So here are the pieces, and there aren't many. The client is the checkout. It holds one thing, a screening chain, calls screen once, and gets back a report. Screening chain is the wiring. It links the handlers together, hands the order to the first one, and then does nothing until somebody answers. Screening handler is the abstract link: one field pointing at the next link, and one method for subclasses to write. Underneath sit the four checks. And coming back out is a report: the decision, who made it, and which links never ran.

## 9. The Handler — And the Line That Is Written Once

This is the whole pattern, and it's about twenty lines. One field, the next link. One method for subclasses to write, called check. And one method that walks the chain, called screen. Look at what check returns. An Optional of a decision. Empty means: I have no opinion, pass it on. A decision means: I am answering, and the chain stops here. Half the confusion about this pattern is people reading returns nothing as says no. Now look at the word final in front of screen. In the textbook version every handler writes its own if-and-else, and the bug everybody hits is a handler that declines and forgets the else. The request vanishes, with no error. Here there is one copy of that logic, and a link author never touches the next link at all.

## 10. The Chain — And What Silence Means

Here's the chain itself, and two things are worth pointing at. The first is what isn't here. No loop over the handlers, no index, no count. It hands the order to the first link and doesn't see it again until somebody answers. That's what makes reordering a wiring change. The second is that or-else fallback. This is the expenses claim nobody can approve — an order really can pass every link with nobody deciding anything. So the fallback is a constructor argument, and there is no constructor without one. Approve by default, and you fail open. Refer by default, and you fail closed. Same links, opposite risk appetites, one argument apart.

## 11. Two Links — And the One With Three Answers

Two of the links, on purpose different shapes. Address check is the ordinary case. It rejects, and it names itself while doing it, so the answer carries the word address in a field rather than buried in a sentence. And when the address is fine it returns empty — no opinion. Fraud score check is the one with three answers. Eighty and above, it rejects. Between fifty five and seventy nine it refers, so a human looks at it. Below that it says nothing. That third answer costs the chain nothing, because the chain never looks inside the decision. A handler stops the chain whenever it is willing to own the answer — and the answer does not have to be no.

## 12. The Tests — Asserting What Did NOT Happen

Twenty one tests, and these two make the point. A test that says a Jersey order gets rejected passes against the naive method just as happily as against the chain. It proves nothing about the pattern. The first one asserts that a link behind a decision never ran. Not that its answer was ignored — that it never ran at all. That's the risk model not being called, and not being billed for, written as an assertion. The second is my favourite. Same four link classes, wired with payment above fraud, and the answer becomes the card again — the naive behaviour, reproduced exactly. It was never wrong. It was a setting you couldn't change without editing code.

## 13. Running It

Run it, and the two halves sit side by side. Section one is the naive method: a fraud score of ninety two reported as a card problem, and a trade order accepted for delivery to an island no courier serves. Section two is the same checks as links. Read the lines that begin never ran. On the monitor, fraud answers and the card link never runs. On the Jersey order, three links never ran — no warehouse query, no risk model call, nothing billed for. That never-ran line is the real difference between this pattern and a validator that collects every problem. A chain gives you one answer, from one link, and stops. And section four is the trade flow: the standard chain with one link left out of the wiring. Nothing was copied, so nothing could go missing, and Jersey is caught.

## 14. What to Remember

So, what to take away. First, the confusion I promised to clear up. Chain of responsibility and decorator have the same class diagram. Not a similar one, the same one — so any explanation that separates them by structure is wrong. The difference is one question you can ask before writing either. Does every layer have to run? If yes, you want a decorator, and a layer that declined to pass the work on would be a bug. If no — a layer might settle the matter by itself — you want a chain. In code that difference is one character deep. In a decorator, the call to the next object always happens. In a handler, it's inside an if. Now the bill, honestly. A policy that read top to bottom in one method now lives across four check classes, a base class and a line of wiring. You need a report to see who decided. And an order can reach the end unanswered. So if the checks and their order never change, write the four ifs. Reach for this when the order is something you need to change without editing any of them.

## 15. Thanks for Watching

That's chain of responsibility. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository — including the exercise I'd most recommend. Take the standard chain, move the payment link above the fraud link, run the demo, and watch a customer get told something different about the same order. If this helped, a like genuinely does help other people find it, and subscribe if you'd like the rest of the behavioural series — iterator is next. Thanks for watching, and I'll see you in the next one.
