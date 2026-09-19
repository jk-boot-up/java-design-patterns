# Strangler Fig Pattern — Video Narration Script

## 1. Strangler Fig

Hello, and welcome. This video explains the Strangler Fig pattern, in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: replace a system by growing the new one around the old, one piece at a time, behind a router that can send each piece to either. This is the last project in the platform category, whose subject is the shape of a system as it changes over time. In our online store, the thing being replaced is the checkout. By the end you will see why the big rewrite fails on a Monday, how a router and shadow reads let you move a piece at a time on evidence, and the outcome that nobody warns you about: the migration that stalls half finished.

## 2. The Scenario

Here is the scenario. The legacy checkout is one large class. It does pricing, stock, payment, and email. It works. It is also where every change is slow, and every incident starts. So the business wants it replaced. The question: how do you replace something that must keep taking orders while you do it?

## 3. The Big-Bang Rewrite

The obvious answer is a rewrite. Build the new checkout beside the old one, and switch over. Twenty-six weeks of work, in parallel with production. In that time, the new code serves no real orders at all, so there is no feedback from real traffic for half a year. Then a cutover weekend. And on Monday, one of the four capabilities is faulty: payment declines large orders. There is one switch, so the only rollback is all of it. All four capabilities go back, including the three that were fine.

## 4. An Analogy: The Strangler Fig

An analogy. A strangler fig begins as a seed, high in a tree. It sends roots down the trunk, and grows around the host, a little at a time. For years, both are alive, and the old tree is still doing its job. One day the fig is complete, and the tree inside it is gone. At no point in all that time did the forest have no tree. That is the pattern, and the name.

## 5. A Router, And A Switch Per Capability

The pattern. Put a router in front of the legacy checkout. Every capability, pricing, stock, payment, email, has its own switch. They all start on legacy. Move pricing first. Now pricing is served by the new code, and the other three still by legacy. An order goes through, and it succeeds. The customer saw no cutover. The checkout never stopped.

## 6. Shadow Reads

Before pricing moves, shadow it. Legacy serves the customer. The new code is called as well, and the two answers are compared. Two hundred and one orders. They disagreed on twenty-nine. Two causes. Legacy rounds the V A T on each line. The new code rounds it once, on the total. And legacy gives free delivery only when the goods cost more than fifty pounds. The new code gives it from fifty pounds. Both are reasonable. Both differ from what customers have paid for years. Found before any customer paid a penny differently. The team decides to reproduce legacy exactly, and shadows again: zero differences in two hundred and one. Now pricing can move.

## 7. One Capability Rolls Back

Now the Monday, done differently. Pricing and payment are on the new code. Payment misbehaves on a large order, and the order fails. Flip one switch. Payment alone goes back to legacy, and the order succeeds. Pricing never moved back. A fault in one capability is answered by moving one capability.

## 8. The Bill: Two Systems

Now the bill. First, two systems are live for months, and both must be maintained. Every business rule that changes while both are live is changed twice: in legacy, and in the new code. There are two on-call rotas, two deployment pipelines. That is a cost, and it is paid every week until legacy is gone.

## 9. The Bill: Two Truths

Second cost. Data. Stock has moved to the new service, and an order takes five of one product. The new service says three hundred and ninety-five on hand. The legacy table, which its reports and its invoices still read, says four hundred. Two tables claim to be the truth. Someone must decide which, and keep them in step until legacy is gone.

## 10. The Failure That Actually Happens

And the failure that actually happens in the field. The migration stalls. Two capabilities move, and then the budget goes elsewhere. Nobody decides to stop. It just stops. Here is a cost model, and it is a model, stated as one. All legacy costs a hundred a quarter. All new costs sixty. While both are live, there is a fixed extra thirty-five for running two. The stalled state costs a hundred and fifteen a quarter. More than all legacy. More than all new. Two checkouts, forever, is worse than either endpoint. And it is the most likely outcome, and nobody warns you.

## 11. The Verdict

My verdict, plainly. Use it. It is how systems that must keep running get replaced. But treat the end date, and the decommissioning of legacy, as part of the migration, not a later job. A strangler you do not finish is worse than the big bang you should have avoided, and worse than not starting at all.

## 12. How To Recognise It

How do you recognise this in code you did not write? A gateway with routes, sending one path to an old service, and another to a new one. A feature flag for each capability, with a name like use new pricing. Two implementations of one interface, a selector between them, and a ticket, somewhere, to delete one. And a package called legacy that has been temporary for years.

## 13. What This Model Does Not Show

What this model does not show. Two real deployments, and a real network between the router and the systems. Moving real data, rather than comparing two maps. And the organisational part, priorities, budgets, and people, which is where most of these migrations actually stall. The costs are assumptions, chosen to show a shape.

## 14. Where You Have Met This

You have met this in every migration that says we are moving to the new platform, one team at a time. And in every slash A P I slash v two, running next to a slash v one.

## 15. When This Is Too Much

So when is it too much? For a system small enough to rewrite in a few weeks, the seam and the router cost more than they save.

## 16. Thanks for Watching

That's the Strangler Fig. If you take one sentence away, take this one: move one piece at a time, on evidence, and finish, because two systems forever is worse than either. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, change the both-live overhead in the cost model to ten, and see whether stalling stops being worse than the endpoints. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
