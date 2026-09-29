# Routing Slip Pattern — Video Narration Script

## 1. Routing Slip

Hello, and welcome. This video explains the Routing Slip pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. With a routing slip, the steps a message needs are worked out once, when it arrives. The list is attached to the message. Each step does its work, and passes the message to the next step on the list. Think of the circulation slip clipped to a magazine in an office. Pass to Anna, then Ben, then Carl. Each person reads it, crosses their name off, and passes it on. Nobody needs to know the whole list. In this video, the domain is an online shop. Its orders need different steps: gift wrap for gifts, age checks for knives, customs for orders abroad. By the end, you will hear what a fixed pipeline wastes. How routing slips fix it. How to add a step. And what a slip cannot do.

## 2. The Scenario

Here is the scenario. The shop has six processing steps. Validate, age check, customs, charge, gift wrap, and pack. Most orders need only some of them. But every order went through all six, one after another.

## 3. Act One — One fixed pipeline

First demo: one fixed pipeline, for every order. Six steps. Validate, age check, customs, charge, gift wrap, and pack. Four orders go through all six. Twenty-four visits. Only fifteen did any work. A UK order needs no customs. A plain order needs no gift wrap. So every step starts by asking: does this even apply to me?

## 4. Act Two — Routing slips

Second demo: a routing slip. As each order enters, its route is worked out once, and attached to it. Order one is a plain UK order: validate, charge, pack. Order two is a gift: gift wrap is added. Order three is age restricted: an age check is added. Order four is going to France: customs is added.

## 5. Act Three — Steps pass it on

Third demo: each step does its job, and passes the order to the next name on the slip. Order two goes: validate, charge, gift wrap, pack. Fifteen visits in all. Every one does work. And no step knows which step comes after it.

## 6. Act Four — A new step

Fourth demo: a new step. Orders over five hundred pounds now need a fraud check. One rule is added, where the slips are written. Order four is worth six hundred and twenty pounds, so its slip gains a fraud check, before charge. Order one's slip is unchanged. No step was changed at all.

## 7. Act Five — The bill

Fifth demo: the bill. The route is fixed when the order sets off. Order five, a kitchen knife, fails its age check. The route stops there, with charge and pack still on the slip. It cannot choose a new route, such as: ask for ID, then carry on. That needs a process manager.

## 8. The Pattern

Let's name the pattern. When a message enters, write down the list of steps it needs. Attach the list to the message. That is its routing slip. Each step does its work, and passes the message to the next step on the slip. No step needs to know what comes after it.

## 9. Who Does What

Here is who does what. The routing slip class writes each order's slip, and runs its steps in turn. The order message carries its slip, and a record of where it has been. The steps each do one job. And the fixed pipeline is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Apache Camel has a routing slip step. Approval workflows often attach a list of approvers to a document. And offices have used circulation slips for as long as there have been offices.

## 11. When To Use It

So, when should you use it? When different messages need different, but predictable, sequences of steps. Keep the rules that write slips in one place. Keep the steps independent. And when the route must change, depending on what happens along the way, use a process manager instead.

## 12. Thanks for Watching

That's the Routing Slip pattern. If you remember one sentence, make it this one. Let each message carry its own route, and each step just pass it on. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a loyalty points step, for registered customers only. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
