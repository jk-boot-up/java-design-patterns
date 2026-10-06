# Strangler Fig Pattern — Video Narration Script

## 1. Strangler Fig

Hello, and welcome. This video explains the Strangler Fig pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. You replace an old system by growing the new one around it, one piece at a time. A router sits in front, and can send each piece to either the old system or the new. The name comes from a kind of fig tree that slowly grows around a host tree, until it replaces it. In our online store, the thing being replaced is the checkout. By the end, you will hear why a big rewrite fails on a Monday. How a router, and quiet side-by-side comparisons, let you move one piece at a time, on evidence. And the outcome nobody warns you about: the migration that stops halfway.

## 2. The Scenario

Here is the scenario. The old checkout is one large class. It handles pricing, stock, payment, and email. It works. But it is where every change is slow, and every incident starts. So the business wants it replaced. So here is the question. How do you replace something that must keep taking orders while you do it?

## 3. The Big-Bang Rewrite

First demo: the big rewrite. Build a new checkout beside the old one, and switch over. Twenty-six weeks of work. In all that time, the new code serves no real orders at all. So there is no feedback from real customers for half a year. Then a switch-over weekend. And on Monday, one of the four parts is faulty. Payment declines large orders. There is only one switch. So the only way back is to undo everything. All four parts go back, including the three that were fine.

## 4. An Analogy: The Strangler Fig

Here is the analogy. A strangler fig starts as a seed, high up in another tree. It sends roots down the trunk. And it grows around the host tree, a little at a time. For years, both trees are alive. And the old tree still does its job. One day, the fig is complete, and the old tree inside is gone. At no point was the forest left without a tree. That is the pattern, and the name.

## 5. A Router, And A Switch Per Capability

Second demo: a router, with a switch for each part. A router sits in front of the old checkout. Each part, pricing, stock, payment, and email, has its own switch. They all start on the old code. Pricing moves first. Now pricing uses the new code. The other three still use the old. An order goes through, and it succeeds. The customer noticed no switch-over. The checkout never stopped.

## 6. Shadow Reads

Third demo: quiet comparisons. Before pricing moves, it is run in shadow. The old code serves the customer. The new code is also asked, quietly, and the two answers are compared. Two hundred and one orders. They disagreed on twenty-nine. There were two causes. The old code rounds the tax on each line. The new code rounds it once, on the total. And the old code gives free delivery only above fifty pounds. The new code gives it from fifty pounds. Both are reasonable. But both differ from what customers have paid for years. And this was found before any customer paid a penny differently. The team makes the new code match the old one exactly. They compare again: no differences in two hundred and one orders. Now pricing can move.

## 7. One Capability Rolls Back

Fourth demo: the Monday, done differently. Pricing and payment now use the new code. Payment misbehaves on a large order, and the order fails. Flip one switch. Payment alone goes back to the old code. And the order succeeds. Pricing stays on the new code. A fault in one part is fixed by moving just that one part.

## 8. The Bill: Two Systems

Now the bill. First cost: two systems. Both are live for months, and both must be kept running. Every business rule that changes during that time must be changed twice. Once in the old code, and once in the new. There are two teams on call, and two release pipelines. That cost is paid every week, until the old system is gone.

## 9. The Bill: Two Truths

Fifth demo, and the second cost: data. Stock has moved to the new service. An order takes five of one product. The new service says three hundred and ninety-five are left. But the old stock table, which old reports and invoices still read, says four hundred. Two tables both claim to be the truth. Someone must decide which is right. And keep them in step, until the old system is gone.

## 10. The Failure That Actually Happens

Sixth demo: the failure that actually happens. The migration stalls. Two parts move, and then the budget goes elsewhere. Nobody decides to stop. It just stops. Here is a simple cost model. All on the old system costs a hundred a quarter. All on the new costs sixty. Running both adds a fixed thirty-five. So the stalled, half-moved state costs a hundred and fifteen a quarter. More than all old. More than all new. Two checkouts, forever, is worse than either end. And it is the most likely outcome. Nobody warns you.

## 11. The Verdict

So, here is the verdict. Use this pattern. It is how systems that must keep running get replaced. But treat the end date, and switching off the old system, as part of the migration. Not as a later job. A strangler fig you never finish is worse than the big rewrite. And worse than not starting at all.

## 12. How To Recognise It

How can you spot this pattern in a system someone else built? Look for a gateway that sends one path to an old service, and another to a new one. Look for a switch for each part, named something like: use new pricing. Look for two versions of one interface, a selector between them, and a ticket somewhere to delete one. And a folder called legacy that has been temporary for years.

## 13. What This Model Does Not Show

What this model does not show. Two real running systems, with a real network between the router and each one. Moving real data, rather than comparing two lists. And the human side: priorities, budgets, and people. That is where most migrations actually stall. The costs are assumptions, chosen to show a shape.

## 14. Where You Have Met This

Where have you met this before? In every migration that says: we are moving to the new platform, one team at a time. And in every version two of an A P I, running beside version one.

## 15. When This Is Too Much

So, when is this too much? For a system small enough to rewrite in a few weeks, the router and the switches cost more than they save.

## 16. Thanks for Watching

That's the Strangler Fig pattern. If you remember one sentence, make it this one. Move one piece at a time, on evidence, and finish, because two systems forever is worse than either one. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. In the cost model, change the cost of running both systems to ten. Then see whether stalling halfway is still worse than either end. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
